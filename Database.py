import mysql.connector


class Database:
    def __init__(self, configs):
        try:
            self.mydb = mysql.connector.connect(
                host=configs['host'],
                user=configs['user'],
                password=configs['password'],
                database=configs['database-name']
            )
            print('Connected')
            self.cursor = self.mydb.cursor()
        except Exception as ex:
            print(ex)

    def insert_log(self, in_message):
        try:
            self.cursor.execute('INSERT INTO log (content) VALUES (%s)', [in_message])
            self.mydb.commit()
        except Exception as ex:
            print(ex)

    def insert_student(self, std_id, userid):
        try:
            self.cursor.execute('INSERT INTO student_users (std_id, username) VALUES (%s, %s)', [std_id, userid])
            self.mydb.commit()
        except Exception as ex:
            print(ex)

    def check_id(self, userid):
        try:
            self.cursor.execute('SELECT std_id FROM student_users WHERE username = %s', [userid])
            rows = self.cursor.fetchall()
            if len(rows) > 0:
                return True, rows[0][0]
        except Exception as ex:
            print(ex)
            return False, ''
        return False, ''
