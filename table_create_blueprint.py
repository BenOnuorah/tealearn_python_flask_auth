from flask import Blueprint, render_template, request

from database import connect_db
conn = connect_db()

tables_bp=Blueprint("table_create_blueprint", __name__,  template_folder="templates")


#setup the tables in the database
@tables_bp.route('/dbsetup') 
def dbsetup(): 
    #sql_create_student_table='DROP TABLE  IF EXISTS student'
    sql_create_student_table='CREATE TABLE  IF NOT EXISTS student (student_id INTEGER PRIMARY KEY, surname TEXT, other_name TEXT, location_address TEXT, email TEXT, password TEXT)'
    sql_create_admin_table='CREATE TABLE  IF NOT EXISTS admin (admin_id INTEGER PRIMARY KEY, username TEXT, password TEXT)'
    sql_create_instructor_table='CREATE TABLE IF NOT EXISTS instructor (instructor_id INTEGER PRIMARY KEY, surname_name TEXT, other_name TEXT, address_address TEXT, qualification TEXT)'
    sql_create_subject_table='CREATE TABLE IF NOT EXISTS subject (subject_id INTEGER PRIMARY KEY, instructor_id INTEGER, subject_title TEXT, more_detail TEXT, max_score INTEGER)'
    sql_create_score_table='CREATE TABLE IF NOT EXISTS student_score (score_id INTEGER PRIMARY KEY, score_value INTEGER, student_id  INTEGER, subject_id INTEGER)'

    try:
		#use the connection to execute the queries to create the tables
        conn.execute(sql_create_student_table)
        conn.commit()
		
        conn.execute(sql_create_instructor_table)
        conn.commit()
		
        conn.execute(sql_create_subject_table)
        conn.commit()
		
        conn.execute(sql_create_score_table)
        conn.commit()
		
        conn.execute(sql_create_admin_table)
        conn.commit()
        
        output="db setup successful"
    except sqlite3.Error as er:
    	output=er.sqlite_errorname
		
    return render_template('dbsetup.html', msg=output) 