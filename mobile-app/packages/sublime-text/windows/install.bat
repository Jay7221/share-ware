@echo off
setlocal enabledelayedexpansion

:: Set the path to the Sublime Text executable (sublime_text.exe)
set SUBLINE_EXECUTABLE_PATH=C:\Path\To\Your\Sublime\sublime_text.exe

:: Set the installation directory for Sublime Text
set INSTALL_DIR=C:\Program Files\Sublime Text

:: Create the installation directory if it doesn't exist
if not exist "%INSTALL_DIR%" (
    mkdir "%INSTALL_DIR%"
)

:: Copy Sublime Text executable to the installation directory
copy "%SUBLINE_EXECUTABLE_PATH%" "%INSTALL_DIR%"

:: Create a shortcut on the desktop
set SHORTCUT_NAME=Sublime Text.lnk
set SHORTCUT_TARGET="%INSTALL_DIR%\sublime_text.exe"
set SHORTCUT_DIR="%userprofile%\Desktop"
set SHORTCUT_SCRIPT="%TEMP%\CreateShortcut.vbs"

:: Create a VBScript to create the desktop shortcut
echo Set oWS = WScript.CreateObject("WScript.Shell") > "%SHORTCUT_SCRIPT%"
echo sLinkFile = %SHORTCUT_DIR%\%SHORTCUT_NAME% >> "%SHORTCUT_SCRIPT%"
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> "%SHORTCUT_SCRIPT%"
echo oLink.TargetPath = %SHORTCUT_TARGET% >> "%SHORTCUT_SCRIPT%"
echo oLink.Save >> "%SHORTCUT_SCRIPT%"

:: Run the VBScript to create the shortcut
cscript "%SHORTCUT_SCRIPT%"

:: Clean up the temporary VBScript file
del "%SHORTCUT_SCRIPT%"

echo Sublime Text has been installed to %INSTALL_DIR%
echo A desktop shortcut has been created.

endlocal
