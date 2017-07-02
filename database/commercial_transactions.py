from .database_writer import DatabaseWriter

class CommercialTransactions(DatabaseWriter):

    def get_transactions_by_session_id(self, session_id):
        connection = self.make_session()
        with connection.cursor() as cursor:
            sql = 'select * from commercial_transactions where session_id=%s' % session_id
            cursor.execute(sql)
            res = cursor.fetchall()

        connection.close()
        return res


    def render(self, transaction):
        return '<tr style="cursor:pointer;" class="event_row" value="%s" onclick="set_video_time(%s)"><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % (transaction['time_stamp'], transaction['time_stamp'], transaction['commercial_transaction_id'], transaction['time_stamp'], transaction['action'], transaction['item_name'], transaction['EAN'], transaction['catagory'])


    def render_all(self, session_id):
        transactions = self.get_transactions_by_session_id(session_id)
        ans = []
        for t in transactions:
            ans.append(self.render(t))
        return ans