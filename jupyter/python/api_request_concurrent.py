from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import mysql.connector
from api_request import concurrent_submain
import logging
import sys
from db_connection import DbConnection as DBC

logging.basicConfig(
    format="%(asctime)s %(levelname)s:%(name)s: %(message)s",
    level=logging.INFO,
    datefmt="%H:%M:%S", 
    filename="/app/jupyter/logs/api_requests_concurrent.log",
    filemode='a',
)

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
        for _ in executor.map(concurrent_submain, results):
            pass