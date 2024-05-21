import json, os
from hf.config import parent_dir
from transformers import AutoTokenizer

def get_stats(checkpoint: str = "bigcode/starcoder2-3b", dataset: str = "smart-contracts-instructions-mod", prompt_template: str = "instruction_task_solution"):
    tokenizer = AutoTokenizer.from_pretrained(
            checkpoint,
            cache_dir=None,
            padding_side="right",
            use_fast=False,
            tokenizer_type=None,
            trust_remote_code=False,
            use_auth_token=False,
        )

    inputs = []
    dataset_path = os.path.join(parent_dir, f"../data/{dataset}.jsonl")
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
            "tokenizer": checkpoint,
            "dataset": dataset,
            "prompt": prompt,
            "output": input["output"],
            "input_tokens_length" : len(input_tokens),
            "output_tokens_length" : len(output_tokens)
        })
    
    return stats

if __name__ == "__main__":
    stats = get_stats()
    print(stats)    