import maya.cmds as mc
import urllib

SCRIPT_PATH = "https://raw.githubusercontent.com/Julian-Fish/FishPythonProject/master/UV.py"

f = url.urlopen(SCRIPT_PATH)

scriptText = f.read()

#print scriptText

exec(scriptText)