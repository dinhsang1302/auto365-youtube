# Rà quảng cáo trước khi chốt nội dung

Policy revision: advertising-review-2026-10-15; bổ sung rules 8. Đây là bước biên tập, không phải kết luận tuân thủ pháp luật toàn diện.

## Nguồn và phạm vi

- [Luật 75/2025/QH15](https://vanban.chinhphu.vn/?classid=1&docid=214561&pageid=27160), hiệu lực 01/01/2026; đối chiếu Điều 8 Luật Quảng cáo hiện hành, đặc biệt khoản 9–11. [Văn bản hợp nhất 88/VBHN-VPQH](https://datafiles.chinhphu.vn/cpp/files/vbpq/2025/8/88-vbhn-vpqh.pdf).
- [Bộ VHTTDL giải thích Thông tư 12/2026/TT-BVHTTDL](https://bvhttdl.gov.vn/bo-vhttdl-ban-hanh-thong-tu-quy-dinh-chi-tiet-mot-so-dieu-cua-luat-quang-cao.htm), hiệu lực 05/07/2026: từ tương tự, hồ sơ chứng minh, thời hạn và thông tin nguồn trên sản phẩm quảng cáo.
- File “Luật Quảng Cáo” người dùng cung cấp là hướng dẫn nội bộ, không là văn bản quy phạm pháp luật. Giữ bản gốc và nhận xét trong hồ sơ riêng; không biến ví dụ, danh sách từ hay khuyến nghị thành điều luật. Tra lại nguồn chính thức/ngày hiệu lực khi luật thay đổi hoặc gặp claim đặc thù.

## Bước thực hiện

1. Trước chốt title/description/thumbnail/script, lưu `advertising-review.json` cùng revision: nguyên văn claim, bề mặt/timestamp, loại claim, nguồn/hồ sơ/ngày/phạm vi/điều kiện, Đạt/Cần sửa/Chưa xác minh, câu thay thế và phần còn lại. Video cũ lưu before/after, chỉ sửa trường được giao.
2. Rà vị thế dẫn đầu, độc bản, tuyệt đối: “mạnh nhất”, “tốt nhất”, “số một”, “duy nhất”, “một không hai”, “dẫn đầu”, “vượt mọi đối thủ” và cách diễn đạt tương tự kể cả tiếng nước ngoài. Xét ngữ cảnh; không cấm máy móc mọi chữ “nhất”, tên model hay “nhất quán”. Không thay từ đồng nghĩa để giữ nguyên claim thiếu chứng cứ.
3. Claim thuộc khoản 11 Điều 8: kiểm kết quả khảo sát của tổ chức hợp pháp có chức năng nghiên cứu thị trường hoặc chứng nhận tại cuộc thi/triển lãm/giải thưởng đúng quy mô/nội dung; kiểm thời hạn, tính độc lập/khách quan, phạm vi và tên/số/ký hiệu/ngày phải thể hiện theo Thông tư 12. Trang bán hàng, báo cáo thử nghiệm, bằng sáng chế và số đo nội bộ không tự chứng minh vị thế số một toàn thị trường. Thiếu hồ sơ phù hợp thì bỏ hoặc viết bằng đặc tính cụ thể có nguồn.
4. So sánh cần tài liệu hợp pháp phù hợp theo khoản 10 Điều 8 hiện hành. Khóa đối tượng/phiên bản, tiêu chí, đơn vị, điều kiện, thời điểm/phương pháp; không suy độ sáng/an toàn từ W/K. “Tăng 300%” khác “bằng 300%”. Thiếu cơ sở thì bỏ so sánh. Không khẳng định luật cấm mọi so sánh hoặc mọi phép so sánh bắt buộc qua phòng thử nghiệm độc lập khi chưa có căn cứ tương ứng.
5. Rà thông số, tương thích, giá/phạm vi, bảo hành, IP/chống nước, an toàn/không chói/phá sương, độc quyền, số cơ sở/quy mô thương hiệu. Website có ghi khác với có chứng chỉ/kết quả thử nghiệm; không mở rộng điều kiện hoặc biến ảnh minh họa thành kết quả đo. Câu thay thế cũng phải có nguồn, không có danh sách câu an toàn mặc định. Giá cũ khác giá hiện hành. Giữ không VAT và một chữ ký từ channel.json.
6. Rà lời nói, chữ trong video, thumbnail và metadata. Sửa metadata không xóa claim trong âm thanh/hình ảnh. Job sửa trường có sẵn: làm đúng phạm vi, ghi claim còn trong video/thumbnail và báo người dùng; không tự render/gỡ/đổi thumbnail/upload lại. Job xuất bản mới phải giải quyết claim trọng yếu trước publish; hỏi khi vượt quyền hoặc thiếu bằng chứng thiết yếu.
7. Review đúng revision trước lưu rồi readback. Script không thay thẩm định chứng cứ hoặc bảo đảm tuân thủ. Không tự tính phạt/cộng dồn chế tài/suy hồi tố từ bảng nội bộ. Đề xuất thận trọng hơn luật phải ghi là chính sách nội bộ.

## Hồ sơ tối thiểu

`checked_at`, `legal_sources[{url,effective_date,scope}]`, `coverage`, `claims[{original,surface,timestamp,evidence,status,decision,replacement}]`, `remaining_issues`, `revision`, `reviewer_scope`. Không công bố hồ sơ nội bộ vào mô tả hoặc chép toàn bộ tài liệu nội bộ vào bộ phân phối công khai.
