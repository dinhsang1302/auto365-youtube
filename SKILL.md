---
name: auto365-youtube
description: Biên tập và đăng video YouTube Auto365 qua trình duyệt tích hợp; tự đọc video, kiểm nguồn, nghiên cứu metadata, tạo thumbnail khi được giao và xác minh đúng revision sau lưu. Dùng cho job video cụ thể, không tự audit toàn kênh.
metadata:
  version: "1.0.4"
---

# Auto365 YouTube

Đọc [rules8](references/editorial-rules.md), [workflow](references/workflow.md) và [templates2](assets/templates/description-templates.json). [channel.example.json8](assets/templates/channel.example.json) là mẫu khởi tạo; nguồn chữ ký vận hành duy nhất là workspace/channel.json, nằm ngoài repo. Profile cụ thể của job quyết định đích kênh. Entrypoint và schema: [runtime](references/runtime.md).

Khi người dùng gọi skill, đưa link/file video và nói **“đăng đi”, “đăng clip này”** hoặc tương đương, nhận toàn bộ job: đọc/kiểm nguồn/nghiên cứu → tự chọn metadata → thumbnail bằng ImageGen sẵn có → upload nếu chưa có → **công khai** → readback/trả link. Kênh mặc định từ channel.json là Auto365 Review. Không đợi nhắc bước hoặc duyệt từng phần; chỉ hỏi thiếu thiết yếu, quyền truy cập hoặc login/OTP. Yêu cầu cụ thể mới nhất như prepare-only/riêng tư/lên lịch/giữ một trường thắng mặc định. Đây không là quyền cho dịch vụ ảnh trả phí khác.

Ghi cách hiểu đó bằng `init-job` vào job.action_request: mode/quyền/kênh/source/selection policy; sửa mô tả khóa revision/hash trước ghi. Quyền cũ không thắng giới hạn mới, prepare-only không ghi remote. Đọc checkpoint trước; reuse cùng hash và đúng ID, không audit/upload lại để sửa metadata hoặc áp clip test sang clip mới. Ví dụ lời gọi nằm trong [runtime](references/runtime.md).

Tìm auto365-writer/copywriting/content-strategy bằng catalog hiện tại hoặc `discover`, đọc SKILL.md khi dùng. Chỉ lấy kiểm nguồn/claim, văn phong/CTA, phân nhóm/playlist; không kéo chuẩn SEO website vào YouTube. Thiếu guidance/Gem gốc thì báo phạm vi và dùng rules tự chứa, không nhận đã đọc nguồn chưa có.

Workflow: Nhận video → Phân tích hình ảnh/âm thanh → Kiểm chứng thông tin → Nghiên cứu từ khóa → Viết nội dung SEO → Tạo thumbnail → Đăng video → Kiểm tra và trả link. Chỉ chạy các bước phù hợp phạm vi job; sửa chữ ký trên video có sẵn thì giữ nguyên phần còn lại.

## Biên tập

1. Tự đọc media/transcript/frame khi chưa có bằng chứng cùng hash. Rà xe/đời/phiên bản, model/SKU và lỗi ASR; giữ raw/corrections/coverage. Không bắt người dùng viết title/dán transcript, không giả xem toàn bộ.
2. Khóa facts/source/QA/timestamp: video đề cập khác nguồn hiện hành. Không bịa thông số/giá/bảo hành/kết quả/nhu cầu khách hoặc suy hiệu quả từ W/K. Giữ thương mại đầy đủ nội bộ.
3. Tự nghiên cứu YouTube/web mỗi video trước final; Analytics chỉ đúng ID/quyền. Lưu query/URL/ngày/origin/lý do/limits; phân biệt metric và đề xuất, không bịa volume/trend. Rà title/description/hashtag và **tags riêng Studio**, không đợi nhắc/ép số lượng. Search lỗi ghi giới hạn, tiếp tục dữ kiện đã kiểm.
4. Title tạo ba góc khi nội dung cho phép, chọn một/đếm ký tự thật; description-only giữ trường khác. Mô tả như người làm nghề: mở vào xe/model/điểm đáng xem, giải thích đủ vấn đề–tính năng–ý nghĩa–lựa chọn có nguồn, CTA ngắn. Gọn bỏ thừa/lặp, không bỏ chiều sâu; Shorts và video dài theo nội dung, templates không ép đủ mục/độ dài/FAQ. Không sáo rỗng, giọng báo cáo, nhồi từ khóa hoặc hứa top/AI citation.
5. narrative_sections có text/purpose/evidence, chỉ text xuất public; không truncate. **Không VAT** trong mô tả/CTA/bình luận đề xuất; giá sản phẩm không là giá hoàn thiện. Giá/bảo hành/link/chapters tùy nguồn/nội dung. Link đúng model/đích đã mở.
6. Timeline mốc thật, không chia đều/copy mẫu: 00:00,≥3mốc tăng, mỗi đoạn≥10s kể cả cuối; đặt TIMELINE CHI TIẾT trước chữ ký. Một chữ ký theo profile: ☎tư vấn đúng dịch vụ và phản ánh đúng số/thứ tự; không đổi theo website. Hashtag sát chủ đề; 6–10 chỉ gợi ý khi đủ liên quan. Comment chỉ là đề xuất nếu chưa có quyền.

## Browser, thumbnail và bàn giao

- Đọc [browser/thumbnail/recovery](references/browser-and-thumbnail.md) trước thao tác. Dùng trình duyệt tích hợp; so live Studio ID/quyền với profile/job trước ghi. Chỉ đi trường được giao, lưu before/intent/checkpoint; ID đã có bỏ upload. Login/OTP/CAPTCHA để người dùng. Playlist đã có; tạo mới/comment/connections/credit cần quyền riêng.
- ImageGen chỉ khi được giao: xem tham chiếu và frame thật, giữ xe/model, chữ Việt rõ16:9; không beam giả thành test hoặc dùng ảnh tiến độ làm thumbnail. Kiểm chữ/hình, lưu job; thiếu ảnh/đọc tham chiếu thì báo phần thiết yếu.
- Validate chính revision với metadata/review/text/hash cùng bản; tự kiểm tám mục và nguồn/giọng văn, xử lý vấn đề trọng yếu trước commit. Chờ Save/processing/checks, reload readback nguyên text đã chốt và một chữ ký; so các trường ngoài scope. Publish/schedule kiểm thêm ID/trạng thái/lịch/trang xem phù hợp. Lưu revision/hash/URL/thời điểm/ảnh; chưa rõ kết quả thì kiểm Studio trước retry, không upload/đăng lại.
- Bàn giao nội dung và giới hạn, Đạt/Cần sửa/Chưa xác minh có lý do; thao tác thật kèm URL/trạng thái/ảnh. Không tự chấm hiệu quả hoặc nhận đã kiểm mọi nhánh remote. [Ví dụ tổng hợp](assets/examples/brief.example.json) chỉ kiểm cấu trúc, không là dữ kiện/metadata để đăng; phạm vi ở runtime.
