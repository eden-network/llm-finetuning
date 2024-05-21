from dotenv import load_dotenv
load_dotenv()

import asyncio
from hf.tokenization import get_stats
from hf.dataset import initialize
from bigquery.writer import async_write

async def async_execute():
    initialize(name="AlfredPros/smart-contracts-instructions", local_name="smart-contracts-instructions", old_input_column="instruction", old_output_column="source_code")
    stats = get_stats(dataset="smart-contracts-instructions-mod")    
    await async_write(stats)

if __name__ == '__main__':
    asyncio.run(async_execute())    
