import sqlite3 

def connect_db():
		#create and connect to the database
		conn = sqlite3.connect('tealearn_grades.db', check_same_thread=False) 
		return conn