import flask
from flask.globals import session
from app import app
from flask import render_template
from flask import request 
from flask import redirect, url_for 
from datetime import timedelta
import sqlite3
#Pour l'ajout du swagger j'ai confrenter un problème lors de l'ajout de la bibliothème(meme si elle est installer je ne peux l'utiliser)


#code secret pour l'app 
app.secret_key = "didij"
app.permanent_session_lifetime = timedelta(minutes=3)

#route de la page de connexion
@app.route('/connexion', methods = ['POST', 'GET'])
def connexion():
     #recupération des données du formulaire 
     if request.method=='POST':
        name=request.form['email']
        password=request.form['password']
        UserName=request.form['UserName']
        DateDeNaissance=request.form['DateDeNaissance']
        Age=request.form['Age']
        #acces à la base de données 
        conn=sqlite3.connect("patient.db")
        conn.row_factory=sqlite3.Row
        c=conn.cursor()
        #requette pour selectionner les infos necessaires
        c.execute("select * from users where email=?  and password=? and UserName=? and DateDeNaissance=? and Age=?",(name, password, UserName,DateDeNaissance,Age))
        data=c.fetchone()

        #verification des données de la session de l'utilisateur
        if data:
            session["email"]=data["email"]
            session["password"]=data["password"]
            session["UserName"]=data["UserName"]
            session["DateDeNaissance"]=data["DateDeNaissance"]
            session["Age"]=data["Age"]
            #connexion réussie et redirection à l'aspace du patient 
            return redirect("welcome")
        else:
            ##problème lors de la connexion
            print("Username and Password Mismatch","danger")
    
     return render_template('connexion.html')

#route de la page de l'espace patient
@app.route('/welcome', methods = ['POST', 'GET'])
def welcome():              
    return render_template('welcome.html')

    
#route de la page d'inscription 
@app.route('/inscription', methods = ['POST','GET'])
def inscription():
    if request.method == 'POST':
        UserName = request.form['UserName']
        email = request.form['email']
        DateDeNaissance = request.form['DateDeNaissance']
        Age = request.form['Age']
        password = request.form['password'] 
        conn = sqlite3.connect('patient.db')
        c = conn.cursor()
        #création de la base de données 
        c.execute("""CREATE TABLE IF NOT EXISTS users (
                     id INTEGER PRIMARY KEY AUTOINCREMENT,
                     UserName TEXT,
                     email TEXT,
                     password VARCHAR,
                     DateDeNaissance DATE,
                     Age INTEGER
                     );""")
        #insertion des informations dans la base de données 
        c.execute('INSERT INTO users (UserName, email, password, DateDeNaissance, Age) VALUES (?,?,?,?,?)', (UserName,  email, password, DateDeNaissance, Age))
        conn.commit()
        conn.close()
        #redirection vers la page de connexion en cas d'inscription réussie 
        return redirect('/connexion')
    #cas de non inscription 
    return render_template('inscription.html')
    


#route pour la déconnexion
@app.route('/logout')
def logout():
    session.clear()
    return render_template('connexion.html')

@app.route('/',methods = ['POST', 'GET'])
def index():
    if request.method == 'POST' or 'GET':
        #Page de connexion
        return render_template('connexion.html')

