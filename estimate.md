# Estimate

**Báo cáo HTML của skill**: [`swp-report/swp-report.html`](swp-report/swp-report.html) — xem trực tiếp: {{PAGES_URL}}/swp-report/swp-report.html
Skill: [`skills/swp-estimator`](skills/swp-estimator) (rubric: `skills/swp-estimator/references/rubric.md`). Dữ liệu chấm: `swp-report/backlog_scored.json`.

## 1. Issue mẫu skill chọn để kiểm
Skill chọn **23 / 53** issue theo 4 luật (SWP cao nhất mỗi epic · ràng buộc đặc thù mà SWP ≤ 3 · SWP ≥ 8 nằm sát ranh giới bậc · SWP ≥ 13). Người review **sửa 4, giữ 19**.

| Issue | Skill chấm (Scope × Complexity → SWP) | Bạn chốt | Lý do |
|---|---|---|---|
| {{#E1-6}} Trang chủ theo vai trò: việc cần làm, cảnh báo đang mở (SC-02) | S3 × C1 → **3** | **3** | Giữ 3: chỉ đếm số liệu từ 4 bảng, không có nhánh nghiệp vụ |
| {{#E2-1}} SKU: xem/sửa dải nhiệt, loại hạn 賞味/消費期限, lane truy xuất, warn_days (SC-03) | S2 × C2 → **3** | **3** | Giữ 3: form CRUD; loại hạn chỉ là giá trị chọn, logic dùng nó nằm ở E4-2a |
| {{#E2-2}} Khách hàng & hợp đồng KH-SKU: rule 1/3, 1/2, LABEL_DATE_ONLY, chưa chốt (SC-04) | S3 × C3 → **8** | **5** | Sửa: 4 endpoint cùng khuôn CRUD đã có trong prototype; nghiệp vụ chỉ hiển thị rule, không tính toán — skill đếm trùng |
| {{#E3-1b}} API RCV-2: ghi phiếu, sinh lô available/quarantine + deviation, idempotent | S3 × C2 → **5** | **5** | Giữ 5: 5 bảng trong 1 giao dịch nhưng khuôn đã có ở prototype; idempotent theo client_request_id đã thiết kế |
| {{#E3-1d}} Gap LAB-4: hiển thị dải nhiệt + cảnh báo “sẽ cách ly” trước xác nhận; nhãn hạn theo 賞味/消費期限 | S1 × C3 → **3** | **3** | Giữ 3: chỉ hiển thị dựa trên rule đã có ở E3-1a, không thêm logic |
| {{#E4-2a}} Bước ①: 消費期限 ≤ ngày giao chặn tuyệt đối; 賞味期限 gần hạn chỉ cảnh báo | S1 × C3 → **3** | **3** | Giữ 3: 2 nhánh rõ (chặn / cảnh báo), test R-06 T2 có sẵn |
| {{#E4-2d}} Bước ⑤: cấm đảo ngày so với lần giao ĐÃ NHẬN gần nhất của cùng khách + SKU | S1 × C3 → **3** | **5** | Sửa: Phải loại bản ghi đảo (source=reversal), chỉ lấy lần giao đã nhận, xử lý dữ liệu migration không có lot_id |
| {{#E4-3}} API preview / commit + RPC allocate_lot (khóa dòng, đồng thời) | S3 × C2 → **5** | **5** | Giữ 5: RPC allocate_lot đã có và đã kiểm trên PostgreSQL; việc chính là nối API + xử lý lỗi M_26 |
| {{#E4-4}} Gap LAB-4: allocation_runs.result thêm expiryDate, deadline, suggestedQty; sửa câu lý do đảo ngày | S1 × C2 → **2** | **2** | Giữ 2: thêm 3 trường vào JSON kết quả + sửa 1 câu |
| {{#E5-2a}} API kiểm trước xuất + xuất xe: ngưỡng theo dải, blocked → deviation | S2 × C4 → **8** | **8** | Giữ 8: ngưỡng theo dải + blocked → deviation + máy trạng thái shipment, đúng mức C4 |
| {{#E5-3a}} API POD: bằng chứng theo 車上渡し / 軒先渡し, shipment → delivered, ghi delivery_history từng lô | S2 × C4 → **8** | **8** | Giữ 8: bằng chứng theo 2 điều kiện giao + ghi delivery_history từng lô (nguồn của quy tắc đảo ngày) |
| {{#E5-3b}} UI POD: form theo điều kiện giao, chỉ mở khi shipment đã xuất xe | S1 × C2 → **2** | **2** | Giữ 2: form đổi trường theo điều kiện giao, logic kiểm ở E5-3a |
| {{#E6-2a}} Lái liên tục ≤ 4h: chỉ đoạn nghỉ (cộng dồn ≥ 30 phút) mới reset; xếp / giao hàng không tính nghỉ | S1 × C3 → **3** | **5** | Sửa: Ca biên: nghỉ cộng dồn từ nhiều đoạn ngắn, tuyến qua nửa đêm; spec LAB-4 từng sai đúng chỗ này (4h30 vs 6,5h) |
| {{#E6-2b}} 拘束時間 trong ngày: cảnh báo > 13h, chặn > 15h | S1 × C2 → **2** | **2** | Giữ 2: so sánh tổng 拘束 với 2 ngưỡng tham số |
| {{#E6-2c}} Nghỉ giữa ca ≥ 9h (so với tuyến hôm trước của tài xế) | S1 × C2 → **2** | **2** | Giữ 2: một phép trừ thời gian với tuyến hôm trước |
| {{#E6-2d}} Lái trong ngày ≤ 9h (bình quân 2 ngày) và 44h/tuần (bình quân 2 tuần) | S1 × C3 → **3** | **5** | Sửa: Bình quân 2 ngày / 2 tuần cần dữ liệu nhiều tuyến; ranh giới tuần chưa rõ; skill chỉ đếm 2 bảng |
| {{#E6-3}} UI timeline SC-32: highlight đúng khoảng vi phạm, Lưu & kiểm giờ lái (PUT /api/routes/[id]) | S3 × C3 → **8** | **8** | Giữ 8: timeline + highlight khoảng vi phạm + lưu/kiểm lại là khối UI nặng nhất E6 |
| {{#E6-5}} Làm rõ với khách: xác minh pháp lý 改善基準告示 và ngoại lệ (OPS-LAW-01) | S1 × C2 → **2** | **2** | Giữ 2: việc làm rõ của BrSE, không có code |
| {{#E7-2}} Gộp chuỗi vượt ngưỡng → cảnh báo (ngưỡng theo version tại read_at) + cách ly lô theo zone | S2 × C4 → **8** | **8** | Giữ 8: gộp chuỗi theo version tại read_at + cách ly lô theo zone, nhiều ca biên |
| {{#E7-4}} Deviation case SC-37: QA quyết định release / scrap, rationale, maker-checker | S3 × C3 → **8** | **8** | Giữ 8: maker-checker + 2 quyết định + cập nhật trạng thái lô |
| {{#E8-1}} Truy xuất xuôi / ngược theo mã bò, xuất xứ gạo, lô, NCC (SC-40) | S3 × C3 → **8** | **8** | Giữ 8: truy xuất xuôi / ngược qua 4 bảng, có điểm dừng khi thiếu liên kết |
| {{#E8-2}} Recall & đối soát 2 đẳng thức, chặn đóng khi lệch (SC-41) | S4 × C2 → **8** | **8** | Giữ 8: 5 endpoint + đối soát 2 đẳng thức, chặn đóng khi lệch |
| {{#E9-2}} Test E2E luồng lõi: nhập → phân bổ → xuất → POD (Playwright) | S2 × C2 → **3** | **3** | Giữ 3: kịch bản E2E dựa trên seed và ảnh chụp đã có ở LAB-4 |

## 2. Cách quy ra giờ
- **Cách chọn**: quy ước đổi SWP → giờ theo bảng cố định, **không** ước giờ trực tiếp từng issue.
- **Vì sao**: SWP đã được chấm từ yếu tố đo được và người review; ước giờ trực tiếp lần nữa tạo ra hai con số dễ mâu thuẫn. Bảng cố định cho phép kiểm lại và áp dụng như nhau cho 53 issue.
- **Quy tắc**: 1 → 2h · 2 → 4h · 3 → 7h · 5 → 12h · 8 → 20h · 13 → 32h (không tuyến tính: bậc cao thêm biên độ bất định). Giờ gồm code + unit test + tự review; không gồm QA hệ thống, BrSE, PM, buffer (G-01).
- **Áp dụng nhất quán**: script `swp_score.py` tính giờ từ SWP **đã chốt** (sau override), cùng một bảng cho mọi issue; Agent ghi đúng giá trị đó lên trường `Giờ ước lượng` của Project — không ai nhập tay.

## 3. Tổng theo epic
| Epic | Số issue | Tổng SWP | Tổng giờ | Ghi chú |
|---|---|---|---|---|
| E1 Nền tảng & phân quyền | 7 | 15 | 32 |  |
| E2 Master data | 3 | 13 | 31 | E2-2 người chốt giảm 8 → 5 |
| E3 Nhập hàng & tồn kho | 7 | 28 | 66 |  |
| E4 Đơn hàng & phân bổ (2 loại hạn, 1/3–1/2, đảo ngày) | 10 | 33 | 77 | P1-2 làm tăng E4-2d |
| E5 Xuất hàng & POD | 6 | 27 | 64 |  |
| E6 Lập tuyến & giờ lái xe tải 2024 | 9 | 42 | 100 | Epic nặng nhất — ràng buộc giờ lái 2024 |
| E7 Nhiệt độ & HACCP | 5 | 30 | 74 |  |
| E8 Truy xuất & recall | 2 | 16 | 40 |  |
| E9 Chất lượng, hạ tầng & tích hợp | 4 | 9 | 20 |  |
| **Tổng** | **53** | **213** | **504** | Skill chấm 210 → người chốt 213 |

## 4. So với estimate LAB-1
Cùng cơ sở so sánh: **giờ dev BE + FE chưa buffer** (LAB-1: cột BE + FE trong Effort Estimation, 7 giờ / MD).

| Phần (chức năng / epic) | LAB-1 | LAB-5 | Chênh | Vì sao |
|---|---|---|---|---|
| E1 ↔ FN-10 Bảo mật, phân quyền & audit | 58.5 MD | 4.6 MD (32 giờ) | -53.9 MD (= 8% LAB-1) | Prototype đã có middleware, requireRole, audit; LAB-5 chỉ hoàn thiện + 3 màn quản trị |
| E2 ↔ FN-01 Master & chính sách | 50.0 MD | 4.4 MD (31 giờ) | -45.6 MD (= 9% LAB-1) | Chỉ 2 màn master + màn version ngưỡng (P1-3); bỏ duyệt master nhiều cấp |
| E3 ↔ FN-02 Nhập hàng + FN-03 Tồn kho | 65.5 MD | 9.4 MD (66 giờ) | -56.1 MD (= 14% LAB-1) | SC-14 / SC-19 đã chạy ở prototype; LAB-5 thêm gap LAB-4 (P1 không đổi phạm vi) |
| E4 ↔ FN-04 Đơn hàng & phân bổ | 49.0 MD | 11.0 MD (77 giờ) | -38.0 MD (= 22% LAB-1) | Engine đã có 74 test; tách 5 bước để hoàn thiện; P1-2 thêm xử lý bản ghi đảo (+2 SWP) |
| E5 ↔ FN-05 Xuất hàng & POD | 59.0 MD | 9.1 MD (64 giờ) | -49.9 MD (= 15% LAB-1) | Bỏ offline 8h, ảnh/chữ ký thật; thêm shipment theo dải (ADR-009, P1-4) |
| E6 ↔ FN-06 Lập tuyến & giờ lái | 54.0 MD | 14.3 MD (100 giờ) | -39.7 MD (= 26% LAB-1) | Tỷ lệ giữ lại cao nhất (26%): ràng buộc 2024 không giảm được nhờ prototype; thêm 9h/ngày + 44h/tuần (P1-1); tích lũy tháng/năm còn phụ thuộc chấm công |
| E7 ↔ FN-07 Nhiệt độ & HACCP | 49.5 MD | 10.6 MD (74 giờ) | -38.9 MD (= 21% LAB-1) | Bỏ datalogger realtime; giữ import CSV + cảnh báo + deviation |
| E8 ↔ FN-08 Truy xuất & recall | 36.5 MD | 5.7 MD (40 giờ) | -30.8 MD (= 16% LAB-1) | Bỏ gửi thông báo recall |
| E9 ↔ FN-11 Tích hợp (một phần) | 14.5 MD | 2.9 MD (20 giờ) | -11.6 MD (= 20% LAB-1) | Chỉ migration, CI, E2E, làm rõ ERP; bỏ thông báo / tích hợp thật |
| FN-09 Báo cáo, KPI & audit export | 48.0 MD | 0 | −48.0 MD | Ngoài phạm vi từ PREMISE LAB-4 |
| FN-12 Migration | 32.0 MD | 0 | −32.0 MD | Ngoài phạm vi từ PREMISE LAB-4 |
| **Tổng dev (BE + FE)** | **516.5 MD** | **72.0 MD (504 giờ)** | **-444.5 MD** | G-01: hoàn thiện từ prototype, AI hỗ trợ, chỉ giờ dev; 18 / 49 màn |

Đọc bảng: chênh lớn **không** có nghĩa LAB-1 ước sai. LAB-1 ước xây mới toàn bộ 49 màn, có migration và báo cáo; LAB-5 ước phần còn lại để đưa 18 màn của prototype lên production (G-01). Epic giữ tỷ lệ cao nhất là **E6 giờ lái 2024** — xác nhận đây là phần không giảm được nhờ prototype.
