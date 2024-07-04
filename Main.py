from UI import app
from Dsystem import Vision
from threading import Thread
import datetime
from helpers.Logmanager import Full_log_read
from helpers.db_manager import db, MainTable

# Done 1: Start Stop Done
# Done 2: DBMS Funtions
# Cancel 3: Gather Under Same User Id 
# TODO 4: TimeLines



app.UI()
# print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Successfully Closed!")

# Full_log_read()