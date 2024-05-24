import customtkinter
import sqlite3
import bcrypt
from tkinter import messagebox
import random
import time
import threading
from PIL import Image, ImageTk

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

def show_final_message():
    final_app = customtkinter.CTk()
    final_app.title('Final Message')
    final_app.geometry('400x200')
    final_app.config(bg='#d6f5ff')

    font1 = ('Arial', 20, 'bold')

    final_label = customtkinter.CTkLabel(final_app, font=font1, text='Your Device has been hacked', text_color='#ff0000', bg_color='#d6f5ff')
    final_label.pack(pady=40)

    quit_button = customtkinter.CTkButton(final_app, text='Quit', command=final_app.destroy, font=font1, fg_color='#ff0000', hover_color='#cc0000', text_color='#ffffff')
    quit_button.pack()

    final_app.mainloop()
    show_claim_window()

def show_thank_you_window():
    thank_you_app = customtkinter.CTk()
    thank_you_app.title('Thank You')
    thank_you_app.geometry('400x400')
    thank_you_app.config(bg='#d6f5ff')

    font1 = ('Arial', 20, 'bold')

    thank_you_label = customtkinter.CTkLabel(thank_you_app, font=font1, text='Thank you for running this practice program\n Also, Thank you sir for teaching us the first steps in programming using Python.', text_color='#000000', bg_color='#d6f5ff')
    thank_you_label.pack(pady=20)

    image = Image.open('Picture.png')
    image = image.resize((200, 200), Image.Resampling.LANCZOS)
    image = ImageTk.PhotoImage(image)

    image_label = customtkinter.CTkLabel(thank_you_app, image=image, text='')
    image_label.pack(pady=10)

    ok_button = customtkinter.CTkButton(thank_you_app, text='OK', command=lambda: [thank_you_app.destroy(), show_final_message()], font=font1, fg_color='#05A312', hover_color='#00850B', text_color='#ffffff')
    ok_button.pack(pady=10)

    thank_you_app.mainloop()

def move_button_randomly(button, start_time):
    elapsed_time = time.time() - start_time
    if elapsed_time >= 15:
        messagebox.showinfo('Data Transfer', 'All data will transfer to my computer. Thank you for participating.')
        root.destroy()
        return
    x = random.randint(0, root.winfo_width() - button.winfo_width())
    y = random.randint(0, root.winfo_height() - button.winfo_height())
    button.place(x=x, y=y)
    root.after(1000, move_button_randomly, button, start_time)

def show_claim_window():
    global root
    root = customtkinter.CTk()
    root.title('Claim Your Prize')
    root.geometry('500x500')
    root.config(bg='#d6f5ff')

    font1 = ('Arial', 20, 'bold')

    claim_button = customtkinter.CTkButton(root, text='Claim your free girlfriend', font=font1)
    claim_button.place(relx=0.5, rely=0.5, anchor='center')
    start_time = time.time()
    claim_button.configure(command=lambda: move_button_randomly(claim_button, start_time))

    root.mainloop()

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
        show_thank_you_window()
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
                show_thank_you_window()
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

image1 = Image.open("Sign up.png")
image1 = image1.resize((180, 200), Image.Resampling.LANCZOS)
image1 = ImageTk.PhotoImage(image1)

image_label1 = customtkinter.CTkLabel(frame1, image=image1, text='')
image_label1.place(x=30, y=50)

image2 = Image.open("EMR.png")
image2 = image2.resize((150, 150), Image.Resampling.LANCZOS)
image2 = ImageTk.PhotoImage(image2)

image_label2 = customtkinter.CTkLabel(frame1, image=image2, text='')
image_label2.place(x=30, y=220)

signup_label = customtkinter.CTkLabel(frame1, font=font1, text='Sign up', text_color='#000000', bg_color='#d6f5ff')
signup_label.place(x=275, y=20)

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
