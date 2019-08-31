import glob
import os
f  = open("pic_list.txt","a")
for i in glob.glob("./origin_pic/*.jpg"):
    i = i.split("\\")[-1]
    i = "template/data/origin_pic/"+i+"\n"
    f.write(i)
f.close()