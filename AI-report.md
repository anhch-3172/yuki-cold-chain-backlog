# AI-report — LAB-5

## 1. Skill và prompt đã dùng
| Việc | Công cụ / skill | Cách viết prompt / cách làm |
|---|---|---|
| Break task | Claude (claude.ai), đầu vào là bộ `specs/` LAB-4 + bảng traceability + bảng đối chiếu DB | Yêu cầu theo luật cố định: issue lá ≤ 8 SWP; mỗi ràng buộc đặc thù một issue; mỗi gap LAB-4 một issue; ghi `spec` nguồn cho mọi issue. Yêu cầu AI **liệt kê chỗ hở của spec** gặp trong lúc break, không tự lấp |
| Chấm SWP | Skill tự viết `skills/swp-estimator` (rubric + `swp_score.py`) | AI không “cảm” điểm: chỉ gán **yếu tố đếm được** (màn hình, API, bảng, số nhánh, cờ đặc thù / toàn vẹn / tích hợp) kèm căn cứ; script tính SWP theo ma trận, tự chọn issue mẫu cho người kiểm |
| Quy giờ | Bảng quy đổi cố định trong rubric, script áp dụng | Không ước giờ trực tiếp; giờ luôn tính từ SWP đã chốt |
| Ghi SWP lên Project (Agent) | Claude Code + `gh` CLI chạy `tools/setup_github_project.py` và `skills/swp-estimator/scripts/push_to_project.sh` | Agent khớp issue theo tiền tố `[id]` trong tiêu đề, ghi `SWP`, `Giờ ước lượng`, `SWP reviewed = Yes`; **chỉ chạy sau khi người review chốt** `overrides.json` |
| Báo cáo tiến độ | Claude, dữ liệu `plan.json` + `burndown.json` | Bảng trạng thái, burndown, rủi ro **sinh từ cùng một dữ liệu** với Project, không viết số tay |

## 2. Review output của AI
**Người review ở các bước**
1. Duyệt danh sách epic và luật chia task trước khi break.
2. **Chốt điểm** 23 issue mẫu skill chọn: chấp nhận đề xuất sửa 4 (E6-2a, E6-2d, E4-2d tăng; E2-2 giảm), giữ 19 kèm lý do (`estimate.md` mục 1).
3. Duyệt kế hoạch 6 sprint và kịch bản giả lập Sprint 1.
4. Kiểm Project sau khi Agent tạo (cửa sổ ẩn danh, đúng cấp epic → issue → sub-issue).

**Vấn đề phát hiện trong output AI và cách xử lý**
| Vấn đề | Phát hiện bằng | Xử lý |
|---|---|---|
| Skill bản đầu chọn **30 / 53** issue làm “mẫu” — quá nhiều để người kiểm thật sự đọc | Đếm kết quả lần chạy đầu | Thu hẹp luật “sát ranh giới” chỉ cho SWP ≥ 8 → 23 issue; ghi lý do vào rubric |
| Skill **đánh giá thấp** quy tắc đặc thù ít bảng (E6-2a, E6-2d, E4-2d = 3 SWP) vì Scope chỉ đếm màn / API / bảng | Luật “đặc thù mà SWP ≤ 3” đưa chúng vào mẫu; người review đối chiếu lịch sử lỗi spec LAB-4 | Nâng lên 5; giữ nguyên rubric nhưng ghi nhận điểm yếu (mục 3) |
| Skill **đánh giá cao** CRUD nhiều endpoint (E2-2 = 8) vì đếm 4 endpoint cùng khuôn như 4 việc | Mẫu “SWP cao nhất epic” | Hạ xuống 5 |
| Script Agent đọc CSV bằng dấu phẩy — hỏng khi tiêu đề tiếng Việt có dấu phẩy | Tự rà script trước khi giao | Xuất thêm `swp.tsv` chỉ gồm id / SWP / giờ cho Agent |
| Câu giải thích E6 ghi “tỷ lệ giữ lại 17%” trong khi số tính ra 26% | Đối chiếu text viết tay với bảng sinh từ dữ liệu | Sửa text; giữ nguyên tắc: số liệu chỉ sinh từ dữ liệu |
| Kế hoạch giả định velocity 40 SWP, Sprint 1 giả lập chỉ đạt 24 | Burndown | Ghi thành rủi ro, giảm cam kết Sprint 2 xuống 32 SWP thay vì giữ số đẹp |
| Thư mục tạo bằng `{a,b}` không chạy trên shell (lặp lại từ LAB-2, LAB-4) | stderr | Tạo từng thư mục; đưa vào danh sách lỗi lặp cần tránh |

## 3. Điểm đặc biệt
**Tin là hiệu quả**
- **Điểm có căn cứ**: SWP tính từ yếu tố đếm được, nên người review tranh luận về *yếu tố* (“E2-2 có thật 4 việc khác nhau không?”) thay vì về *con số*.
- **Một nguồn dữ liệu**: `backlog.json` → skill → HTML / markdown / Project. Đổi một điểm là mọi nơi đổi theo, không lệch.
- **Ràng buộc đặc thù được ép tách** bằng luật của skill, không phụ thuộc trí nhớ người break.

**Chưa tốt, cần cải thiện khi làm thật**
- Rubric thiên về Scope (màn / API / bảng): quy tắc nghiệp vụ dày nhưng ít bảng bị chấm thấp — nên thêm yếu tố “số ca biên phải test”.
- Bảng quy đổi giờ là quy ước, chưa hiệu chỉnh bằng dữ liệu thật; cần đo lại sau 2–3 sprint.
- Sprint 1 là **giả lập** — trạng thái và burndown do người dựng kịch bản, không phải dữ liệu đội thật.
- AI không có quyền GitHub trực tiếp; mọi thao tác Project đi qua Claude Code trên máy PL.

**Câu neo**
- **P2-07** — Vận hành vai trò quản lý trong luồng AIDD: AI sinh backlog, điểm, script; người chốt luật, điểm và kế hoạch; Agent thực thi trên Project.
- **P2-11** — Đánh giá độ tin cậy báo cáo do AI tổng hợp: phát hiện chỗ “tô hồng” (velocity 40 SWP giả định) và chỗ sai số (17% vs 26%) trước khi dùng.
- **P2-12** — Cổng chất lượng: SWP chỉ được ghi lên Project khi skill đã chấm **và** người review đã chốt mẫu (`SWP reviewed = Yes`).
- **P2-13** — Dùng AI tổng hợp báo cáo đợt (Sprint 1): trạng thái, burndown, rủi ro sinh từ dữ liệu Project, người kiểm trước khi gửi.
