import os
import time
import argparse
from natsort import natsorted
from datetime import date, datetime, timezone
import datetime

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
                                                
for item in create_array('./'):                                 #image_0.jpg
    name = item.split('.')[0]                               #image_0
    newindex = int(item.split('.')[0].split('_')[1]) + 1    #1
    os.rename(item,f'{name}-{newindex}.jpg')                #image_0-1

time.sleep(0.1)                                             #by adding a slight delay, we prevent it from breaking
                                              
for item in create_array('./'): 
    name = item.split('.')[0].split('_')[0]                 #image 
    newindex = item.split('.')[0].split('-')[1]             #1
    os.rename(item , f'{name}_{newindex}.jpg')              #image_1.jpg


current_time = datetime.datetime.now(timezone.utc)
current_utc_time = current_time.replace(tzinfo=timezone.utc)
current_utc_timestamp = round(current_utc_time.timestamp())                                      #populate teh json file with i and name etc

number = len(create_array("/var/www/hasdata.xyz/images/")) + 1 #get number of images
# write a json file so we can reference it in the app.js file to dynamically update te menu

with open("/var/www/hasdata.xyz/js/dynamic_time_data.json", "w", encoding="utf8") as f:

    f.write("{\n")
    f.write("   \"time_data\":{ \n")
    f.write(f"      \"n_images\": {number},\n")
    f.write(f"      \"last_updated\": {current_utc_timestamp}\n")
    f.write("   }\n")
    f.write("}\n")
    
    f.close()


