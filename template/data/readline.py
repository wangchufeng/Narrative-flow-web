import glob
path = "./category_txt/*"
total = 0 
for i in glob.glob(path):
    with open(i) as file:
        lines = file.readlines()
        total += len(lines)

print(total)