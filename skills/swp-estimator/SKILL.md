---
name: swp-estimator
description: Chấm SWP (story weight point) cho backlog đã break theo ma trận Scope × Complexity, chọn issue mẫu để người review, xuất báo cáo HTML và ghi SWP + giờ lên GitHub Project. Dùng skill này mỗi khi cần ước lượng story point / SWP cho issue, review estimate do AI chấm, quy SWP ra giờ, hoặc cập nhật trường point trên GitHub Project — kể cả khi người dùng chỉ nói "estimate backlog", "chấm điểm task", "story point".
---

# SWP Estimator

Chấm điểm phải **giải thích được**: SWP không do mô hình "cảm" ra, mà tính từ các yếu tố đếm được của từng issue. Người review sửa yếu tố (hoặc ghi đè SWP kèm lý do), không sửa con số trống trơn.

## Đầu vào
`backlog.json` — danh sách issue lá (issue không có sub-issue, hoặc sub-issue). Mỗi phần tử:
```json
{"id":"E4-2c","epic":"E4","parent":"E4-2","title":"...","spec":"SC-24 bước ⑤",
 "f":{"screens":1,"apis":1,"tables":2,"branches":3,"special":true,"integrity":false,"integration":false},
 "why":"căn cứ ngắn cho từng yếu tố"}
```
Định nghĩa từng yếu tố, ma trận và quy tắc tách: đọc `references/rubric.md` trước khi gán yếu tố.

## Quy trình
1. **Gán yếu tố** cho từng issue từ spec (màn hình, API, bảng, số nhánh nghiệp vụ, cờ đặc thù / toàn vẹn / tích hợp). Ghi căn cứ vào `why`. Không có căn cứ trong spec → để yếu tố ở mức thấp nhất và ghi "thiếu căn cứ".
2. **Chấm**: `python scripts/swp_score.py backlog.json --out out/` → `backlog_scored.json`, `swp-report.html`, `swp.csv` (đọc bằng mắt), `swp.tsv` (cho Agent).
3. **Người review** mở `swp-report.html`, xem mục “Issue mẫu cần người kiểm” (script tự chọn: issue SWP cao nhất mỗi epic, issue mang ràng buộc đặc thù có SWP thấp, issue nằm sát ranh giới, issue bị cờ “phải tách”). Ghi quyết định vào `overrides.json`:
   `{"E6-2a": {"swp": 8, "reason": "..."}}` rồi chạy lại bước 2 với `--overrides overrides.json`. Báo cáo ghi cả điểm skill chấm và điểm người chốt.
4. **Ghi lên Project** (Agent): `bash scripts/push_to_project.sh out/swp.tsv <owner> <project-number>` — ghi trường `SWP`, `Giờ ước lượng`, `SWP reviewed = Yes` cho từng issue (khớp theo tiêu đề có tiền tố `[id]`).

## Quy tắc không được bỏ qua
- SWP ≥ 13 ở issue lá → **phải tách**; báo cáo đánh dấu đỏ.
- Issue mang ràng buộc đặc thù (vd giờ lái xe tải 2024, 2 loại hạn, đảo ngày) được cộng 1 bậc Complexity — không gộp vào issue UI chung.
- Không ghi SWP lên Project trước khi người review đã xem mục issue mẫu.
