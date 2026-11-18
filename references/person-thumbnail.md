# Thumbnail có người: người + xe + sản phẩm

Người dùng chốt **18/11/2026**, thay câu cũ "có người hay không tùy bố cục" (15/10/2026). Áp dụng cho mọi thumbnail video dài được giao
(và Shorts khi được yêu cầu thumbnail). Đọc cùng [workflow ImageGen](imagegen-workflow.md), [packaging-style](packaging-style.md) và
[cổng chất lượng](thumbnail-quality-gate.md). Ảnh mẫu: `../assets/thumbnail-references/auto365-channel-nguoi-xe-san-pham-20261118.png`,
`../assets/thumbnail-references/auto365-channel-xlight-v12-transit-20261118.png`.

## Luật
1. **Clip có người** (người dẫn, kỹ thuật viên, chủ xe nói trước máy) → thumbnail **bắt buộc có người**, kết hợp với **xe** và **sản phẩm**.
   Không làm thumbnail chỉ có xe (+ chữ) khi clip có người. Chỉ bỏ người khi: clip không có người, mọi frame người đều hỏng
   (mờ, nhắm mắt, quay lưng, bị che), hoặc người dùng yêu cầu rõ. Bỏ người phải ghi lý do vào `thumbnail-review.json`.
2. **Chọn phân đoạn có người trước**: chạy `scripts/person_frames.py <video> <job>/thumbnail/person` để dò các phân đoạn có người và trích
   frame ứng viên (mặt lớn, nét, nhìn thẳng). Mở `person_contact.jpg`, chọn 1–2 frame tốt nhất. Thoát mã 2 = không có người → bố cục xe + sản phẩm.
3. **Tiêu chí frame người**: mặt rõ, **mắt mở**, nhìn vào máy, biểu cảm tươi/ngạc nhiên vừa phải; ưu tiên **cử chỉ hướng về xe/sản phẩm**
   (chỉ tay, cầm sản phẩm, xoè tay giới thiệu), thấy từ ngực/eo trở lên, áo đồng phục có logo thương hiệu. Tránh miệng méo giữa chữ, chớp mắt,
   tay che mặt, nghiêng đầu khó coi. Clip AI có dấu ✦ Gemini/Veo → không để dấu đó lọt vào reference.
4. **Đủ ba thành phần** đưa vào ImageGen làm reference riêng: frame người đã chọn + frame xe đẹp nhất (đúng xe của clip) + frame/ảnh sản phẩm
   thật (hộp, bóng, bi, camera, cuộn phim…). Ghi timestamp và vai trò từng ảnh.

## Bố cục (học từ mẫu kênh đã chốt)
- **Người** đứng một bên (trái hoặc phải, ~25–40% bề ngang), thấy từ eo/ngực lên, nhìn vào người xem; cử chỉ dẫn mắt về sản phẩm/xe.
- **Xe** vẫn lớn, ở phía còn lại hoặc phía sau người, thấy rõ mặt xe/vị trí lắp. **Sản phẩm** đặt gần tay người hoặc tiền cảnh, đủ to để nhận ra ở 320px.
- **Chữ** khối nghiêng trắng–vàng/đỏ (theo packaging-style) ở vùng trống phía trên/bên cạnh — **không đè mặt người**, không đè xe/sản phẩm/đèn.
- Clip nhiều người (câu chuyện, tư vấn) → tối đa 2–3 người, người nói chính lớn nhất; không làm thành lưới ô rời.
- Ảnh sáng/so sánh nhiệt màu (khi có) vẫn theo cổng thumbnail: thêm vào bố cục, không thay người.

## Trung thực về người
- Người trong thumbnail phải là **người thật trong chính clip** (giữ đúng khuôn mặt, kiểu tóc, đồng phục, logo áo). Không để ImageGen sinh người khác,
  không đổi mặt/giới tính/độ tuổi, không ghép người của video khác, không dùng người mẫu AI thay người dẫn.
- ImageGen được dựng lại ánh sáng/nền và tư thế tự nhiên quanh frame thật nhưng **không bịa cử chỉ cầm sản phẩm** mà clip không có
  nếu điều đó tạo thành tuyên bố (vd. đang lắp đặt); cầm/chỉ sản phẩm để giới thiệu là được.
- Không thêm tay/ngón thừa, logo áo méo, chữ trên áo sai — kiểm kỹ ở bản lớn.

## Kiểm trước khi chốt (ghi vào `thumbnail-review.json` → `person_check`)
- `has_person_in_clip` (theo `person_frames.json`), `person_frame_t` đã dùng, `kept_identity` (so mặt với frame gốc), `eyes_open`,
  `gesture`, `text_not_on_face`, lý do nếu bỏ người.
- Ở bản 320px vẫn nhận ra: người (mặt), xe, sản phẩm và chữ chính. Thiếu một trong bốn → sửa bằng ImageGen, làm revision mới.
