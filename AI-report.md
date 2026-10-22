# AI report — dùng AI để break task, chấm SWP, quy giờ và báo cáo tiến độ

Công cụ: Claude Code (desktop) trên bộ skill Takumi. Agent chính điều phối toàn bộ. 5 subagent `sun-estimate-worker` chấm điểm song song. Mọi thao tác ghi lên GitHub đi qua script trong `scripts/`, AI không sửa board bằng tay. Người (học viên) giữ các quyết định: phạm vi, nền backlog, duyệt tài liệu, duyệt điểm mẫu, cho phép tạo repo / Project public.

## 1. Đã dùng skill nào, prompt thế nào cho từng việc

| Việc | Skill / agent | Prompt (người viết) | AI đã làm |
|---|---|---|---|
| Phân tích đề | — (agent chính) | "Đọc đề bài LAB-5, trước tiên phân tích giúp tôi và nêu ra các công việc cần làm" | Đọc đề, đối chiếu với thư mục LAB-1 → LAB-4. Tách 4 tiêu chí chấm, lên 8 bước. Phát hiện máy chưa có `gh` CLI. Liệt kê các quyết định thuộc về người |
| Break task | — (agent chính đọc spec) | "Chỉ break 13 màn đã có detail design ở LAB-4 core. Phần còn lại ghi là chưa thành issue." Sau đó chọn trong câu hỏi: "Nâng prototype lên to-be" | Đọc §8 (API), §9 (khác prototype), §11 (câu hỏi mở) của 13 spec, cùng T2, T3, ADR. Dựng `backlog/backlog-items.json` (10 epic, 41 issue, 42 sub-issue), mỗi task lá có dòng "Xong khi". Chạy script kiểm: mọi mục D# của spec có issue, mọi câu hỏi mở nằm trong một issue làm rõ. Viết PREMISE.md và task-breakdown.md |
| Đưa lên GitHub | — (agent chính viết script) | "Đồng ý tạo repo public sakura-market-lab5-backlog và Project trên anhnn-1576" | Tạo repo, Project, các trường Status / Iteration / SWP / Estimate (h) / Phụ trách (giả định). Viết `push-backlog-to-github-project.py` (chạy lặp được, lưu map mã ↔ số issue) để tạo 93 issue và sub-issue. Đọc lại bằng GraphQL để kiểm cha con và tư cách thành viên Project |
| Chấm SWP | `tkm:sun-estimate` (+ `tkm:confidence`), 5 × `sun-estimate-worker` | "ok, chấm SWP" | Skill đọc Project (chỉ đọc, qua cổng kiểm `tool_policy.py`), chọn 67 task lá bằng selector cố định, chia 5 lô. Mỗi worker nhận prompt gồm **hợp đồng chấm** (bảng Scope × Complexity → SWP, thang băng, từ vựng signature, quy tắc chống đếm trùng, điều kiện tách) và dữ liệu issue của lô, không nhận gì khác. Worker trả JSON. Agent chính validate, chọn 5 mẫu bằng thuật toán của skill, hỏi người từng mẫu một (mức độ khó → điểm cụ thể), rồi xuất báo cáo HTML |
| Agent ghi SWP lên Project | — (agent chính viết script) | "Viết script ghi finalSWP từ payload đã validate vào trường SWP của 67 task lá trên Project, kiểm lại rồi commit báo cáo HTML" | Skill chỉ được đọc, nên agent viết script riêng. Script đọc payload **nhúng trong báo cáo HTML đã validate** (không đọc từ trí nhớ của AI), từ chối nếu báo cáo chưa qua review mẫu, chỉ ghi task lá. Sau đó đọc board bằng một lệnh độc lập để so: 67/67 |
| Quy giờ | — (agent chính) | "Đề xuất cách quy SWP ra giờ, ghi trường Estimate (h) lên Project và viết estimate.md (kèm so sánh LAB-1)" | Đề xuất `giờ = SWP × 1,5 + 1` (issue làm rõ không +1). Neo vào 2 mẫu người đã duyệt. Đưa quy tắc vào một hàm duy nhất trong script. Đọc `01_Server` của file estimate LAB-1, ghép dòng LAB-1 với epic LAB-5 để so |
| Báo cáo tiến độ | — (agent chính) | "Lên kế hoạch Sprint 1 (giả lập 26/10–6/11), gán Iteration, người phụ trách, cập nhật trạng thái trên Project rồi viết progress-report.md có burndown và rủi ro trễ" | Dựng `backlog/sprint-plan.json` (năng lực, gán người, trạng thái cuối sprint, ngày Done). Viết script áp kế hoạch lên board và script vẽ burndown. **Cả hai đọc cùng một file**, nên board, ảnh và bảng không thể lệch nhau. Viết báo cáo kèm dự báo trễ và 6 rủi ro |

## 2. Review output của AI: ai review, ở bước nào, bắt được gì

**Người review ở các bước sau:**
1. Chọn phạm vi (13 màn) và nền backlog (nâng prototype). AI hỏi và đưa khuyến nghị, người quyết.
2. Đọc PREMISE.md và task-breakdown.md **trước khi đẩy lên GitHub** (người chủ động chặn lại để đọc). Không có góp ý.
3. Cho phép tạo repo và Project public trên tài khoản của mình.
4. Duyệt 5 issue mẫu của skill chấm SWP, mỗi mẫu 2 vòng (mức độ khó, rồi điểm). Giữ nguyên cả 5. Lý do ghi ở `estimate.md` mục 1.
5. Duyệt từng bước tiếp theo qua câu hỏi cuối mỗi lượt. AI không tự chuyển bước.

**AI tự kiểm (lớp AI của quality gate):** script đối chiếu spec với backlog, validator của skill, đọc lại board sau mỗi lần ghi, tự soát số liệu báo cáo trước khi push. Ngoài ra có một agent `reviewer` đọc chéo số liệu giữa các file trước lần push cuối.

**Vấn đề phát hiện trong output của AI và cách xử lý:**

| # | Ở đâu | Vấn đề | Ai / cái gì bắt được | Xử lý |
|---|---|---|---|---|
| 1 | Backlog | Câu hỏi Q-F0301-05 (mục "荷目") không nằm trong issue làm rõ nào | Script đối chiếu §11 của 13 spec với backlog | Thêm vào C08 (#93) |
| 2 | Backlog | Script đối chiếu báo thiếu F08-02 D1 | Script đối chiếu | Không phải lỗi: cố ý bỏ (kiểm tranh chấp cần bảng chưa thiết kế). Ghi thành PREMISE S01 thay vì để lặng lẽ |
| 3 | task-breakdown.md | AI viết "gom 70 câu hỏi", đếm thật là 68 | Script đếm mã câu hỏi | Sửa thành 68 |
| 4 | PREMISE.md, task-breakdown.md | Khi thay mã tạm bằng số issue, regex bỏ sót mã đứng trước dấu chấm (ví dụ "08.2.") và để lại ô epic rỗng dạng "#13 —" | Script quét lại sau khi thay | Sửa regex, chạy lại, quét đến khi không còn mã sót |
| 5 | Commit đầu tiên | Tác giả commit là email công ty. Repo public thì email này lộ ra, trái luật "không dữ liệu cá nhân" | Agent kiểm `git log` trước khi push | Đổi sang email noreply của GitHub (chỉ cho repo này), sửa commit trước khi push lần đầu |
| 6 | Script đẩy backlog | Lỗi 1: dừng vì lỗi bảng mã khi in. Lỗi 2: workflow "tự thêm sub-issue" của Project khiến bước thêm vào Project báo "đã có", **issue #4 được tạo mà chưa ghi vào map**. Chạy lại mù sẽ tạo issue trùng | Agent đọc log lỗi và kiểm danh sách issue trên GitHub | Ghi tay #4 vào map, đổi thứ tự (thêm vào Project trước, nối sub-issue sau). Kiểm cuối: 93/93 issue, không trùng tiêu đề, cha con đúng |
| 7 | Skill chấm SWP | Trên Windows, script của skill ghi tiếng Việt theo cp1252: dữ liệu issue bị vỡ chữ **trước khi** gửi cho worker. Không bắt thì worker chấm trên chữ hỏng | Agent đọc lại đầu ra của planner | Chạy lại selector và planner với UTF-8, kiểm lại chữ rồi mới gửi worker |
| 8 | Output của worker | 20 dòng sắp nhãn signature sai thứ tự. 8 issue làm rõ đều xếp discipline `Unknown`, trong đó 7 issue có confidence chưa phải `low` (hợp đồng bắt buộc low; #93 đã low sẵn) | Validator của skill (hỏng ở bước validate, không cho đi tiếp) | Sắp lại thứ tự, hạ confidence của 7 dòng. Không đổi trục điểm nào. Ghi cả hai vào caveat của báo cáo HTML |
| 9 | Kiểm tra của agent | Đoạn kiểm SWP do agent tự viết tra bảng sai cách (dùng giá trị băng làm chỉ số), báo cả 67 dòng sai | Agent đối chiếu với `derive_swp()` của skill | Báo động giả. Bỏ đoạn tự viết, dùng hàm của skill làm chuẩn |
| 10 | Điểm SWP | Các bước tính 完納奨励金 chỉ 1–4 SWP mỗi bước, đa số 1–2. Dễ hiểu nhầm là hạng mục này nhẹ | Agent đọc lại kết quả trước khi báo cho người | Nêu rõ trong estimate.md: phần nặng nằm ở ghi nguyên tử (#79) và nghiệm thu test vector (#81), không nằm ở từng công thức |
| 11 | progress-report.md (bản nháp) | Số task chuyển tiếp ghi 13 (đúng là 14). Rủi ro R1 trỏ tới #9 (container) thay vì #56. Dự báo ghi "trễ 2–3 tuần, giữa Sprint 4 hoặc 5", không khớp phép tính (≈ 22/12). Rủi ro SES ghi sai sprint của #48, #51 | Agent tự soát từng con số với dữ liệu kế hoạch trước khi commit | Sửa cả 4 chỗ. Lỗi dự báo là kiểu "tô hồng / nói mơ hồ" mà báo cáo gửi khách không được có |
| 12 | 6 file .md (lần soát cuối trước khi push) | Agent `reviewer` dùng script tính lại hơn 100 con số. Số liệu khớp hết, nhưng bắt được 4 lỗi câu chữ: ghi "1–2 SWP mỗi bước" trong khi #75 là 4 SWP; câu "không con số nào gõ hai lần" là nói quá (bảng .md chép tay); tham chiếu #82 (epic) thay cho #83; làm tròn 43 % thay vì 44 %. Thêm 2 chỗ viết chưa rõ: số issue làm rõ (8 issue, 7 bị hạ confidence) và mốc 10:30 / 11:00 của #65 | Agent `reviewer` (chỉ đọc, độc lập với agent viết) | Người điều phối kiểm từng điểm với dữ liệu, sửa cả 6. Hai chỗ "viết chưa rõ" không sai nội dung, chỉ viết lại cho rõ. Sửa tiêu đề #65 trên GitHub. Ghi rõ trong báo cáo tiến độ đâu là số liệu giả lập |

## 3. Điểm đặc biệt trong cách dùng AI

**Chỗ tin là hiệu quả:**
- **Một nguồn dữ liệu, nhiều đầu ra.** `backlog-items.json` → issue. Payload của báo cáo HTML → SWP và giờ trên board. `sprint-plan.json` → trạng thái trên board và burndown. Board, báo cáo HTML và burndown được sinh từ các file này nên không lệch nhau. Riêng các bảng số trong file .md vẫn chép tay từ dữ liệu. Chúng được kiểm lại bằng script và bởi agent `reviewer`, và vẫn có lệch câu chữ (xem dòng 12). Làm thật nên sinh luôn các bảng này từ dữ liệu.
- **Đọc lại sau mỗi lần ghi.** Mỗi lần ghi lên GitHub đều có một lần đọc lại độc lập với script ghi (93/93, 67/67). Lỗi #6 bị bắt nhờ thói quen này.
- **Chấm SWP theo hợp đồng cố định, không theo cảm giác.** Bảng tra cố định, worker cô lập, validator chặn output sai hợp đồng, người chỉ duyệt 5 mẫu do thuật toán chọn. Bảng tra và validator là cố định. Riêng phần chấm trục Scope / Complexity vẫn do LLM, và bài này chưa chạy lại lần hai để chứng minh điểm lặp lại được.
- **Tách nhỏ ràng buộc đặc thù ngay từ khâu break.** Vì 完納奨励金 đã tách theo biến, mỗi task chỉ 1–4 SWP và có test vector riêng. Khi khách trả lời C05 chỉ phải sửa đúng task bị ảnh hưởng.

**Chỗ chưa tốt, cần cải thiện khi làm thật:**
- **Tiến độ là giả lập.** Ngày Done do AI dựng theo kịch bản hợp lý. Làm thật thì burndown phải lấy từ lịch sử đổi trạng thái trên Project (API `ProjectV2ItemFieldValue` theo ngày), không lấy từ file kế hoạch.
- **Tỉ lệ 1,5 giờ/SWP chưa có dữ liệu lịch sử.** Chỉ neo vào 2 mẫu. Sau 2–3 sprint thật cần hiệu chỉnh bằng giờ thực tế (skill có sẵn phần đọc lịch sử qua KPI Insight).
- **Tốn token ở bước worker.** Worker không có tool nên agent phải chép toàn bộ dữ liệu lô vào prompt (khoảng 10 KB × 5). Với backlog vài trăm issue nên dùng một bước gom lô có giới hạn, hoặc cho worker đọc file chỉ-đọc.
- **Môi trường Windows gây lỗi lặt vặt** (bảng mã, `python -I` bỏ qua biến môi trường). Nên chuẩn hoá `PYTHONUTF8=1` trong cấu hình dự án từ đầu.
- **Script chưa có test tự động.** Hiện kiểm bằng đọc lại board. Làm thật cần test cho phần suy trạng thái container và quy tắc quy giờ.
- **Đóng issue chưa đi cùng đổi Status.** Thanh tiến độ sub-issue của GitHub đếm theo issue đã đóng, không theo trường Status. AI chỉ phát hiện điều này khi mở Project ở chế độ chưa đăng nhập, sau khi ghi Status Done. Người duyệt rồi mới đóng 16 issue (14 task lá + 2 container đã xong hết con). Làm thật nên để workflow của Project đồng bộ hai chiều Status ↔ đóng / mở issue.
- **View của Project không cấu hình được bằng API.** Các cột SWP, giờ, Iteration, người phụ trách phải do người tự bật trên giao diện. Người chưa đăng nhập cũng không mở được danh sách sub-issue, nên cần cột Parent issue.

**Chưa có ý tưởng tốt:** làm sao để AI tự nhận ra khi giả định (A01–A11) đã cũ mà khách chưa trả lời. Hiện vẫn dựa vào BrSE theo dõi các issue làm rõ.
