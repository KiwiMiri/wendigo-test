import os
import pickle
import pandas as pd

# 분석 대상 디렉토리 (경로는 상황에 맞게 수정 가능)
STEP_DIR = "results/steps/Wendigo-DVGA-Random-Greedy-Large-Step"
OUTPUT_CSV = "results/wendigo_summary.csv"

# 결과 누적 리스트
step_records = []

# .p 파일 순회하며 파싱
for filename in sorted(os.listdir(STEP_DIR)):
    if filename.endswith(".p"):
        filepath = os.path.join(STEP_DIR, filename)
        with open(filepath, "rb") as f:
            try:
                data = pickle.load(f)
                step_records.append({
                    "step_file": filename,
                    "query": data.get("query", "").replace("\n", " ").strip(),
                    "response_time": data.get("response_time", None),
                    "rejected": data.get("rejected", None),
                    "terminated": data.get("terminated", None),
                    "truncated": data.get("truncated", None),
                })
            except Exception as e:
                step_records.append({
                    "step_file": filename,
                    "query": None,
                    "response_time": None,
                    "rejected": None,
                    "terminated": None,
                    "truncated": None,
                    "error": str(e)
                })

# DataFrame으로 변환 후 저장
df = pd.DataFrame(step_records)
os.makedirs(os.path.dirname(OUTPUT_CSV), exist_ok=True)
df.to_csv(OUTPUT_CSV, index=False)

print(f"✅ CSV 저장 완료: {OUTPUT_CSV}")
