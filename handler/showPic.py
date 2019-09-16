import tornado.web


class ShowPicHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")


class ShowAllPicHandler(tornado.web.RequestHandler):
    def post(self):
        imglist = []
        print("Loading...")
        with open("./template/data/pic_list.txt","r") as f:
            lines = f.readlines()
            for line in lines:
                pic = line.split("\n")[0]
                pic = self.static_url(pic)
                imglist.append(pic)
        self.write({"status": "success load", "imglist": imglist})


class ShowOnePicHandler(tornado.web.RequestHandler):
    def post(self):
        pic_id = self.get_argument("pic_id")
        f = open("./template/data/pic_list.txt", "r")
        lines = f.readlines()
        pic_url = 0
        for line in lines:
            if pic_id == line.split("/")[-1].split("\n")[0]:
                pic_url = line.split("\n")[0]
                pic_url = self.static_url(pic_url)
        if pic_url:
            self.write({"status": "true", "pic_id": pic_url})
        else:
            self.write({"status": "false"})
