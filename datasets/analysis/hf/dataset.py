import json, os, logging
from hf.config import parent_dir
from datasets import load_dataset, load_from_disk

def get_dataset_format(name: str) -> dict:
    logging.info(f"getting dataset format for {name}...")
    dataset_formats_path = os.path.join(parent_dir, "../data/dataset_formats.json")
    with open(dataset_formats_path, 'r') as dataset_formats:
        formats = json.load(dataset_formats)
    if name not in formats:
        raise ValueError(f"format for dataset '{name}' not found in {dataset_formats_path}.")
    return formats[name]


def validate_column_mappings(column_mappings: dict, dataset_format: dict) -> bool:
    logging.info("validating column mappings for dataset format...")
    for key in column_mappings.keys():
        if key not in dataset_format.keys():
            logging.error(f"column '{key}' not found in dataset format.")
            raise ValueError(f"column '{key}' not found in dataset format.")
    return True

def pull(name: str) -> str:
    logging.info(f"pulling dataset {name}...")
    local_name = name.split("/")[1]
    local_path = os.path.join(parent_dir, f"../data/{local_name}")
    if os.path.exists(local_path):
        logging.info(f"dataset already exists at {local_path}. skipping...")
        return local_name

    dataset = load_dataset(name)    
    dataset.save_to_disk(local_path)
    logging.info(f"dataset local name: {local_name}")
    return local_name

def transform(name: str, column_mappings: dict, dataset_format: str) -> str:
    logging.info(f"transforming dataset {name} using dataset format {dataset_format}...")
    
    dataset_format = get_dataset_format(dataset_format)    
    validate_column_mappings(column_mappings, dataset_format)

    transformed_name = f"{name}-mod"
    transformed_filepath = os.path.join(parent_dir, f"../data/{transformed_name}")
    if os.path.exists(transformed_filepath):
        logging.info(f"dataset {name} already transformed. can be found here at {transformed_filepath}. skipping...")
        return transformed_name
    
    dataset_path = os.path.join(parent_dir, f"../data/{name}")
    dataset = load_from_disk(dataset_path)    

    def rename_columns(row):
        for new_col, old_col in column_mappings.items():
            if old_col is not None and old_col in row:
                row[dataset_format[new_col]] = row.pop(old_col)
        return row

    renamed_dataset = dataset.map(rename_columns)    
    renamed_dataset.save_to_disk(transformed_filepath)
    logging.info(f"dataset transformed name: {transformed_name}")
    return transformed_name

def to_jsonl(name: str, split: str = "train") -> str:
    logging.info(f"converting dataset {name} to jsonl...")
    jsonl_filename = f"{name}.jsonl"
    output_jsonl_filepath = f"{parent_dir}/../data/{jsonl_filename}"
    if os.path.exists(output_jsonl_filepath):
        logging.info(f"dataset {name} already converted to jsonl. can be found at {output_jsonl_filepath}. skipping...")
        return jsonl_filename

    local_path = os.path.join(parent_dir, f"../data/{name}")
    dataset = load_from_disk(local_path)    

    with open(output_jsonl_filepath, 'w') as jsonl_writer:
        for example in dataset[split]:
            json_line = json.dumps(example)
            jsonl_writer.write(json_line + '\n')

    logging.info(f"dataset converted to jsonl. jsonl file name: {jsonl_filename}")
    return jsonl_filename

def process(name: str, column_mappings: dict, dataset_format: str) -> str:
    logging.info(f"processing dataset {name}...")
    local_name = pull(name)
    transformed_name = transform(local_name, column_mappings, dataset_format)
    jsonl_name = to_jsonl(transformed_name)
    return jsonl_name