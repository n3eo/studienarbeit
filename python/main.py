from concurrent.futures import ProcessPoolExecutor
from utils.api_request import process_json

if __name__ == "__main__":
    logging.basicConfig(
        format="%(asctime)s %(levelname)s:%(name)s: %(message)s",
        level=logging.INFO,
        datefmt="%H:%M:%S",
        filename="../jupyter/logs/concurrent_db_ingestions.log",
        filemode='a',
    )

    workers = 128
    dbc = DBC()
    results = dbc.get_jsons()
    dbc.close()

    with ProcessPoolExecutor(max_workers=workers) as executor:
        for _ in executor.map(process_json, results):
            pass