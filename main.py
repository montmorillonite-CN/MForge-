import tkinter.filedialog
import tkinter.ttk
import pyautogui
import getpass
import json
import os

# config
flag = 0
tab = '    '
version = '0.0.0'
defaultSize = '640x480'
defaultFileName = 'main.mff'
shortcuts = {
    'info': {
        'name': ['untitled', ''],
        'version': ['0.0.1', ''],
        'title': ['untitled', ''],
        'author': [getpass.getuser(), ''],
        'factorio_version': ['1.1', ''],
        'dependencies': {
            'base': ['>=1.1.0', '']
        },
        'description': ['Well, this mod is not described yet.', '']
    },
    'data': {
        'require-1': ['item', ''],
        'require-2': ['recipe', ''],
        'require-3': ['technology', '']
    },
    'file': {
        'name': ['file', ''],
        'path': ['prototypes', '']
    },
    'item': {
        'name': ['name', ''],
        'stack_size': ['100', '']
    }
}


def mkdir(path):
    if not os.path.exists(path):
        os.mkdir(path)


def textinput(title=None, prompt=None):
    def OK():
        global flag
        flag = 1

    def Cancel():
        global flag
        flag = -1

    global flag
    flag = 0
    dx, dy = 140, 50
    width, height = 166, 103
    textInput = tkinter.Tk()
    textInput.resizable(False, False)
    textInput.title(f'MForge {version} by 一块蒙脱石')
    textInput.geometry(f'+{min(max(0, pyautogui.position().x - dx), main.winfo_screenwidth() - width)}'
                       f'+{min(max(0, pyautogui.position().y - dy), main.winfo_screenheight() - height)}')
    if title is not None:
        textInput.title(title)
    fme = tkinter.Frame(textInput)
    fme.pack(padx=10, pady=10)
    if prompt is not None:
        tkinter.Label(fme, text=prompt).pack(anchor='w')
    ety = tkinter.Entry(fme)
    ety.pack()
    tkinter.Button(fme, text='取消', command=textInput.destroy).pack(side='left')
    tkinter.Button(fme, text='确定', command=OK).pack(side='right')
    textInput.bind('<Destroy>', lambda events: Cancel())
    textInput.bind('<Return>', lambda events: OK())
    textInput.update()
    while True:
        textInput.update()
        if flag == 1:
            text = ety.get()
            textInput.destroy()
            return text
        elif flag == -1:
            return None


def addItem(name, Root=None, dic=None):
    if dic is None:
        dic = shortcuts[name]
    if Root is None:
        Root = tree.focus()
    node = tree.insert(Root, tkinter.END, text=name, open=True)
    for i in dic:
        if type(dic[i]) is dict:
            addItem(i, node, dic[i])
        else:
            tree.insert(node, tkinter.END, text=i, values=dic[i], open=True)


def add_add_shortcut(key):
    add.add_command(label=key, command=lambda: addItem(key))


def find(findPath, path='', MPath=''):
    for i in tree.get_children(path):
        Path = MPath + '.' + tree.item(i)['text']
        if findPath in Path:
            return i
        else:
            j = find(findPath, i, Path)
            if j is not None:
                return j


def lstAll(path='', deep=0):
    string = ''
    for i in tree.get_children(path):
        string = string + deep * tab + str(tree.item(i)) + '\n' + lstAll(i, deep + 1)
    return string


def save(path=None):
    if path is None:
        path = tkinter.filedialog.askdirectory() + '\\' + tree.item(find('info.name'))['values'][0] + '_' + \
               tree.item(find('info.version'))['values'][0]
    if not os.path.exists(path):
        os.mkdir(path)
    with open(os.path.join(path, defaultFileName), 'w') as file:
        file.write(lstAll())
    with open(os.path.join(path, 'info.json'), 'w') as file:
        file.write(json.dumps(getDic('info'), indent=tab))


def getDic(MPath='', item=None):
    dic = {}
    lst = []
    if item is None:
        item = find(MPath)
    for i in tree.get_children(item):
        if tree.get_children(i) == ():
            dic[tree.item(i)['text']] = tree.item(i)['values'][0]
        else:
            if tree.item(i)['text'] == 'dependencies':
                for j in tree.get_children(i):
                    lst.append(tree.item(j)['text'] + tree.item(j)['values'][0])
                dic[tree.item(i)['text']] = lst
            else:
                dic[tree.item(i)['text']] = getDic(item=i)
    return dic


def test():
    print(find('info.name'))


if __name__ == '__main__':
    # main
    main = tkinter.Tk()
    main.geometry(defaultSize)
    main.title(f'MForge {version} by 一块蒙脱石')
    main.iconphoto(True, tkinter.PhotoImage(file='MForge.ico'))

    # list
    tree = tkinter.ttk.Treeview(main)
    tree.config(show='tree headings', columns=('value', 'note'), height=128)
    tree.heading('#0', text='键', anchor='w')
    tree.heading('#1', text='值', anchor='w')
    tree.heading('#2', text='备注', anchor='w')
    tree.pack(padx=10, pady=10, fill='both')

    # menu
    menu = tkinter.Menu(main)
    menu.add_command(label='保存', command=save)
    menu.add_command(label='查询', command=lambda: print(find(textinput())))
    menu.add_command(label='测试', command=test)
    main.config(menu=menu)

    # pop
    pop = tkinter.Menu(main)
    add = tkinter.Menu(pop)
    pop.add_command(label='添加', command=lambda: tree.insert(tree.focus(), tkinter.END, text=textinput(), open=True))
    pop.add_cascade(label='添加...', menu=add)
    add_add_shortcut('info')
    add_add_shortcut('data')
    add_add_shortcut('file')
    add.add_separator()
    add_add_shortcut('item')
    pop.add_command(label='删除', command=lambda: tree.delete(tree.focus()))
    tree.bind('<Double-1>', lambda events: tree.set(tree.focus(), 'value', textinput()))
    tree.bind('<Button-3>', lambda events: pop.post(pyautogui.position().x, pyautogui.position().y))

    # init
    root = tree.insert('', tkinter.END, text='root', open=True)
    addItem('info', root)
    addItem('data', root)
    addItem('file', root)

    main.mainloop()
