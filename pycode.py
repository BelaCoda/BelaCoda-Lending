
from select import select
from tkinter import W
from flask import Flask,redirect,url_for,render_template,request,session
import mysql.connector
from mysqlx import View
from DBcm import UseDatabase
from mysql.connector import MySQLConnection, Error
from nn import read_db_config


app=Flask(__name__)


def execute_login():
    try:
        db_config = read_db_config()
        conn = MySQLConnection(**db_config)
        cursor = conn.cursor()
        cursor.execute("SELECT login FROM userslog;")
        resultlogin = cursor.fetchall()
        cursor.close()
        conn.close() 
        return resultlogin
    except Error as e:
        print("бара бара бара бири бири бири")




def execute_password():
    try:
        db_config = read_db_config()
        conn = MySQLConnection(**db_config)
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM userslog;")
        resultpassword = cursor.fetchall()
        cursor.close()
        conn.close()
        return resultpassword 
    except Error as e:
        print("бара бара бара бири бири бири")



def regestr(l,p):
    data_save = 0
    try:
        db_config = read_db_config()
        conn = MySQLConnection(**db_config)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO userslog (login,password) values (%s,%s);",(l,p))
        conn.commit()
        cursor.close()
        conn.close() 
        return 1
    except mysql.connector.errors.InterfaceError as err:
        print('o no:',str(err))  
        return 0
    
          
    
#здесь выполняется регистрация
@app.route('/r',methods = ['post','get'])
def registrated():
    if request.method == 'POST':
     l = request.form.get('l')
     p = request.form.get('p')
     datasave =  regestr(l,p)
     if datasave == 1:
        session['logged_in'] = True
        return  render_template('w.html',the_title = 'wiew',the_welcom = l,)
     else:
        return render_template('r.html',the_title = 'registr error',the_incorect = 'ooops,error:(')
    return render_template('r.html',the_title = 'registr')
    

@app.route('/start')
def start():
    if 'logged_in' in session:
        return render_template('w.html',the_title = 'start wiew')
    else:
        return render_template('index.html',the_title = 'start')
    return render_template('index.html',the_title = 'start')


@app.route('/start again')
def start_again():
    
    if 'logged_in' in session:
        session.pop('logged_in')
        return render_template('start.html',the_title = 'start again')


    return render_template('start.html',the_title = 'start again')


@app.route('/w')
def wiew():
    if 'logged_in' in session:
        return render_template('w.html',the_title = 'wiew')
    else:
        return render_template('l.html',the_title = 'view log',the_header = 'LOGIN')#нужно сделать кнопку ИЛИ ЗАРЕГИТМРИРОВАТЬСЯ   
    return render_template('w.html',the_title = 'wiew')

    
#здесь выполняется вход
@app.route('/l',methods = ['post','get'])
def login2():
    login = execute_login()
    password = execute_password()
    login_list = list(sum(login,()))
    password_list = list(sum(password,()))
    if request.method == 'POST':
     ll = request.form.get('ll')
     pp = request.form.get('pp')
     if (ll in login_list and pp in password_list):
         session['logged_in'] = True
         return render_template('w.html',the_title = 'goood login',the_welcom = ll,)
     else:
        return render_template('l.html',the_title = 'login again',the_header = 'LOGIN AGAIN', the_incorect = 'incorect login or password')

    return render_template('l.html',the_title = 'log',the_header = 'LOGIN')



app.secret_key = 'COHhpoey7-duf7Yu'


if __name__ == '__main__':
    app.run(debug=True)