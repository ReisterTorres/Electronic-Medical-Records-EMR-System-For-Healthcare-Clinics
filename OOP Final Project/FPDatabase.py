import sqlite3

def create_table():
    conn = sqlite3.connect('EMR.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS EMR(
            id TEXT PRIMARY KEY,
            name TEXT,
            role TEXT,
            gender TEXT,
            maritalstat TEXT,
            age TEXT,
            DoB TEXT,
            Hadrress TEXT,
            email TEXT)''')
    conn.commit()
    conn.close()

def fetch_EMR():
    conn = sqlite3.connect('EMR.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM EMR')
    employees = cursor.fetchall()
    conn.close()
    return employees

def insert_EMR(id, name, role, gender, maritalstat, age, DoB, Hadrress, email):
    conn = sqlite3.connect('EMR.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO EMR (id, name, role, gender, maritalstat, age, DoB, Hadrress, email) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
                   (id, name, role, gender, maritalstat, age, DoB, Hadrress, email))
    conn.commit()
    conn.close()

def delete_EMR(id):
    conn = sqlite3.connect('EMR.db')
    cursor = conn.cursor()
    cursor.execute('DELETE from EMR WHERE id=?', (id,))
    conn.commit()
    conn.close()

def update_EMR(new_name, new_role, new_gender, id, new_maritalstat, new_age, new_DoB, new_Hadrress, new_email):
    conn = sqlite3.connect('EMR.db')
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE EMR 
        SET name = ?, role = ?, gender = ?, maritalstat = ?, age = ?, DoB = ?, Hadrress = ?, email = ? 
        WHERE id = ?
    ''', (new_name, new_role, new_gender, new_maritalstat, new_age, new_DoB, new_Hadrress, new_email, id))
    conn.commit()
    conn.close()

def id_exists(id):
    conn = sqlite3.connect('EMR.db')
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM EMR WHERE id = ?', (id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] > 0

create_table()

"""import sqlite3

def create_table():
    conn=sqlite3.connect('EMR.db')
    cursor=conn.cursor()


    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS EMR(
                   id TEXT PRIMARY KEY,
                   name TEXT,
                   role TEXT,
                   gender TEXT,
                   maritalstat TEXT,
                   age TEXT,
                   DoB TEXT,
                   Hadrress TEXT,
                   email TEXT)'''
                   )
    conn.commit()
    conn.close()

def fetch_EMR():
    conn =sqlite3.connect('EMR.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM EMR')
    employees= cursor.fetchall()
    conn.close()
    return employees

def insert_EMR(id, name, role, gender, maritalstat, age, DoB, Hadrress, email):
    conn =sqlite3.connect('EMR.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO EMR (id, name, role, gender, maritalstat, age, DoB, Hadrress, email) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?) ',
                   (id, name, role, gender, maritalstat, age, DoB, Hadrress, email))
    conn.commit()
    conn.close()

def delete_EMR(id):
    conn = sqlite3.connect('EMR.db')
    cursor =conn.cursor()
    cursor.execute('DELETE FROM EMR WHERE id=?', (id,))
    conn.commit()
    conn.close()

def update_EMR(new_name, new_role, new_gender, id, new_maritalstat, new_age,  new_DoB, new_Hadrress, new_email):
    conn =sqlite3.connect('EMR.db')
    cursor =conn.cursor()
    cursor.execute("UPDATE EMR SET name =?, role=?, gender =?, maritalstat=?, age=?, DoB=?, Hadrress=?, email=? WHERE id=?",
                   (new_name, new_role, new_gender, new_maritalstat, new_age, new_DoB, new_Hadrress, new_email, id))
    conn.commit()
    conn.close()

def id_exists(id):
    conn =sqlite3.connect('EMR.db')
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM EMR WHERE id = ?', (id,))
    result=cursor.fetchone()
    conn.close()
    return result[0] > 0 

create_table()"""

                   