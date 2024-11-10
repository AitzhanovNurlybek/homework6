import psycopg2

config = psycopg2.connect(
    host = 'localhost',
    database='phonebook',
    user='postgres',
    password='1236'
)
def adding(id, username, password):
    current = config.cursor()#Этот инструмент позволяет нам взаимодействовать с данными в базе данных


    sql = '''
        INSERT INTO tablitsa
        VALUES (%s, %s, %s);
    '''
    current.execute(sql, (id, username, password))#для заполнения(өзгерту)
    current.close()#завершает базы данных сеанс работы
    config.commit()#сохранить изменения, для подтверждения этих изменений
    config.close()#освободить ресурсы и завершить соединение
# вставляем данные в телефонную книгу вводя их с консоли

print("ID:")
id = int(input())
print("Name:")
username = input()
print('Password:')
password=input()

adding(id, username, password)