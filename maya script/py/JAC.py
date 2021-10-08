'''
import maya.cmds as mc
from openpyxl import Workbook, load_workbook
#load excel
workRootDir = mc.workspace(q = 1, rootDirectory = 1)
wb = load_workbook(workRootDir + "test.xlsx")
ws = wb["kadai01"]
uuid = mc.ls("JAC", uuid=1)
#find number by uuid
for row in ws.values:
    if row[2] == uuid[0]:
        mc.rename("JAC", row[0])
'''
import PySide2
import maya.cmds as mc
from openpyxl import Workbook, load_workbook
import shutil
import maya.mel as mel
#load excel
workRootDir = mc.workspace(q = 1, rootDirectory = 1)
wb = load_workbook(workRootDir + "test.xlsx")
ws = wb.active

#create tableWidget
tableWidget = QTableWidget()
headerLabels = [u"学籍番号", u"名前", u"UUID"]
tableWidget.setColumnCount(len(headerLabels))
tableWidget.setRowCount(len(tuple(ws.rows)))
tableWidget.setHorizontalHeaderLabels(headerLabels)

tableWidget.verticalHeader().setVisible(False)

for row, rowData in enumerate(ws.values):
    if rowData[0] is None:
        break
    for col, v in enumerate(rowData):
        item = QTableWidgetItem(v)
        tableWidget.setItem(row, col, item)
        

tableWidget.show()
#find item
tableWidget.setItemSelected(item, 1)
# =============================================================================
# #newSheet = "kadai01"
# #ws = wb.create_sheet(newSheet)
# uuidCol = ws["C"]
# i = 0
# for row in ws.iter_rows(min_row = 1):
#     if row[0].value is None:
#         #file end
#         #print "End"
#         break
#     num = row[0].value
#     name = row[1].value
#     fileName = num + " " + name
#     #create jac empty group
#     jac = mc.group(em=True, name="JAC")
#     uuid = mc.ls("JAC", uuid=1)
#     uuidCol[i].value = uuid[0].encode("ascii", "ignore")
#     i += 1
#     #hiden jac empty group
#     mc.setAttr("JAC.hiddenInOutliner", True)
#     mc.outlinerEditor("outlinerPanel1", edit = True, refresh = True)
#     #lock jac, save and copy map file
#     mc.lockNode("JAC", lock = 1)
#     mel.eval("file -save")
#     originMapName = "map1.mb"
#     originMapDir = workRootDir + "scenes/" + originMapName
#     targetMapDir = workRootDir + "scenes/" + fileName + ".mb"
#     shutil.copy(originMapDir, targetMapDir)
#     #unlock and delete jac
#     mc.lockNode("JAC", lock = 0)
#     mc.delete(jac)
# #save excel
# wb.save(workRootDir + "test.xlsx")
# =============================================================================
