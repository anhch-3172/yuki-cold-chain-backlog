# Rubric SWP — Scope × Complexity

## 1. Scope (độ rộng thay đổi)
Điểm scope = `screens + apis + tables` (số màn hình / khối UI, số endpoint, số bảng DB phải tạo hoặc sửa).
| Bậc | Điểm scope | Ví dụ |
|---|---|---|
| S1 | 0–2 | Sửa 1 API hoặc 1 khối UI |
| S2 | 3–4 | 1 màn + 1–2 API + 1 bảng |
| S3 | 5–7 | 1 màn đầy đủ + vài API + nhiều bảng |
| S4 | ≥ 8 | Nhiều màn / luồng xuyên module → nên tách |

## 2. Complexity (độ khó)
Điểm complexity = bậc nhánh nghiệp vụ + cờ:
- Nhánh nghiệp vụ (`branches` = số quy tắc / điều kiện rẽ nhánh phải cài và test): 0 → 0 · 1–2 → 1 · 3–4 → 2 · ≥ 5 → 3
- `special` (ràng buộc đặc thù của đề: giờ lái 2024, 賞味/消費期限, đảo ngày theo lịch sử khách, quy tắc 1/3–1/2, truy xuất gạo/bò, ngưỡng nhiệt theo chính sách) → +1
- `integrity` (đồng thời, khóa dòng, append-only, máy trạng thái, maker-checker) → +1
- `integration` (hệ thống ngoài / dữ liệu ngoài chưa rõ đặc tả) → +1

| Bậc | Điểm complexity |
|---|---|
| C1 | 0–1 |
| C2 | 2 |
| C3 | 3 |
| C4 | ≥ 4 |

## 3. Ma trận SWP
| | C1 | C2 | C3 | C4 |
|---|---|---|---|---|
| **S1** | 1 | 2 | 3 | 5 |
| **S2** | 2 | 3 | 5 | 8 |
| **S3** | 3 | 5 | 8 | 13 |
| **S4** | 5 | 8 | 13 | 21 |

SWP ≥ 13 ở issue lá → bắt buộc tách sub-issue.

## 4. Chọn issue mẫu cho người kiểm
1. Issue SWP cao nhất của mỗi epic (rủi ro estimate thấp hơn thực tế lớn nhất).
2. Issue `special = true` có SWP ≤ 3 (nghi đánh giá thấp ràng buộc đặc thù).
3. Issue **SWP ≥ 8** có điểm scope (2, 4, 7) hoặc complexity (1, 3) nằm đúng ranh giới bậc — đổi 1 yếu tố là đổi bậc, sai số giờ lớn. (Bản đầu xét mọi SWP ≥ 5 → chọn 30/53 issue, quá nhiều để gọi là mẫu; đã thu hẹp.)
4. Mọi issue bị cờ “phải tách”.

## 5. Quy đổi SWP → giờ (quy ước dự án, dùng thống nhất)
| SWP | 1 | 2 | 3 | 5 | 8 | 13 |
|---|---|---|---|---|---|---|
| Giờ (dev + unit test + tự review) | 2 | 4 | 7 | 12 | 20 | 32 |
Bậc cao quy đổi không tuyến tính vì độ bất định tăng. Giờ QA hệ thống, PM, BrSE tính riêng ở estimate tổng.
