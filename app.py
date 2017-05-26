from flask import Flask
from flask_restful import Api, Resource, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:findasecret@localhost/postgres'
db = SQLAlchemy(app)

Base = declarative_base()
engine = create_engine('postgresql://<user>:<password>@localhost/postgres')
Session = sessionmaker(bind=engine)
session = Session()


user_fields = {
        'id': fields.Integer,
        'username': fields.String,
        'email': fields.String
        }

class UserResource(Resource):
    @marshal_with(user_fields)
    def get(self, id):
        user = session.query(User).get(id)
        print(id)
        return user


class UserList(Resource):
    @marshal_with(user_fields)
    def get(self):
        return session.query(User).all()


class User(Base):
    __tablename__= 'User'

    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True)
    email = Column(String(120), unique=True)

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return "<User(id = '%s', username='%s', email='%s')>" % (self.id, self.username, self.email)

api.add_resource(UserResource, '/users/<int:id>', endpoint='user')
api.add_resource(UserList, '/users')

if __name__ == '__main__':
    app.run(debug=True)
