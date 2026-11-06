# Yuki Cold Chain — Backlog, GitHub Project & báo cáo tiến độ (LAB-5)

**Học viên**: chieu.hoang.anh · **Mã học viên**: anhch-3172 · **Đề**: Product B — Hệ thống quản lý chuỗi kho lạnh thực phẩm (giả lập)

## Tổng quan
- Backlog break từ bộ thiết kế **LAB-4 nộp ngày 06/11/2026** (repo prototype, nhánh `lab4-specs`, thư mục `specs/`).
- **PREMISE.md có thay đổi**: 5 điểm sửa / thêm spec (P1-1…P1-5), 7 giả định (G-01…G-07), 5 hướng đã chốt.
- **9 epic**, 6 issue cha, **53 issue lá** · **213 SWP · 504 giờ dev** (skill chấm 210, người review chốt 213).
- Sprint giả lập đã chạy: **Sprint 1 (09/11–20/11/2026)** — hoàn thành 24 / 43 SWP; kế hoạch tổng 6 sprint (đến 29/01/2027).

## Link
| | Link |
|---|---|
| Repo | https://github.com/anhch-3172/yuki-cold-chain-backlog |
| GitHub Project | https://github.com/users/anhch-3172/projects/1 |
| Báo cáo HTML của skill (trong repo) | [`swp-report/swp-report.html`](swp-report/swp-report.html) |
| Báo cáo HTML (xem trực tiếp qua GitHub Pages) | https://anhch-3172.github.io/yuki-cold-chain-backlog/swp-report/swp-report.html |
| Đã mở thử bằng cửa sổ ẩn danh | {{INCOGNITO_CHECK}} |

## Cấu trúc repo
| File / thư mục | Nội dung |
|---|---|
| `README.md` | File này |
| `PREMISE.md` | Tiền đề: spec thêm/bỏ/sửa so với LAB-4, giả định bổ sung, hướng đã chốt |
| `task-breakdown.md` | Nguyên tắc chia task, spec → issue, hạng mục ràng buộc giờ lái 2024, chỗ hở spec LAB-4 |
| `estimate.md` | Issue mẫu skill chọn để kiểm, cách quy ra giờ, tổng theo epic, so với LAB-1 |
| `progress-report.md` | Báo cáo Sprint 1: trạng thái, burndown, rủi ro trễ |
| `AI-report.md` | Cách dùng AI, review của người, điểm đặc biệt |
| `swp-report/` | Báo cáo HTML của skill chấm SWP + dữ liệu đã chấm (`backlog_scored.json`, `swp.csv`, `swp.tsv`) |
| `skills/swp-estimator/` | Skill tự viết: rubric Scope × Complexity, script chấm + báo cáo HTML, script Agent ghi SWP lên Project |
| `backlog/` | Dữ liệu đầu vào: `backlog.json` (issue + yếu tố chấm), `overrides.json` (điểm người chốt), `plan.json` (iteration, phụ trách, trạng thái) |
| `progress/` | Ảnh và dữ liệu burndown Sprint 1 |
| `tools/` | Script tạo GitHub Project, issue / sub-issue, field, và cập nhật trạng thái Sprint 1 |

## Spec → epic
| Spec (mã / file LAB-4, hoặc dòng PREMISE) | Epic trên Project | Ghi chú |
|---|---|---|
| SC-01, SC-02, SC-46/47, CS-01…03, CS-09, CS-10 | #1 — Nền tảng & phân quyền | — |
| SC-03, SC-04, ADR-005 (ngưỡng nhiệt), PREMISE P1-3 | #2 — Master data | Ngưỡng 3 dải nhiệt là chính sách riêng của Yuki, có version |
| SC-14, SC-19 | #3 — Nhập hàng & tồn kho | Truy xuất bắt buộc chỉ với gạo / bò (lane riêng) |
| SC-22, SC-24, SC-25, PREMISE P1-2 | #4 — Đơn hàng & phân bổ | 2 loại hạn; cửa sổ giao 1/3–1/2 theo hợp đồng; cấm đảo ngày theo lịch sử từng khách |
| SC-27, SC-29, ADR-009, PREMISE P1-4 | #5 — Xuất hàng & POD | Shipment theo dải nhiệt |
| SC-32, PREMISE P1-1, P1-3 | #6 — Lập tuyến & giờ lái xe tải 2024 | **Ràng buộc giờ lái từ 2024** — mỗi quy tắc một sub-issue |
| SC-35, SC-36, SC-37, PREMISE P1-5 | #7 — Nhiệt độ & HACCP | — |
| SC-40, SC-41 | #8 — Truy xuất & recall | — |
| db-diagram #3 #10, ADR-002, ADR-008 | #9 — Chất lượng, hạ tầng & tích hợp | — |
