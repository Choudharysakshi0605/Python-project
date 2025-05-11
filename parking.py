import mysql.connector
con=mysql.connector.connect(host='localhost',password='sakshi2002',user='root',database="parking")
if con.is_connected():
   print("connection established")
mycursor=con.cursor()   
mycursor.execute("select * from parking_entries")
for i in mycursor:
   print(i)
