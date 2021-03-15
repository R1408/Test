from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
# from sqlalchemy import ForeignKey
# from sqlalchemy.orm import relationship, backref
# from sqlalchemy.orm import backref
from sqlalchemy.dialects.postgresql import JSON
from datetime import datetime
from sqlalchemy.types import Text

from main import *

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:''@localhost:3306/test'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    phone_number = db.Column(db.String(255))
    name = db.Column(db.String(255))
    password = db.Column(db.String(255))

    def serialize(self):
        return {'id': self.id, 'phone_number': self.phone_number, 'name': self.name, 'password': self.password}

class User_email(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    email = db.Column(db.String(255))
    user = db.relationship("User", backref=db.backref("user", uselist=False))

    def serialize(self):
        return {'id': self.id, 'user_id': self.user_id, 'email': self.email}


class User_login(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    session = db.Column(db.String(255))
    last_login = db.Column(db.DateTime, default=datetime.utcnow())
    user = db.relationship("User", backref=db.backref("user_id", uselist=False))

    def serialize(self):
        return {'id': self.id, 'user_id': self.user_id, 'session': self.session, 'last_login': self.last_login}

if __name__ == '__main__':
    manager.run()