from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5.QtWidgets import QMainWindow
import tkinter as tk
from tkinter import *
from tkinter.filedialog import asksaveasfile, askopenfile
from tkinter.messagebox import showerror
from tkinter import messagebox

import sys
import json
import sqlite3
import os
from functools import partial
import settings as sets





FILE_NAME = NONE
listdata = NONE
selected = NONE


def clear():
	global FILE_NAME
	FILE_NAME = "Untitled"
	text.delete('1.0', END)

def create_new_db():
    conn = sqlite3.connect(sets.database) 
    cursor = conn.cursor()
    
    cursor.execute("""CREATE TABLE IF NOT EXISTS `passwords_db` (
                        `id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL ,
                        `title` varchar(255) NOT NULL,
                        `data` varchar(255) NOT NULL);
                """)
    conn.commit()

def load_list():
    global listdata
    conn = sqlite3.connect(sets.database)
    
    cursor = conn.cursor()
    
    for listdata in cursor.execute("SELECT title FROM passwords_db"):
        box.insert(0, listdata)

def load_data(select):
    conn = sqlite3.connect(sets.database)
    
    cursor = conn.cursor()
    
    sql = "SELECT data FROM passwords_db WHERE title=?"
    cursor.execute(sql, select)
    text.delete('1.0', END)
    text.insert('1.0', cursor.fetchall())

def delete_point(selected):
    
    conn = sqlite3.connect(sets.database)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM passwords_db WHERE title = \"{}\"".format(selected))
    conn.commit()
    messagebox.showinfo("Information", selected+" was deleted from your database")
    box.delete(0, END)
    text.delete('1.0', END)
    load_list()

def edit_point():
    pass



def onselect(event):
    global selected
    w = event.widget
    idx = int(w.curselection()[0])
    value = w.get(idx)
    selected = value[0]
    load_data(value)

 
def do_popup(event): 
    try: 
        m.tk_popup(event.x_root, event.y_root) 
    finally: 
        m.grab_release() 


''' Add new password to db '''

class SavePass(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.geometry('330x230+350+350')
        self.resizable(width=False, height=False)
        self.title(sets.app_name+' | Add password')

        self.pass_title = tk.StringVar()
        self.pass_username = tk.StringVar()
        self.pass_password = tk.StringVar()
        self.pass_description = tk.StringVar()

        self.pass_title_Label = tk.Label(self, text="Title password: ")
        
        self.pass_title_Entry = tk.Entry(self, textvariable=self.pass_title, width=35)

        self.pass_username_Label = tk.Label(self, text="Username: ")
        
        self.pass_username_Entry = tk.Entry(self, textvariable=self.pass_username, width=35)

        self.pass_password_Label = tk.Label(self, text="Password: ")
        
        self.pass_password_Entry = tk.Entry(self, textvariable=self.pass_password, width=35)

        self.pass_description_Label = tk.Label(self, text="Description: ")
        
        self.pass_description_Entry = tk.Entry(self, textvariable=self.pass_description, width=35)

        self.saveButton = tk.Button(self, text="Save", command=self.on_button)
        
        
        self.pass_title_Label.pack()
        self.pass_title_Entry.pack()
        self.pass_username_Label.pack()
        self.pass_username_Entry.pack()
        self.pass_password_Label.pack()
        self.pass_password_Entry.pack()
        self.pass_description_Label.pack()
        self.pass_description_Entry.pack()
        self.saveButton.pack()


        self.mainloop()

    def on_button(self):
        
        self.title = str(self.pass_title_Entry.get())
        self.username = str(self.pass_username_Entry.get())
        self.password = str(self.pass_password_Entry.get())
        self.descript = str(self.pass_description_Entry.get())
        
        self.data = self.title + " account information\nUsername: "+ self.username + "\nPassword: "+ self.password +"\nDescription: "+ self.descript
        
        if self.title in listdata:
            messagebox.showinfo("Information", self.title+" is in your database. Try again to think of a new password name")
            self.destroy()
        else:

            conn = sqlite3.connect(sets.database)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO passwords_db (title, data) VALUES (\"{}\",\"{}\")".format(self.title, self.data))
            conn.commit()
            
            box.delete(0, END)
            text.delete('1.0', END)
            load_list()
            self.destroy()

''' edit selected password '''

class EditPass(tk.Tk):
    def __init__(self):

        conn = sqlite3.connect(sets.database)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM passwords_db WHERE title = \"{}\"".format(selected))
        edit_data = cursor.fetchall()
        for row in edit_data:
            edit_data_id = row[0]
            edit_data_title = row[1]
            edit_data_data = row[2]


        self.post_id = edit_data_id
        tk.Tk.__init__(self)
        self.geometry('330x230+350+350')
        self.resizable(width=False, height=False)
        self.title(sets.app_name+' | Edit password')

        self.edit_pass_title = tk.StringVar()
        self.edit_pass_data = tk.StringVar()

        self.edit_pass_title_Label = tk.Label(self, text="Title password: ")
        self.edit_pass_title_Entry = tk.Entry(self, textvariable=self.edit_pass_title, width=35)

        self.edit_pass_data_Label = tk.Label(self, text="Password data: ")
        self.edit_pass_data_Entry = tk.Text(self, width=35, height=8)


        self.edit_saveButton = tk.Button(self, text="Save", command=self.save_on_button)
        
        self.edit_pass_title_Entry.insert(0, edit_data_title)
        self.edit_pass_data_Entry.insert('1.0', edit_data_data)
        
        self.edit_pass_title_Label.pack()
        self.edit_pass_title_Entry.pack()
        self.edit_pass_data_Label.pack()
        self.edit_pass_data_Entry.pack()
        self.edit_saveButton.pack()


        self.mainloop()

    def save_on_button(self):
        
        self.edit_title = str(self.edit_pass_title_Entry.get())
        self.edit_data = str(self.edit_pass_data_Entry.get('1.0', tk.END))
        
        conn = sqlite3.connect(sets.database)
        cursor = conn.cursor()
        cursor.execute("UPDATE passwords_db set title=\"{}\", data=\"{}\" where id=\"{}\"".format(self.edit_title, self.edit_data, self.post_id))
        conn.commit()
        
        box.delete(0, END)
        text.delete('1.0', END)
        load_list()
        self.destroy()
        

tkWindow = Tk()  
tkWindow.geometry('630x380+300+300')
tkWindow.resizable(width=True, height=True)

tkWindow.title(sets.app_name)



# pass list
box = Listbox(selectmode=EXTENDED, height=100, width=30)
box.pack(side=LEFT)
scroll = Scrollbar(command=box.yview)
scroll.pack(side=LEFT, fill=Y)
box.config(yscrollcommand=scroll.set)

if os.path.exists(sets.database):
    load_list()

box.bind('<<ListboxSelect>>', onselect)
box.bind("<Button-3>", do_popup) 


# text area
text = Text(tkWindow, width=400, height=400, wrap="word")
scrollb = Scrollbar(tkWindow, orient=VERTICAL, command=text.yview)
scrollb.pack(side="right", fill="y")
text.configure(yscrollcommand=scrollb.set)
text.pack()


# menubar
menuBar = Menu(tkWindow)
fileMenu = Menu(menuBar)
fileMenu.add_command(label="Create DB", command=create_new_db)
fileMenu.add_command(label="Import")
fileMenu.add_command(label="Export")
fileMenu.add_command(label="Help")

settingsMenu = Menu(menuBar)
settingsMenu.add_command(label="Keys")
settingsMenu.add_command(label="Languages")
settingsMenu.add_command(label="Server")
settingsMenu.add_command(label="GIT")

menuBar.add_cascade(label="File", menu=fileMenu)
menuBar.add_cascade(label="Settings", menu=settingsMenu)
menuBar.add_cascade(label="Clear", command=clear)
menuBar.add_cascade(label="Exit", command=tkWindow.quit)
tkWindow.config(menu=menuBar)

# right click menu
m = Menu(tkWindow, tearoff = 0) 
m.add_command(label ="Add", command=SavePass) 
m.add_command(label ="Edit", command=EditPass) 
m.add_command(label ="Delete", command=lambda: delete_point(selected)) 


tkWindow.mainloop()