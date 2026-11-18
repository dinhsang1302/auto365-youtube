# Auto365 YouTube — skill Codex + Claude Code

Bản **1.0.18**, đồng bộ ngày **18/11/2026**. Chạy trên **Codex** và **Claude Code** (xem mục "Dùng trên Claude Code"). Skill giúp Codex đọc video, kiểm nguồn, viết tiêu đề/mô tả/tags/hashtag, tạo thumbnail khi áp dụng, đăng hoặc lên lịch và xác minh trong YouTube Studio.

## Cài đặt trên Windows

Cần có Codex và Git. Chạy trong PowerShell:

```powershell
$auto365SkillsRoot = if ($env:CODEX_HOME) { Join-Path $env:CODEX_HOME 'skills' } else { Join-Path $env:USERPROFILE '.codex\skills' }
$auto365SkillDir = Join-Path $auto365SkillsRoot 'auto365-youtube'
New-Item -ItemType Directory -Path $auto365SkillsRoot -Force | Out-Null
if (Test-Path -LiteralPath $auto365SkillDir) { throw 'Đã có auto365-youtube. Xem mục Cập nhật; không cài chồng.' }
git clone https://github.com/dinhsang1302/auto365-youtube.git $auto365SkillDir
```

Mở lại Codex, chọn workspace làm việc và kiểm tra skill `auto365-youtube` xuất hiện. Thư mục cài phải chứa trực tiếp `SKILL.md`, `agents`, `assets`, `references`, `scripts`; tránh lồng thêm `auto365-youtube-main` bên trong.

**Không dùng Git:** chọn **Code → Download ZIP** trên GitHub, giải nén, đổi tên thư mục chứa `SKILL.md` thành `auto365-youtube`, chép vào `%USERPROFILE%\.codex\skills\` hoặc `CODEX_HOME/skills` nếu đã cấu hình. Chỉ giữ một bản cài hoạt động; bảo toàn thay đổi riêng trước khi thay bản cũ.

macOS/Linux có thể clone:

```sh
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
git clone https://github.com/dinhsang1302/auto365-youtube.git "${CODEX_HOME:-$HOME/.codex}/skills/auto365-youtube"
```

Bản này kiểm trên Windows/Python 3.12; chưa kiểm media/Studio trên hệ điều hành khác. NAS Windows cần quyền truy cập riêng trên máy mới.

## Dùng trên Claude Code

```sh
git clone https://github.com/dinhsang1302/auto365-youtube.git ~/.claude/skills/auto365-youtube
```

Windows (PowerShell): `git clone https://github.com/dinhsang1302/auto365-youtube.git "$env:USERPROFILE\.claude\skills\auto365-youtube"`. Mở Claude Code trong workspace job và gõ như với Codex (vd. `dùng skill auto365-youtube đăng clip "D:\Video\Innova.mp4"`). Cần thêm **Codex CLI đã đăng nhập** (Claude Code gọi ImageGen của Codex qua `codex exec` để tạo thumbnail) và **tiện ích Claude in Chrome** (đăng/sửa YouTube Studio thay IAB). Thiếu Codex thì vẫn làm metadata, thumbnail báo chặn. Chi tiết: [claude-code.md](references/claude-code.md).

## Công cụ cần có

- **Python 3.12** là môi trường đã kiểm. Khởi tạo/render/validate/check chỉ dùng thư viện chuẩn. `render` là tạo **văn bản mô tả**, không thiết kế ảnh.
- **Trình duyệt tích hợp Codex (IAB)** có đọc/điều khiển trang và chọn file. Đăng nhập YouTube đúng tài khoản có quyền kênh; người dùng xử lý login, OTP/CAPTCHA.
- **FFmpeg/FFprobe trong PATH** để phân tích và trích frame video mới.
- Nhánh đọc media mới cần **Pillow, faster-whisper, ctranslate2, opencv-python-headless** và **model Whisper local**. Thumbnail clip có người: `scripts/person_frames.py` dò phân đoạn có người (model YuNet kèm sẵn ở `assets/models/`). Các phiên bản tham chiếu trong [requirements-media.txt](requirements-media.txt). Python, FFmpeg, model không nằm trong repo. Có thể dùng virtualenv ngoài skill:

```powershell
python -m venv "$env:USERPROFILE\Documents\Auto365YouTubeEnv"
& "$env:USERPROFILE\Documents\Auto365YouTubeEnv\Scripts\Activate.ps1"
python -m pip install -r (Join-Path $auto365SkillDir 'requirements-media.txt')
```

Nếu máy chặn kích hoạt script, gọi trực tiếp Python trong virtualenv; không cần đổi chính sách bảo mật Windows. Cung cấp đường dẫn model đã có cho Codex, không tự tải model hoặc gọi API trả phí.

- **ImageGen Skill và công cụ tạo ảnh thực sự** cần có khi làm thumbnail video dài hoặc được giao riêng. Shorts giữ ảnh từ video không cần ImageGen. Thiếu công cụ thì báo bước chặn, không tự thay bằng script/dịch vụ khác.
- `auto365-writer`, `copywriting`, `content-strategy` là guidance tùy chọn. Thiếu thì dùng rules tự chứa và báo giới hạn; không nhận đã đọc skill chưa có.

## Tạo workspace và cấu hình

Lưu jobs **ngoài thư mục skill**. Sau bước cài, chạy PowerShell:

```powershell
$auto365Workspace = Join-Path $env:USERPROFILE 'Documents\Auto365YouTubeJobs'
New-Item -ItemType Directory -Path $auto365Workspace -Force | Out-Null
if (-not (Test-Path -LiteralPath (Join-Path $auto365Workspace 'channel.json'))) {
    Copy-Item -LiteralPath (Join-Path $auto365SkillDir 'assets\templates\channel.example.json') -Destination (Join-Path $auto365Workspace 'channel.json')
}
if (-not (Test-Path -LiteralPath (Join-Path $auto365Workspace 'products.json'))) {
    Copy-Item -LiteralPath (Join-Path $auto365SkillDir 'assets\templates\products.example.json') -Destination (Join-Path $auto365Workspace 'products.json')
}
```

Mở workspace đó trong Codex. Profile mẫu hướng tới **Auto365 Review / @ChannelAuto365**, ID `UCfSB3t7meifCacbB4zOrW3w`. Đối chiếu profile và kênh live Studio trước ghi. Registry sản phẩm khởi tạo rỗng: bổ sung tên/model/nguồn theo clip, không lấy fixture tổng hợp làm dữ kiện thật. Logo trong profile mẫu giải theo `assets/templates` của skill trong catalog, không theo vị trí bản sao profile.

Chữ ký chỉ sinh từ `channel.json`: đèn/camera/phụ kiện **0365 365 911**; phim/PPF **0365 365 365**; phản ánh **1900 9365**. Không thay số theo website hoặc nối mẫu chữ ký khác.

## Sử dụng trong Codex

Gửi skill cùng file, đường dẫn máy/NAS hoặc link YouTube:

```text
$auto365-youtube đăng clip "D:\Video\Toyota Innova.mp4"

$auto365-youtube đăng clip "D:\Video\Toyota Innova.mp4", lên lịch 19:00 ngày 02/11/2026 giờ Việt Nam

$auto365-youtube đăng các Shorts sau, cách nhau 3 tiếng, bắt đầu 07:00 ngày 02/11/2026: [các đường dẫn]

$auto365-youtube chỉ chuẩn bị tiêu đề, mô tả, tags; chưa upload hoặc đăng: [file]

$auto365-youtube video [link]: chỉ sửa thumbnail, giữ nguyên tiêu đề, mô tả và lịch đăng
```

“Đăng clip này/đăng đi” kèm nguồn là giao trọn workflow và công khai sau kiểm. Chỉ thị cụ thể như xem trước, chuẩn bị, riêng tư, sửa duy nhất một trường hoặc lên lịch thắng mặc định. Script local chỉ tạo/kiểm hồ sơ; **Codex upload và đặt lịch qua IAB**, không cài scheduler/OAuth nền trên máy.

### Quy tắc hiện hành

- **Shorts không tạo thumbnail riêng:** giữ ảnh từ video, không gọi ImageGen hoặc thêm cover frame. Chỉ tạo thumbnail Shorts khi yêu cầu rõ.
- **Shorts dùng chữ ký gọn ba dòng:** thương hiệu → tư vấn đúng ngành → phản ánh. Không nối địa chỉ/maps/Facebook/bản quyền dài. Video dài giữ chữ ký đầy đủ.
- Thumbnail được giao: **video gốc → trích frame thật → ImageGen tạo toàn artwork → kiểm ảnh/chữ → xuất → cập nhật YouTube**. Không dùng code ghép xe/beam/chữ thay ImageGen. Premium automotive đỏ–đen–trắng, thống nhất, tương phản vừa phải. CTR là mục tiêu thiết kế, không cam kết.
- Lịch mặc định **GMT+7, giờ Việt Nam**. Ngày/giờ chưa rõ hoặc đã qua thì hỏi phần thiếu, không tự dời ngày hay đăng ngay. Lưu timestamp có offset và đọc lại lịch Studio.
- Kiếm tiền mặc định **Bật** theo quy tắc Auto365; chỉ thị mới hơn ưu tiên. Đánh giá quảng cáo theo nội dung thực, báo nếu còn xét duyệt/giới hạn.
- Không thêm playlist/bộ lọc hoặc báo nhóm mặc định. Dùng checkpoint/videoID chống trùng; không upload lại để sửa metadata.
- Tiêu đề có ngành hàng đúng clip, xe/model, hook đủ nghĩa. Không bịa thông số/giá/bảo hành/hiệu năng. Tags riêng Studio, hashtag riêng mô tả.
- **Báo mỗi clip theo dòng/mục đánh số, có link và trạng thái hoặc lịch đăng; không kẻ bảng.** Chưa tải/xử lý/xác minh xong phải ghi đúng tình trạng.

Chi tiết: [SKILL](SKILL.md), [rules](references/editorial-rules.md), [workflow](references/workflow.md), [browser](references/codex-browser-only.md), [ImageGen](references/imagegen-workflow.md), [cổng thumbnail](references/thumbnail-quality-gate.md).

## Cập nhật

Với bản Git, kiểm thay đổi riêng trước:

```powershell
git -C $auto365SkillDir status --short
git -C $auto365SkillDir pull --ff-only
```

Nếu có thay đổi local, lưu lại trước; không reset/ghi đè. Bản ZIP thì tải lại và thay thư mục sau khi bảo toàn tùy chỉnh. Giữ profile/products/jobs/video trong workspace riêng. Khi nâng bản cũ, đối chiếu `shorts_signature_template`, `shorts_consultation_label`, bản quyền video dài và policy mới; không thay toàn bộ profile làm mất cấu hình riêng. Git pull không tự cập nhật profile workspace. Mở lại Codex để nạp bản mới.

## Kiểm tra cài đặt

Chạy trong workspace ngoài skill, không cần YouTube/model để kiểm offline:

```powershell
Set-Location -LiteralPath $auto365Workspace
python (Join-Path $auto365SkillDir 'scripts\auto365_youtube.py') --help
python (Join-Path $auto365SkillDir 'scripts\auto365_youtube.py') check
python -m unittest discover -s (Join-Path $auto365SkillDir 'scripts') -p 'test_description_completeness.py' -v
```

Entrypoint duy nhất: `scripts/auto365_youtube.py`. Lệnh nâng cao (thay placeholder bằng giá trị thực):

```text
python SKILL_DIR/scripts/auto365_youtube.py init-job --workspace WORKSPACE --job jobs/clip-01 --request "đăng clip này, lên lịch" --video VIDEO_PATH --mode schedule --publish-at 2026-11-02T19:00:00+07:00
python SKILL_DIR/scripts/auto365_youtube.py prepare --workspace WORKSPACE --job jobs/clip-01 --video VIDEO_PATH --model-dir LOCAL_MODEL_PATH
python SKILL_DIR/scripts/auto365_youtube.py render --workspace WORKSPACE --brief jobs/clip-01/revisions/REV/brief.json --output-dir jobs/clip-01/revisions/REV
python SKILL_DIR/scripts/auto365_youtube.py validate --workspace WORKSPACE --job jobs/clip-01 --revision REV --output-dir reports/NEW_CHECK
```

`--workspace` độc lập vị trí cài; CLI input tương đối tính theo workspace. Mặc định đọc `WORKSPACE/channel.json`, hoặc chọn `--profile`. Output nằm trong workspace. Không chạy lại media/ASR để sửa metadata cùng hash. Với Shorts, agent xác minh format và chuẩn hóa quyền thumbnail theo SKILL; helper chưa tự phân loại Shorts. Xem [runtime](references/runtime.md).

Kiểm offline dùng bytes/brief tổng hợp, không phải media đã decode hay phép đo. Chưa kiểm toàn bộ Studio/ASR/ImageGen trên máy mới. Repo không kèm job sản xuất, transcript, Analytics, đăng nhập hoặc model. Logo/mẫu phong cách phục vụ workflow Auto365, không là giấy phép sử dụng thương hiệu tùy ý. [Bản kê đồng bộ](references/distribution-provenance.json) ghi hash nguồn và các điều chỉnh của bản GitHub.
