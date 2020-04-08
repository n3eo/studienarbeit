from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import mysql.connector
from api_request import setup, concurrent_submain
import logging
import sys
from db_connection import DbConnection as DBC

logging.basicConfig(
    format="%(asctime)s %(levelname)s:%(name)s: %(message)s",
    level=logging.INFO,
    datefmt="%H:%M:%S", 
    filename="../jupyter/logs/api_requests_concurrent.log",
    filemode='a',
)


dbc = DBC()
results = dbc.get_pending()
del dbc

def inf_dbc():
    while True:
        yield DBC()


with ProcessPoolExecutor(max_workers=2) as executor:
    for _ in executor.map(concurrent_submain, results, inf_dbc()):
        pass