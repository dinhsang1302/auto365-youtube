#!/usr/bin/env python3
"""Dò phân đoạn CÓ NGƯỜI trong video và trích frame ứng viên làm reference thumbnail (người dẫn/kỹ thuật viên).

Chỉ là công cụ PHÂN TÍCH + TRÍCH FRAME (được phép theo imagegen-workflow.md): không thiết kế, không ghép ảnh.
Thumbnail vẫn do ImageGen tạo toàn artwork từ các frame này + frame xe + frame sản phẩm.

Cách chấm mỗi frame (lấy mẫu 2 frame/giây, mặc định):
  - Nhận diện mặt bằng YuNet (assets/models/face_detection_yunet_2023mar.onnx, OpenCV FaceDetectorYN).
  - Điểm = độ tin cậy × cỡ mặt (mặt lớn, gần máy) × độ nét (Laplacian vùng mặt) × nhìn thẳng (2 mắt cân quanh mũi)
           × mặt không sát mép khung; trừ điểm frame quá tối/cháy sáng.
  - Gom các frame có người liền nhau thành PHÂN ĐOẠN có người (khoảng hở ≤ 1,5 s vẫn tính một đoạn).
  - Chọn top-N frame cách nhau ≥ 3 s (đa dạng tư thế/cử chỉ), xuất JPEG gốc độ phân giải nguồn.

Dùng:
  python scripts/person_frames.py <video> <thư_mục_ra> [--fps 2] [--top 8] [--min-face 0.06]
Ra:
  <ra>/person_frames.json   phân đoạn có người + danh sách frame ứng viên (timestamp, điểm, hộp mặt, số người)
  <ra>/person_<giây>.jpg     frame ứng viên ở độ phân giải gốc
  <ra>/person_contact.jpg    contact sheet các ứng viên (mở xem trước khi chọn)
Không có người (không phân đoạn nào) → in "KHÔNG CÓ NGƯỜI" và thoát mã 2: thumbnail theo bố cục xe + sản phẩm.
Cần: opencv-python-headless ≥ 4.8 (FaceDetectorYN), numpy, Pillow, ffmpeg/ffprobe trong PATH.
"""
import argparse, json, math, os, subprocess, sys
from pathlib import Path

import numpy as np

try:
    import cv2
except ImportError:
    sys.exit("Thiếu OpenCV: pip install opencv-python-headless")
from PIL import Image

HERE = Path(__file__).resolve().parent
MODEL = HERE.parent / "assets/models/face_detection_yunet_2023mar.onnx"


def probe(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                        "stream=width,height:stream_side_data=rotation:format=duration", "-of", "json", str(path)],
                       capture_output=True, text=True, encoding="utf-8")
    j = json.loads(r.stdout); st = j["streams"][0]
    rot = next((abs(int(sd.get("rotation", 0))) for sd in st.get("side_data_list", []) if "rotation" in sd), 0)
    w, h = (st["height"], st["width"]) if rot == 90 else (st["width"], st["height"])
    return w, h, float(j["format"]["duration"])


def frames(path, fps, aw):
    """Đọc frame đã thu nhỏ (bề ngang aw) để phân tích nhanh; ffmpeg tự xoay theo metadata."""
    w, h, dur = probe(path); ah = int(round(h * aw / w / 2) * 2)
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-threads", "2", "-i", str(path), "-vf", f"fps={fps},scale={aw}:{ah}",
                          "-f", "rawvideo", "-pix_fmt", "bgr24", "-"], stdout=subprocess.PIPE)
    n = aw * ah * 3; i = 0
    while True:
        b = p.stdout.read(n)
        if len(b) < n: break
        yield i / fps, np.frombuffer(b, np.uint8).reshape(ah, aw, 3)
        i += 1
    p.wait()


def score_faces(img, det, min_face):
    h, w = img.shape[:2]; det.setInputSize((w, h))
    _, faces = det.detect(img)
    if faces is None: return 0.0, None, 0
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    best, box, n = 0.0, None, 0
    for f in faces:
        x, y, fw, fh, conf = *f[:4], f[14]
        if fh / h < min_face: continue                      # mặt quá nhỏ (người ở xa) không dùng làm hero
        n += 1
        x0, y0, x1, y1 = max(int(x), 0), max(int(y), 0), min(int(x + fw), w), min(int(y + fh), h)
        roi = gray[y0:y1, x0:x1]
        if roi.size == 0: continue
        sharp = min(cv2.Laplacian(roi, cv2.CV_64F).var() / 300.0, 1.0)
        (rex, rey), (lex, ley), (nx, ny) = f[4:6], f[6:8], f[8:10]
        d1, d2 = abs(nx - rex), abs(lex - nx)
        frontal = 1 - min(abs(d1 - d2) / max(d1 + d2, 1e-6), 1)   # 1 = nhìn thẳng máy
        cx, cy = (x + fw / 2) / w, (y + fh / 2) / h
        edge = 1.0 if 0.08 < cx < 0.92 and 0.12 < cy < 0.85 else 0.5
        lum = roi.mean() / 255; expo = 1.0 if 0.18 < lum < 0.85 else 0.5
        s = float(conf) * math.sqrt(fh / h) * (0.4 + 0.6 * sharp) * (0.5 + 0.5 * frontal) * edge * expo
        if s > best: best, box = s, [round(float(v), 4) for v in (x0 / w, y0 / h, x1 / w, y1 / h)]
    return float(best), box, n


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("video"); ap.add_argument("out")
    ap.add_argument("--fps", type=float, default=2); ap.add_argument("--top", type=int, default=8)
    ap.add_argument("--min-face", type=float, default=0.06, help="chiều cao mặt tối thiểu / chiều cao khung")
    a = ap.parse_args(); out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    if not MODEL.exists(): sys.exit(f"Thiếu model {MODEL}")
    det = cv2.FaceDetectorYN.create(str(MODEL), "", (640, 360), 0.6, 0.3, 5000)
    rows = []
    for t, img in frames(a.video, a.fps, 640):
        s, box, n = score_faces(img, det, a.min_face)
        rows.append((t, s, box, n))
    have = [r for r in rows if r[1] > 0]
    segs = []
    for t, s, box, n in have:
        if segs and t - segs[-1][1] <= 1.5: segs[-1][1] = t
        else: segs.append([t, t])
    segs = [dict(start=round(a0, 2), end=round(b0 + 1 / a.fps, 2)) for a0, b0 in segs]
    if not have:
        json.dump(dict(video=str(a.video), has_person=False, segments=[], candidates=[]),
                  open(out / "person_frames.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print("KHÔNG CÓ NGƯỜI trong video (theo nhận diện mặt) → thumbnail bố cục xe + sản phẩm."); sys.exit(2)
    pick = []
    for t, s, box, n in sorted(have, key=lambda r: -r[1]):
        if all(abs(t - p[0]) >= 3 for p in pick): pick.append((t, s, box, n))
        if len(pick) >= a.top: break
    pick.sort()
    cands = []
    for t, s, box, n in pick:
        f = out / f"person_{t:07.2f}.jpg"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.3f}", "-i", str(a.video), "-frames:v", "1", "-q:v", "2", str(f)], check=True)
        cands.append(dict(t=round(t, 2), score=round(s, 4), face_box=box, faces=n, file=f.name))
    thumbs = [Image.open(out / c["file"]).convert("RGB") for c in cands]
    tw = 480; th = int(thumbs[0].height * tw / thumbs[0].width); cols = 4; rws = math.ceil(len(thumbs) / cols)
    sheet = Image.new("RGB", (cols * tw, rws * th), (20, 20, 20))
    for i, im in enumerate(thumbs): sheet.paste(im.resize((tw, th)), ((i % cols) * tw, (i // cols) * th))
    sheet.save(out / "person_contact.jpg", quality=88)
    total = sum(s["end"] - s["start"] for s in segs)
    json.dump(dict(video=str(a.video), has_person=True, person_seconds=round(total, 1), segments=segs, candidates=cands),
              open(out / "person_frames.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"CÓ NGƯỜI: {len(segs)} phân đoạn, ~{total:.0f}s. Ứng viên: " + ", ".join(f"{c['t']}s" for c in cands))
    print(f"Xem {out / 'person_contact.jpg'} rồi chọn frame mặt rõ, mắt mở, cử chỉ hướng về xe/sản phẩm.")


if __name__ == "__main__":
    main()
