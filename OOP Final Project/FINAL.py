import customtkinter
import sqlite3
import bcrypt
from tkinter import ttk
from tkinter import *
import tkinter as tk
from tkinter import messagebox
import FPDatabase
import FPMedInfo
from PIL import Image, ImageTk

main_app = customtkinter.CTk()
main_app.title('Electronic Medical Record System')
main_app.geometry('1280x690')
main_app.config(bg='#161C25')
main_app.resizable(False, False)

font1 = ('Arial', 20, 'bold')
font2 = ('Arial', 12, 'bold')
font3 = ('Arial', 15)
font4 = ('Arial', 15, 'bold')


def initialize_database():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def open_main_window():
    def add_to_treeview():

        EMR = FPDatabase.fetch_EMR()
        tree.delete(*tree.get_children())
        for data in EMR:
            tree.insert('', 'end', values=data)

    def clear(clear_selection=False):

        if clear_selection:
            tree.selection_remove(tree.focus())
            tree.focus('')
        id_entry.delete(0, 'end')
        name_entry.delete(0, 'end')
        role_entry.delete(0, 'end')
        gender_var.set('Male')
        marital_status_entry.delete(0, 'end')
        age_entry.delete(0, 'end')
        dob_entry.delete(0, 'end')
        home_address_entry.delete(0, 'end')
        email_entry.delete(0, 'end')

    def display_data(event):

        selected_item = tree.focus()
        if selected_item:
            row = tree.item(selected_item)['values']
            clear()
            id_entry.insert(0, row[0])
            name_entry.insert(0, row[1])
            role_entry.insert(0, row[2])
            gender_var.set(row[3])
            marital_status_entry.insert(0, row[4])
            age_entry.insert(0, row[5])
            dob_entry.insert(0, row[6])
            home_address_entry.insert(0, row[7])
            email_entry.insert(0, row[8])

    def delete():
        selected_item=tree.selection()
        if not selected_item:
            messagebox.showerror('ERROR', 'Choose a Patient Data to delete.') 
        else:
            id = id_entry.get()
            FPDatabase.delete_EMR(id,)
            add_to_treeview()
            clear()
            messagebox.showinfo('Success', 'Data has been deleted')

    def update():

        selected_item = tree.focus()
        if not selected_item:
            messagebox.showerror('Error', 'Select an patient to update.')
        else:
            id = id_entry.get()
            name = name_entry.get()
            role = role_entry.get()
            gender = gender_var.get()
            marital_status = marital_status_entry.get()
            age = age_entry.get()
            dob = dob_entry.get()
            home_address = home_address_entry.get()
            email = email_entry.get()
            FPDatabase.update_EMR(name, role, gender, id, marital_status, age, dob, home_address, email)
            add_to_treeview()
            clear()
            messagebox.showinfo('Success', 'Patient Data has been updated.')

    def insert():

        id = id_entry.get()
        name = name_entry.get()
        role = role_entry.get()
        gender = gender_var.get()
        marital_status = marital_status_entry.get()
        age = age_entry.get()
        dob = dob_entry.get()
        home_address = home_address_entry.get()
        email = email_entry.get()

        if not (id and name and role and gender and marital_status and age and dob and home_address and email):
            messagebox.showerror('Error', 'Enter all fields.')
        elif FPDatabase.id_exists(id):
            messagebox.showerror('Error', 'ID already exists.')
        else:
            FPDatabase.insert_EMR(id, name, role, gender, marital_status, age, dob, home_address, email)
            add_to_treeview()
            messagebox.showinfo('Success', 'Data has been inserted.')

    id_label = customtkinter.CTkLabel(main_app, font=font1, text='ID:', text_color='#fff', bg_color='#161C25')
    id_label.place(x=20, y=30)
    id_entry = customtkinter.CTkEntry(main_app, font=font1, text_color='#000', fg_color='#fff', border_width=2, width=180)
    id_entry.place(x=100, y=20)

    name_label = customtkinter.CTkLabel(main_app, font=font1, text='NAME:', text_color='#fff', bg_color='#161C25')
    name_label.place(x=20, y=80)
    name_entry = customtkinter.CTkEntry(main_app, font=font1, text_color='#000', fg_color='#fff', border_width=2, width=180)
    name_entry.place(x=100, y=80)

    role_label = customtkinter.CTkLabel(main_app, font=font1, text='ROLE:', text_color='#fff', bg_color='#161C25')
    role_label.place(x=20, y=140)
    role_entry = customtkinter.CTkEntry(main_app, font=font1, text_color='#000', fg_color='#fff', border_width=2, width=180)
    role_entry.place(x=100, y=140)

    gender_label = customtkinter.CTkLabel(main_app, font=font1, text='GENDER:', text_color='#fff', bg_color='#161C25')
    gender_label.place(x=20, y=200)

    age_label = customtkinter.CTkLabel(main_app, font=font1, text='AGE:', text_color='#fff', bg_color='#161C25')
    age_label.place(x=20, y=260)
    age_entry = customtkinter.CTkEntry(main_app, font=font1, text_color='#000', fg_color='#fff', border_width=2, width=180)
    age_entry.place(x=100, y=260)

    marital_status_label = customtkinter.CTkLabel(main_app, font=font1, text='MARITAL STATUS:', text_color='#fff', bg_color='#161C25')
    marital_status_label.place(x=20, y=320)
    marital_status_entry = customtkinter.CTkEntry(main_app, font=font1, text_color='#000', fg_color='#fff', border_width=2, width=180)
    marital_status_entry.place(x=210, y=320)

    dob_label = customtkinter.CTkLabel(main_app, font=font1, text='DATE OF BIRTH:', text_color='#fff', bg_color='#161C25')
    dob_label.place(x=20, y=380)
    dob_entry = customtkinter.CTkEntry(main_app, font=font1, text_color='#000', fg_color='#fff', border_width=2, width=180)
    dob_entry.place(x=190, y=380)

    home_address_label = customtkinter.CTkLabel(main_app, font=font1, text='HOME ADDRESS:', text_color='#fff', bg_color='#161C25')
    home_address_label.place(x=20, y=440)
    home_address_entry = customtkinter.CTkEntry(main_app, font=font1, text_color='#000', fg_color='#fff', border_width=2, width=180)
    home_address_entry.place(x=210, y=440)

    email_label = customtkinter.CTkLabel(main_app, font=font1, text='EMAIL:', text_color='#fff', bg_color='#161C25')
    email_label.place(x=20, y=500)
    email_entry = customtkinter.CTkEntry(main_app, font=font1, text_color='#000', fg_color='#fff', border_width=2, width=180)
    email_entry.place(x=105, y=500)

    options = ['Male', 'Female']
    gender_var = StringVar()
    gender_options = customtkinter.CTkComboBox(main_app, font=font1, text_color='#000', fg_color='#fff', dropdown_hover_color='#0C9295', button_color='#0C9295', button_hover_color='#0C9295', border_color='#0C9295', width=180, variable=gender_var, values=options, state='readonly')
    gender_options.set('Male')
    gender_options.place(x=130, y=200)

    add_button = customtkinter.CTkButton(main_app, command=insert, font=font1, text_color='#fff', text='Add Patient Data', fg_color='#05A312', hover_color='#00850B', bg_color='#161C25', cursor='hand2', corner_radius=5, width=210)
    add_button.place(x=590, y=455)

    clear_button = customtkinter.CTkButton(main_app, command=lambda: clear(True), font=font1, text_color='#fff', text='New Entry', fg_color='#05A312', hover_color='#00850B', bg_color='#161C25', cursor='hand2', corner_radius=5, width=175)
    clear_button.place(x=410, y=455)

    update_button = customtkinter.CTkButton(main_app, command=update, font=font1, text_color='#fff', text='Update Patient Data', fg_color='#05A312', hover_color='#00850B', bg_color='#161C25', cursor='hand2', corner_radius=5, width=210)
    update_button.place(x=805, y=455)

    delete_button = customtkinter.CTkButton(main_app, command=delete, font=font1, text_color='#fff', text='Delete Patient Data', fg_color='#D52914', hover_color='#A31504', bg_color='#161C25', cursor='hand2', corner_radius=5, width=210)
    delete_button.place(x=1025, y=455)

    new_window_button = customtkinter.CTkButton(main_app, text='Access Medical Information', command=med_info, font=font1, text_color='#000000', fg_color='#FFFF00', hover_color='#00850B', bg_color='#161C25', cursor='hand2', corner_radius=5, width=330)
    new_window_button.place(x=620, y=550) 

    tree_frame = customtkinter.CTkFrame(main_app, width=1000, height=400, fg_color='#fff', bg_color='#fff', corner_radius=5)
    tree_frame.place(x=410, y=50)

    style = ttk.Style(main_app)
    style.theme_use('clam')
    style.configure('Treeview.Heading', background='#161C25', font=font2, foreground='white')
    style.configure('Treeview', font=('Arial', 13), rowheight=30, foreground='#000', background='#fff')

    tree = ttk.Treeview(tree_frame, columns=('ID', 'Name', 'Role', 'Gender', 'Marital Status', 'Age', 'DOB', 'Home Address', 'Email'), show='headings', height=15)
    tree.column('ID', anchor=tk.CENTER, width=50)
    tree.column('Name', anchor=tk.CENTER, width=150)
    tree.column('Role', anchor=tk.CENTER, width=100)
    tree.column('Gender', anchor=tk.CENTER, width=100)
    tree.column('Marital Status', anchor=tk.CENTER, width=120)
    tree.column('Age', anchor=tk.CENTER, width=50)
    tree.column('DOB', anchor=tk.CENTER, width=120)
    tree.column('Home Address', anchor=tk.CENTER, width=150)
    tree.column('Email', anchor=tk.CENTER, width=150)

    tree.heading('ID', text='ID')
    tree.heading('Name', text='Name')
    tree.heading('Role', text='Role')
    tree.heading('Gender', text='Gender')
    tree.heading('Marital Status', text='Civil Status')
    tree.heading('Age', text='Age')
    tree.heading('DOB', text='Date of Birth')
    tree.heading('Home Address', text='Home Address')
    tree.heading('Email', text='Email')

    tree.pack(side=tk.LEFT, fill=tk.Y)
    scrollbar = customtkinter.CTkScrollbar(tree_frame, command=tree.yview, fg_color='#161C25', bg_color='#161C25', button_color='#0C9295', button_hover_color='#0C9295')
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    tree.config(yscrollcommand=scrollbar.set)

    tree.bind('<<TreeviewSelect>>', display_data)

    add_to_treeview()

    '''def close_main_window():
        med_info()
        main_app.destroy()'''

    main_app.mainloop()

def med_info():
    med_info = customtkinter.CTk()
    med_info.title('Medial Information')
    med_info.geometry('1180x700')
    med_info.config(bg='#161C25')
    med_info.resizable(False, False)

    font1 = ('Arial', 20, 'bold')
    font2 = ('Arial', 12, 'bold')
    font3 = ('Arial', 15)
    font4 = ('Arial', 15, 'bold')

    def add_to_treeview():
        medrec = FPMedInfo.fetch_MedInfo()
        tree.delete(*tree.get_children())
        for data in medrec:
            tree.insert('', 'end', values=data)

    def clear(clear_selection=False):
        if clear_selection:
            tree.selection_remove(tree.focus())
            tree.focus('')
        patient_id_entry.delete(0, 'end')
        attending_physician_entry.delete(0, 'end')
        diagnosis_entry.delete(0, 'end')
        blood_type_entry.delete(0, 'end')
        medical_history_entry.delete(0, 'end')
        allergies_entry.delete(0, 'end')
        date_of_first_visit_entry.delete(0, 'end')

    def display_data(event):
        selected_item = tree.focus()
        if selected_item:
            row = tree.item(selected_item)['values']
            clear()
            patient_id_entry.insert(0, row[0])
            date_of_first_visit_entry.insert(0, row[1])
            attending_physician_entry.insert(0, row[2])
            blood_type_entry.insert(0, row[3])
            diagnosis_entry.insert(0, row[4])
            medical_history_entry.insert(0, row[5])
            allergies_entry.insert(0, row[6])

    def delete():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showerror('ERROR', 'Choose a Patient Data to delete.')
        else:
            id = patient_id_entry.get()
            FPMedInfo.delete_MedInfo(id)
            add_to_treeview()
            clear()
            messagebox.showinfo('Success', 'Data has been deleted')

    def update():
        selected_item = tree.focus()
        if not selected_item:
            messagebox.showerror('Error', 'Select a patient to update.')
        else:
            patient_id = patient_id_entry.get()
            date_of_first_visit = date_of_first_visit_entry.get()
            attending_physician = attending_physician_entry.get()
            diagnosis = diagnosis_entry.get()
            blood_type = blood_type_entry.get()
            medical_history = medical_history_entry.get()
            allergies = allergies_entry.get()
            FPMedInfo.update_MedInfo(patient_id, date_of_first_visit, attending_physician, blood_type, diagnosis, medical_history, allergies)
            add_to_treeview()
            clear()
            messagebox.showinfo('Success', 'Patient Data has been updated.')

    def insert():
        pt = patient_id_entry.get()
        date_of_first_visit = date_of_first_visit_entry.get()
        attending_physician = attending_physician_entry.get()
        diagnosis = diagnosis_entry.get()
        blood_type = blood_type_entry.get()
        medical_history = medical_history_entry.get()
        allergies = allergies_entry.get()

        print(f"Blood Type: {blood_type}")

        if not pt:
            messagebox.showerror('Error', 'Patient ID is required.')
            return

        if FPMedInfo.id_exists(pt):
            messagebox.showerror('Error', 'ID already exists.')
        else:
            FPMedInfo.insert_MedInfo(pt, date_of_first_visit, attending_physician, diagnosis, blood_type, medical_history, allergies)
            add_to_treeview()
            clear()
            messagebox.showinfo('Success', 'Data has been inserted.')

    patient_id_label = customtkinter.CTkLabel(med_info, font=font3, text='Patient ID:', text_color='#fff', bg_color='#161C25')
    patient_id_label.place(x=20, y=18)
    patient_id_entry = customtkinter.CTkEntry(med_info, font=font3, text_color='#000', fg_color='#fff', border_width=2, width=180)
    patient_id_entry.place(x=145, y=18)

    date_of_first_visit_label = customtkinter.CTkLabel(med_info, font=font3, text='Date of first Visit:', text_color='#fff', bg_color='#161C25')
    date_of_first_visit_label.place(x=20, y=55)
    date_of_first_visit_entry = customtkinter.CTkEntry(med_info, font=font3, text_color='#000', fg_color='#fff', border_width=2, width=180)
    date_of_first_visit_entry.place(x=145, y=55)

    attending_physician_label = customtkinter.CTkLabel(med_info, font=font3, text='Attending Physician:', text_color='#fff', bg_color='#161C25')
    attending_physician_label.place(x=20, y=90)
    attending_physician_entry = customtkinter.CTkEntry(med_info, font=font3, text_color='#000', fg_color='#fff', border_width=2, width=180)
    attending_physician_entry.place(x=160, y=90)

    diagnosis_label = customtkinter.CTkLabel(med_info, font=font4, text='Diagnosis:', text_color='#fff', bg_color='#161C25')
    diagnosis_label.place(x=20, y=120)
    diagnosis_entry = customtkinter.CTkEntry(med_info, font=font3, text_color='#000', fg_color='#fff', border_width=2, width=335, height=140)
    diagnosis_entry.place(x=20, y=147)

    blood_type = customtkinter.CTkLabel(med_info, font=font3, text='Blood Type:', text_color='#fff', bg_color='#161C25')
    blood_type.place(x=20, y=300)
    blood_type_entry = customtkinter.CTkEntry(med_info, font=font3, text_color='#000', fg_color='#fff', border_width=2, width=90)
    blood_type_entry.place(x=120, y=300)
   
    medical_history_label = customtkinter.CTkLabel(med_info, font=font3, text='Medical History:', text_color='#fff', bg_color='#161C25')
    medical_history_label.place(x=20, y=335)
    medical_history_entry = customtkinter.CTkEntry(med_info, font=font3, text_color='#000', fg_color='#fff', border_width=2, width=335, height=150)
    medical_history_entry.place(x=20, y=365)

    allergies_label = customtkinter.CTkLabel(med_info, font=font3, text='Allergies:', text_color='#fff', bg_color='#161C25')
    allergies_label.place(x=20, y=520)
    allergies_entry = customtkinter.CTkEntry(med_info, font=font3, text_color='#000', fg_color='#fff', border_width=2, width=335, height=110)
    allergies_entry.place(x=20, y=550)

    add_button = customtkinter.CTkButton(med_info, command=insert, font=font1, text_color='#fff', text='Add Patient Data', fg_color='#05A312', hover_color='#00850B', bg_color='#161C25', cursor='hand2', corner_radius=5, width=260)
    add_button.place(x=400, y=475)

    clear_button = customtkinter.CTkButton(med_info, command=lambda: clear(True), font=font1, text_color='#fff', text='New Entry', fg_color='#05A312', hover_color='#00850B', bg_color='#161C25', cursor='hand2', corner_radius=5, width=260)
    clear_button.place(x=400, y=520)

    update_button = customtkinter.CTkButton(med_info, command=update, font=font1, text_color='#fff', text='Update Patient Data', fg_color='#05A312', hover_color='#00850B', bg_color='#161C25', cursor='hand2', corner_radius=5, width=260)
    update_button.place(x=680, y=475)

    delete_button = customtkinter.CTkButton(med_info, command=delete, font=font1, text_color='#fff', text='Delete Patient Data', fg_color='#D52914', hover_color='#A31504', bg_color='#161C25', cursor='hand2', corner_radius=5, width=260)
    delete_button.place(x=680, y=520)
    
    listbox_frame = customtkinter.CTkFrame(med_info, width=900, height=400, fg_color='#fff', bg_color='#fff', corner_radius=5)
    listbox_frame.place(x=440, y=50)

    style = ttk.Style(med_info)
    style.theme_use('clam')
    style.configure('Treeview.Heading', background='#161C25', font=font2, foreground='white')
    style.configure('Treeview', font=('Arial', 13), rowheight=30, foreground='#000', background='#fff')

    tree = ttk.Treeview(listbox_frame, columns=('Patient ID', 'Date of First Visit', 'Attending Physician', 'Blood Type', 'Diagnosis', 'Medical History', 'Allergies'), show='headings', height = 15)
    tree.column('Patient ID', anchor=tk.CENTER, width=100)
    tree.column('Date of First Visit', anchor=tk.CENTER, width=120)
    tree.column('Attending Physician', anchor=tk.CENTER, width=150)
    tree.column('Blood Type', anchor=tk.CENTER, width=90)
    tree.column('Diagnosis', anchor=tk.CENTER, width=100)
    tree.column('Medical History', anchor=tk.CENTER, width=100)
    tree.column('Allergies', anchor=tk.CENTER, width=100)

    tree.heading('Patient ID', text='Patient ID')
    tree.heading('Date of First Visit', text='Date of First Visit')
    tree.heading('Attending Physician', text='Attending Physician')
    tree.heading('Blood Type', text='Blood Type')
    tree.heading('Diagnosis', text='Diagnosis')
    tree.heading('Medical History', text='Medical History')
    tree.heading('Allergies', text='Allergies')

    tree.pack(side=tk.LEFT, fill=tk.Y)
    scrollbar = customtkinter.CTkScrollbar(listbox_frame, command=tree.yview, fg_color='#161C25', bg_color='#161C25', button_color='#0C9295', button_hover_color='#0C9295')
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    tree.config(yscrollcommand=scrollbar.set)

    add_to_treeview()
    tree.bind('<<TreeviewSelect>>', display_data)

    def close_new_window():
        med_info.destroy()

    close_button = customtkinter.CTkButton(med_info, text='Close', command=close_new_window)
    close_button.place(x=1000, y=650)

    med_info.mainloop()

def login_account():
    username = username_entry.get()
    password = password_entry.get().encode('utf-8')

    if not (username and password):  
        messagebox.showerror('Login Error', 'Please enter both username and password')
        return

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE email = ?', (username,))
    user = cursor.fetchone()
    conn.close()

    if user and bcrypt.checkpw(password, user[2]):
        messagebox.showinfo('Login', 'Login successful!')
        app.destroy() 
        open_main_window()
    else:
        messagebox.showerror('Error', 'Invalid username or password')

def create_account():
    email = username_entry.get() 
    password = password_entry.get().encode('utf-8')  

    hashed = bcrypt.hashpw(password, bcrypt.gensalt())

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
    if cursor.fetchone():
        messagebox.showerror('Signup Error', 'Invalid email or password')
    else:
        cursor.execute('INSERT INTO users (email, password) VALUES (?, ?)', (email, hashed))
        conn.commit()
        conn.close()
        messagebox.showinfo('Success', 'Account created successfully! Please log in.')
       
        username_entry.delete(0, 'end')  
        password_entry.delete(0, 'end')  


app = customtkinter.CTk()
app.title('Sign up/Login')
app.geometry('450x360')
app.config(bg=None)
app.resizable(False, False)

font1 = ('Calibri', 25)
font2 = ('Calibri', 17)
font3 = ('Calibri', 13)
font4 = ('Calibri', 13)

conn = sqlite3.connect('data.db')
cursor = conn.cursor()

cursor.execute('''
            CREATE TABLE IF NOT EXISTS users(
              username TEXT NOT NULL,
              password TEXT NOT NULL)''')

def signup():
    username = username_entry.get()
    password = password_entry.get()
    if username != '' and password != '':
        cursor.execute('SELECT username FROM users WHERE username=?', [username])
        if cursor.fetchone() is not None:
            messagebox.showerror('Error', 'Username already exists')
        else:
            encoded_password = password.encode('utf-8')
            hashed_password = bcrypt.hashpw(encoded_password, bcrypt.gensalt())
            cursor.execute('INSERT INTO users VALUES (?, ?)', [username, hashed_password])
            conn.commit()
            messagebox.showinfo('Success', 'Account has been created.')
    else:
        messagebox.showerror('Error', 'Enter all data!')

def login_account():
    username = username_entry2.get()
    password = password_entry2.get()
    if username != '' and password != '':
        cursor.execute('SELECT password FROM users WHERE username=?', [username])
        result = cursor.fetchone()
        if result:
            if bcrypt.checkpw(password.encode('utf-8'), result[0]):
                messagebox.showinfo('Success', 'Logged in successfully')
                app.destroy()
                open_main_window()
            else:
                messagebox.showerror('Error', 'Invalid password')
        else:
            messagebox.showerror('Error', 'Invalid Username')
    else:
        messagebox.showerror('Error', 'Enter all data!')

def login():
    if 'frame1' in globals():
        frame1.destroy() 

    global frame2
    frame2 = customtkinter.CTkFrame(app, bg_color='#d6f5ff', fg_color='#d6f5ff', width=470, height=360)
    frame2.place(x=0, y=0)

    login_label2 = customtkinter.CTkLabel(frame2, font=font1, text='Log In', text_color='#000000', bg_color='#d6f5ff')
    login_label2.place(x=200, y=80)

    global username_entry2
    global password_entry2

    
    username_entry2 = customtkinter.CTkEntry(frame2, font=font2, text_color='#000000', fg_color='#6dceed', bg_color='#6dceed', border_color='#000000', border_width=1, placeholder_text='Username', placeholder_text_color='#3e4d4f', width=200, height=50)
    username_entry2.place(x=(470-200)/2, y=120)

    password_entry2 = customtkinter.CTkEntry(frame2, font=font2, show='*', text_color='#000000', fg_color='#6dceed', bg_color='#6dceed', border_color='#000000', border_width=1, placeholder_text='Password', placeholder_text_color='#3e4d4f', width=200, height=50)
    password_entry2.place(x=(470-200)/2, y=190)

    login_button2 = customtkinter.CTkButton(frame2, command=login_account, font=font4, text='Login', text_color='#000000', bg_color='#d6f5ff')
    login_button2.place(x=170, y=250)


    
frame1 = customtkinter.CTkFrame(app, bg_color='#d6f5ff', fg_color='#d6f5ff', width=470, height=360)
frame1.place(x=0, y=0)

#image1 = Image.open("Sign up.png")
#image1 = image1.resize((180, 200), Image.Resampling.LANCZOS)
#image1 = ImageTk.PhotoImage(image1)

#image_label1 = customtkinter.CTkLabel(frame1, image=image1, text='')
#image_label1.place(x=30, y=50)

#image2 = Image.open("EMR.png")
#image2 = image2.resize((150, 150), Image.Resampling.LANCZOS)
#image2 = ImageTk.PhotoImage(image2)

#image_label2 = customtkinter.CTkLabel(frame1, image=image2, text='')
#image_label2.place(x=30, y=220)

#signup_label = customtkinter.CTkLabel(frame1, font=font1, text='Sign up', text_color='#000000', bg_color='#d6f5ff')
#signup_label.place(x=275, y=20)

username_entry = customtkinter.CTkEntry(frame1, font=font2, text_color='#000000', fg_color='#6dceed', bg_color='#6dceed', border_color='#000000', border_width=1, placeholder_text='Username', placeholder_text_color='#3e4d4f', width=200, height=50)
username_entry.place(x=220, y=90)

password_entry = customtkinter.CTkEntry(frame1, font=font2, show='*', text_color='#000000', fg_color='#6dceed', bg_color='#6dceed', border_color='#000000', border_width=1, placeholder_text='Password', placeholder_text_color='#3e4d4f', width=200, height=50)
password_entry.place(x=220, y=160)

signup_button = customtkinter.CTkButton(frame1, command=signup, font=font2, text_color='#000000', text='Sign up', fg_color='#00965d', hover_color='#006e44', bg_color='#ffffff', cursor='hand2', corner_radius=5, width=120)
signup_button.place(x=220, y=240)

login_label = customtkinter.CTkLabel(frame1, font=font3, text='Already have an account?', text_color='#000000', bg_color='#d6f5ff')
login_label.place(x=220, y=290)

login_button = customtkinter.CTkButton(frame1, command=login, font=font4, text='Login', text_color='#000000', bg_color='#d6f5ff')
login_button.place(x=215, y=320)

app.mainloop()