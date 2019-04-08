import tornado
import os
from handler import showPic
URL = [
    tornado.web.URLSpec("/",showPic.ShowPicHandler),
    tornado.web.URLSpec("/showallpic",showPic.ShowAllPicHandler),
    tornado.web.URLSpec("/onepic",showPic.ShowOnePicHandler),
    tornado.web.URLSpec("/picflow",showPic.ShowPicFlowHandler),
    tornado.web.URLSpec("/similar_pic",showPic.ShowSimilarPicHandler),
    tornado.web.URLSpec("/draw_select",showPic.ShowDrawSelectHandler),
    tornado.web.URLSpec("/click_pic",showPic.ShowClickPicHandler),
    tornado.web.URLSpec("/query",showPic.QueryHandler),
]

def run():
    app = tornado.web.Application(
        URL,
        template_path = os.path.join(
            os.path.dirname(__file__),"template"
        ),
        static_path = os.path.join(
            os.path.dirname(__file__),"./"
        ),
        debug = True
    )
    http_server = tornado.httpserver.HTTPServer(app)
    app.listen(12121)
    tornado.ioloop.IOLoop.instance().start()
if __name__ == "__main__":
    run()