import maya.cmds as cmds

# +-+------------------+
# |-|  Doing Nothing   |
# +--------------------+
# | Sleeping: 40%      |
# |                    |
# | +----------------+ |
# | |||||||          | |
# | +----------------+ |
# |                    |
# | Hit ESC to Cancel  |
# +--------------------+

# Always use the progress dialog from a script, never directly
# from the Script Editor.

def myFun():
    amount = 0
    cmds.progressWindow(	title='Doing Nothing',
                        progress=amount,
                        status='Sleeping: 0%',
                        isInterruptable=True )
    while True :
        # Check if the dialog has been cancelled
        if cmds.progressWindow( query=True, isCancelled=True ) :
            break

        # Check if end condition has been reached
        if cmds.progressWindow( query=True, progress=True ) >= 100 :
            break

        amount += 5

        cmds.progressWindow( edit=True, progress=amount, status=('Sleeping: ' + `amount` + '%' ) )

        cmds.pause( seconds=1 )

    cmds.progressWindow(endProgress=1)

myFun()