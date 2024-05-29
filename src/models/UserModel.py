from database.db import get_connection
from .entities.User import User
import logging
def convertTuple(tup):
    str = ''
    for item in tup:
        str = str + item
    return str



class UserModel():
    @classmethod
    def get_users(self):
        try:
            connection = get_connection()
            Users = []

            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM users ORDER BY Id ASC")
                resultset = cursor.fetchall()

                for row in resultset:
                    user = User(row[0], row[1], row[2], row[3],row[4],row[5],row[6],row[7])
                    Users.append(user.to_JSON())
            connection.close()
            return Users
        except Exception as ex:
            raise Exception(ex)
            
    @classmethod
    def get_user_by_id(self,id):
        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                id=tuple(map(str, id.split(', ')))
                cursor.execute(
                 "SELECT * FROM users WHERE id=%s",(id))
                row = cursor.fetchone()
                resultset=None
                if row!=None:
                    resultset= User(row[0],row[1],row[2],row[3],None,row[5],row[6],row[7])
            connection.close()
            return resultset
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_user_by_name(self,name):
        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                cursor.execute(
                 "SELECT * FROM users WHERE name='%s'" % (name))
                row = cursor.fetchone()
                resultset=None
                if row!=None:
                    resultset= User(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7])
            connection.close()
            return resultset
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def login(self,user):
        try:
            connection = get_connection()     
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM users WHERE name='%s' AND password='%s' OR email='%s' AND password='%s'" % (user.name,user.password,user.email,user.password))
                row = cursor.fetchone()
                result_user = None
                if row != None:
                    result_user = User(row[0], row[1],  row[2],row[3],row[4],row[5],row[6])
            connection.close()
            return result_user
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def add_user(self,user):
        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO users ( name, email,mobile_number, password,adress, isadmi,img) VALUES (%s,%s,%s,%s,%s,%s,%s) ", (user.name,user.email,user.mobile_number,user.password,user.adress,user.isadmi,user.img))
                affect_rows=cursor.rowcount
                connection.commit()
            connection.close()
            return affect_rows
        except Exception as ex:
            raise Exception(ex)


    @classmethod
    def delete_user(self,Id):
        try:
            connection = get_connection()

            with connection.cursor() as cursor:
                Id=tuple(map(str, Id.split(', ')))
                cursor.execute("DELETE FROM users WHERE id =%s", (Id))
                affect_rows=cursor.rowcount
                connection.commit()
            connection.close()
            return affect_rows
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def update_user(self,user):
        try:
            connection = get_connection()

            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE users SET name=%s, email=%s,mobile_number=%s, password=%s,adress=%s, isadmi=%s WHERE id =%s ",
                    (user.name,user.email,user.mobile_number,user.password,user.adress,user.isadmi,user.id))
                affect_rows=cursor.rowcount
                connection.commit()
            connection.close()
            return affect_rows
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def update_user_profile(self,user):
        try:
            connection = get_connection()

            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE users SET name=%s, email=%s,mobile_number=%s,adress=%s,img=%s WHERE id =%s ",
                    (user.name,user.email,user.mobile_number,user.adress,user.img,user.id))
                affect_rows=cursor.rowcount
                connection.commit()
            connection.close()
            return affect_rows
        except Exception as ex:
            raise Exception(ex)
    @classmethod        
    def update_user_password(self,password,id):
        try:
            connection = get_connection()
            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE users SET password=%s WHERE id =%s ",
                    (password,id))
                affect_rows=cursor.rowcount
                connection.commit()
            connection.close()
            return affect_rows
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod        
    def check_password(self,opass,c_id):
        try:
            connection = get_connection()
            password=User.generate_password(opass)   
            row=None
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM users WHERE id=%s AND password=%s",(c_id,password))
                row=cursor.fetchone()
            connection.close()
            if row!=None:
                return 1
            else:
                return 0
        except Exception as ex:
            raise Exception(ex)


   