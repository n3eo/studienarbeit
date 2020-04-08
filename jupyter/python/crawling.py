from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import mysql.connector
import requests
import logging
import sys
from db_connection import DbConnection as DBC
import time, random

logging.basicConfig(
    format="%(asctime)s %(levelname)s:%(name)s: %(message)s",
    level=logging.INFO,
    datefmt="%H:%M:%S",
    filename="../jupyter/logs/crawling.log",
    filemode='a',
)

workers = 1024

dbc = DBC()
results = dbc.get_pending()
del dbc


def set_status(cnx, cursor, id, status):
    cursor.execute(
        f'UPDATE api_request SET Status="{status}" WHERE ID={id}')
    cnx.commit()

def set_prossesing(cnx, cursor, id):
    set_status(cnx, cursor, id, "Processing")

def set_done(cnx, cursor, id):
    set_status(cnx, cursor, id, "Done")

def set_json(cnx, cursor, id):
    set_status(cnx, cursor, id, "JSON")

def set_pending(cnx, cursor, id):
    set_status(cnx, cursor, id, "Pending")

def insert_json(cnx, cursor, id, json):
    cursor.execute(
        "UPDATE api_request SET JSON=%s WHERE ID=%s", (json, id))
    cnx.commit()

def crawlJSON(start_value):
    time.sleep(random.random()*((start_value % workers / workers) * 5))

    cnx = mysql.connector.connect(
        host='db', port='3306', database='nico_studienarbeit', user='studienarbeit', password='dbstuar2020')

    cursor = cnx.cursor(buffered=True)


    logging.info(f"Crawling {start_value}.")
    set_prossesing(cnx, cursor, start_value)
    try:
        r = requests.get(
            f"https://api.lib.harvard.edu/v2/items.json?q=*&limit=250&start={start_value*250}&sort=recordIdentifier", timeout=workers)
    except Exception as e:
        set_pending(cnx, cursor, start_value)
        logging.error(e, exc_info=False)
    else:
        insert_json(cnx, cursor, start_value, r.content)
        set_json(cnx, cursor, start_value)
    finally:
        cnx.close()

with ProcessPoolExecutor(max_workers=workers) as executor:
    for _ in executor.map(crawlJSON, results):
        pass
