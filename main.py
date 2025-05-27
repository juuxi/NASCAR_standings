import psycopg2

conn = psycopg2.connect(database="postgres", user="postgres", password="111", host="localhost", port=5432)


cursor = conn.cursor()

# Создаем таблицу Users
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users (
    id INTEGER PRIMARY KEY,
    username VARCHAR(20) NOT NULL,
    age INTEGER
)
''')

cursor.execute("""
    INSERT INTO users (id, username, age)
    VALUES (1, 'juuxi', 19)
""")

cursor.execute("""
    INSERT INTO users (id, username, age)
    VALUES (2, 'Z', 21)
""")

# Сохраняем изменения и закрываем соединение
conn.commit()
conn.close()