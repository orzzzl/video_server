from .database_writer import DatabaseWriter


class Pods(DatabaseWriter):
    def __init__(self):
        DatabaseWriter.__init__(self)

    def get_pod_by_id(self, pod_id):
        connection = self.make_session()
        with connection.cursor() as cursor:
            sql = 'SELECT * FROM `pods` where pod_id=%s' % pod_id
            cursor.execute(sql)
            res = cursor.fetchone()

        connection.close()
        return res
