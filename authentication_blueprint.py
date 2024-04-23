from flask import Blueprint, render_template, request, url_for, redirect, session
import re 
import sqlite3 

from database import connect_db
conn = connect_db()

auth_bp=Blueprint("authentication_blueprint", __name__, static_folder="static", template_folder="templates")


@auth_bp.route('/register', methods =['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST':
        surname = request.form['surname']
        other_name = request.form['othernames']
        address = request.form['address']
        email = request.form['email']
        password = request.form['password']

        cursor = conn.cursor() 
        cursor.execute(f"SELECT * FROM student WHERE email = '{email}'  OR password = '{password}' ")
        record = cursor.fetchone()
        if record:
            msg = 'Email or password already registered try again!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not surname or not other_name or not email or not password:
            msg = 'Please fill out the * form fields !'
        else:
            conn.execute(f"INSERT INTO student (surname, other_name, location_address, email, password) VALUES ('{surname}', '{other_name}', '{address}', '{email}', '{password}')")
            conn.commit()
            msg = 'You have successfully registered !'
            return render_template('register.html', msg = msg)
    else:
      return render_template('register.html')
      

@auth_bp.route('/login', methods =['GET', 'POST'])
def login():
    msg = ''
    
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        cursor = conn.cursor() 
        cursor.execute(f"SELECT * FROM student WHERE email = '{email}' AND password = '{password}' ")
        record = cursor.fetchone()
        if record:
            session['loggedin'] = True
            session['id'] = record[0]
            session['login_sname'] = record[1]
            session['login_id'] = record[4] #student email
            session['login_pw'] = record[5] #student pw
            
            #check if login id is email
            if re.match(r'[^@]+@[^@]+\.[^@]+', session['login_id'] ):
              #use is student
               session['level'] = "student"
            else:
              #user is an admin
              session['level'] = "admin"
            
            #redirect to success login URL 
            return redirect(url_for('auth'))
        else:
          msg = 'Incorrect username / password !'
          return render_template('login.html', msg = msg)
    else:
      return render_template('login.html')
      
@auth_bp.route('/logout')
def logout():
    msg = ''
    session.pop('loggedin', None)
    session.pop('login_id', None)
    session.pop('login_pw', None)
    session.pop('level', None)
    msg = 'You have logout now'
    #return redirect(url_for('login'))
    return render_template('login.html', msg = msg)