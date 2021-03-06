import requests
import json
import logging
import mysql.connector
from faker import Faker
from base64 import a85encode
import re
import random, base64
import time, hashlib
from utils.db_connection import DbConnection as DBC

random.seed(0)

def timeit(method):
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

def flattenObj(obj):
    dictVal = {}
    
    if isinstance(obj,(dict, list)):
        
        # add indexes to list for iteration
        obj = dict(enumerate(obj)) if isinstance(obj, list) else obj
        
        # loop over entrys and store them in new dict
        for key, val in obj.items():
            if isinstance(val,(str, int)):
                dictVal[str(key)] = val
            
            # flatten again of the new value is a dict or list
            flattened = flattenObj(val)
            for key_new, val_new in flattened.items():
                dictVal[f"{key}_{key_new}"] = val_new
    
    return dictVal

def nestedDictGet(item, *keys):
    nextBaseItem = item
    for key in keys:        
        # test if type is list and get the index
        # beforeand check if the given value is a 
        # integer and a valid position in the dict
        if isinstance(nextBaseItem, list):
            if str(key).isdigit():
                if int(key) < len(nextBaseItem):
                    nextBaseItem = nextBaseItem[int(key)]
                    continue
            # return none if the index ist not valid for the
            # list and is a not existend as a key in the dict
            elif nextBaseItem.get(key) is None:
                return None
        
        # str and int are the information wanted, directly return it
        if isinstance(nextBaseItem,(str,int)):
            return nextBaseItem
        
        # test if the key exists onthe dict
        # otherwise returns null
        if not nextBaseItem.get(key):
            return None
        
        # as a default get the next nested object based on the key
        nextBaseItem = nextBaseItem.get(key)
        
    return nextBaseItem

def extractListSubject(subjects):
    if isinstance(subjects, str):
        return subjects

    topics = []
    if isinstance(subjects, list):
        for item in subjects:
            flattened = flattenObj(item)
            topics += extractListSubject(flattened)
    
    if isinstance(subjects, dict):
        for key, val in subjects.items():
            if not key.find("@authority") >= 0 and not isinstance(val, dict):
                topics += val if isinstance(val,list) and not isinstance(val, dict) else [val] # extractListSubject(val))
    
    # have every topic only one time by 
    # first cating to set and then back to list
    return list(set(topics))

def getInformationFromDifferentPaths(flattend, PATHS):
    information = None
    for path in PATHS:
        val = flattend.get(str(path))
        if val is not None:
            information = val
            break
    return information

def extractOneGenre(genre_flattend, GENRE_PATHS= ["0_#text", "#text"]):
    return getInformationFromDifferentPaths(genre_flattend, GENRE_PATHS)

def extractCreator(name_flattend, NAME_PATHS = ["0_namePart_0", "namePart_0", "0_namePart"]):
    return getInformationFromDifferentPaths(name_flattend, NAME_PATHS)

def extractPublisher(publisher_flattend, PUBLISHER_PATHS = ["publisher_0", "publisher_1"]):
    return getInformationFromDifferentPaths(publisher_flattend, PUBLISHER_PATHS)

def extractDate(date_flattend, DATE_PATHS = ["dateCreated", "dateCreated_0_#text", "dateIssued", "dateIssued_#text", "dateIssued_0_#text", "dateIssued_0"]):
    publish_date = getInformationFromDifferentPaths(date_flattend, DATE_PATHS)
    
    # remove chars because sometimes c (=circa) is included
    search = re.search(r'\d+', str(publish_date))
    return search[0] if publish_date and search else None

def extractEdition(edition_flattend, EDITION_PATHS = ["edition"]):
    edition = getInformationFromDifferentPaths(edition_flattend, EDITION_PATHS)
    
    # remove chars because sometimes c (=circa) is included
    search = re.search(r'\d+', str(edition))
    return search[0] if edition and search else None

def extractAbstract(abstract_flattend, ABSTRACT_PATHS = ["#text", "0"]):
    return getInformationFromDifferentPaths(abstract_flattend, ABSTRACT_PATHS)

def extractURL(location_flattend, LOCATION_PATHS = ["0_url_1_#text"]):
    return getInformationFromDifferentPaths(location_flattend, LOCATION_PATHS)

def extractInformation(item):
    # extracts general information, available for every type
    titleInfo_flattend = flattenObj(nestedDictGet(item, "titleInfo"))
    
    title = titleInfo_flattend.get("title") if titleInfo_flattend.get("title") is not None else titleInfo_flattend.get("0_title")
    subtitle = titleInfo_flattend.get("subTitle") if titleInfo_flattend.get("subTitle") is not None else titleInfo_flattend.get("0_subTitle")
    
    name_flattend = flattenObj(nestedDictGet(item, "name"))
    creator = creator = extractCreator(name_flattend)
        
    date_flattend = flattenObj(nestedDictGet(item, "originInfo"))
    publish_date = extractDate(date_flattend)
    
    abstract_flattend = flattenObj(nestedDictGet(item, "abstract"))
    abstract = extractAbstract(abstract_flattend)
    
    subjects = extractListSubject(nestedDictGet(item, "subject"))
    
    fake = Faker()
    Faker.seed( hashlib.blake2b(bytes(str(title) + str(sorted(subjects)), "utf-8") ).digest() )

    genre_flattend = flattenObj(nestedDictGet(item, "genre")) 
    genre = extractOneGenre(genre_flattend) if genre_flattend != {} else None
    
    return title, subtitle, publish_date, abstract, creator, subjects, genre

# @timeit
def extractPicture(item):
    # downloads the specialized information for pictures
    title, subtitle, publish_date, abstract, creator, subjects, genre = extractInformation(item)
    
    # only gets small preview
    location_flattend = flattenObj(nestedDictGet(item, "location"))
    url = extractURL(location_flattend)
    # if url:
    #     try:
    #         r = requests.get(url)
    #         image_a85 = a85encode(r.content)
    #     except Exception as e:
    #         logging.error(e)
    #         image_a85 = None
    # else:
    #     image_a85 = None
    image_a85 = url

    fake = Faker()
    Faker.seed( hashlib.md5(bytes(str(title) + str(sorted(subjects)), "utf-8")).digest() )
    
    val_sorte = {
        "Name": genre if genre else None,
        "Beschreibung": fake.paragraph() if genre else None
    }

    creator = gen_creator(creator if creator else fake.name())
    val_person = {
        "Vorname": creator[0],
        "Name": creator[-1],
        "Email": f"{creator[0].lower()}@{creator[-1].lower()}.{fake.tld()}",
        "Geburtsdatum": fake.date_of_birth()
    }

    val_maler = {
        "PersonId": "",
        "Beschreibung": fake.paragraph()
    }

    val_nichttextmedien = {
        "Titel": title,
        "Untertitel": subtitle,
        "Erscheinungsjahr": publish_date,
        "Kurzbeschreibung": abstract if abstract else fake.paragraph(),
        "SorteId": "",
        "Typ": ""
    }

    val_bild = {
        "NichtTextMediumId": "",
        "Bild": image_a85,
        "MalerId": ""
    }

    return val_sorte, val_person, val_maler, val_nichttextmedien, val_bild

# @timeit
def extractVideo(item):
    # downloads the specialized information for vidoes
    title, subtitle, publish_date, abstract, _, subjects, genre = extractInformation(item)

    language_flattend = flattenObj(nestedDictGet(item, "language"))
    language = language_flattend.get("languageTerm_1_#text")

    fake = Faker()
    Faker.seed( hashlib.md5(bytes(str(title) + str(sorted(subjects)), "utf-8")).digest() )

    val_sorte = {
        "Name": genre if genre else None,
        "Beschreibung": fake.paragraph() if genre else None
    }

    val_nichttextmedien = {
        "Titel": title,
        "Untertitel": subtitle,
        "Erscheinungsjahr": publish_date,
        "Kurzbeschreibung": abstract if abstract else fake.paragraph(),
        "SorteId": "",
        "Typ": ""
    }

    val_video = {
        "NichtTextMediumId": "",
        "Sprache": language
    }

    return val_sorte, val_nichttextmedien, val_video

def gen_creator(creator):
    if creator.find(",")>=0:
        return list(reversed([ elem.strip() for elem in creator.split(",") ]))
    return creator.split(" ")

# @timeit
def extractBook(item):
    # downloads the specialized information for books
    title, subtitle, publish_date, abstract, creator, subjects, genre = extractInformation(item)
    
    language_flattend = flattenObj(nestedDictGet(item, "language"))
    language = language_flattend.get("languageTerm_1_#text")
    
    originInfo_flattend = flattenObj(nestedDictGet(item, "originInfo"))
    edition = extractEdition(originInfo_flattend)
    
    publisher = extractPublisher(originInfo_flattend)
    
    # factor 100 to create cent values when dividing again
    random.seed(title)
    price = random.randint(100, 10000)/100

    fake = Faker()
    Faker.seed( hashlib.md5(bytes(str(title) + str(sorted(subjects)), "utf-8")).digest() )

    val_verlag = {
        "Kurzname" : publisher,
        "Name" : fake.company(),
        "Postleitzahl" : fake.postalcode(),
        "Strasse" : fake.street_address(),
        "Internetadresse" : fake.domain_name(),
        "Beschreibung" : fake.paragraph()
    }

    val_schlagwort = [
        {   "Wort": word if word else fake.word(), "Beschreibung": fake.paragraph() } for word in subjects
    ]

    val_buch = {
        "ISBN": fake.isbn13(),
        "Titel": title,
        "Untertitel": subtitle,
        "VerlagId": "",
        "Erscheinungsjahr": publish_date,
        "SorteId": "",
        "Kurzbeschreibung": abstract if abstract else fake.paragraph(),
        "Preis": str(price),
        "Auflage": edition,
        "Sprache": language
    }

    creator = gen_creator(creator if creator else fake.name())
    val_person = {
        "Vorname": creator[0],
        "Name": creator[-1],
        "Email": f"{creator[0].lower()}@{creator[-1].lower()}.{fake.tld()}",
        "Geburtsdatum": fake.date_of_birth()
    }

    val_autor = {
        "PersonId": "",
        "Beschreibung": fake.paragraph()
    }

    val_sorte = {
        "Name": genre if genre else None,
        "Beschreibung": fake.paragraph() if genre else None
    }
    
    return val_schlagwort, val_verlag, val_buch, val_person, val_autor, val_sorte

# @timeit
def gen_ebook(buch_isbn):
    fake = Faker()
    Faker.seed(buch_isbn)

    return {
        "ISBN": fake.isbn13(),
        "BuchISBN": buch_isbn,
        "Dateiformat": fake.file_extension(category="text")
    }

# @timeit
def gen_audiobook(buch_isbn):
    fake = Faker()
    Faker.seed(buch_isbn)

    val_verlag = {
        "Kurzname" : None,
        "Name" : fake.company(),
        "Postleitzahl" : fake.postalcode(),
        "Strasse" : fake.street_address(),
        "Internetadresse" : fake.domain_name(),
        "Beschreibung" : fake.paragraph()
    }

    creator = fake.name()
    val_person = {
        "Vorname": creator.split(" ")[0],
        "Name": creator.split(" ")[-1],
        "Email": f"{creator.split(' ')[0]}@{creator.split(' ')[-1].lower()}.{fake.tld()}",
        "Geburtsdatum": fake.date_of_birth()
    }

    val_sprecher = {
        "PersonId": "",
        "Beschreibung": fake.paragraph()
    }

    val_hoerbuch = {
        "ISBN": fake.isbn13(),
        "BuchISBN": buch_isbn,
        "SprecherId": "",
        "VerlagId": ""
    }

    return val_person, val_sprecher, val_verlag, val_hoerbuch

# @timeit
def gen_ausleihe():
    fake = Faker()

    creator = fake.name()
    val_person = {
        "Vorname": creator.split(" ")[0],
        "Name": creator.split(" ")[-1],
        "Email": f"{creator.split(' ')[0]}@{creator.split(' ')[-1].lower()}.{fake.tld()}",
        "Geburtsdatum": fake.date_of_birth()
    }

    val_ausleiher = {
        "PersonId": "",
        "Strasse": fake.street_address(),
        "Postleitzahl": fake.postalcode(),
        "Ort": fake.city(),
        "Telefonnummer" : fake.phone_number()
    }

    return val_person, val_ausleiher

# @timeit
def process_json(res):
    id, TYP = res

    t_start = time.time()
    # create a new instance of the database connection
    dbc = DBC()
    logging.info(f"Loading: {id}")
    
    
    j = dbc.get_json(id, TYP)
    obj = json.loads(j)
    logging.info(f"Loaded: {id}")

    # iterate over the items
    for num, item in enumerate(obj["items"]["mods"]):
        try:
            if item["typeOfResource"] == "text":
                val_schlagwort, val_verlag, val_buch, val_person, val_autor, val_sorte = extractBook(item)
                dbc.insert_book(val_schlagwort, val_verlag,
                                val_buch, val_person, val_autor, val_sorte)
                # Random insert of ebook
                if random.random() < 0.4:
                    val_ebook = gen_ebook(val_buch["ISBN"])
                    dbc.insert_ebook(val_ebook)
                # Random insert of audio book
                if random.random() < 0.1:
                    val_person, val_sprecher, val_verlag, val_hoerbuch = gen_audiobook(val_buch["ISBN"])
                    dbc.insert_hoerbuch(val_person, val_sprecher, val_verlag, val_hoerbuch)
                # Random insert of borrowed book
                if random.random() < 0.05:
                    val_person, val_ausleiher = gen_ausleihe()
                    dbc.insert_ausleihe(val_person, val_ausleiher, val_buch["ISBN"])
            elif item["typeOfResource"] == "moving image":
                val_sorte, val_nichttextmedien, val_video = extractVideo(item)
                dbc.insert_video(val_sorte, val_nichttextmedien, val_video)
            elif item["typeOfResource"] == "still image":
                val_sorte, val_person, val_maler, val_nichttextmedien, val_bild = extractPicture(item)
                dbc.insert_bild(val_sorte, val_person,
                                val_maler, val_nichttextmedien, val_bild)
        except Exception as e:
            logging.error(f"{id}:i{num}: {e}", exc_info=False)
    logging.info(f"Done with: {id} in {round(time.time()-t_start,2)}s")
    dbc.set_done(id, TYP)    
    dbc.del_id(id, TYP)
    dbc.close()