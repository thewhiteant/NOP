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
        # table = db.table("das")
        data_entry  = {'id':data,'sec':sec}
        srch = table.search(query.Time == time)
        if not srch:
                table.insert({'Time': time, 'data': [data_entry]})
        else:
                srch = srch[0] 
                if srch['data'][-1]['sec'] != str(sec):
                        d = srch['data']
                        d.append(data_entry)
                        table.update({'data': d}, query.Time == time)      


def Searchlog(day, tm=""):
        dt = datetime.datetime.today()
        time = dt.strftime("%I:%M")
        table =  db.table(day)
        if(time!=""):
            srch = table.search(query.Time == tm)
            return srch[0]['data']
        return table.all()
        



def Full_log_read():
        print(db.all())







 # if not srch:
        #         table.insert({'Time':time,'data':[data_entry]})
        # srch = table.search(query.Time == time)[0]
        # if srch['data'][-1][-2:] != str(sec):
        #         d = srch['data']
        #         d.append(data)
        #         table.update({'data': d}, query.Time == time)