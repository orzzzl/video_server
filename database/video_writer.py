from .database_writer import DatabaseWriter
import os
from tornado import template
from .helpers import findVideoMetada



class VideoWriter(DatabaseWriter):
    def __init__(self):
        DatabaseWriter.__init__(self)

    def write_video_to_db(self, session_id, camera_idx):
        file_path = 'static/videos/%s_%s.mp4' % (session_id, camera_idx)
        assert os.path.isfile(file_path)

        duration = findVideoMetada(file_path)

        sql = 'INSERT INTO videos (file_path, local_camera_idx, duration, session_id) VALUES ("%s", %s, %s, %s)' % (file_path, camera_idx, duration, session_id)
        self.execute(sql)


    def get_videos_by_session_id(self, session_id):
        connection = self.make_session()
        with connection.cursor() as cursor:
            sql = 'SELECT * FROM `videos` where session_id=%s' % session_id
            cursor.execute(sql)
            res = cursor.fetchall()

        connection.close()
        return res
