from UI import app
from Dsystem import Vision
from threading import Thread
import datetime

def run_ui():
    app.UI()

def run_face_recognition():
    Vision.FD()

# UIThre = Thread(target=run_ui)
Face_Recognition_thread = Thread(target=run_face_recognition)

Face_Recognition_thread.start()
# UIThre.start()

# Wait for both threads to finish
# UIThre.join()
Face_Recognition_thread.join()

print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Successfully Closed!")
