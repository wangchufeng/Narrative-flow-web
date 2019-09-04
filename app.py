import tornado
import os
from handler import showPic
from handler import draw_select
from handler import click_similar
from handler import click_vnf
from handler import vnf_condition_select
URL = [
    tornado.web.URLSpec("/", showPic.ShowPicHandler),
    tornado.web.URLSpec("/showallpic", showPic.ShowAllPicHandler),
    tornado.web.URLSpec("/onepic", showPic.ShowOnePicHandler),
    tornado.web.URLSpec("/picflow", click_vnf.ShowPicFlowHandler),
    tornado.web.URLSpec("/similar_pic",draw_select.ShowSimilarPicHandler),
    tornado.web.URLSpec("/draw_select", draw_select.ShowDrawSelectHandler),
    tornado.web.URLSpec("/click_pic", click_similar.ShowClickPicHandler),
    tornado.web.URLSpec("/query", vnf_condition_select.QueryHandler),
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
