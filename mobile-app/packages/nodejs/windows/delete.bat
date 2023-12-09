@echo off
echo Uninstalling Node.js...

:: Set the installation directory where Node.js is located
set INSTALL_DIR=C:\Node

:: Check if Node.js is installed in the specified directory
if not exist %INSTALL_DIR% (
    echo Node.js is not installed in %INSTALL_DIR%
    exit /b
)

:: Uninstall Node.js
msiexec /x %INSTALL_DIR%\nodejs\nodejs.msi /qn /l*v %TEMP%\nodejs_uninstall.log

:: Check if the uninstallation was successful
if not exist %INSTALL_DIR%\nodejs\nodejs.msi (
    echo Node.js has been successfully uninstalled from %INSTALL_DIR%
) else (
    echo Uninstallation of Node.js failed. Please check %TEMP%\nodejs_uninstall.log for details.
)

:: Remove the installation directory
rmdir /s /q %INSTALL_DIR%
