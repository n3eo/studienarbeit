import mysql.connector
import requests
import json

def main():
    cnx = mysql.connector.connect(
        host='db', port='3306', database='nico_studienarbeit', user='studienarbeit', password='dbstuar2020')

    cursor = cnx.cursor()

    cursor.execute("DROP TABLE IF EXISTS `api_request`;")
    cursor.execute("CREATE TABLE `api_request` (`ID` int(11) NOT NULL,`Status` varchar(20) COLLATE utf8_bin NOT NULL DEFAULT 'Pending', `JSON` longblob NULL, `HASH` VARCHAR(64) NULL DEFAULT NULL) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;")
    cursor.execute("ALTER TABLE `api_request` ADD PRIMARY KEY (`ID`);")
    cursor.execute("ALTER TABLE `api_request` ADD UNIQUE(`HASH`); ")
    cnx.commit()

    total = json.loads(requests.get(
        f"https://api.lib.harvard.edu/v2/items.json?q=*&limit=250&sort=recordIdentifier").text).get("pagination").get("numFound")

    for i in range((total // 250) + 2):
        cursor.execute(f"INSERT IGNORE INTO api_request(ID) VALUES({i});")
    cnx.commit()

if __name__ == "__main__":
    main()