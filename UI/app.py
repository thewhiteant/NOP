from flask import Flask, render_template, request, redirect, url_for, Response
import datetime
import os
import threading
import shutil
from werkzeug.datastructures import FileStorage
from flask_socketio import SocketIO
from helpers import idgenerator
from Dsystem import Vision
from helpers.db_manager import db, MainTable,get_user,delete_user_by_uid # Import db and MainTable from database.py
import json

current_directory = os.getcwd()
Saved_location = os.path.join(current_directory, 'UI/static/DB/Saved_imgs')
unknownLocations = os.path.join(current_directory, 'UI/static/DB/imgs')

if not os.path.exists(Saved_location):
    os.makedirs(Saved_location)

if not os.path.exists(unknownLocations):
    os.makedirs(unknownLocations)

def UI():
    # print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] UI Check.")
    app = Flask(__name__)
    socketio = SocketIO(app)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Main.db'
    # app.config['DEBUG'] = True 
    db.init_app(app)  

    with app.app_context():
        db.create_all()

    @app.route('/')
    def home():
        un_all_images = []
        un_face_names = []
        for filename in os.listdir(Saved_location):
            if filename not in un_all_images:
                un_all_images.append(filename)
                un_face_names.append(get_user(os.path.splitext(filename)[0]))
        final_arr = zip(un_all_images, un_face_names)
        final_arr = list(final_arr)
        return render_template('home.html', imglist=final_arr, ck=Vision.Status_OF_Running)



    @app.route('/login')
    def login():
        return render_template('login.html')

    @app.route('/start')
    def StartFace_recgonition():
        if Vision.Status_OF_Running:
            return "<script>alert('Already Running'); window.location.href = '/';</script>"
        else:
            Vision.Status_OF_Running = True
            Face_recog = threading.Thread(target=Vision.FD, args=(socketio,))
            Face_recog.daemon = True
            Face_recog.start()
            return redirect(url_for('home'))

    @app.route('/stop')
    def Stop_Face_recognition():
        if not Vision.Status_OF_Running:
            return "<script>alert('Already Stopped'); window.location.href = '/';</script>"
        else:
            Vision.Status_OF_Running = False
            return redirect(url_for('home'))

    @app.route('/timeline')
    def Timeline():
        with open('UI/static/DB/Logs/log.json', 'r') as f:
             data = json.load(f)
        return render_template('timeline.html',data=data,get_user=get_user)

    @app.route('/faces')
    def Unknown_Face():
        un_all_images = []
        un_face_names = []
        for filename in os.listdir(unknownLocations):
            if filename not in un_all_images:
                un_all_images.append(filename)
                un_face_names.append(get_user(os.path.splitext(filename)[0]))
        final_arr = zip(un_all_images, un_face_names)
        final_arr = list(final_arr)
        return render_template('unknown.html', imglist=final_arr)

    @app.route('/details/<ID>')
    def Details(ID):
        return render_template('details.html', iden=ID)

    @app.route('/live')
    def GO_live():
        return render_template('golive.html')

    @app.route('/video_feed')
    def video_feed():
        # return Response(Vision.FD(), mimetype='multipart/x-mixed-replace; boundary=frame')
        # TODO: Dangerous Lines
        pass

    @app.route("/delete", methods=['POST', 'GET'])
    def home_delete_item():
        if request.method == "POST":
            uid = request.form["delete_item"]
            delete_user_by_uid(uid[:-4])
            file_path = os.path.join(Saved_location, f"{uid}")
            if os.path.isfile(file_path):
                os.remove(file_path)
        return redirect(url_for('home'))


    @app.route("/faces/add", methods=['POST', 'GET'])
    def Face_add():
        if request.method == "POST":
            idd = request.form["Id"]
            return render_template("details.html", id=idd, loc="test")

        IDGEN = idgenerator.GetIdGenNotSvae()
        return render_template("details.html", id=IDGEN, loc="")


    @app.route("/faces/add_face_success", methods=['POST', 'GET'])
    def add_DB():
        if request.method == "POST":
            imge = request.files['img']
            myname = request.form['myname']
            emaill = request.form['emaill']
            phone = request.form["phone"]
            addrs = request.form["Address"]
            idd = request.form["Id"]
            extrea = request.form["note"]
            if imge and myname:
                chk = MainTable.query.filter_by(UIDs=idd).first()
                if not chk:
                    # TODO: In future face recognition function called for check face
                    imge.save(os.path.join(Saved_location, f"{idd}.jpg"))
                    try:
                        new_iden = MainTable(UIDs=idd, Name=myname, Email=emaill, Phone=phone, Address=addrs, Extra=extrea)
                        db.session.add(new_iden)
                        db.session.commit()
                    except Exception as e:
                        print(e)
                        print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Database Problem!")
                return redirect(url_for("home"))

    @app.route("/faces/add_face_already_success", methods=['POST', 'GET'])
    def add_DB_already():
        myname = request.form['myname']
        emaill = request.form['emaill']
        phone = request.form["phone"]
        addrs = request.form["Address"]
        idd = request.form["Id"]
        extrea = request.form["note"]

        shutil.copy(os.path.join(unknownLocations, f"{idd}.jpg"), Saved_location)
        if myname:
            chk = MainTable.query.filter_by(UIDs=idd).first()
            if not chk:
                # TODO: In future face recognition function called for check face
                new_iden = MainTable(UIDs=idd, Name=myname, Email=emaill, Phone=phone, Address=addrs, Extra=extrea)
                db.session.add(new_iden)
                try:
                    db.session.commit()
                except Exception as e:
                    db.session.rollback()
                    print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Database Commit Error:", e)
                return redirect(url_for("home"))



    


    @socketio.on('connect')
    def handle_connect():
        print('Client connected')
 
    @socketio.on('disconnect')
    def handle_disconnect():
        print('Client disconnected')



    Face_recog = threading.Thread(target=Vision.FD, args=(socketio,))
    Face_recog.daemon = True
    Face_recog.start()

    # socketio.run(app)
    socketio.run(app, host='0.0.0.0', port=5000)
