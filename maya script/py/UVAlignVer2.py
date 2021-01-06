import maya.cmds as mc
import maya.mel as mel
import math
import sys
import time
sys.setrecursionlimit(5000)
#---------------------------OPTION------------------------------#
''' ドット演算の閾値 '''
OPTION_MINDOT = 0.707   
#---------------------------OPTION------------------------------#

#---------------------------関数定義------------------------------#
def signal_handler(signum, frame):
    raise Exception("Time Out")

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

def findUVinLine(_pivot, _lineDirV2):
    _pivot = mc.polyListComponentConversion(_pivot, tuv = True)
    _pivot = _pivot[0]
    pivotPos = mc.polyEditUV(_pivot, query = True)

    edge_fuv = fuv2e(_pivot)
    
    uv_fe = fe2uv(edge_fuv)
    uv_fe.remove(_pivot)

    maxDotProduct = -10.0
    index_maxDot = 0
    nextVec = 0
    for uv in uv_fe:
        # 選択している頂点のシェールしか処理しない
        if uv not in uvList_Shell:
            continue

        # ベクトルの計算
        uvPos = mc.polyEditUV(uv, query = True)
        vec = normalize( [uvPos[0] - pivotPos[0], uvPos[1] - pivotPos[1]] )
        if(vec == False): continue

        # ラインに最も近いUVを探す
        dotResult = dot(vec, _lineDirV2)
        if dotResult > maxDotProduct:
            maxDotProduct = dotResult
            uv_maxDot = uv
            dir_maxDot = vec

    # 結果が閾値以上しか受け取らない
    if(maxDotProduct > OPTION_MINDOT):
        return uv_maxDot, dir_maxDot
    else:
        return -1, -1

# 整列を行う（mode = 0 垂直に；mode = 1 水平に）
def doAlign(_pivot, mode = 0):
    verticalUVList = [_pivot]
    horizentalUVList = [_pivot]
    _pivotPos = mc.polyEditUV(_pivot, query = True)

    if mode == 0:
        # 垂直方向のUVを取得する
        for dirV2 in verticalDir:
            nextUV, nextDirV2 = findUVinLine(_pivot, dirV2)
            while nextUV != -1 and nextDirV2 != -1:
                # 方向がループしている場合、中止
                if nextUV in verticalUVList:
                    return False

                verticalUVList.append(nextUV)
                nextUV, nextDirV2 = findUVinLine(nextUV, nextDirV2)
        
        for uv in verticalUVList:
            # 垂直に整列する
            mc.polyEditUV(uv, r = False, u = _pivotPos[0])

    elif mode == 1:
        # 水平方向のUVを取得する
        for dirV2 in horizentalDir:
            nextUV, nextDirV2 = findUVinLine(_pivot, dirV2)
            while nextUV != -1 and nextDirV2 != -1:
                # 方向がループしている場合、中止
                if nextUV in horizentalUVList:
                    return False

                horizentalUVList.append(nextUV)
                nextUV, nextDirV2 = findUVinLine(nextUV, nextDirV2)

        for uv in horizentalUVList:
            # 水平に整列する
            mc.polyEditUV(uv, r = False, v = _pivotPos[1])

    else:
        return False

    return verticalUVList, horizentalUVList


def alignUV(_pivot):
    PROGRESS_AMOUNT = 0
    verticalUVList = []
    horizentalUVList = []
    verticalUVList, a   = doAlign(_pivot, 0)
    a, horizentalUVList = doAlign(_pivot, 1)

    if verticalUVList == False or horizentalUVList == False:
        return False

    # 進捗状況を表示する
    UVAmount = len(verticalUVList) + len(horizentalUVList) - 2
    mc.progressWindow(title = "UVAlign", progress = 0, max = UVAmount, status = "Aligning ", isInterruptable = True)

    # 各垂直のUVをpivotに対して、水平に整列する
    verticalUVList.remove(_pivot)
    for uv in verticalUVList:
        if mc.progressWindow(query = True, isCancelled = True):
            return False
        
        PROGRESS_AMOUNT += 1
        #progress = PROGRESS_AMOUNT / UVAmount
        mc.progressWindow(title = "UVAlign", edit = True, progress = PROGRESS_AMOUNT)
        doAlign(uv, 1)
    # 各水平のUVをpivotとして、垂直に整列する
    horizentalUVList.remove(_pivot)
    for uv in horizentalUVList:
        if mc.progressWindow(query = True, isCancelled = True):
            return False
        
        PROGRESS_AMOUNT += 1
        #progress = PROGRESS_AMOUNT / UVAmount
        mc.progressWindow(title = "UVAlign", edit = True, progress = PROGRESS_AMOUNT)
        doAlign(uv, 0)
    
    return True


#---------------------------------------------#
# pivotの格納
pivot = mc.ls(selection = True)
# 最初の方向（上下左右）
verticalDir = [[0, 1], [0, -1]]
horizentalDir = [[1, 0], [-1, 0]]
# UVShellに含めているUVを取得する
uvList_Shell = flatten(mc.polyListComponentConversion(pivot, tuv = True, uvShell = True))

isDone = alignUV(pivot[0])
mc.progressWindow(title = "UVAlign", endProgress = True)
print isDone
#mc.select(uvList_Shell)
#print(uvList_Shell)
    