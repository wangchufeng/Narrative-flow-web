import tornado.web
from handlers import user as user_handlers
from handlers import showPic
import tornado.httpserver
import os


HANDLERS = [
    (r"/api/users", user_handlers.UserListHandler),
    (r"/",showPic.ShowPicHandler),
    (r"/select",showPic.Select_picHandler),
    (r"/start",showPic.StartHandler),
    (r"/goodpic",showPic.GoodPicHandler)
]
# settings = {
#     "static_path":"D:/Git_repository/Narrative-flow-web/demo1/data/pic_data"
# }
def run():
    app = tornado.web.Application(
        HANDLERS,
        template_path = os.path.join(
            os.path.dirname(__file__),"template"
        ),
        static_path = os.path.join(os.path.dirname(__file__),"./"),
        debug = True
    )
    http_server = tornado.httpserver.HTTPServer(app)
    app.listen(12121)
    tornado.ioloop.IOLoop.instance().start()
if __name__ == "__main__":
    run()