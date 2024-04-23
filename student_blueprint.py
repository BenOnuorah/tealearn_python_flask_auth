from flask import Blueprint, render_template, request, url_for, redirect, session
import re 
import sqlite3 

from database import connect_db
conn = connect_db()

student_bp=Blueprint("student_blueprint", __name__, static_folder="static", template_folder="templates")

#load form
@student_bp.route('/student', methods =['GET']) 
def student():
  args = request.args
  msg=''
  if 'task' in args: #check if in edit mode    
    sel_id = args.get('value')  

    cursor = conn.cursor() 
    cursor.execute('SELECT * FROM student WHERE id = "'+sel_id+'"')  
    data_preview = cursor.fetchone()            
    msg="Edit"
    return render_template('student.html', preview=data_preview)
  else: # else load add mode      
	  return render_template('student.html')

#display record
@student_bp.route('/seestudents') 
def seestudents():	 

  cursor = conn.cursor()  
  cursor.execute('SELECT * FROM student')
  data = cursor.fetchall()

  return render_template('seestudents.html', students=data)
	 
#process the student add
@student_bp.route('/addstudent', methods=['GET', 'POST']) 
def addstudent(): 
  if request.method == 'POST': 
    surname = request.form['surname'] 
    othernames = request.form['othernames'] 
    address = request.form['address']  

    if "edit_id" in request.form: # Edit Record
      edit_id = request.form['edit_id'] 
      conn.execute('UPDATE student SET surname_name="'+surname+'", other_name="'+othernames+'", address_address="'+address+'" WHERE id = "'+edit_id+'"')              
      conn.commit()
        
      return redirect('student?task=edit&value='+edit_id+'&done=1')

    else: #Add  Record 
      conn.execute('INSERT INTO student (surname_name,other_name,address_address) VALUES (?,?,?)',(surname, othernames, address)) 
      conn.commit() 
    
      output="Student record saved"
      return render_template('student.html', msg=output) 


@student_bp.route('/delete_student', methods =['GET'])
def delete():
  if 'loggedin' in session and session['level']=="admin":
    args = request.args
    sel_id = args.get('value')
   
   
    conn.execute('DELETE FROM student WHERE id = "'+sel_id+'"')              
    conn.commit()
    
    #returning back to seestudents 
    return redirect(url_for('student_blueprint.seestudents'))  
  else:
        return redirect(url_for('login'))