from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

db = SQLAlchemy()

class MainTable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    UIDs = db.Column(db.String(225))
    Name = db.Column(db.String(225))
    Email = db.Column(db.String(225))
    Phone = db.Column(db.String(225))
    Adress = db.Column(db.String(225))
    Extra = db.Column(db.String(225))
    created = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def get_name(self):
        pass
    

    def __repr__(self):
        return f"<User {self.UIDs}>"



