import cv2 
import face_recognition
import os
import datetime
from helpers.Logmanager import Writelog
from  helpers.idgenerator import GetId
import base64
from time import sleep


# face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Face_Recognition File Check.")

Status_OF_Running = True


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
            try:      
                Face_Encoding = face_recognition.face_encodings(reference_face)[0]
                faces.append(Face_Encoding)
                face_names.append(os.path.splitext(filename)[0])
                print(len(filename))
            except:
                print(filename)




print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Images ready For recognition Check")



def FD(socketio=""):
    
    global Status_OF_Running
    if not Status_OF_Running  : return
    print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Face_Recognition Fucntion Check")
    
    cap = cv2.VideoCapture(0)
    while Status_OF_Running:

        print("Runnoing")
        ret, frame = cap.read()
        if not ret:
            break
        
        if socketio != "":
            _,buffer = cv2.imencode(".jpg",frame)
            bfreame = base64.b64encode(buffer).decode('utf-8')
            socketio.emit("new_frame",{'image':bfreame})
    

        face_locations = face_recognition.face_locations(frame) #gies multiple faces of frames
        face_encodings = face_recognition.face_encodings(frame,face_locations) # encode all of them

        
        if not face_locations:
            continue
   
        for (top, right, bottom, left), FE in zip(face_locations, face_encodings):

        


                try:
                    matches = face_recognition.compare_faces(faces, FE)
         
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
        
        sleep(0.05)  
    

    cap.release()
    cv2.destroyAllWindows()




def face_match(face_file_location):

        open_face_Image = face_recognition.load_image_file(face_file_location)
        open_face_Image = cv2.cvtColor(open_face_Image,cv2.COLOR_BGR2RGB)
        face_location = face_recognition.face_locations(open_face_Image)[0]
        face_encoding = face_recognition.face_encodings(face_location)
        matches = face_recognition.compare_faces(faces,face_encoding)

        if any(matches):
              return True
        return False
