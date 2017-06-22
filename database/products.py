from .database_writer import DatabaseWriter


class Products(DatabaseWriter):
    def __init__(self):
        DatabaseWriter.__init__(self)

    def get_product_name_by_id(self, product_id):
        connection = self.make_session()
        with connection.cursor() as cursor:
            sql = 'SELECT * FROM `products` where product_id=%s' % product_id
            cursor.execute(sql)
            res = cursor.fetchone()

        connection.close()
        return res['product_name']
