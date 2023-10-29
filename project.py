import tkinter as tk 
from tkinter import ttk
import sqlite3

# Класс навнго окна

class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = db
        self.view_records()

# Инициализируем виджеты для главного окна

    def init_main(self):
        toolbar = tk.Frame(bg='#d78e0', bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        # Кнопка добавления

        self.add_img = tk.PhotoImage(file='./img/add.png')
        self.btn_open_dialog = tk.Button(toolbar, bg='d78e0', bd=0, image=self.add_img, command=self.open_dialog)
        self.btn_open_dialog .pack(side=tk.LEFT)

        # Таблица
        self.tree = tk.Treeview(self, columns=('ID','name','tel','email'), height=45, show='headings')\
            
        scroll = tk.Scrollbar(self, command=self.tree.yview)
        scroll.pack(side=tk.RIGH, fill=ttk.Y)
        self.tree.configure(yscrollcommand=scroll.set)

        self.tree = column('ID', width=30, anchor=tk.CENTER)
        self.tree = column('name', width=300, anchor=tk.CENTER)
        self.tree = column('tel', width=150, anchor=tk.CENTER)
        self.tree = column('email', width=150, anchor=tk.CENTER)

        self.tree.heading('ID', text='ID')
        self.tree.heading('name', text='ФИО')
        self.tree.heading('tel', text='Телефон')
        self.tree.heading('email', text='E-mail')

        self.tree.pack(side=tk.LEFT)

        # Кнопка изменения

        self.update_png = tk.PhotoImage(file='./img/change.png')
        btn_edit = tk.Button(toolbar, bg='d7d8e0', bd=0, image=self.update_png)
        btn_edit.pack(side=tk.LEFT)


        self.delete_png = tk.PhotoImage(file='./img/delete.png')
        btn_delete = tk.Button(toolbar, bg='d7d8e0', bd=0, image=self.delete_png, command=self.delete_record)
        btn_delete.pack(side=tk.LEFT)

        # Кнопка поиска

        self.search_img = tk.PhotoImage(file='./img/search.png')
        btn_search = tk.Button(toolbar, bg='#d7d8e0', bd=0, image=self.search_img, command=self.view_records)
        btn_search.pack(side=tk.LEFT)

        # Кнопка обновления

        self.refresh_img = tk.PhotoImage(file='./img/refresh.png')
        btn_refresh = tk.Button(toolbar, bg='d7d8e0', bd=0, image=self.refresh_img, command=self.view_records)
        btn_refresh.pack(side=tk.LEFT)
        

        
    # Метод вызывающий дочернее окно
    def open_dialog(self):
        Child()


    # Метод добавления данных

    def records(self, name, tel, email):
        self.db.insert_data(name, tel, email)
        self.view_records

    # Отображение данных в treeview

    def view_records(self):
        self.db.cur.execute('SELECT * FROM db')
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('','end', values=row,) for row in self.db.cur.fechall()] 
    
    # Метод вызывающий дочернее окно для редактирования
    def open_update_dialog(self):
        Update()

    # Метод изменения данных

    def update_record(self, name, tel, email):
        self.db.cur.execute(''' UPDATE db SET name = ?, tel = ?, email = ? WHERE id = ? ''', (name, tel, email,
                                                                                              self.tree.set(self.tree.selection() [0], '#1')))
        self.db.conn.commit()
        self.view_records()

    # Метод удаления строк

    def delete_record(self):
        for select_item in self.tree.selection():
            self.db.cur.execute('DELETE FROM db WHERE id=?', self.tree.set(select_item, '#1'))


    # Метод вызывающий дочернее окно для поиска данных

    def open_searcg_dialog(self):
        Search()        


    # Метод поиска данных

    def search_records(self,name):
        name = ('%' + name + '%')
        self.db.cur.execute('SELECT * FROM db WHERE name LIKE ?', name)

        [self.tree.delete(i) for i in self.tree.get_children]

        [self.tree.insert('', 'end', values=row) for row in self.db.cur.fetchall()]




        self.db.conn.commit()
        self.view_records()


# Класс дочернего окна

class Child(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app

    # Инициализируем виджеты для дочернего окна

    def init_child(self):
        self.title('Добавить')
        self.geometry('400x200')
        self.resizable(False,False)

        # Перехватываем все события
        self.grab_set()

        # Перехватываем фокус

        self.focus.set()

        label_name = tk.Label(self, text='ФИО:')
        label_name.place(x=50, y=50)
        label_select = tk.Label(self,text='Телефон:')
        label_select.place(x=50, y=80)
        label_email = tk.Label(self, text='E-mail:')
        label_email.place(x=50, y=110)

        self.entry_name = tk.Entry(self)
        self.entry_name.place(x=200, y=50)
        self.entry_email = tk.Entry(self)
        self.entry_email.place(x=200, y=80)
        self.entry_tel = tk.Entry(self)
        self.entry_tel.place(x=200, y=110)

        self.btn_cancel = tk.Button(self, text='Закрыть', command= self.destroy)
        self.btn_cancel.place(x=300, y=170)

        self.btn_ok = tk.Button(self, text='Добавить')
        self.btn_ok.place(x=220, y=170)
        self.btn_ok.bind('<Button-1>', lambda event:
                         self.view.records(self.entry_name.get(),
                                           self.entry_email.get(),
                                           self.entry_tel.get()))
        self.btn_ok.bind('<Button-1>', lambda event: self.destroy(), add='+')        

# класс дочернего окна для изменения данных

class Update(Child):
    def __init__(self):
        super().__init__()
        self.init_update()
        self.view = app
        self.db = db
        self.default_data()

    def init_update(self):
        self.title('Редактировать контакт')
        btn_edit = tk.Button(self, text='Редактировать')
        btn_edit.place(x=205, y=170)
        btn_edit.bind('<Button-1>', lambda event:
                      self.view.update_record(self.entry_name.get(),
                                              self.entry_email.get(),
                                              self.entry_tel.get()))
        btn_edit.bind('<Button-1>', lambda event: self.destroy, add='+')
        self.btn_ok.destroy()

    def default_data(self):
        self.db.cur.execute('SEKECT * FROM db WHERE id=?', (self.view.tree.set(self.view.tree.selection() [0], '#1'),))
        row = self.db.cur.fetchone()
        self.entry_name.insert(0, row[1])
        self.entry_email.insert(0, row[2])
        self.entry_tel.insert(0, row[3])


class Search(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app

    # инициализация виджетов дочернего окна

    def init_child(self):
        self.title("Поиск контакта")
        self.geometry("300x100")
        self.resizable(False, False)

        self.grab_set()

        self.focus_set()

        label_name = tk.Label(self, text="ФИО")
        label_name.place(x=30, y=30)

        self.entry_name = tk.Entry(self)
        self.entry_name.place(x=130, y=30)

        btn_cancel = tk.Button(self, text="Закрыть", command=self.destroy)
        btn_cancel.place(x=150, y=70)

        self.btn_add = tk.Button(self, text="Найти")
        self.btn_add.bind("<Button-1>",
                          lambda ev: self.view.search_records(self.entry_name.get()))
        self.btn_add.bind("<Button-1>", lambda ev: self.destroy(), add = "+")
        self.btn_add.place(x=225, y=70)


# Класс БД
class DB: 
    def __init__(self):
        self.conn = sqlite3.connect(db.db)
        self.cur = self.cursor()
        self.cur.execute('''CREATE TABLE IF NOT EXISTS db(
            id INTEGER PRIMARY KEY,
            name TEXT,
            tel TEXT,
            email TEXT
        );
        ''')
        self.conn.commit()

    def insert_data(self, name, tel, email):
        self.cur.execute('INSERT INTO db (name, tel, email) VALUES (?, ?, ?);', (name, tel, email))
        self.conn.commit()



# При запуске программы
if __name__ == '__name__':
    root = tk.Tk()
    db = DB()
    app = Main(root)
    app.back()

    root.title("Телефонная книга")
    root.geometry('665x450')
    root.resizable(False,False)
    root.mainloop()
