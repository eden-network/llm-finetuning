## Make executable with `chmod +x get_stats.sh` then run with `./get_stats.sh`
## Use --write_to_bq flag to write to bigquery
COLUMN_MAPPINGS='{"instruction": "instruction", "input": None, "output": "source_code"}'

python get_hf_dataset_token_limit_stats.py \
    --hf_dataset AlfredPro/smart-contracts-instructions \
    --tokenizer bigcode/starcoder2-3b \
    --target_dataset_format alpaca \
    --column_mappings "$COLUMN_MAPPINGS" \
    --prompt_template alpaca