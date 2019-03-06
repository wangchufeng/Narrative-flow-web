import tornado.web
from tornado.escape import json_encode
from models.user import UserModel
from tornado.web import RequestHandler, MissingArgumentError
import json

class ShowPicHandler(tornado.web.RequestHandler):
    def get(self):
        # msg = "/static/data/pic_data/"+ str(id) +".jpg"
        # pic_id = int(self.get_argument('pic_id'));
        # self.write({
        #     'pic_id':pic_id,
        # })
        self.render("index.html")
    def post(self):
        # pic_id = self.get_argument('formData')
        # pic_path = "./pic_data/"+str(pic_id) +".jpg"
        # try:
        # pic_ = self.get_argument("pic_id")
        # print("pic_id",pic_id)
        # self.write({
        #     'pic_id':pic_id,
        # })
        pass
        # except MissingArgumentError as e:
            # pass
        # self.render("index.html",msg = "")

class Select_picHandler(tornado.web.RequestHandler):
    def post(self):
        pic_ = self.get_argument("pic_id",None)
        path = 'data/pic_data/'+str(pic_)+'.jpg'
        path = self.static_url(path)
        print(path)
        self.write({"pic_path":path})
        