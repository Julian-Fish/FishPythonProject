import urllib2 as url

SCRIPT_PATH = {
    "UVAlign":"https://raw.githubusercontent.com/Julian-Fish/FishPythonProject/master/UVAlignVer2.py",
    "MultiRename":"https://raw.githubusercontent.com/Julian-Fish/FishPythonProject/master/maya%20script/py/multiRename.py"
}

QTUI_PATH = {
    "MultiRename":"https://raw.githubusercontent.com/Julian-Fish/FishPythonProject/master/maya%20script/qtui/multiRename.ui"
}

def loadFromGitHub(name):
    f = url.urlopen(SCRIPT_PATH[name])
    scriptText = f.read()
    
def downloadQTUI(name):
    uiText = url.urlopen(QTUI_PATH[name]).read()
    fileName = mc.workspace(fullName = True) + "/qtui/" + name + ".ui"
    f = open(fileName, "w")   
    f.write(uiText)
    f.close()

downloadQTUI("MultiRename")
