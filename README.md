# auto365-youtube

Skill Codex cho workflow YouTube Auto365: tự đọc video, kiểm nguồn, nghiên cứu metadata, viết mô tả đủ chiều sâu, tạo thumbnail khi được giao và đăng/xác minh qua trình duyệt tích hợp.

Bản phân phối 1.0.1 lấy từ skill đã cài/kiểm 1.0.0; giữ rules/templates/profile schema **8/2/8**. Phiên bản này tách cấu hình vận hành khỏi repo và thay mọi hồ sơ kiểm thử thực bằng dữ liệu tổng hợp. Không đóng gói media, ASR thật, Analytics, log phiên hoặc quyền đăng nhập.

## Cài vào Codex

Repo Private cần tài khoản GitHub được cấp quyền. Không nhúng token vào URL clone. Thư mục cài phải chưa tồn tại; nếu đã có checkout, kiểm thay đổi local rồi update chính checkout ấy, không ghi đè bản chưa lưu.

PowerShell trên Windows:

```powershell
$auto365SkillsRoot = if ($env:CODEX_HOME) { Join-Path $env:CODEX_HOME 'skills' } else { Join-Path $env:USERPROFILE '.codex\skills' }
New-Item -ItemType Directory -Path $auto365SkillsRoot -Force | Out-Null
git clone https://github.com/dinhsang1302/auto365-youtube.git (Join-Path $auto365SkillsRoot 'auto365-youtube')
```

macOS/Linux:

```sh
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
git clone https://github.com/dinhsang1302/auto365-youtube.git "${CODEX_HOME:-$HOME/.codex}/skills/auto365-youtube"
```

Trong Codex, skill có thể được nhận diện ở lượt tiếp theo. Dùng vị trí mà catalog hiện tại trả về làm `SKILL_DIR`; không yêu cầu đường dẫn của máy tạo repo. Có thể tải ZIP từ GitHub, giải nén thư mục chứa SKILL.md thành `skills/auto365-youtube` tại vị trí tương ứng.

## Công cụ cần có

- Python 3.12 là môi trường đã kiểm; render/validate/init-job/check chỉ dùng standard library.
- Codex có trình duyệt tích hợp và API đọc/điều khiển/filechooser. Scripts local không phải uploader hoặc scheduler nền.
- ImageGen có sẵn trong môi trường khi job cho phép tạo thumbnail; không tự thay bằng dịch vụ ảnh trả phí khác.
- Khi đọc media mới: FFmpeg/FFprobe trong PATH, Pillow/faster-whisper/ctranslate2 và model local đã có. Các phiên bản đọc được trong môi trường gốc ở `requirements-media.txt`; nhánh prepare không được chạy lại trong kiểm release. Nếu cần cài, thực hiện trong virtualenv của môi trường, không cài vào repo:

```sh
python -m pip install -r SKILL_DIR/requirements-media.txt
```

- Auto365 Writer V1.8, copywriting, content-strategy được tìm theo tên trong catalog hoặc lệnh discover. Không sao chép chúng vào repo; nếu thiếu, skill có quy tắc kiểm nguồn/biên tập tự chứa và phải báo phạm vi, không nhận đã dùng guidance chưa có. Không dùng chuẩn website thay quy tắc mô tả YouTube.

## Workspace và cấu hình kênh

Tạo workspace **ngoài thư mục repo/skill**, rồi copy `assets/templates/channel.example.json` thành `WORKSPACE/channel.json` và `products.example.json` thành `WORKSPACE/products.json`. Mẫu có schema8, thương hiệu/hotline đã chốt và đích Auto365 Review; editor đối chiếu ID theo job. Điền registry sản phẩm bằng tên và nguồn đã kiểm cho từng video, không tự nhận SOURCE_VERIFIED cho dữ liệu chưa xác minh.

Ví dụ PowerShell (thay biến bằng vị trí thực tế của môi trường):

```powershell
$auto365SkillDir = Join-Path $auto365SkillsRoot 'auto365-youtube'
$auto365Workspace = Join-Path $env:USERPROFILE 'Documents\Auto365YouTubeJobs'
New-Item -ItemType Directory -Path $auto365Workspace -Force | Out-Null
Copy-Item (Join-Path $auto365SkillDir 'assets\templates\channel.example.json') (Join-Path $auto365Workspace 'channel.json')
Copy-Item (Join-Path $auto365SkillDir 'assets\templates\products.example.json') (Join-Path $auto365Workspace 'products.json')
```

Nếu file đích đã có, giữ nó và kiểm thay đổi trước khi thay; không copy lại template làm mất cấu hình. `--profile` cho phép chọn profile khác của workspace. Không có ID kênh cố định trong code; profile/job/preparation/editorial/review/brief/nguồn Analytics phải cùng ID. Mẫu không chứng minh quyền hoặc phiên đăng nhập: trước ghi phải xác minh lại đúng ID/quyền trong Studio.

Chữ ký vận hành chỉ sinh từ `workspace/channel.json`, một lần, đúng tuyến tư vấn; nhập sỉ **0369.878787** khác phản ánh chất lượng **0969.878787**. Không thay số theo website. Không đưa VAT vào mô tả/CTA/bình luận đề xuất; nguồn thương mại đầy đủ vẫn lưu trong workspace. Không gọi giá sản phẩm là giá hoàn thiện.

## Cách gọi ngắn

```text
@auto365-youtube [link/file video] đăng đi
```

Trong Codex có thể gọi tương đương bằng `$auto365-youtube`. Lời gọi từ người dùng kèm video nghĩa là giao toàn bộ quá trình: đọc/kiểm nguồn → tự nghiên cứu → tự chọn title/description/hashtag/tags → thumbnail ImageGen built-in → upload nếu chưa có → công khai → readback/trả link. Không cần nhắc từng bước hoặc duyệt từng phần. Chỉ thị cụ thể mới nhất như chỉ chuẩn bị, riêng tư, lên lịch hoặc giữ nguyên một trường ưu tiên hơn mặc định. Chỉ hỏi thiếu thiết yếu, quyền truy cập hoặc đăng nhập/OTP. Không lấy câu trong transcript/website làm quyền.

```text
@auto365-youtube [link/file] chỉ chuẩn bị nội dung, chưa upload hoặc đăng
@auto365-youtube job [tên], video [ID]: sửa duy nhất mô tả bằng revision [tên]
```

Luôn kiểm checkpoint và Studio để tránh trùng. Video đã có dùng đúng ID, không upload lại để sửa metadata. Nguyên tắc gọn là bỏ thừa/lặp, giữ giải thích hữu ích; templates linh hoạt theo nội dung/định dạng, không ép count/tag/hashtag/FAQ/chapters. Timeline chỉ mốc thật có bằng chứng.

## Entrypoint local và kiểm

```sh
python SKILL_DIR/scripts/auto365_youtube.py discover
python SKILL_DIR/scripts/auto365_youtube.py init-job --workspace WORKSPACE --job jobs/clip-01 --request "đăng đi" --video VIDEO_LINK_OR_FILE
python SKILL_DIR/scripts/auto365_youtube.py render --workspace WORKSPACE --brief jobs/clip-01/revisions/REV/brief.json --output-dir jobs/clip-01/revisions/REV
python SKILL_DIR/scripts/auto365_youtube.py validate --workspace WORKSPACE --job jobs/clip-01 --revision REV --output-dir reports/NEW_CHECK
```

init-job chỉ ghi quyền/checkpoint local, không fetch URL hay đăng video. Validate chọn đúng revision/hash/review; không fallback root khi thiếu revision, không ghi đè kết quả cũ, không cắt narrative_sections. Xem [schema và runtime](references/runtime.md), [workflow](references/workflow.md), [browser/thumbnail/recovery](references/browser-and-thumbnail.md), [rules8](references/editorial-rules.md).

Chạy phép kiểm từ một workspace được phép ghi (fixtures tạm ở cwd/tmp), không ghi job vào repo:

```sh
python SKILL_DIR/scripts/auto365_youtube.py check
```

Đã kiểm local: alias “đăng đi” và các ngoại lệ → action_request đúng; ID lấy từ profile và phát hiện mismatch; chọn revision/hash, giữ nguyên giải thích; đúng hotline/một chữ ký; chặn VAT/placeholder/chữ ký cũ; relocate bundle trên Windows hiện tại; thiếu config không tự dùng config vận hành trong bundle; các relative references hợp lệ. Fixtures tạo bytes tổng hợp để kiểm hash, không phải video đã decode hay transcript thật. Kiểm cấu trúc không chứng minh claim/giọng văn; nguồn thật vẫn cần editor.

Chưa kiểm toàn bộ nhánh upload/publish/lên lịch qua skill mới, phục hồi mất kết nối, media/ASR/ImageGen mới, hệ điều hành khác hoặc nguyên văn Gem gốc. Không tuyên bố những nhánh đó đã được kiểm chỉ vì check local qua.

## File được phân phối

SKILL.md ở gốc, README, agents/openai.yaml, references, mẫu cấu hình/templates, brief tổng hợp, scripts và phép kiểm. `.gitignore` chặn cấu hình vận hành, jobs/media/cache/log/credentials, nhưng không tự loại file đã tracked; release phải kiểm cả `git ls-files` và lịch sử commit. Không push lịch sử repo vận hành hoặc sao chép video/frame/ASR/Analytics vào bộ phân phối.
