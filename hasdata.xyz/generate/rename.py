import os
import time
import argparse
from natsort import natsorted
import time
# -------


parser = argparse.ArgumentParser(description='rename files')
parser.add_argument('-p', '--path', type=str, metavar='', required=True, help='path of py')
args = parser.parse_args()

os.chdir('/var/www/hasdata.xyz/images')
pwd = os.getcwd()

def create_array(path):
    array = []
    for file in os.listdir(path):
        if file.endswith((".png", ".jpg", "jpeg")):
            array.append(file)
    return natsorted(array)

# every image of format output_n becomes output_n-n+1 as a way of temperary storing the images under a different name.
# if we dont do this and directly name the image output_n+1, we will overwrite the next one in the sequence.
# there are other alternatives e.g. copying the image under a different folder, and renaming it in the meantime. I found this method the quickest.
                                                
for item in create_array(pwd):                                 #image_0.jpg
    name = item.split('.')[0]                               #image_0
    newindex = int(item.split('.')[0].split('_')[1]) + 1    #1
    os.rename(item,f'{name}-{newindex}.jpg')                #image_0-1

time.sleep(0.1)                                             #by adding a slight delay, we prevent it from breaking

for item in create_array(pwd): 
    name = item.split('.')[0].split('_')[0]                 #image 
    newindex = item.split('.')[0].split('-')[1]             #1
    os.rename(item , f'{name}_{newindex}.jpg')              #image_1.jpg

