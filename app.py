from flask import Flask
from flask_restful import Api, Resource, fields, marshal_with
#from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)
api = Api(app)
#db = SQLAlchemy(app)

@app.after_request

def after_request(response):
    response.headers.add('Access-Control-Allow-Origin','*')
    return response

Base = declarative_base()
engine = create_engine('postgresql://juanpa:dagBMX20@localhost/todo')
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
    __tablename__= 'user_account'

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
