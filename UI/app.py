from flask import Flask, render_template,request,redirect,url_for
import datetime
import os
from helpers import idgenerator
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from werkzeug.datastructures import FileStorage
import shutil









current_directory = os.getcwd()
Saved_location = os.path.join(current_directory,'UI/static/DB/Saved_imgs')
unknownLocations = os.path.join(current_directory,'UI/static/DB/imgs')



if not os.path.exists(Saved_location):
    os.makedirs(Saved_location)


def UI():

    print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] WebApplication Start.")

  
    app = Flask(__name__)

# DB Setup
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Main.db'
    db = SQLAlchemy(app)
    class MainTable(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        UIDs = db.Column(db.String(225))
        Name = db.Column(db.String(225))
        Email = db.Column(db.String(225))
        Phone = db.Column(db.String(225))
        Adress = db.Column(db.String(225))
        Extra = db.Column(db.String(225))
        created = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<User {self.usr}>"
    
    with app.app_context():
         db.create_all()

    @app.route('/')
    def home():
        un_all_images = []
        un_face_names = []
        for filename in os.listdir(Saved_location):
                if(filename not in un_all_images):
                    un_all_images.append(filename)
                    un_face_names.append(os.path.splitext(filename)[0])
        final_arr =  zip(un_all_images,un_face_names)
        final_arr = list(final_arr)        
        return render_template('home.html',imglist = final_arr)
        
    @app.route('/login')
    def login():
        return render_template('login.html')


    @app.route('/')
    def Add_User():
        return render_template('adduser.html')


    @app.route('/faces')
    def Unknown_Face():
        un_all_images = []
        un_face_names = []
        for filename in os.listdir(unknownLocations):
                if(filename not in un_all_images):
                    un_all_images.append(filename)
                    un_face_names.append(os.path.splitext(filename)[0])
        final_arr =  zip(un_all_images,un_face_names)
        final_arr = list(final_arr)
        
        return render_template('unknown.html',imglist = final_arr)
   
    @app.route('/details/<ID>')
    def Details(ID):
        return render_template('details.html', iden = ID)


    @app.route('/goLive')
    def GO_live():
        return render_template('golive.html')
    

    @app.route("/faces/add", methods=['POST','GET'] )
    def Face_add():
        if request.method == "POST":
                idd = request.form["Id"]
                return render_template("details.html",id = idd,loc ="test")
        
        IDGEN = idgenerator.GetIdGenNotSvae()
        return render_template("details.html",id = IDGEN,loc = "")
        

    @app.route("/faces/add_face_success", methods=['POST','GET'])
    def add_DB():
          if request.method == "POST":
                imge = request.files['img']
                myname = request.form['myname']
                emaill = request.form['emaill']
                phone = request.form["phone"]
                addrs = request.form["Address"]
                idd = request.form["Id"]
                extrea = request.form["note"]


                if(imge and myname):
                    chk = MainTable.query.filter_by(UIDs=idd).first()
                    if(not chk):
                        # TODO: Infuture face recognation fuction called for check face 
                        imge.save(os.path.join(Saved_location, f"{idd}.jpg"))
                        try:
                            new_iden = MainTable(UIDs=idd,Name=myname,Email=emaill,Phone=phone,Adress=addrs,Extra=extrea)
                            db.session.add(new_iden)
                            db.session.commit()
                        except Exception as e: 
                            print(e)
                            print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Databse Problem!")
                    return redirect(url_for("home"))

    @app.route("/faces/add_face_already_success", methods=['POST','GET'])
    def add_DB_already():
                myname = request.form['myname']
                emaill = request.form['emaill']
                phone = request.form["phone"]
                addrs = request.form["Address"]
                idd = request.form["Id"]
                extrea = request.form["note"]
                
                shutil.copy(os.path.join(unknownLocations, f"{idd}.jpg"),Saved_location)
                if(myname):
                    chk = MainTable.query.filter_by(UIDs=idd).first()
                    if(not chk):
                        # TODO: Infuture face recognation fuction called for check face 
                        try:
                            new_iden = MainTable(UIDs=idd,Name=myname,Email=emaill,Phone=phone,Adress=addrs,Extra=extrea)
                            db.session.add(new_iden)
                            db.session.commit()
                        except Exception as e: 
                            print(e)
                            print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Databse Problem!")
                    return redirect(url_for("home"))



    app.run(debug=True)

    



