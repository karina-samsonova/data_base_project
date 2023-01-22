from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox, Treeview, Notebook
from sqlalchemy import create_engine
import psycopg2


def space(x):
    var = Label(fr, height=x)
    var.pack()
def clear():
    for widget in fr.winfo_children():
       widget.destroy()
    fr.pack()
def destroy(event, window):
    window.destroy()
def create_list(string):
    values = list(cursor.execute(string))
    for i in range(len(values)):
        string = str(values[i])
        values[i] = string[2:-3]
    return values
def delete_db_alert(event, db_name):
    answer = messagebox.askyesno(
        title="Alert",
        message="Вы уверены, что хотите удалить текщую базу данных?")
    if answer:
        cursor.execution_options(autocommit=1).execute("call delete_db('{}')".format(db_name))
        raise SystemExit
def clear_db_alert(event, tables, db_name):
    answer = messagebox.askyesno(
        title="Alert",
        message="Вы уверены, что хотите очистить все таблицы?")
    if answer:
        for tab in tables:
            cursor.execution_options(autocommit=1).execute("call clear_tab('{}')".format(tab))
            fr.bind('<Enter>', lambda e: db_main(e, db_name))
def delete_tab_alert(tab_name, db_name):
    answer = messagebox.askyesno(
        title="Alert",
        message="Вы уверены, что хотите удалить текщую таблицу?")
    if answer:
        cursor.execution_options(autocommit=1).execute("call delete_tab('{}')".format(tab_name))
        fr.bind('<Enter>', lambda e: db_main(e, db_name))
def clear_tab_alert(tab_name, db_name, frtab, frmenu):
    answer = messagebox.askyesno(
        title="Alert",
        message="Вы уверены, что хотите очистить текущую таблицу?")
    if answer:
        cursor.execution_options(autocommit=1).execute("call clear_tab('{}')".format(tab_name))
        return select_table(db_name, tab_name, frtab, frmenu)
def new_db2(event, alert, name):
    cursor.execution_options(autocommit=1).execute("call lib.public.create_db('{}')".format(name))
    alert.destroy()
    fr.bind('<Enter>', lambda e: db_main(e, name))
def new_db(event):
    alert = Tk()
    alert.title("Создание базы данных")
    alert.geometry('300x100-500-300')
    var = Label(alert, height=1)
    var.pack()
    txt = Label(alert, text='Введите название для базы данных:', font='Times 12')
    txt.pack()
    var = Label(alert, width=1)
    var.pack(side=RIGHT)
    btn = Button(alert, text=" Далее ")
    btn.pack(side=RIGHT)
    name = Entry(alert, width=36)
    name.pack(side=RIGHT)
    btn.bind('<Button-1>', lambda e: new_db2(e, alert, name.get()))
def del_row(event, tab_name, col, ind, db_name, frtab, frmenu):
    cursor.execution_options(autocommit=1).execute("call drop_row(NULL::{}, '{}', {});".format(tab_name, col, ind))
    return select_table(db_name, tab_name, frtab, frmenu)
def select_table(db_name, tab_name, frtab, frmenu):
    for widget in frtab.winfo_children():
       widget.destroy()
    frtab.pack()
    for widget in frmenu.winfo_children():
       widget.destroy()
    frmenu.pack()
    columns = create_list("select * from get_columns('{}', '{}')".format(db_name, tab_name))
    rows = cursor.execute("select * from select_all(NULL::{})".format(tab_name))
    table = Treeview(frtab, columns=columns, show='headings')
    for i in range(len(columns)):
        table.column(columns[i], width=int(700/len(columns)), anchor=CENTER)
    table.heading(columns[i], text=columns[i])
    table["show"] = "headings"
    table.config(height=470)
    for i in columns:
        table.heading(i, text=i)
    for i in rows:
        table.insert("", END, values=tuple(i))
    table.pack()
    var = Label(frmenu, height=3)
    var.pack()
    btndel = Button(frmenu, text="Удалить строку")
    btndel.pack()
    btndel.bind('<Button-1>', lambda e: del_row(e, tab_name, columns[0], table.item(table.selection())['values'][0], db_name, frtab, frmenu))
    return table
def del_search(event, col, inds, db_name, tab_name, frtab, frmenu):
    for i in inds:
        cursor.execution_options(autocommit=1).execute("call drop_row(NULL::{}, '{}', {});".format(tab_name, col, i))
    return search_del(db_name, tab_name, frtab, frmenu)
def search(event, table, columns, frtab, msg, ind, tab_name, frmenu, db_name):
    frmenu.unbind('<Enter>')
    for widget in frtab.winfo_children():
       widget.destroy()
    frtab.pack()
    rows = list(cursor.execute("select * from select_all(NULL::{})".format(tab_name)))
    table = Treeview(frtab, columns=columns, show='headings')
    for i in range(len(columns)):
        table.column(columns[i], width=int(700 / len(columns)), anchor=CENTER)
    table.heading(columns[i], text=columns[i])
    table["show"] = "headings"
    table.config(height=470)
    for i in columns:
        table.heading(i, text=i)
    inds = []
    for i in rows:
        if str(i[ind]) == msg:
            table.insert("", END, values=tuple(i))
            inds.append(int(i[0]))
    table.pack()
    var = Label(frmenu, height=2)
    var.pack()
    btn = Button(frmenu, text="Удалить строки")
    btn.pack()
    btn.bind('<Button-1>', lambda e: del_search(e, columns[0], inds, db_name, tab_name, frtab, frmenu))
def search_del(db_name, tab_name, frtab, frmenu):
    for widget in frtab.winfo_children():
        widget.destroy()
    frtab.pack()
    for widget in frmenu.winfo_children():
        widget.destroy()
    frmenu.pack()
    columns = create_list("select * from get_columns('{}', '{}')".format(db_name, tab_name))
    rows = cursor.execute("select * from select_all(NULL::{})".format(tab_name))
    table = Treeview(frtab, columns=columns, show='headings')
    for i in range(len(columns)):
        table.column(columns[i], width=int(700 / len(columns)), anchor=CENTER)
    table.heading(columns[i], text=columns[i])
    table["show"] = "headings"
    table.config(height=470)
    for i in columns:
        table.heading(i, text=i)
    for i in rows:
        table.insert("", END, values=tuple(i))
    table.pack()

    columns = create_list("select * from get_columns('{}', '{}')".format(db_name, tab_name))
    var = Label(frmenu, height=1)
    var.pack()
    entry = Label(frmenu, text='Выберите колонку:', font='Times 10')
    entry.pack()
    menutabs = Combobox(frmenu, font='Times 10', width=25, values=columns)
    menutabs.pack()
    entry = Label(frmenu, text='Введите выражение\nдля поиска:', font='Times 10')
    entry.pack()
    msg = Entry(frmenu, width=28)
    msg.pack()
    space(1)
    btn = Button(frmenu, text=" Поиск ")
    btn.pack()
    btn.bind('<Button-1>', lambda e: search(e, table, columns, frtab, msg.get(), columns.index(menutabs.get()), tab_name, frmenu, db_name))
def insert2(event, frtab, frmenu, db_name, tab_name, ins, msg, cols):
    colstr = '('
    message = '('
    for i in range(len(msg)):
        message = message+'\'\''+msg[i].get()+'\'\''
        colstr += cols[i]
        if i < len(msg) - 1:
            message += ', '
            colstr += ', '
    message += ')'
    colstr += ')'
    cursor.execution_options(autocommit=1).execute("call insert_values(NULL::{}, '{}', '{}')".format(tab_name, colstr, message))
    ins.destroy()
    for widget in frtab.winfo_children():
        widget.destroy()
    frtab.pack()
    columns = create_list("select * from get_columns('{}', '{}')".format(db_name, tab_name))
    rows = cursor.execute("select * from select_all(NULL::{})".format(tab_name))
    table = Treeview(frtab, columns=columns, show='headings')
    for i in range(len(columns)):
        table.column(columns[i], width=int(700 / len(columns)), anchor=CENTER)
    table.heading(columns[i], text=columns[i])
    table["show"] = "headings"
    table.config(height=470)
    for i in columns:
        table.heading(i, text=i)
    for i in rows:
        table.insert("", END, values=tuple(i))
    table.pack()
def insert(event, frtab, frmenu, db_name, tab_name):
    columns = create_list("select * from get_columns('{}', '{}')".format(db_name, tab_name))
    if columns[0].count('id') > 0:
        columns.pop(0)
    ins = Tk()
    ins.title("Добавление данных")
    ins.geometry('300x{}-500-300'.format(len(columns)*35))
    msg = []
    k = 0
    for i in columns:
        entry = Label(ins, text=i+': ', font='Times 10')
        entry.grid(row=k+1, column=1)
        msg.append(Entry(ins, width=30))
        msg[k].grid(row=k+1, column=2)
        k+=1
    btnn = Button(ins, text=" Далее ")
    btnn.grid(row=k+1, column=2)
    btnn.bind("<Button-1>", lambda e: insert2(e, frtab, frmenu, db_name, tab_name, ins, msg, columns))
def tab_creation(event, vars, tab_name, db_name, namestr, typestr, notnull, pk, defaultstr, newtab):
    if len(vars) > 1:
        vars += ', '
    vars = vars+namestr+' '+typestr+' '
    if notnull['bg'] == 'powderblue':
        vars = vars+' not null'
    if pk['bg'] == 'powderblue':
        vars = vars+' primary key'
    if len(defaultstr) > 0:
        vars = vars+' default \'\''+defaultstr+'\'\''
    vars += ')'
    print(vars)
    cursor.execution_options(autocommit=1).execute("call create_table('{}', '{}')".format(tab_name, vars))
    newtab.destroy()
    fr.bind('<Enter>', lambda e: db_main(e, db_name))
def var_plus(event, vars, namestr, typestr, notnull, pk, defaultstr, frnewtab, frnewtab2, tab_name, db_name, newtab):
    if len(vars) > 1:
        vars += ', '
    vars = vars+namestr+' '+typestr+' '
    if notnull['bg'] == 'powderblue':
        vars = vars+' not null'
    if pk['bg'] == 'powderblue':
        vars = vars+' primary key'
    if len(defaultstr) > 0:
        vars = vars+' default \'\''+defaultstr+'\'\''
    print(vars)

    for widget in frnewtab.winfo_children():
       widget.destroy()
    frnewtab.pack()
    for widget in frnewtab2.winfo_children():
       widget.destroy()
    frnewtab2.pack()
    entry = Label(frnewtab, text='Name', font='Times 10')
    entry.grid(row=1, column=1)
    entry = Label(frnewtab, text='Data type', font='Times 10')
    entry.grid(row=1, column=2)
    entry = Label(frnewtab, text='Default', font='Times 10')
    entry.grid(row=1, column=5)
    name = Entry(frnewtab, width=10)
    name.grid(row=2, column=1)
    type = Entry(frnewtab, width=10)
    type.grid(row=2, column=2)
    notnull = Button(frnewtab, text=" Not Null ", bg='whitesmoke')
    notnull.grid(row=2, column=3)
    notnull.bind('<Button-1>', lambda e: not_null(e, notnull))
    pk = Button(frnewtab, text="Primary Key", bg='whitesmoke')
    pk.grid(row=2, column=4)
    pk.bind('<Button-1>', lambda e: primary_key(e, pk))
    default = Entry(frnewtab, width=10)
    default.grid(row=2, column=5)
    plus = Button(frnewtab, text=" + ")
    plus.grid(row=2, column=6)
    plus.bind('<Button-1>', lambda e: var_plus(e, vars, name.get(), type.get(), notnull, pk, default.get(), frnewtab,
                                               frnewtab2, tab_name, db_name, newtab))
    var = Label(frnewtab2, height=1)
    var.pack()
    ready = Button(frnewtab2, text=" Готово ")
    ready.pack()
    ready.bind('<Button-1>', lambda e: tab_creation(e, vars, tab_name, db_name, name.get(), type.get(), notnull, pk, default.get(), newtab))
def not_null(event, notnull):
    if notnull['bg'] == 'whitesmoke':
        notnull['bg'] = 'powderblue'
    else:
        notnull['bg'] = 'whitesmoke'
def primary_key(event, pk):
    if pk['bg'] == 'whitesmoke':
        pk['bg'] = 'powderblue'
    else:
        pk['bg'] = 'whitesmoke'
def create_table2(event, db_name, tab_name, frnewtab, newtab):
    for widget in frnewtab.winfo_children():
       widget.destroy()
    frnewtab.pack()
    frnewtab2 = Frame(newtab, width=400, height=30)
    frnewtab2.pack()
    vars = '('
    entry = Label(frnewtab, text='Name', font='Times 10')
    entry.grid(row=1, column=1)
    entry = Label(frnewtab, text='Data type', font='Times 10')
    entry.grid(row=1, column=2)
    entry = Label(frnewtab, text='Default', font='Times 10')
    entry.grid(row=1, column=5)
    name = Entry(frnewtab, width=10)
    name.grid(row=2, column=1)
    type = Entry(frnewtab, width=10)
    type.grid(row=2, column=2)
    notnull = Button(frnewtab, text=" Not Null ", bg='whitesmoke')
    notnull.grid(row=2, column=3)
    notnull.bind('<Button-1>', lambda e: not_null(e, notnull))
    pk = Button(frnewtab, text="Primary Key", bg='whitesmoke')
    pk.grid(row=2, column=4)
    pk.bind('<Button-1>', lambda e: primary_key(e, pk))
    default = Entry(frnewtab, width=10)
    default.grid(row=2, column=5)
    plus = Button(frnewtab, text=" + ")
    plus.grid(row=2, column=6)
    plus.bind('<Button-1>', lambda e: var_plus(e, vars, name.get(), type.get(), notnull, pk, default.get(), frnewtab,
                                               frnewtab2, tab_name, db_name, newtab))
    var = Label(frnewtab2, height=1)
    var.pack()
    ready = Button(frnewtab2, text=" Готово ")
    ready.pack()
    ready.bind('<Button-1>', lambda e: tab_creation(e, vars, tab_name, db_name, name.get(), type.get(), notnull, pk, default.get(), newtab))
def create_table(event, db_name):
    newtab = Tk()
    newtab.title("Создание таблицы")
    newtab.geometry('400x120-475-300')
    frnewtab = Frame(newtab, width=400, height=90)
    frnewtab.pack()
    var = Label(frnewtab, height=1)
    var.pack()
    txt = Label(frnewtab, text='Введите название для таблицы:', font='Times 12')
    txt.pack()
    var = Label(frnewtab, width=1)
    var.pack(side=RIGHT)
    btn = Button(frnewtab, text=" Далее ")
    btn.pack(side=RIGHT)
    name = Entry(frnewtab, width=36)
    name.pack(side=RIGHT)
    btn.bind('<Button-1>', lambda e: create_table2(e, db_name, name.get(), frnewtab, newtab))

    #fr.bind('<Enter>', lambda e: db_main(e, db_name))
def tab_menu(event, db_name, tab_name, action, frtab, frmenu):
    if action == 'Удаление таблицы':
        return delete_tab_alert(tab_name, db_name)
    elif action == 'Очищение таблицы':
        return clear_tab_alert(tab_name, db_name, frtab, frmenu)
    elif action == 'Вывод содержимого':
        return select_table(db_name, tab_name, frtab, frmenu)
    elif action == 'Поиск и удаление':
        return search_del(db_name, tab_name, frtab, frmenu)
    elif action == 'Добавление данных':
        for widget in frtab.winfo_children():
            widget.destroy()
        frtab.pack()
        for widget in frmenu.winfo_children():
            widget.destroy()
        frmenu.pack()
        columns = create_list("select * from get_columns('{}', '{}')".format(db_name, tab_name))
        rows = cursor.execute("select * from select_all(NULL::{})".format(tab_name))
        table = Treeview(frtab, columns=columns, show='headings')
        for i in range(len(columns)):
            table.column(columns[i], width=int(700 / len(columns)), anchor=CENTER)
        table.heading(columns[i], text=columns[i])
        table["show"] = "headings"
        table.config(height=470)
        for i in columns:
            table.heading(i, text=i)
        for i in rows:
            table.insert("", END, values=tuple(i))
        table.pack()

        var = Label(frmenu, height=3)
        var.pack()
        btnins = Button(frmenu, text="Добавить данные")
        btnins.pack()
        btnins.bind("<Button-1>", lambda e: insert(e, frtab, frmenu, db_name, tab_name))
        return
def db_main(event, db_name):
    clear()
    fr.unbind("<Enter>")
    cursor.execution_options(autocommit=1).execute("call set_to_db('{}')".format(db_name))
    root.title("База данных "+db_name)
    tables = create_list("select * from get_all_tabs('{}')".format(db_name))
    frtab = Frame(fr, width=700, height=470)
    frtab.pack(side=LEFT)
    frmenu = Frame(fr, width=200, height=250)

    entry = Label(fr, text='Выберите таблицу:', font='Times 10')
    entry.pack()
    menutabs = Combobox(fr, font='Times 10', width=25, values=tables)
    menutabs.pack()
    space(1)
    entry = Label(fr, text='Выберите действие:', font='Times 10')
    entry.pack()
    menu = Combobox(fr, font='Times 10', width=25, values=['Вывод содержимого', 'Поиск и удаление',
                                                            'Добавление данных', 'Очищение таблицы',
                                                            'Удаление таблицы'])

    menu.pack()
    menu.bind('<<ComboboxSelected>>', lambda e: tab_menu(e, db_name, menutabs.get(), menu.get(), frtab, frmenu))

    frmenu.pack()
    deletedb = Button(fr, text="Удалить базу данных", font='Times 8', bg='crimson', fg='whitesmoke')
    deletedb.pack(side=BOTTOM)
    deletedb.bind("<Button-1>", lambda e: delete_db_alert(e, db_name))
    var = Label(fr, height=1)
    var.pack(side=BOTTOM)
    cleardb = Button(fr, text="Очистить все таблицы", font='Times 10', fg='crimson')
    cleardb.pack(side=BOTTOM)
    cleardb.bind("<Button-1>", lambda e: clear_db_alert(e, tables, db_name))
    var = Label(fr, height=1)
    var.pack(side=BOTTOM)
    createtab = Button(fr, text="Добавить таблицу", font='Times 10')
    createtab.pack(side=BOTTOM)
    createtab.bind("<Button-1>", lambda e: create_table(e, db_name))

engine = create_engine('postgresql://postgres:0400642@localhost:5432/lib', echo=True)
cursor = engine.connect()
root = Tk()
root.title("Window")
root.geometry('900x500-200-100')
fr = Frame(root)
fr.pack()
space(8)
entry = Label(fr, text='Выберите, с какой базой данных Вы хотите работать:', font='Times 15')
entry.pack()
space(2)
combo = Combobox(fr, font='Times 13', width=35, values=create_list("select * from public.get_all_dbs()"))
combo.pack()
space(9)
btn = Button(fr, text="Создать новую базу данных", font='Times 13')
btn.pack()
btn.bind("<Button-1>", lambda e: new_db(e))
combo.bind('<<ComboboxSelected>>', lambda e: db_main(e, combo.get()))

root.mainloop()