from app import db
from flask_login import UserMixin

class User(UserMixin, db.Document):
    meta = {'collection': 'appUsers'}
    email = db.StringField(max_length=30)
    password = db.StringField()
    name = db.StringField()

    @staticmethod
    def getUser(email):
        return User.objects(email=email).first()
    
    @staticmethod    
    def getAllUsers():
        users = list(User.objects())
        return sorted(users, key=lambda user: user.name)

    @staticmethod #singleto pattern
    def createUser(email, name, password):
        user = User.getUser(email)
        if not user:
            user = User(email=email, name=name, password=password).save()
        return user