from UI import app
import os
from Dsystem import Vision
from threading import Thread
import datetime



reference_folder = 'UI/static/DB/imgs'
current_directory = os.getcwd()
addrees = os.path.join(current_directory,reference_folder)


all_images = []
face_names = []

for filename in os.listdir(reference_folder):
    if filename.endswith(".jpg") or filename.endswith(".png"):
            all_images.append(filename)
            face_names.append(os.path.splitext(filename)[0])



def u():
    app.UI()
def v():
    Vision.FD(all_images,face_names,addrees)



ux = Thread(target=u)
vs = Thread(target=v)


u()

         
# ux.start()
# vs.start()



print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Successfully Closed!")




