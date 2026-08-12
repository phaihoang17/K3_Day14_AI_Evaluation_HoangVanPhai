import json
from template import RAGASEvaluator, rerank_by_overlap

with open('artifacts/actual_answers.json', 'r') as f:
    answers = json.load(f)['answers']
with open('golden_dataset.json', 'r') as f:
    golden = json.load(f)['qa_pairs']

golden_map = {q['id']: q for q in golden}

evaluator = RAGASEvaluator()
cases = ["M02", "M04", "M05", "H04", "A02"]

for cid in cases:
    gold = golden_map[cid]
    actual = next(a for a in answers if a['id'] == cid)
    
    q = gold['question']
    expected_ans = gold['expected_answer']
    actual_ctxs = [c['text'] for c in actual['retrieved_contexts']]
    
    # Before
    recall_before = evaluator.evaluate_context_recall(actual_ctxs, expected_ans)
    prec_before = evaluator.evaluate_context_precision(actual_ctxs, expected_ans)
    
    # Rerank
    reranked_ctxs = rerank_by_overlap(actual_ctxs, q)
    
    # After
    recall_after = evaluator.evaluate_context_recall(reranked_ctxs, expected_ans)
    prec_after = evaluator.evaluate_context_precision(reranked_ctxs, expected_ans)
    
    print(f"| {cid} | {recall_before:.3f} | {recall_after:.3f} | {prec_before:.3f} | {prec_after:.3f} | {prec_after - prec_before:+.3f} |")

