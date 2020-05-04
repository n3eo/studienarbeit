from concurrent.futures import ProcessPoolExecutor
from utils.api_request import process_json
import logging
from utils.db_connection import DbConnection as DBC

if __name__ == "__main__":
    logging.basicConfig(
        format="%(asctime)s %(levelname)s:%(name)s: %(message)s",
        level=logging.INFO,
        datefmt="%H:%M:%S",
        filename="/app/logs/ingestion.log",
        filemode='a',
    )

    workers = 64
    dbc = DBC()
    results = dbc.get_jsons()
    dbc.close()

    with ProcessPoolExecutor(max_workers=workers) as executor:
        for _ in executor.map(process_json, results):
            pass    