import logging, asyncio, io, json
from google.cloud import bigquery
from os import getenv

project_id = getenv("PROJECT_ID")
dataset_id = getenv("DATASET_ID")
table_id = getenv("TABLE_ID")

async def async_write(json_data):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(
        None,
        write,
        json_data
    )

def write(json_data) -> bool:
    logging.info(f"loading data to bigquery table: {project_id}.{dataset_id}.{table_id}")
    try:
        client = bigquery.Client(project=project_id)
        table_ref = client.dataset(dataset_id).table(table_id)
        job_config = bigquery.LoadJobConfig()
        job_config.source_format = bigquery.SourceFormat.NEWLINE_DELIMITED_JSON
        jsonl_data = '\n'.join(json.dumps(item) for item in json_data)        
                
        with io.StringIO(jsonl_data) as json_data_io:
            job = client.load_table_from_file(
                json_data_io,
                table_ref,
                location='US',
                job_config=job_config,
            )
            
        job.result()
        logging.info(f"data upload complete")

    except Exception as e:
        logging.error(f"unexpected error occurred when loading data to {project_id}.{dataset_id}.{table_id}: {e}")
        return False    

    return True