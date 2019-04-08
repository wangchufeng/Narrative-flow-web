import csv
import numpy as np
from PIL import Image
import heapq
import shutil

file_name = "4"
file =open('pca.csv','r')
lines=file.readlines()
file.close()
row=[]#定义行数组
column=[]#定义列数组
for line in lines:
    row.append(line.split(','))
dist_list = []
img_list = []

file_index = np.where(np.array(row)=="1367.jpg")
print(file_index[0][0])
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

max_num_index_list = map(dist_list.index, heapq.nsmallest(25, dist_list))

for i in max_num_index_list:
    # Image.open(img_list[i]).show()
    filename = img_list[i].split("/")[-1]
    file_path = r"D:/Git_repository/Narrative-flow-web/demo/template/data/same_flow/"
    file_path = file_path + filename
    print(file_path)

    jpg_file = "./origin_pic/" + filename.split("_flow")[0]+".jpg"
    jpg_path = "./same_flow/"+ filename.split("_flow")[0]+".jpg"
    # shutil.copyfile(img_list[i],file_path)
    # shutil.copyfile(jpg_file,jpg_path)

# for col in row:
#     column.append(col[0])
# print(column)#打印第一列数组
