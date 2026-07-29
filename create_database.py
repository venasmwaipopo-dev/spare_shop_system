import sqlite3


conn = sqlite3.connect("database.db")

cursor = conn.cursor()



cursor.execute("""
CREATE TABLE IF NOT EXISTS users (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    username TEXT UNIQUE NOT NULL,

    password TEXT NOT NULL,

    fullname TEXT,

    role TEXT DEFAULT 'Owner'

)
""")


cursor.execute("""
INSERT INTO users
(username,password,fullname,role)

VALUES
('admin','12345','Juma Mussa','Owner')
""")


conn.commit()

conn.close()


print("Database created successfully")