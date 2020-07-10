import mysql.connector
from datetime import date
import logging
import random, base64, hashlib
random.seed(0)

def timeit(method):
    import time
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()        
        if 'log_time' in kw:
            name = kw.get('log_name', method.__name__.upper())
            kw['log_time'][name] = int((te - ts) * 1000)
        else:
            logging.info('%r  %2.2f ms' % \
                (method.__name__, (te - ts) * 1000))
        return result
    
    return timed
log_trace = False

class DbConnection():
    __instance = None
    __cursor = None

    INSERT_SORTE = "INSERT INTO Sorte(Name,Beschreibung) VALUES(%s,%s)"
    SELECT_SORTE = "SELECT SorteId FROM Sorte WHERE Name=%s -- AND (Beschreibung=%s OR Beschreibung IS NULL);"

    INSERT_VERLAG = "INSERT INTO Verlag(Kurzname, Name, Postleitzahl, Strasse, Internetadresse, Beschreibung) VALUES(%s,%s,%s,%s,%s,%s)"
    SELECT_VERLAG = "SELECT VerlagId FROM Verlag WHERE (Kurzname=%s OR Kurzname IS NULL) AND Name=%s AND (Postleitzahl=%s OR Postleitzahl IS NULL) AND (Strasse=%s OR Strasse IS NULL) AND (Internetadresse=%s OR Internetadresse IS NULL) AND (Beschreibung=%s OR Beschreibung IS NULL);"

    INSERT_BUCH = "INSERT IGNORE INTO Buch(ISBN,Titel,Untertitel,VerlagId,Erscheinungsjahr,SorteId,Kurzbeschreibung,Preis,Auflage,Sprache) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
    
    INSERT_AUTORBUCHZUORD = "INSERT INTO AutorBuchZuord(AutorId,ISBN) VALUES(%s,%s);"
    SELECT_AUTORBUCHZUORD = "SELECT AutorBuchZuordId FROM AutorBuchZuord WHERE AutorId=%s AND ISBN=%s;"

    INSERT_MEDIUMWORTZUORD = "INSERT INTO MediumWortZuord(MediumId,Wort) VALUES(%s,%s)"
    SELECT_MEDIUMWORTZUORD = "SELECT MediumWortId FROM MediumWortZuord WHERE MediumId=%s AND Wort=%s;"

    INSERT_SCHLAGWORT = "INSERT IGNORE INTO Schlagwort(Wort,Beschreibung) VALUES(%s,%s)"

    INSERT_PERSON = "INSERT INTO Person(Vorname,Name,Email,Geburtsdatum) VALUES(%s,%s,%s,%s);"
    SELECT_PERSON = "SELECT PersonId FROM Person WHERE Vorname=%s AND Name=%s AND (Email=%s OR Email IS NULL) AND (Geburtsdatum=%s OR Geburtsdatum IS NULL);"

    INSERT_SPRECHER = "INSERT INTO Sprecher(PersonId,Beschreibung) VALUES(%s,%s)"
    SELECT_SPRECHER = "SELECT SprecherId FROM Sprecher WHERE PersonId=%s AND (Beschreibung=%s OR Beschreibung IS NULL);"

    INSERT_HOERBUCH = "INSERT IGNORE INTO Hoerbuch(ISBN,BuchISBN,SprecherId,VerlagId) VALUES(%s,%s,%s,%s);"

    INSERT_EBOOK = "INSERT IGNORE INTO Ebook(ISBN,BuchISBN,Dateiformat) VALUES(%s,%s,%s)"

    INSERT_AUSLEIHER = "INSERT INTO Ausleiher(PersonId,Strasse,Postleitzahl,Ort,Telefonnummer) VALUES(%s,%s,%s,%s,%s)"
    SELECT_AUSLEIHER = "SELECT AusleiherId FROM Ausleiher WHERE PersonId=%s AND Strasse=%s AND Postleitzahl=%s AND Ort=%s AND (Telefonnummer=%s OR Telefonnummer IS NULL);"

    INSERT_AUTOR = "INSERT INTO Autor(PersonId,Beschreibung) VALUES(%s,%s)"
    SELECT_AUTOR = "SELECT AutorId FROM Autor WHERE PersonId=%s AND (Beschreibung=%s OR Beschreibung IS NULL);"

    INSERT_MALER = "INSERT INTO Maler(PersonId,Beschreibung) VALUES(%s,%s)"
    SELECT_MALER = "SELECT MalerId FROM Maler WHERE PersonId=%s AND (Beschreibung=%s OR Beschreibung IS NULL);"

    INSERT_NICHTTEXTMEDIUM = "INSERT INTO NichtTextMedium(Titel,Untertitel,Erscheinungsjahr,Kurzbeschreibung,SorteId,Typ) VALUES(%s,%s,%s,%s,%s,%s)"
    SELECT_NICHTTEXTMEDIUM = "SELECT NichtTextMediumId FROM NichtTextMedium WHERE Titel=%s AND (Untertitel=%s OR Untertitel IS NULL) AND (Erscheinungsjahr=%s OR Erscheinungsjahr IS NULL) AND (Kurzbeschreibung=%s OR Kurzbeschreibung IS NULL) AND SorteId=%s AND Typ=%s;"

    INSERT_BILD = "INSERT IGNORE INTO Bild(NichtTextMediumId,Bild,MalerId) VALUES(%s,%s,%s)"
    SELECT_BILD = "SELECT BildId FROM Bild WHERE NichtTextMediumId=%s AND (Bild=%s OR BILD IS NULL) AND MalerId=%s;"

    INSERT_VIDEO = "INSERT IGNORE INTO Video(NichtTextMediumId,Sprache) VALUES(%s,%s)"
    SELECT_VIDEO = "SELECT VideoId FROM Video WHERE NichtTextMediumId=%s AND (Sprache=%s OR Sprache IS NULL);"

    INSERT_AUSLEIHE = "INSERT INTO Ausleihe(AusleiherId,MediumId) VALUES(%s,%s)"

    # def __new__(cls):
    #     if DbConnection.__instance is None:
    #         DbConnection.__instance = object.__new__(cls)
    #     return DbConnection.__instance
    
    def __init__(self):
        self.__cnx = mysql.connector.connect(
            host='db', port='3306', database='BuchDB', user='studienarbeit', password='dbstuar2020')

        self.__cursor = self.__cnx.cursor(buffered=True)

    def __del__(self):
        self.__cnx.close()
    def close(self):
        self.__del__()
    
    def __set_status(self, id, status, typ):
        self.__cursor.execute(
            f'UPDATE api_request_{typ} SET Status="{status}" WHERE ID={id}')
        self.__cnx.commit()

    def set_done(self, id, typ):
        self.__set_status(id, "Done", typ)
      
    def get_jsons(self, typ):
        self.__cursor.execute(
            f'SELECT ID FROM api_request_{typ} WHERE Status="JSON";')  # OR JSON IS NULL
        results = self.__cursor.fetchall()
        return [(i[0], typ) for i in results]

    def get_json(self, id, typ):
        self.__cursor.execute(
            f'SELECT JSON FROM api_request_{typ} WHERE ID={id};')  # OR JSON IS NULL
        i = self.__cursor.fetchone()
        return i[0]

    def del_id(self, id, typ):
        self.__cursor.execute(
            f"DELETE FROM api_request_{typ} WHERE ID={id};")
        self.__cnx.commit()
    
    # @timeit
    def __insert_db(self, INSERT, values, SELECT=None):
        val = list(values.values())

        first_result = None
        if SELECT:
            self.__cursor.execute(SELECT, val)
            first_result = self.__cursor.fetchone()
                
        if not first_result:
            self.__cursor.execute(INSERT, val)
            self.__cnx.commit()
            if INSERT.find("IGNORE") == -1:
                return self.__cursor.lastrowid
            else:
                return val[0]

        return first_result[0]

    # @timeit
    def insert_book(self, val_schlagworte, val_verlag, val_buch, val_person, val_autor, val_sorte):
        # print("--- Inserting Sorte")
        sorte_id = self.__insert_db(
            self.INSERT_SORTE, val_sorte, self.SELECT_SORTE)
        val_buch["SorteId"] = sorte_id

        # print("--- Inserting Verlag")
        verlag_id = self.__insert_db(self.INSERT_VERLAG, val_verlag, self.SELECT_VERLAG)
        val_buch["VerlagId"] = verlag_id
        
        # print("--- Inserting Buch")
        buch_id = self.__insert_db(self.INSERT_BUCH, val_buch)

        # print("--- Inserting Schlagworte")
        for schlagwort in val_schlagworte:
            # print("--- --- Inserting Schlagwort")
            self.__insert_db(self.INSERT_SCHLAGWORT, schlagwort)

            # print("--- --- Inserting MediumWortZuord")
            val_mediumwortzuord = {
                "MediumId": buch_id,
                "Wort": schlagwort["Wort"]
            }
            self.__insert_db(self.INSERT_MEDIUMWORTZUORD, val_mediumwortzuord, self.SELECT_MEDIUMWORTZUORD)

        # print("--- Inserting Person")
        person_id = self.__insert_db(self.INSERT_PERSON, val_person, self.SELECT_PERSON)
        val_autor["PersonId"] = person_id
        
        # print("--- Inserting Autor")
        autor_id = self.__insert_db(self.INSERT_AUTOR, val_autor, self.SELECT_AUTOR)

        # print("--- Inserting AutorBuchZuord")
        val_autorbuchzuord = {
            "AutorId" : autor_id,
            "IBSN" : val_buch["ISBN"]
        }
        self.__insert_db(self.INSERT_AUTORBUCHZUORD, val_autorbuchzuord, self.SELECT_AUTORBUCHZUORD)
            # print("--- Done")
    
    # ### Hörbuch
    # self.INSERT_SORTE, self.INSERT_VERLAG, self.INSERT_BUCH, self.INSERT_SPRECHER

    # @timeit
    def insert_hoerbuch(self, val_person, val_sprecher, val_verlag, val_hoerbuch):
        # print("--- Inserting Person")
        person_id = self.__insert_db(self.INSERT_PERSON, val_person, self.SELECT_PERSON)
        val_sprecher["PersonId"] = person_id

        # print("--- Inserting Sprecher")
        sprecher_id = self.__insert_db(self.INSERT_SPRECHER, val_sprecher, self.SELECT_SPRECHER)
        val_hoerbuch["SprecherId"] = sprecher_id

        # print("--- Inserting Verlag")
        verlag_id = self.__insert_db(self.INSERT_VERLAG, val_verlag, self.SELECT_VERLAG)
        val_hoerbuch["VerlagId"] = verlag_id

        # print("--- Inserting Hoerbuch")
        self.__insert_db(self.INSERT_HOERBUCH, val_hoerbuch)

    # @timeit
    def insert_ebook(self, val_ebook):
        # print("--- Inserting Ebook")
        self.__insert_db(self.INSERT_EBOOK, val_ebook)

    def insert_ausleiher(self, val_person, val_ausleiher):
        # print("--- Inserting Person")
        person_id = self.__insert_db(self.INSERT_PERSON, val_person, self.SELECT_PERSON)
        val_ausleiher["PersonId"] = person_id

        # print("--- Inserting Ausleiher")
        self.__insert_db(self.INSERT_AUSLEIHER, val_ausleiher, self.SELECT_AUSLEIHER)

        # print("--- Done")

    # @timeit
    def insert_bild(self, val_sorte, val_person, val_maler, val_nichttextmedien, val_bild):
        # print("--- Inserting Sorte")
        sorte_id = self.__insert_db(self.INSERT_SORTE, val_sorte, self.SELECT_SORTE)
        val_nichttextmedien["SorteId"] = sorte_id

        # print("--- Inserting Person")
        person_id = self.__insert_db(self.INSERT_PERSON, val_person, self.SELECT_PERSON)
        val_maler["PersonId"] = person_id
        
        # print("--- Inserting Maler")
        maler_id = self.__insert_db(self.INSERT_MALER, val_maler, self.SELECT_MALER)
        val_bild["MalerId"] = maler_id

        # print("--- Inserting NichtTextMedium")
        val_nichttextmedien["Typ"] = "Bild"
        ntm_id = self.__insert_db(self.INSERT_NICHTTEXTMEDIUM, val_nichttextmedien, self.SELECT_NICHTTEXTMEDIUM)
        val_bild["NichtTextMediumId"] = ntm_id
        
        # print("--- Inserting Bild")
        self.__insert_db(self.INSERT_BILD, val_bild, self.SELECT_BILD)

        # print("--- Done")    

    # @timeit
    def insert_video(self, val_sorte, val_nichttextmedien, val_video):
        # print("--- Inserting Sorte")
        sorte_id = self.__insert_db(self.INSERT_SORTE, val_sorte, self.SELECT_SORTE)
        val_nichttextmedien["SorteId"] = sorte_id

        # print("--- Inserting NichtTextMedium")
        val_nichttextmedien["Typ"] = "Video"
        ntm_id = self.__insert_db(self.INSERT_NICHTTEXTMEDIUM, val_nichttextmedien, self.SELECT_NICHTTEXTMEDIUM)
        val_video["NichtTextMediumId"] = ntm_id

        # print("--- Inserting Video")
        self.__insert_db(self.INSERT_VIDEO, val_video, self.SELECT_VIDEO)

        # print("--- Done")     

    # @timeit
    def insert_ausleihe(self, val_person, val_ausleiher, ISBN):
        # print("--- Inserting Person")
        person_id = self.__insert_db(self.INSERT_PERSON, val_person, self.SELECT_PERSON)
        val_ausleiher["PersonId"] = person_id

        # print("--- Inserting Ausleiher")
        ausleiher_id = self.__insert_db(self.INSERT_AUSLEIHER, val_ausleiher, self.SELECT_AUSLEIHER)

        val_ausleihe = {
            "AusleiherId": ausleiher_id,
            "MediumId": ISBN
        }
        self.__insert_db(self.INSERT_AUSLEIHE, val_ausleihe)

if __name__ == "__main__":
    dbc = DbConnection()

    val_verlag = {
        "Kurzname" : "hi",
        "Name" : "hiverlag",
        "Postleitzahl" : "89078",
        "Strasse" : "Rubelstraße 33",
        "Internetadresse" : "hi@verlag.com",
        "Beschreibung" : "Für alles was high ist."
    }

    val_schlagwort = [
        {   "Wort": "Fun",
            "Beschreibung": "Fun ist eine tolle Kategorie."},
        {   "Wort": "Lust",
            "Beschreibung": "Lust im Herz"}
    ]

    val_buch = {
        "ISBN": "1234567890123",
        "Titel": "WOW",
        "Untertitel": "Ein WOW für dich!",
        "VerlagId": "",
        "Erscheinungsjahr": "2017",
        "SorteId": "",
        "Kurzbeschreibung": "Klassebuch",
        "Preis": "9.99",
        "Auflage": "1",
        "Sprache": "deutsch"
    }

    val_person = {
        "Vorname": "Guenter",
        "Name": "Pauli",
        "Email": "guenter@pauli.sucks",
        "Geburtsdatum": date(2000, 12, 2)
    }

    val_autor = {
        "PersonId": "",
        "Beschreibung": "Pauli aus Pauli"
    }

    val_sorte = {
        "Name": "Spassbuch",
        "Beschreibung": "Diese Bücher machen Spaß"
    }

    dbc.insert_book(val_schlagwort, val_verlag, val_buch, val_person, val_autor, val_sorte)


    # ## [TEST] Hoerbuch

    val_verlag = {
        "Kurzname" : "hi_hoerbuch",
        "Name" : "hiverlag für Hörbücher",
        "Postleitzahl" : "89078",
        "Strasse" : "Rubelstraße 33",
        "Internetadresse" : "hihoeren@verlag.com",
        "Beschreibung" : "Für alles was high ist."
    }

    val_person = {
        "Vorname": "Manfred",
        "Name": "Manni",
        "Email": "manni@manii.sk",
        "Geburtsdatum": date(1970, 4, 1)
    }

    val_sprecher = {
        "PersonId": "",
        "Beschreibung": "Spricht männliche charaktere"
    }

    val_hoerbuch = {
        "ISBN": "5678456456234",
        "BuchISBN": "1234567890123",
        "SprecherId": "",
        "VerlagId": ""
    }

    dbc.insert_hoerbuch(val_person, val_sprecher, val_verlag, val_hoerbuch)


    # ## [TEST] Ebook

    val_ebook = {
        "ISBN": "5678456498776",
        "BuchISBN": "1234567890123",
        "Dateiformat": "epub"
    }

    dbc.insert_ebook(val_ebook)


    # ## [TEST] Bild

    val_sorte = {
        "Name": "Spaßbild",
        "Beschreibung": "Dieses Bild erzeugt Spaß"
    }

    val_person = {
        "Vorname": "Mali",
        "Name": "Maler",
        "Email": "mal@er.sk",
        "Geburtsdatum": date(1980, 2, 28)
    }

    val_maler = {
        "PersonId": "",
        "Beschreibung": "Malt immer in Grau"
    }

    val_nichttextmedien = {
        "Titel": "WOW",
        "Untertitel": "Ein WOW für dich!",
        "Erscheinungsjahr": "2017",
        "Kurzbeschreibung": "Ein Bild von Klasse",
        "SorteId": "",
        "Typ": ""
    }

    with open("testimg_base64") as f:
        test_bild = f.read()
    val_bild = {
        "NichtTextMediumId": "",
        "Bild": test_bild,
        "MalerId": ""
    }

    dbc.insert_bild(val_sorte, val_person, val_maler,
                    val_nichttextmedien, val_bild)


    # ## [TEST] Video

    val_sorte = {
        "Name": "Spaßbild",
        "Beschreibung": "Dieses Bild erzeugt Spaß"
    }

    val_nichttextmedien = {
        "Titel": "18 Movie",
        "Untertitel": "18 klassiker",
        "Erscheinungsjahr": "1982",
        "Kurzbeschreibung": "Ein Video von Klasse",
        "SorteId": "",
        "Typ": ""
    }

    val_video = {
        "NichtTextMediumId": "",
        "Sprache": "deutsch"
    }

    dbc.insert_video(val_sorte, val_nichttextmedien, val_video)


    # ## [TEST] Ausleiher

    val_person = {
        "Vorname": "Max",
        "Name": "Mustermann",
        "Email": "max.mustermann@denken.de",
        "Geburtsdatum": date(1999, 6, 30)
    }

    val_ausleiher = {
        "PersonId": "",
        "Strasse": "Nostreet 24",
        "Postleitzahl": "56789",
        "Ort": "Entenhausen",
        "Telefonnummer" : "23458/856765567"
    }

    dbc.insert_ausleiher(val_person, val_ausleiher)


    # ## [TEST] Ausleihe

    val_person = {
        "Vorname": "Max",
        "Name": "Mustermann",
        "Email": "max.mustermann@denken.de",
        "Geburtsdatum": date(1999, 6, 30)
    }

    val_ausleiher = {
        "PersonId": "",
        "Strasse": "Nostreet 24",
        "Postleitzahl": "56789",
        "Ort": "Entenhausen",
        "Telefonnummer" : "23458/856765567"
    }

    ISBN = "1234567890123"

    dbc.insert_ausleihe(val_person, val_ausleiher, ISBN)