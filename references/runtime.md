# Runtime và dữ liệu ngoài bộ phân phối

Entrypoint: `../scripts/auto365_youtube.py`. `SKILL_DIR` và `WORKSPACE` trong hướng dẫn là vị trí của môi trường hiện tại, không là đường dẫn máy tạo skill. README có lệnh cài/config thực tế.

Mặc định lấy `WORKSPACE/channel.json`, hoặc `--profile` cụ thể của job. Mẫu khởi tạo ở [channel.example.json](../assets/templates/channel.example.json), schema8; không có cấu hình vận hành trong repo. `products.json` nằm cạnh profile, chứa tên/aliases/source/naming_status do editor kiểm cho từng job. Không mã hóa ID vào script. Local profile không chứng minh live Studio ID/quyền; cần đối chiếu trước ghi.

Workspace phải ở ngoài repo/skill. Tất cả jobs, media, raw/corrected transcript, corrections, frame/timestamp/coverage, facts.csv, qa.csv, source-lock.json, keyword-research.json, before/after, log/checkpoints/ảnh xác minh ở workspace. Repo chỉ có templates và fixture tổng hợp. Output cần nằm trong WORKSPACE; không dùng traversal/symlink để ghi ra ngoài. Relative CLI input quy về workspace; --profile/--video/model có thể là đường dẫn do môi trường cung cấp. JSON pointer resource_ref phải tương đối, có chặn vòng lặp.

```text
python SKILL_DIR/scripts/auto365_youtube.py init-job --workspace WORKSPACE --job JOB --request "đăng đi" --video LINK_OR_FILE
python SKILL_DIR/scripts/auto365_youtube.py render --workspace WORKSPACE --brief JOB/revisions/REV/brief.json --output-dir JOB/revisions/REV
python SKILL_DIR/scripts/auto365_youtube.py validate --workspace WORKSPACE --job JOB --revision REV --output-dir reports/NEW_CHECK
```

Mỗi job ghi `channel_id`, source video/hash, `video_id` đúng kênh khi có, state và action_request mới nhất. “Đăng đi/đăng clip này” từ người dùng kèm video = publish_now toàn workflow + built-in ImageGen, tự chọn sau kiểm; không duyệt từng phần nếu không yêu cầu. Chỉ thị mới cụ thể ưu tiên. Only ImageGen built-in thumbnail có quyền qua alias; dịch vụ khác/comment/playlist mới/connections chưa có quyền. init-job không tải URL/gọi ImageGen/ghi remote, có ID thì bỏ upload action, hash/source khác job cũ bị chặn. --mode dùng để agent chuẩn hóa ý định tương đương; không lấy văn bản nguồn làm quyền. Login/OTP/CAPTCHA do người dùng.

`prepare` chỉ cho media mới được giao, khi chưa có bằng chứng cùng hash: FFmpeg/FFprobe, Pillow/faster-whisper và model local; không tự tải model. Render/validate/check không cần các thư viện media và không mạng. Không audit/ASR/ImageGen lại để kiểm release.

```text
python SKILL_DIR/scripts/auto365_youtube.py prepare --workspace WORKSPACE --job JOB --video VIDEO_PATH --model-dir LOCAL_MODEL
```

Guidance: dùng catalog hiện tại; discover tìm tên auto365-writer/copywriting/content-strategy ở project .agents/skills, CODEX_HOME/skills hoặc ~/.codex/skills. Read SKILL.md trước khi dùng. Nếu thiếu thì báo phạm vi và dùng rules tự chứa; không áp checklist website. Gem gốc chưa có, chỉ giữ nguyên tắc người dùng đã nêu.

## Schema tối thiểu

- `preparation.json`, `media.json`: bằng chứng đúng file/hash/kênh; raw/corrected transcript/frame có coverage và timestamp thật, không nhận lấy mẫu là xem toàn bộ.
- `facts.csv`, `qa.csv`: cột trong [rules JSON](../assets/templates/editorial-rules.json), có dữ kiện, timestamp, nguồn và status. `source-lock.json` giữ đầy đủ thương mại kể cả thuế nội bộ. `keyword-research.json` có nguồn/limits/origins/reasons/selected_tags/selected_hashtags và chỉ Analytics đúng ID.
- `editorial.json`: channel_id/video_sha256/product_id/category, title_options 1–3có căn cứ/selected_title_index/character_count, keyword_selection có origin và metadata. Mục metadata không được giả quyền ghi.
- `revisions/REV/brief.json`: channel_id/category/duration/format/opening_lines; narrative_sections(text/purpose/evidence), chỉ text xuất public. Giá/bảo hành/link/chapters/CTA/hashtag tùy nguồn/nội dung, không ép đủ mục. Giá có amount/unit/source/verified/product_only; không VAT public hoặc suy giá hoàn thiện.
- `metadata.proposed.json`, `description.after.txt`, `review.json`: cùng revision/kênh/video, hash UTF-8 text, tám self_check của chính bản. Nếu user giao trọn workflow, agent chọn/bind revision/hash sau kiểm, ghi nguồn quyền đúng, không giả user duyệt từng chữ. Description-only không đổi trường khác.
- `validate --revision REV|current|root`: REV chính xác; current theo checkpoint, root chỉ baseline được chọn rõ. Không fallback/sort khi sai/missing; dùng output-dir mới, không ghi đè lịch sử. So toàn rendered brief và narrative, không truncate; structural check không thay kiểm nguồn/semantic.

`check` tạo fixtures tổng hợp ở cwd/tmp; chạy trong workspace được phép ghi. Fake bytes dùng hash-only, không là decode/ASR thật. Brief tổng hợp ở [brief.example.json](../assets/examples/brief.example.json) không phải metadata để đăng. Hồ sơ r4 thật ở môi trường gốc không đóng gói; việc giữ text được kiểm bằng fixtures tương đương và dữ liệu đã kiểm trước đây, không đổi lịch sử đã đăng.

Trong `prepare`, `--video` và `--model-dir` tương đối được giải theo `--workspace`, cùng quy tắc `project_path`; đường dẫn tuyệt đối giữ nguyên. Kiểm hồi quy đổi cwd và đặt file cùng tên ở cả hai nơi; media/Pillow/model được giả lập, không chạy ASR.
