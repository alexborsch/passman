from tkinter import *    
master = Tk()

# Create this method before you create the entry
def return_entry(en):
    """Gets and prints the content of the entry"""
    content = entry.get()
    print(content)  

Label(master, text="Input: ").grid(row=0, sticky=W)

entry = Entry(master)
entry.grid(row=0, column=1)

# Connect the entry with the return button
entry.bind('<Return>', return_entry) 

mainloop()