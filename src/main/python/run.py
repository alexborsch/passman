from tkinter import *
from functools import partial


tkWindow = Tk()  
tkWindow.geometry('300x80+300+300')
tkWindow.resizable(width=False, height=False)
#tkWindow.iconbitmap('Icon.ico')  
tkWindow.title('CDLSRV | Login remote.it account')

''' decrypt '''
decryptLabel = Label(tkWindow, text="Enter decryption key").grid(row=0, column=0)
decrypt = StringVar()
decryptEntry = Entry(tkWindow, textvariable=decrypt, width=40).grid(row=1, column=0)

decryptButton = Button(tkWindow, text="Decrypt").grid(row=1, column=1)  
tkWindow.mainloop()