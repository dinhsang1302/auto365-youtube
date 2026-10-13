# Trình duyệt tích hợp, thumbnail và phục hồi

Đọc [workflow máy đọc](browser-workflow.json) cùng policy8. Dùng API browser tích hợp được môi trường cung cấp và tài liệu hiện hành; không dùng endpoint nội bộ YouTube/cookie hoặc một browser khác để thay thế. Nếu thiếu khả năng/filechooser, báo chính xác bước chặn; không nhận đã upload.

## Thumbnail từ tư liệu thật

1. Tìm ảnh đúng video trong nguồn. Nhiều ảnh không phân biệt được hoặc thiếu ảnh thì hỏi phần thiết yếu; quyền chọn đại ảnh của job test không áp video khác. Ảnh tiến độ/yêu cầu không tự là thumbnail.
2. Khi người dùng giao ImageGen: đọc skill/tool ImageGen đang có; xem thumbnail tham chiếu thật, nêu nếu không đọc được. Chọn frame nét thấy rõ xe/đèn/chi tiết hợp title. Đưa cả frame thật và ảnh tham chiếu vào yêu cầu tạo.
3. Học cách bố cục/màu/chữ/nổi chủ thể, thay bằng đúng xe và model hiện tại. Chữ Việt ngắn/lớn,16:9. Không sao chép xe/sản phẩm/giá/thông số của mẫu, không tạo chùm sáng giả như kết quả test thật.
4. Kiểm chữ/model/hình dáng/scope; lưu output vào job, nếu sửa thì sửa trên ảnh đã tạo. Không gọi dịch vụ ảnh trả phí khác hoặc tiêu credit chưa có quyền. Khai báo nội dung thay đổi theo hình/video thực và câu hỏi Studio; không mặc định mọi ảnh hỗ trợ thumbnail có cùng khai báo.

## Preflight và commit

- So đúng live channel ID và quyền hiện tại với profile + job. Config/Analytics snapshot không chứng minh đang đăng nhập đúng kênh. Login/OTP/CAPTCHA để người dùng làm, không lưu secrets. Không đọc Analytics kênh test/vidIQ khác để kết luận về kênh đích; không tự đổi kết nối.
- Kiểm nhật ký và Nội dung đúng kênh, gồm nháp/private/unlisted/scheduled/public, Video/Shorts theo phạm vi cần thiết. SHA xác định file local; Studio không lộ hash gốc. Nếu video ngoài nhật ký, tên file/thời lượng/frame/chủ đề là tín hiệu, không chứng minh byte identity. Nghi trùng chưa kết luận được thì không upload tiếp; hỏi quyết định cần thiết.
- Có đúng video ID thì dùng lại và chỉ đi trường được giao. Capture title/description/tags/thumbnail/playlist/audience/disclosures/visibility trước sửa. Đọc default-description và hợp nhất một chữ ký; block cũ khác mẫu cần rà, không xóa bằng heuristic. Không đổi title/thumb/tags để sửa description.
- Upload mới khi có quyền: ghi UPLOAD_INTENT trước chọn file; dùng filechooser API đúng đường dẫn, ghi ID ngay khi có. Chọn audience/disclosures theo nội dung thật, playlist phù hợp đã có; tạo mới/comment/connections/paidservice cần quyền riêng.
- Validate đúng revision và hash, tự kiểm nguồn/semantic tám mục. Quyền cụ thể đã được giao thì tiếp tục sau kiểm, không hỏi lại; chưa có quyền thì bàn giao local. Ghi COMMIT_INTENT hoặc DESCRIPTION_SAVE_INTENT trước nút cuối. Chờ upload/processing/checks, xử lý vấn đề trọng yếu trước publish/schedule. Với schedule, ghi giờ+timezone từ yêu cầu/phiên và đối chiếu giờ hiển thị Studio, không đoán từ timezone máy thực thi.

## Readback và retry

- Sau Save, chờ thông báo đã lưu/nút Save disabled; reload đọc lại. So nguyên text đã chốt: chỉ chuẩn hóa CRLF/LF và newline cuối, không bỏ ☎ hoặc thay lời. Kiểm một chữ ký và ba tuyến hotline đúng profile, đúng thứ tự. So các trường ngoài scope với before; thumbnail có thể chuẩn hóa bỏ tham số cache nhưng giữ asset/version.
- Sau publish/schedule, mở Studio và trang xem khi phù hợp, kiểm ID/kênh/trạng thái/lịch/title/description/thumb/tags theo phạm vi. Chỉ ghi VERIFIED_* khi có bằng chứng. Lưu URL/revision/hash/thời điểm/snapshot/ảnh và embed ảnh xác minh khi bàn giao thao tác thật.
- Nếu timeout/mất kết nối/lỗi save hoặc commit chưa rõ: ghi UNCERTAIN + URL/ID/bước/error/ảnh, đọc kết quả hiện có trước retry. Không bấm publish/upload lại khi chưa rõ. Có ID thì mở chính ID đó, thiếu ID thì kiểm danh sách kênh. Không hứa exactly-once.

Kiểm local/skill không tương đương kiểm mọi nhánh browser. Lịch sử có private-upload/publish/description-readback trên các job cụ thể; scheduling, recovery mất kết nối và phiên/quyền mới phải kiểm khi thực sự được giao. Không tự chạy thử trên kênh thật để hoàn tất kiểm skill.
