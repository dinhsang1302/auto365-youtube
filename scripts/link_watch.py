#!/usr/bin/env python3
"""Theo dõi bài link xe trên auto365.vn cho video YouTube đã đăng khi chưa có bài đúng xe.

Luật (anh Việt chốt 20/11/2026): mô tả ưu tiên bài đúng xe + dịch vụ; chưa có thì lấy bài
xe khác cùng dịch vụ; không có nữa thì bỏ link xe. Hai trường hợp sau → thêm video vào danh
sách theo dõi, quét lại sitemap mỗi 7 ngày, báo kết quả mỗi lần quét; có bài đúng xe thì báo
và ngừng theo dõi video đó.

  link_watch.py add --video URL --title "..." --car fortuner [--car toyota-fortuner] \
                    --service phim-cach-nhiet [--service ppf] [--fallback URL]
  link_watch.py scan [--force]        # chạy hằng ngày bởi launchd, chỉ quét mục đến hạn
  link_watch.py list
Danh sách: $AUTO365_LINK_WATCH hoặc ~/Movies/Edit365/work/yt_link_watch/watchlist.json
"""
import argparse, datetime as dt, json, os, re, subprocess

LIST = os.environ.get("AUTO365_LINK_WATCH",
                      os.path.expanduser("~/Movies/Edit365/work/yt_link_watch/watchlist.json"))
LOG = os.path.join(os.path.dirname(LIST), "scan_log.md")
SITEMAP = "https://auto365.vn/sitemap.xml"
DAYS = 7


def load():
    try:
        return json.load(open(LIST, encoding="utf-8"))
    except FileNotFoundError:
        return []


def save(items):
    os.makedirs(os.path.dirname(LIST), exist_ok=True)
    json.dump(items, open(LIST, "w", encoding="utf-8"), ensure_ascii=False, indent=2)


def fetch(url):
    # curl dùng kho chứng chỉ hệ thống (python.org trên macOS thường thiếu chứng chỉ SSL)
    r = subprocess.run(["curl", "-fsSL", "--max-time", "60", "-A", "auto365-link-watch/1.0", url],
                       capture_output=True, check=True)
    return r.stdout.decode("utf-8", "replace")


def all_urls():
    locs = re.findall(r"<loc>\s*([^<]+?)\s*</loc>", fetch(SITEMAP))
    out = []
    for u in locs:
        if u.endswith(".xml"):
            out += re.findall(r"<loc>\s*([^<]+?)\s*</loc>", fetch(u))
        else:
            out.append(u)
    return out


def match(urls, item):
    hits = []
    for u in urls:
        slug = u.lower().rstrip("/").rsplit("/", 1)[-1]
        if any(c in slug for c in item["car"]) and any(s in slug for s in item["service"]):
            hits.append(u)
    return hits


def notify(msg):
    print(msg)
    try:
        subprocess.run(["osascript", "-e", f'display notification {json.dumps(msg, ensure_ascii=False)} with title "Auto365 link xe"'],
                       timeout=10)
    except Exception:
        pass


def log(lines):
    os.makedirs(os.path.dirname(LOG), exist_ok=True)
    with open(LOG, "a", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def cmd_add(a):
    items = load()
    today = dt.date.today()
    items.append({"video": a.video, "title": a.title, "car": [c.lower() for c in a.car],
                  "service": [s.lower() for s in a.service], "fallback": a.fallback or "",
                  "added": today.isoformat(), "next_scan": (today + dt.timedelta(days=DAYS)).isoformat(),
                  "status": "watching", "found": []})
    save(items)
    print("Đã thêm, quét lại ngày", items[-1]["next_scan"])


def cmd_scan(a):
    items = load()
    today = dt.date.today()
    due = [i for i in items if i["status"] == "watching" and (a.force or i["next_scan"] <= today.isoformat())]
    if not due:
        print("Không có mục đến hạn.")
        return
    urls = all_urls()
    lines = [f"\n## Quét {today.isoformat()} ({len(urls)} URL sitemap)"]
    for i in due:
        hits = match(urls, i)
        if hits:
            i["status"], i["found"] = "found", hits
            m = f"ĐÃ CÓ bài cho {i['title']}: {hits[0]} → cập nhật link xe trong mô tả {i['video']}"
        else:
            i["next_scan"] = (today + dt.timedelta(days=DAYS)).isoformat()
            m = f"Chưa có bài cho {i['title']} ({i['video']}); quét lại {i['next_scan']}"
        lines.append("- " + m)
        notify(m)
    save(items)
    log(lines)


def cmd_list(a):
    for i in load():
        print(i["status"], i["next_scan"], i["title"], i["video"], *i["found"])


p = argparse.ArgumentParser()
sp = p.add_subparsers(dest="cmd", required=True)
x = sp.add_parser("add")
x.add_argument("--video", required=True); x.add_argument("--title", required=True)
x.add_argument("--car", action="append", required=True); x.add_argument("--service", action="append", required=True)
x.add_argument("--fallback")
x.set_defaults(f=cmd_add)
x = sp.add_parser("scan"); x.add_argument("--force", action="store_true"); x.set_defaults(f=cmd_scan)
sp.add_parser("list").set_defaults(f=cmd_list)
a = p.parse_args(); a.f(a)
