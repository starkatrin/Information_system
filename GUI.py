import tkinter as tk
from tkinter import ttk

from BD import DB

class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = db
        self.view_records()

    def init_main(self):
        toolbar = tk.Frame(bg='#d7d8e0', bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        self.add_img = tk.PhotoImage(file='add.png')
        btn_open_dialog = tk.Button(toolbar, text='Добавить позицию', command=self.open_dialog, bg='#d7d8e0', bd=0,
                                    compound=tk.TOP, image=self.add_img)
        btn_open_dialog.pack(side=tk.LEFT)

        self.update_img = tk.PhotoImage(file='update.png')
        btn_edit_dialog = tk.Button(toolbar, text='Редактировать', bg='#d7d8e0', bd=0, image=self.update_img,
                                    compound=tk.TOP, command=self.open_update_dialog)
        btn_edit_dialog.pack(side=tk.LEFT)

        self.delete_img = tk.PhotoImage(file='delete.png')
        btn_delete = tk.Button(toolbar, text='Удалить позицию', bg='#d7d8e0', bd=0, image=self.delete_img,
                               compound=tk.TOP, command=self.delete_records)
        btn_delete.pack(side=tk.LEFT)

        self.search_img = tk.PhotoImage(file='search.png')
        btn_search = tk.Button(toolbar, text='Поиск', bg='#d7d8e0', bd=0, image=self.search_img,
                               compound=tk.TOP, command=self.open_search_dialog)
        btn_search.pack(side=tk.LEFT)

        self.refresh_img = tk.PhotoImage(file='refresh.png')
        btn_refresh = tk.Button(toolbar, text='Обновить', bg='#d7d8e0', bd=0, image=self.refresh_img,
                                compound=tk.TOP, command=self.view_records)
        btn_refresh.pack(side=tk.LEFT)

        self.tree = ttk.Treeview(self,
                                 columns=('id', 'movie', 'genre', 'premiere', 'age_requirement',
                                          'rating', 'country'), height=15, show='headings')

        self.tree.column('id', width=30, anchor=tk.CENTER)
        self.tree.column('movie', width=365, anchor=tk.CENTER)
        self.tree.column('genre', width=150, anchor=tk.CENTER)
        self.tree.column('premiere', width=100, anchor=tk.CENTER)
        self.tree.column('age_requirement', width=100, anchor=tk.CENTER)
        self.tree.column('rating', width=60, anchor=tk.CENTER)
        self.tree.column('country', width=150, anchor=tk.CENTER)

        self.tree.heading('id', text='id')
        self.tree.heading('movie', text='Фильм')
        self.tree.heading('genre', text='Жанр')
        self.tree.heading('premiere', text='Премьера')
        self.tree.heading('age_requirement', text='Возрастной ценз')
        self.tree.heading('rating', text='Рейтинг')
        self.tree.heading('country', text='Страна')

        self.tree.pack(side=tk.LEFT)

        scroll = tk.Scrollbar(self, command=self.tree.yview)
        scroll.pack(side=tk.LEFT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scroll.set)

    def records(self, movie, genre, premiere, age_requirement,
                                          rating, country):
        self.db.c.execute("""insert into movies (id, movie_name, genre, premiere, age_requirement, rating, country)
          values (NULL, ?, ?, ?, ?, ?, ?)""",
                         ( movie, genre, premiere, age_requirement,
                          rating, country))
        self.db.conn.commit()
        self.view_records()

    def update_record(self, movie, genre, premiere, age_requirement,
                                          rating, country):
        self.db.c.execute('''UPDATE movies SET movie_name=?, genre=?, premiere=?, age_requirement=?,
                                          rating=?, country=? WHERE id=?''',
                          (movie, genre, premiere, age_requirement,
                                          rating, country, self.tree.set(self.tree.selection()[0], '#1')))
        self.db.conn.commit()
        self.view_records()

    def view_records(self):
        self.db.c.execute('''SELECT * FROM movies''')
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]

    def delete_records(self):
        for selection_item in self.tree.selection():
            self.db.c.execute('''DELETE FROM movies WHERE id=?''', (self.tree.set(selection_item, '#1'),))
        self.db.conn.commit()
        self.view_records()

    def search_records(self, value, column):
        value = ('%' + value + '%',)
        if column == 'Фильм':
            column = 'movie_name'
        if column == 'Жанр':
            column = 'genre'
        if column == 'Премьера':
            column = 'premiere'
        if column == 'Ценз':
            column = 'age_requirement'
        if column == 'Рейтинг':
            column = 'rating'
        if column == 'Страна':
            column = 'country'
        self.db.c.execute(f'''SELECT * FROM movies WHERE {column} LIKE ?''', value)
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]

    def open_dialog(self):
        Child()

    def open_update_dialog(self):
        Update()

    def open_search_dialog(self):
        Search()


class Child(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app

    def init_child(self):
        self.title('Добавить фильм')
        self.geometry('400x320+400+300')
        self.resizable(False, False)

        label_movie = tk.Label(self, text='Фильм:')
        label_movie.place(x=50, y=50)
        label_genre = tk.Label(self, text='Жанр:')
        label_genre.place(x=50, y=80)
        label_premiere = tk.Label(self, text='Премьера:')
        label_premiere.place(x=50, y=110)
        label_age_requirement = tk.Label(self, text='Ценз:')
        label_age_requirement.place(x=50, y=140)
        label_rating = tk.Label(self, text='Рейтинг:')
        label_rating.place(x=50, y=170)
        label_country = tk.Label(self, text='Страна:')
        label_country.place(x=50, y=200)

        self.entry_movie = ttk.Entry(self)
        self.entry_movie.place(x=200, y=50)

        self.combobox_genre = ttk.Combobox(self, values=[u'драма', u'фэнтэзи', u'фантастика', u'мультфильм',
            u'комедия', u'триллер',u'криминал', u'боевик'])
        self.combobox_genre.current(0)
        self.combobox_genre.place(x=200, y=80)

        self.entry_premiere = ttk.Entry(self)
        self.entry_premiere.place(x=200, y=110)

        self.entry_age_requirement = ttk.Entry(self)
        self.entry_age_requirement.place(x=200, y=140)

        self.entry_rating = ttk.Entry(self)
        self.entry_rating.place(x=200, y=170)

        self.combobox_country = ttk.Combobox(self, values=[u'США', u'Новая Зеландия', u'Великобритания',
                    u'СССР', u'Германия', u'Австралия'])
        self.combobox_country.current(0)
        self.combobox_country.place(x=200, y=200)

        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=300, y=230)

        self.btn_ok = ttk.Button(self, text='Добавить')
        self.btn_ok.place(x=220, y=230)
        self.btn_ok.bind('<Button-1>', lambda event: self.view.records(self.entry_movie.get(),
                                                                       self.combobox_genre.get(),
                                                                       self.entry_premiere.get(),
                                                                       self.entry_age_requirement.get(),
                                                                       self.entry_rating.get(),
                                                                       self.combobox_country.get()))

        self.grab_set()
        self.focus_set()


class Update(Child):
    def __init__(self):
        super().__init__()
        self.init_edit()
        self.view = app
        self.db = db
        self.default_data()

    def init_edit(self):
        self.title('Редактировать фильм')
        btn_edit = ttk.Button(self, text='Редактировать')
        btn_edit.place(x=205, y=230)
        btn_edit.bind('<Button-1>', lambda event: self.view.update_record(self.entry_movie.get(),
                                                                       self.combobox_genre.get(),
                                                                       self.entry_premiere.get(),
                                                                       self.entry_age_requirement.get(),
                                                                       self.entry_rating.get(),
                                                                       self.combobox_country.get()))

        self.btn_ok.destroy()

    def default_data(self):
        self.db.c.execute('''SELECT * FROM movies WHERE id=?''',
                          (self.view.tree.set(self.view.tree.selection()[0], '#1'),))
        row = self.db.c.fetchone()
        self.entry_movie.insert(0, row[1]),
        self.combobox_genre.current(0),
        self.entry_premiere.insert(0, row[3]),
        self.entry_age_requirement.insert(0, row[4]),
        self.entry_rating.insert(0, row[5]),
        self.combobox_country.current(0)


class Search(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.init_search()
        self.view = app

    def init_search(self):
        self.title('Поиск')
        self.geometry('400x300+400+300')
        self.resizable(False, False)

        label_search = tk.Label(self, text='Поиск')
        label_search.place(x=30, y=20)

        self.combobox_search = ttk.Combobox(self, values=[u'Фильм', u'Жанр', u'Премьера',
                                                          u'Ценз', u'Рейтинг', u'Страна'])
        self.combobox_search.current(0)
        self.combobox_search.place(x=110, y=20)

        self.entry_search = ttk.Entry(self)
        self.entry_search.place(x=250, y=20, width=120)

        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=185, y=50)

        btn_search = ttk.Button(self, text='Поиск')
        btn_search.place(x=105, y=50)
        btn_search.bind('<Button-1>', lambda event: self.view.search_records(self.entry_search.get(),
                                                                             self.combobox_search.get()))
        btn_search.bind('<Button-1>', lambda event: self.destroy(), add='+')


if __name__ == "__main__":
    root = tk.Tk()
    db = DB()
    app = Main(root)
    app.pack()
    root.title("Копилка фильмов")
    root.geometry("980x450+60+50")
    root.resizable(False, False)
    root.mainloop()
    db.conn.close()