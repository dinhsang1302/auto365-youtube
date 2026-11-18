# Thumbnail Auto365: toàn bộ artwork bằng ImageGen

**Ngoại lệ phạm vi Shorts — người dùng chốt 30/10/2026:** mặc định giữ ảnh đại diện từ video, không tạo thumbnail riêng và không gọi ImageGen. Không dùng tài liệu này để bắt buộc thiết kế thumbnail cho một job Shorts đăng thông thường. Chỉ áp dụng quy trình/cổng thiết kế khi người dùng yêu cầu cụ thể tạo hoặc sửa thumbnail Shorts. Video dài và các thumbnail được giao vẫn theo ImageGen.

Người dùng chốt23/10/2026 cho mọi thumbnail của dự án. Áp dụng cả tạo mới và chỉnh sửa; thay hướng cũ cho phép ImageGen tạo nền rồi hoàn thiện chữ/logo/xe/cảnh sáng bằng script. Chỉ yêu cầu rõ ràng mới hơn của người dùng mới đổi phương pháp. Giữ nguyên các revision lịch sử.

## Trình tự bắt buộc

**VIDEO GỐC → TRÍCH FRAME → IMAGEGEN SKILL → KIỂM TRA → XUẤT THUMBNAIL → CẬP NHẬT YOUTUBE**

1. Đọc clip, transcript và checkpoint đúng video/hash; không chạy lại những bước nguồn đã xác minh còn phù hợp.
2. Trích frame đẹp, rõ bằng FFmpeg; chọn xe, sản phẩm/cảnh lắp và tất cả cảnh thử sáng liên quan. **Clip có người:** chạy trước `scripts/person_frames.py <video> <job>/thumbnail/person`, chọn frame người từ phân đoạn có người (mắt mở, nhìn máy, cử chỉ hướng về xe/sản phẩm) và đưa vào ImageGen cùng frame xe + sản phẩm theo [thumbnail có người](person-thumbnail.md). Xác minh model, nhãn/nhiệt màu/timestamp; mở xem từng ảnh reference.
3. Đọc `imagegen/SKILL.md` từ catalog hiện hành và thực sự gọi công cụ `image_gen.imagegen` built-in. Không chỉ đọc skill hay viết prompt. Đưa toàn bộ reference cần thiết, logo gốc và chuỗi chữ chính xác vào lời gọi; ghi rõ vai trò từng ảnh và các chi tiết phải giữ.
4. ImageGen trực tiếp tạo **một artwork hoàn chỉnh**: xe/sản phẩm, không gian, typography, logo và cụm so sánh ánh sáng. Không yêu cầu chỉ một nền rồi tự dựng phần còn lại.
5. Mở chính đầu ra để kiểm nội dung/nhận diện, dấu tiếng Việt, số/model, bố cục, phối ánh sáng và khác biệt beam theo nguồn. Sai hoặc chưa đạt thì dùng ImageGen chỉnh trên chính bản đó cùng reference; không vá bằng code. Thiếu nguồn thì bổ sung nguồn, không bịa hình/kết quả.
6. Sao chép đầu ra trực tiếp vào job, giữ file gốc; chỉ chuyển định dạng/kích thước để xuất16:9≥1280×720. Mở JPEG cuối và preview320px sinh từ JPEG này; chốt revision/hash sau kiểm.
7. Cập nhật YouTube bằng IAB trong đúng phạm vi được giao. Xác minh đúng video/kênh; với thumbnail-only, giữ nguyên title/description/tags/lịch/kiếm tiền và các thiết lập khác. Save hoàn tất, reload, đọc lại và chụp bằng chứng thumbnail mới. Không đăng/gửi nhóm khi không có quyền.

## Công cụ được phép và bị cấm

- Code/FFmpeg được dùng để trích frame, phân tích video, kiểm kích thước/hash/ảnh, chuyển định dạng/kích thước và hỗ trợ upload.
- Không dùng Pillow, OpenCV, SVG, HTML/CSS, Python, Remotion hoặc `render_integrated.py`/script tương tự để thiết kế thumbnail, tách xe dán nền, ghép beam, chèn chữ/logo, vẽ ánh sáng hay giả lập đầu ra ImageGen.
- Không có ngoại lệ mặc định “native finishing”: chữ, logo và beam cũng phải có trong artwork đầu ra trực tiếp của ImageGen. Cung cấp asset nguồn làm reference và sửa bằng ImageGen khi sai.
- ImageGen không khả dụng: báo đúng bước chặn. Không âm thầm chuyển sang collage code hoặc API/dịch vụ khác. CLI/API chỉ theo điều kiện của skill và chỉ thị rõ của người dùng.

## Phong cách và trung thực nguồn

**PREMIUM AUTOMOTIVE ADVERTISING ARTWORK:** đỏ–đen–trắng, cinematic lighting, realistic reflections, typography mạnh có chiều sâu, xe/sản phẩm lớn nhưng tự nhiên, các thành phần hòa cùng key visual, tương phản có kiểm soát. Không sticker/cutout lộ, lưới ảnh rời hoặc collage cơ bản. CTR là mục tiêu thị giác, không số liệu đã đo hay lời bảo đảm.

Reference phải là ảnh thật đã xác minh trong clip. Giữ nhận diện xe/model và sự khác biệt về nhiệt màu/cường độ camera ghi nhận; không recolour một beam thành nhiều mức, khuếch đại hiệu năng hoặc dùng gradient thay kết quả nguồn. Đối chiếu từng view sau khi gen. Artwork ImageGen theo reference không đồng nghĩa file ảnh gốc giữ nguyên pixel hoặc phép đo thực tế; không nhận là ảnh trích clip nguyên bản. Nhãn nguồn/loại minh họa phải rõ khi cần, không bịa thông số hoặc trải nghiệm thực.

## Bằng chứng và bàn giao

Lưu vào revision: skill/công cụ thực dùng, prompt cuối, danh sách reference+hash+timestamp/vai trò, đường dẫn+hash **đầu ra trực tiếp ImageGen**, bản sao trong job, chuỗi chuyển định dạng sang JPEG/preview, nhận xét thực trên đúng JPEG/hash. Không dùng báo cáo Python render hoặc prompt thay bằng chứng lời gọi tạo ảnh thực sự.

Báo ngắn gọn: skill nào; đã gọi công cụ hay chưa; file trực tiếp nào; đã cập nhật đúng video và reload xác minh chưa; workflow được lưu ở đâu. Mọi giới hạn còn lại phải nêu đúng phạm vi, không dùng kiểm kỹ thuật để thay kiểm thẩm mỹ hoặc nguồn.
