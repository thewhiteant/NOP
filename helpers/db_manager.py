from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

db = SQLAlchemy()

class MainTable(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    UIDs = db.Column(db.String(225), unique=True, nullable=False)
    Name = db.Column(db.String(225))
    Email = db.Column(db.String(225))
    Phone = db.Column(db.String(225))
    Address = db.Column(db.String(225))
    Extra = db.Column(db.String(225))
    created = db.Column(db.DateTime(timezone=True), server_default=func.now())

    @property
    def name(self):
        return self.Name
    
    @name.setter
    def name(self, value):
        self.Name = value

    @property
    def email(self):
        return self.Email
    
    @email.setter
    def email(self, value):
        self.Email = value

    @property
    def phone(self):
        return self.Phone
    
    @phone.setter
    def phone(self, value):
        self.Phone = value

    @property
    def address(self):
        return self.Address
    
    @address.setter
    def address(self, value):
        self.Address = value

    @property
    def extra(self):
        return self.Extra
    
    @extra.setter
    def extra(self, value):
        self.Extra = value

    def __repr__(self):
        return f"<MainTable id={self.id}, Name={self.Name}, Email={self.Email}, Phone={self.Phone}, Address={self.Address}, Extra={self.Extra}, UIDs={self.UIDs}, created={self.created}>"

def get_user(user_uid):
    user = MainTable.query.filter_by(UIDs=user_uid).first()
    if user:
        return user.Name
    return  user_uid


def get_all_data():
    return MainTable.query.all()

def delete_user_by_uid(user_id):
    user = MainTable.query.filter_by(UIDs=user_id).first()
    if user:
        db.session.delete(user)
        db.session.commit()