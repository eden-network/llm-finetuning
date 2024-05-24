import unittest, os
from hf.config import parent_dir
from hf.dataset import pull, transform, to_jsonl

class TestIntegrationHfDataset(unittest.TestCase):

    def test_pull(self):
        local_name = pull(name="AlfredPros/smart-contracts-instructions")
        local_filepath = f"{parent_dir}/../data/{local_name}"
        assert os.path.exists(local_filepath)

    def test_transform(self):        
        transformed_name = transform(name="smart-contracts-instructions", old_input_column="instruction", old_output_column="source_code")
        transformed_filepath = f"{parent_dir}/../data/{transformed_name}"
        assert os.path.exists(transformed_filepath)

    def test_to_jsonl(self):
        transformed_name = "smart-contracts-instructions-mod"        
        jsonl_name = to_jsonl(name=transformed_name)
        jsonl_filepath = f"{parent_dir}/../data/{jsonl_name}"
        assert os.path.exists(jsonl_filepath)

if __name__ == '__main__':
    unittest.main()