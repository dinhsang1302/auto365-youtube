# Trình duyệt tích hợp, thumbnail và phục hồi

**Cập nhật bắt buộc23/10/2026:** mọi thumbnail dùng [ImageGen trực tiếp tạo toàn artwork](imagegen-workflow.md). Phong cách mặc định premium automotive advertising đỏ–đen–trắng. Các mục lịch sử về ghép chữ/logo/cảnh sáng hoặc Remotion/CSS bên dưới không còn cho phép native finishing bằng code; chỉ giữ ý nghĩa kiểm nguồn, nhận diện, chính tả và chất lượng. Nếu sai, sửa bằng ImageGen. Thứ tự: video gốc → trích frame → ImageGen Skill/công cụ thật → kiểm → xuất → YouTube theo quyền.



Người dùng chốt 16/10/2026: chỉ dùng trình duyệt tích hợp Codex cho web, Studio và xem thử HTML/thumbnail, cả trang localhost. Áp dụng [codex-browser-only.md](codex-browser-only.md) cho cả agent phụ; không dùng browser riêng/Playwright/Puppeteer/Selenium ngoài IAB hoặc lệnh shell mở trình duyệt mặc định. Giữ tab thử ẩn khi hỗ trợ và đóng sau kiểm tra.



Đọc [workflow máy đọc](browser-workflow.json) cùng policy8. Dùng API browser tích hợp được môi trường cung cấp và tài liệu hiện hành; không dùng endpoint nội bộ YouTube/cookie hoặc một browser khác để thay thế. Nếu thiếu khả năng/filechooser, báo chính xác bước chặn; không nhận đã upload.



## Thumbnail từ tư liệu thật

Bộ mẫu người dùng chốt ngày 17/10/2026 được lưu trong `../assets/thumbnail-references/`. Trước thiết kế, đọc [packaging-style.md](packaging-style.md) và mở ảnh mẫu liên quan: xe lớn/nền liền mạch, chữ khối nghiêng trắng–vàng sáng, nhấn đỏ, logo gốc cao góc trái. Mẫu chỉ hướng dẫn style, không thay nguồn xe/beam hoặc bằng chứng của job.



Trước thiết kế và trước upload/bàn giao, áp dụng [cổng chất lượng thumbnail](thumbnail-quality-gate.md). Đây là tiêu chí bắt buộc cho cả thumbnail mới và revision sửa lỗi, gồm job chuyển từ skill dựng clip; có đủ nguồn/đúng kích thước không tự chứng minh bố cục đạt.



Người dùng chốt 15/10/2026: poster đèn/xe phải thể hiện sản phẩm, ánh sáng và xe thi công thực tế của job; có người hay không tùy bố cục. Ánh sáng dùng cảnh thật, không dựng chùm sáng/đổi cường độ để giả kết quả test. Nếu clip review rời không có xe thi công xác minh được, ghi rõ giới hạn, ưu tiên sản phẩm + cảnh chiếu sáng thật, không ghép xe khác thành ca của clip. Khi thiếu tư liệu thiết yếu không thể xác định thì hỏi.



Logo bắt buộc lấy file gốc người dùng cung cấp làm reference cho ImageGen: `../assets/brand/auto365-white.png` nền tối, `../assets/brand/auto365-black.png` nền sáng. Yêu cầu giữ tỷ lệ, hình chữ, màu và slogan; đối chiếu đầu ra, sai thì sửa bằng ImageGen. Không tự ghép logo/chữ bằng script. ImageGen trực tiếp xuất toàn artwork; giữ master và chỉ chuyển định dạng/kích thước sang JPEG để đăng.



Bài học người dùng chốt lại 16/10/2026: **clip có 3 nhiệt màu thì thumbnail bắt buộc thể hiện đủ cả 3 nhiệt màu**, kể cả khi chữ chính không ghi “3 nhiệt màu”. Dùng ba cảnh/vùng sáng thật đúng phiên bản trong chính clip hoặc nguồn đúng job đã xác minh; gắn nhãn đúng thông số của clip (ví dụ 3000K/4300K/5500K khi clip xác nhận ba giá trị này), lưu timestamp và ánh xạ từng nhãn. Không đổi hue một ảnh để giả ba phiên bản, không tự suy đủ bộ từ tên model, không dựng beam bằng ImageGen thành ảnh test. Thiếu một màu thật thì giữ ảnh ở trạng thái Chưa đủ tư liệu, không lược bỏ màu để upload. Màu qua camera/màn hình không là phép đo hiệu suất hay bằng chứng hiệu quả mưa/sương.



Bố cục người dùng sửa 16/10/2026: xe thật phải lớn và nổi bật, bố cục tràn hình/nền liền mạch như các thumbnail thiết kế đã được chấp nhận; không chia xe, hộp sản phẩm và ánh sáng thành lưới các ô viền, không đặt chú thích nguồn nhỏ chi chít lên ảnh. Sản phẩm và ba vùng sáng có thể ghép tự nhiên quanh chủ thể, tránh che xe/chữ. Không tạo banner chữ quá lớn khiến xe chỉ còn một ô nhỏ. Kiểm ở bản đầy đủ và 320px: xe/model đúng, chữ rõ, đủ ba màu đúng nhãn khi áp dụng, logo gốc hòa nền không đóng hộp. Mẫu sai giữ lại trong lịch sử và làm revision mới; chỉ thay thumbnail do chính job vừa tạo khi người dùng yêu cầu sửa, không lan sang thumbnail thiết kế đã có khác.



Bài học người dùng bổ sung 16/10/2026 cho **phim cách nhiệt và PPF**: thumbnail phải thể hiện rõ **phim** (lớp phim/cuộn phim/tấm phim trên bề mặt phù hợp) và **hiệu ứng được nói đến trong clip gốc**, không chỉ có xe và tên sản phẩm. Với phim cách nhiệt, chọn hiệu ứng đúng nội dung đã kiểm như cản nhiệt, giảm chói, tầm nhìn hoặc riêng tư; với PPF cũng thể hiện lớp phim và hiệu ứng/bảo vệ/hoàn thiện bề mặt mà chính clip xác nhận. Các ví dụ này không tự cấp quyền gán tính năng cho mọi sản phẩm. Lưu timestamp/nguồn và ánh xạ hiệu ứng vào thumbnail-review.json; kiểm cả bản lớn và 320px có nhìn thấy phim lẫn hiệu ứng. Hiệu ứng đồ họa minh họa được dùng khi bám nội dung nguồn và nhận diện rõ là minh họa; không dựng thành ảnh test thật, không bịa kết quả/so sánh/số liệu hay thêm tính năng ngoài clip. Mẫu chỉ có xe + chữ hoặc thiếu hiệu ứng nguồn phải sửa revision trước upload; giữ nguyên lịch sử.



1. Tìm ảnh đúng video trong nguồn. Nhiều ảnh không phân biệt được hoặc thiếu ảnh thì hỏi phần thiết yếu; quyền chọn đại ảnh của job test không áp video khác. Ảnh tiến độ/yêu cầu không tự là thumbnail.

2. Mọi thumbnail: đọc và dùng skill/tool ImageGen thật theo [workflow bắt buộc](imagegen-workflow.md); mở frame/reference đã xác minh, đưa toàn bộ ảnh cần thiết và chữ chính xác vào lời gọi tạo artwork hoàn chỉnh. Thiếu công cụ thì báo chặn, không dựng thay bằng code.

3. Học cách bố cục/màu/chữ/nổi chủ thể, thay bằng đúng xe và model hiện tại. Chữ Việt ngắn/lớn,16:9. Không sao chép xe/sản phẩm/giá/thông số của mẫu, không tạo chùm sáng giả như kết quả test thật.

4. Kiểm chữ/model/hình dáng/scope; lưu output vào job, nếu sửa thì sửa trên ảnh đã tạo. Không gọi dịch vụ ảnh trả phí khác hoặc tiêu credit chưa có quyền. Khai báo nội dung thay đổi theo hình/video thực và câu hỏi Studio; không mặc định mọi ảnh hỗ trợ thumbnail có cùng khai báo.



### Cổng kiểm chính tả trước upload



Kiểm độ tách nền của logo sau ghép: phần 365 đỏ không đặt chìm trên sọc đỏ. Giữ màu/hình logo gốc; ưu tiên vùng nền sạch hoặc làm tối mềm trung tính ngay sau logo, không tự đổi màu 365. Người dùng đã bỏ khung bo góc/đường viền vì làm logo giống đóng hộp; không đưa khung đó thành mặc định. Logo nhỏ góc trên trái, nền hòa vào ảnh, kiểm cả bản đầy đủ/mobile và không lấn chủ thể/chữ chính.



Lựa chọn thẩm mỹ người dùng chốt cho F10 Turbo: giữ kiểu chữ đậm, nghiêng, có chiều sâu trắng–vàng của ảnh tham chiếu do người dùng gửi; không sửa lỗi dấu bằng cách thay toàn bộ thành chữ phẳng khác style. Logo gốc đặt nhỏ góc trên trái, không làm banner thương hiệu lớn ở giữa. Dùng như ưu tiên nhận diện cho các mẫu sau khi phù hợp, không ép mọi video cùng bố cục; chỉ thị mới hơn thắng.



Đọc chữ trên file cuối, không chỉ prompt: dấu Việt (đặc biệt MÀU khác MÁU), model, số/đơn vị, nhãn và slogan. Xem đầy đủ và320px. Có lỗi thì Cần sửa, chưa upload; dùng ImageGen sửa đúng chữ trên chính artwork, không ghép typography bằng script. Mở lại bản xuất cuối sau sửa. Lưu thumbnail-review.json với file/hash, exact_copy, kết quả chính tả/model/logo, reference/timestamp, nhãn, khả năng đọc và giới hạn. Không cách điệu gây nhầm dấu.



Bổ sung lỗi font 16/10/2026: khi ghép chữ bằng Remotion/CSS, kiểm font có đủ từng ký tự tiếng Việt thực dùng, nhất là “Ệ” trong “NHIỆT”; không coi chữ hiện ra là bằng chứng không có font fallback. Nhúng đúng file font và chờ font tải xong trước render; không dựa tên font/weight tự dò của máy. Đồng bộ chữ phụ/nhãn nhiệt màu với kiểu đậm, nghiêng, có chiều sâu của tiêu đề; không chữa dấu bằng font phẳng lệch phong cách. Bản JPEG xuất cuối phải qua kiểm trực quan cả đầy đủ và 320px trước upload.



Tham khảo Pinterest/mẫu công khai: phải xem được ảnh trước khi nhận đã tham khảo, lưu URL/ngày và yếu tố bố cục học hỏi; không sao chép xe/claim/giá/model. Trang yêu cầu đăng nhập thì báo chưa xem được và dùng nguồn công khai thay thế với nhãn rõ, không tự nhận đã xem pin. Mẫu đẹp, nhiều lượt xem/lưu hoặc điểm AI không chứng minh CTR cao. Chỉ gọi CTR đã quan sát khi có Analytics đúng video/kênh/kỳ và quyền; không bảo đảm hiệu quả từ bố cục.



## Preflight và commit



- So đúng live channel ID và quyền hiện tại với profile + job. Config/Analytics snapshot không chứng minh đang đăng nhập đúng kênh. Login/OTP/CAPTCHA để người dùng làm, không lưu secrets. Không đọc Analytics kênh test/vidIQ khác để kết luận về kênh đích; không tự đổi kết nối.

- Kiểm nhật ký và Nội dung đúng kênh, gồm nháp/private/unlisted/scheduled/public, Video/Shorts theo phạm vi cần thiết. SHA xác định file local; Studio không lộ hash gốc. Nếu video ngoài nhật ký, tên file/thời lượng/frame/chủ đề là tín hiệu, không chứng minh byte identity. Nghi trùng chưa kết luận được thì không upload tiếp; hỏi quyết định cần thiết.

- Có đúng video ID thì dùng lại và chỉ đi trường được giao. Capture title/description/tags/thumbnail/playlist/audience/disclosures/visibility trước sửa. Đọc default-description và hợp nhất một chữ ký; block cũ khác mẫu cần rà, không xóa bằng heuristic. Không đổi title/thumb/tags để sửa description.

- Upload mới khi có quyền: ghi UPLOAD_INTENT trước chọn file; dùng filechooser API đúng đường dẫn, ghi ID ngay khi có. Chọn audience/disclosures theo nội dung thật, playlist phù hợp đã có; tạo mới/comment/connections/paidservice cần quyền riêng.

- Validate đúng revision và hash, tự kiểm nguồn/semantic tám mục. Quyền cụ thể đã được giao thì tiếp tục sau kiểm, không hỏi lại; chưa có quyền thì bàn giao local. Ghi COMMIT_INTENT hoặc DESCRIPTION_SAVE_INTENT trước nút cuối. Chờ upload/processing/checks, xử lý vấn đề trọng yếu trước publish/schedule. Với schedule, ghi giờ+timezone từ yêu cầu/phiên và đối chiếu giờ hiển thị Studio, không đoán từ timezone máy thực thi.



## Readback và retry



- Sau Save, chờ thông báo đã lưu/nút Save disabled; reload đọc lại. So nguyên text đã chốt: chỉ chuẩn hóa CRLF/LF và newline cuối, không bỏ ☎ hoặc thay lời. Kiểm một chữ ký, dòng tư vấn đúng ngành hàng và dòng phản ánh chất lượng1900 9365 đúng profile/thứ tự; không có hotline nhập sỉ. So các trường ngoài scope với before; thumbnail có thể chuẩn hóa bỏ tham số cache nhưng giữ asset/version.

- Sau publish/schedule, mở Studio và trang xem khi phù hợp, kiểm ID/kênh/trạng thái/lịch/title/description/thumb/tags theo phạm vi. Chỉ ghi VERIFIED_* khi có bằng chứng. Lưu URL/revision/hash/thời điểm/snapshot/ảnh và embed ảnh xác minh khi bàn giao thao tác thật.

- Nếu timeout/mất kết nối/lỗi save hoặc commit chưa rõ: ghi UNCERTAIN + URL/ID/bước/error/ảnh, đọc kết quả hiện có trước retry. Không bấm publish/upload lại khi chưa rõ. Có ID thì mở chính ID đó, thiếu ID thì kiểm danh sách kênh. Không hứa exactly-once.



Kiểm local/skill không tương đương kiểm mọi nhánh browser. Lịch sử có private-upload/publish/description-readback trên các job cụ thể; scheduling, recovery mất kết nối và phiên/quyền mới phải kiểm khi thực sự được giao. Không tự chạy thử trên kênh thật để hoàn tất kiểm skill.


## Bài học VF8 ngày23/10/2026

Khi clip có cảnh lắp thực tế và người dùng chọn cảnh đó, trích đúng frame để thể hiện bi, pát và cụm đèn; ưu tiên ảnh này thay sản phẩm minh họa rời. Giữ chi tiết phần cứng từ ảnh gốc khi hoàn thiện, không dùng bản AI tái sinh làm bằng chứng thi công. Bố cục xe lớn và cụm đèn rõ, mép ghép sạch; không dùng mảng ảnh đường nhỏ với feather rộng làm vùng sáng lem hoặc trộn vào thân xe. Nếu bỏ cảnh đường để ưu tiên cụm đèn, không gắn nhãn test đường hoặc tạo beam giả. Không ép mọi clip theo đúng vị trí trái/phải của mẫu VF8.

Đăng bình thường theo yêu cầu23/10/2026: bỏ bước lọc danh sách nội dung và gán playlist/nhóm như một bước mặc định. Dùng checkpoint/videoID của job để tránh đăng lại; chỉ kiểm tra bản trùng có mục tiêu khi có dấu hiệu trùng hoặc sau lỗi chưa rõ kết quả. Yêu cầu không báo group thắng workflow thông báo mặc định; trả link tại chat sau xác minh.

Bổ sung23/10/2026: trước upload/bàn giao, áp dụng mục kiểm lỗi ghép trong [thumbnail-quality-gate.md](thumbnail-quality-gate.md): tự rà đường bao, quầng/mép nhòe, sơn xe loang, phối cảnh/ánh sáng của xe–nền, phần beam bị mất và chữ bị overlay cắt. Lưu nhận xét sửa thật ở `composite_qc` của đúng JPEG/hash; không chờ người dùng chỉ lỗi.
