#curl -X PUT http://data.hasdata.xyz/ -H 'Content-Type: application/json' -d '{"id":33, "sensorID": 4, "type":4, "metric":4, "value": 1, "time":"from crontab on other linux pc"}'


#user params
script="data_viz.py"
h_version="19.5"
wdir='/root/Documents/houdini_on_the_cloud/'

#init houdini environment and source houdini_setup
cd "/opt/hfs"$h_version"/"
# instead of source, use '.' -> https://stackoverflow.com/questions/13702425/source-command-not-found-in-sh-shell
. ./houdini_setup > /dev/null 2>&1
echo `pwd`
#execute python file that generates the houdini scene
hython $wdir'/'$script

