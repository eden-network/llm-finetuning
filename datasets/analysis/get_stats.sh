## Make executable with `chmod +x get_stats.sh` then run with `./get_stats.sh`
## Use --write_to_bq flag to write to bigquery

python get_hf_dataset_token_limit_stats.py \
    --hf_dataset AlfredPro/smart-contracts-instructions \
    --old_input_column instruction \
    --old_output_column source_code \
    --tokenizer bigcode/starcoder2-3b \
    --prompt_template instruction_task_solution