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
                'tz':3,
                'resx':200,
                'resy':200,
                })

print('geo')
# create nodes on geometry context
python_sop = geo.createNode('python')
python_sop_script = '''

node = hou.pwd()
geo = node.geometry()
#import requests
import random
#sensorID = 0
#query = f'http://data.hasdata.xyz/?show=*&sensorID=*&data=*&limit=1'
#r = requests.get(query)
#jsonObj = r.json()

pt = geo.createPoint()
geo.addAttrib(hou.attribType.Point, "value", "")
#for obj in jsonObj:
#	value = obj["value"]
test = random.randint(0,100)
pt.setAttribValue("value", f'{test}')
'''
temperature = random.randint(10,25)
humidity = random.randint(245,567)
proximity = random.uniform(0.0, 1.0)

with open("/var/www/hasdata.xyz/js/dynamic_sensor_data.json", "w", encoding="utf8") as f:

    f.write("{\n")
    f.write("   \"sensor_data\":{ \n")
    f.write(f"      \"temperature\": {temperature},\n")
    f.write(f"      \"humidity\": {humidity},\n")
    f.write(f"      \"proximity\": {proximity}\n")
    f.write("   }\n")
    f.write("}\n")
    
    f.close()




python_sop.parm('python').set(python_sop_script)

font = geo.createNode('font')
font_expression = '''`points("../python1", 0, "value")`'''

font.setParms({
	'text': font_expression,
	'fontsize': 0.5
})

null = geo.createNode('null')
null.setInput(0, font)


print('null copmlete')
# create nodes in ropnet
ropnet = geo.createNode('ropnet')
opengl = ropnet.createNode('opengl')
opengl.setParms({
                'camera': camera.path(),
                'picture': f'/var/www/hasdata.xyz/images/output_0.jpg',
                'gamma': 2.2,
                'shadingmode': 2,
                })


# set desplayflag
null.setDisplayFlag(True)
null.setRenderFlag(True)


# layout nodes
obj.layoutChildren()
geo.layoutChildren()

print('geo complete')
# render the file
opengl.parm('execute').pressButton()
print('render complete')

# save hipfile (optional)
hou.hipFile.save(f'{wdir}data_viz.hipnc')
print('file saved')
