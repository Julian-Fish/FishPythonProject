import maya.cmds as mc

SHELVES_NAME = "FishShelves"

shelvesPath = mc.internalVar( userShelfDir = True ) + "FishShelves/"
print shelvesPath

if not os.path.exists(shelfPath):
    os.mkdir(shelvesPath)

if mc.shelfLayout(SHELVES_NAME, query = 1, ex = 1):
    mc.saveShelf( SHELVES_NAME, (shelvesPath + SHELVES_NAME) )