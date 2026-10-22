# Task breakdown — từ detail design LAB-4 ra backlog

Nguồn: 13 screen spec của LAB-4 core, T2 (ERD và bảng chênh lệch G01–G23), T3 (kiến trúc), ADR-001 → 005. Các thay đổi so với LAB-4 và các giả định nằm ở [PREMISE.md](PREMISE.md).
Dữ liệu gốc của backlog: [`backlog/backlog-items.json`](backlog/backlog-items.json), gồm 10 epic, 41 issue, 42 sub-issue (67 task lá được chấm SWP và giờ). Mã như `08.1.6` là mã trong file đó. Số issue trên GitHub Project ghi trong ngoặc, ví dụ `08.1.6 (#…)`.

## 1. Nguyên tắc chia task

**Độ hạt: chia tới đâu thì dừng**

- Mỗi task lá (issue không có con, hoặc sub-issue) phải đủ để **một người làm xong trong ≤ 2 ngày (≤ 16 giờ)** và có dòng "Xong khi" kiểm được bằng một test hoặc một lần so với wireframe.
- Dừng chia khi chia tiếp chỉ ra những bước không kiểm riêng được. Ví dụ "viết migration" và "viết test migration" là một task, không tách hai.
- Màn nào thay đổi ít, tất cả nằm trong một tầng, thì cả màn là một issue (ví dụ 07.2, 08.3).

**Khi nào tách sub-issue**

1. Issue chạm nhiều tầng mà mỗi tầng có thể giao cho người khác: DB/SQL, API, UI, test E2E.
2. Issue ước lượng vượt 16 giờ.
3. Issue chứa nhiều quy tắc nghiệp vụ, mỗi quy tắc có test vector riêng. Đây là lý do 完納奨励金 tách theo từng bước tính (mục 3).
4. Một phần của issue phụ thuộc issue khác, còn phần kia thì không. Tách ra để phần không phụ thuộc chạy trước.

**Định nghĩa xong (áp cho mọi task lá)**

- Code đã merge vào nhánh chính. Test tự động ghi ở "Xong khi" xanh trên CI.
- Migration lên và lùi được trên DB có seed.
- Qua quality gate hai lớp: AI review (agent `reviewer`) **và** một người review đạt. AI đạt mà người chưa đạt thì chưa xong.
- Màn hình khớp wireframe LAB-4 (số tròn xanh = cột No của spec).
- Nếu lúc làm phải khác spec thì sửa spec và thêm dòng vào PREMISE.md trước khi đóng issue.
- Issue làm rõ (nhãn `clarify`) xong khi có câu trả lời của khách, PREMISE.md đã cập nhật, và các issue bị ảnh hưởng đã sửa mô tả.

**Cách dùng epic → issue → sub-issue trên Project**

| Cấp | Là gì | Trên GitHub |
|---|---|---|
| Epic | Một nhóm chức năng (1–2 màn) hoặc một khối nền tảng | Issue có nhãn `epic`; các issue con gắn bằng sub-issue |
| Issue | Một màn, hoặc một thay đổi có giá trị kiểm được | Sub-issue của epic |
| Sub-issue | Phần việc một người làm | Sub-issue của issue |

- **SWP** chỉ chấm ở task lá. Issue cha và epic lấy tổng của các con, không chấm riêng.
- **Giờ ước lượng** ghi ở task lá. Cha lấy tổng.
- Nhãn: `layer:db`, `layer:api`, `layer:ui`, `layer:test`, `layer:infra`, `clarify`, `constraint:完納奨励金`.
- Mỗi task lá có Status, Iteration và người phụ trách giả định (tên bịa, không phải người thật).

## 2. Spec → issue

| Spec | Epic | Issue / sub-issue | Phần spec chưa thành issue và vì sao |
|---|---|---|---|
| T2 G08, G09, G13, G18; T3 §5, I2, I5, I6 (dùng chung) | E01 Nền tảng dùng chung | 01.1 (01.1.1–01.1.3) tệp chứng cứ · 01.2 (01.2.1–01.2.2) email · 01.3 (01.3.1–01.3.2) offline · 01.4 job | T3 I3 xuất kế toán IF-ACC-01: chưa chốt cách truyền (Q12), và không gắn với màn nào trong 13 màn. T3 I7 in phiếu lô: chưa có mẫu in (Q07) |
| SCR-F02-02 Đăng ký / sửa người tham gia | E02 Tư cách theo căn cứ | 02.1 (02.1.1–02.1.2) mô hình dữ liệu · 02.2 (02.2.1–02.2.3) | Màn quản lý danh mục 出荷者 (`shippers`): chưa có spec, chưa biết vai trò nào được sửa (Q-F0202-06, C06). Đợt này chỉ tạo bảng và seed |
| SCR-F02-03 Chi tiết, đổi trạng thái tư cách | E02 | 02.3 (02.3.1–02.3.4) · 02.4 job hết hạn | Nhánh 買出人 bị khoá (A07, chờ C06). Đường ra của 条件確認中 khi không đạt điều kiện: chưa có trong T3 §6 (Q-F0203-03) |
| SCR-F03-01 Tiếp nhận lô | E03 Tiếp nhận, đánh giá lô | 03.1 (03.1.1–03.1.4) | Mục "荷目" của FR-LOT-01: chưa rõ là gì (Q-F0301-05, C08). Màn xử lý trùng SCR-F16-01: không thuộc 13 màn; đợt này chỉ hỏi xác nhận ngay trên SCR-F03-01 |
| SCR-F03-02 Đánh giá lô | E03 | 03.2 (03.2.1–03.2.2) | Đánh giá lại lô `完売` (Q-F0302-01): chưa quyết, prototype không cho |
| SCR-F04-01 Nhập giao dịch 相対 | E04 Chốt giao dịch | 04.1 (04.1.1–04.1.2) dùng chung · 04.2 (04.2.1–04.2.2) | Cảnh báo 単価 bất thường (Q-F0401-01): RFP không yêu cầu, chờ khách |
| SCR-F05-01 Nhập kết quả せり | E04 | 04.1 dùng chung · 04.3 (04.3.1–04.3.2) | Một lô せり nhiều người trúng (Q-F0501-03): giữ như prototype, không có việc mới |
| SCR-F06-01 Tạo yêu cầu sửa | E05 Sửa sau chốt | 05.1 (05.1.1–05.1.2) | Sửa người mua / lô hoặc bản ghi giao hàng qua yêu cầu sửa (Q-F0601-02, Q-F0601-03): chưa có trong spec |
| SCR-F06-03 Duyệt yêu cầu sửa | E05 | 05.2 (05.2.1–05.2.2) · 05.3 test hồi quy | Logic duyệt, delta, 差分 giữ như prototype (spec §9 ghi rõ). Chỉ thêm test hồi quy 05.3 |
| SCR-F07-02 Giao hàng và ngoại lệ | E06 Giao hàng | 06.1 · 06.2 · 06.3 · 06.4 · 06.5 | Người xử lý ngoại lệ `未処理` và cách đóng ngoại lệ (Q-F0702-06, C04): đợt này chỉ tạo ngoại lệ và hiện trên bảng |
| SCR-F08-01 Đối soát ngày | E07 Đối soát, khoá ngày | 07.1 (07.1.1–07.1.2) · 07.2 · 07.3 | Màn tranh chấp SCR-F08-03/04: chưa có detail design, đợt này chỉ đặt link (D1). 11 báo cáo RPT còn lại: chưa có spec (S04) |
| SCR-F08-02 Khoá / mở khoá ngày | E07 | 07.4 (07.4.1–07.4.2) · 07.5 · 07.6; D3 → 01.4; D6 → 06.4 | D1 kiểm tranh chấp trước khoá: bỏ khỏi đợt này vì cần bảng `disputes` (S01). Mở khoá hai người (Q-F0802-03): chưa quyết |
| SCR-F09-02 Tính 完納奨励金 | E08 完納奨励金 | 08.1 (08.1.1–08.1.6) · 08.2 · 08.3 · 08.4 | Điều chỉnh hồi tố khi rollback một bản quy tắc đã có hiệu lực (Q-F1003-04): cần cơ chế ngoài FR-INC-03, chờ C07 |
| SCR-F10-03 Duyệt phiên bản quy tắc | E09 Phiên bản quy tắc | 09.1 · 09.2 | Đính kèm 市場規程 khi lập / duyệt (Q-F1003-05): RFP chưa yêu cầu |
| Mục 11 "Câu hỏi mở" của 13 spec, T2 §4 | E10 Làm rõ với khách | C01–C08 (gom 68 câu hỏi theo chủ đề) | Q-F0202-01 đã gộp vào Q-F0203-02; Q-F0203-01 đã giải quyết ở LAB-4. Hai câu này không còn việc |

## 3. Hạng mục chịu ràng buộc đặc thù của đề (Product A: 完納奨励金)

BR-INC-01 có nhiều biến, mỗi biến sai theo một kiểu riêng. Gộp chung vào một task "tính thưởng" thì không ước lượng được và khi test hỏng không biết hỏng ở đâu. Vì vậy mỗi biến là một sub-issue, có test vector riêng (nhãn `constraint:完納奨励金`).

| Ràng buộc | Issue | Vì sao tách riêng |
|---|---|---|
| Đối tượng tính: giao dịch 確定 trong kỳ, giá trị hiệu lực sau sửa, chỉ người có `payments` kỳ đó | 08.1.1 | Đây là chỗ prototype đang sai ngầm: chỉ đọc được khoảng 1.000 giao dịch mỗi kỳ (G23), trong khi một tháng bình thường có khoảng 18.000. Phải chuyển sang tổng hợp trong SQL và có test tải riêng. Còn phụ thuộc giả định A11 (giao chia lần) |
| Đúng hạn: `paid_date ≤ due_date`, không có ân hạn, theo ngày JST; trễ hoặc chưa trả thì thưởng bằng 0 nhưng vẫn lưu dòng | 08.1.2 | Quy tắc "trễ 1 ngày cũng mất toàn bộ thưởng" có ảnh hưởng tiền lớn và dễ lệch múi giờ. Cần test biên theo ngày riêng |
| Phiên bản quy tắc: chọn bản 承認済 theo ngày hiệu lực, tách dòng khi kỳ có 2 bản, bỏ bản 取消 | 08.1.3 | Phải đổi cấu trúc dữ liệu (text → FK, G12) và phụ thuộc E09 (rollback). Tách ra để làm song song với E09 |
| Bậc tỉ lệ: chọn theo tổng cả kỳ (mọi phiên bản cộng lại); đúng bằng ngưỡng thì lấy bậc trên | 08.1.4 | Ca biên INC-EDGE-01 của RFP. Chọn bậc theo tổng kỳ nhưng áp cho từng dòng phiên bản là chỗ dễ làm sai |
| Hệ số thuế 110/100 và cắt lẻ JPY bằng số nguyên | 08.1.5 | Ca INC-EDGE-03. Dùng số thực là lệch 1 円. Cần test số rất lớn để chắc không tràn |
| Điều chỉnh sau khi chốt kỳ: dòng 差分 ở kỳ sau, kế thừa tỉ lệ và cờ đúng hạn của kỳ gốc, không sửa kỳ gốc; quy tắc làm tròn số âm | 08.1.6 | Ca INC-EDGE-02, nối với E05 (sửa sau chốt). Còn câu hỏi mở về số âm (A10) và về bậc của 差分 (Q-F0902-03). Tách ra để khi khách trả lời chỉ phải sửa một task |
| Ghi kết quả một lần, không sửa được: khoá theo kỳ, kiểm "đã tính", đánh dấu chênh lệch đã dùng, audit | 08.2 | Kết quả không sửa được, nên bấm 2 lần hoặc 2 người cùng bấm là lỗi khó lùi. Đây là bài test đồng thời, khác hẳn bài test công thức |
| Nghiệm thu theo test vector của khách | 08.4, C05 | RFP C.3 không cho số cụ thể. Cần khách cung cấp số liệu, và việc này có thể trễ độc lập với việc code |

## 4. Chỗ hở hoặc mâu thuẫn của spec LAB-4 phát hiện khi break

| Spec | Chỗ hở / mâu thuẫn | Xử lý |
|---|---|---|
| SCR-F08-02 §9 D1 | Kiểm tranh chấp trước khi khoá cần bảng `disputes` (G07), nhưng màn tranh chấp chưa có detail design | Đã sửa thiết kế ([PREMISE S01](PREMISE.md#1-spec-thêm--bỏ--sửa-so-với-lab-4)) |
| SCR-F05-01 §9 D7 | Vẫn trỏ tới F04-01 D10 (`?next=`), trong khi review R09 đã bỏ D10 | Đã sửa thiết kế (PREMISE S02) |
| SCR-F07-02 D8 và SCR-F08-02 D6 | Hai spec cùng mô tả một thay đổi (G21). Để nguyên thì thành hai issue và đếm trùng | Đã sửa thiết kế (PREMISE S03) → một issue 06.4 |
| SCR-F08-01 §9 D4 | "Báo cáo ngày" không nói gồm báo cáo nào. T3 §2 ghi 12 báo cáo nhưng không có spec | Đã sửa thiết kế (PREMISE S04) |
| SCR-F09-02 §7 bước 1 | Không nói giao hàng chia lần, 不足 có làm đổi số tiền đủ điều kiện không, dù RFP coi đây là điều kiện để chốt estimate | Đã sửa thiết kế (PREMISE S05) + giả định (PREMISE A11) + tạo issue làm rõ C05 (#…) |
| SCR-F07-02 D8 / G21 | Giao hàng trên ngày đã khoá: spec để hai phương án, chưa chốt | Giả định (PREMISE A05, H03) + tạo issue làm rõ C04 (#…) |
| SCR-F02-02, F02-03, F03-01, F06-01, F07-02 | Chính sách tệp chứng cứ (bắt buộc ở đâu, loại, dung lượng) để ngỏ ở cả 5 spec | Giả định (PREMISE A02) + tạo issue làm rõ C01 (#…) |
| SCR-F02-03, F08-02, F09-02, F10-03 | "Chỉ 責任者 được làm" hiểu khác nhau giữa các spec. Không spec nào nói MFA | Giả định (PREMISE A01) + tạo issue làm rõ C02 (#…) |
| SCR-F03-01, F03-02, F07-02 | Phạm vi offline rộng hơn T3 §5 ở một số chỗ (đánh giá lô, 完了, ngoại lệ, đổi ca trên tablet) | Giả định (PREMISE A06) + tạo issue làm rõ C03 (#…) |
| SCR-F09-02 §7 bước 6 | BR-INC-01 ghi "切り捨て" nhưng không nói cách làm với số âm | Giả định (PREMISE A10) + tạo issue làm rõ C05 (#…) |
| SCR-F10-03 §11 | Rollback có tính vào giới hạn 4 lần không; năm dương lịch hay năm tài chính | Giả định (PREMISE A09) + tạo issue làm rõ C07 (#…) |
| SCR-F02-02 No 1, SCR-F04-01 No 3 | RFP nói khác nhau về việc 買出人 có được là bên mua không (02-02 và FR-AITAI-01) | Giả định (PREMISE A07) + tạo issue làm rõ C06 (#…) |
| T3 I3 (xuất kế toán IF-ACC-01) | Cách truyền, xác thực, retry chưa chốt (Q12) | Để mở: không thuộc 13 màn của đợt này. Đưa vào đợt sau, cùng với màn xuất kế toán |
| SCR-F10-03 Q-F1003-04 | Rollback một bản đã có hiệu lực có điều chỉnh thưởng hồi tố không: cần cơ chế mới ngoài FR-INC-03 | Để mở: RFP không yêu cầu hồi tố. Hỏi trong C07; nếu khách cần thì là hạng mục mới, báo giá riêng |
