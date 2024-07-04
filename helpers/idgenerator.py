from tinydb import TinyDB,Query
import datetime
import random
import string
import os

current_directory = os.getcwd()
reference_folder = "UI/static/DB/logs/ids.json"
addrees = os.path.join(current_directory,reference_folder)

db = TinyDB(addrees)
query = Query()
table = db.table("IDSavingtable")

def GetId():
    dt = datetime.datetime.today()
    res = dt.strftime("%m%d%I%M%S")
    time = dt.strftime("%I:%M:%S")
    characters = string.ascii_letters + string.digits
    code_length = 4
    hulfhash = chr(65+(int(res[0:2])%26 )) + chr(65+(int(res[2:4]))%26 ) + chr(48+(int(res[4:6])%9)) + chr(65+(int(res[6:8]))%26 ) + chr(65+(int(res[8:10]))%26 )
    random_code = "".join(random.choice(characters) for _ in range(code_length))
    hash = hulfhash+random_code
    h = table.search(query.ID == hash)
    if h or (len(hash)!= 9):
        hash = GetId()
    table.insert({'ID':hash,"Time":time,'userid':-1})
    return hash



def GetIdGenNotSvae():
    dt = datetime.datetime.today()
    res = dt.strftime("%m%d%I%M%S")
    time = dt.strftime("%I:%M:%S")
    characters = string.ascii_letters + string.digits
    code_length = 4
    hulfhash = chr(65+(int(res[0:2])%26 )) + chr(65+(int(res[2:4]))%26 ) + chr(48+(int(res[4:6])%9)) + chr(65+(int(res[6:8]))%26 ) + chr(65+(int(res[8:10]))%26 )
    random_code = "".join(random.choice(characters) for _ in range(code_length))
    hash = hulfhash+random_code
    h = table.search(query.ID == hash)
    if h or (len(hash)!= 9):
        hash = GetId()
    return hash


def saveId(hash):
    dt = datetime.datetime.today()
    time = dt.strftime("%I:%M:%S")
    table.insert({'ID':hash,"Time":time,'userid':-1})


