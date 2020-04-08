import httpx, requests
import json
import logging
import mysql.connector
from faker import Faker
from base64 import a85encode
import re
import random
import time

from db_connection import DbConnection as DBC

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
    Faker.seed(hash(str(title) + str(subjects)))

    genre_flattend = flattenObj(nestedDictGet(item, "genre")) 
    genre = extractOneGenre(genre_flattend) if genre_flattend != {} else fake.word()
    
    return title, subtitle, publish_date, abstract, creator, subjects, genre

def extractPicture(item):
    title, subtitle, publish_date, abstract, creator, subjects, genre = extractInformation(item)
    
    # only gets small preview
    location_flattend = flattenObj(nestedDictGet(item, "location"))
    url = extractURL(location_flattend)
    if url:
        r = requests.get(url)
        image_a85 = a85encode(r.content)
    else:
        image_a85 = None

    fake = Faker()
    Faker.seed(hash(str(title) + str(subjects)))

    val_sorte = {
        "Name": genre if genre else fake.word(),
        "Beschreibung": fake.paragraph()
    }

    creator = creator if creator else fake.name()
    val_person = {
        "Vorname": creator.split(" ")[0],
        "Name": creator.split(" ")[-1],
        "Email": f"{creator.split(' ')[0]}@{creator.split(' ')[-1]}.{fake.tld()}",
        "Geburtsdatum": fake.date_of_birth()
    }

    val_maler = {
        "PersonenId": "",
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
        "NichtTextMedienId": "",
        "Bild": image_a85,
        "MalerId": ""
    }

    return val_sorte, val_person, val_maler, val_nichttextmedien, val_bild

def extractVideo(item):
    title, subtitle, publish_date, abstract, _, subjects, genre = extractInformation(item)

    language_flattend = flattenObj(nestedDictGet(item, "language"))
    language = language_flattend.get("languageTerm_1_#text")

    fake = Faker()
    Faker.seed(hash(str(title) + str(subjects)))

    val_sorte = {
        "Name": genre if genre else fake.word(),
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

    val_video = {
        "NichtTextMedienId": "",
        "Sprache": language
    }

    return val_sorte, val_nichttextmedien, val_video

def extractBook(item):
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
    Faker.seed(hash(str(title) + str(subjects)))

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
        "ISBN": fake.isbn13().replace("-",""),
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

    creator = creator if creator else fake.name()
    val_person = {
        "Vorname": creator.split(" ")[0],
        "Name": creator.split(" ")[-1],
        "Email": f"{creator.split(' ')[0]}@{creator.split(' ')[-1]}.{fake.tld()}",
        "Geburtsdatum": fake.date_of_birth()
    }

    val_autor = {
        "PersonenId": "",
        "Beschreibung": fake.paragraph()
    }

    val_sorte = {
        "Name": genre if genre else fake.word(),
        "Beschreibung": fake.paragraph()
    }
    
    return val_schlagwort, val_verlag, val_buch, val_person, val_autor, val_sorte

def setup():
    logging.basicConfig(filename="../jupyter/logs/api_requests.log",
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.INFO)

    dbc = DBC()

    start = 0 # 0
    rtyp = "text" # "still%20image" "moving%20image"
    default_sleep_time = 2

    r = requests.get(f"https://api.lib.harvard.edu/v2/items.json?q=*&limit=250&sort=recordIdentifier&resourceType={rtyp}")
    obj = json.loads(r.text)

    total = obj.get("pagination").get("numFound")

    return dbc, start, rtyp, default_sleep_time, total

async def submain(start_value,rtyp,dbc,total):
    t_start = time.time()
    async with httpx.AsyncClient() as client:
        r = await client.get(f"https://api.lib.harvard.edu/v2/items.json?q=*&limit=250&start={start_value*250}&sort=recordIdentifier&resourceType={rtyp}")

    obj = json.loads(r.text)

    print("Processing items...")
    for item in obj["items"]["mods"]:
        try:
            if item["typeOfResource"] == "text":
                val_schlagwort, val_verlag, val_buch, val_person, val_autor, val_sorte = await extractBook(item)
                dbc.insert_book(val_schlagwort, val_verlag,
                                val_buch, val_person, val_autor, val_sorte)
            elif item["typeOfResource"] == "moving image":
                val_sorte, val_nichttextmedien, val_video = await extractVideo(item)
                dbc.insert_video(val_sorte, val_nichttextmedien, val_video)
            else:
                val_sorte, val_person, val_maler, val_nichttextmedien, val_bild = await extractPicture(item)
                dbc.insert_bild(val_sorte, val_person,
                                val_maler, val_nichttextmedien, val_bild)
        except Exception as e:
            logging.error(e, exc_info=True)
    logging.info(
        f"{(start_value+1)*250} of {total} ({(((start_value+1)*250)/total)*100} %)")
    logging.info(f"Took: {time.time()-t_start}")

@timeit
def concurrent_submain(start_value):
    dbc = DBC()    
    logging.info(f"Starting with {start_value}.")
    dbc.set_prossesing(start_value)
    try:
        r = requests.get(f"https://api.lib.harvard.edu/v2/items.json?q=*&limit=250&start={start_value*250}&sort=recordIdentifier")
    except Exception as e:
        dbc.set_pending(start_value)
        logging.error(e, exc_info=True)
        return
    obj = json.loads(r.text)
    
    for num, item in enumerate(obj["items"]["mods"]):
        try:
            if item["typeOfResource"] == "text":
                val_schlagwort, val_verlag, val_buch, val_person, val_autor, val_sorte = extractBook(item)
                dbc.insert_book(val_schlagwort, val_verlag,
                                val_buch, val_person, val_autor, val_sorte)
            elif item["typeOfResource"] == "moving image":
                val_sorte, val_nichttextmedien, val_video = extractVideo(item)
                dbc.insert_video(val_sorte, val_nichttextmedien, val_video)
            else:
                val_sorte, val_person, val_maler, val_nichttextmedien, val_bild = extractPicture(item)
                dbc.insert_bild(val_sorte, val_person,
                                val_maler, val_nichttextmedien, val_bild)
        except Exception as e:
            logging.error(e, exc_info=True)
    logging.info(f"Done with {start_value}.")
    dbc.set_done(start_value)
    dbc.close()
    

async def main(dbc, start, rtyp, default_sleep_time, total):
    for start_value in range( start, total // 250 + 1):
        await submain(start_value,rtyp,dbc,total)
    
if __name__ == "__main__":
    dbc, start, rtyp, default_sleep_time, total = setup()
    main(dbc, start, rtyp, default_sleep_time, total)




