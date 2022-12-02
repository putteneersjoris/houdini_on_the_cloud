import os

i = 0
for file in os.listdir('./'):
    if file.endswith((".png", ".jpg", "jpeg")):
        i +=1
        name_ = file.split('.')[0].split('_')[0]
        num = str(int(file.split('.')[0].split('_')[1]) +1)
        ext = file.split('.')[1]
        newname = name_ + '_'+ num + '.'+ ext
        os.rename(file, newname)



# write the js file
with open("./images_hierarchy.js", "w", encoding="utf8") as f:
        f.write(f'max images of out is {i} with name :  {name_}')
f.close()