# 選択しているオブジェクトの中に、キーフレームが設定されたのを洗い出す
import maya.cmds as mc

slObjList = []
keyFObjList = []
slObjList = mc.ls(sl = 1, flatten = 1)

print slObjList

# 選択しているオブジェクトはキーフレームがあるかどうかを検索する
for obj in slObjList:
    keyIndex = mc.keyframe(obj, query = 1, indexValue = 1)
    print keyIndex
    # キーフレームがない場合、リストから除く
    if keyIndex != None:
        keyFObjList.append(obj)
        print obj + " has keyFrame"

mc.select(keyFObjList)
print keyFObjList