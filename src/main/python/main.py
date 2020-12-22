from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5.QtWidgets import QMainWindow
from tkinter import *
from tkinter.filedialog import asksaveasfile, askopenfile
from tkinter.messagebox import showerror
from tkinter import messagebox

import sys
import json
import sqlite3
import os
from functools import partial

app_name = 'passman alpha'
database = 'data/database.db'

with open('settings.json') as f:
    file_content = f.read()
    data = json.loads(file_content)


FILE_NAME = NONE

def clear():
	global FILE_NAME
	FILE_NAME = "Untitled"
	text.delete('1.0', END)

def create_new_db():
    conn = sqlite3.connect(database) # или :memory: чтобы сохранить в RAM
    cursor = conn.cursor()
    
    cursor.execute("""CREATE TABLE IF NOT EXISTS `passwords_db` (
                        `id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL ,
                        `title` varchar(255) NOT NULL,
                        `data` varchar(255) NOT NULL);
                """)
    conn.commit()

def load_list():
    conn = sqlite3.connect(database)
    #conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    for i in cursor.execute("SELECT title FROM passwords_db"):
        box.insert(0, i)

def load_data(select):
    conn = sqlite3.connect(database)
    #conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    sql = "SELECT data FROM passwords_db WHERE title=?"
    cursor.execute(sql, select)
    text.delete('1.0', END)
    text.insert('1.0', cursor.fetchall())

def delete_point(selected):
    
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM passwords_db WHERE title = \"{}\"".format(selected))
    conn.commit()
    messagebox.showinfo("Information", selected+" was delete")
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
    print(selected)
    load_data(value)

 
def do_popup(event): 
    try: 
        m.tk_popup(event.x_root, event.y_root) 
    finally: 
        m.grab_release() 




def add_pass():
    def saveData(pass_title, pass_username, pass_password, pass_description):
        
        title = str(pass_title.get())
        username = str(pass_username.get())
        password = str(pass_password.get())
        descript = str(pass_description.get())
        data = title + " account information\nUsername: "+ username + "\nPassword: "+ password +"\nDescription: "+ descript
        print(title + '  ' + data)
        '''
        conn = sqlite3.connect(database)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO passwords_db (title, data) VALUES (\"{}\",\"{}\")".format(title, data))
        conn.commit()
        '''
        box.delete(0, END)
        text.delete('1.0', END)
        load_list()
        tkWindow.destroy()

    tkWindow = Tk()  
    tkWindow.geometry('330x130+350+350')
    tkWindow.resizable(width=False, height=False)
    
    tkWindow.title(app_name+' | Add password')

    pass_title_Label = Label(tkWindow, text="Title password: ").grid(row=0, column=0)
    pass_title = StringVar()
    pass_title_Entry = Entry(tkWindow, textvariable=pass_title, width=35).grid(row=0, column=1)

    pass_username_Label = Label(tkWindow, text="Username: ").grid(row=1, column=0)
    pass_username = StringVar()
    pass_username_Entry = Entry(tkWindow, textvariable=pass_username, width=35).grid(row=1, column=1)

    pass_password_Label = Label(tkWindow, text="Password: ").grid(row=2, column=0)
    pass_password = StringVar()
    pass_password_Entry = Entry(tkWindow, textvariable=pass_password, width=35).grid(row=2, column=1)

    pass_description_Label = Label(tkWindow, text="Description: ").grid(row=3, column=0)
    pass_description = StringVar()
    pass_description_Entry = Entry(tkWindow, textvariable=pass_description, width=35).grid(row=3, column=1)

    
    validateSave = partial(saveData, pass_title, pass_username, pass_password, pass_description)
    saveButton = Button(tkWindow, text="Save", command=validateSave).grid(row=4, column=0)
    tkWindow.mainloop()

    

tkWindow = Tk()  
tkWindow.geometry('630x380+300+300')
tkWindow.resizable(width=True, height=True)
#tkWindow.iconbitmap('Icon.ico')  
tkWindow.title(app_name)



# pass list
box = Listbox(selectmode=EXTENDED, height=100, width=30)
box.pack(side=LEFT)
scroll = Scrollbar(command=box.yview)
scroll.pack(side=LEFT, fill=Y)
box.config(yscrollcommand=scroll.set)

if os.path.exists(database):
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
m.add_command(label ="Add", command=add_pass) 
m.add_command(label ="Edit", command=edit_point) 
m.add_command(label ="Delete", command=lambda: delete_point(selected)) 


tkWindow.mainloop()