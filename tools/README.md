# tools — dựng GitHub Project

1. Chạy thử (không gọi GitHub): `python tools/setup_github_project.py --owner <user> --repo <repo> --student-id <mã> --dry-run`
2. Chạy thật (repo đã push, public): bỏ `--dry-run`. Tạo label, 68 issue (9 epic, 6 issue cha, 53 issue lá), quan hệ sub-issue, Project public + liên kết repo, field `Trạng thái`, `Iteration`, `Phụ trách (giả định)`, `SWP`, `Giờ ước lượng`, `SWP reviewed`; gán iteration / phụ trách / trạng thái Sprint 1; đóng issue Done; thay mã `{{#ID}}` trong markdown bằng số issue thật; bật GitHub Pages.
3. Agent ghi SWP: `bash skills/swp-estimator/scripts/push_to_project.sh swp-report/swp.tsv <user> <project-number>`
4. Commit lại các file markdown đã được thay mã issue.

Chạy lại an toàn: `tools/state.json` lưu issue / liên kết / item đã tạo. Không tạo được field Iteration bằng API → script dừng và hướng dẫn tạo tay rồi chạy lại.
