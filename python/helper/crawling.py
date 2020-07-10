from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import mysql.connector
import requests
import logging
import sys
import hashlib
import time, random

def get_pending(typ="text"):
    cnx = mysql.connector.connect(
        host='db', port='3306', database='BuchDB', user='studienarbeit', password='dbstuar2020')

    cursor = cnx.cursor(buffered=True)

    cursor.execute(
        f'SELECT ID FROM api_request_{typ} WHERE Status="Pending"')  # OR JSON IS NULL
    results = cursor.fetchall()
    return [i[0] for i in results]

def set_status(cnx, cursor, id, status, typ):
    cursor.execute(
        f'UPDATE api_request_{typ} SET Status="{status}" WHERE ID={id}')
    cnx.commit()

def set_prossesing(cnx, cursor, id, typ="text"):
    set_status(cnx, cursor, id, "Processing", typ)

def set_done(cnx, cursor, id, typ="text"):
    set_status(cnx, cursor, id, "Done", typ)

def set_json(cnx, cursor, id, typ="text"):
    set_status(cnx, cursor, id, "JSON", typ)

def set_pending(cnx, cursor, id, typ="text"):
    set_status(cnx, cursor, id, "Pending", typ)

def insert_json(cnx, cursor, id, json, typ):
    cursor.execute(
        f"UPDATE api_request_{typ} SET JSON=%s WHERE ID=%s", (json, id))
    cnx.commit()

def insert_hash(cnx, cursor, id, hash, typ):
    cursor.execute(
        f"UPDATE api_request_{typ} SET HASH=%s WHERE ID=%s", (hash, id))
    cnx.commit()

def crawlJSON(start_value):
    time.sleep(random.random()*2)
    t_start = time.time()

    logging.info(f"Crawling {start_value}")
    # set_prossesing(cnx, cursor, start_value, TYP)
    try:
        r = requests.get(
            f"https://api.lib.harvard.edu/v2/items.json?q=*&limit=250&start={start_value - (0 if start_value <= 100000 else 100000)}&sort.{'asc' if start_value <= 100000 else 'desc'}=recordIdentifier&resourceType={TYP}".replace("_"," "), timeout=30 if workers < 30 else workers)
    except Exception as e:
        logging.error(f"Crawling {start_value} failed with the error: {e}", exc_info=False)
        return
    
    if len(r.content) < 500:
        logging.error(f"Crawling {start_value} returned invalid response (too short)")
        return
    
    cnx = mysql.connector.connect(
        host='db', port='3306', database='BuchDB', user='studienarbeit', password='dbstuar2020')

    cursor = cnx.cursor(buffered=True)

    insert_json(cnx, cursor, start_value, r.content, TYP)
    try:
        insert_hash(cnx, cursor, start_value, hashlib.blake2s(r.content).hexdigest(), TYP)
    except Exception as e:
        logging.warning(f"Crawling {start_value} resulted in an duplicate error: {e}")
    set_json(cnx, cursor, start_value, TYP)
    
    cnx.close()
    
    logging.info(f"Crawling {start_value} took {time.time()-t_start}s")

logging.basicConfig(
    format="%(asctime)s %(levelname)s:%(name)s: %(message)s",
    level=logging.INFO,
    datefmt="%H:%M:%S",
    filename="/app/logs/crawling.log",
    filemode='a',
)

if __name__ == "__main__":
    workers = 16

    TYP = "moving_image"
    results = get_pending(TYP)
    if not results:
        TYP = "still_image"
        results = get_pending(TYP)
    if not results:
        TYP = "text"
        results = get_pending(TYP)
    
    # No results
    if not results:
        logging.info("Nothing to crawl. Crawling done.")
        exit(1)
    
    results = results[:384]

    with ProcessPoolExecutor(max_workers=workers) as executor:
        for _ in executor.map(crawlJSON, results):
            pass