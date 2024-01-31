import datetime
from tinydb import TinyDB,Query
import os


reference_folder = "UI/static/DB/logs/log.json"
current_directory = os.getcwd()
addrees = os.path.join(current_directory,reference_folder)
db = TinyDB(addrees)
query = Query()



def Writelog(data):
        dt = datetime.datetime.today()
        date = dt.date()
        time = dt.strftime("%I:%M")
        sec = dt.strftime("%S")
        table = db.table(str(date))
        data = data+" "+sec
        srch = table.search(query.Time == time)
        if not srch:
                table.insert({'Time':time,'data':[data]})
        srch = table.search(query.Time == time)[0]
        if srch['data'][-1][-2:] != str(sec):
                d = srch['data']
                d.append(data)
                table.update({'data': d}, query.Time == time)

        


def Searchlog(day, tm=""):
        dt = datetime.datetime.today()
        time = dt.strftime("%I:%M")
        table =  db.table(day)
        if(time!=""):
            srch = table.search(query.Time == tm)
            return srch[0]['data']
        return table.all()
        





