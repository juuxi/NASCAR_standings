import psycopg2
import csv


names = []
points = []

with open('scoreboard.csv', newline='') as f:
    reader = csv.reader(f)
    for row in reader:
        names.append(row[0])
        points.append(row[1])

conn = psycopg2.connect(database="nascar", user="juuxi", password="111", host="localhost", port=5432)

cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS drivers (
    place INTEGER PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    points INTEGER,
    team VARCHAR(40)
)
""")

for i in range(len(names)):
    cursor.execute("""
        INSERT INTO drivers (place, name, points, team)
        VALUES (%s, %s, %s, %s)
    """, (i, names[i], points[i], 'None'))

# Сохраняем изменения и закрываем соединение
conn.commit()
conn.close()