# Chỉ dùng trình duyệt tích hợp Codex

Người dùng chốt ngày 16/10/2026: “ko tự chạy trên trình duyệt local, chỉ chạy trên trình duyệt của codex thôi”.

- Mọi thao tác web, nghiên cứu, đăng nhập, YouTube Studio, upload, đọc lại kết quả và xem thử HTML/thumbnail đều dùng Codex In-app Browser (`iab`) qua công cụ browser của Codex. Quy tắc áp dụng cả agent chính và agent phụ.
- Không tự mở Chrome/Edge/trình duyệt mặc định ngoài app; không dùng `Start-Process <URL>`, `webbrowser.open`, lệnh `start/open`, Playwright/Puppeteer/Selenium hoặc phiên browser/CDP riêng để thay trình duyệt Codex. Nếu IAB không hỗ trợ một bước, giữ trạng thái công việc và báo đúng bước chặn; không tự chuyển trình duyệt.
- Địa chỉ `localhost`/`127.0.0.1` chỉ là đích của trang xem thử. Nếu cần mở trang đó, vẫn mở trong IAB; URL local không cho phép khởi chạy trình duyệt riêng. Tạo tab kiểm tra ở chế độ ẩn khi công cụ hỗ trợ, không tự đưa trang thử lên trước người dùng; đóng tab thử sau khi kiểm tra. Chỉ đưa bản cần xem/duyệt ra khi có mục đích bàn giao rõ.
- Remotion/FFmpeg vẫn được chạy như công cụ render file offline đã được giao. Chromium nội bộ do Remotion dùng để encode/still là một phần của renderer, không được tái sử dụng để duyệt web, điều khiển Studio hoặc chụp trang HTML thay IAB.
- Khi giao việc, nhắc rõ `browser_surface = codex_iab_only`; không cho agent phụ tự mở trình duyệt hoặc đổi công cụ khi gặp lỗi. Quy tắc này không thay đổi quyền đăng/gửi tin hay các cửa duyệt nội dung và bố cục.

## Link xem video — người dùng chốt 19/10/2026

- Xem video bằng link trang thông thường `youtube.com/watch?v=...`, `youtu.be/...` hoặc trang YouTube Studio trong IAB. Không mở link tải media trực tiếp dài như `*.googlevideo.com/videoplayback`, `*.c.youtube.com/videoplayback` hoặc URL CDN có tham số ký/token như ảnh người dùng gửi. Không dùng `downloadMedia` hay nút Tải xuống Studio để sinh yêu cầu tải CDN trong job dùng link video.
- Ưu tiên transcript và xem/tua clip trực tiếp trong trình phát; dùng frame quan sát trên trình duyệt hoặc tư liệu local sẵn có đã xác minh. Không trích URL stream từ player, không chuyển qua shell/API/browser khác để tải. Khi tải bị từ chối, giữ giới hạn đó và tiếp tục phần việc an toàn không cần tải; chỉ hỏi nếu thiếu tư liệu thiết yếu thực sự chặn kết quả.
