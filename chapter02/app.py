from tornado.web import StaticFileHandler, RedirectHandler

#1. RedirectHandler
#1. 301是永久重定向， 302是临时重定向，获取用户个人信息， http://www.baidu.com https

#StaticFileHandler
import time

from tornado import web
import tornado
web.URLSpec

class MainHandler(web.RequestHandler):
    #当客户端发起不同的http方法的时候， 只需要重载handler中的对应的方法即可
    async def get(self, *args, **kwargs):
        time.sleep(5)
        self.write("hello world")

class MainHandler2(web.RequestHandler):
    #当客户端发起不同的http方法的时候， 只需要重载handler中的对应的方法即可
    async def get(self, *args, **kwargs):
        self.write("hello world2")

settings = {
    "static_path":"D:/Git_repository/Narrative-flow-web/chapter02/static"
}

if __name__ == "__main__":
    app = web.Application([
        ("/", MainHandler),
        ("/2/", RedirectHandler, {"url":"/"})
    ], debug=True, **settings)
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
