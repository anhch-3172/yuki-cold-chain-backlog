# Task breakdown

## 1. Nguyên tắc chia task
**Độ hạt**
- Issue lá (issue không có sub-issue, hoặc sub-issue) làm xong trong **≤ 3 ngày của 1 người**, tương đương **≤ 8 SWP (≤ 20 giờ)**.
- **Tách sub-issue** khi: (1) skill `swp-estimator` chấm ≥ 13 SWP; hoặc (2) issue chứa nhiều quy tắc nghiệp vụ **test được độc lập** — mỗi quy tắc một sub-issue để test, review và estimate riêng.
- **Mỗi ràng buộc đặc thù của đề là một issue riêng** (giờ lái 2024, 2 loại hạn, cửa sổ giao theo hợp đồng, đảo ngày) — không gộp vào issue UI chung.
- Dừng chia khi một issue chỉ còn một trách nhiệm (một quy tắc, một API, hoặc một khối UI) và có tiêu chí xong kiểm được.

**Định nghĩa xong (DoD)**
1. Code + unit test, gồm các test case R-06 liên quan (ghi trong mô tả issue).
2. API ghi: `requireRole` + validate zod + `writeAudit` (ADR-001).
3. Pull Request được **người** review và CI xanh (lint, test, build).
4. Nếu làm khác spec LAB-4: cập nhật spec / PREMISE trong cùng PR.

**Cách dùng Project**
- **Epic** = issue gắn label `epic`; issue thường là **sub-issue của epic**; issue lớn có sub-issue riêng (3 cấp: epic → issue → sub-issue).
- Field: `Status` (Todo → In Progress → In Review → Done; `Blocked` khi chờ bên ngoài), `Iteration` (Sprint 1–6, 2 tuần), `SWP` (đã review), `SWP reviewed` (Yes/No), `Giờ ước lượng`, `Phụ trách (giả định)`.
- Label: `epic`, `rang-buoc-dac-thu`, `gap-lab4`, `lam-ro`.
- Chỉ issue lá mang SWP và giờ; issue cha cộng dồn để xem tổng.

## 2. Spec → issue
| Spec (LAB-4) | Epic | Issue / sub-issue | Phần spec chưa thành issue và vì sao |
|---|---|---|---|
| SC-01, CS-01 | E1 | {{#E1-1}} | SSO/MFA — chờ IdP của khách (Q-07), ngoài phạm vi |
| CS-02, CS-03, CS-09, CS-10 | E1 | {{#E1-2}}, {{#E1-3}}, {{#E1-7}} | — |
| SC-46/47, SC-02 | E1 | {{#E1-5}}, {{#E1-4}}, {{#E1-6}} | Tạo / sửa user trên UI — làm bằng script, không cần cho vận hành 30–50 người |
| SC-03, SC-04 | E2 | {{#E2-1}}, {{#E2-2}} | Version hợp đồng theo ngày hiệu lực — chưa có yêu cầu đổi điều kiện giữa kỳ |
| ADR-005 (ngưỡng nhiệt) | E2 | {{#E2-3}} | — |
| SC-14 | E3 | {{#E3-1}} → {{#E3-1a}} {{#E3-1b}} {{#E3-1c}} {{#E3-1d}} {{#E3-1e}} | Máy quét mã vạch, ảnh hàng — phụ thuộc thiết bị (Q-05) |
| SC-19 | E3 | {{#E3-2}}, {{#E3-3}} | — |
| SC-22 | E4 | {{#E4-1}} | Nhận đơn qua SFTP ERP — chuyển thành issue làm rõ {{#E9-4}} |
| SC-24 | E4 | {{#E4-2}} → {{#E4-2a}} {{#E4-2b}} {{#E4-2c}} {{#E4-2d}} {{#E4-2e}}; {{#E4-3}}, {{#E4-4}}, {{#E4-5}} | — |
| SC-25 | E4 | {{#E4-6}} | — |
| SC-27 | E5 | {{#E5-1}}, {{#E5-2}} → {{#E5-2a}} {{#E5-2b}} | Quét barcode khi xếp xe (OPT-03) |
| SC-29 | E5 | {{#E5-3}} → {{#E5-3a}} {{#E5-3b}}; {{#E5-4}} | Offline 8h, ảnh / chữ ký thật — cần Service Worker + Storage, để Phase sau |
| SC-32 | E6 | {{#E6-1}}, {{#E6-2}} → {{#E6-2a}} {{#E6-2b}} {{#E6-2c}} {{#E6-2d}} {{#E6-2e}}; {{#E6-3}}, {{#E6-4}}, {{#E6-5}} | Ngoại lệ (nghỉ chia nhỏ đặc biệt, 2 người lái, đi phà — OPT-02); API bản đồ |
| SC-35, SC-36, SC-37 | E7 | {{#E7-1}} → {{#E7-1a}} {{#E7-1b}}; {{#E7-2}}, {{#E7-3}}, {{#E7-4}} | Datalogger realtime (OPT-04); gửi email/SMS cảnh báo (mail relay) |
| SC-40, SC-41 | E8 | {{#E8-1}}, {{#E8-2}} | Gửi thông báo recall (mail relay) |
| db-diagram #3 #10, ADR-002, ADR-008 | E9 | {{#E9-1}}, {{#E9-2}}, {{#E9-3}}, {{#E9-4}} | — |
| Màn ngoài phạm vi LAB-4 (migration, 12 báo cáo, legal hold, kiểm kê…) | — | — | Đã bỏ ở PREMISE LAB-4, không đưa vào backlog |

## 3. Hạng mục chịu ràng buộc đặc thù — giới hạn giờ lái xe tải từ 2024
| Ràng buộc | Issue | Vì sao tách riêng |
|---|---|---|
| Lái liên tục ≤ 4h; chỉ nghỉ (cộng dồn ≥ 30 phút) mới reset | {{#E6-2a}} | Quy tắc dễ sai nhất — spec LAB-4 từng sai (4h30 vs 6,5h); cần nhiều ca biên; chờ xác minh pháp lý |
| 拘束時間 / ngày: cảnh báo > 13h, chặn > 15h | {{#E6-2b}} | Hai mức (cảnh báo / chặn) khác hành vi publish |
| Nghỉ giữa ca ≥ 9h | {{#E6-2c}} | Cần dữ liệu tuyến hôm trước của tài xế — phụ thuộc khác các quy tắc trong ngày |
| Lái 9h/ngày (bình quân 2 ngày), 44h/tuần (bình quân 2 tuần) | {{#E6-2d}} | Quy tắc nhiều ngày, phát hiện thiếu khi break (P1-1) |
| Tích lũy 284h/tháng, 3.300h/năm, tăng ca 960h/năm | {{#E6-2e}} | Phụ thuộc dữ liệu chấm công bên ngoài — rủi ro tích hợp riêng |
| Bộ tham số có version | {{#E6-1}} | Luật đổi → thêm version, không sửa code (ADR-005) |
| Publish gắn rule_version, chặn khi vi phạm | {{#E6-4}} | Bằng chứng tuân thủ cho từng tuyến |
| Xác minh pháp lý OPS-LAW-01 | {{#E6-5}} | Việc của BrSE với khách, chặn E6-2a nếu chưa có kết luận |

Các ràng buộc đặc thù khác cũng tách riêng (label `rang-buoc-dac-thu`): 消費期限 / 賞味期限 {{#E4-2a}}, cửa sổ giao theo hợp đồng {{#E4-2c}}, đảo ngày {{#E4-2d}}, lane gạo / bò {{#E3-1a}}.

## 4. Chỗ hở / mâu thuẫn của spec LAB-4 phát hiện khi break
| Spec | Chỗ hở / mâu thuẫn | Xử lý |
|---|---|---|
| SC-32 | Không kiểm 9h/ngày bình quân 2 ngày và 44h/tuần dù tham số có trong `driver_rule_sets` | Đã sửa thiết kế — PREMISE P1-1 |
| SC-32, AS-31 | “Nghỉ ≥ 30 phút” không rõ có cộng dồn đoạn ngắn | Giả định — PREMISE G-02; tạo issue làm rõ {{#E6-5}} |
| SC-32 | Không định nghĩa ranh giới tuần | Giả định — PREMISE G-03 |
| SC-24 ⑤ ↔ ADR-004 | Đảo ngày lấy “lần giao gần nhất” nhưng không loại bản ghi đã bị đảo | Đã sửa thiết kế — PREMISE P1-2 / G-04 |
| ADR-009 ↔ SC-22 | Nhiều shipment / đơn nhưng trạng thái đơn vẫn là một giá trị | Đã sửa thiết kế — PREMISE P1-4 / G-05 |
| ADR-005 | Cần màn duyệt version nhưng không có SC | Đã sửa thiết kế (thêm) — PREMISE P1-3 |
| SC-36 | Quá SLA 15 phút rồi làm gì | Đã sửa thiết kế (khóa nghĩa, không thêm phạm vi) — PREMISE P1-5 |
| API_List DLH-2 | Endpoint có trong repo, spec không mô tả mục đích / quyền | Hướng đã chốt — PREMISE mục 3; issue {{#E4-6}} |
| SC-22 ↔ IF-ERP-01 | Đặc tả file ERP chưa có (Q-04) | Tạo issue làm rõ {{#E9-4}} |
| SC-29 | Bộ bằng chứng POD chuẩn chờ khách xác nhận (Q-19) | Để mở — đã cấu hình theo business-rules; đổi bộ bằng chứng chỉ là cấu hình, không chặn sprint nào |
