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


with open('settings.json') as f:
    file_content = f.read()
    data = json.loads(file_content)


FILE_NAME = NONE

def clear():
	global FILE_NAME
	FILE_NAME = "Untitled"
	text.delete('1.0', END)

def create_new_db():
    conn = sqlite3.connect("data/database.db") # или :memory: чтобы сохранить в RAM
    cursor = conn.cursor()
    
    cursor.execute("""CREATE TABLE IF NOT EXISTS `passwords_db` (
                        `id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL ,
                        `title` varchar(255) NOT NULL,
                        `data` varchar(255) NOT NULL);
                """)
    conn.commit()

def load_list():
    conn = sqlite3.connect("data/database.db")
    #conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    for i in cursor.execute("SELECT title FROM passwords_db"):
        box.insert(0, i)

def load_data(select):
    conn = sqlite3.connect("data/database.db")
    #conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    sql = "SELECT data FROM passwords_db WHERE title=?"
    cursor.execute(sql, select)
    text.delete('1.0', END)
    text.insert('1.0', cursor.fetchall())

def delete_point(selected):
    
    conn = sqlite3.connect("data/database.db")
    cursor = conn.cursor()
    #sql = "DELETE FROM passwords_db WHERE title=:point", point
    cursor.execute("DELETE FROM passwords_db WHERE title=:point", selected)
    conn.commit()

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
  



tkWindow = Tk()  
tkWindow.geometry('630x380+300+300')
tkWindow.resizable(width=True, height=True)
#tkWindow.iconbitmap('Icon.ico')  
tkWindow.title('passman alpha')



# pass list
box = Listbox(selectmode=EXTENDED, height=100, width=30)
box.pack(side=LEFT)
scroll = Scrollbar(command=box.yview)
scroll.pack(side=LEFT, fill=Y)
box.config(yscrollcommand=scroll.set)

if os.path.exists("data/database.db"):
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
fileMenu.add_command(label="Add")
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
m.add_command(label ="Edit", command=edit_point) 
m.add_command(label ="Delete", command=lambda: delete_point(selected[0])) 


tkWindow.mainloop()