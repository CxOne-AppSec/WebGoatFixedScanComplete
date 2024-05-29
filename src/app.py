from config import config
import json
from flask import Flask,render_template,request,redirect,url_for,flash,jsonify
from flask_login import LoginManager,login_user,logout_user,login_required
from urllib.parse import urlparse
import requests
import psycopg2.extras
psycopg2.extras.register_uuid() 
import uuid
#models
from models.UserModel import UserModel
from models.ProductModel import ProductModel
from models.CommentModel import CommentModel
#entities
from models.entities.User import User
from models.entities.Product import Product
from models.entities.Comment import Comment
#other
from flask_cors import CORS,cross_origin
import logging
import datetime
import pickle
import sys
import os
import re
app = Flask(__name__)
login_manager_app=LoginManager(app)
app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app, resource={r"/*":{"origins":"*"}})

@login_manager_app.user_loader
def load_user(user_id):
    return UserModel.get_user_by_id(user_id)


def convertTuple(tup):
    str = ''
    for item in tup:
        str = str + item
    return str
@app.route('/')
def index():
    products=[]
    products=ProductModel.get_products()
    return render_template('store/home.html',queryset=products)

@app.route('/search', methods=['POST'])
def search():
    search=request.form['search']
    Products=[]
    Products=ProductModel.get_product_by_names(search)
    return render_template('store/home.html',queryset=Products)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:         
            name = request.form['Username']
            password = request.form['Password']
            user = User(0, name, name,0,User.generate_password(password))
            logged_user = UserModel.login(user)
            if logged_user != None:
                    login_user(logged_user)
                    return redirect(url_for('index'))
            else:
                flash('Invalid user ...')
                return render_template('auth/login.html')
        except Exception as ex:
            return jsonify({'message': str(ex)}), 500
    else:
        return render_template('auth/login.html')
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def created_account():
    if request.method == 'POST':
        try:
            UserName = request.form['Username']
            Password = request.form['Password']
            ConfirmPassword = request.form['Password2']
            Email = request.form['Email']
            Mobile_number = request.form['Mobile_number']
            Adress = request.form['Adress']
            IsAdmi=request.form['IsAdmi']
            if Password != ConfirmPassword:
                flash("Password not match, please enter again")
                return render_template('/auth/register.html')
            Password=User.generate_password(Password)
            user = User(0, UserName, Email,Mobile_number,Password,Adress ,IsAdmi,None)
            affect_rows = UserModel.add_user(user)
            if affect_rows == 1:
                return render_template('/auth/login.html')
            else:
                return jsonify({'message': str(ex)}), 500
        except Exception as ex:
            return jsonify({'message': str(ex)}), 500
    else:
        return render_template('/auth/register.html')


@app.route('/create_user',methods=['GET', 'POST'])
def created_user():
    if request.method == 'POST':
        try:
            Name = request.form['Name']
            Email = request.form['Email']
            Mobile=request.form['Mobile_number']
            Adress=request.form['Adress']
            IsAdmi=request.form['IsAdmi']
            Password=request.form['Password']
            ConfirmPassword=request.form['PasswordC']
            if Password != ConfirmPassword:
                flash("Password not match, please enter again")
                return redirect(url_for('Manage_users'))
            Password=convertTuple(Password)
            Password=User.generate_password(Password)
            user = User(0,Name, Email,Mobile,Password,Adress ,IsAdmi)
            affect_rows = UserModel.add_user(user)
            affect_rows=1
            if affect_rows == 1:
                return redirect(url_for('Manage_users'))
            else:
                return jsonify({'message': str(ex)}), 500
        except Exception as ex:
            return jsonify({'message': str(ex)}), 500
    else:
        return render_template('/store/Manage_Users/manage_users.html')

@app.route('/delete_user/<Id>')
def delete_user(Id):
        UserModel.delete_user(Id)
        return redirect(url_for('Manage_users'))

@app.route('/update_user',methods=['GET', 'POST'])
@login_required
def update_user():
    if request.method == 'POST':
        try:
            Id = request.form['Id']
            Name = request.form['Name']
            Email = request.form['Email']
            Mobile=request.form['Mobile_number']
            Adress=request.form['Adress']
            IsAdmi=request.form['IsAdmi']
            Password=request.form['Password']
            ConfirmPassword=request.form['PasswordC']
            if Password != ConfirmPassword:
                flash("Password not match, please enter again")
                return redirect(url_for('Manage_users'))
            Password=convertTuple(Password)
            Password=User.generate_password(Password)
            user=User(Id,Name,Email,Mobile,Password,Adress,IsAdmi)
            affect_rows =UserModel.update_user(user)
            if affect_rows == 1:
                return redirect(url_for('Manage_users'))
            else:
                return jsonify({'message': str(ex)}), 500
        except Exception as ex:
            return jsonify({'message': str(ex)}), 500
    else:
        Id=request.args.get('Id',default='', type=str)
        usuario=UserModel.get_user_by_id(Id)
        return render_template('/store/Manage_Users/EditUser.html',usuario=usuario)


@app.route('/MyProfile/<Id>')  
@login_required 
def Profile(Id):
    usuario=UserModel.get_user_by_id(Id)
    return render_template('auth/Profile.html',user=usuario)

@app.route('/ExportProfile/<Id>')  
@login_required 
def Export_profile(Id):
    usuario=UserModel.get_user_by_id(Id)
    Usuario={'User':usuario.name,
            'Email':usuario.email,
            'Phone':usuario.mobile_number,
            'Adress':usuario.adress,
            'Image':usuario.img}
    with open(usuario.name + ".json","wb") as outfile:    
        json.dump(Usuario,outfile)
    return render_template('auth/Profile.html',user=usuario)



@app.route('/User/<Name>')
def profile_public(Name):
    try:
        print(Name)
        usuario=UserModel.get_user_by_name(Name)
        return render_template('auth/Profile_public.html',user=usuario)
    except Exception as ex:
        return jsonify({'message': str(ex),'Source':usuario}), 500


@app.route('/display/<img>')
#@login_required
def display_image(img):
    return redirect(url_for('static',filename= "media/" + img), code=301)

    

@app.route('/update_profile',methods=['POST'])
@login_required 
def update_profile():
    if request.method == 'POST':
        try:
            Id = request.form['ModUsrId']
            Current_Id=request.form['LogUsrId']
            if Id==Current_Id:
                Name = request.form['Name']
                Mobile=request.form['Mobile_number']
                Adress=request.form['Adress']
                Email =request.form['Email']
                Image=request.files['Image']
                file=request.files['File']

                if file.filename!='':
                    with open(file.filename, "rb") as infile:
                        Profile=json.load(infile)
                        user=User(Id,Profile['User'],Profile['Email'],Profile['Phone'],None,Profile['Adress'],None,Profile['Image'])
                    affect_rows =UserModel.update_user_profile(user)
                    if affect_rows == 1:
                        return redirect(url_for('Profile',Id=Id))
                    else:
                        flash("invalid upload")
                        return redirect(url_for('Profile',Id=Id))
                else:
                    if Image.filename== '':
                        user=User(Id,Name,Email,Mobile,None,Adress,None,None)
                        affect_rows =UserModel.update_user_profile(user)
                        if affect_rows == 1:
                            return redirect(url_for('Profile',Id=Id))
                        else:
                            flash("invalid upload")
                            return redirect(url_for('Profile',Id=Id))
                    else:
                        if Image.filename == '':
                            flash('No image selected for uploading')
                            return redirect(url_for('Profile',Id=Id))
                        imagefilename=Image.filename
                        Image.save(os.path.join(app.config['UPLOAD_FOLDER'],imagefilename))
                        user=User(Id,Name,Email,Mobile,None,Adress,None,imagefilename)
                        affect_rows =UserModel.update_user_profile(user)
                        if affect_rows == 1:
                            return redirect(url_for('Profile',Id=Id))
                        else:
                            flash("invalid upload")
                            return redirect(url_for('Profile',Id=Id))
            else:
                Id=request.form['LogUsrId']
                return redirect(url_for('Profile',Id=Id)) 
        except Exception as ex:
            return jsonify({'message': str(ex)}), 500
    else:
        Id=request.form['LogUsrId']
        return redirect(url_for('Profile',Id=Id))

@app.route('/update_password',methods=['POST'])
@login_required 
def update_password():
    if request.method == 'POST':
        try:
            Id = request.form['ModUsrId']
            Current_Id=request.form['LogUsrId']
            if Id==Current_Id:
                OldPassword = request.form['Password']
                if UserModel.check_password(OldPassword,Current_Id):
                    NewPassword=request.form['NewPassword']
                    ConfPassword=request.form['ConfPassword']
                    if NewPassword==ConfPassword:
                        NewPassword=convertTuple(NewPassword)
                        NewPassword=User.generate_password(NewPassword)
                        affect_rows =UserModel.update_user_password(NewPassword,Current_Id)
                        if affect_rows == 1:
                         return redirect(url_for('Profile',Id=Id))
                        else:
                             return jsonify({'message': str(ex)}), 500
                    else:
                        flash('New password dont match')
                        return redirect(url_for('Profile',Id=Id))
                else:
                    flash('Password user invalid')
                    return redirect(url_for('Profile',Id=Id))

            else:
                Id=request.form['LogUsrId']
                return redirect(url_for('Profile',Id=Id)) 
        except Exception as ex:
            return jsonify({'message': str(ex)}), 500
    else:
        Id=request.form['LogUsrId']
        return redirect(url_for('Profile',Id=Id))

@app.route('/ManageUsers')
@login_required
def Manage_users():
    users=[]
    users=UserModel.get_users()
    return render_template ('/store/Manage_Users/manage_users.html',queryset=users)

################PRODUCTOS###################

@app.route('/ViewProduct/<Id>')
def View_product(Id):
    try:
        producto=ProductModel.get_product_by_id(Id)
        coment=CommentModel.get_comment_by_product_id(Id)
        return render_template('/store/product.html',product=producto,coment=coment)
    except Exception as ex:
        return print(ex)

@app.route('/ManageProduct')
def Manage_products():
    products=[]
    products=ProductModel.get_products()
    return render_template ('/store/Manage_Products/manage_products.html',queryset=products)

@app.route('/create_product',methods=['GET', 'POST'])
@login_required
def created_product():
    if request.method == 'POST':
        try:         
            name = request.form['Name']
            price = request.form['Price']
            category=request.form['Category']
            description=request.form['Description']
            image=request.form['Image']
            product=Product(uuid.uuid4(),name,price,category,description,image)
            affect_rows = ProductModel.add_product(product)
            if affect_rows == 1:
                return redirect(url_for('Manage_products'))
            else:
                return jsonify({'message': str(ex)}), 500
        except Exception as ex:
            return jsonify({'message': str(ex)}), 500
    else:
        return render_template('/store/Manage_Products/manage_products.html')

@login_required
@app.route('/update_product',methods=['GET', 'POST'])
def update_product():
    if request.method == 'POST':
        try:
            Id = request.form['Id']
            name = request.form['Name']
            price = request.form['Price']
            category=request.form['Category']
            description=request.form['Description']
            image=request.form['Image']
            Id=tuple(map(str, Id.split(', ')))
            product=Product(Id,name,price,category,description,image)
            affect_rows = ProductModel.update_product(product)
            if affect_rows == 1:
                return redirect(url_for('Manage_products'))
            else:
                return jsonify({'message': str(ex)}), 500
        except Exception as ex:
            return jsonify({'message': str(ex)}), 500
    else:
        Id=request.args.get('Id',default='', type=str)
        producto=ProductModel.get_product_by_id(Id)
        return render_template('/store/Manage_Products/Edit.html',producto=producto)

@app.route('/delete_product/<Id>')
@login_required
def delete_product(Id):
        ProductModel.delete_product(Id)
        return redirect(url_for('Manage_products'))

#######################COMENTARIOS###############################
@app.route('/add_comment',methods=['POST'])
@login_required
def add_comment():
    if request.method == 'POST':
        try:         
            comment= request.form['Comment']
            Id_user=request.form['LogUsrId']
            Name=request.form['LogUsrName']
            Date=str(datetime.datetime.now())[:10]
            Id_product=request.form['ProductId']
            Comm=Comment(uuid.uuid4(),comment,Date,Id_user,Id_product,Name)
            affect_rows=CommentModel.add_comment(Comm)
            if affect_rows==1:
                return redirect(url_for('View_product',Id=Id_product))
            else:
                return jsonify({'message': str(ex)}), 500
        except Exception as ex:
            return jsonify({'message': str(ex)}), 500
    else:
        return redirect(url_for('View_product',Id=Id_product))

@app.route('/delete_comment/<Idp>/<Id>')
@login_required
def delete_comment(Idp,Id):
        CommentModel.delete_comment(Id)
        return redirect(url_for('View_product',Id=Idp))

@app.route('/logs')
@login_required
def view_logs():
     with open("registros_app.log",'r') as f:
        content=[line for line in reversed(list(f.readlines()))]
        return render_template('store/logs.html',monitoring=content,content=None)

@app.route('/urltest',methods=['POST'])
@login_required
def UrlTest():
    url=request.form['Url']
    Urlparse=urlparse(url)
    #Tanto para la comparacion y la busqueda de la expresion regular
    # #es recomandable que solo sea el nombre de host para este caso seria
    #"Urlparse.hostname"
    regex=re.compile(r"127.0.0.1:5500$",re.M)
    match=regex.search(Urlparse.hostname)
    if not match:
        return render_template('store/logs.html',alert="Invalid output")
    res=requests.get(url)
    return render_template('store/logs.html',content=res.text.splitlines(),monitoring=None)


@app.route('/ZkRla34Tsxc-V1-test')
def TestV1():
    try:
        users=UserModel.get_users()
        return jsonify(users)
    except Exception as ex:

        return jsonify({'message': str(ex)}),500
        

@app.route('/payment')
@login_required
def do_payment():
    return render_template('/auth/payments.html')

@app.route('/cart')
@login_required
def my_shopping_cart():
    return render_template('/store/cart.html')

@app.route('/orders')
@login_required
def orders():
    return render_template('/store/orders.html')


def not_authorized(error):
    return "<h1>not authorized</h1>", 401
def page_not_found(error):
    return "<h1>Page not found</h1>", 404




if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(401, not_authorized)
    app.run(port=5500)

