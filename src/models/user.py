from .common import *


class User(BasicModel):
    name: str
    email: str
    user_id: str = ""
    registration_date: str = ""
    role_type: str = ""
    
class UserBasic(BasicModel):
    user_id: str = ""
    email: str = ""
    password: str = ""