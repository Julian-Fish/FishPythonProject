import maya.cmds as mc

#---------------------------------------------------------#
def dot(vec1, vec2):
    return vec1[0] * vec2[0] + vec1[1] * vec2[1]

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
    pivotPos = mc.polyEditUV(pivot, query = True)
    print(pivotPos)

    edge_fuv = fuv2e(pivot)
    #mc.select(edge_fuv)
    
    uv_fe = fe2uv(edge_fuv)
    print(uv_fe)
    print(pivot)
    uv_fe.remove(pivot[0])
    
    for uv1 in uv_fe:
        uv1Pos = mc.polyEditUV(uv1, query = True)
        # uv1Pos - pivotPos
        vec1 = [uv1Pos[0] - pivotPos[0], uv1Pos[1] - pivotPos[1]]
        for uv2 in uv_fe:
            uv2Pos = mc.polyEditUV(uv2, query = True)
            # uv2Pos - pivotPos
            vec2 = [uv2Pos[0] - pivotPos[0], uv2Pos[1] - pivotPos[1]]
            if(dot(vec1, vec2) < 0 and uv1 not in isAlignedList and uv2 not in isAlignedList):
                vecs = [vec1, vec2]
                uvs = [uv1, uv2]
                for i in range(2):
                    # 水平方向-----pivotPos.u -> uv1.u
                    if(abs(vecs[i][0]) > abs(vecs[i][1])):
                        #print(uv1)
                        #print(uv2)
                        mc.polyEditUV(uvs[i], r = False, v = pivotPos[1])
                    # 垂直方向-----pivotPos.v -> uv1.v
                    else:
                        #print(uv1)
                        #print(uv2)
                        mc.polyEditUV(uvs[i], r = False, u = pivotPos[0])
                        
                isAlignedList.append(uv1)
                isAlignedList.append(uv2)
    #mc.select(uv_fe)

#---------------------------------------------#
# pivotの格納
pivot = mc.ls(selection = True)
# UVShellに含めているUVを取得する
uvList_Shell = flatten(mc.polyListComponentConversion(pivot, tuv = True, uvShell = True))
isAlignedList = [pivot]
alignUV(pivot)
#mc.select(uvList_Shell)
#print(uvList_Shell)
    