import mysql.connector
con=mysql.connector.connect(host='localhost',password='sakshi2002',user='root')
if con.is_connected():
   print("connection established")