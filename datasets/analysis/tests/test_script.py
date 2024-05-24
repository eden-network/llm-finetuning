import unittest, os
from get_hf_dataset_token_limit_stats import async_execute

class TestIntegrationHfDataset(unittest.IsolatedAsyncioTestCase):

    async def test_async_execute(self):
        await async_execute(hf_dataset="AlfredPro/smart-contracts-instructions", old_input_column="instruction", old_output_column="source_code", tokenizer="bigcode/starcoder2-3b", prompt_template="instruction_task_solution", write_to_bq=False)        

if __name__ == '__main__':
    unittest.main()