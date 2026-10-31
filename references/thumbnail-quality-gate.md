# Cổng chất lượng thumbnail trước upload và bàn giao

**Ngoại lệ phạm vi Shorts — người dùng chốt 30/10/2026:** mặc định giữ ảnh đại diện từ video, không tạo thumbnail riêng và không gọi ImageGen. Không dùng tài liệu này để bắt buộc thiết kế thumbnail cho một job Shorts đăng thông thường. Chỉ áp dụng quy trình/cổng thiết kế khi người dùng yêu cầu cụ thể tạo hoặc sửa thumbnail Shorts. Video dài và các thumbnail được giao vẫn theo ImageGen.

Áp dụng từ bài học người dùng ngày16/10/2026 cho thumbnail Auto365 được giao tạo/sửa, cả job mới từ `edit-video-seo-template`/`edit-phim-cach-nhiet-template` và agent phụ. Đọc cùng [nguồn, chính tả/font, logo và browser](browser-and-thumbnail.md). Không tự thay thumbnail thiết kế đã có ngoài phạm vi người dùng giao.

## Thiết kế và phạm vi công cụ

Theo yêu cầu23/10/2026, **mọi thumbnail được giao phải do ImageGen trực tiếp tạo toàn artwork**, theo [workflow bắt buộc](imagegen-workflow.md). Phải đọc skill và gọi công cụ thật với frame/reference đã xem; không tự dựng bằng code hoặc chỉ dùng ImageGen tạo nền. Không khả dụng thì báo chặn, không tự fallback. Chỉ yêu cầu rõ ràng mới hơn của người dùng mới đổi phương pháp.

Chữ, logo và cụm cảnh sáng phải nằm trong đầu ra ImageGen hoàn chỉnh; sai thì sửa bằng ImageGen, không native finishing bằng script. Code chỉ hỗ trợ trích frame/phân tích/kiểm tra/chuyển định dạng-kích thước/upload. Cung cấp đủ frame beam thật làm reference và đối chiếu khác biệt quan sát được; không bịa phép đo/hiệu năng hoặc gọi artwork gen là ảnh gốc không đổi pixel. Quyền tạo ảnh không cấp quyền metadata/Publish/gửi nhóm ngoài `action_request`.

## Những điều phải nhìn thấy trên ảnh cuối

- **Xe và sản phẩm:** đúng xe/đời/phiên bản và model đã xác minh. Xe lớn, nhận diện rõ, bố cục tràn hình với nền liền mạch; giữ được các chi tiết cần thấy của ca xe. Ưu tiên ảnh hoàn thiện thấy rõ vị trí lắp; ảnh có khăn thi công/dụng cụ/hộp che chủ thể không tự là hero đạt, phải ghi lý do phù hợp với chủ đề. Thiếu ảnh hoàn thiện thì không bịa kết quả thi công hoặc bật đèn giả để bù. Xe là ảnh nền lớn nhưng bị chữ/ảnh khác che vẫn chưa đạt. Không lặp lại cùng hộp sản phẩm thành một ô nổi không có mục đích.
- **Phân cấp chữ:** câu chữ ngắn, model chính đọc được ở320px; bố trí vùng chữ riêng để không che mặt xe, đèn, sản phẩm hoặc vùng sáng cần đối chiếu. Theo mẫu người dùng đã chốt: chữ đậm/nghiêng có chiều sâu trắng–vàng khi phù hợp, không tự thay bằng cả mảng chữ Arial phẳng chồng lên ảnh xe. Không thêm claim để lấp chỗ trống; yêu cầu thẩm mỹ mới hơn thắng mẫu cũ.
- **Bố cục:** không chia xe/hộp/beam thành các ô rời. Bỏ đường viền hoặc feather mép ảnh không tự biến collage rời thành thiết kế đạt. Chủ thể, chữ và bằng chứng phải tạo thành một bố cục cân đối, nhìn rõ ở bản nhỏ.
- **Ba nhiệt màu:** clip có ba lựa chọn thì phải có đủ ba mẫu thật đúng nguồn/nhãn. Khi thu nhỏ, vẫn nhìn thấy vùng chiếu sáng có ý nghĩa và phân biệt được ba mẫu. Giữ chân/cutoff, vùng phủ và hai mép quan trọng của chùm sáng; không ép ảnh đường rộng vào dải thấp rồi `cover`/crop mất phần chứng minh. Dùng fit/contain hoặc crop chỉ phần thừa; nếu không đủ chỗ thì dàn lại bố cục/giảm chữ. Không gắn mode/nhiệt màu theo thứ tự đoán. Nếu nguồn là ảnh sản phẩm, khác phép test trên chính xe trong clip, đặt nhãn rõ trên ảnh như **“MẪU3NHIỆT MÀU”** hoặc **“MẪU ÁNH SÁNG SẢN PHẨM”**; ghi ở JSON nội bộ là chưa đủ.
- **Phim cách nhiệt/PPF:** phải thấy lớp/cuộn phim và hiệu ứng được chính nguồn đề cập; xe + tên phim chưa đủ. Phân biệt hình minh họa với test thật trên ảnh, nhãn phải đọc được ở bản320px; không bịa thông số/kết quả.
- **Logo và chữ:** dùng nguyên logo gốc, nhỏ góc trái, hòa nền và đủ tương phản; không hộp/viền thương hiệu hoặc logo sinh lại. Đọc từng chữ trên JPEG cuối: dấu Việt, model, số/đơn vị và nhãn; kiểm glyph/font thực dùng. Giữ toàn bộ chữ quan trọng trong khung, không cắt, chồng nét hoặc bị thời lượng YouTube góc phải dưới che mất.

## Review phải gắn đúng ảnh và bằng chứng

Sau mọi lần sửa/ghép logo/chữ/crop/xuất JPEG, xem lại **chính file sẽ upload** ở1280×720 và bản320px sinh từ file đó. Không dùng PNG cũ, HTML preview, manifest v1 hoặc review v2 để duyệt file v3. Bản người dùng phản hồi chưa đạt phải mở revision mới; giữ lịch sử, không coi PASS trước đó là lý do bỏ qua lỗi.

Trong `thumbnail-review.json`, lưu:

- `revision`, đường dẫn và SHA-256 của JPEG upload; bản320px và hash JPEG nguồn tạo ra nó.
- `generation_method`, output ImageGen và prompt/reference đã dùng; hoặc yêu cầu trực tiếp của người dùng cho phương pháp khác. Ghi mẫu đã thực sự xem cùng các đặc điểm bố cục/chữ học theo và nhận xét ảnh cuối có đáp ứng hay không.
- `exact_copy`, logo nguồn/hash, bản đồ xe/sản phẩm/mode/nhiệt màu → asset/timestamp; loại bằng chứng là ca xe, mẫu sản phẩm hay minh họa.
- `visual_findings` theo bố cục xe/chữ/sản phẩm, crop từng vùng sáng, nhãn nguồn, chính tả/font, logo và khả năng đọc bản nhỏ. Ghi dòng chữ chính/nhãn thiết yếu nào thực sự đọc được ở320px; chữ phụ quá nhỏ thì bỏ/bố trí lại, không ghi chung “mọi chữ đều rõ”. Mô tả những gì thực sự nhìn thấy và lỗi còn lại; các boolean `true` hay “đã xem/đúng nguồn” không thay nhận xét ảnh.
- `status`: `NEEDS_FIX`, `INSUFFICIENT_SOURCE` hoặc `PASS_FINAL_VISUAL_QA`; chỉ dùng PASS khi không còn lỗi thuộc các tiêu chí trên.

Agent chính phải tự mở JPEG cuối và bản320px khi nhận kết quả agent phụ; không chỉ chép kết luận PASS. Tách kết quả kỹ thuật, nguồn/claim và thiết kế; cả ba phải đạt trên cùng JPEG/hash mới được PASS cuối. Metadata validation, hash, font cmap và kích thước đúng chỉ là kiểm kỹ thuật, không chứng minh đẹp/đọc được/không che/crop. Không tự chấm CTR hoặc hiệu quả.

## Chặn upload/Publish/bàn giao khi còn lỗi

Khóa file/revision/hash được chọn sau review. Nếu còn lỗi, sửa trước bước remote tiếp theo; không upload/Publish hoặc thông báo hoàn tất/gửi nhóm bằng ảnh chưa đạt. Việc người dùng duyệt kịch bản hoặc bố cục video không tự là duyệt thumbnail. Trong workflow trọn gói đã được giao, agent tự sửa/kiểm và tiếp tục; không tạo vòng xin phép thumbnail mới nếu người dùng không yêu cầu duyệt riêng.

Sau Save, đợi hoàn tất, reload Studio, so ảnh thực hiển thị với JPEG đã khóa và giữ nguyên các trường ngoài phạm vi. Ghi ảnh chụp/readback đúng revision rồi mới ghi `VERIFIED`. Nếu workflow có gửi nhóm/bàn giao, bằng chứng thumbnail phải thuộc revision hiện hành đã xác minh, không dùng trạng thái Public hay ảnh cũ để bỏ qua cổng này. Khi phiên bản mới được chọn, kiểm các trường thumbnail/file/hash liên quan trong checkpoint/manifest có thống nhất; giữ bản cũ trong lịch sử, không sửa thành bằng chứng đã duyệt.

## Kiểm lỗi ghép ảnh trước khi bàn giao —23/10/2026

Người dùng yêu cầu tự phát hiện và sửa lỗi ghép, không chờ nhắc. Kiểm trên JPEG cuối sau mọi bước hoàn thiện, mở cả1280px và320px; xuất thêm vùng cận khi có nghi vấn ở mép chủ thể. Trong workflow đã giao đăng/lên lịch, tự sửa rồi tiếp tục, không tạo một vòng xin duyệt mới chỉ vì ảnh nháp lỗi.

- Rà mép tóc/xe/sản phẩm: không quầng trắng/đen, nền cũ sót quanh chủ thể, đường cắt gãy, mép nhòe hoặc bóng dính sang ảnh khác. Tách theo đường bao vật thể khi dùng cutout; không dùng feather rộng để che mép cắt chưa sạch.
- Rà bố cục và vật thể: bánh xe, cản, hốc đèn, sản phẩm không bị crop ngoài ý đồ hoặc bị chữ che; không kéo méo tỷ lệ, sinh thêm chi tiết hay dùng biển số/logo giả để lấp chỗ trống. Giữ chủ thể trong khung và có lề phù hợp.
- Đồng bộ nguồn sáng/độ nét/phối cảnh giữa xe và nền thiết kế: hướng bóng, màu môi trường và độ tương phản phải có chủ ý. Bỏ phản chiếu/sương/vệt sáng AI làm sơn xe loang hoặc mất chi tiết. Điều này KHÔNG cho phép đổi màu/cường độ ảnh beam thật để ép khớp palette; các mẫu sáng giữ đúng nguồn và được trình bày rõ là vùng đối chiếu.
- Ghép cảnh sáng: giữ toàn bộ phần chứng minh gồm chân/cutoff, vùng phủ và hai mép quan trọng. Chỉ cắt phần trời/nền thừa đã xem; không co dải sáng thành vệt mỏng, không hòa beam vào thân xe. Vùng mẫu/nhãn phải đủ chỗ riêng, rõ nguồn và nhiệt màu; không để overlay mới cắt chữ cũ.
- Ghi `composite_qc` trong thumbnail-review.json: vùng đã kiểm, lỗi thấy trên bản trước, cách sửa và nhận xét bản cuối gắn đúng file/hash. Có lỗi thì `NEEDS_FIX`; không dùng kích thước/hash, prompt đúng hoặc PASS trước đó thay kiểm trực quan. Chỉ bàn giao/upload bản đã tự sửa xong và qua cả kiểm đầy đủ lẫn mobile.

Bổ sung từ phản hồi cùng ngày: qua kiểm kỹ thuật và mép ghép sạch vẫn chưa đủ nếu tổng thể nặng chữ, nền/phản chiếu lấn át xe hoặc các mẫu sáng bị xếp thành cột rời rạc. Người dùng chê toàn bộ thiết kế thì đổi hướng bố cục, giảm chữ và chi tiết trang trí; không chỉ sửa crop hoặc đổi màu rồi coi là làm lại. Giữ các mẫu sáng thật đầy đủ nhưng tổ chức lại theo phân cấp chung của ảnh, không dùng hiệu ứng hòa trộn lem để che đường ghép.

Reference xe/sản phẩm/cảnh sáng phải là frame thật từ clip và được lưu ánh xạ asset/timestamp. Theo quy trình mới23/10/2026, ImageGen tạo toàn artwork trực tiếp từ các reference này; không tự ghép bù ảnh/chữ/logo bằng code. Không nhận artwork AI là ảnh trích clip nguyên bản; so nhận diện/model và từng màu với nguồn, không tạo hiệu năng thiếu bằng chứng hay thay ba cảnh bằng gradient/swatch. “Nổi bật/CTR cao” là mục tiêu thiết kế, không cam kết số CTR. Giữ tương phản vừa phải.
