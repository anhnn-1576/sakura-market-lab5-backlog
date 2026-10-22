# Sakura Market LAB-5 Backlog

| Mục | Nội dung |
|---|---|
| Tên dự án | 桜水産市場 業務支援システム — backlog, estimate và báo cáo tiến độ |
| Mã học viên | AnhNN(B) |
| Đề | **Product A** — sàn đấu giá thủy sản |

## 1. Tổng quan

- **Backlog break từ bản LAB-4 nào:** bản LAB-4 core, nộp ngày **22/10/2026**. Bản này gồm T2 ERD và bảng chênh lệch v0.2, T3 kiến trúc v0.2, ADR-001 → 005, và 13 screen spec + wireframe sau review R09.
- **Phạm vi:** chỉ 13 màn đã có detail design. Nền của backlog là nâng prototype LAB-2 lên to-be: mỗi issue là một mục "việc cho LAB-5" ở §9 của spec, cộng test cho phần giữ nguyên.
- **PREMISE.md có thay đổi:** có. Gồm 5 chỗ sửa spec (S01–S05), 11 giả định (A01–A11) và 6 hướng đã chốt (H01–H06). Xem [PREMISE.md](PREMISE.md).
- **Số epic:** 10 epic, 41 issue, 42 sub-issue. Trong đó có 67 task lá được chấm **250 SWP · 434 giờ**.
- **Sprint giả lập đã chạy:** **Sprint 1** (26/10 → 06/11/2026). Sprint 2 và 3 đã lên kế hoạch, chưa chạy. Xem [progress-report.md](progress-report.md).
- **Ràng buộc đặc thù của đề:** 完納奨励金 là epic riêng [#71](https://github.com/anhnn-1576/sakura-market-lab5-backlog/issues/71). Mỗi biến của BR-INC-01 là một sub-issue riêng (#73–#78), kèm ghi kết quả nguyên tử (#79), UI (#80) và nghiệm thu test vector (#81).

## 2. Link

| Gì | Link |
|---|---|
| Repo | https://github.com/anhnn-1576/sakura-market-lab5-backlog |
| GitHub Project | https://github.com/users/anhnn-1576/projects/1 |
| Báo cáo HTML của skill chấm SWP (trong repo) | [`reports/sun-estimate-anhnn-1576-project-1-20261022-1015.html`](reports/sun-estimate-anhnn-1576-project-1-20261022-1015.html) |

GitHub hiện file HTML ở dạng mã nguồn. Muốn xem báo cáo thì bấm **Download raw file** rồi mở bằng trình duyệt. Báo cáo chạy offline, không gọi mạng ra ngoài.

**Đã mở thử khi chưa đăng nhập** (ngày 22/10/2026): cả 3 link đều mở được bằng trình duyệt không đăng nhập GitHub và bằng request không kèm token, không bị chuyển sang trang đăng nhập. Repo và Project đều để public.

## 3. Cấu trúc repo

| File / thư mục | Nội dung |
|---|---|
| `README.md` | File này: thông tin bài nộp, link, cấu trúc, bảng spec → epic |
| `PREMISE.md` | Tiền đề: spec thêm / bỏ / sửa so với LAB-4, giả định bổ sung, hướng đã chốt |
| `task-breakdown.md` | Nguyên tắc chia task, bảng spec → issue, hạng mục chịu ràng buộc 完納奨励金, chỗ hở / mâu thuẫn của spec |
| `estimate.md` | Issue mẫu skill chọn để kiểm, cách quy SWP ra giờ, tổng theo epic, so với LAB-1 |
| `progress-report.md` | Báo cáo Sprint 1: trạng thái, burndown, rủi ro trễ |
| `AI-report.md` | Đã dùng AI thế nào, review ra sao, lỗi đã bắt được trong output của AI |
| `reports/` | Báo cáo HTML của skill chấm SWP (`sun-estimate-…html`) và ảnh burndown Sprint 1 (`burndown-sprint-1.svg`) |
| `backlog/` | Dữ liệu gốc: `backlog-items.json` (93 epic / issue / sub-issue), `issue-number-map.json` (mã ↔ số issue ↔ item trên Project), `sprint-plan.json` (Iteration, người phụ trách, trạng thái, ngày Done giả lập) |
| `scripts/` | Script đẩy và cập nhật dữ liệu lên GitHub: `push-backlog-to-github-project.py` (tạo issue, sub-issue, thêm vào Project), `write-swp-and-hours-to-github-project.py` (ghi SWP và giờ từ báo cáo đã validate), `apply-sprint-plan-to-github-project.py` (ghi Iteration, người phụ trách, trạng thái), `render-sprint-burndown.py` (vẽ burndown) |

Không có thư mục `skills/`: bài này dùng skill có sẵn (`tkm:sun-estimate`, `tkm:confidence`), không tự viết hay sửa skill nào.

## 4. Spec → epic

| Spec (mã / file LAB-4, hoặc dòng PREMISE) | Epic trên Project | Ghi chú |
|---|---|---|
| T2 G08, G09, G13, G18; T3 §5, I2, I5, I6 (`lab4-t2-…`, `lab4-t3-…`) | [#1](https://github.com/anhnn-1576/sakura-market-lab5-backlog/issues/1) — Nền tảng dùng chung: tệp chứng cứ, email, offline, job định kỳ | Khối dùng chung cho 5 epic khác. Chốt Vercel Cron (PREMISE H01) và Amazon SES (H02) |
| SCR-F02-02, SCR-F02-03; ADR-001 | [#13](https://github.com/anhnn-1576/sakura-market-lab5-backlog/issues/13) — Tư cách tham gia theo căn cứ | Không gộp 許可 và 承認 (RFP 02-08). Nhánh 買出人 bị khoá (PREMISE A07) |
| SCR-F03-01, SCR-F03-02 | [#27](https://github.com/anhnn-1576/sakura-market-lab5-backlog/issues/27) — Tiếp nhận và đánh giá lô | Tiếp nhận lô được khi mất mạng (PREMISE A06) |
| SCR-F04-01, SCR-F05-01 | [#36](https://github.com/anhnn-1576/sakura-market-lab5-backlog/issues/36) — Chốt giao dịch 相対 / せり theo căn cứ tư cách | Sửa thiết kế S02 (bỏ tham chiếu D10 còn sót ở F05-01) |
| SCR-F06-01, SCR-F06-03; ADR-003 | [#46](https://github.com/anhnn-1576/sakura-market-lab5-backlog/issues/46) — Sửa sau chốt có duyệt | Logic delta giữ như prototype, thêm test hồi quy |
| SCR-F07-02 | [#54](https://github.com/anhnn-1576/sakura-market-lab5-backlog/issues/54) — Giao hàng và ngoại lệ, có offline | PREMISE S03 (gộp F07-02 D8 với F08-02 D6), A05 (chặn ghi trên ngày đã khoá) |
| SCR-F08-01, SCR-F08-02 | [#60](https://github.com/anhnn-1576/sakura-market-lab5-backlog/issues/60) — Đối soát ngày và khoá ngày nghiệp vụ | PREMISE S01 (bỏ kiểm tranh chấp khỏi đợt này), S04 (thu hẹp báo cáo ngày) |
| SCR-F09-02; RFP BR-INC-01, FR-INC-01/03; PREMISE S05 | [#71](https://github.com/anhnn-1576/sakura-market-lab5-backlog/issues/71) — 完納奨励金: tính thưởng thanh toán đúng hạn | **Ràng buộc đặc thù Product A.** Mỗi biến một sub-issue: đối tượng, đúng hạn, phiên bản, bậc tỉ lệ, hệ số thuế và cắt lẻ, 差分 kỳ sau. Giả định A10 (số âm), A11 (giao chia lần) |
| SCR-F10-03; ADR-004 | [#82](https://github.com/anhnn-1576/sakura-market-lab5-backlog/issues/82) — Phiên bản quy tắc: duyệt và rollback | Giả định A09 (cách đếm giới hạn 4 lần / năm) |
| Mục 11 "Câu hỏi mở" của 13 spec; T2 §4 | [#85](https://github.com/anhnn-1576/sakura-market-lab5-backlog/issues/85) — Làm rõ yêu cầu với khách | 68 câu hỏi gom thành 8 issue C01–C08, mỗi issue trỏ tới giả định đang dùng thay |
