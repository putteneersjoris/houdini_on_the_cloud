
#curl -X PUT http://data.hasdata.xyz/ -H 'Content-Type: application/json' -d '{"id":33, "sensorID": 4, "type":4, "metric":4, "value": 1, "time":"from crontab on other linux pc"}'
#execute python script that renames the previous output file form houdini

#user params
visualize_data="data_viz.py"
rename_img_files="rename.py"
h_version="19.5"

wdir='/var/www/hasdata.xyz/generate/'

cd $wdir
python3 $rename_img_files --path './'

#init houdini environment and source houdini_setup
cd "/opt/hfs"$h_version"/"
# instead of source, use '.' -> https://stackoverflow.com/questions/13702425/source-command-not-found-in-sh-shell
. ./houdini_setup > /dev/null 2>&1

#execute python file that generates the houdini scene
cd $wdir
hython $visualize_data --path $wdir



