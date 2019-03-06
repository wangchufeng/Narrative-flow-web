import tornado.ioloop
import tornado.httpserver
import tornado.web
import tornado.gen
import time
import datetime as dt
class SleepHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def get(self):
        yield tornado.gen.sleep(5)
        self.write(str(dt.datetime.now()))


if __name__ == "__main__":
    app = tornado.web.Application(
        [
            (r"/sleep",SleepHandler)
        ],
        debug = True
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(12345)
    tornado.ioloop.IOLoop.instance().start()