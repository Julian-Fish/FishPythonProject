import maya.cmds as mc
import sys
sys.setrecursionlimit(5000)
#---------------------------------------------------------#
def dot(vec1, vec2):
    return vec1[0] * vec2[0] + vec1[1] * vec2[1]

def nearAxis(vec):
    maxDotProduct = -10
    index_maxDot = 0

    for axis in axisList:
        dotResult = dot(vec, axis)
        if dotResult > maxDotProduct:
            maxDotProduct = dotResult
            index_maxDot = axisList.index(axis)

    return index_maxDot

def flatten(_list):
    return mc.ls(_list, flatten = True)

def fuv2e(_list):
    return mc.polyListComponentConversion(_list, fuv = True, te = True)

def fe2uv(_list):
    uvList = flatten(mc.polyListComponentConversion(_list, fe = True, tuv = True))
    uvListForQuery = uvList
    for uv in uvListForQuery:
        if(uv not in uvList_Shell):
            uvList.remove(uv)
    return uvList

def alignUV(pivot):
    pivot = mc.polyListComponentConversion(pivot, tuv = True)
    pivot = pivot[0]
    pivotPos = mc.polyEditUV(pivot, query = True)

    edge_fuv = fuv2e(pivot)
    
    uv_fe = fe2uv(edge_fuv)
    uv_fe.remove(pivot)
    
    # 上下左右
    nextPivotList = ["", "", "", ""]
    
    for uv in uv_fe:
        
        # 選択している頂点のシェールしか処理しない
        if uv not in uvList_Shell:
            continue

        # ベクトルの計算
        uvPos = mc.polyEditUV(uv, query = True)
        vec = [uvPos[0] - pivotPos[0], uvPos[1] - pivotPos[1]]
        nearAxisIndex = nearAxis(vec)
        nextPivotList[nearAxisIndex] = uv
        # 垂直方向に整列-----pivotPos.u -> uv.u
        if nearAxisIndex == 0 or nearAxisIndex == 1:
            mc.polyEditUV(uv, r = False, u = pivotPos[0])
        # 水平方向に整列-----pivotPos.v -> uv.v
        else:
            mc.polyEditUV(uv, r = False, v = pivotPos[1])

    for pivot in nextPivotList:
        # 整列完了に入れて、再帰する
        if pivot not in isAlignedList and pivot != "":
            isAlignedList.append(pivot)
            alignUV(pivot)


#---------------------------------------------#
# pivotの格納
pivot = mc.ls(selection = True)
# 軸(上下左右)
axisList = [[0, 1], [0, -1], [-1, 0], [1, 0]]
# UVShellに含めているUVを取得する
uvList_Shell = flatten(mc.polyListComponentConversion(pivot, tuv = True, uvShell = True))
# 整列完了の頂点
isAlignedList = [pivot[0]]

alignUV(pivot)
#mc.select(uvList_Shell)
#print(uvList_Shell)
    