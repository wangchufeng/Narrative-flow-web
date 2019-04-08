import tornado.web
import glob
import csv
import numpy as np
import pandas as pd
import heapq
from PIL import Image
import shutil
from sklearn.decomposition import PCA
import cv2
class ShowPicHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")

class ShowAllPicHandler(tornado.web.RequestHandler):
    def post(self):
        imglist = []
        print("Loading...")
        f = open("./template/data/pic_list.txt","r")
        lines = f.readlines()
        for line in lines:
            pic = line.split("\n")[0]
            pic = self.static_url(pic)
            imglist.append(pic)
        self.write({"status":"success load","imglist":imglist})

class ShowOnePicHandler(tornado.web.RequestHandler):
    def post(self):
        pic_id = self.get_argument("pic_id")
        f = open("./template/data/pic_list.txt","r")
        lines = f.readlines()
        pic_url = 0
        for line in lines:
            if pic_id == line.split("/")[-1].split("\n")[0]:
                pic_url = line.split("\n")[0]
                pic_url = self.static_url(pic_url)         
        if pic_url:
            self.write({"status":"true","pic_id":pic_url})
        else:
            self.write({"status":"false"})

class ShowPicFlowHandler(tornado.web.RequestHandler):
    def post(self):
        pic_flow = self.get_argument("pic_flow")
        seed_id = self.get_argument("seed_id")
        # print(pic_flow)
        # pic_flow = pic_flow.split("?")[0].split("/")[-1].split(".")[0]
        print(pic_flow)
        category = "./template/data/category_txt/"+pic_flow+".txt"
        categorylist = []
        f=open(category,"r")
        lines = f.readlines()
        print("the input is: ",seed_id)
        for line in lines:
            line = line.split("\n")[0]
            if len(line)<4:
                line = list(line)
                times = 4-len(line)
                for i in range(times):
                    line.insert(0,"0")
                line = "".join(line)
            pic_id = "template/data/origin_pic/"+line+".jpg"
            pic_id = self.static_url(pic_id)
            if seed_id == "none":
                print(pic_id)
                categorylist.append(pic_id)
            else:
                seed_number = []
                group_txt = "template/data/group_txt/"+line+"_group.txt"
                group_txt = open(group_txt,"r")
                g_lines = group_txt.readlines()
                for g_line in g_lines:
                    g_line = g_line.split(",")[2]
                    seed_number.append(g_line)
                seed_number = len(set(seed_number))-1
                print("seed_number is: ",seed_number)
                if int(seed_id) - seed_number==0:
                    print("yeah!!!!!!!")
                    categorylist.append(pic_id)

        print(len(categorylist))
        self.write({"status":"true","categorylist":categorylist,"pic_number":len(categorylist)})


class ShowSimilarPicHandler(tornado.web.RequestHandler):
    def post(self):
        similar_pic = self.get_argument("similar_pic")
        jpg_list,flow_list = self.similar_pic(similar_pic)
        img_list=[]
        for i in jpg_list:
            jpgname = self.static_url(i)
            img_list.append(jpgname)
        self.write({"status":"ok","img_list":img_list})

    def similar_pic(self,img):
        print(img)
        file =open('./template/data/pca.csv','r')
        lines=file.readlines()
        file.close()
        row=[]#定义行数组
        column=[]#定义列数组
        for line in lines:
            row.append(line.split(','))
        dist_list = []
        img_list = []
        file_index = np.where(np.array(row)==img)
        print(file_index[0])
        print(row[file_index[0][0]].pop(0))
        r1=np.array(row[file_index[0][0]])
        r1 = r1.astype(float)

        for x in range(1,len(row)):
            ###
            name = row[x].pop(0)
            if x == file_index[0][0]:
                continue
            if len(name) < 4:
                for times in range(4-len(name)):
                    name = "0"+name
            name = "./flow_pic/"+name+"_flow.png"
            img_list.append(name)
            r2=np.array(row[x])
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
            jpg_file = "./template/data/origin_pic/" + filename.split("_flow")[0]+".jpg"
            jpg_list.append(jpg_file)
        return jpg_list,file_list


class ShowDrawSelectHandler(tornado.web.RequestHandler):
    def post(self):
        #降采样
        data = self.get_argument("data")
        Group_Number = self.get_argument("Group_Number")
        Number_Index = self.get_argument("Number_Index")
        data = data.split(",")
        np_img = np.array(data).reshape(400,400,4)
        np_img = np.asarray(np_img, dtype=np.uint8)
        im = Image.fromarray(np_img,'RGBA')
        im = im.resize((100, 100))
        gray=im.convert('L')
        gray.save("1.jpg")
        pic = np.array(gray)
        print(pic.shape)

        pic = pic.reshape(10000,)
        pic = pic.tolist()

        file =open('./template/data/pixel.csv','r')
        lines=file.readlines()
        str_0 = len(lines)-1
        file.close()

        file =open('./template/data/pixel.csv','a')
        csv_write = csv.writer(file,dialect='excel')
        pic.insert(0,str_0)
        pic.append("test")
        csv_write.writerow(pic)
        file.close()
        pic_list = self.compute_pca(Group_Number,Number_Index)

        self.write({"status":"ok","pic_list":pic_list})

    def compute_pca(self,Group_Number,Number_Index):

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
        for i in range(pca_result.shape[0]-1):
            dist = np.sqrt(np.sum(np.square(pca_result[i] - object_pic)))
            dist_list.append(dist)

        max_num_index_list = map(dist_list.index, heapq.nsmallest(600, dist_list))
        pic_list = []
        print("Number_Index: ",Number_Index)
        for i in max_num_index_list:
            img = str(img_list[i])
            for x in range(4-len(img)):
                img="0"+img

            if Group_Number != "":
                seed_number = []
                group_txt = "template/data/group_txt/"+img+"_group.txt"
                group_txt = open(group_txt,"r")
                g_lines = group_txt.readlines()
                group_txt.close()
                for g_line in g_lines:
                    g_line = g_line.split(",")[2]
                    seed_number.append(g_line)
                seed_number = len(set(seed_number))-1
                if int(Group_Number) - seed_number != 0:
                    print("Ffafa")
                    continue

            shaobin = 0
            if Number_Index == "1":
                if img[-1] != "g":
                    f = open("template/data/label_txt/jpg/"+img+".txt","r")
                    label_line = f.readlines()
                    f.close()
                    for line in label_line:
                        name = line.split(" ")[0]
                        if  name == "z_number" or name == "number":
                            shaobin =1
                if shaobin ==0:
                    print("yes")
                    continue

            if Number_Index == "2":
                if img[-1] != "g":
                    f = open("template/data/label_txt/jpg/"+img+".txt","r")
                    label_line = f.readlines()
                    f.close()
                    for line in label_line:
                        name = line.split(" ")[0]
                        if  name == "z_number" or name == "number":
                            shaobin =1
                if shaobin == 1:
                    print("no")
                    continue


            img = 'template/data/origin_pic/'+img+".jpg"
            img = self.static_url(img)
            pic_list.append(img)
        return(pic_list)

class ShowClickPicHandler(tornado.web.RequestHandler):
    def post(self):
        file_name = self.get_argument("file_name")
        file_name = file_name.split("?")[0].split("/")[-1][0:-4]
        if file_name[-3:] != "jpg":
            while(file_name[0]=="0"):
                file_name = file_name[1:]
        categorylist = glob.glob("./template/data/category_txt/*.txt")
        print(file_name)
        for i in categorylist:
            f = open(i,"r")
            lines = f.readlines()

            # if (file_name in str(lines)) and (file_name+".jpg" not in str(lines)):
            #     category = i
            #     break
            for line in lines:
                line = line.split("\n")[0]
                if file_name == str(line):
                    category = i
                    break
            f.close()
        print(category)
        pic_list = self.get_category(category,file_name)
        self.write({"status":"ok","pic_list":pic_list})

    def get_category(self,category,file_name):
        categorylist = []
        f=open(category,"r")
        lines = f.readlines()
        lines.remove(file_name+"\n")
        for line in lines:
            line = line.split("\n")[0]
            if len(line)<4:
                line = list(line)
                times = 4-len(line)
                for i in range(times):
                    line.insert(0,"0")
                line = "".join(line)
            pic_id = "template/data/origin_pic/"+line+".jpg"
            pic_id = self.static_url(pic_id)
            categorylist.append(pic_id)
        return categorylist

class QueryHandler(tornado.web.RequestHandler):
    def post(self):
        category_now = self.get_argument("category_now")
        Group_Number = self.get_argument("Group_Number")
        # Textbox_Orientation = self.get_argument("Textbox_Orientation")
        Number_Index = self.get_argument("Number_Index")

        f = open("template/data/category_txt/"+category_now+".txt","r")
        img_list = f.readlines()
        f.close()

        if Group_Number != "":
            print("ffffff")
            for i in img_list:
                img_name = i.split("\n")[0]
                if img_name[-1] != "g":
                    for x in range(4-len(img_name)):
                        img_name = "0"+img_name
                seed_number = []
                group_txt = "template/data/group_txt/"+img_name+"_group.txt"
                group_txt = open(group_txt,"r")
                g_lines = group_txt.readlines()
                group_txt.close()
                for g_line in g_lines:
                    g_line = g_line.split(",")[2]
                    seed_number.append(g_line)
                seed_number = len(set(seed_number))-1
                print(group_txt,seed_number)
                if int(Group_Number) - seed_number != 0:
                    img_list.remove(i)   ##  has "\n"

        new_list = []
        if Number_Index == "1":
            for i in img_list:
                img_name = i.split("\n")[0]
                if img_name[-1] != "g":
                    for x in range(4-len(img_name)):
                        img_name = "0"+img_name
                    f = open("template/data/label_txt/jpg/"+img_name+".txt","r")
                    label_line = f.readlines()
                    f.close()
                    for line in label_line:
                        name = line.split(" ")[0]
                        if  name == "z_number" or name == "number":
                            new_list.append(i)
                            break
            img_list = new_list

        if Number_Index == "2":
            for i in img_list:
                img_name = i.split("\n")[0]
                if img_name[-1] != "g":
                    for x in range(4-len(img_name)):
                        img_name = "0"+img_name
                    f = open("template/data/label_txt/jpg/"+img_name+".txt","r")
                    label_line = f.readlines()
                    f.close()
                    shaobin = 0
                    for line in label_line:
                        name = line.split(" ")[0]
                        if  name == "z_number" or name == "number":
                            shaobin =1
                    if shaobin == 0:
                        new_list.append(i)
            img_list = new_list

        result = []
        for i in img_list:
            img_name = i.split("\n")[0]
            if len(img_name)<4 :
                for x in range(4-len(img_name)):
                    img_name = "0"+img_name
            img = "template/data/origin_pic/" + img_name + ".jpg"
            img = self.static_url(img)
            result.append(img)

        print(len(result))
        self.write({"status":"ok","pic_list":result})
        
        
