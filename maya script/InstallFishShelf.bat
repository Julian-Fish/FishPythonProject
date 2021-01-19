set MAYA_Version=2019
set FISHSHELF_PATH=%UserProfile%\Documents\maya\%MAYA_Version%\prefs\shelves\FishShelf

md %FISHSHELF_PATH%
md %FISHSHELF_PATH%\qtui

xcopy .\qtui %FISHSHELF_PATH%\qtui /e /y
xcopy .\FishShelf.mel %FISHSHELF_PATH% /y

pause