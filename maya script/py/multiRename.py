# -*- coding: utf-8 -*-
from PySide2 import QtWidgets
from PySide2.QtUiTools import QUiLoader
from maya.app.general.mayaMixin import MayaQWidgetBaseMixin
import maya.cmds as mc

# 間接パスの指定
UIFILEPATH = shelfPath = mc.internalVar( userShelfDir = True )  + '\FishShelf/qtui/MultiRename.ui'
# パターンの定義
patternAlpha = "abcdefghijklmnpbqrstuvwxyz"
patternListEng = ["First", "Second", "Third", "Fourth", "Fifth", "sixth", "seventh", "ninth", "tenth"]
patternRoman = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X"]
patternList = [patternAlpha, patternListEng, patternRoman]

## MainWindowを作るクラス
class MainWindow(MayaQWidgetBaseMixin, QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        # UIのパスを指定
        self.UI = QUiLoader().load(UIFILEPATH)
        # ウィンドウタイトルをUIから取得
        self.setWindowTitle(self.UI.windowTitle())
        # ウィジェットをセンターに配置
        self.setCentralWidget(self.UI)

        # ボタンを接続
        self.UI.renamePushButton.clicked.connect(self.refreshPushButton)

    def refreshPushButton(self):
        # prefixパターンの取得
        prefixIndex = self.UI.prefixComboBox.currentIndex()
        # suffixパターンの取得
        suffixIndex = self.UI.suffixComboBox.currentIndex()
        self.RenameConfirm(prefixIndex, suffixIndex)

    def RenameConfirm(self, prefixIndex, suffixIndex):
        selections = mc.ls(selection = True)
        # old
        #inputText = mc.textFieldGrp(textGroup, q=True, text=True)
        i = 0
        for each in selections:
            newNameText = self.UI.newName.toPlainText()
            # パタンを取得する
            if prefixIndex > 0:
                prefixText = patternList[prefixIndex - 1][i]
                newNameText = prefixText + "_" + newNameText
            if suffixIndex > 0:
                suffixText = patternList[suffixIndex - 1][i]
                newNameText = newNameText + "_" + suffixText
            i += 1
            cmds.rename(newNameText)

## MainWindowの起動
def main():
    window = MainWindow()
    window.show()

if __name__ == '__main__':
    main()