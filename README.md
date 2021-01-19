# FishPythonProject
Maya Python Script Learning

## インストール方法：

A、Bから一つ選んでください

### A)ネットでダウンロードする：

![Construct](https://raw.githubusercontent.com/Julian-Fish/FishPythonProject/master/maya%20script/py/Construct.py)
のコードをMayaのScript EditorにPythonとして実行する

![InstallGif](https://raw.githubusercontent.com/Julian-Fish/FishPythonProject/master/gif/Construct/install.gif)

※ インターネット環境が必須

### B)ローカルから読み込む：

①![Zipファイル](https://github.com/Julian-Fish/FishPythonProject/raw/master/maya%20script/zip/FishShelf.zip)
をダウンロードして、Mayaのユーザ シェルフ ディレクトリに解凍する


②スクリプト「maya.mel.eval('loadNewShelf "FishShelf/FishShelf.mel"')」を実行して完成

※ ユーザ シェルフ ディレクトリがわからない場合、スクリプト「print cmds.internalVar(ush=True)」を実行したら出力する

![install_local](https://raw.githubusercontent.com/Julian-Fish/FishPythonProject/master/gif/install/install_local.png)

## スクリプトの機能：

### ![MultiRename](https://raw.githubusercontent.com/Julian-Fish/FishPythonProject/master/maya%20script/py/multiRename.py) 名前一括変更

選択しているオブジェクトの名前の接頭辞と接尾辞を特定のパータンに一括で変更する

![MultiRenameGif](https://raw.githubusercontent.com/Julian-Fish/FishPythonProject/master/gif/multiRename/multiRename.gif)

### ![UVAlign](https://raw.githubusercontent.com/Julian-Fish/FishPythonProject/master/maya%20script/py/UVAlignVer2.py) UV整列（格子状）

選択しているUV頂点のシェールを格子状に整列する

![MultiRenameGif](https://raw.githubusercontent.com/Julian-Fish/FishPythonProject/master/gif/UVAlign/UVAlign.gif)

### ![Construct](https://raw.githubusercontent.com/Julian-Fish/FishPythonProject/master/maya%20script/py/Construct.py) シェルフの更新

シェルフを更新する

※ インターネット環境が必須

![ConstructGif](https://raw.githubusercontent.com/Julian-Fish/FishPythonProject/master/gif/Construct/construct.gif)

