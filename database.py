import sqlite3
import os


def createTableReg():
    cursor.execute("""CREATE TABLE IF NOT EXISTS regions (
        reg_id INTEGER PRIMARY KEY AUTOINCREMENT,
        regname VARCHAR(80) NOT NULL)""")


def createTableCity():
    cursor.execute("""CREATE TABLE IF NOT EXISTS cities (
      city_id INTEGER PRIMARY KEY AUTOINCREMENT,
      cityname VARCHAR(80),
      reg_id INT NOT NULL,
      FOREIGN KEY (reg_id) REFERENCES regions(reg_id))""")


def createTableComment():
    cursor.execute("""CREATE TABLE IF NOT EXISTS comments (
    comment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    surname VARCHAR(40) NOT NULL,
    first_name VARCHAR(40) NOT NULL,
    middle_name VARCHAR(40) NOT NULL,
    reg_id INT ,
    city_id INT ,
    phone VARCHAR(11),
    email VARCHAR(40),
    content TEXT,
    FOREIGN  KEY (reg_id) REFERENCES regions(reg_id),
    FOREIGN  KEY (city_id) REFERENCES cities(city_id))""")


def fillDataRegAndCity():
    towns = [['Краснодар', 'Кропоткин', 'Славянск'], ['Ростов', 'Шахты', 'Батайск'],
             ['Ставрополь', 'Пятигорск', 'Кисловодск']]
    # Вставляем данные в таблицу
    for i, region in enumerate(['Краснодарский край', 'Ростовская область', 'Ставропольский край']):
        cursor.execute("INSERT INTO regions VALUES (NULL, ?)", (region,))
        region_id = cursor.lastrowid
        for town in towns[i]:
            cursor.execute("INSERT INTO cities VALUES (NULL, ?, ?)", (town, region_id))
            # Сохраняем изменения
    conn.commit()


def getRegions():
    cursor.execute("SELECT * FROM regions")
    return cursor.fetchall()


def getComments():
    cursor.execute("""SELECT
                comment_id,
                surname,
                first_name,
                content,
                ifnull(cityname,'Не указано'),
                ifnull(regname,'Не указано')
                 FROM comments
                 LEFT JOIN cities ON comments.city_id == cities.city_id
                 LEFT JOIN regions ON comments.reg_id == regions.reg_id""")
    return cursor.fetchall()


def deleteComment(idComment):
    try:
        cursor.execute("DELETE FROM comments WHERE comment_id = ?", (idComment,))
        conn.commit()
        return 'OK'
    except:
        return 'BAD'


def getStatRegion():
    cursor.execute("""SELECT
                    regions.reg_id ,
                    regions.regname AS state,
                    COUNT(comment_id) AS kol
                    FROM comments JOIN regions ON comments.reg_id = regions.reg_id
                    GROUP BY regions.regname
                    HAVING kol > 5 """)
    return cursor.fetchall()


def getStatCity(idRegion):
    cursor.execute("""SELECT
                        ifnull(cities.cityname,'Город не указан') AS city,
                        count(ifnull(comments.city_id,'Пусто')) AS id
                        FROM comments LEFT JOIN cities ON comments.city_id = cities.city_id
                        WHERE comments.reg_id = ?
                        GROUP BY city""", (idRegion,))
    return cursor.fetchall()


def getCities(id):
    cursor.execute("SELECT * FROM  cities WHERE reg_id = ? ", (id,))
    return cursor.fetchall()


def insertNewComment(surname, first_name, middle_name, reg_id, city_id, phone, email, content):
    try:
        query = """INSERT INTO comments
                (surname, first_name,middle_name,reg_id,city_id,phone,email,content)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?)"""
        cursor.execute(query, (surname, first_name, middle_name, reg_id, city_id, phone, email, content))
        conn.commit()
        return "OK"
    except:
        return "BAD"


not_exist = False
if not 'db.sqlite' in os.listdir(os.getcwd()):
    not_exist = True

conn = sqlite3.connect(os.path.abspath('db.sqlite'))
cursor = conn.cursor()

if not_exist:
    createTableReg()
    createTableCity()
    fillDataRegAndCity()
    createTableComment()
