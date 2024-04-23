from flask import Flask, render_template, request, session, url_for, redirect
import re 

from database import connect_db
conn = connect_db()

from student_blueprint import student_bp
from table_create_blueprint import tables_bp
from authentication_blueprint import auth_bp

app = Flask(__name__) 
app.secret_key = 'your secret key'

#register blueprints
app.register_blueprint(student_bp)
app.register_blueprint(tables_bp)
app.register_blueprint(auth_bp)

#load the home or index page
@app.route('/home') 
@app.route('/') 
def home(): 
  return render_template('index.html')

#user loggedin URL
@app.route('/auth') 
def auth(): 
  if 'loggedin' in session:
      value=session['login_sname']
      return render_template('auth.html', logname = value)
  else:
      return redirect(url_for('home'))
        
if __name__ == '__main__': 
       app.run(debug=True)