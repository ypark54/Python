import multiprocessing as mp
import tkinter as tk
from tkinter import ttk

import datetime



def init_gui(channel_id):
    #read from que and update ui
    def update():
        currentTime = datetime.datetime.now()
        label['text'] = currentTime
        root.after(1000, update)
        tree[0].insert('', 0, values=contact)
    
    #display details when double click
    def pop_window(dummy):
        top = tk.Toplevel(root)
        tk.Label(top, text=type(dummy)).pack()

    root = tk.Tk()
    root.title('Main Application')
    # define columns
    columns = ('first_name', 'last_name', 'email')

    tabControl = ttk.Notebook(root)
    tab = []
    tree = []
    for index,ch in enumerate(channel_id, start=0):
        tab.append(ttk.Frame(tabControl))
        tabControl.add(tab[index], text=ch)
        tabControl.grid(row=0, column=0, sticky='ew')

        ttk.Label(tab[index]).grid(row=0, column=0)

        tree.append(ttk.Treeview(tab[index], columns=columns, show='headings'))
        contacts = []
        for n in range(1, 100):
            contacts.append((f'first {n}', f'last {n}', f'email{n}@example.com'))

        # add data to the treeview
        for contact in contacts:
            tree[index].insert('', 0, values=contact)
        # define headings
        tree[index].heading('first_name', text='First Name')
        tree[index].heading('last_name', text='Last Name')
        tree[index].heading('email', text='Email')
        
        tree[index].grid(row=0, column=0, sticky='nsew')
        tree[index].bind("<Double-Button-1>", pop_window)

        scrollbar = ttk.Scrollbar(tab[index], orient=tk.VERTICAL, command=tree[index].yview)
        tree[index].configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky='ns')
        
        
    label = tk.Label(root, text="placeholder")
    label.grid(row=1)
    update()

    root.mainloop()

if __name__ == '__main__':
    channel_id = ['966421494307639366','asdf']


    p = mp.Process(target=init_gui, args=(channel_id,)).start()
    




    