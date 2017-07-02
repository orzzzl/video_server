from .database_writer import DatabaseWriter


class Merchants(DatabaseWriter):
    def __init__(self):
        DatabaseWriter.__init__(self)

    def get_merchant_name_by_id(self, merchant_id):
        connection = self.make_session()
        with connection.cursor() as cursor:
            sql = 'SELECT * FROM `merchants` where merchant_id=%s' % merchant_id
            cursor.execute(sql)
            res = cursor.fetchone()

        connection.close()
        return res['merchant_name']
