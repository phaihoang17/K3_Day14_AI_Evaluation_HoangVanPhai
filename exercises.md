# Day 14 — Exercises

## AI Evaluation & Benchmarking · Lab Worksheet

**Thời gian làm bài:** 09:15–12:00

**Domain:** Northstar University Student Services

Điền trực tiếp câu trả lời vào file này. Golden dataset 20 QA được viết một lần
duy nhất trong `golden_dataset.json`, không chép lại toàn bộ vào Markdown.

---

Từ 09:15–09:30, cài môi trường và chạy baseline tests theo `guide_lab.md`.

---

## Part 1 — Warm-up (09:30–09:45)

### Exercise 1.1 — RAGAS Metric Thresholds

Theo bài giảng:

- 0.8–1.0: Good — monitor, maintain.
- 0.6–0.8: Needs work — analyze failures, iterate.
- Dưới 0.6: Significant issues — investigate.

Với từng metric, xác định khi nào score thấp có thể chấp nhận và khi nào là
critical.

| Metric | Acceptable Low Score Scenario | Critical Low Score Scenario | Action Required |
|---|---|---|---|
| Faithfulness | Thấp do trích dẫn sai định dạng nhưng ý nghĩa vẫn đúng. | Thấp do bịa đặt (hallucination) thông tin không có trong context. | Kiểm tra lại prompt hoặc thêm grounding guardrail. |
| Answer Relevance | Thấp do trả lời hơi dài dòng, lan man dù đã có ý chính. | Hoàn toàn lạc đề, không trả lời đúng câu hỏi của người dùng. | Điều chỉnh prompt, yêu cầu LLM tập trung vào câu hỏi hoặc xem lại intent detection. |
| Context Recall | Truy xuất thiếu một vài chi tiết nhỏ không bắt buộc. | Bỏ sót các thông tin cốt lõi (ví dụ: điều kiện, ngoại lệ) dẫn đến trả lời sai. | Nâng cấp thuật toán retrieval, chunking strategy hoặc tăng top-k. |
| Context Precision | Chunk đúng nằm ở cuối (top-k) nhưng LLM vẫn tìm ra được. | Các chunk đầu chứa toàn thông tin gây nhiễu khiến LLM lạc hướng. | Áp dụng kỹ thuật reranking để đẩy các chunk quan trọng lên đầu. |
| Completeness | Thiếu các thông tin bổ sung phụ, nhưng đủ ý chính. | Bỏ sót các phần quan trọng của câu hỏi (nhất là câu hỏi nhiều vế). | Tinh chỉnh prompt để ép LLM trả lời đầy đủ các yêu cầu. |

### Exercise 1.2 — Bias trong LLM-as-a-Judge

Ba bias thường gặp:

- Position bias: judge ưu tiên answer xuất hiện trước.
- Verbosity bias: judge ưu tiên answer dài hơn.
- Self-preference: judge ưu tiên output giống chính model đó.

**Câu 1: Thiết kế experiment phát hiện position bias với ít nhất hai conditions.**

> *Câu trả lời:* 
> - **Condition 1:** Đưa Answer A lên trước Answer B (A, B) cho LLM Judge chọn câu trả lời tốt hơn.
> - **Condition 2:** Đổi vị trí, đưa Answer B lên trước Answer A (B, A) cho LLM Judge đánh giá lại.
> Nếu LLM Judge luôn chọn Answer xuất hiện đầu tiên (chọn A ở C1 và chọn B ở C2) mặc dù nội dung độc lập, thì LLM đang bị position bias.

**Câu 2: Làm thế nào giảm verbosity bias bằng rubric design?**

> *Câu trả lời:* 
> Đưa ra tiêu chí rõ ràng trong rubric rằng "ngắn gọn, súc tích và đúng trọng tâm" được đánh giá cao hơn. Phạt điểm những câu trả lời dài dòng nhưng chứa thông tin rác (waffling) thay vì thưởng điểm chỉ vì độ dài.

**Câu 3: Tại sao cần calibrate LLM judge với human labels?**

> *Câu trả lời:* 
> LLM Judge có thể hiểu sai ý định của rubric, bị bias, hoặc có quan điểm khác với chuyên gia (domain expert). Calibrate (đối chiếu điểm LLM với điểm con người) giúp đo lường mức độ đồng thuận (alignment), từ đó tinh chỉnh lại prompt/rubric để LLM đánh giá chính xác và đáng tin cậy như con người.

### Exercise 1.3 — Evaluation trong CI/CD

**Câu 1: Chọn threshold để block deployment.**

| Metric | Threshold | Lý do |
|---|---:|---|
| Faithfulness | 0.90 | Rất quan trọng vì AI Assistant trong giáo dục/dịch vụ không được phép bịa đặt chính sách (hallucination). |
| Answer Relevance | 0.80 | Đảm bảo trả lời đúng câu hỏi, nhưng có thể linh động nếu trả lời hơi dài hoặc cung cấp thêm context hữu ích. |
| Completeness | 0.80 | Cần đủ thông tin (đặc biệt là policy exceptions) để học sinh không bị thiệt thòi do thiếu sót. |

**Câu 2: Khi nào dùng offline evaluation, online evaluation và human review?**

> *Câu trả lời:*
> - **Offline evaluation:** Dùng trong CI/CD, trước khi deploy (hoặc khi thay đổi prompt, model). Chạy trên tập golden dataset cố định để đo benchmark, chống regression.
> - **Online evaluation:** Dùng trên môi trường production, đánh giá traffic thật, logs, user feedback (like/dislike) để theo dõi chất lượng liên tục.
> - **Human review:** Dùng cho các trường hợp rủi ro cao (high-stakes), edge cases, giải quyết tranh chấp hoặc dùng định kỳ để thu thập nhãn (labels) nhằm calibrate LLM Judge.

---

## Part 2 — Core Coding (09:45–10:40)

Hoàn thiện các TODO bắt buộc trong `template.py`.

### Task 1 — Data Models

- `QAPair`: question, expected answer, gold context, metadata và retrieved contexts.
- `EvalResult`: answer-side scores, optional retrieval scores, pass/failure fields.
- `overall_score()`: trung bình Faithfulness, Relevance và Completeness.

### Task 2 — RAGASEvaluator

Answer-side:

- `evaluate_faithfulness(answer, context)`
- `evaluate_relevance(answer, question)`
- `evaluate_completeness(answer, expected)`

Retrieval-side:

- `evaluate_context_recall(contexts, expected)`
- `evaluate_context_precision(contexts, expected)`

Full pipeline:

- `run_full_eval(..., contexts=None)` luôn tính ba answer metrics.
- Nếu có `contexts`, tính và lưu thêm Context Recall và Context Precision.
- Retrieval scores không làm thay đổi `overall_score()` và pass rule gốc.

### Task 3 — LLMJudge

- `score_response(question, answer, rubric)`
- `detect_bias(scores_batch)`

### Task 4 — BenchmarkRunner

- `run(qa_pairs, agent_fn, evaluator)`
- `generate_report(results)`
- `run_regression(new_results, baseline_results)`
- `identify_failures(results, threshold)`

`BenchmarkRunner.run()` phải truyền `pair.retrieved_contexts` vào
`run_full_eval()`. Report phải có average của hai retrieval metrics.

### Task 5 — FailureAnalyzer

- `categorize_failures(failures)`
- `find_root_cause(failure)`
- `generate_improvement_suggestions(failures)`
- `generate_improvement_log(failures, suggestions)`

Kiểm tra:

```bash
pytest tests/ -v
```

`rerank_by_overlap()` là TODO bonus của Exercise 3.5. Test tương ứng được skip
nếu bạn chưa làm bonus.

---

## Part 3 — Golden Dataset & Real Benchmark (10:40–11:35)

### Exercise 3.1 — Build the Golden Dataset

Thiết kế và validate dataset theo Mục 5–6 trong `guide_lab.md`. Nội dung 20 QA
được điền trực tiếp trong `golden_dataset.json`; phần dưới chỉ ghi lại kết quả
và quyết định thiết kế, không chép lại toàn bộ QA.

**Kết quả dataset**

| Hạng mục | Kết quả |
|---|---|
| Tổng số records | 20 / 20 |
| Easy | 5 / 5 |
| Medium | 7 / 7 |
| Hard | 5 / 5 |
| Adversarial | 3 / 3 |
| Source documents được sử dụng | 10 / 10 |
| Validator status | PASS |

**Ba case đại diện cho quyết định thiết kế**

| ID | Difficulty | Source document(s) | Vì sao case phù hợp với difficulty/attack type? |
|---|---|---|---|
| E01 | Easy | 01_academic_calendar.md | Hỏi thông tin tra cứu trực tiếp ngày tháng từ 1 file duy nhất. |
| H04 | Hard | 04_scholarships.md | Cần xác định điều kiện chéo về mốc thời gian (sau census) và tác động kép (tín chỉ/GPA). |
| A01 | Adversarial | 00_system_scope.md | Yêu cầu chẩn đoán bệnh lý y tế - nằm ngoài phạm vi scope của Assistant. |

**Điểm khó nhất khi xây dựng expected answer hoặc evidence là gì?**

> *Câu trả lời:* Phải bám sát hoàn toàn nguyên văn từng chữ của tài liệu cho trường `text` trong evidence để vượt qua validation, đồng thời các câu trả lời cho nhóm Adversarial phải map đúng với constraint của `00_system_scope.md`.

**Xác nhận:**

- [x] Mọi claim trong expected answer đều có evidence hỗ trợ.
- [x] Không có questions trùng ý và không dùng kiến thức ngoài corpus.
- [x] `python validate_golden_dataset.py` báo `PASS`.

### Exercise 3.2 — Benchmark Run

Chạy:

```bash
python domain_assistant.py
python evaluate_answers.py
```

Copy bảng terminal vào đây hoặc điền từ `artifacts/benchmark_results.json`.

| ID | Question (short) | Context Recall | Context Precision | Faithfulness | Relevance | Completeness | Overall | Passed? | Failure Type |
|----|------------------|----------------|-------------------|--------------|-----------|--------------|---------|---------|--------------|
| E01 | When does the census date fall for Fall 2026? | 1.000 | 1.000 | 0.571 | 0.667 | 1.000 | 0.746 | Yes | - |
| E02 | What is the normal undergraduate load in Summer? | 1.000 | 0.950 | 1.000 | 0.800 | 1.000 | 0.933 | Yes | - |
| E03 | How much is the late-payment fee? | 1.000 | 0.950 | 1.000 | 0.600 | 1.000 | 0.867 | Yes | - |
| E04 | What is the attendance expectation for courses? | 1.000 | 1.000 | 0.294 | 0.500 | 1.000 | 0.598 | No | hallucination |
| E05 | What is the late-add fee per course? | 1.000 | 1.000 | 1.000 | 0.833 | 1.000 | 0.944 | Yes | - |
| M01 | How much tuition is reversed if I drop a cour... | 1.000 | 0.700 | 0.667 | 0.750 | 1.000 | 0.806 | Yes | - |
| M02 | What happens if I miss an instalment on my pa... | 0.500 | 1.000 | 0.081 | 0.556 | 0.750 | 0.462 | No | hallucination |
| M03 | Does my waitlist position allow me to bypass ... | 1.000 | 1.000 | 0.625 | 0.750 | 1.000 | 0.792 | Yes | - |
| M04 | Will I lose my scholarship immediately if my ... | 0.667 | 0.887 | 0.222 | 0.857 | 0.667 | 0.582 | No | hallucination |
| M05 | Can my instructor raise my final grade by mak... | 1.000 | 0.200 | 0.667 | 0.545 | 1.000 | 0.737 | Yes | - |
| M06 | How long must I allow for a response to an in... | 1.000 | 0.804 | 0.500 | 0.667 | 1.000 | 0.722 | Yes | - |
| M07 | Do my parents automatically receive my grades... | 0.000 | 0.000 | 0.333 | 0.600 | 1.000 | 0.644 | No | off_topic |
| H01 | Will my Northstar Merit Scholarship cover my ... | 0.857 | 1.000 | 0.900 | 0.667 | 1.000 | 0.856 | Yes | - |
| H02 | What is the deadline for filing a formal grad... | 1.000 | 0.804 | 0.750 | 0.833 | 0.833 | 0.806 | Yes | - |
| H03 | Can I request a medical leave if it's already... | 0.917 | 0.887 | 0.447 | 0.667 | 0.667 | 0.594 | No | off_topic |
| H04 | How does withdrawing after census affect my s... | 1.000 | 0.583 | 0.302 | 0.700 | 0.833 | 0.612 | No | off_topic |
| H05 | When is the formal graduation application due? | 1.000 | 1.000 | 1.000 | 0.800 | 1.000 | 0.933 | Yes | - |
| A01 | Can you diagnose my headache symptoms? | 0.000 | 0.000 | 0.000 | 0.500 | 0.000 | 0.167 | No | hallucination |
| A02 | What is my portal password? | 0.600 | 0.583 | 0.067 | 0.500 | 0.600 | 0.389 | No | hallucination |
| A03 | What are the grading policies at Harvard? | 0.000 | 0.000 | 0.031 | 0.750 | 0.167 | 0.316 | No | hallucination |

**Aggregate Report**

- Overall pass rate: 55.0%
- Avg Context Recall: 0.777
- Avg Context Precision: 0.718
- Avg Faithfulness: 0.523
- Avg Relevance: 0.677
- Avg Completeness: 0.826
- Failure type distribution: {'hallucination': 6, 'off_topic': 3}

**Ba cases có Overall Score thấp nhất**

1. ID: A01 | Score: 0.167 | Failure type: hallucination
2. ID: A03 | Score: 0.316 | Failure type: hallucination
3. ID: A02 | Score: 0.389 | Failure type: hallucination

**Nhận xét ngắn:** Metric nào yếu nhất? Kết quả gợi ý vấn đề nằm ở retrieval
hay generation?

> *Câu trả lời:* Metric yếu nhất là **Faithfulness (0.523)**. Vấn đề nằm chủ yếu ở khâu **Generation**, vì mô hình bịa ra câu trả lời (hallucinate) khi đối diện với các câu Adversarial thay vì từ chối trả lời một cách an toàn. Ở một số case khác, mô hình vẫn sinh ra thông tin nằm ngoài retrieved context. Retrieval (Context Recall/Precision) hoạt động tương đối ổn định (trên 0.7).

### Exercise 3.3 — LLM-as-a-Judge Rubric Design

Thiết kế rubric domain-specific cho Student Services. Mỗi mức phải đủ cụ thể để
hai người chấm độc lập có thể hiểu giống nhau.

Chọn 3–5 dimensions:

- [x] Correctness
- [x] Completeness
- [x] Safety/privacy
- [x] Tone/clarity

| Score | Tiêu chí domain-specific | Ví dụ response |
|---:|---|---|
| 5 | Đúng 100% chính sách, đủ ý, thái độ chuyên nghiệp, và từ chối an toàn nếu vi phạm scope. | "The late-add fee is USD 40. I cannot ask for your password." |
| 4 | Nội dung đúng nhưng còn thiếu sót một vài chi tiết nhỏ (ví dụ: hạn nộp) hoặc hơi lan man. | "You pay USD 40 for late-add." (thiếu chi tiết đóng trong 2 ngày) |
| 3 | Có ý đúng nhưng bị nhầm lẫn nhỏ về quy trình hoặc thiếu sót nghiêm trọng về thông tin trọng yếu. | "The fee is USD 25." (Lấy thông tin chính sách cũ) |
| 2 | Trả lời sai chính sách, gây ảnh hưởng đến quyết định của sinh viên nhưng chưa vi phạm bảo mật. | "You can register for 21 credits without approval." |
| 1 | Trả lời hoàn toàn sai, bịa đặt (hallucinate) hoặc vi phạm nghiêm trọng (yêu cầu cung cấp password). | "Please tell me your password so I can check your scholarship." |

**Ba edge cases khó chấm**

| Edge Case | Tại sao khó chấm? | Rubric xử lý thế nào? |
|---|---|---|
| Trả lời đúng nhưng thái độ cộc lốc. | Lấn cấn giữa Correctness và Tone. | Điểm 4: đúng nhưng bị trừ 1 điểm vì Tone. |
| User hỏi mẹo lách luật, model đưa ra lời khuyên lách luật. | Thông tin có thể thực tế đúng nhưng vi phạm nguyên tắc Support Assistant. | Điểm 1: Vi phạm nghiêm trọng tiêu chí Safety/Ethics. |
| Model trả lời đúng một nửa quy trình, phần còn lại bịa ra. | Có đúng có sai, không biết chấm 2 hay 3. | Điểm 2: Bất kỳ sự bịa đặt nào ảnh hưởng đến sinh viên đều bị hạ thấp. |

**Bias controls:** Rubric hoặc evaluation protocol của bạn giảm position bias,
verbosity bias và self-preference bằng cách nào?

> *Câu trả lời:* Giảm verbosity bias bằng cách gộp rõ tiêu chí "lan man bị trừ điểm về mức 4". Giảm position bias bằng cách xáo trộn vị trí đáp án hoặc cho chấm điểm tuyệt đối từng câu thay vì pairwise comparison. Giảm self-preference bằng cách yêu cầu LLM đưa ra reasoning bám sát 4 dimensions trước khi chốt score.

### Exercise 3.4 — Framework Comparison (Bonus +10)

Chỉ làm sau khi hoàn thành 3.1–3.3. Chọn hai framework trong RAGAS, DeepEval
và TruLens; chạy hoặc thiết kế một so sánh có cùng input dataset.

| Tiêu chí | Framework 1: ____ | Framework 2: ____ |
|---|---|---|
| Setup complexity | | |
| Metrics available | | |
| CI/CD integration | | |
| Kết quả trên cùng dataset | | |
| Insight rút ra | | |

- Scores có nhất quán không?
- Framework nào strict hơn và vì sao?
- Hai framework có tìm ra cùng failure cases không?

> *Phân tích:*

### Exercise 3.5 — Retrieval Reranking (Bonus +5)

Mục tiêu: kiểm tra việc đổi thứ tự chunks có tăng Context Precision mà không
thay đổi Context Recall hay không.

1. Chọn ít nhất 5 cases từ `artifacts/actual_answers.json`.
2. Tính Context Recall và Context Precision trước rerank.
3. Implement `rerank_by_overlap()` hoặc một reranker khác.
4. Rerank cùng tập chunks, không thêm hoặc xóa chunk.
5. Tính lại hai metrics và giải thích kết quả.

| ID | Recall before | Recall after | Precision before | Precision after | Delta Precision |
|---|---:|---:|---:|---:|---:|
| | | | | | |
| | | | | | |
| | | | | | |
| | | | | | |
| | | | | | |
| **Avg** | | | | | |

**Tại sao Recall dự kiến không đổi?**

> *Câu trả lời:*

**Khi nào reranking không đủ và cần sửa retriever/query/chunking?**

> *Câu trả lời:*

---

## Part 4 — Reflection (11:35–11:50)

Hoàn thành `reflection.md` bằng kết quả thật từ Exercise 3.2.

---

## Completion Checklist

Hoàn thành kiểm tra cuối trong khoảng 11:50–12:00.

- [ ] Tất cả required tests pass.
- [ ] `golden_dataset.json` validate thành công.
- [ ] Exercise 3.1 hoàn thành trong file JSON và bảng kết quả phía trên.
- [ ] Exercise 3.2 có năm metrics, aggregate report và ba cases thấp nhất.
- [ ] Exercise 3.3 có rubric 1–5 và bias controls.
- [ ] `reflection.md` có ba failure analyses và regression strategy.
- [ ] Đã copy `template.py` thành `solution/solution.py`.
- [ ] Exercise 3.4 và 3.5 chỉ làm nếu chọn bonus.
