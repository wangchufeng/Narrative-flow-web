import imagehash
import tornado.web
import glob
import csv
import numpy as np
import pandas as pd
import heapq
from PIL import Image
import shutil


class ShowSimilarPicHandler(tornado.web.RequestHandler):
    def post(self):
        similar_pic = self.get_argument("similar_pic")
        jpg_list, flow_list = self.similar_pic(similar_pic)
        img_list = []
        for i in jpg_list:
            jpgname = self.static_url(i)
            img_list.append(jpgname)
        self.write({"status": "ok", "img_list": img_list})

    def similar_pic(self, img):
        print(img)
        file = open('./template/data/pca.csv', 'r')
        lines = file.readlines()
        file.close()
        row = []  # 定义行数组
        column = []  # 定义列数组
        for line in lines:
            row.append(line.split(','))
        dist_list = []
        img_list = []
        file_index = np.where(np.array(row) == img)
        # print(file_index[0])
        # print(row[file_index[0][0]].pop(0))
        r1 = np.array(row[file_index[0][0]])
        r1 = r1.astype(float)

        for x in range(1, len(row)):
            ###
            name = row[x].pop(0)
            if x == file_index[0][0]:
                continue
            if len(name) < 4:
                for times in range(4 - len(name)):
                    name = "0" + name
            name = "./flow_pic/" + name + "_flow.png"
            img_list.append(name)
            r2 = np.array(row[x])
            r2 = r2.astype(float)
            dist = np.sqrt(np.sum(np.square(r1 - r2)))
            dist_list.append(dist)

        max_num_index_list = map(dist_list.index, heapq.nsmallest(300, dist_list))
        jpg_list = []
        file_list = []
        for i in max_num_index_list:
            filename = img_list[i].split("/")[-1]
            file_path = r"./template/data/flow_pic/"
            file_path = file_path + filename
            file_list.append(file_path)
            jpg_file = "./template/data/origin_pic/" + filename.split("_flow")[0] + ".jpg"
            jpg_list.append(jpg_file)
        return jpg_list, file_list


class ShowDrawSelectHandler(tornado.web.RequestHandler):
    vnf_flow_path = "./template/icon/*.png"
    def post(self):
        # 降采样
        data = self.get_argument("data")
        Group_Number = self.get_argument("Group_Number")
        Number_Index = self.get_argument("Number_Index")
        data_width = int(self.get_argument("Data_Width"))
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
        flow_path = "./template/data/flow_pic/*_flow.png"
        for i in glob.glob(flow_path):
            flow_name.append(i)
        for i in flow_name:
            i = self.read_vnf_flow_hash(i)
            distance.append(self.hammingDistance(i, im_hash))
        flow_index = list(self.similarest_pic(distance))
        pic_list = []
        for i in flow_index:
            flow_name[i] = flow_name[i].replace("_flow.png", ".jpg")
            flow_name[i] = flow_name[i].replace("flow_pic", "origin_pic")
            flow_name[i] = flow_name[i].replace("\\", "/")
            flow_name[i] = self.static_url(flow_name[i])
            pic_list.append(flow_name[i])

            # sim_pic = Image.open(flow_name[i])
            # sim_pic.show()

        # pic = np.array(gray)
        # self.read_csv(pic)
        # pic_list = self.compute_pca(Group_Number,Number_Index)

        self.write({"status": "ok", "pic_list": pic_list})
        # self.write({"status": "ok"})

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
        # max_similar = list(heapq.nlargest(similar_n, n))
        # for similar_n in max_similar:
        #     _temp_index = [i for i, x in enumerate(max_similar) if i == similar_n]
        #     print(_temp_index)
        #     _index = _index + _temp_index
        Inf = 0
        _index = []
        for i in range(similar_n):
            _index.append(n.index(max(n)))
            n[n.index(max(n))] = Inf
        print(_index)
        # max_num_index_list = map(n.index, heapq.nlargest(20, n))
        # _index = list(set(max_num_index_list))

        return _index

    def read_csv(self, pic):
        pic = pic.reshape(10000, )
        pic = pic.tolist()
        file = open('./template/data/pixel.csv', 'r')
        lines = file.readlines()
        str_0 = len(lines) - 1
        file.close()
        file = open('./template/data/pixel.csv', 'a')
        csv_write = csv.writer(file, dialect='excel')
        pic.insert(0, str_0)
        pic.append("test")
        csv_write.writerow(pic)
        file.close()

    def compute_pca(self, Group_Number, Number_Index):
        CSV_FILE_PATH = './template/data/pixel.csv'
        df = pd.read_csv(CSV_FILE_PATH)
        img_list = df['imgName'].values
        df = df.drop(columns=['index', 'imgName'])
        # X = df.values.tolist()
        # df = pd.DataFrame(X, columns=feat_cols)
        featureNum = 50
        pca = PCA(n_components=featureNum)
        pca_result = pca.fit_transform(df.values)
        print(pca_result.shape)
        dist_list = []
        object_pic = pca_result[-1]
        for i in range(pca_result.shape[0] - 1):
            dist = np.sqrt(np.sum(np.square(pca_result[i] - object_pic)))
            dist_list.append(dist)

        max_num_index_list = map(dist_list.index, heapq.nsmallest(600, dist_list))
        pic_list = []
        print("Number_Index: ", Number_Index)
        for i in max_num_index_list:
            img = str(img_list[i])
            for x in range(4 - len(img)):
                img = "0" + img

            if Group_Number != "undefined":
                seed_number = []
                group_txt = "template/data/group_txt/" + img + "_group.txt"
                group_txt = open(group_txt, "r")
                g_lines = group_txt.readlines()
                group_txt.close()
                for g_line in g_lines:
                    g_line = g_line.split(",")[2]
                    seed_number.append(g_line)
                seed_number = len(set(seed_number)) - 1
                if int(Group_Number) - seed_number != 0:
                    continue

            shaobin = 0
            if Number_Index == "1":
                if img[-1] != "g":
                    f = open("template/data/label_txt/jpg/" + img + ".txt", "r")
                    label_line = f.readlines()
                    f.close()
                    for line in label_line:
                        name = line.split(" ")[0]
                        if name == "z_number" or name == "number":
                            shaobin = 1
                if shaobin == 0:
                    print("yes")
                    continue

            if Number_Index == "2":
                if img[-1] != "g":
                    f = open("template/data/label_txt/jpg/" + img + ".txt", "r")
                    label_line = f.readlines()
                    f.close()
                    for line in label_line:
                        name = line.split(" ")[0]
                        if name == "z_number" or name == "number":
                            shaobin = 1
                if shaobin == 1:
                    print("no")
                    continue

            img = 'template/data/origin_pic/' + img + ".jpg"
            img = self.static_url(img)
            pic_list.append(img)
        return (pic_list)








