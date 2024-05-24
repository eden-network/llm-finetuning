import json, os, logging
from hf.config import parent_dir
from transformers import AutoTokenizer

access_token = os.getenv('HUGGINGFACE_TOKEN')
os.environ["TOKENIZERS_PARALLELISM"] = "false"

def get_stats(dataset_jsonl, prompt_template, tokenizer):
    logging.info(f"getting stats for dataset {dataset_jsonl} with tokenizer {tokenizer}...")
    tokenizer = AutoTokenizer.from_pretrained(
            tokenizer,
            cache_dir=None,
            padding_side="right",
            use_fast=False,
            tokenizer_type=None,
            trust_remote_code=False,
            use_auth_token=access_token
        )

    inputs = []
    dataset_path = os.path.join(parent_dir, f"../data/{dataset_jsonl}")
    with open(dataset_path, 'r') as file_inputs:
        for line in file_inputs:
            inputs.append(json.loads(line))

    prompts_path = os.path.join(parent_dir, f"../data/prompts.json")
    with open(prompts_path, 'r') as file_prompts:
        prompts = json.load(file_prompts)

    stats = []           
    for input in inputs:    
        prompt = prompts[prompt_template].replace("{input}", input["input"]).replace("\\n", "\n")
        input_tokens = tokenizer.tokenize(prompt)            
        output_tokens = tokenizer.tokenize(input["output"])            
        # encoded_inputs = tokenizer(prompt, return_tensors="pt", truncation=True)
        # input_ids = encoded_inputs['input_ids'].to("cuda:0")
        # encoded_outputs = tokenizer(input["output"], return_tensors="pt", truncation=True)
        # output_ids = encoded_outputs['input_ids'].to("cuda:0")
        
        stats.append({
            "tokenizer": tokenizer.name_or_path,
            "dataset": dataset_jsonl,
            "prompt": prompt,
            "output": input["output"],
            "input_tokens_length" : len(input_tokens),
            "output_tokens_length" : len(output_tokens)
        })
    
    return stats