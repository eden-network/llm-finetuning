import asyncio, argparse, os, logging
from dotenv import load_dotenv
from statistics import mean
from tabulate import tabulate

load_dotenv()

logging_level = os.getenv("LOGGING_LEVEL", "INFO")

logging.basicConfig(level=logging.getLevelName(logging_level))

from hf.tokenization import get_stats
from hf.dataset import process
from bigquery.writer import async_write

async def async_execute(hf_dataset: str, old_input_column: str, old_output_column: str, tokenizer: str, prompt_template: str, write_to_bq: bool):
    logging.info(f"calculating token limit stats for hf_dataset: {hf_dataset}; with tokenizer: {tokenizer}; prompt_template: {prompt_template}; write_to_bq: {write_to_bq}")
    jsonl_filename = process(hf_dataset, old_input_column, old_output_column)
    stats = get_stats(jsonl_filename, prompt_template, tokenizer)
    print_stats(stats, tokenizer, jsonl_filename, prompt_template)
    if write_to_bq:
        await async_write(stats)

def print_stats(stats, tokenizer, dataset, prompt_template):
    logging.info("................................      stats        ..........................................\n")
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

def parse_arguments():
    parser = argparse.ArgumentParser(description='Process dataset and write stats to BigQuery.')
    parser.add_argument('--hf_dataset', type=str, required=True, help='Name of the dataset to pull from Hugging Face')
    parser.add_argument('--old_input_column', type=str, required=True, help='The name of the input column in the dataset you want to process. This will be changed to "input" in the new dataset.')
    parser.add_argument('--old_output_column', type=str, required=True, help='The name of the output column in the dataset you want to process. This will be changed to "output" in the new dataset.')
    parser.add_argument('--tokenizer', type=str, required=True, help='Tokenizer to use for calculating token limits. This should be a Hugging Face model checkpoint name.')    
    parser.add_argument('--prompt_template', type=str, help='The prompt template to use in get_stats. This needs to be available in the prompts.json file and note that {{input}} will be replaced with the input from the dataset')
    parser.add_argument('--write_to_bq', action='store_true', help='Write the stats to BigQuery? Default is False.')
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_arguments()
    asyncio.run(async_execute(args.hf_dataset, args.old_input_column, args.old_output_column, args.tokenizer, args.prompt_template, args.write_to_bq))