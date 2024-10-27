import sqlite3


'''открываем соединение с БД и объявляем переменную с параметрами соединения'''
connection = sqlite3.connect('not_telegram.db')
cursor = connection.cursor()

'''создаем таблицу согласно задания. Ее можно не комментировать, \
так как используется условие IF NOT EXISTS. скрин в файлах \
create_structure.png, create_browser.png'''
cursor.execute('''
CREATE TABLE IF NOT EXISTS Users(
id INTEGER PRIMARY KEY,
username TEXT NOT NULL,
email TEXT NOT NULL,
age INTEGER,
balance INTEGER NOT NULL
)
''')

'''добавляем индекс на первичный ключ'''
cursor.execute('CREATE INDEX IF NOT EXISTS idx_id ON Users(id)')

'''добавляем 10 записей с помощью цикла. Скрин в файле insert.png'''
# for i in range(1, 11):
#      cursor.execute('INSERT INTO Users (username, email, age, balance) VALUES (?, ?, ?, ?)', (f'User{i}', f'example{i}@gmail.com', f'{i*10}', 1000))

'''обновляем баланс у каждой второй записи, начиная с первой, применяя WHERE с вычислением нечетных id записей \
(этот способ работает только если строки не удалялись, выбор этого варианта обусловлен тем, что с помощью цикла \
с использованием шага - step, мы применим на следующем примере с удалением для демонстрации различных вариантов). \
Скрин в файле  update.png'''
#cursor.execute('UPDATE Users SET balance = ? WHERE id % 2 = 1', (500,))

'''Удаляем каждую третью запись через цикл с шагом - step = 3, для этого сначала вычисляем количество записей через функцию COUNT, \
присваивая результат запроса в переменную с использованием функции fetchone(). Скрин в файле delete.png'''
# cursor.execute('SELECT COUNT(id) FROM Users')
# count_row = cursor.fetchone()[0]
# for i in range(1, count_row + 1, 3):
#     cursor.execute('DELETE FROM Users WHERE id = ?', (i,))

'''Делаем выборку записей с возрастом, не равным 60 и выводим результат на консоль в заданном формате. Скрин в файле select.png'''
cursor.execute('SELECT * FROM Users WHERE age <> ?', (60,))
users = cursor.fetchall()
for user in users:
    print(f'Имя: {user[1]} | Почта: {user[2]} | Возраст: {user[3]} | Баланс: {user[4]}')

'''применяем изменения и закрываем соединение'''
connection.commit()
connection.close()

