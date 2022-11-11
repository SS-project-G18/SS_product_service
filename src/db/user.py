from models import User, UserBasic

from . import users_db


def get_user_with_id(user_id):
    user = users_db.find_one({"user_id": user_id})
    if user!=None:
        return User.parse_obj(user)
    

def find_user_with_email(email):
    user = users_db.find_one({"email": email})
    if user!=None:
        return UserBasic.parse_obj(user)