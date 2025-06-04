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

with open('team-manufacturer.csv') as f:
    reader = csv.reader(f)
    manufacturer_team = dict(reader)

conn = psycopg2.connect(database="nascar", user="juuxi", password="111", host="localhost", port=5432)

cursor = conn.cursor()

cursor.execute("""
    DROP TABLE IF EXISTS manufacturers
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS manufacturers (
    place SERIAL PRIMARY KEY,
    name VARCHAR(15),
    points INTEGER
    )
""")

cursor.execute("""
    DROP TABLE IF EXISTS teams
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS teams (
    place SERIAL PRIMARY KEY,
    name  VARCHAR(40),
    points INTEGER,  
    manufacturer VARCHAR(15),
    manufacturer_id INTEGER,
    CONSTRAINT fk_manufacturer
        FOREIGN KEY (manufacturer_id)
        REFERENCES manufacturers(place)    
)
""")

cursor.execute("""
    DROP TABLE IF EXISTS drivers
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS drivers (
    place SERIAL PRIMARY KEY,
   name VARCHAR(50) NOT NULL,
    points INTEGER,
    team VARCHAR(40),
    team_id INTEGER,
    CONSTRAINT fk_team
        FOREIGN KEY (team_id)
        REFERENCES teams(place)
)
""")

for name, point, team in zip(names, points, teams):
    cursor.execute("""
        INSERT INTO drivers (name, points, team)
        VALUES (%s, %s, %s)
    """, (name, point, team))

cursor.execute("""
    INSERT INTO teams (name, points)
    SELECT team, SUM(points) AS points FROM drivers
    GROUP BY team
    ORDER BY points DESC
""")

chevrolet_teams = manufacturer_team["Chevrolet"].split(sep="\n")
ford_teams = manufacturer_team["Ford"].split(sep="\n")
toyota_teams = manufacturer_team["Toyota"].split(sep="\n")


for manufacturer, teams in manufacturer_team.items():
    teams = teams.split('\n')

    placeholders = ', '.join(['%s'] * len(teams))
    query = f"""
        UPDATE teams
        SET manufacturer = %s
        WHERE name IN ({placeholders})
    """

    cursor.execute(query, [manufacturer] + teams)

cursor.execute("""
    SELECT * FROM teams
    ORDER BY points DESC
""")

print(cursor.fetchall())

cursor.execute("""
    INSERT INTO manufacturers (name, points)
    SELECT manufacturer, SUM(points) AS points FROM teams
    GROUP BY manufacturer
    ORDER BY points DESC
""")

cursor.execute("""
    UPDATE drivers 
    SET team_id = teams.place
    FROM teams 
    WHERE drivers.team = teams.name
""")

cursor.execute("""
    UPDATE teams 
    SET manufacturer_id = manufacturers.place
    FROM manufacturers 
    WHERE teams.manufacturer = manufacturers.name
""")

# Сохраняем изменения и закрываем соединение
conn.commit()
conn.close()