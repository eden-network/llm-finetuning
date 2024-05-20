import json, os
from config import parent_dir
from datasets import load_dataset, load_from_disk

def pull(name: str = "AlfredPros/smart-contracts-instructions", local_name: str = "smart-contracts-instructions"):
    dataset = load_dataset(name)
    save_path = os.path.join(parent_dir, f"../data/{local_name}")
    dataset.save_to_disk(save_path)

def transform(local_name: str = "smart-contracts-instructions", old_input_column: str = "instruction", old_output_column: str = "source_code"):
    dataset_path = os.path.join(parent_dir, f"../data/{local_name}")
    dataset = load_from_disk(dataset_path)

    def rename_columns(row):        
        row["input"] = row.pop(old_input_column)
        row["output"] = row.pop(old_output_column)
        return row

    renamed_dataset = dataset.map(rename_columns)
    renamed_dataset.save_to_disk(f"{parent_dir}/../data/{local_name}-mod")

def to_jsonl(local_name: str = "smart-contracts-instructions-mod"):
    local_path = os.path.join(parent_dir, f"../data/{local_name}")
    dataset = load_from_disk(local_path)
    output_jsonl_file = f"{parent_dir}/../data/{local_name}.jsonl"

    with open(output_jsonl_file, 'w') as jsonl_writer:
        for example in dataset['train']:
            json_line = json.dumps(example)
            jsonl_writer.write(json_line + '\n')

if __name__ == "__main__":
    pull()
    transform()
    to_jsonl()