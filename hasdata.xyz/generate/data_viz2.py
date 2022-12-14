import hou
import random
import argparse
import os


parser = argparse.ArgumentParser(description='rename files')
parser.add_argument('-p', '--path', type=str, metavar='', required=True, help='path of py')
args = parser.parse_args()


wdir = args.path

hou.hipFile.load(f'{wdir}starter.hipnc')
print('succesfully loaded starter.hipnc')

obj = hou.node('/obj')

# create nodes on object context

geo = obj.createNode('geo')
camera = obj.createNode('cam')
camera.setParms({
                'tx':9.2,
                'ty':8,
                'tz':8.8,
                'rx':-30,
                'ry':45,
                'resx':500,
                'resy':500,
                'projection':1,
                'orthowidth':6.8
                })

print('camera wa succesfully build')
# create nodes on geometry context
python_sop = geo.createNode('python')
python_sop_script = '''

import requests
import json
import hou

node = hou.pwd()
geo = node.geometry()


sensor_data_array = []
sensor_mac_adresses = [ "EC:62:60:9E:32:38","EC:62:60:9C:E1:10","EC:62:60:9E:36:64","EC:62:60:83:3A:70","EC:62:60:9C:D6:48", "EC:62:60:9C:23:3C", "EC:62:60:9D:3D:E4","EC:62:60:9C:13:58", "EC:62:60:9E:3E:10","EC:62:60:9E:3A:C0" ]
sensordata =  [
                    ["luminosity",  [1,0]],
                    ["temperature", [2,0]], 
                    ["humidity",    [2,1]], 
                    ["proximity",   [3,0]], 
                    ["CO",          [4,0]], 
                    ["C2H5OH",      [4,1]], 
                    ["NO2",         [4,2]], 
                    ["VOCsss",      [4,3]], 
                    ["VOC",         [4,5]], 
]
attribute_array = []

def empty_sensor_array():
    for i in range(len(sensordata)):
        sensor_data_array.append([])

empty_sensor_array()
    
    
for i, sensor in enumerate(sensordata):
    attribute_array.append(sensordata[i][0])
    geo.addArrayAttrib(hou.attribType.Point, sensordata[i][0], hou.attribData.Float, 1)           # make attributes for all sensordata elements
  
    
file = "$HIP/json/sensorposition.json" #get json from external file
with open(file,'r') as position_f:
    position_jsonObj = json.load(position_f)
           
    for j, mac in enumerate(sensor_mac_adresses):
        pt = geo.createPoint()
        
        for obj in position_jsonObj:
            if int(obj) == j:       #set j equal to the json index so we can match the correct position to the right sensor
                x = position_jsonObj[obj]['x']
                y = position_jsonObj[obj]['y']
                z = position_jsonObj[obj]['z']
            
                pt.setPosition(hou.Vector3(x,y,z))
        
       
        r = requests.get(f'https://api.creativemakers.xyz/sensor-data.php?mac={mac}')
        jsonObj = r.json()
    
        for obj in jsonObj:
            for i, sensor in enumerate(sensordata):
    
            
                if [ int(obj['type']),int(obj['metric']) ] == sensordata[i][1]:
    
                    sensor_data_array[i].append(float(obj['value']))
    
         
        for i, item in enumerate(attribute_array):
    
            pt.setAttribValue(attribute_array[i],sensor_data_array[i]) 
        empty_sensor_array()
        
              
position_f.close()        
'''

python_sop.parm('python').set(python_sop_script)

print("python sop was succesfully build")

process_data = geo.createNode("attribwrangle")
process_data_vex = ''' 
float limited_data[] = f[]@temperature[-50:-1];

f@data_i = limited_data[0];
float data_max = pop(sort(limited_data));
float data_min = pop(reverse(sort(limited_data)));

adddetailattrib(0,"n_data_min", 1e10); //bug check https://www.sidefx.com/forum/topic/66653/
setdetailattrib(0,"n_data_min", data_min, "min");
setdetailattrib(0,"n_data_max", data_max, "max");


'''
process_data.setInput(0, python_sop)
process_data.parm('snippet').set(process_data_vex)

print('data succesfully processed and promoted to detail')


calculate_data = geo.createNode('attribwrangle')
calculate_data.setInput(0, process_data)
calculate_data_vex = '''
float n_data_min = detail(0, "n_data_min");
float n_data_max = detail(0, "n_data_max");


f@data_mult = float(@data_i - n_data_min) / float(n_data_max-n_data_min);

 '''
calculate_data.setInput(0, process_data)
calculate_data.parm('snippet').set(calculate_data_vex)

print('the data was normalized and ready to be interpolated')



bound = geo.createNode('bound')
bound.setInput(0, calculate_data)
print('bound was created')

points_from_volume = geo.createNode('pointsfromvolume')
points_from_volume.setInput(0, bound)
print('points from volume was succesfully created')

attribtransfer = geo.createNode('attribtransfer')
attribtransfer.setParms({
                'pointattriblist': "data_mult",
                'kernelradius': 2.6,
                'maxsamplecount': 5,

                
                })
attribtransfer.setInput(0, points_from_volume)
attribtransfer.setInput(1, calculate_data)
print('attribtransfer was succesfully created')

set_colormap = geo.createNode('attribwrangle')
set_colormap_vex = '''



//----------------------------------- color function
function dict color( string colorspace){

        dict viridis = set("color1", {0.057951,0, 0.0886574}, "color2", {0.0886574,0.0825261,0.25791}, "color3", {0.0011667,0.277341,0.264559}, "color4", {0.106996,0.58031,0.124487}, "color5", {0.984709,0.799651,0.00141203});
        dict magma = set("color1", {6.873e-05,6.58561e-05,0.000110699}, "color2", {0.0784851,0.000460286,0.198807}, "color3", {0.462306,0.00288181,0.193542}, "color4", {0.967762,0.241026,0.118867}, "color5", {0.9708,0.980633,0.521749});
        dict plasma = set("color1", {0.000307313,0.000182439,0.240854}, "color2", {0.20405,9.68185e-05,0.391191}, "color3", {0.594629,0.0618097,0.189997}, "color4", {0.937121,0.296127,0.0528725}, "color5", {0.868931,0.944416,0.00120667});
        dict infra_red = set("color1", {0.2,0,1}, "color2", {0,0.85,1}, "color3", {0,1,0.1}, "color4", {0.95,1,0}, "color5", {1,0,0});
        
        if(colorspace == "viridis"){
            return viridis;
        }
        if(colorspace == "magma"){
            return magma;
        }
         if(colorspace == "plasma"){
            return plasma;
        }
         if(colorspace == "infra_red"){
            return infra_red;
        }
        else{return viridis;}
}

//----------------------------------- code

int quantize_value = 40;
float data = rint(f@data_mult*quantize_value)/ quantize_value;

float position1 = 0.25;
float position2 = 0.5;
float position3 = 0.75;

float colorgrad1 = fit(clamp(data, 0,position1),0,position1,0,1);
float colorgrad2 = fit(clamp(data, position1,position2),position1,position2,0,1);
float colorgrad3 = fit(clamp(data, position2,position3),position2,position3,0,1);
float colorgrad4 = fit(clamp(data, position3,1),position3,1,0,1);

dict colorspace = color("viridis");

vector lerp1 = lerp(colorspace["color1"]    , colorspace["color2"], colorgrad1);
vector lerp2 = lerp(lerp1                   , colorspace["color3"], colorgrad2);
vector lerp3 = lerp(lerp2                   , colorspace["color4"], colorgrad3);
vector lerp4 = lerp(lerp3                   , colorspace["color5"], colorgrad4);

v@Cd = lerp4;

f@pscale = 0.05;


'''
set_colormap.setInput(0, attribtransfer)
set_colormap.parm('snippet').set(set_colormap_vex)

print('color are set in vex')

obj_export = geo.createNode('file')
obj_export.setInput(0, set_colormap)
obj_export.setParms({
                'filemode': 2,
                'file': '$HIP/model.obj'
                })


# set desplayflag
obj_export.setDisplayFlag(True)
obj_export.setRenderFlag(True)

print('succesfully exported object')

# create nodes in ropnet
ropnet = geo.createNode('ropnet')
opengl = ropnet.createNode('opengl')
opengl.setParms({
                'camera': camera.path(),
                'aamode': 6,
                'picture': '/var/www/hasdata.xyz/images/output_0.jpg',
                'wirewidth': 0.1,
                'pointsize': 10,
                'gamma': 2.2,
                'shadingmode': 1,
                })


print('ropnet and opengl where succesfully created')


# layout nodes
obj.layoutChildren()
geo.layoutChildren()

print('objects are layed out')
# render the file
opengl.parm('execute').pressButton()
print('render complete')

# save hipfile (optional)
hou.hipFile.save(f'{wdir}data_viz.hipnc')
print('file saved')
