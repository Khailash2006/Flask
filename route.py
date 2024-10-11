from flask import Blueprint,request,session,render_template,url_for,redirect
from flask_sqlalchemy import SQLAlchemy
import random

db = SQLAlchemy()
auth_user = Blueprint("auth_user",__name__)
library = Blueprint("library",__name__)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(10), nullable=False) 

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(200), nullable=False)
    available = db.Column(db.Boolean, default=True)

@auth_user.route('/register',methods = ['GET','POST'])
def register():
    if request.method == "POST":
        user = request.form.get('name')
        password = request.form.get('password')
        role = request.form.get('role')
        print (user,password,role)
        newuser = User(id = random.randint(1,1000),username = user,password = password,role = role)
        try:
            db.session.add(newuser)
            db.session.commit()
            return "User registered successfully", 201
        except Exception as e:
            db.session.rollback()
            print(f"Error registering user: {e}") 
            return "An error occurred during registration.", 500
    
    else:
        return render_template("register.html")

@auth_user.route('/login', methods=['GET','POST'])
def login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
    
        if user and user.password == password: 
            session['user_id'] = user.id
            return "Login successful",200

        return "Invalid credentials",401
    
    else:
        return render_template("login.html")

@library.route('/addbooks', methods=['GET','POST'])
def addbooks():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
    
        if user and user.password == password: 
            session['user_id'] = user.id
            return "Login successful",200

        return redirect(url_for("library.adddata"))
    
    else:
        return render_template("login.html")
    
@library.route('/adddata', methods=['GET','POST'])
def adddata():
    if request.method == "POST":
        name = request.form.get('name')
        author = request.form.get('author')
        num = request.form.get('stock')
        newlist = Book(id = random.randint(1,1000),title = name,author = author,available = True)
        try:
            db.session.add(newlist)
            db.session.commit()
            return "Book added", 201
        except Exception as e:
            db.session.rollback()
            print(f"Error adding book: {e}")
            return "An error occurred during book addition.", 500
    
    else:
        return render_template("library.html")