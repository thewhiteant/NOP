import cv2 
import face_recognition
import os
import datetime
from helpers.Logmanager import Writelog,Searchlog
from  helpers.idgenerator import GetId


# face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')


def FD(reference_faces,reference_face_names,reference_folder):
    # reference_folder = '/DB/unknown/'
    # unknown_faces_folder = '/DB/unknown/'
    # if not os.path.exists(reference_folder):
    #     os.makedirs(reference_folder)
    faces = []
    face_names = []
    #face load from file
    # for filename in os.listdir(reference_folder):
    #     if filename.endswith(".jpg") or filename.endswith(".png"):

    #         reference_face = face_recognition.load_image_file(os.path.join(reference_folder, filename))
    for filename in reference_faces:
        reference_face = face_recognition.load_image_file(os.path.join(reference_folder, filename))
        try:
                reference_face_encoding = face_recognition.face_encodings(reference_face)[0]
                faces.append(reference_face_encoding)
                face_names.append(os.path.splitext(filename)[0])

        except:
                print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Some error")




    cap = cv2.VideoCapture(0)
    print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Recognation Process Ready.")

    while True:

        xti = datetime.datetime.now()
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        try:
            #prottecta frame er face detect
            face_locations = face_recognition.face_locations(frame)
            face_encodings = face_recognition.face_encodings(frame, face_locations)
        except:
            print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] frame multiple face")
            # pass

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):

                try:
                    matches = face_recognition.compare_faces(faces, face_encoding)
                except:
                    print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Match error")
                    # pass
                name = "Unknown"

                # cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                # cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                # cv2.imshow("data",frame)


                if True in matches:
                        matched_indices = [i for i, match in enumerate(matches) if match]
                        name = ', '.join([face_names[i] for i in matched_indices])
                        # print(name + " " + xti.strftime("%H:%M:%S %p"))
                        Writelog(name)
                else:
                            # unknown_face = cv2.rectangle(frame,(left, top), (right, bottom), (0, 0, 225), 2)
                            unknown_face = frame[top-100:bottom+100,left-100:right+100]
                            uname = GetId()
                            unknown_face_path = os.path.join(reference_folder, uname)
                            try:
                                cv2.imwrite(unknown_face_path+".jpg", unknown_face)
                            except:
                                  pass
                                # print("Image save error")
                            # unknown_face_locations = face_recognition.face_locations(unknown_face)
                            try:
                                unknown_face_encodings = face_recognition.face_encodings(unknown_face)[0]
                                reference_faces.append(unknown_face_encodings)
                                reference_face_names.append(uname)
                                faces.append(unknown_face_encodings)
                                face_names.append(uname)
                            except:
                                print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Uknown face detect problem")




    cap.release()
    cv2.destroyAllWindows()






