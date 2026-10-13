# Quy tắc YouTube Auto365 — bản hợp nhất

Phiên bản 8, người dùng chốt ngày 13/10/2026, Asia/Bangkok. Đây là quy tắc hiện hành; thay các bổ sung trùng/mâu thuẫn trước đó. JSON cùng phiên bản: `../assets/templates/editorial-rules.json`. Bản cũ ở `workflow-history`, chỉ là lịch sử.

## 1. Kênh, quyền từng job và tiến độ

Kênh Auto365 Review / @ChannelAuto365: UCfSB3t7meifCacbB4zOrW3w. Nguyen Hoa là kênh test, vidIQ 365 Auto là kênh khác; không lấy Analytics hai kênh đó đánh giá Auto365. Xác minh phiên Studio/ID/quyền trước mỗi hành động ghi.

Chế độ thao tác lấy từ yêu cầu mới nhất của từng job, lưu ở `job.action_request`: chỉ chuẩn bị, sửa video đã có, upload riêng tư/không công khai, công khai hoặc lên lịch. Yêu cầu “chưa cập nhật YouTube” chỉ áp job/lượt đó, không thành lệnh cấm vĩnh viễn. Quyền cũ không thắng hạn chế mới; không suy quyền từ file metadata/cấu hình kênh. Đã được giao hành động cụ thể trên đúng video/kênh thì tiếp tục trong quyền ấy, không hỏi lại cùng thao tác. Khi chưa có hành động được giao, soạn để xem, không tự ghi remote. Dịch vụ tiêu hao credit, mua gói, đổi kết nối, tạo playlist và đăng bình luận phải có quyền riêng.

Video đã có dùng đúng video ID/kênh; không upload lại để đổi metadata. Lưu trước/sau đúng trường được giao. Khi cùng hash, tái dùng media/ASR/nguồn đã hoàn tất, không chạy lại audit. Ghi checkpoint/ý định trước thao tác cuối, lưu ID ngay khi có. Sau lưu, chờ Studio báo đã lưu và nút Lưu vô hiệu hóa; tải lại, đọc đúng nội dung revision/hash đã chốt, chỉ chuẩn hóa CRLF/LF và newline cuối. Với sửa mô tả, so title/tags/thumbnail/playlist/audience/visibility trước–sau để chứng minh không đổi trường khác. Lưu thời điểm, snapshot và ảnh; bấm Lưu chưa đủ để kết luận. Sau lỗi hoặc commit chưa rõ, kiểm Studio/video/checkpoint trước retry; không bấm đăng lại hoặc upload lại khi chưa biết kết quả. Đăng nhập/OTP/CAPTCHA để người dùng làm. Không lưu key/token/cookie/OTP. Runtime không lấy quyền publish cũ làm quyền mặc định cho lượt mới; phải ghi action_request mới nhất.

## 2. Đọc video, khóa dữ kiện và nguồn

Tự trích transcript bằng công cụ có sẵn, kết hợp xem frame; không bắt người dùng viết title hoặc dán transcript. Rà xe/đời/phiên bản, thương hiệu/model/SKU và thuật ngữ dễ sai ASR. Giữ raw và bản rà riêng; nêu phạm vi lấy mẫu/đoạn chưa đọc, không giả xem/nghe toàn bộ nếu chưa làm.

`facts.csv`: Dữ kiện | Nội dung nghe/thấy trong video | Timestamp đã kiểm | Nguồn đối chiếu | Trạng thái xác minh. Gồm khi có: ngành hàng/loại video; xe/đời/phiên bản; SKU; vấn đề/câu hỏi thật; cấu hình/thông số/test; giá/bảo hành; chi nhánh/link. Phân biệt video đề cập và nguồn hiện hành xác minh. Giá cũ không tự là giá đang áp dụng; không biến nhu cầu phổ biến thành lời/nhu cầu khách thật.

Nguồn đúng cấp: trang hãng/TDS khác thông tin phân phối, hồ sơ ca xe khác phép đo độc lập/báo giá. Khóa giá trị, đơn vị, phạm vi, nguồn/ngày đối chiếu và trạng thái trong `source-lock.json`. Dữ liệu nội bộ giữ đầy đủ giá, VAT/thuế, công/vật tư/phụ kiện, điều kiện/hiệu lực và giới hạn nguồn. Không làm mất dữ kiện thương mại chỉ vì không đưa chúng lên bản đăng.

`qa.csv`: Câu hỏi của người xem | Trả lời ngắn | SKU/xe liên quan | Timestamp | Nguồn | Trạng thái xác minh. Câu hỏi biên tập ghi rõ nguồn gốc, không giả lời khách. Bảng để nội bộ, dùng hỗ trợ mô tả/chapters/ý tưởng khi phù hợp; không nhét tất cả vào mô tả hoặc bảo đảm AI trích dẫn.

## 3. Nghiên cứu từ khóa, hashtag và tags

Tự nghiên cứu trước khi chốt metadata: đọc nội dung → tìm YouTube/web công khai → tham khảo cách gọi/metadata video cùng chủ đề → kết hợp truy vấn Analytics đúng channel ID khi có quyền/dữ liệu. Không audit lại chỉ để viết mô tả. Lưu query/URL/ngày/phạm vi quan sát/lý do/giới hạn ở `keyword-research.json`. Phân biệt Analytics quan sát, số liệu công cụ, tìm kiếm công khai và đề xuất biên tập; không bịa volume/độ khó/thứ hạng/trend/chuyển đổi. Search lỗi thì chọn theo dữ kiện đã kiểm, ghi giới hạn; chỉ hỏi thiếu thiết yếu. Không gọi dịch vụ tiêu hao credit ngoài quyền.

Chọn một cụm chính và các cụm phụ theo xe/sản phẩm/vấn đề/câu hỏi/địa phương thực. Không mặc định thêm mọi xe/brand/địa phương. Hashtag thường 6–10 nếu đủ liên quan; không lấp đầy. Chọn xe/model/brand/hạng mục/nhu cầu/Auto365 khi có, loại trùng nghĩa quá nhiều, sai model và trend chung. Rà cả title/description/tags.

Tags là trường riêng trong Studio, không trộn vào mô tả. Rà xe/đời/phiên bản, tên model/thương hiệu/cách viết hữu ích, hạng mục/nhu cầu thật, Auto365/Auto365 Review. Không cố đủ ký tự/số lượng; không thêm xe/model khác hoặc từ chung không liên quan. Đọc lại sau lưu. Bình luận ghim là đề xuất tùy yêu cầu: ngắn, câu hỏi cụ thể và một CTA; không tự đăng/ghim, không nhắc VAT trong bản đề xuất.

## 4. Title và mô tả tự nhiên

Khi viết mới title, tạo ba phương án theo góc nội dung cho phép: câu hỏi/vấn đề; sản phẩm/khác biệt có căn cứ; thi công/kết quả trên xe thật. Không bịa góc để đủ ba; góc giá chỉ dùng khi đã xác minh và phù hợp. Chọn một, đếm ký tự Unicode NFC thực tế, nêu lý do nhu cầu tìm kiếm/khớp video-thumbnail; không dự đoán CTR. Nhiệm vụ chỉ sửa description không tự viết lại title/thumbnail/tags.

Mô tả tự nhiên như người làm nghề giới thiệu ca xe. Hai dòng đầu vào xe/model/hạng mục và điểm đáng xem; câu rõ, đoạn ngắn, từ quen với chủ xe. Không mặc định “Cùng xem… trước khi chọn cấu hình”; không lặp “các anh”, không kể toàn checklist. Tránh giọng báo cáo như “phạm vi giá”, “cấu hình sản phẩm được giới thiệu”, “nội dung gồm”, “được trình bày để tham khảo”; không lặp “video giúp”, “theo công bố”, “có thể cân nhắc”, “cần kiểm tra” ở mọi đoạn. Không mở đầu sáo rỗng/giải pháp hoàn hảo/nâng tầm trải nghiệm.

Trả lời điều người xem cần: lắp ở đâu, điểm đáng chú ý có bằng chứng, giá sản phẩm và báo giá hoàn thiện, thông tin để tư vấn. CTA ngắn, rõ, dễ thực hiện. Không thêm lời khách/cảm nhận lái xe/kết quả chưa có căn cứ để làm câu hấp dẫn. SEO/AEO/GEO/AIO: chủ thể/model/đơn vị/giá nhất quán, từ khóa tự nhiên, câu trả lời đủ ngữ cảnh và link nguồn đúng nhu cầu; không FAQ/mật độ cố định, không hứa lên top/AI trích dẫn/đạt chuẩn hoặc chấm điểm hiệu quả chưa đo. Local SEO chỉ dùng cơ sở/địa phương thật đã xác minh.

Luồng triển khai gợi ý cho video dài, chỉ chọn phần có trong clip: vấn đề/nhu cầu → điểm đáng chú ý → tính năng và ý nghĩa với người dùng → lưu ý lựa chọn/thi công → giá/bảo hành nếu phù hợp → CTA. Link, timeline, chữ ký và hashtag bố trí theo nội dung và quy tắc dưới đây; không ép mọi video đủ các mục. Không bắt mọi video có hai link, giá, bảo hành, chapters hoặc FAQ. Độ dài theo nội dung, không ép bài SEO dài. Gộp lưu ý trùng, đặt giới hạn ngắn cạnh claim; ảnh minh họa khác test ca xe thì nói một câu rõ. Không ép câu về lux/công suất/điều kiện đo khi không liên quan. Dữ kiện thiếu và ghi chú nội bộ nằm ngoài bản đăng; không placeholder.

“Viết gọn” là bỏ câu thừa/lặp ý, không cắt giải thích hữu ích. Độ dài và số đoạn phụ thuộc định dạng, lượng nội dung và câu hỏi clip thực sự trả lời; không có chuẩn từ/ký tự chung ngoài giới hạn nền tảng. Với video dài, giữ chiều sâu tư vấn bằng bối cảnh, nguyên nhân lựa chọn và ý nghĩa sử dụng có bằng chứng. Với Shorts, mô tả ngắn theo nội dung thực, không kéo đủ dàn bài của video dài; không gọi Shorts chỉ từ thời lượng.

Nêu tính năng kèm ý nghĩa cho người dùng khi video/nguồn có căn cứ. Giải thích việc tính năng cho phép chọn/hiểu điều gì, giới hạn nào ảnh hưởng quyết định; không chỉ liệt kê thông số và không suy độ sáng/hiệu quả/an toàn từ công suất hoặc nhiệt màu. Lưu ý lựa chọn hoặc thi công được chọn vì giúp chủ xe hiểu, không là toàn checklist.

Giữ tinh thần giải thích vấn đề và trả lời câu hỏi chủ xe từ Gem cũ theo yêu cầu người dùng; bỏ sáo rỗng, lặp ý và claim thiếu nguồn. Chưa có bản Gem gốc thì không nhận đã đọc hoặc sao chép toàn bộ. SEO/AEO/GEO/AIO là câu trả lời rõ, đủ ngữ cảnh và dữ kiện nhất quán; không kéo dài bằng từ khóa.

`../assets/templates/description-templates.json` chỉ gợi ý mục đích/câu hỏi cho video dài và Shorts. Biên tập viên chọn/gộp/bỏ mục theo nguồn, ghi narrative_sections(text, purpose, evidence) trong brief; chỉ text được đưa lên bản đăng. Script không tự suy ý nghĩa sử dụng, không cắt đoạn theo số từ hoặc ép đủ mọi mục. Trước bàn giao kiểm thêm: bản rút gọn có mất giải thích hữu ích trong clip không; tính năng–ý nghĩa có nguồn không; chiều sâu có hợp định dạng/nội dung không?

## 5. Giá và bảo hành công khai

Mặc định **không nhắc VAT** trong description, CTA hoặc bình luận đề xuất. Giữ dữ kiện thuế và phạm vi thương mại đầy đủ trong nguồn nội bộ. Không thay bằng câu ngầm khẳng định đã gồm thuế, giá trọn gói hoặc tổng thanh toán.

Nếu giữ giá bộ đèn đã xác minh, dùng đúng giá/đơn vị:
“Giá bộ đèn tham khảo: 6.000.000 đồng/cặp. Liên hệ Auto365 để được tư vấn cấu hình và báo giá hoàn thiện theo xe.”
Đây là ví dụ diễn đạt giá, không là báo giá hay dữ kiện của job hiện tại, không là giá mặc định mọi sản phẩm. Script dùng giá và đơn vị có nguồn của từng job, bỏ phần giá nếu không phù hợp/chưa đủ nguồn. Không khẳng định công lắp, căn chỉnh và phụ kiện luôn thành khoản riêng khi nguồn chưa xác nhận. Bảo hành ngắn, đúng thời hạn và điều kiện đã kiểm; không suy bảo hành sản phẩm sang công lắp hoặc cả combo. Giá/bảo hành đều tùy nội dung, không bắt buộc.

## 6. Link, timeline và chữ ký

Ưu tiên link đúng sản phẩm/model/phiên bản trên auto365.vn; nếu không có thì hub/dịch vụ đúng nhu cầu. Mở kiểm đích, có lời dẫn rõ; không dựng URL hoặc thay bằng model khác. Hồ sơ xe/playlist/video liên quan chỉ thêm khi có URL thật phù hợp; không đủ URL thì bỏ, không placeholder. Không có số link bắt buộc.

Timeline từ thay đổi nội dung thật, đối chiếu transcript/âm-hình; không chia đều hoặc lấy tên/mốc từ ảnh mẫu. Nếu có, đặt TIMELINE CHI TIẾT trước chữ ký; timestamp + tên rõ, ưu tiên câu hỏi chủ xe. Chapters bắt đầu00:00, ít nhất3mốc tăng, mỗi đoạn kể cả cuối≥10giây. Mốc ước lượng chỉ nội bộ. Không ép chapters; khi sửa mô tả giữ mốc đã kiểm trừ khi được giao kiểm/sửa lại.

Nguồn chữ ký duy nhất: `workspace/channel.json` → `signature_template`; script `youtube_description.signature_for` chọn số theo ngành hàng và kiểm đúng mẫu/thứ tự hotline. Rules JSON tham chiếu cấu hình này, không chứa bộ số riêng. Dòng thương hiệu: AUTO365 | Hệ thống nâng cấp xe toàn quốc. Dòng tư vấn luôn có ký hiệu ☎. Tư vấn đèn/camera/phụ kiện0365 365 911; phim/PPF3M0587 365 365. Hotline nhập sỉ0369.878787 đặt ngay sau dòng tư vấn; hotline phản ánh chất lượng0969.878787 là tuyến riêng khác số. Cả hai cùng được giữ trong signature_template. Website, chi nhánh, địa chỉ trụ sở/bản đồ và Facebook dùng cấu hình người dùng đã chốt, không thay số theo website. Chọn tuyến chính của video; dịch vụ hỗn hợp chỉ ghi cả hai khi thật có và nhãn rõ. Chữ ký xuất hiện một lần sau hợp nhất mô tả mặc định. Không tự thêm số cơ sở/địa chỉ/hotline/chính sách chưa xác minh.

Thumbnail dùng tư liệu đúng video; nếu được giao ImageGen, xem ảnh tham chiếu và frame thật trước khi tạo. Học bố cục/màu/chữ, giữ đúng xe/model, không sao chép giá/thông số hoặc tạo chùm sáng giả thành bằng chứng test. Tạo 16:9, kiểm chữ tiếng Việt/model/hình ảnh, lưu vào job. Không đọc được ảnh tham chiếu thì báo phạm vi, không nhận đã xem. Chưa có quyền ImageGen thì không tự gọi; ảnh yêu cầu/tiến độ không tự là thumbnail.

## 7. Claim và tự kiểm

Không bịa/mặc định thông số, tương thích xe, giá, bảo hành, phép đo, kết quả, số chi nhánh, “phá sương”, “không chói”, “không cản sóng”, “không lỗi VETC”, “không ảnh hưởng bảo hành”, an toàn hoặc hiệu quả SEO. Không khái quát mọi phim kim loại gây phản chiếu taplo/chói mắt; chỉ nêu phạm vi có bằng chứng. Không công kích đối thủ/hù dọa/phóng đại. Rà theo ngữ cảnh, không kết luận mọi câu chứa từ nhạy cảm đều sai.

Dùng Đạt/Cần sửa/Chưa xác minh kèm lý do cho8mục: đúng xe/SKU/phiên bản; dữ kiện/nguồn/phạm vi; title khớp video/thumbnail; mô tả riêng/tự nhiên; link/CTA đúng; chapters nếu có; bản đăng sạch; chữ ký đúng tuyến/không lặp. Đọc như chủ xe: hiểu ngay chủ đề? đoạn giống báo cáo/lặp từ? chi tiết vô ích? dữ kiện/điều kiện quan trọng còn đủ? Tool kiểm cấu trúc không thay kiểm nguồn, không là bảo đảm kết quả.

## 8. Script và tài liệu dùng lại

`../scripts/youtube_editorial.py`: prepare/validate local, không cấp quyền hay ghi Studio. Validate bắt buộc chọn --revision <id|current|root>. current lấy ID từ checkpoint, không chọn bằng tên file mới nhất; metadata, review, description.after.txt và hash phải thuộc cùng revision. Không dùng self-check hoặc approval gốc thay review của revision đang sửa. Nội dung ghép từ brief phải khớp toàn bộ, gồm narrative_sections; thiếu text/purpose/evidence thì báo lỗi, không âm thầm bỏ đoạn. Kết quả kiểm ghi vào thư mục mới, không ghi đè validation lịch sử. `../scripts/youtube_description.py`: ghép các đoạn do biên tập viên viết/kiểm, phần giá/bảo hành/link/chapters tùy chọn; dùng một chữ ký và chặn VAT ở bản công khai. Nó không tự suy thông số/giá từ tên file hay tự viết cảm nhận. --workspace xác định project, hoặc dò marker rules từ cwd; tuyệt đối không lấy vị trí script làm workspace. Mọi output dẫn xuất nằm trong project, chặn traversal/symlink ra ngoài. Thiếu job/revision thì dừng, không tạo bản thay thế để validate.

Cả các script migration/consolidate/depth dùng một lần đều đã lưu lịch sử và entrypoint hiện hành ngừng chạy để không chèn lại quy tắc cũ. Workflow v1/v2 chỉ là pointer đã ngừng dùng tới workflow v3 hiện hành. Hồ sơ/video đã đăng và revision cũ giữ nguyên lịch sử, không giả là đã theo chuẩn mới. Website/FAQ/gói nhúng chỉ làm khi được yêu cầu; không áp H1/Schema/canonical/index hoặc ngưỡng chấm website vào YouTube.
