import tornado.ioloop
import tornado.web
import os
from inventory import *
import logging, json
from database.session_manager import SessionManager
from database.video_writer import VideoWriter


log = logging.getLogger(__name__)
sm = SessionManager()
vw = VideoWriter()

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Server is on")


class Upload(tornado.web.RequestHandler):
    def post(self):
        success = True
        session_id = self.get_argument('session_id')
        camera_idx = self.get_argument('camera_idx')
        file_path = 'tmpdata/' + str(session_id) + '/' + str(camera_idx)
        if not os.path.exists(os.path.abspath(file_path)):
            os.mkdir(file_path)
        for f, data in self.request.files.items():
            filename = f
            data_to_write = data[0].body
            with open(os.path.abspath(file_path + '/' + filename), 'wb') as f:
                f.write(data_to_write)
            if self.check_file_exist(filename, session_id) == False:
                success = False
                break
        response = {'success': success}
        self.finish(json.dumps(response))


    def check_file_exist(self, filename, session_id):
        filepath = os.path.abspath('./tmpdata/' + str(session_id) + '/' + filename)
        return os.path.isfile(filepath)


class VideoSessionStart(tornado.web.RequestHandler):
    def get(self):
        self.finish('Video Session Start is up and running')

    def post(self):
        customer_id = self.get_argument('customer_id')
        pod_id = self.get_argument('pod_id')
        start_time = self.get_argument('start_time')
        res = sm.create_session(customer_id, pod_id, start_time)
        os.mkdir('tmpdata/%s' % res)
        response = {
            'session_id': res
        }
        self.finish(json.dumps(response))

class VideoSessionEnd(tornado.web.RequestHandler):
    def get(self):
        self.finish('Video Session End is up and running')

    def post(self):
        session_id = self.get_argument('session_id')
        end_time = self.get_argument('end_time')
        duration = self.get_argument('duration')
        cameras = eval(self.get_argument('cameras'))
        cmd = 'sh concat_videos.sh tmpdata/%s' % (session_id)
        os.system(cmd)
        sm.end_session(session_id, end_time, duration)
        for idx in cameras:
            vw.write_video_to_db(session_id, idx)



class ViewSessionHandler(tornado.web.RequestHandler):
    def get(self, session_id):
        videos = vw.get_videos_by_session_id(int(session_id))
        session = sm.render_session2(sm.get_session_by_id(int(session_id)))
        v1 = str(videos[0]['session_id']) + '_' + str(videos[0]['local_camera_idx'])
        src1 = self.static_url('videos/%s.mp4' % v1)
        v2 = str(videos[1]['session_id']) + '_' + str(videos[1]['local_camera_idx'])
        src2 = self.static_url('videos/%s.mp4' % v2)
        return self.render('viewsession.html', src1=src1, src2=src2, session=session)


class SessionListHandler(tornado.web.RequestHandler):
    def get(self):
        return self.render("sessionlist.html", sessions=sm.render_sessions(sm.get_all_sessions()))


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/upload", Upload),
        (r"/createsession", VideoSessionStart),
        (r"/endsession", VideoSessionEnd),
        (r"/dashboard/viewsession/([^/]+)", ViewSessionHandler),
        (r"/dashboard/sessionlist", SessionListHandler),

    ],
        cookie_secret="DeepMagic",
        template_path=os.path.join(os.path.dirname(__file__), "templates"),

        static_path = os.path.join(os.path.dirname(__file__), "static"),
    )

if __name__ == "__main__":
    logging.basicConfig(format='%(levelname)s - %(asctime)s - %(message)s', level=logging.DEBUG)
    app = make_app()
    app.listen(BASE_PORT, '0.0.0.0')
    log.info("app is listening on %d", BASE_PORT)
    tornado.ioloop.IOLoop.current().start()