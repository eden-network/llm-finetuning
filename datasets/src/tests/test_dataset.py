import unittest, os
from hf.config import parent_dir
from hf.dataset import pull, transform
from datasets import load_from_disk

class TestIntegrationHfDataset(unittest.TestCase):

    def test_pull(self):
        pull(name="bigcode/the-stack-v2-dedup", local_name="the-stack-v2-dedup/solidity", data_files="data/Solidity/*.parquet")

    def test_transform(self):
        transform(local_name="the-stack-v2-dedup/solidity", old_input_column="code", old_output_column="code")

    def test_look_into_dataset(self):
        dataset_path = os.path.join(parent_dir, f"../data/the-stack-v2-dedup/solidity")
        dataset = load_from_disk(dataset_path)
        def rename_columns(row):        
            print(f"https://github.com/{row['repo_name']}{row['path']}")
        dataset.map(rename_columns)

if __name__ == '__main__':
    unittest.main()