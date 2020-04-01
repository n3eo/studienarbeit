import requests
import json
import traceback
import itertools
import re
import random

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
    topics = []
    if isinstance(subjects, list):
        for item in subjects:
            flattened = flattenObj(item)
            topics += extractListSubject(flattened)
    
    if isinstance(subjects, dict):
        for key, val in subjects.items():
            if not key.find("@authority") >= 0:
                topics.append(val)
    
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
    
    return title, subtitle, publish_date, abstract, creator, subjects

def extractBook(item):
    title, subtitle, publish_date, abstract, creator, subjects = extractInformation(item)
    
    language_flattend = flattenObj(nestedDictGet(item, "language"))
    language = language_flattend.get("languageTerm_1_#text")
    
    originInfo_flattend = flattenObj(nestedDictGet(item, "originInfo"))
    edition = extractEdition(originInfo_flattend)
    
    publisher = extractPublisher(originInfo_flattend)
    
    # factor 100 to create cent values when dividing again
    random.seed(title)
    price = random.randint(100, 10000)/100
    
    return title, subtitle, publish_date, abstract, creator, subjects, language, edition, publisher, price

r = requests.get("https://api.lib.harvard.edu/v2/items.json?q=*&limit=250&sort=recordIdentifier")
obj = json.loads(r.text)

# obj.get("pagination").get("numFound") exists always
for start_value in range( obj.get("pagination").get("numFound") // 250 + 1):
    print(f"{(start_value+1)*250}")
    
    r = requests.get(f"https://api.lib.harvard.edu/v2/items.json?q=*&limit=250&start={start_value*250}&sort=recordIdentifier")
    obj = json.loads(r.text)
    
    for num, item in enumerate(obj["items"]["mods"]):
        try:
            extractInformation(item)
            # TODO Do something
        except Exception as e:
            print(f"\nError in Round {start_value} Entry {num}:\n\n")
            print(traceback.print_exc())
            print("\n\n")
            print(item)
            test_break = True
            break
    if test_break: break


# # Test single entrys

# In[37]:


start_value = 37
entry = 200

r = requests.get(f"https://api.lib.harvard.edu/v2/items.json?q=*&limit=250&start={start_value*250}&sort=recordIdentifier")
item = json.loads(r.text)["items"]["mods"][entry]


# In[46]:


extractInformation(item)

