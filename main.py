import os
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

img = None


def load(Path, parent=''):
    item = tree.insert(parent, tk.END, text=os.path.basename(Path), values=[Path], open=True)
    for i in os.listdir(Path):
        path = os.path.join(Path, i)
        if os.path.isdir(path):
            load(path, item)
        else:
            tree.insert(item, tk.END, text=i, values=[path], open=True)


def show(path):
    global img
    image = Image.open(path)
    img = ImageTk.PhotoImage(image)
    canvas.update()
    canvas.create_image(canvas.winfo_width() / 2, canvas.winfo_height() / 2, image=img)


if __name__ == '__main__':
    main = tk.Tk()
    main.title('MForge-alpha')
    main.geometry('640x480')

    fme = tk.Frame(main)
    fme1 = tk.Frame(fme)
    fme2 = tk.Frame(fme)
    buff = tk.Frame(fme, width=2, cursor='sb_h_double_arrow')
    tree = ttk.Treeview(fme1, height=114, show='tree', selectmode='browse')
    text = tk.Text(fme2, width=514)
    bar1 = tk.Scrollbar(fme1)
    bar2 = tk.Scrollbar(fme2)
    canvas = tk.Canvas(fme, width=114514, height=1919810)
    menu = tk.Menu()
    menu.add_command(label='test', command=lambda: [
        tree.config(columns='path', show='tree headings'),
        tree.heading('#0', text='tree'),
        tree.heading('#1', text='path')
    ])

    bar1.config(command=tree.yview)
    bar2.config(command=text.yview)
    main.config(menu=menu)

    fme.pack(padx=10, pady=10, fill='both')
    fme1.pack(side='left', fill='both')
    buff.pack(side='left', fill='y')
    fme2.pack(side='left', fill='both')
    bar1.pack(side='right', fill='y')
    bar2.pack(side='right', fill='y')
    tree.pack(side='left', fill='both')
    text.pack(side='left', fill='both')

    main.update()
    buff.bind('<B1-Motion>', lambda events: [
        tree.pack_forget(),
        tree.column('#0', width=tree.winfo_width() + events.x),
        tree.pack(side='left', fill='both'),
    ])
    tree.bind('<ButtonRelease-1>', lambda events: [
        [
            fme2.pack_forget(),
            canvas.pack(side='left', fill='both'),
            show(tree.item(tree.focus())['values'][0])
        ] if tree.item(tree.focus())['values'][0].endswith('.png') or
             tree.item(tree.focus())['values'][0].endswith('.jpg') else [
            canvas.pack_forget(),
            text.delete('1.0', tk.END),
            fme2.pack_forget() if os.path.isdir(tree.item(tree.focus())['values'][0]) else [
                fme2.pack(side='left', fill='both'),
                text.insert('1.0', open(tree.item(tree.focus())['values'][0], encoding='utf-8').read())
            ]
        ]
    ])
    text.bind('<Control-s>', lambda events: [
        open(tree.item(tree.focus())['values'][0], 'w').write(text.get('0.0', tk.END)),
        messagebox.showinfo('MForge-Alpha', 'Save successfully!')
    ])
    canvas.bind('<Configure>', lambda events: show(tree.item(tree.focus())['values'][0]))
    load(filedialog.askdirectory())
    main.mainloop()
