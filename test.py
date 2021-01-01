import urllib as url

SCRIPT_PATH = {
    "UVAlign":"https://raw.githubusercontent.com/Julian-Fish/FishPythonProject/master/UVAlignVer2.py"
}

def loadFromGitHub(name):
    f = url.urlopen(SCRIPT_PATH[name])
    scriptText = f.read()
    print(scriptText)
    
loadFromGitHub("UVAlign")