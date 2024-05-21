select  io.tokenizer,
        dataset,
        dtl.limit as token_limit,
        count(*) as num_entries,
        avg(input_tokens_length) as average_input_tokens,
        avg(output_tokens_length) as average_output_tokens,
        countif(input_tokens_length > dtl.limit) as num_inputs_gt_token_limit,
        countif(output_tokens_length > dtl.limit) as num_outputs_gt_token_limit,
        dtl.associated_model_notes
from `${project_id}.${dataset_id}.${view_id}` io
join `${project_id}.${dataset_id}.tokenizer_token_limit` as dtl on io.tokenizer = dtl.tokenizer
group by io.tokenizer, dataset, dtl.limit, dtl.associated_model_notes