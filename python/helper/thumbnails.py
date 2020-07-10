from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import mysql.connector
import requests
import logging
from base64 import a85encode


def get_image_urls():
    cnx = mysql.connector.connect(
        host='db', port='3306', database='BuchDB', user='studienarbeit', password='dbstuar2020')

    cursor = cnx.cursor(buffered=True)

    cursor.execute(
        'SELECT BildId, Bild FROM Bild WHERE Bild IS NOT NULL;')
    
    results = cursor.fetchall()

    cnx.close()

    return results

def dl_image(t):
    iD, url = t
    cnx = mysql.connector.connect(
        host='db', port='3306', database='BuchDB', user='studienarbeit', password='dbstuar2020')

    cursor = cnx.cursor(buffered=True)

    try:
        r = requests.get(url)
        image_a85 = a85encode(r.content)
    except Exception as e:
        logging.error(e)
        image_a85 = None

    cursor.execute("UPDATE Bild SET Bild=%s WHERE BildId=%s",(image_a85, iD))
    cnx.commit()

    cnx.close()

if __name__ == "__main__":
    logging.basicConfig(
        format="%(asctime)s %(levelname)s:%(name)s: %(message)s",
        level=logging.INFO,
        datefmt="%H:%M:%S",
        filename="/app/logs/crawling.log",
        filemode='a',
    )

    workers = 16

    results = get_image_urls()

    with ProcessPoolExecutor(max_workers=workers) as executor:
        for _ in executor.map(dl_image, results):
            pass