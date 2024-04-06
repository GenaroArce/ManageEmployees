import customtkinter as ctk
from CTkMessagebox import CTkMessagebox as messagebox
import sqlite3
import json
import re

#Load Configuration
def config():
    with open('./config/messages.json', 'r') as file:
        data = json.load(file)
        return data
    
#Connect Database SQLite3
def connect_db():
    message = config()
    try:
        return sqlite3.connect('./db/db.sqlite3')
    except sqlite3.Error as error:
        messagebox(title=message["title_screen"], message=message["errors"]["error"], icon="cancel", option_1="Exit")
        return None

def clear_text(event, entry, default_text):
    if entry.get() == default_text:
        entry.delete(0, ctk.END)

def restore_text(event, entry, default_text):
    if entry.get() == "":
        entry.insert(0, default_text)


    
def disabled_all(event):
    event.email_input.configure(state="disabled")
    event.name_input.configure(state="disabled")
    event.lastname_input.configure(state="disabled")
    event.post_input.configure(state="disabled")
    event.age_input.configure(state="disabled")
    event.button.configure(state="disabled")
    event.button_search.configure(state="disabled")

def enabled_all(event):
    event.email_input.configure(state="normal")
    event.name_input.configure(state="normal")
    event.lastname_input.configure(state="normal")
    event.post_input.configure(state="normal")
    event.age_input.configure(state="normal")
    event.button.configure(state="normal")
    event.button_search.configure(state="normal")

def check_email(event, email):
    return True if re.match(r"[^@]+@(gmail|hotmail)\.com", email) else False

def check_name_db(event, name):
    message = config()
    try:
        db = connect_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM employees WHERE name = ?", (name,))
        result = cursor.fetchone()
        return True if result else False

    except sqlite3.Error as error:
        messagebox(title=message["title_screen"], message=message["errors"]["error"], icon="cancel", option_1="Exit")
        return False

    finally:
        if db:
            db.close()

def check_email_db(event, email):
    message = config()
    try:
        db = connect_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM employees WHERE email = ?", (email,))
        result = cursor.fetchone()
        return True if result else False

    except sqlite3.Error as error:
        messagebox(title=message["title_screen"], message=message["errors"]["error"], icon="cancel", option_1="Exit")
        return False

    finally:
        if db:
            db.close()
    
def add_employee(event, email, name, lastname, post, age):
    message = config()
    age = int(age)
    try:
        with connect_db() as db:
            cursor = db.cursor()
            cursor.execute("INSERT INTO employees (email, name, lastname, post, age) VALUES (?, ?, ?, ?, ?)", (email, name, lastname, post, age))
            db.commit()
            messagebox(title=message["title_screen"], message=f"Added Employee\n\nEmail: {email}\nName: {name}\nLastname: {lastname}\nPost: {post}\nAge: {age}", icon="check", option_1="Ok")
    except sqlite3.Error as error:
        messagebox(title=message["title_screen"], message=message["errors"]["error"], icon="cancel", option_1="Exit")

def search_employee(email):
    message = config()
    if check_email(None, email):
        try:
            with connect_db() as db:
                cursor = db.cursor()
                cursor.execute("SELECT * FROM employees WHERE email = ?", (email,))
                result = cursor.fetchone()
                if result:
                    name = result[2]
                    lastname = result[3]
                    post = result[4]
                    age = result[5]
                    messagebox(title=message["title_screen_search"], message=f"Employee found\n\nEmail: {email}\nName: {name}\nLastname: {lastname}\nPost: {post}\nAge: {age}", icon="check", option_1="Ok")
                else:
                    messagebox(title=message["title_screen_search"], message=message["errors"]["employee_invalid"], icon="cancel", option_1="Retry")

        except Exception as e:
            messagebox(title=message["title_screen"], message=message["errors"]["error"], icon="cancel", option_1="Exit")
    else:
        messagebox(title=message["title_screen_search"], message=message["errors"]["email_invalid"], icon="warning", option_1="Retry")