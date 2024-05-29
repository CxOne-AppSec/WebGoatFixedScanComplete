import hashlib
from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id, name=None, email=None,mobile_number=None, password=None,adress=None, isadmi=None,img=None) -> None:
        self.id = id
        self.name = name
        self.email=email
        self.mobile_number=mobile_number
        self.password = password
        self.adress=adress
        self.isadmi = isadmi
        self.img=img
        
    def to_JSON(self):
        return{
            'id':self.id,
            'name':self.name,
            'email':self.email,
            'mobile_number':self.mobile_number,
            'password':self.password,
            'adress':self.adress,
            'isadmi':self.isadmi,
            'img':self.img
        }

    @classmethod
    def Check_password(self,hashed_password,password):
        password2=hashlib.md5(password.encode('utf8')).hexdigest()
        return hashed_password==password2

    @classmethod
    def generate_password(self,password:str):
        return hashlib.md5(password.encode('utf8')).hexdigest()
