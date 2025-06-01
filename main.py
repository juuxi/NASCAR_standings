import psycopg2
import csv


names = []
points = []
teams = []

with open('scoreboard.csv', newline='') as f:
    reader = csv.reader(f)
    for row in reader:
        names.append(row[0])
        points.append(row[1])

with open('team-driver.csv', newline='') as f:
    reader = csv.reader(f)
    for row in reader:
        teams.append(row[1])

conn = psycopg2.connect(database="nascar", user="juuxi", password="111", host="localhost", port=5432)

cursor = conn.cursor()

cursor.execute("""
    DROP TABLE IF EXISTS drivers
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS drivers (
    place SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    points INTEGER,
    team VARCHAR(40)
)
""")

for name, point, team in zip(names, points, teams):
    cursor.execute("""
        INSERT INTO drivers (name, points, team)
        VALUES (%s, %s, %s)
    """, (name, point, team))

cursor.execute("""
    DROP TABLE IF EXISTS teams
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS teams (
    place SERIAL PRIMARY KEY,
    name  VARCHAR(40),
    points INTEGER               
)
""")

cursor.execute("""
    INSERT INTO teams (name, points)
    SELECT team, SUM(points) AS points FROM drivers
    GROUP BY team
    ORDER BY points DESC
""")

# Сохраняем изменения и закрываем соединение
conn.commit()
conn.close()