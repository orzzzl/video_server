from .database_writer import DatabaseWriter
from tornado import template
from .customers import Customers

session_entity_html = '''
    <tr>
        <td> {{session_id}} </td>
        <td> {{start_time}} </td>
        <td> {{end_time}} </td>
        <td> {{duration}} </td>
        <td> {{pod_id}} </td>
        <td> {{customer_name}} </td>
        <td> <a href='/dashboard/viewsession/{{session_id}}'> view </a> </td>
    </tr>
'''

html_str = """
<div class="content">
    <span class="col-md-4"> <label>Session ID:</label> <span>{{session_id}}</span> </span>
    <span class="col-md-4"> <label>Pod ID:</label> <span>{{pod_id}}</span> </span>
    <span class="col-md-4"> <label>Customer Name:</label> <span>{{customer_name}}</span> </span>
    <br>
    <span class="col-md-4"> <label>Start Time:</label> <span>{{start_time}}</span> </span>
    <span class="col-md-4"> <label>End Time:</label> <span>{{end_time}}</span> </span>
    <span class="col-md-4"> <label>Duration:</label> <span>{{duration}}</span></span>
    <br>
    <span class="col-md-4"> <label>Pod Address:</label> <span>625 6AV, New York, 10011</span></span>
    <span class="col-md-4"> <label>Merchant id:</label> <span>0</span></span>
    <span class="col-md-4"> <label>Merchant name:</label> <span>Zeleng Zhuang</span></span>
    <br>
    <br>
</div>
"""

class SessionManager(DatabaseWriter):
    def __init__(self):
        DatabaseWriter.__init__(self)
        self._customer = Customers()
        self.html_template = template.Template(session_entity_html)
        self.html_template2 = template.Template(html_str)

    def create_session(self, customer_id, pod_id, start_time):
        connection = self.make_session()
        with connection.cursor() as cursor:
            sql = 'INSERT INTO `sessions` (`customer_id`, `pod_id`, `start_time`) VALUES (%s, %s, "%s")'
            cursor.execute(sql % (customer_id, pod_id, start_time))

        connection.commit()

        with connection.cursor() as cursor:
            sql = 'SELECT LAST_INSERT_ID();'
            cursor.execute(sql)
            res = cursor.fetchone()

        connection.close()
        return res['LAST_INSERT_ID()']


    def end_session(self, session_id, end_time, duration):
        sql = 'UPDATE sessions SET end_time="%s", duration="%s" WHERE session_id=%s' % (end_time, duration, session_id)
        self.execute(sql)



    def get_all_sessions(self):
        connection = self.make_session()
        with connection.cursor() as cursor:
            sql = 'SELECT * FROM `sessions` WHERE end_time IS NOT NULL ORDER BY session_id DESC'
            cursor.execute(sql)
            res = cursor.fetchall()

        connection.close()
        return res

    def get_session_by_id(self, session_id):
        connection = self.make_session()
        with connection.cursor() as cursor:
            sql = 'SELECT * FROM `sessions` WHERE session_id=%s' % session_id
            cursor.execute(sql)
            res = cursor.fetchone()

        connection.close()
        return res

    def render_session(self, session):
        return self.html_template.generate(session_id=session['session_id'],
                                           start_time=session['start_time'],
                                           end_time=session['end_time'],
                                           customer_name=self._customer.get_customer_name_by_id(session['customer_id']),
                                           pod_id=session['pod_id'],
                                           duration=session['duration'][:7]
        )

    def render_session2(self, session):
        return self.html_template2.generate(session_id=session['session_id'],
                                           start_time=session['start_time'],
                                           end_time=session['end_time'],
                                           customer_name=self._customer.get_customer_name_by_id(session['customer_id']),
                                           pod_id=session['pod_id'],
                                           duration=session['duration'][:7]
        )

    def render_sessions(self, sessions):
        res = []
        for session in sessions:
            res.append(self.render_session(session))
        return res
