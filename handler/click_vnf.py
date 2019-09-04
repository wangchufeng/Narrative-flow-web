import tornado.web

class ShowPicFlowHandler(tornado.web.RequestHandler):
    def post(self):
        pic_flow = self.get_argument("pic_flow")
        seed_id = self.get_argument("seed_id")
        # print(pic_flow)
        # pic_flow = pic_flow.split("?")[0].split("/")[-1].split(".")[0]
        print(pic_flow)
        category = "./template/data/category_txt/" + pic_flow + ".txt"
        categorylist = []
        f = open(category, "r")
        lines = f.readlines()
        print("the input is: ", seed_id)
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
            if seed_id == "none":
                print(pic_id)
                categorylist.append(pic_id)
            else:
                seed_number = []
                group_txt = "template/data/group_txt/" + line + "_group.txt"
                group_txt = open(group_txt, "r")
                g_lines = group_txt.readlines()
                for g_line in g_lines:
                    g_line = g_line.split(",")[2]
                    seed_number.append(g_line)
                seed_number = len(set(seed_number)) - 1
                print("seed_number is: ", seed_number)
                if int(seed_id) - seed_number == 0:
                    print("yeah!!!!!!!")
                    categorylist.append(pic_id)

        print(len(categorylist))
        self.write({"status": "true", "categorylist": categorylist, "pic_number": len(categorylist)})
