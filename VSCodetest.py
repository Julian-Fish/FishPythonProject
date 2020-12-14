import maya.cmds as cmds

rename_Window = cmds.window(title = "Rename", w=300, h=100)
cmds.columnLayout(adj=True)
rename_TextGroup = cmds.textFieldGrp(label="Rename", ed=True, text="Input New Name")
rename_ConfirmButtom = cmds.button(label="Rename Confirm", command="RenameConfirm()")

cmds.showWindow(rename_Window)

def RenameConfirm():
    newName_String = cmds.textFieldGrp(rename_TextGroup, q=True, text=True)
    cmds.rename(newName_String)
