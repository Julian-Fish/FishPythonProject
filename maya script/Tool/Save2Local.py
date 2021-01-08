# シェルフとQTUIをディスクに保存するスクリプト
# path = userShelfDir/FishShelf/

import maya.cmds as mc

SHELF_NAME = "FishShelf"

shelfPath = mc.internalVar( userShelfDir = True ) + SHELF_NAME + "/"
print shelfPath

if not os.path.exists(shelfPath):
    os.mkdir(shelfPath)

if mc.shelfLayout(SHELF_NAME, query = 1, ex = 1):
    mc.saveShelf( SHELF_NAME, (shelfPath + SHELF_NAME) )