import maya.cmds as mc

pivot = mc.ls(selection = True)
pivot = mc.polyListComponentConversion(pivot, tuv = True)
# 最初の方向（上下左右）
verticalDir = [[0, 1], [0, -1]]
horizentalDir = [[1, 0], [-1, 0]]
# UVShellに含めているUVを取得する
uvList_Shell = flatten(mc.polyListComponentConversion(pivot, tuv = True, uvShell = True))