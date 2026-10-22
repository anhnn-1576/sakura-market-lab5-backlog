# Estimate — SWP và giờ cho backlog LAB-5

**Báo cáo HTML của skill chấm SWP:** [`reports/sun-estimate-anhnn-1576-project-1-20261022-1015.html`](reports/sun-estimate-anhnn-1576-project-1-20261022-1015.html)

Skill `tkm:sun-estimate` đọc 93 issue trên [GitHub Project](https://github.com/users/anhnn-1576/projects/1) và chấm 67 task lá (Scope × Complexity → SWP). 26 container (epic, issue cha) lấy tổng điểm của con. Tổng: **250 SWP · 434 giờ**. Hai trường `SWP` và `Estimate (h)` trên Project được ghi bằng [`scripts/write-swp-and-hours-to-github-project.py`](scripts/write-swp-and-hours-to-github-project.py). Script đọc thẳng payload đã validate trong báo cáo HTML, nên số trên board và số trong báo cáo cùng một nguồn. Đã đọc lại board: 67/67 khớp.

## 1. Issue mẫu skill chọn để kiểm

Skill tự chọn 5 issue mẫu theo quy tắc cố định: nhỏ nhất, trung vị, lớn nhất, lệch xa trung vị, độ tin cậy thấp nhất. Mỗi issue mẫu được hỏi 2 vòng: mức độ khó, rồi điểm cụ thể.

| Issue | Skill chấm (Scope × Complexity → SWP) | Bạn chốt | Lý do |
|---|---|---|---|
| [#49](https://github.com/anhnn-1576/sakura-market-lab5-backlog/issues/49) Gắn tệp chứng cứ thay ô text (SCR-F06-01) — nhỏ nhất | 1 × 0 → 1 | Giữ 1 (rất dễ) | Component tải tệp làm ở #5, issue này chỉ đặt nó vào form có sẵn. Không có trạng thái mới |
| [#93](https://github.com/anhnn-1576/sakura-market-lab5-backlog/issues/93) Làm rõ: câu hỏi còn lại (C08) — trung vị | 3 × 0 → 3 | Giữ 3 (dễ) | 26 câu nhưng đều đã viết sẵn ở mục 11 của spec. Không chặn issue nào, nên không cần nhiều vòng trao đổi |
| [#56](https://github.com/anhnn-1576/sakura-market-lab5-backlog/issues/56) Offline ghi giao hàng, xung đột → ngoại lệ 未処理 — lớn nhất | 5 × 3 → 10 | Giữ 10 (vừa) | Luồng trọn vẹn qua DB, UI, thông báo, với 3 ca xung đột. Hàng đợi dùng chung đã tách ra #10, nên chưa tới mức khó |
| [#3](https://github.com/anhnn-1576/sakura-market-lab5-backlog/issues/3) Bảng attachments, migration bỏ evidence_note — lệch xa trung vị | 3 × 3 → 6 | Giữ 6 (vừa) | Migration chạm 4 bảng, phải chuyển dữ liệu cũ và lùi được. Dữ liệu là seed của prototype nên không cần lên mức khó |
| [#58](https://github.com/anhnn-1576/sakura-market-lab5-backlog/issues/58) Chặn ghi giao hàng trên ngày đã khoá — độ tin cậy thấp nhất | 2 × 1 → 3 | Giữ 3 (dễ) | Theo giả định [PREMISE A05](PREMISE.md#2-giả-định-bổ-sung): chỉ thêm hàm kiểm có sẵn vào 3 hàm SQL. Rủi ro khách chọn phương án khác đã ghi ở A05 (+16 giờ), không cộng vào điểm |

**Không sửa issue nào, vì sao giữ nguyên:** cả 5 điểm khớp với cách chia task ở [task-breakdown.md](task-breakdown.md) mục 1. Phần khó của mỗi luồng đã tách thành issue riêng, nên từng task lá nhỏ. Điểm cao nhất (10 SWP) quy ra 16 giờ, đúng bằng trần "≤ 2 ngày" của quy tắc chia. Vì không có hiệu chỉnh nào nên không có quy tắc lan sang các issue khác. Báo cáo ghi trạng thái `accepted` và 0 dòng bị đổi.

## 2. Cách quy ra giờ

**Cách đã chọn:** quy ước đổi SWP ra giờ, không ước giờ trực tiếp cho từng issue.

**Vì sao:**
- Một quy tắc áp cho cả 67 task thì nhất quán. Người review chỉ cần kiểm quy tắc và điểm, không phải kiểm 67 con số giờ riêng lẻ.
- Khi khách trả lời làm rõ và điểm thay đổi, giờ tự tính lại theo điểm.
- Chưa có dữ liệu giờ thực tế theo SWP của đội (KPI Insight không có lịch sử cho repo này). Vì vậy tỉ lệ được neo vào các issue mẫu đã duyệt, không lấy theo cảm giác.

**Quy tắc cụ thể:**

```
giờ = SWP × 1,5 + 1      (task code: nhãn layer:*)
giờ = SWP × 1,5          (issue làm rõ: nhãn clarify)
```

- **1,5 giờ / SWP** được neo vào 2 issue mẫu ở hai đầu thang điểm. #49 (1 SWP) ra 2,5 giờ: đủ cho việc đặt component vào form và chạy lại test của màn. #56 (10 SWP) ra 16 giờ, đúng bằng trần task lá. Tỉ lệ cao hơn sẽ đẩy #56 vượt trần, mà #56 đã được duyệt là không cần tách.
- **+1 giờ quality gate** cho mỗi task code: tạo PR, chờ AI review (`reviewer`), người review, sửa theo góp ý (định nghĩa xong ở task-breakdown.md mục 1). Phần này không nằm trong SWP, vì SWP đo độ rộng và độ khó của bản thân việc làm.
- **Issue làm rõ không cộng +1 giờ** vì không có PR. Thời gian khách trả lời là thời gian chờ, không tính vào effort.
- **Áp dụng nhất quán:** script ghi giờ dùng đúng công thức này (`hours_for()`), không có ngoại lệ tay. Mọi số giờ đều là bội của 0,5. Khi điểm đổi thì chạy lại script, không sửa giờ trực tiếp trên board.
- **Không bao gồm:** quản lý dự án, BrSE cố định hằng tháng, kiểm thử hệ thống / UAT và buffer. Các phần này tính ở mức dự án như LAB-1 (`06_Other Tasks`), không chia vào task lá.

## 3. Tổng theo epic

| Epic | Số issue (task lá) | Tổng SWP | Tổng giờ | Ghi chú |
|---|---:|---:|---:|---|
| [#1](https://github.com/anhnn-1576/sakura-market-lab5-backlog/issues/1) Nền tảng dùng chung | 8 | 37 | 63,5 | Tệp chứng cứ, email, offline, job. Làm trước vì 5 epic khác dùng lại |
| [#13](https://github.com/anhnn-1576/sakura-market-lab5-backlog/issues/13) Tư cách tham gia theo căn cứ | 10 | 40 | 70,0 | Epic lớn nhất: đổi mô hình dữ liệu theo ADR-001 và máy trạng thái có duyệt |
| [#27](https://github.com/anhnn-1576/sakura-market-lab5-backlog/issues/27) Tiếp nhận và đánh giá lô | 6 | 24 | 42,0 | |
| [#36](https://github.com/anhnn-1576/sakura-market-lab5-backlog/issues/36) Chốt giao dịch 相対 / せり | 6 | 22 | 39,0 | Phụ thuộc #16 (kiểm tư cách theo căn cứ) |
| [#46](https://github.com/anhnn-1576/sakura-market-lab5-backlog/issues/46) Sửa sau chốt có duyệt | 5 | 18 | 32,0 | Logic duyệt và delta giữ như prototype |
| [#54](https://github.com/anhnn-1576/sakura-market-lab5-backlog/issues/54) Giao hàng và ngoại lệ | 5 | 26 | 44,0 | Gồm #56, task lớn nhất (10 SWP) |
| [#60](https://github.com/anhnn-1576/sakura-market-lab5-backlog/issues/60) Đối soát và khoá ngày | 8 | 25 | 45,5 | |
| [#71](https://github.com/anhnn-1576/sakura-market-lab5-backlog/issues/71) **完納奨励金** | 9 | 25 | 46,5 | Ràng buộc đặc thù. Mỗi bước tính chỉ 1–2 SWP (#74, #76, #77 mỗi bước 1 SWP), vì từng biến đã tách riêng. Phần nặng nằm ở ghi nguyên tử (#79, 6 SWP) và nghiệm thu test vector (#81, 5 SWP) |
| [#82](https://github.com/anhnn-1576/sakura-market-lab5-backlog/issues/82) Phiên bản quy tắc | 2 | 9 | 15,5 | |
| [#85](https://github.com/anhnn-1576/sakura-market-lab5-backlog/issues/85) Làm rõ với khách | 8 | 24 | 36,0 | Việc của BrSE, không cộng quality gate |
| **Tổng** | **67** | **250** | **434,0** | ≈ 54,3 ngày công (8 giờ/ngày) |

## 4. So với estimate LAB-1

LAB-1 lấy theo file `[PRODUCT-A] … Effort Estimation 20261001.xlsx` của bài nộp LAB-1 (không đưa vào repo này), sheet `01_Server`. Mỗi dòng LAB-1 tính cả Backend, Frontend (Implement + FixBug + Unit Test) và Design UX/UI. Đổi ra giờ theo 1 MD = 8 giờ. Chỉ lấy các dòng ứng với phần việc của 13 màn này. Các dòng LAB-1 khác (danh sách, báo cáo RPT, tranh chấp…) không thuộc đợt này nên không đưa vào so sánh.

| Phần (chức năng / epic) | LAB-1 | LAB-5 | Chênh | Vì sao |
|---|---:|---:|---:|---|
| #1 Nền tảng (F03-02, F07-06 đính kèm; F11-02 email; F16-01→03 offline) | 34,0 MD · 272 h | 63,5 h | −208,5 h (23 %) | Nền backlog là nâng prototype ([PREMISE H05](PREMISE.md#3-hướng-đã-chốt)). Prototype đã có xác thực, audit, thông báo trong app, nên chỉ còn phần to-be. Job định kỳ (#12) là việc mới, LAB-1 không có dòng riêng |
| #13 Tư cách (F02-05, SCR-F02-02, SCR-F02-03) | 29,75 MD · 238 h | 70,0 h | −168 h (29 %) | H05. Tỉ lệ còn lại cao nhất: ADR-001 đổi mô hình dữ liệu và thêm luồng duyệt ([PREMISE H06](PREMISE.md#3-hướng-đã-chốt)). LAB-1 chưa có các phần này |
| #27 Lô (SCR-F03-01, SCR-F03-02) | 24,75 MD · 198 h | 42,0 h | −156 h (21 %) | H05. Phần còn lại tập trung vào offline (#30) và tablet |
| #36 Chốt giao dịch (F04-02, SCR-F04-01, SCR-F05-01) | 31,75 MD · 254 h | 39,0 h | −215 h (15 %) | H05. `create_trade` nguyên tử, có khoá dòng, đã chạy thật ở prototype (ADR-002 "đã áp dụng") |
| #46 Sửa sau chốt (F06-03, F06-04, SCR-F06-01, SCR-F06-03) | 28,5 MD · 228 h | 32,0 h | −196 h (14 %) | H05. Delta và chênh lệch kỳ sau đã có (ADR-003 "đã áp dụng"). Chỉ còn tệp, email và test hồi quy (#53) |
| #54 Giao hàng (F07-03, F07-04, SCR-F07-02, SCR-F07-03) | 35,75 MD · 286 h | 44,0 h | −242 h (15 %) | H05. LAB-1 tách màn ngoại lệ riêng, LAB-4 gộp vào SCR-F07-02. G21 gộp còn một issue ([PREMISE S03](PREMISE.md#1-spec-thêm--bỏ--sửa-so-với-lab-4)) |
| #60 Đối soát, khoá ngày (F08-01, SCR-F08-01, SCR-F08-02, F12-14) | 36,75 MD · 294 h | 45,5 h | −248,5 h (15 %) | H05. Bỏ kiểm tranh chấp ([PREMISE S01](PREMISE.md#1-spec-thêm--bỏ--sửa-so-với-lab-4)). Báo cáo ngày thu hẹp còn báo cáo đối soát ([PREMISE S04](PREMISE.md#1-spec-thêm--bỏ--sửa-so-với-lab-4)) |
| #71 完納奨励金 (F09-02, F09-03, SCR-F09-02) | 27,25 MD · 218 h | 46,5 h | −171,5 h (21 %) | H05: công thức đã có ở prototype. Tỉ lệ còn lại cao hơn các epic chốt giao dịch / sửa vì phải viết lại phần tổng hợp trong SQL (G23, prototype đang tính thiếu ngầm), đổi phiên bản sang FK, và thêm bộ test vector nghiệm thu. Còn phụ thuộc [PREMISE A11](PREMISE.md#2-giả-định-bổ-sung): nếu tính theo số đã giao thì +8 giờ |
| #82 Phiên bản quy tắc (F10-05, SCR-F10-03) | 13,25 MD · 106 h | 15,5 h | −90,5 h (15 %) | H05. Chỉ thêm rollback và đếm giới hạn có khoá |
| #85 Làm rõ với khách | — | 36,0 h | +36 h | LAB-1 tính BrSE cố định 0,5 MM/tháng ở `06_Other Tasks`, không chia theo chức năng. LAB-5 tách thành 8 issue để theo dõi trên board |
| **Tổng phần so được (trừ #85)** | **261,75 MD · 2.094 h** | **398,0 h** | **−1.696 h (19 %)** | |

**Đọc bảng này thế nào:**
- Lý do chính của mức chênh là H05. LAB-1 ước làm mới từ đầu. LAB-5 chỉ ước phần nâng prototype LAB-2 lên to-be, vì LAB-4 ghi rõ phần còn lại là mục §9 "việc cho LAB-5".
- LAB-5 không có cột Design: wireframe và spec đã xong ở LAB-4.
- FixBug và Unit Test nằm trong "Xong khi" của từng task, cùng các sub-issue test riêng.
- Số giờ LAB-5 giả định đội làm theo AIDD (AI sinh code và test, người review qua quality gate). Đó là lý do tỉ lệ 1,5 giờ/SWP thấp. LAB-1 bản AIDD (`Effort Estimation AIDD 20261014.xlsx`) cũng giảm theo hệ số, nhưng vẫn trên nền làm mới.
- Tổng 434 giờ là effort task lá của đợt này, chưa gồm PM, kiểm thử hệ thống / UAT và buffer. Không dùng con số này làm giá trị hợp đồng.
