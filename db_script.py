import sqlite3
from random import randint

conn = None
cursor = None

def open():
    global conn, cursor
    conn = sqlite3.connect("quiz.db")
    cursor = conn.cursor()


def close():
    cursor.close()
    conn.close()

def check_answer(q_id, ans_text):
    query = '''
            SELECT question.answer 
            FROM quiz_content, question 
            WHERE quiz_content.id = ? 
            AND quiz_content.question_id = question.id
        '''
    open()
    cursor.execute(query, str(q_id))
    result = cursor.fetchone()
    close()
    # print(result)
    if result is None:
        return False # не нашли
    else:
        if result[0] == ans_text:
            return True # ответ совпал
        else:
            return False

def clear_db():
    global conn, cursor
    cursor.execute('''DROP TABLE IF EXISTS question''')
    conn.commit()

    cursor.execute('''DROP TABLE IF EXISTS quiz''')
    conn.commit()

    cursor.execute('''DROP TABLE IF EXISTS quiz_content''')
    conn.commit()

def create_db():
    global conn, cursor
    cursor.execute('''PRAGMA foreign_keys = ON''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS question(
        id INTEGER PRIMARY KEY,
        question VARCHAR,
        answer VARCHAR,
        wrong1 VARCHAR,
        wrong2 VARCHAR,
        wrong3 VARCHAR
    )''')

    conn.commit()

    cursor.execute('''CREATE TABLE IF NOT EXISTS quiz(
        id INTEGER PRIMARY KEY,
        name VARCHAR,
        age_from INTEGER,
        age_to INTEGER
    )''')
    conn.commit()

    cursor.execute('''CREATE TABLE IF NOT EXISTS quiz_content(
        id INTEGER PRIMARY KEY,
        question_id INTEGER,
        quiz_id INTEGER,
        FOREIGN KEY(question_id) REFERENCES question(id),
        FOREIGN KEY(quiz_id) REFERENCES quiz(id)
    )''')

def add_questions():
    global conn, cursor
    questions = [
            ('Сколько месяцев в году имеют 28 дней?', 'Все', 'Один', 'Ни одного', 'Два'),
            ('Каким станет зелёный утёс, если упадёт в Красное море?', 'Мокрым', 'Красным', 'Не изменится', 'Фиолетовым'),
            ('Какой рукой лучше размешивать чай?', 'Ложкой', 'Правой', 'Левой', 'Любой'),
            ('Что не имеет длины, глубины, ширины, высоты, а можно измерить?', 'Время', 'Глупость', 'Море', 'Воздух'),
            ('Когда сетью можно вытянуть воду?', 'Когда вода замерзла', 'Когда нет рыбы', 'Когда уплыла золотая рыбка', 'Когда сеть порвалась'),
            ('Что больше слона и ничего не весит?', 'Тень слона', 'Воздушный шар', 'Парашют', 'Облако')
        ]

    cursor.executemany('''INSERT INTO question(question, answer, wrong1, wrong2, wrong3) VALUES(?,?,?,?,?)''', questions)
    conn.commit()

def add_quiz():
    global conn, cursor
    quizes = [
            ('Своя игра', 2,6),
            ('Кто хочет стать миллионером?', 7,9),
            ('Самый умный', 8, 10)
        ]

    cursor.executemany('''INSERT INTO quiz(name, age_from, age_to) VALUES(?,?,?)''', quizes)
    conn.commit()

def add_links():
    links = [
            (2,1),
            (2,3),
            (1,3),
            (6,3),
            (4,1),
            (3,1),
            (5,2),
            (6,2),
            (3,2)
        ]

    cursor.executemany('''INSERT INTO quiz_content(question_id, quiz_id) VALUES(?,?)''', links)
    conn.commit()

def get_question_after(question_id = 0, quiz_id=1):
    global conn, cursor
    conn = sqlite3.connect("quiz.db")
    cursor = conn.cursor()
    query = '''
    SELECT quiz_content.id, question.question, question.answer, question.wrong1, question.wrong2, question.wrong3
    FROM question, quiz_content
    WHERE quiz_content.question_id == question.id
    AND quiz_content.id > ? AND quiz_content.quiz_id == ?
    ORDER BY quiz_content.id '''
    cursor.execute(query, [question_id, quiz_id] )
    result = cursor.fetchone()
    conn.commit()
    cursor.close()
    conn.close()
    return result

def get_quises():
    query = 'SELECT * FROM quiz ORDER BY id'
    open()
    cursor.execute(query)
    result = cursor.fetchall()
    close()
    return result

def get_random_quiz_id():
    query = 'SELECT quiz_id FROM quiz_content'
    open()
    cursor.execute(query)
    ids = cursor.fetchall()
    rand_num = randint(0, len(ids) - 1)
    rand_id = ids[rand_num][0]
    close()
    return rand_id


def main():
    global conn, cursor
    conn = sqlite3.connect('quiz.db')
    cursor = conn.cursor()
    print(cursor)
    clear_db()
    create_db()
    add_questions()
    add_quiz()
    add_links()
    print(get_question_after(2,1))

if __name__ == '__main__':
    main()

