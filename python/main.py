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

    

    dbc = DBC()

    TYP = "moving_image"
    results = dbc.get_jsons(TYP)
    if not results:
        TYP = "still_image"
        results = dbc.get_jsons(TYP)
    if not results:
        TYP = "text"
        results = dbc.get_jsons(TYP)
    
    # No results
    if not results:
        logging.info("Nothing to process. Processing done.")
        exit(1)
    
    results = results[:4096]
    dbc.close()

    workers = 2

    # with ProcessPoolExecutor(max_workers=workers) as executor:
    #     for _ in executor.map(process_json, results):
    #         pass
    for elem in results:
        process_json(elem)