import unittest
from hf.tokenization import get_stats
from statistics import mean
from tabulate import tabulate

class TestIntegrationHfDataset(unittest.TestCase):

    def test_get_stats(self):
        dataset = "smart-contracts-instructions-mod-short.jsonl"
        prompt_template = "instruction_task_solution"
        tokenizer = "bigcode/starcoder2-3b"        

        stats = get_stats(dataset_jsonl=dataset, prompt_template=prompt_template, tokenizer=tokenizer)        
        
        input_lengths = [item["input_tokens_length"] for item in stats]
        output_lengths = [item["output_tokens_length"] for item in stats]
        
        average_input_length = mean(input_lengths)
        min_input_length = min(input_lengths)
        max_input_length = max(input_lengths)

        average_output_length = mean(output_lengths)
        min_output_length = min(output_lengths)
        max_output_length = max(output_lengths)
        
        row = {
            "tokenizer": tokenizer,
            "dataset": dataset,
            "prompt_template": prompt_template,
            "avg_input_length": average_input_length,
            "min_input_length": min_input_length,
            "max_input_length": max_input_length,
            "avg_output_length": average_output_length,
            "min_output_length": min_output_length,
            "max_output_length": max_output_length
        }
        
        headers = ["tokenizer", "dataset", "prompt_template", "avg_input_length", "min_input_length", "max_input_length", "avg_output_length", "min_output_length", "max_output_length"]
        rows = [list(row.values())]
        
        print(tabulate(rows, headers, tablefmt="grid"))

if __name__ == '__main__':
    unittest.main()