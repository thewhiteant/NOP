import cv2 
import face_recognition
import os
import datetime
from helpers.Logmanager import Writelog,Searchlog
from  helpers.idgenerator import GetId
from queue import Queue

# face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Face_Recognition File Check.")

Status_OF_Running = True
# Streaming_var = False
# counter = 0
# Frame_holder = Queue()

reference_folder = 'UI/static/DB/imgs'
current_directory = os.getcwd()
addrees = os.path.join(current_directory,reference_folder)


reference_faces = []
reference_face_names = []

for filename in os.listdir(reference_folder):
    if filename.endswith(".jpg"):
            reference_faces.append(filename)
            reference_face_names.append(os.path.splitext(filename)[0])


print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Loading all images Check")
faces = [] 
face_names = []
for filename in reference_faces:
            reference_face = face_recognition.load_image_file(os.path.join(reference_folder, filename))
            reference_face =  cv2.cvtColor(reference_face,cv2.COLOR_BGR2RGB)
            face_location = face_recognition.face_locations(reference_face)[0]
            Face_Encoding = face_recognition.face_encodings(reference_face)

            faces.append(Face_Encoding)
            face_names.append(os.path.splitext(filename)[0])



print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Images ready For recognition Check")



def face_match(face_file_location):

        open_face_Image = face_recognition.load_image_file(face_file_location)
        open_face_Image = cv2.cvtColor(open_face_Image,cv2.COLOR_BGR2RGB)
        face_location = face_recognition.face_locations(open_face_Image)[0]
        face_encoding = face_recognition.face_encodings(face_location)
        matches = face_recognition.compare_faces(faces,face_encoding)

        if any(matches):
              return True
        return False





def FD():
    pass
    global Status_OF_Running
    if not Status_OF_Running  : return
    print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Face_Recognition Fucntion Check")
    
    cap = cv2.VideoCapture(0)
    while Status_OF_Running:
    
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame,face_locations)


        
        if not face_locations:
            continue

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                try:
                    matches = face_recognition.compare_faces(faces, face_encoding)
                except:
                    print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Opp's Not A Face")
                    continue

                name = "Unknown"
                if True in matches:
                        matched_indices = [i for i, match in enumerate(matches) if match]
                        name = ', '.join([face_names[i] for i in matched_indices])
                        print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] ID:{name} Hi ")
                        Writelog(name)
                else:
                            unknown_face = frame[top:bottom,left:right]
                            uname = GetId()
                            unknown_face_path = os.path.join(reference_folder, uname)
                            try:
                                cv2.imwrite(unknown_face_path+".jpg", unknown_face)
                            except:
                                  continue
                                  pass
                            try:
                                unknown_face_encodings = face_recognition.face_encodings(unknown_face)[0]
                                reference_faces.append(unknown_face_encodings)
                                reference_face_names.append(uname)
                                faces.append(unknown_face_encodings)
                                face_names.append(uname)
                            except:
                                print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Uknown face problem")
                                continue



        # ret, jpeg = cv2.imencode('.jpg', frame)
        # test = jpeg.tobytes()
        # yield (b'--frame\r\n'
        #             b'Content-Type: image/jpeg\r\n\r\n' + test + b'\r\n\r\n')
    

 
    cap.release()




# def Streaming():
#             global Streaming_var
#             while True and Status_OF_Running:
                    
#                 Streaming_var = True
#                 frm = Frame_holder.get()
#                 ret, jpeg = cv2.imencode('.jpg', frm)
#                 test = jpeg.tobytes()
#                 yield (b'--frame\r\n'
#                     b'Content-Type: image/jpeg\r\n\r\n' + test + b'\r\n\r\n')






