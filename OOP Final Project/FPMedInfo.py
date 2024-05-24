import sqlite3

def med_database():
    conn = sqlite3.connect('med.db')
    cursor = conn.cursor()

    cursor.execute('''
            CREATE TABLE IF NOT EXISTS med(
            patient_id TEXT PRIMARY KEY,
            date TEXT,
            attending TEXT,
            diagnosis TEXT,
            btype TEXT,
            medhistory TEXT,
            allergies TEXT)''')
    conn.commit()
    conn.close()

def fetch_MedInfo():
    conn =sqlite3.connect('med.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM med')
    employees= cursor.fetchall()
    conn.close()
    return employees

def insert_MedInfo(patient_id, date_of_first_visit, attending_physician, diagnosis,  blood_type, medical_history, allergies):
    conn =sqlite3.connect('med.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO med (patient_id, date, attending, btype, diagnosis, medhistory, allergies) VALUES (?, ?, ?, ?, ?, ?, ?) ',
                   (patient_id, date_of_first_visit, attending_physician, blood_type, diagnosis, medical_history, allergies))
    conn.commit()
    conn.close()

def delete_MedInfo(id):
    conn = sqlite3.connect('med.db')
    cursor =conn.cursor()
    cursor.execute('DELETE FROM med WHERE id=(?)', (id,))
    conn.commit()
    conn.close()

def update_MedInfo(patient_id, new_date_of_first_visit, new_attending_physician, new_blood_type, new_diagnosis, new_medical_history, new_allergies):
    conn =sqlite3.connect('med.db')
    cursor =conn.cursor()
    cursor.execute("UPDATE med SET name =?, role=?, gender =?, maritalstat=?, age=?, DoB=?, Hadrress=?, email=? WHERE patient_id=?",
                   (new_date_of_first_visit, new_attending_physician, new_blood_type, new_diagnosis, new_medical_history, new_allergies, patient_id))
    conn.commit()
    conn.close()

def id_exists(id):
    conn =sqlite3.connect('med.db')
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM med WHERE patient_id = ?', (id,))
    result=cursor.fetchone()
    conn.close()
    return result[0] > 0 

med_database()