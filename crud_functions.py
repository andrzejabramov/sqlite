import sqlite3


"""Функция создает таблицу в БД"""
def initiate_db(filename):
    connection = sqlite3.connect(filename)
    cursor = connection.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Products(
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    price INTEGER NOT NULL
    );
    """)
    connection.commit()
    connection.close()

"""Функция добавляет 4-е продукта в БД"""
def insert_db(filename):
    connection = sqlite3.connect(filename)
    cursor = connection.cursor()
    for row in range(1, 5):
        cursor.execute("""
        INSERT INTO Products (title, description, price)
        VALUES (?, ?, ?);
        """, (f'Продукт{row}', f'Описание{row}', f'{row * 100}'))
    connection.commit()
    connection.close()

"""Функция выбирает все данные из таблицы БД в виде списка 
(каждый элемент которого - запись из таблицы в виде кортежа, 
в свою очередь каждый элемент которого - поле записи)"""
def get_all_products(filename):
    connection = sqlite3.connect(filename)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Products")
    prod_list = cursor.fetchall()
    connection.commit()
    connection.close()
    return prod_list