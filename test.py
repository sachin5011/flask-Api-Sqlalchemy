import mysql.connector

conn = mysql.connector.connect(user='admin', password='admin', host='localhost', port=3306, database='adv_works')
print("success")
cursor = conn.cursor()
cursor.execute("SELECT * from accessibility_view")
data = cursor.fetchall()

for i in data:
    print(i)