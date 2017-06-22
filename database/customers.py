from .database_writer import DatabaseWriter


class Customers(DatabaseWriter):
    def __init__(self):
        DatabaseWriter.__init__(self)

    def get_customer_name_by_id(self, customer_id):
        connection = self.make_session()
        with connection.cursor() as cursor:
            sql = 'SELECT * FROM `customers` where customer_id=%s' % customer_id
            cursor.execute(sql)
            res = cursor.fetchone()

        connection.close()
        return res['customer_name']
