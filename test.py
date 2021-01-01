import maya.cmds as mc
import maya.mel as mel
import math
import sys
sys.setrecursionlimit(5000)
#---------------------------OPTION------------------------------#
OPTION_MINDOT = 0.707
#---------------------------OPTION------------------------------#

#---------------------------闁㈡暟瀹氱京------------------------------#
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
        # 閬告姙銇椼仸銇勩倠闋傜偣銇偡銈с兗銉仐銇嬪嚘鐞嗐仐銇亜
        if uv not in uvList_Shell:
            continue

        # 銉欍偗銉堛儷銇▓绠?        uvPos = mc.polyEditUV(uv, query = True)
        vec = normalize( [uvPos[0] - pivotPos[0], uvPos[1] - pivotPos[1]] )
        if(vec == False): continue

        # 銉┿偆銉炽伀鏈€銈傝繎銇刄V銈掓帰銇?        dotResult = dot(vec, _lineDirV2)
        if dotResult > maxDotProduct:
            maxDotProduct = dotResult
            uv_maxDot = uv
            dir_maxDot = vec

    # 绲愭灉銇岄柧鍊や互涓娿仐銇嬪彈銇戝彇銈夈仾銇?    if(maxDotProduct > OPTION_MINDOT):
        return uv_maxDot, dir_maxDot
    else:
        return -1, -1

# 鏁村垪銈掕銇嗭紙mode = 0 鍨傜洿銇紱mode = 1 姘村钩銇級
def doAlign(_pivot, mode = 0):
    verticalUVList = [_pivot]
    horizentalUVList = [_pivot]
    _pivotPos = mc.polyEditUV(_pivot, query = True)

    if mode == 0:
        # 鍨傜洿鏂瑰悜銇甎V銈掑彇寰椼仚銈?        for dirV2 in verticalDir:
            nextUV, nextDirV2 = findUVinLine(_pivot, dirV2)
            while nextUV != -1 and nextDirV2 != -1:
                verticalUVList.append(nextUV)
                nextUV, nextDirV2 = findUVinLine(nextUV, nextDirV2)
        
        for uv in verticalUVList:
        # 鍨傜洿銇暣鍒椼仚銈?            mc.polyEditUV(uv, r = False, u = _pivotPos[0])

    elif mode == 1:
        # 姘村钩鏂瑰悜銇甎V銈掑彇寰椼仚銈?        for dirV2 in horizentalDir:
            nextUV, nextDirV2 = findUVinLine(_pivot, dirV2)
            while nextUV != -1 and nextDirV2 != -1:
                horizentalUVList.append(nextUV)
                nextUV, nextDirV2 = findUVinLine(nextUV, nextDirV2)

        for uv in horizentalUVList:
        # 姘村钩銇暣鍒椼仚銈?            mc.polyEditUV(uv, r = False, v = _pivotPos[1])

    else:
        return False

    return verticalUVList, horizentalUVList


def alignUV(_pivot):
    verticalUVList = []
    horizentalUVList = []
    verticalUVList, a   = doAlign(_pivot, 0)
    a, horizentalUVList = doAlign(_pivot, 1)

    # 鍚勫瀭鐩淬伄UV銈抪ivot銇銇椼仸銆佹按骞炽伀鏁村垪銇欍倠
    verticalUVList.remove(_pivot)
    for uv in verticalUVList:
        doAlign(uv, 1)
    # 鍚勬按骞炽伄UV銈抪ivot銇ㄣ仐銇︺€佸瀭鐩淬伀鏁村垪銇欍倠
    horizentalUVList.remove(_pivot)
    for uv in horizentalUVList:
        doAlign(uv, 0)


#---------------------------------------------#
# pivot銇牸绱?pivot = mc.ls(selection = True)
# 鏈€鍒濄伄鏂瑰悜锛堜笂涓嬪乏鍙筹級
verticalDir = [[0, 1], [0, -1]]
horizentalDir = [[1, 0], [-1, 0]]
# UVShell銇惈銈併仸銇勩倠UV銈掑彇寰椼仚銈?uvList_Shell = flatten(mc.polyListComponentConversion(pivot, tuv = True, uvShell = True))
# 鏁村垪瀹屼簡銇爞鐐?isAlignedList = [pivot[0]]

alignUV(pivot[0])
#mc.select(uvList_Shell)
#print(uvList_Shell)
    