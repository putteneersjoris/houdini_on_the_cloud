import hou
import random

wdir = '/root/Documents/houdini_on_the_cloud/'

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
sphere = geo.createNode('sphere')
sphere.setParms({
                'type':2,
                'rows': random.randint(1,10), 
                'cols': random.randint(3,25), 
                })

null = geo.createNode('null')
null.setInput(0, sphere)


print('null copmlete')
# create nodes in ropnet
ropnet = geo.createNode('ropnet')
opengl = ropnet.createNode('opengl')
opengl.setParms({
                'camera': camera.path(),
                'picture': f'{wdir}/output.jpg',
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
# hou.hipFile.save(f'{wdir}render_sphere.hipnc')
# print('file saved')
