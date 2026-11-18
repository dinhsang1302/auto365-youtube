---

name: auto365-youtube

description: Biên tập và đăng video YouTube Auto365 qua trình duyệt tích hợp; tự đọc video, kiểm nguồn, nghiên cứu metadata, tạo thumbnail khi được giao và xác minh đúng revision sau lưu. Dùng cho job video cụ thể, không tự audit toàn kênh.

metadata:

  version: "1.0.17"

---



# Auto365 YouTube

**Thumbnail clip có người — chốt 18/11/2026:** clip có người (người dẫn/kỹ thuật viên) thì chạy `scripts/person_frames.py` chọn phân đoạn có người, thumbnail **bắt buộc kết hợp người + xe + sản phẩm**, không chỉ xe; người phải đúng người thật trong clip. Xem [thumbnail có người](references/person-thumbnail.md).

**Shorts mặc định không tạo thumbnail riêng — chốt 30/10/2026.** Quy tắc ImageGen bên dưới chỉ áp dụng khi thực sự được giao tạo/sửa thumbnail; xem mục Shorts.

**Thumbnail bắt buộc ImageGen toàn artwork —23/10/2026:** đọc skill `imagegen` và thực sự gọi công cụ tạo/sửa ảnh cho mọi thumbnail mới/chỉnh sửa trong phạm vi được giao. Tuân thủ **VIDEO GỐC → TRÍCH FRAME → IMAGEGEN SKILL → KIỂM TRA → XUẤT THUMBNAIL → CẬP NHẬT YOUTUBE**; xem [workflow ImageGen bắt buộc](references/imagegen-workflow.md). Không tự thiết kế/ghép chữ, logo, xe, beam bằng code hoặc chỉ dùng ImageGen tạo nền. Công cụ lập trình chỉ hỗ trợ trích frame, phân tích/kiểm tra, chuyển kích thước/định dạng và upload. Thiếu ImageGen thì báo chặn, không tự fallback. Hướng này thay các ngoại lệ hoàn thiện artwork bằng script trước đây, trừ khi người dùng yêu cầu rõ phương pháp khác sau này.

Theo yêu cầu23/10/2026: đăng bình thường không thêm bước lọc danh sách hoặc gán playlist/nhóm mặc định. Giữ chống trùng qua checkpoint/videoID; chỉ kiểm sâu khi có dấu hiệu trùng hoặc kết quả thao tác chưa rõ. Bài học ảnh cụm đèn lắp thực tế và mép ghép sạch nằm trong [browser/thumbnail](references/browser-and-thumbnail.md).



Mọi thao tác web và xem thử HTML chỉ dùng **Codex In-app Browser (`iab`)**, kể cả agent phụ. Không tự chạy trình duyệt local/Chrome/Edge ngoài app hoặc browser riêng bằng script. Đọc [quy tắc trình duyệt Codex](references/codex-browser-only.md) trước thao tác browser/preview; trang localhost cũng phải mở trong IAB. Dùng link xem YouTube/Studio thông thường; không mở link tải CDN/videoplayback dài hoặc gọi tải media từ link video (bổ sung 19/10/2026 trong tài liệu browser).



Đọc [rules8](references/editorial-rules.md), [workflow](references/workflow.md) và [templates2](assets/templates/description-templates.json). [mẫu channel8](assets/templates/channel.example.json) là nguồn chữ ký duy nhất; profile cụ thể của job có thể thay đích kênh. Entrypoint và schema: [runtime](references/runtime.md).



Khi người dùng gọi skill, đưa link/file video và nói **“đăng đi”, “đăng clip này”** hoặc tương đương, nhận toàn bộ job: đọc/kiểm nguồn/nghiên cứu → tự chọn metadata → thumbnail bằng ImageGen cho video dài (Shorts bỏ qua mặc định) → upload nếu chưa có → **công khai** → readback/trả link. Kênh mặc định từ channel.json là Auto365 Review. Không đợi nhắc bước hoặc duyệt từng phần; chỉ hỏi thiếu thiết yếu, quyền truy cập hoặc login/OTP. Yêu cầu cụ thể mới nhất như prepare-only/riêng tư/lên lịch/giữ một trường thắng mặc định. Đây không là quyền cho dịch vụ ảnh trả phí khác.



Ghi cách hiểu đó bằng `init-job` vào job.action_request: mode/quyền/kênh/source/selection policy; sửa mô tả khóa revision/hash trước ghi. Quyền cũ không thắng giới hạn mới, prepare-only không ghi remote. Đọc checkpoint trước; reuse cùng hash và đúng ID, không audit/upload lại để sửa metadata hoặc áp clip test sang clip mới. Ví dụ lời gọi nằm trong [runtime](references/runtime.md).



Tìm auto365-writer/copywriting/content-strategy bằng catalog hiện tại hoặc `discover`, đọc SKILL.md khi dùng. Chỉ lấy kiểm nguồn/claim, văn phong/CTA, phân nhóm/playlist; không kéo chuẩn SEO website vào YouTube. Thiếu guidance/Gem gốc thì báo phạm vi và dùng rules tự chứa, không nhận đã đọc nguồn chưa có.



Workflow: Nhận video → Phân tích hình ảnh/âm thanh → Kiểm chứng thông tin → Nghiên cứu từ khóa → Viết nội dung SEO → Tạo thumbnail khi áp dụng (Shorts bỏ qua mặc định) → Đăng video → Kiểm tra và trả link. Chỉ chạy các bước phù hợp phạm vi job; sửa chữ ký trên video có sẵn thì giữ nguyên phần còn lại.



Trước viết mới/sửa tiêu đề hoặc tạo thumbnail, đọc [bài học tiêu đề có hook và bộ ảnh tham chiếu đã chốt](references/packaging-style.md). Tiêu đề phải có keyword ngành hàng đúng nội dung cùng xe/model, như “đèn bi gầm”, “đèn bi LED”, “phim cách nhiệt” hoặc loại “camera” thực tế; viết đủ ý, không rút cụt để chỉ còn tên xe/model. Hook hỏi lý do quyết định phải rõ chủ thể và hành động: ví dụ “Đèn zin vẫn sáng, sao chủ xe vẫn đổi?”, không cắt thành “sao đổi?”. Dùng “nâng cấp” thay “độ” trong tiêu đề mới; xem các ảnh mẫu lưu cùng skill trước thiết kế thumbnail để đồng bộ chữ khối nghiêng trắng–vàng và bố cục xe lớn.

<!-- service-action-object-title-20261021 -->
Tiêu đề phải nêu rõ dịch vụ hoặc thao tác thay đổi và đối tượng của thao tác đó, đúng nội dung clip: ví dụ “nâng cấp đèn bi gầm”, “thay đèn LED zin”. Trong hook, không rút “thay đèn LED zin” thành “thay LED zin” làm thiếu đối tượng dịch vụ. Chọn động từ “lắp”, “thay”, “nâng cấp”, “dán”… theo ca thật; không ép mọi video dùng từ “thay”. Giữ đủ tên xe, hạng mục và model khi có, đồng thời đếm ký tự thực trong giới hạn 100. Chỉ áp dụng tiêu đề mới hoặc video đang được người dùng giao sửa.

## Shorts: chữ ký, thumbnail và lịch đăng — cập nhật 30/10/2026

- **Không tạo thumbnail riêng cho Shorts theo mặc định.** Giữ ảnh đại diện có sẵn/tạo tự động từ chính video; không gọi ImageGen, không thiết kế/xuất/upload ảnh thumbnail và không chèn thêm khung ảnh vào clip chỉ để làm bìa. Chỉ tạo/sửa thumbnail Shorts khi người dùng yêu cầu cụ thể; khi đó vẫn dùng ImageGen theo quy tắc thiết kế hiện hành. Video dài giữ quy trình thumbnail hiện hành.
- Sau khi xác minh định dạng Shorts, ghi `thumbnail_policy.mode: KEEP_AUTO_VIDEO_FRAME`; loại `generate_thumbnail_imagegen` và `edit_thumbnail` khỏi phạm vi mặc định trong `job.action_request`, đặt `service_authorizations.built_in_imagegen_thumbnail: false`, trừ khi có yêu cầu thumbnail rõ ràng. Bỏ qua cổng artwork/JPEG thiết kế khi giữ ảnh từ video, nhưng vẫn kiểm đúng clip/ảnh đại diện sau đăng. Không để quyền thumbnail mặc định của helper khởi tạo thắng quy tắc Shorts này.

- Shorts dùng chữ ký gọn **ba dòng trong mô tả**, xuất một lần từ `channel.shorts_signature_template`: thương hiệu → tư vấn đúng ngành hàng → hotline phản ánh. Không nối chữ ký dài, địa chỉ, maps, website, Facebook hoặc dòng bản quyền vào mẫu gọn. Video dài giữ `channel.signature_template`. Không mặc định chèn nguyên chữ ký lên hình hay kéo dài đoạn kết.
- Ghi `brief.format: "shorts"` sau khi xác minh định dạng thực; truyền cùng format qua bước render và validate, không suy Shorts chỉ từ thời lượng.
- Anh gửi ngày/giờ đăng thì **lên lịch theo đúng ngày/giờ đó**, áp dụng cả Shorts và video dài; mặc định giờ Việt Nam (GMT+7), trừ khi anh chỉ định khác. Ngày tương đối lấy theo thời gian phiên hiện tại. Chỉ gửi giờ: dùng ngày đã rõ trong job, nếu chưa có thì hôm nay khi giờ đó còn ở phía trước; thiếu ngày rõ hoặc giờ đã qua thì hỏi đúng phần thiếu, không tự dời ngày hay đăng ngay.
- Lưu `action_request` mode `schedule` và `publish_at` ISO có offset; kiểm đúng ngày, giờ, múi giờ tại Studio, lưu rồi tải lại xác nhận trạng thái Đã lên lịch. Trả link kèm ngày/giờ cụ thể; không xin xác nhận lại lịch đã rõ. Xem [rules](references/editorial-rules.md) và [runtime](references/runtime.md).

## Biên tập



1. Tự đọc media/transcript/frame khi chưa có bằng chứng cùng hash. Rà xe/đời/phiên bản, model/SKU và lỗi ASR; giữ raw/corrections/coverage. Không bắt người dùng viết title/dán transcript, không giả xem toàn bộ.

2. Khóa facts/source/QA/timestamp: video đề cập khác nguồn hiện hành. Không bịa thông số/giá/bảo hành/kết quả/nhu cầu khách hoặc suy hiệu quả từ W/K. Giữ thương mại đầy đủ nội bộ. Trước chốt nội dung đọc [rà quảng cáo](references/advertising-law.md), kiểm claim dẫn đầu/tuyệt đối/so sánh và bằng chứng trên metadata, thumbnail, lời nói/chữ trong video; lưu advertising-review.json của đúng revision. Phân biệt hướng dẫn nội bộ với điều luật; thiếu hồ sơ thì bỏ/viết lại claim, không nhận tuân thủ toàn diện khi video gốc còn claim ngoài phạm vi sửa.

3. Tự nghiên cứu YouTube/web mỗi video trước final; Analytics chỉ đúng ID/quyền. Lưu query/URL/ngày/origin/lý do/limits; phân biệt metric và đề xuất, không bịa volume/trend. Rà title/description/hashtag và **tags riêng Studio**, không đợi nhắc/ép số lượng. Search lỗi ghi giới hạn, tiếp tục dữ kiện đã kiểm.

4. Title tạo ba góc khi nội dung cho phép, chọn một/đếm ký tự thật; description-only giữ trường khác. Mô tả như người làm nghề: mở vào xe/model/điểm đáng xem, giải thích đủ vấn đề–tính năng–ý nghĩa–lựa chọn có nguồn, CTA ngắn. Gọn bỏ thừa/lặp, không bỏ chiều sâu; Shorts và video dài theo nội dung, templates không ép đủ mục/độ dài/FAQ. Không sáo rỗng, giọng báo cáo, nhồi từ khóa hoặc hứa top/AI citation.

5. narrative_sections có text/purpose/evidence, chỉ text xuất public; không truncate. **Không VAT** trong mô tả/CTA/bình luận đề xuất; giá sản phẩm không là giá hoàn thiện. Giá/bảo hành/link/chapters tùy nguồn/nội dung. Link đúng model/đích đã mở.

6. Video dài phải rà timeline: thêm mốc thật khi có phân đoạn; nếu không phù hợp, ghi timeline_review với lý do/bằng chứng, không chấm Đạt khi chưa kiểm. Không chia đều/copy mẫu: 00:00,≥3mốc tăng, mỗi đoạn≥10s kể cả cuối; đặt TIMELINE CHI TIẾT trước chữ ký. Một chữ ký theo profile: ☎tư vấn đúng dịch vụ và phản ánh đúng số/thứ tự; không đổi theo website. Với video dài, dòng bản quyền Auto365 lấy từ cùng signature_template, một lần; Shorts dùng mẫu gọn không nối dòng này; rà quyền tư liệu/nhạc, nguồn không rõ phải giải quyết trước khi nhận sở hữu. Hashtag sát chủ đề; 6–10 chỉ gợi ý khi đủ liên quan. Comment chỉ là đề xuất nếu chưa có quyền.



## Browser, thumbnail và bàn giao



- Trước tạo/chọn thumbnail và trước upload/Publish/bàn giao, đọc [workflow ImageGen](references/imagegen-workflow.md), [cổng chất lượng thumbnail](references/thumbnail-quality-gate.md) và [luật ảnh, chữ/phục hồi](references/browser-and-thumbnail.md), kể cả job từ hai skill dựng video. ImageGen tạo/sửa toàn bộ artwork; logo gốc, chữ chính xác và đủ frame sáng thật đều được cung cấp làm đầu vào. Không ghép bù artwork bằng script. JPEG cuối và bản320px cùng hash phải được mở kiểm bố cục, nguồn, dấu Việt, model và beam; lỗi thì sửa bằng ImageGen rồi xuất/kiểm lại. Metadata validation không thay kiểm ảnh; tiếp tục theo quyền job, không tự thêm vòng duyệt nếu đã giao toàn workflow.



- Kiếm tiền: người dùng chốt ngày 13/10/2026 **mặc định bật kiếm tiền** cho job YouTube; chỉ thị cụ thể mới hơn thắng mặc định. Chọn Bật trong Studio, đánh giá quảng cáo theo nội dung thật và báo riêng nếu YouTube còn xét duyệt hoặc giới hạn quảng cáo.



- Đọc [browser/thumbnail/recovery](references/browser-and-thumbnail.md) trước thao tác. Dùng trình duyệt tích hợp; so live Studio ID/quyền với profile/job trước ghi. Chỉ đi trường được giao, lưu before/intent/checkpoint; ID đã có bỏ upload. Login/OTP/CAPTCHA để người dùng. Playlist đã có; tạo mới/comment/connections/credit cần quyền riêng.

- Mọi thumbnail được giao đều dùng ImageGen theo [workflow bắt buộc](references/imagegen-workflow.md): xem frame thật/reference, xác minh xe/model, đủ cảnh sáng, dùng logo gốc từ channel.brand_assets làm reference. Artwork premium đỏ–đen–trắng,16:9≥1280×720, giữ nhận diện và khác biệt nhiệt màu nguồn; không bịa ca xe, phép đo hay kết quả test. Lưu đầu ra ImageGen trực tiếp/prompt/reference/hash; không tuyên bố dùng ImageGen nếu chỉ render Python. Quyền tạo/sửa thumbnail không cấp quyền sửa metadata, Publish hay gửi nhóm ngoài yêu cầu.

- Validate chính revision với metadata/review/text/hash cùng bản; tự kiểm tám mục và nguồn/giọng văn, xử lý vấn đề trọng yếu trước commit. Chờ Save/processing/checks, reload readback nguyên text đã chốt và một chữ ký; so các trường ngoài scope. Publish/schedule kiểm thêm ID/trạng thái/lịch/trang xem phù hợp. Lưu revision/hash/URL/thời điểm/ảnh; chưa rõ kết quả thì kiểm Studio trước retry, không upload/đăng lại.

- Bàn giao nội dung và giới hạn, Đạt/Cần sửa/Chưa xác minh có lý do; thao tác thật kèm URL/trạng thái/ảnh. Không tự chấm hiệu quả hoặc nhận đã kiểm mọi nhánh remote. [Ví dụ tổng hợp](assets/examples/brief.example.json) chỉ dùng kiểm cấu trúc, không có dữ kiện media thật hay quyền đăng; phạm vi ở runtime.

- **Định dạng báo kết quả — người dùng chốt 30/10/2026:** báo từng clip theo dòng hoặc danh sách đánh số, **không kẻ bảng**. Mỗi mục ghi tên/tiêu đề clip, link video hiển thị rõ và bấm được, cùng trạng thái thực tế đã xác minh. Clip hẹn giờ ghi ngày và giờ đăng cụ thể, kèm múi giờ chung khi cả lô dùng cùng múi giờ. Có thể xuống dòng đặt link ngay dưới thông tin clip. Clip đang tải/xử lý/chưa xác minh phải ghi đúng tình trạng, không báo đã đăng hoặc đã lên lịch khi chưa kiểm. Áp dụng cả Shorts, video dài và lô nhiều clip; chỉ đổi cách trình bày khi người dùng yêu cầu rõ khác đi.



## Bản GitHub portable

Đọc [README](README.md) để cài đặt và tạo workspace ngoài thư mục skill. Cấu hình vận hành duy nhất là `WORKSPACE/channel.json`, khởi tạo từ `assets/templates/channel.example.json`; registry sản phẩm nằm cạnh profile. Không dùng ví dụ tổng hợp làm nguồn thật. Bộ phân phối giữ các quy tắc hiện hành và runtime; không kèm hồ sơ video, transcript, Analytics hoặc đăng nhập của máy nguồn.
