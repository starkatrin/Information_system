import sqlite3 as sql

class DB:
    def __init__(self):
        self.conn = sql.connect('kino.db')
        self.c = self.conn.cursor()

    def create_table(self, sql_create_films):
        self.c.executescript(sql_create_films)
        self.conn.commit()

    def insert_movies(self, sql_insert_values, movies):
        self.c.executemany(sql_insert_values, movies)
        self.conn.commit()

if __name__ == '__main__':
    sql_create_films = """
            CREATE TABLE IF NOT EXISTS movies (
              id INTEGER PRIMARY KEY NOT NULL,
              movie_name VARCHAR(255) NOT NULL,
              genre VARCHAR(255) NOT NULL,
              premiere DATE,
              age_requirement TINYINT,
              rating REAL,
              country VARCHAR(255) NOT NULL,
              created_at DATETIME DEFAULT CURRENT_TIMESTAMP)
        """

    sql_insert_values = """insert into movies (id, movie_name, genre, premiere, age_requirement, rating, country)
          values (NULL, ?, ?, ?, ?, ?, ?)"""
    movies = [('Зеленая миля', 'драма', 1999, 16, 9.2, 'США'),
              ('Побег из Шоушенка', 'драма', 1994, 16, 9.1, 'США'),
              ('Список Шиндлера', 'драма', 1993, 16, 8.8, 'США'),
              ('Форрест Гамп', 'драма', 1994, 16, 9.0, 'США'),
              ('Властелин колец: братство кольца', 'фэнтэзи', 2001, 12, 8.8, 'Новая Зеландия'),
              ('Пираты карибского моря: проклятье черной жемчужины', 'фэнтэзи', 2003, 12, 8.6, 'США'),
              ('Гарри Поттер и философский камень', 'фэнтэзи', 2001, 12, 8.6, 'Великобритания'),
              ('Назад в будущее', 'фантастика', 1985, 12, 8.8, 'США'),
              ('Кин-дза-дза', 'фантастика', 1986, 16, 8.0, 'СССР'),
              ('Темный рыцарь', 'фантастика', 2008, 16, 8.5, 'Великобритания'),
              ('Тайна Коко', 'мультфильм', 2017, 12, 8.7, 'США'),
              ('Король Лев', 'мультфильм', 1994, 0, 8.8, 'США'),
              ('Ледниковый период', 'мультфильм', 2002, 0, 8.0, 'США'),
              ('Двенадцать стульев', 'комедия', 1971, 16, 8.2, 'СССР'),
              ('Бриллиантовая рука', 'комедия', 1968, 16, 8.5, 'СССР'),
              ('Отель Гранд Будапешт', 'комедия', 2014, 16, 7.9, 'Германия'),
              ('Остров проклятых', 'триллер', 2009, 18, 8.5, 'США'),
              ('Бойцовский клуб', 'триллер', 1999, 18, 8.6, 'США'),
              ('Престиж', 'триллер', 2006, 16, 8.5, 'Великобритания'),
              ('Криминальное чтиво', 'криминал', 1994, 18, 8.6, 'США'),
              ('Большой куш', 'криминал', 2000, 16, 8.5, 'Великобритания'),
              ('Поймай меня, если сможешь', 'криминал', 2002, 16, 8.5, 'США'),
              ('Крепкий орешек', 'боевик', 1988, 16, 8.0, 'США'),
              ('Троя', 'боевик', 2004, 16, 8.0, 'США'),
              ('Бесславные ублюдки', 'боевик', 2009, 16, 8.3, 'Германия')
              ]

    db = DB()

    db.create_table(sql_create_films)
    db.insert_movies(sql_insert_values, movies)

    db.conn.close()
