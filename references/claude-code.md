# Chạy skill trên Claude Code

Người dùng chốt **18/11/2026**: cùng một bộ skill chạy được trên **Codex** và **Claude Code**. Luật biên tập, nguồn, thumbnail, quyền đăng
giữ nguyên; chỉ đổi **công cụ** theo nền tảng đang chạy. Trên Codex mọi thứ giữ như cũ (IAB + ImageGen built-in).

## Nhận nền tảng (đầu mỗi job)
- Có công cụ `image_gen.imagegen` / trình duyệt `iab` của Codex → **nền tảng Codex**, làm theo tài liệu gốc.
- Có công cụ Claude Code (Bash/Read/Edit, Skill, `mcp__claude-in-chrome__*`), skill nằm trong `~/.claude/skills/` hoặc `.claude/skills/` → **nền tảng Claude Code**, áp các ánh xạ dưới đây.
- Ghi `runtime_platform` (`codex` | `claude_code`) vào `job.json` → `action_request` và vào `thumbnail-review.json`.

## Ánh xạ công cụ
| Việc | Codex | Claude Code |
|---|---|---|
| Script local (discover, init-job, prepare, render, validate, `person_frames.py`) | Python + FFmpeg | **Y hệt** (Bash) |
| Xem frame/contact sheet/thumbnail | xem ảnh | công cụ Read đọc ảnh |
| Tạo/sửa thumbnail | `image_gen.imagegen` built-in | **ImageGen của Codex qua CLI** `codex exec` (mục dưới) |
| Web, YouTube Studio, upload, readback | Codex In-app Browser (`iab`) | **Claude in Chrome** (`mcp__claude-in-chrome__*`), đọc skill `claude-in-chrome` trước |
| Agent phụ | agent Codex | agent Claude Code (Agent tool), cùng luật |

## Thumbnail trên Claude Code: ImageGen qua Codex CLI
Luật "ImageGen tạo toàn artwork" giữ nguyên — Claude Code **không** tự vẽ/ghép bằng Pillow/HTML. Gọi Codex (đã cài, đã đăng nhập) chạy trong
thư mục thumbnail của job, đưa mọi reference bằng `-i` (đặt **trước** `--`, nếu không nó nuốt prompt):

```sh
cd JOB/thumbnail/rN && codex exec --skip-git-repo-check -s workspace-write \
  -i ref_nguoi.jpg -i ref_xe.jpg -i ref_san_pham.jpg -i SKILL_DIR/assets/brand/auto365-white.png \
  -- "Use the image generation tool to create ONE complete 16:9 YouTube thumbnail (1280x720 or larger) ... \
      Save as thumb_rN.png in the current directory." < /dev/null
```
- Prompt tiếng Anh, nêu vai trò từng ảnh (người thật của clip — giữ đúng mặt/đồng phục; xe đúng model; sản phẩm thật; logo gốc giữ nguyên),
  chuỗi chữ tiếng Việt chính xác, bố cục theo [thumbnail có người](person-thumbnail.md) + [packaging-style](packaging-style.md).
- Mỗi ảnh ~1–2 phút. Sửa = gọi lại với `-i thumb_rN.png` + yêu cầu sửa, lưu `thumb_rN+1.png` (revision mới, giữ bản cũ).
- Ghi vào revision: lệnh/prompt cuối, danh sách `-i` + hash, file ra + hash, `generation_method = "imagegen_via_codex_cli"`.
- Không có `codex` hoặc chưa đăng nhập → báo chặn đúng bước ("cần cài/đăng nhập Codex CLI để tạo thumbnail"), **không fallback** sang code
  hay dịch vụ ảnh khác. Phần metadata/upload vẫn làm tiếp nếu được giao; thumbnail để trạng thái chờ.
- Kiểm ảnh ra bằng Read ở bản đầy đủ và bản 320px như [cổng chất lượng](thumbnail-quality-gate.md).

## Trình duyệt trên Claude Code
- Thay "chỉ IAB" bằng **chỉ Claude in Chrome** (trình duyệt thật của người dùng, đã đăng nhập YouTube). Vẫn cấm Playwright/Puppeteer/Selenium,
  `open <URL>`, `webbrowser.open`, phiên CDP riêng, endpoint nội bộ YouTube/cookie. Mở tab mới, không dùng tab người dùng đang làm.
- Login/OTP/CAPTCHA để người dùng tự làm. Xác minh đúng kênh (channel ID) trước khi ghi.
- Upload file (video, thumbnail): dùng công cụ `file_upload`/`upload_image` của Claude in Chrome; không có thì báo chặn đúng bước, không nhận đã upload.
- Không bấm nút gây hộp thoại alert/confirm của trình duyệt; nếu lỡ thì báo người dùng tự đóng.
- Link xem video vẫn theo luật 19/10/2026: không mở link CDN/videoplayback, không tải media từ link.
- Chưa bật Claude in Chrome → làm phần local (đọc nguồn, metadata, thumbnail) rồi báo người dùng bật tiện ích để đăng.

## Cài trên Claude Code
```sh
git clone https://github.com/dinhsang1302/auto365-youtube.git ~/.claude/skills/auto365-youtube
```
Windows: `git clone https://github.com/dinhsang1302/auto365-youtube.git "$env:USERPROFILE\.claude\skills\auto365-youtube"`.
Cần thêm: Python 3.12, FFmpeg, `pip install -r requirements-media.txt` (đọc media mới), Codex CLI đã đăng nhập (thumbnail),
tiện ích Claude in Chrome (đăng/sửa Studio). Workspace job (`channel.json`…) như hướng dẫn chung trong README.
