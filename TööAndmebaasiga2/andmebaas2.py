from sqlite3 import *
from sqlite3 import Error
from os import *

def create_connect(path:str):
    connection=None
    try:
        connection=connect(path)
        print("Ühendus on olemas!")
    except Error as e:
        print(f"Tekkis viga: {e}")
    return connection
def execute_query(connection,query):
    try:
        cursor=connection.cursor()
        cursor.execute(query)
        connection.commit()
        print("Tabel on loodud või andmed on sisestatud")
    except Error as e:
        print(f"Tekkis viga: {e}")
def execute_read_query(connection,query):
    cursor=connection.cursor()
    result=None
    try:
        cursor.execute(query)
        result=cursor.fetchall()
        return result
    except Error as e:
        print(f"Tekkis viga: {e}")
def execute_insert_query(connection,data):
    query="INSERT INTO users(Name,Lastname,Age,GenderId) VALUES(?,?,?,?)"
    cursor=connection.cursor()
    cursor.execute(query,data)
    connection.commit()

create_users_table="""
CREATE TABLE IF NOT EXISTS users(
Id INTEGER PRIMARY KEY AUTOINCREMENT,
Name TEXT NOT NULL,
Lastname TEXT NOT NULL,
Age INTEGER NOT NULL,
GenderId INTEGER,
FOREIGN KEY (GenderId) REFERENCES gender (Id)
)
"""
create_gender_table="CREATE TABLE IF NOT EXISTS gender(Id INTEGER PRIMARY KEY AUTOINCREMENT,Nimetus TEXT NOT NULL)"
insert_users="""
INSERT INTO
users(Name,Lastname,Age,GenderId)
VALUES
('Valeria','Allik',17,2),
('Daria','Halchenko',17,2),
('Maxim','Svirilin',18,1),
('Alexandra','Semjonova',16,2)
"""
insert_gender="INSERT INTO gender(Nimetus) VALUES('mees'),('naine')"
select_users="SELECT * from users"
select_users_gender="SELECT users.Name,users.Lastname,gender.Nimetus from users INNER JOIN gender ON users.GenderId=gender.Id"



filename=path.abspath(__file__)
dbdir=filename.rstrip('TööAndmebaasiga2.py')
dbpath=path.join(dbdir,"data.db")
conn=create_connect(dbpath)
execute_query(conn,create_gender_table)
execute_query(conn,insert_gender)
execute_query(conn,create_users_table)
execute_query(conn,insert_users)

insert_user=(input("Eesnimi:"),input("Perenimi"),int(input("Vanus:")),int(input("Sugu:")))
execute_insert_query(conn,insert_user)

users=execute_read_query(conn,select_users)
print("Kautajate tabel 1:")
for user in users:
    print(user)
genders=execute_read_query(conn,select_users_gender)
print("Gender tabel 2:")
for gender in genders:
    print(gender)
