import maya.cmds as mc
import urllib as url

PathListURL = "https://raw.githubusercontent.com/Julian-Fish/FishPythonProject/master/maya%20script/py/PathList.py"

def _null(*args):
    pass


class _shelf():
    '''A simple class to build shelves in maya. Since the build method is empty,
    it should be extended by the derived class to build the necessary shelf elements.
    By default it creates an empty shelf called "customShelf".'''

    def __init__(self, name="FishShelves", iconPath=""):
        self.name = name

        self.iconPath = iconPath

        self.labelBackground = (0, 0, 0, 0)
        self.labelColour = (.9, .9, .9)

        #self._cleanOldShelf()
        self.build()
        mc.setParent(self.name)

    def build(self):
        '''This method should be overwritten in derived classes to actually build the shelf
        elements. Otherwise, nothing is added to the shelf.'''
        pass

    def addButon(self, label, icon="commandButton.png", command=_null, doubleCommand=_null):
        '''Adds a shelf button with the specified label, command, double click command and image.'''
        mc.setParent(self.name)
        if icon:
            icon = self.iconPath + icon
        mc.shelfButton(width=37, height=37, image=icon, l=label, command=command, dcc=doubleCommand, imageOverlayLabel=label, olb=self.labelBackground, olc=self.labelColour)

    def addMenuItem(self, parent, label, command=_null, icon=""):
        '''Adds a shelf button with the specified label, command, double click command and image.'''
        if icon:
            icon = self.iconPath + icon
        return mc.menuItem(p=parent, l=label, c=command, i="")

    def addSubMenu(self, parent, label, icon=None):
        '''Adds a sub menu item with the specified label and icon to the specified parent popup menu.'''
        if icon:
            icon = self.iconPath + icon
        return mc.menuItem(p=parent, l=label, i=icon, subMenu=1)

    def _cleanOldShelf(self):
        '''Checks if the shelf exists and empties it if it does or creates it if it does not.'''
        if mc.shelfLayout(self.name, ex=1):
            if mc.shelfLayout(self.name, q=1, ca=1):
                for each in mc.shelfLayout(self.name, q=1, ca=1):
                    mc.deleteUI(each)
        else:
            mc.shelfLayout(self.name, p="ShelfLayout")


###################################################################################
'''This is an example shelf.'''
# class customShelf(_shelf):
#     def build(self):
#         self.addButon(label="button1")
#         self.addButon("button2")
#         self.addButon("popup")
#         p = mc.popupMenu(b=1)
#         self.addMenuItem(p, "popupMenuItem1")
#         self.addMenuItem(p, "popupMenuItem2")
#         sub = self.addSubMenu(p, "subMenuLevel1")
#         self.addMenuItem(sub, "subMenuLevel1Item1")
#         sub2 = self.addSubMenu(sub, "subMenuLevel2")
#         self.addMenuItem(sub2, "subMenuLevel2Item1")
#         self.addMenuItem(sub2, "subMenuLevel2Item2")
#         self.addMenuItem(sub, "subMenuLevel1Item2")
#         self.addMenuItem(p, "popupMenuItem3")
#         self.addButon("button3")
# customShelf()
###################################################################################

class FishShelves(_shelf):
    def downloadScriptsFromGitHub(self, name):
        raw = url.urlopen(SCRIPT_PATH[name]).read()
        text_decode = raw.decode("utf-8")
        return text_decode

    def downloadQTUIFromGitHub(self, name):
        uiText = url.urlopen(QTUI_PATH[name]).read()
        fileName = mc.workspace(fullName = True) + "/qtui/" + name + ".ui"
        f = open(fileName, "w")   
        f.write(uiText)
        f.close()

    def build(self):
        # パスリストの読み込み
        pathListCmd = url.urlopen(PathListURL).read()
        if pathListCmd == "":
            mc.error("Download Error")
            return "Download Error"

        exec(pathListCmd)
        self._cleanOldShelf()

        progressAmount = len(SCRIPT_PATH) + len(QTUI_PATH)
        prog = 0

        mc.progressWindow(title = "Construct", progress = 0, max = progressAmount, status = "Loading")

        # スクリプトのダウンロード
        for name in SCRIPT_NAME:
            prog += 1
            mc.progressWindow(edit = True, progress = prog, status = "Loading Script: " + name)
            self.addButon(name, command = self.downloadScriptsFromGitHub(name))

        # QTUIのダウンロード
        for name in QTUI_PATH:
            prog += 1
            mc.progressWindow(edit = True, progress = prog, status = "Loading QTUI: " + name)

            self.downloadQTUIFromGitHub(name)

        mc.progressWindow( endProgress = True)
        return "Construct Success"

print FishShelves()