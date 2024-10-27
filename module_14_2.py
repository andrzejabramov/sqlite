import sqlite3


'''открываем соединение с БД и объявляем переменную с параметрами соединения'''
connection = sqlite3.connect('not_telegram.db')
cursor = connection.cursor()

'''удаляем запись с id = 6'''
#cursor.execute('DELETE FROM Users WHERE id = ?', (6,))

'''подсчитываем количество всех пользователей \
Замечание: можно было бы применить: SELECT COUNT(*)..., \
но при равном итоге COUNT(одно любое поле) работает быстрее'''
cursor.execute('SELECT COUNT(id) FROM Users')
total_users = cursor.fetchone()[0]

'''считаем сумму всех балансов'''
cursor.execute('SELECT SUM(balance) FROM Users')
all_balances = cursor.fetchone()[0]

print(all_balances / total_users)

'''применяем изменения и закрываем соединение'''
connection.commit()
connection.close()