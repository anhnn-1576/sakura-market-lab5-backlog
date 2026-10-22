# PREMISE — Tiền đề của backlog LAB-5

Backlog break từ bản LAB-4 core (`lab4-deliverables-core`: T2 v0.2, T3 v0.2, ADR-001 → 005, 13 screen spec sau review R09).
Phạm vi: **chỉ 13 màn đã có detail design**. Nền của backlog: **nâng prototype LAB-2 lên to-be**. Mỗi issue là một mục "Khác với prototype (việc cho LAB-5)" ở §9 của spec, cộng với test cho phần giữ nguyên (xem H05).

Số issue (#…) là issue trong repo này, đều nằm trên [GitHub Project](https://github.com/users/anhnn-1576/projects/1). Tiêu đề issue bắt đầu bằng mã trong [`backlog/backlog-items.json`](backlog/backlog-items.json), ví dụ `[08.1.6]`; bảng đối chiếu mã ↔ số ở [`backlog/issue-number-map.json`](backlog/issue-number-map.json).

## 1. Spec thêm / bỏ / sửa so với LAB-4

| # | Spec | Thêm / Bỏ / Sửa | Trước → sau | Vì sao | Issue bị ảnh hưởng |
|---|---|---|---|---|---|
| S01 | SCR-F08-02 §9 D1, mục 3 No 11, §7 | Bỏ (khỏi đợt này) | Trước: kiểm tra trước khi khoá gồm giao hàng chưa xong, yêu cầu sửa đang mở **và tranh chấp chưa giải quyết** → Sau: chỉ giao hàng và yêu cầu sửa. Phần tranh chấp làm cùng SCR-F08-03/04 | Phát hiện khi break: phần kiểm tranh chấp cần bảng `disputes` (G07), mà bảng này thuộc SCR-F08-03/04 chưa có detail design. Tạo issue lúc này thì phải tự thiết kế bảng tranh chấp ngoài spec | #67 |
| S02 | SCR-F05-01 §9 D7 | Sửa | Trước: "…, 401 kèm `next`) như F04-01 D7, D9, D10" → Sau: "… như F04-01 D7, D9" | Mâu thuẫn còn sót: review R09 đã bỏ D10 (`?next=`) ở F04-01, nhưng dòng D7 của F05-01 vẫn trỏ tới D10 | #45 |
| S03 | SCR-F07-02 §9 D8 và SCR-F08-02 §9 D6 | Sửa | Trước: hai dòng D ở hai spec → Sau: một hạng mục (cùng G21) | Phát hiện khi break: hai dòng mô tả cùng một thay đổi (thêm `assert_day_open` vào 3 hàm giao hàng). Để hai issue thì sẽ làm trùng và đếm trùng effort | #58 |
| S04 | SCR-F08-01 §9 D4 | Sửa (thu hẹp) | Trước: "Báo cáo ngày chạy bằng job sau khoá sổ" (không rõ gồm báo cáo nào; T3 §2 ghi "12 báo cáo") → Sau: job tạo **báo cáo đối soát của ngày vừa khoá**, kèm email cảnh báo nếu tới 10:30 JST chưa xong | Chỗ hở phát hiện khi break: 12 báo cáo RPT không thuộc 13 màn và chưa có spec cột / định dạng. Không ước lượng được nếu để nguyên | #65 |
| S05 | SCR-F09-02 §7 "Cách tính" bước 1 | Thêm | Trước: "giao dịch 確定 trong kỳ, đọc giá trị hiệu lực" → Sau: thêm câu "giao hàng chia lần, 不足 hoặc 部分キャンセル **không** làm đổi số tiền đủ điều kiện, cho tới khi có yêu cầu sửa được duyệt" (A11) | Ràng buộc RFP bị bỏ sót: RFP yêu cầu đề xuất phải nêu rõ thời điểm giao hàng chia lần được phản ánh vào 精算 và 完納奨励金, và coi đây là điều kiện để chốt estimate. Spec LAB-4 chưa nói điều này | #73, #90 |

## 2. Giả định bổ sung

Giả định chỉ lấp chỗ spec / RFP để ngỏ. Mỗi giả định có một issue làm rõ (C0x). Khi khách trả lời thì sửa dòng này và các issue bị ảnh hưởng.

| # | Giả định | Chỗ spec / RFP để ngỏ | Ảnh hưởng tới issue / estimate |
|---|---|---|---|
| A01 | Việc "chỉ 責任者 được làm" (duyệt tư cách, xác nhận khoá khi còn việc tồn, chạy tính thưởng) = tài khoản có `is_manager` trong vai trò tương ứng. Đợt này chưa làm MFA | Q-F0203-02, Q-F0802-01, Q-F0902-05; MFA: Q09 / Q-F0603-04 (#87) | #23, #70, #79. Nếu khách cần MFA thì thêm issue mới, khoảng +16 giờ |
| A02 | Tệp chứng cứ: JPEG / PNG / PDF, tối đa 10 MB mỗi tệp, 5 tệp mỗi bản ghi. Chỉ bắt buộc ở chỗ spec ghi "bắt buộc". Tệp mồ côi bị xoá sau 24 giờ. Đợt này chưa quét virus | Q-F0202-04, Q-F0601-01, Q-F0702-02; T3 I5 "chưa có số" (#86) | #3–#5. Nếu thêm quét virus thì #4 tăng khoảng +12 giờ |
| A03 | Ngưỡng "sắp hết hạn" của tư cách là 30 ngày | Q-F0401-03 (#93) | #26, #41. Đổi số không đổi effort |
| A04 | Kỳ thưởng là tháng của ngày giao dịch, `payments.period` theo cùng tháng đó | Q-F0902-04 (#90) | #73, #74. Nếu kỳ không theo tháng thì phải thêm bảng lịch kỳ, khoảng +8 giờ |
| A05 | Không cho ghi giao hàng / ngoại lệ trên ngày đã khoá: 3 hàm giao hàng gọi `assert_day_open`. Giao hàng phát sinh sau khi khoá đi qua yêu cầu sửa | Q-F0702-04 (= G21), Q-F0802-02 (#89). BR-CLOSE-01 cấm sửa trực tiếp ngày đã khoá, nhưng chưa nói riêng về giao hàng | #58, #69. Nếu khách chọn "cho phép và ghi chênh lệch theo ngày giao" thì #58 phải viết lại, khoảng +16 giờ |
| A06 | Offline chỉ áp cho tiếp nhận lô và ghi giao hàng. 完了 và ngoại lệ không làm được khi offline. Lô tạo offline thuộc ngày nghiệp vụ lúc đồng bộ. Hàng đợi gắn với người đã lưu thao tác, và không cho đăng xuất khi còn mục `未送信` | Q-F0301-03, Q-F0301-04, Q-F0302-02, Q-F0702-01 (#88) | #10, #30, #56. Nếu thêm đánh giá lô hoặc ngoại lệ offline thì mỗi thao tác khoảng +8 giờ |
| A07 | 買出人 chưa được là bên mua và chưa có luật mở lại. Nhánh 買出人 bị khoá (seed `取引地点登録` nhưng không chọn được làm người mua) | Q-T2-02, Q-T2-06 (#91). RFP 02-02 và FR-AITAI-01 nói khác nhau | #15, #22, #38. Nếu 買出人 được mua thì cần thêm issue kiểm hạn `取引地点登録` lúc chốt, khoảng +12 giờ |
| A08 | Audit lần thử ghi vào ngày đã khoá áp cho mọi route ghi theo ngày, kể cả giao hàng (theo A05) | Q-F0802-02 (#89) | #69 |
| A09 | Giới hạn 4 lần / năm đếm theo năm dương lịch của ngày hiệu lực (giống prototype). Bản rollback cũng được đếm, vì nó là một bản mới phải qua duyệt | Q-T2-03, Q-F1003-02, Q-F1003-03 (#92) | #83. Đổi cách đếm không đổi effort |
| A10 | Dòng `差分` âm được cắt về phía 0 (−203,69 → −203), giống prototype | Q-F0902-01 (#90). BR-INC-01 chỉ ghi "切り捨て", không nói về số âm | #78. Nếu đổi sang `floor` thì chỉ sửa 1 dòng code và test vector |
| A11 | Số tiền đủ điều kiện để tính 完納奨励金 = giá trị hiệu lực của giao dịch (`trade_effective`). Giao chia lần, 不足, 部分キャンセル không làm đổi số tiền này cho tới khi có yêu cầu sửa được duyệt | Q-F0702-07; mục 分割引渡し của RFP (#89, #90) | #73 (S05). Nếu tính theo số đã giao thì #73 phải join thêm bảng giao hàng, khoảng +8 giờ, và cần thêm test vector |

## 3. Hướng đã chốt

| # | Vấn đề | Các phương án ở LAB-4 | Phương án chốt | Vì sao |
|---|---|---|---|---|
| H01 | Cơ chế job định kỳ (T3 I6) | Vercel Cron gọi API nội bộ có khoá bí mật · `pg_cron` gọi hàm SQL | **Vercel Cron** gọi API nội bộ | Worker gửi email cần code ứng dụng, `pg_cron` không làm được. Dùng một cơ chế cho mọi job thì log nằm một chỗ. Hàm SQL vẫn được gọi qua API |
| H02 | Nhà cung cấp email (T3 I2) | Amazon SES · SendGrid | **Amazon SES**, vùng Tokyo | Dữ liệu người tham gia gửi qua email nằm trong Nhật (APPI). Lượng email ít (thông báo nội bộ, khoảng 180 tài khoản), giá theo lượng của SES thấp |
| H03 | Giao hàng trên ngày đã khoá (G21, F07-02 D8, F08-02 D6) | Chặn (`assert_day_open` ở 3 hàm) · Cho phép và ghi chênh lệch theo ngày giao | **Tạm chốt chặn** (A05), đổi nếu #89 có câu trả lời khác | Khớp BR-CLOSE-01. Ít việc hơn phương án kia, và không cần cơ chế chênh lệch mới. Rủi ro trễ được ghi ở `progress-report.md` |
| H04 | Tổng hợp dữ liệu lớn (G23, ADR-003) | View `GROUP BY` / hàm SQL đọc mỗi lần · Materialized view | **Hàm SQL tổng hợp** khi đọc. Materialized view chỉ dùng nếu bài đo tải ở #63 / #73 không đạt | Đối soát trong ngày cần số liệu tức thời, materialized view phải làm mới nên dễ cũ. YAGNI: chưa có số đo nào cho thấy cần |
| H05 | Nền của backlog | LAB-4 chỉ ghi các mục §9 là "việc cho LAB-5", chưa nói làm tiếp prototype hay viết lại | **Nâng prototype lên to-be**: issue = mục D# ở §9, cộng test cho phần giữ nguyên | Prototype đã có phân quyền 3 tầng, hàm SQL nguyên tử, delta (ADR-002, ADR-003 "đã áp dụng"). Viết lại thì bỏ phí phần đã làm. Hệ quả: tổng effort nhỏ hơn LAB-1 nhiều (xem `estimate.md`) |
| H06 | ADR-001 và ADR-004 đang ở trạng thái "Đề xuất" | Chờ Q-T2-01/02/03/04 rồi mới quyết · Áp dụng ngay, câu hỏi còn lại xử lý sau | **Áp dụng ngay** | #15, #16, #38, #39, #75, #83 đều dựa trên hai ADR này. Các câu hỏi còn mở chỉ ảnh hưởng một nhánh nhỏ (買出人, cách đếm rollback) và đã có giả định A07, A09 |
