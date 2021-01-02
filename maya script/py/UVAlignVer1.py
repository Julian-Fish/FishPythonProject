import maya.cmds as mc
import maya.mel as mel
import math
import sys

mc.refreshEditorTemplates()

sys.setrecursionlimit(5000)
#---------------------------関数定義------------------------------#
def dot(vec1, vec2):
    return vec1[0] * vec2[0] + vec1[1] * vec2[1]

def normalize(vec):
    _len = math.sqrt(vec[0] ** 2 + vec[1] ** 2)
    if(_len == 0.0) : 
        return False
    else:
        return [vec[0] / _len, vec[1] / _len]
    

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
        vec = normalize( [uvPos[0] - pivotPos[0], uvPos[1] - pivotPos[1]] )
        if(vec == False): continue
            
        nearAxisIndex = nearAxis(vec)
        nextPivotList[nearAxisIndex] = uv
        moveVertex = uv
        move2Pos = pivotPos

        # uv頂点の整列がやっていた場合、uv頂点の変わりにpivotを整列する
        if uv in isAlignedList:
            moveVertex = pivot
            move2Pos = uvPos

        # 垂直方向に整列-----pivotPos.u -> uv.u
        if nearAxisIndex == 0 or nearAxisIndex == 2:
            mc.polyEditUV(moveVertex, r = False, u = move2Pos[0])
        # 水平方向に整列-----pivotPos.v -> uv.v
        else:
            mc.polyEditUV(moveVertex, r = False, v = move2Pos[1])

    for _pivot in nextPivotList:
        # 整列完了に入れて、再帰する
        if _pivot not in isAlignedList and _pivot != "":
            isAlignedList.append(_pivot)
            alignUV(_pivot)
            #mc.select(_pivot)

#---------------------------------------------#
# pivotの格納
pivot = mc.ls(selection = True)
# 軸
axisList = [[0, 1], [-1, 0], [0, -1], [1, 0]]
# UVShellに含めているUVを取得する
uvList_Shell = flatten(mc.polyListComponentConversion(pivot, tuv = True, uvShell = True))
# 整列完了の頂点
isAlignedList = [pivot[0]]

alignUV(pivot)
#mc.select(uvList_Shell)
#print(uvList_Shell)
    