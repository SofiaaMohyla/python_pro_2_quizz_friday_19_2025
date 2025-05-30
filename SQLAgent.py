import sqlite3


class SQLAgent:
    def __init__(self, name_db):
        self.db = sqlite3.connect(name_db)
        self.db.row_factory = sqlite3.Row

    def create_tables(self):
        cursor = self.db.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Quizz (
            quizz_id INTEGER PRIMARY KEY,
            quizz_name TEXT NOT NULL,
            description TEXT
            )
        ''')
        cursor.execute('''
                      CREATE TABLE IF NOT EXISTS Questions (
                           question_id INTEGER PRIMARY KEY,
                           quiz_id INTEGER,
                           content TEXT,
                           FOREIGN KEY (quiz_id) REFERENCES Quizz(quiz_id)
                      );
                      ''')
        cursor.execute('''
                      CREATE TABLE IF NOT EXISTS Answers (
                           answer_id INTEGER PRIMARY KEY,
                           question_id INTEGER,
                           content TEXT,
                           is_right BOOLEAN,
                           FOREIGN KEY (question_id) REFERENCES Questions(question_id)
                      );
                      ''')
        cursor.close()
        self.db.commit()




    def populate_data(self):
        cursor = self.db.cursor()

        quizzes = [
            ("Україна", "Тест на знання історії та географії України"),
            ("Python", "Основи мови програмування Python")
        ]

        ukraine_questions = [
            ("Столиця України?", [("Київ", True), ("Львів", False)]),
            ("Національна валюта України?", [("Гривня", True), ("Рубль", False)]),
            ("Найвища гора України?", [("Говерла", True), ("Піп Іван", False)]),
            ("Коли Україна стала незалежною?", [("1991", True), ("1989", False)]),
            ("Державна мова України?", [("Українська", True), ("Російська", False)]),
            ("Яке місто є портом на Чорному морі?", [("Одеса", True), ("Харків", False)]),
            ("Головний символ незалежності?", [("Тризуб", True), ("Серп і молот", False)]),
            ("Найбільша річка України?", [("Дніпро", True), ("Дністер", False)]),
            ("Національна страва?", [("Борщ", True), ("Піца", False)]),
            ("Скільки областей в Україні?", [("24", True), ("25", False)]),
        ]

        python_questions = [
            ("Що таке Python?", [("Мова програмування", True), ("Тварина", False)]),
            ("Як створити змінну в Python?", [("x = 10", True), ("int x = 10", False)]),
            ("Яке ключове слово використовується для циклу?", [("for", True), ("loop", False)]),
            ("Яке розширення файлів Python?", [(".py", True), (".java", False)]),
            ("Який тип даних для списку?", [("list", True), ("tuple", False)]),
            ("Як вивести текст?", [("print()", True), ("echo()", False)]),
            ("Як створити функцію?", [("def", True), ("function", False)]),
            ("Що таке словник у Python?", [("dict", True), ("array", False)]),
            ("Що таке None?", [("Спеціальне значення порожнечі", True), ("Тип рядка", False)]),
            ("Який оператор для додавання?", [("+", True), ("&", False)]),
        ]

        for quizz_name, description in quizzes:
            cursor.execute("INSERT INTO Quizz (quizz_name, description) VALUES (?, ?)", (quizz_name, description))
            quizz_id = cursor.lastrowid

            questions = ukraine_questions if quizz_name == "Україна" else python_questions

            for content, answers in questions:
                cursor.execute("INSERT INTO Questions (quiz_id, content) VALUES (?, ?)", (quizz_id, content))
                question_id = cursor.lastrowid
                for answer_text, is_right in answers:
                    cursor.execute("INSERT INTO Answers (question_id, content, is_right) VALUES (?, ?, ?)",
                                   (question_id, answer_text, is_right))

        cursor.close()
        self.db.commit()

    def get_all_quizzes(self):
        cursor = self.db.cursor()
        cursor.execute('SELECT * FROM Quizz')
        quizzes = cursor.fetchall()
        cursor.close()
        return quizzes

    def get_questions_for_quizz(self, quizz_id):
        cursor = self.db.cursor()
        query = 'SELECT * FROM Questions WHERE quiz_id = ?'
        cursor.execute(query, (quizz_id,))
        questions = cursor.fetchall()
        cursor.close()
        return questions

    def get_answer_for_question(self, question_id):
        cursor = self.db.cursor()
        query = 'SELECT * FROM Answers WHERE question_id = ?'
        cursor.execute(query, (question_id,))
        answers = cursor.fetchall()
        cursor.close()
        return answers
