set MAYA_Version=2019
set FISHSHELF_PATH=%UserProfile%\Documents\maya\%MAYA_Version%\prefs\shelves\FishShelf

md %FISHSHELF_PATH%

xcopy .\FishShelf %FISHSHELF_PATH% /e /y

pause