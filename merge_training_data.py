import os
import json
import re

def merge_training_blocks(input_folder="training data", output_file="merged_harshil_data.jsonl"):
    merged_data = []

    for filename in os.listdir(input_folder):
        if filename.endswith(".jsonl"):
            filepath = os.path.join(input_folder, filename)

            with open(filepath, "r", encoding="utf-8") as f:
                raw = f.read().strip()
                raw = re.sub(r"\n\s*\n", "\n", raw)
                blocks = re.split(r"}\s*{", raw)

                for i, block in enumerate(blocks):
                    block = block.strip()

                    if not block.startswith("{"):
                        block = "{" + block
                    if not block.endswith("}"):
                        block = block + "}"

                    try:
                        parsed = json.loads(block)
                        merged_data.append(parsed)
                    except json.JSONDecodeError as e:
                        print(f"Invalid JSON block in {filename}: {e}")
                        

    with open(output_file, "w", encoding="utf-8") as fout:
        for record in merged_data:
            fout.write(json.dumps(record, ensure_ascii=False) + "\n")

    print(f"Merged {len(merged_data)} blocks into {output_file}")

merge_training_blocks()
