import tornado.web
import imagehash
from PIL import Image
import numpy as np
import glob

class ConditionalSearch(tornado.web.RequestHandler):
    def post(self):
        imglist = []

        category = self.get_argument("category")
        group_number = self.get_argument("group_number")
        number_index = self.get_argument("number_index")
        sketch_data = self.get_argument("sketch_data")
        data_width = self.get_argument("data_width")

        imglist = self.category_filter(category)
        imglist = self.group_number_filter(group_number, imglist)
        imglist = self.number_index_filter(number_index, imglist)
        imglist =self.sketch_data_filter(sketch_data, data_width, imglist)
        for i,img in enumerate(imglist):
            imglist[i] = self.static_url(img)
        self.write({"status": "success load", "imglist": imglist})

    def category_filter(self, category):
        if category == "all":
            path = "./template/data/pic_list.txt"
            imglist = self.get_img_list(path)
        else:
            path = "./template/data/category_txt/" + category + ".txt"
            imglist = self.get_img_list(path)
        return imglist

    def group_number_filter(self, group_number, imglist):
        if group_number == "*":
            return imglist

        filter_imglist = []
        for v in imglist:
            g_txt = v.replace("origin_pic", "group_txt")
            g_txt = g_txt[:-4]
            g_txt = g_txt + "_group.txt"
            with open(g_txt, "r") as f:
                seed = []
                lines = f.readlines()
                for line in lines[1:]:
                    line = line.split(",")
                    seed.append(line[2])
                seed_number = len(set(seed))
                if seed_number == int(group_number):
                    filter_imglist.append(v)
        return filter_imglist

    def number_index_filter(self, number_index, imglist):
        new_list = []
        if number_index == "all":
            return imglist

        if number_index == "yes":
            for img in imglist:
                file_name = "jpgjpg/" if img[-8:] == ".jpg.jpg" else "jpg/"
                label_txt = "./template/data/label_txt/" + file_name + img.split("/")[-1].split(".")[0] + ".txt"
                with open(label_txt, "r") as file:
                    lines = file.readlines()
                    for line in lines:
                        name = line.split(" ")[0]
                        if name == "z_number" or name == "number":
                            new_list.append(img)
                            break
            return new_list

        if number_index == "no":
            for img in imglist:
                file_name = "jpgjpg/" if img[-8:] == ".jpg.jpg" else "jpg/"
                label_txt = "./template/data/label_txt/" + file_name + img.split("/")[-1].split(".")[0] + ".txt"
                with open(label_txt, "r") as file:
                    lines = file.readlines()
                    flag = 0
                    for line in lines:
                        name = line.split(" ")[0]
                        if name == "z_number" or name == "number":
                            flag = 1
                    if flag == 0:
                        new_list.append(img)
            return new_list


    def sketch_data_filter(self, data, data_width, imglist):
        if data == "null":
            return imglist
        else:
            data_width = int(data_width)
            data = data.split(",")
            np_img = np.array(data).reshape(data_width, data_width, 4)
            np_img = np.asarray(np_img, dtype=np.uint8)
            im = Image.fromarray(np_img, 'RGBA')
            im = im.resize((100, 100))
            gray = im.convert('L')
            gray.save("1.jpg")

            im_hash = self.read_vnf_flow_hash('1.jpg')
            distance = []
            flow_name = []
            for i in imglist:
                flow_path = i.replace("origin_pic", "flow_pic")
                flow_path = flow_path[:-4]
                flow_path = flow_path + "_flow.png"
                flow_name.append(flow_path)

            for i in flow_name:
                i = self.read_vnf_flow_hash(i)
                distance.append(self.hammingDistance(i, im_hash))
            flow_index = list(self.similarest_pic(distance))
            pic_list = []
            for i in flow_index:
                flow_name[i] = flow_name[i].replace("_flow.png", ".jpg")
                flow_name[i] = flow_name[i].replace("flow_pic", "origin_pic")
                flow_name[i] = flow_name[i].replace("\\", "/")
                pic_list.append(flow_name[i])
            return pic_list


    def hammingDistance(self, x, y):
        x = int(str(x), 16)
        y = int(str(y), 16)
        hamming_distance = 0
        s = str(bin(x ^ y))
        for i in range(2, len(s)):
            if int(s[i]) is 1:
                hamming_distance += 1
        a = 1 - hamming_distance / 64
        return a

    def read_vnf_flow_hash(self, filename):
        hash_str = imagehash.average_hash(Image.open(filename))
        return hash_str

    # 求出相似最高的前x个
    def similarest_pic(self, n):
        similar_n = 300
        Inf = 0
        _index = []
        for i in range(similar_n):
            _index.append(n.index(max(n)))
            n[n.index(max(n))] = Inf
        print(_index)
        return _index


    def get_img_list(self, path):
        imglist = []
        with open(path, "r") as f:
            lines = f.readlines()
            for line in lines:
                pic = line.split("\n")[0]
                imglist.append(pic)
        return imglist