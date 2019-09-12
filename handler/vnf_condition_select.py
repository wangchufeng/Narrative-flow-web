import tornado.web


class QueryHandler(tornado.web.RequestHandler):
    def post(self):
        category_now = self.get_argument("category_now")
        Group_Number = self.get_argument("Group_Number")
        # Textbox_Orientation = self.get_argument("Textbox_Orientation")
        Number_Index = self.get_argument("Number_Index")

        f = open("template/data/category_txt/" + category_now + ".txt", "r")
        img_list = f.readlines()
        f.close()

        if Group_Number != "":
            for i in img_list:
                img_name = i.split("\n")[0]
                if img_name[-1] != "g":
                    for x in range(4 - len(img_name)):
                        img_name = "0" + img_name
                seed_number = []
                group_txt = "template/data/group_txt/" + img_name + "_group.txt"
                group_txt = open(group_txt, "r")
                g_lines = group_txt.readlines()
                group_txt.close()
                for g_line in g_lines:
                    g_line = g_line.split(",")[2]
                    seed_number.append(g_line)
                seed_number = len(set(seed_number)) - 1
                print(group_txt, seed_number)
                if int(Group_Number) - seed_number != 0:
                    img_list.remove(i)  ##  has "\n"

        new_list = []
        if Number_Index == "1":
            for i in img_list:
                img_name = i.split("\n")[0]
                if img_name[-1] != "g":
                    for x in range(4 - len(img_name)):
                        img_name = "0" + img_name
                    f = open("template/data/label_txt/jpg/" + img_name + ".txt", "r")
                    label_line = f.readlines()
                    f.close()
                    for line in label_line:
                        name = line.split(" ")[0]
                        if name == "z_number" or name == "number":
                            new_list.append(i)
                            break
            img_list = new_list

        if Number_Index == "2":
            for i in img_list:
                img_name = i.split("\n")[0]
                if img_name[-1] != "g":
                    for x in range(4 - len(img_name)):
                        img_name = "0" + img_name
                    f = open("template/data/label_txt/jpg/" + img_name + ".txt", "r")
                    label_line = f.readlines()
                    f.close()
                    shaobin = 0
                    for line in label_line:
                        name = line.split(" ")[0]
                        if name == "z_number" or name == "number":
                            shaobin = 1
                    if shaobin == 0:
                        new_list.append(i)
            img_list = new_list

        result = []
        for i in img_list:
            img_name = i.split("\n")[0]
            if len(img_name) < 4:
                for x in range(4 - len(img_name)):
                    img_name = "0" + img_name
            img = "template/data/origin_pic/" + img_name + ".jpg"
            img = self.static_url(img)
            result.append(img)
        self.write({"status": "ok", "pic_list": result})
