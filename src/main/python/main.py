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
import pyAesCrypt




FILE_NAME = NONE
listdata = NONE
selected = NONE


def clear():
	global FILE_NAME
	FILE_NAME = "Untitled"
	text.delete('1.0', END)


def load_list():
    global listdata
    listdata = os.listdir('data/'+sets.database+'/')
    
    for i in listdata:
        box.insert(0, i)

    #print(listdata)
    #box.insert(0, listdata)
    

def load_data(select):
    passfile = open('data/'+sets.database+'/'+select, 'r')
    text.delete('1.0', END)
    text.insert('1.0', passfile.read())

def delete_point(selected):

    passfile = 'data/'+sets.database+'/'+selected
    #os.remove(passfile)
    print(passfile)
    box.delete(0, END)
    text.delete('1.0', END)
    load_list()



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


def encryptdb(file):
    buffersize = 512 * 1024
    pyAesCrypt.encryptFile(str(file), str(file) + '.aes', password, buffersize)

def decryptdb(file):

    pyAesCrypt.decryptFile(str(file), str(os.path.splitext(file)[0]) + '.aes', password, buffersize)

''' Create database '''
class CreateDB(tk.Tk):
    def __init__(self):

        tk.Tk.__init__(self)
        self.geometry('300x80+300+300')
        self.resizable(width=False, height=False)
        self.title(sets.app_name+' | Create DB')

        self.newdb = tk.StringVar()

        self.newdbLabel = tk.Label(self, text="Enter database name")
        self.newdbLabel.grid(row=0, column=0)
        self.newdbEntry = tk.Entry(self, textvariable=self.newdb, width=40)
        self.newdbEntry.grid(row=1, column=0)

        self.newdbButton = tk.Button(self, text="Create", command=self.create_db)
        self.newdbButton.grid(row=1, column=1)
        self.mainloop()

    def create_db(self):
        self.path = 'data/'+str(self.newdbEntry.get())+'/'
        try:
            os.mkdir(self.path)
            currentdbedit = open('settings.json', 'r')
            jsonfield = json.load(currentdbedit)
            currentdbedit.close()
            jsonfield["database"] = str(self.newdbEntry.get())
            currentdbedit = open('settings.json', 'w')
            json.dump(jsonfield, currentdbedit)
            currentdbedit.close()
        except OSError:
            messagebox.showinfo(sets.app_name+" | Create DB", "Creation of the directory %s failed" % self.path)
        else:
            box.delete(0, END)
            text.delete('1.0', END)
            load_list()
            self.destroy()
            messagebox.showinfo(sets.app_name+" | Create DB", "Successfully created the directory %s " % self.path)
        

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
        self.pass_title_Label.grid(row=0, column=0)
        self.pass_title_Entry = tk.Entry(self, textvariable=self.pass_title, width=35)
        self.pass_title_Entry.grid(row=0, column=1)

        self.pass_username_Label = tk.Label(self, text="Username: ")
        self.pass_username_Label.grid(row=1, column=0)
        self.pass_username_Entry = tk.Entry(self, textvariable=self.pass_username, width=35)
        self.pass_username_Entry.grid(row=1, column=1)

        self.pass_password_Label = tk.Label(self, text="Password: ")
        self.pass_password_Label.grid(row=2, column=0)
        self.pass_password_Entry = tk.Entry(self, textvariable=self.pass_password, width=35)
        self.pass_password_Entry.grid(row=2, column=1)

        self.pass_description_Label = tk.Label(self, text="Description: ")
        self.pass_description_Label.grid(row=3, column=0)
        self.pass_description_Entry = tk.Entry(self, textvariable=self.pass_description, width=35)
        self.pass_description_Entry.grid(row=3, column=1)

        self.saveButton = tk.Button(self, text="Save", command=self.on_button).grid(row=4, column=0)

        self.mainloop()

    def on_button(self):
        
        new_pass = open('data/'+sets.database+'/'+self.pass_title_Entry.get(), 'w')
        new_pass.write(self.pass_username_Entry.get()+'\n'+self.pass_password_Entry.get()+'\n'+self.pass_description_Entry.get()+'\n')
        new_pass.close()

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
        
''' decrypt database '''
class DecryptDB(tk.Tk):
    def __init__(self):

        tk.Tk.__init__(self)
        self.geometry('300x80+300+300')
        self.resizable(width=False, height=False)
        self.title(sets.app_name+' | Decrypt DB')

        self.decrypt = tk.StringVar()

        self.decryptLabel = tk.Label(self, text="Enter decryption key").grid(row=0, column=0)
        self.decryptEntry = tk.Entry(self, textvariable=self.decrypt, width=40).grid(row=1, column=0)

        self.decryptButton = tk.Button(self, text="Decrypt", command=self.decrypt_db).grid(row=1, column=1)
        self.mainloop()

    def decrypt_db(self):
        self.buffersize = 512 * 1024
        pyAesCrypt.decryptFile('data/database.db.mk', str(os.path.splitext('data/database.db')[0]) + '.db', self.decrypt, self.buffersize)
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

if os.path.isdir('data/'+sets.database):
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
fileMenu.add_command(label="Create DB", command=CreateDB)
fileMenu.add_command(label="Decrypt", command=DecryptDB)
fileMenu.add_command(label="Load list", command=load_list)
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