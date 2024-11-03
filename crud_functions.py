import sqlite3
from sqlite3 import Error
import logging
import os
from dotenv import load_dotenv


logging.basicConfig(level=logging.INFO, filename="logs/py_log.log", filemode='a',
                    format="%(asctime)s %(levelname)s %(message)s")
load_dotenv()
CONN = os.getenv("CONN_DB")# параметры соединения с БД берем из .env

#функция создает экземпляр соединения с БД с возвращает его как объект
def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        logging.info('connection successful')
    except Error as e:
        logging.error(f'The error {e}, occurred')
    return connection

"""Функция создает таблицу в БД"""
def initiate_db(connection):
    with connection:# синтаксис позволяет не использовать запись connection.commit()
        connection.executescript("""
        CREATE TABLE IF NOT EXISTS Products(
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        description TEXT,
        price INTEGER NOT NULL
        );
        CREATE TABLE IF NOT EXISTS Users(
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL,
        email TEXT NOT NULL,
        age INTEGER NOT NULL,
        balance INTEGER NOT NULL
        );
        """)
        logging.info('таблицы успешно созданы')

"""Функция добавляет 4-е продукта в БД"""
def insert_db(connection, data):
    sql = "INSERT INTO Products (title, description, price) VALUES (?, ?, ?);"
    with connection:
        connection.executemany(sql, data)
        logging.info('Продукты добавлены')

"""Функция выбирает все данные из таблицы БД в виде списка 
(каждый элемент которого - запись из таблицы в виде кортежа, 
в свою очередь каждый элемент которого - поле записи)"""
def get_all_products(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Products")
    prod_list = cursor.fetchall()
    connection.commit()
    logging.info(f'result: {prod_list}')
    return prod_list

def add_user(connection, *param):
    sql = "INSERT INTO Users (username, email, age, balance) VALUES (?, ?, ?, ?)"
    with connection:
        connection.execute(sql, *param)
        logging.info('user added')

def is_included(connection, user_name):
    cursor = connection.cursor()
    cursor.execute("SELECT username FROM Users WHERE username = ?", (user_name,))
    if cursor.fetchone():
        connection.commit()
        logging.info('user has been found')
        return True
    connection.commit()
    logging.info('user was not found')
    return False