import tornado.web
from tornado.escape import json_encode
from models.user import UserModel
from tornado.web import RequestHandler
import json
import os
class BaseHandler(tornado.web.RequestHandler):
    # 这是自己定义的基类,业务类继承这个基类
    def __init__(self, *argc, **kwarg):
        super(BaseHandler, self).__init__(*argc, **kwarg)

    def get_current_user(self):
        return self.get_secure_cookie("user")

    def get(self):
        self.send_error(404)
    
    def mywrite(self, chunk):
    # 定义自己实现的write()方法
        if self._finished:
            raise RuntimeError("Cannot write() after finish()")
        if not isinstance(chunk, (unicode_type, list, dict)):
            message = "write() only accepts bytes, unicode, list and dict objects"
            raise TypeError(message)
        if isinstance(chunk, (list, dict)):
            chunk = json.dumps(chunk).replace("</", "<\\/")
            self.set_header("Content-Type", "application/json; charset=UTF-8")
        chunk = utf8(chunk)
        self._write_buffer.append(chunk)

    def write_error(self, status_code, **kwargs):
        if status_code == 404:
            self.render('public/404.html')
        elif status_code == 500:
            self.render('public/500.html')
        else:
            self.write('error' + str(status_code))

class ShowPicHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")
    def post(self):
        pass


class Select_picHandler(tornado.web.RequestHandler):
    def post(self):
        # pic_path
        pic_ = self.get_argument("pic_id",None)
        pic_path = 'data/pic_data/'+str(pic_)+'.jpg'
        pic_path = self.static_url(pic_path)
        print("pic_path",pic_path)
        # label_path
        label_path = 'data/label_data/'+str(pic_)+'.jpg'
        label_path = self.static_url(label_path)
        print("label_path",label_path)
        self.write({"label_path":label_path,
            "pic_path":pic_path})

class StartHandler(BaseHandler):
    def post(self):
        path = "./data/pic_data/"
        for root,dirs,files in os.walk(path):
            pass
        pic_path =[]
        label_path = []
        for file in files:
            pic_ = 'data/pic_data/'+file
            label_ = 'data/label_data/'+file
            pic_ = self.static_url(pic_)
            label_ = self.static_url(label_)
            pic_path.append(pic_)
            label_path.append(label_)
        self.write({"pic_path":pic_path,
            "label_path":label_path})