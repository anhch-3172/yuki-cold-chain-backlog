# PREMISE — Tiền đề của backlog LAB-5

Backlog break từ bộ thiết kế LAB-4 (nhánh `lab4-specs`, nộp 06/11/2026). Mục dưới đây chỉ ghi **chỗ backlog khác bản LAB-4 đã nộp** và các giả định / quyết định phát sinh khi break.

## 1. Spec thêm / bỏ / sửa so với LAB-4
| # | Spec (mã / file LAB-4) | Thêm/Bỏ/Sửa | Trước → sau | Vì sao | Issue bị ảnh hưởng |
|---|---|---|---|---|---|
| P1-1 | SC-32 Event Error, `business-rules` mục 8 | Sửa | Chỉ kiểm “lái trong ngày > 9h” → kiểm thêm **9h/ngày bình quân 2 ngày** và **44h/tuần bình quân 2 tuần** | Khi break E6-2 theo từng quy tắc, đối chiếu bảng tham số `driver_rule_sets` (AS-32) thấy 2 tham số bình quân có trong dữ liệu nhưng spec SC-32 không có nhánh kiểm | {{#E6-2d}} |
| P1-2 | SC-24 bước ⑤, `delivery_history` | Sửa | “Lần giao đã nhận gần nhất” → **bỏ qua lần giao đã bị đảo** (`source = reversal` / `reverses_id`); dòng migration không có lot_id vẫn dùng hạn | Khi break E4-2d: spec LAB-4 cho phép bản ghi đảo (ADR-004) nhưng không nói quy tắc đảo ngày xử lý chúng thế nào → kết quả sai nếu lấy bản ghi đã bị hủy làm mốc | {{#E4-2d}} |
| P1-3 | ADR-005 (hệ quả: “cần màn duyệt version”) | Thêm | Không có màn hình → **màn xem / duyệt version** cho `driver_rule_sets` và `temp_policies` (maker-checker) | ADR-005 ghi nhu cầu nhưng LAB-4 chưa có SC; không có màn thì đổi ngưỡng / luật phải sửa DB tay, trái mục tiêu “dữ liệu có version” | {{#E6-1}}, {{#E2-3}} |
| P1-4 | ADR-009, SC-22 | Sửa | Trạng thái đơn `shipped / delivered` chưa định nghĩa khi 1 đơn có nhiều shipment → **tổng hợp từ các shipment** (xem G-05) | Khi break E5-1 (shipment theo dải nhiệt): một đơn có tới 3 shipment, spec SC-22 vẫn mô tả 1 trạng thái đơn | {{#E5-1}}, {{#E5-3a}} |
| P1-5 | SC-36 B-5 (SLA 15 phút) | Sửa (giữ phạm vi) | Quá SLA chỉ đổi badge → **giữ nguyên**, ghi rõ: leo thang (gửi thông báo) thuộc tích hợp mail (mock) | Khi break E7-3 thấy “quá hạn rồi làm gì” không có trong spec; không thêm phạm vi, chỉ khóa nghĩa | {{#E7-3}} |

## 2. Giả định bổ sung
| # | Giả định | Chỗ spec / RFP để ngỏ | Ảnh hưởng tới issue / estimate |
|---|---|---|---|
| G-01 | Backlog là việc **hoàn thiện bản production từ prototype LAB-2** (tái sử dụng code, AI hỗ trợ sinh code); giờ = dev + unit test + tự review; QA hệ thống, BrSE, PM, buffer tính ngoài | LAB-4 không nói backlog làm lại từ đầu hay nối tiếp prototype | Toàn bộ estimate (504 giờ dev); giải thích chênh với LAB-1 trong `estimate.md` |
| G-02 | Nghỉ “cộng dồn ≥ 30 phút” chỉ cộng các đoạn nghỉ **≥ 10 phút**; hai giá trị là tham số trong `driver_rule_sets` | Spec SC-32 / AS-31 chỉ nói “nghỉ ≥ 30 phút mới reset”, không nói đoạn nghỉ ngắn có được cộng không; chờ xác minh OPS-LAW-01 | {{#E6-2a}} (đổi giá trị không phải sửa code), {{#E6-5}} |
| G-03 | “Tuần” cho 44h/tuần tính từ **thứ Hai 00:00 JST** | Không có định nghĩa ranh giới tuần | {{#E6-2d}} |
| G-04 | Lần giao có bản ghi đảo không dùng làm mốc đảo ngày | LAB-4 không nói (xem P1-2) | {{#E4-2d}} |
| G-05 | Đơn = `shipped` khi **mọi** shipment đã xuất xe; = `delivered` khi **mọi** shipment có POD | ADR-009 tách shipment nhưng chưa định nghĩa trạng thái đơn | {{#E5-1}}, {{#E5-3a}} |
| G-06 | Đội giả định: BE-1, BE-2, FE-1, QA-1, BrSE-1 (bán thời gian); sprint 2 tuần; velocity kế hoạch ~40 SWP / sprint | Đề yêu cầu “người phụ trách giả định” | Iteration, sắp xếp 6 sprint |
| G-07 | Sprint 4 (21/12–01/01) trùng nghỉ cuối năm → capacity giảm ~25% (kế hoạch 30 SWP) | Không có lịch nghỉ của đội | Phân bổ Sprint 4 |

## 3. Hướng đã chốt
| Vấn đề | Các phương án ở LAB-4 | Phương án chốt | Vì sao |
|---|---|---|---|
| Tính “lái liên tục” | (a) Chuỗi đoạn lái liên tiếp, bất kỳ đoạn không lái nào cũng ngắt · (b) Chỉ nghỉ mới ngắt (LAB-4 đã sửa theo prototype) | (b) + cộng dồn nghỉ có tham số (G-02) | Khớp nguyên tắc 2024 “gián đoạn lái về nguyên tắc là nghỉ”; tham số hóa để đổi theo kết quả OPS-LAW-01 mà không sửa code |
| API danh sách phiếu nhập (RCV-1 chưa có trong repo) | Bỏ C-3 khỏi phạm vi · Làm API | Làm API `GET /api/receipts` | Nhân viên nhận hàng cần xem lại phiếu vừa nhập để đối chiếu; chi phí nhỏ (2 SWP) |
| `POST /api/delivery-history` (DLH-2 có trong repo, spec chưa mô tả) | Bỏ endpoint · Giữ | Giữ, **chỉ cho ghi bản ghi đảo**, role admin / qa | `delivery_history` append-only (ADR-004) cần một đường chính thức để sửa sai bằng bản ghi đảo |
| Shipment và dải nhiệt | 1 shipment / đơn (thiết kế ban đầu) · 1 shipment / (đơn × dải) (prototype) | 1 shipment / (đơn × dải) | ADR-009 đã chấp nhận ở LAB-4; LAB-5 bổ sung trạng thái đơn (G-05) và kiểm xe cùng dải |
| Quy đổi estimate | Ước giờ trực tiếp từng issue · Quy đổi SWP → giờ theo bảng | Quy đổi theo bảng (skill `swp-estimator`) | Nhất quán, kiểm lại được; chi tiết trong `estimate.md` |
