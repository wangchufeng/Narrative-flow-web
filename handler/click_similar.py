import tornado.web
import glob
class ShowClickPicHandler(tornado.web.RequestHandler):
    def post(self):
        file_name = self.get_argument("file_name")
        file_name = file_name.split("?")[0].split("/")[-1][0:-4]
        if file_name[-3:] != "jpg":
            while (file_name[0] == "0"):
                file_name = file_name[1:]
        categorylist = glob.glob("./template/data/category_txt/*.txt")
        print(file_name)
        for i in categorylist:
            f = open(i, "r")
            lines = f.readlines()
            for line in lines:
                line = line.split("\n")[0]
                if file_name == str(line):
                    category = i
                    break
            f.close()
        print(category)
        pic_list = self.get_category(category, file_name)
        self.write({"status": "ok", "pic_list": pic_list})

    def get_category(self, category, file_name):
        categorylist = []
        f = open(category, "r")
        lines = f.readlines()
        lines.remove(file_name + "\n")
        for line in lines:
            line = line.split("\n")[0]
            if len(line) < 4:
                line = list(line)
                times = 4 - len(line)
                for i in range(times):
                    line.insert(0, "0")
                line = "".join(line)
            pic_id = "template/data/origin_pic/" + line + ".jpg"
            pic_id = self.static_url(pic_id)
            categorylist.append(pic_id)
        return categorylist