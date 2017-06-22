import pymysql

class DatabaseWriter:
    @staticmethod
    def make_session():
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='121328',
            db='ai_server',
            cursorclass=pymysql.cursors.DictCursor
        )
        return connection

    def execute(self, sql_statement):
        c = self.make_session()
        try:
            with c.cursor() as cursor:
                cursor.execute(sql_statement)

                c.commit()
        finally:
            c.close()