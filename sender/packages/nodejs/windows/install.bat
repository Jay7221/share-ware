@echo off
echo Installing Node.js...

:: Set the Node.js version you want to install
set NODE_VERSION=14.17.0

:: Set the installation directory
set INSTALL_DIR=C:\Node

:: Create the installation directory
if not exist %INSTALL_DIR% mkdir %INSTALL_DIR%

:: Download the Node.js installer
curl -o %TEMP%\nodejs_installer.msi https://nodejs.org/dist/v%NODE_VERSION%/node-v%NODE_VERSION%-x64.msi

:: Install Node.js
msiexec /i %TEMP%\nodejs_installer.msi /qn /l*v %TEMP%\nodejs_install.log INSTALLDIR=%INSTALL_DIR%

:: Check if installation was successful
if exist %INSTALL_DIR%\node.exe (
    echo Node.js %NODE_VERSION% has been successfully installed to %INSTALL_DIR%
) else (
    echo Installation of Node.js failed. Please check %TEMP%\nodejs_install.log for details.
)

:: Clean up the installer
del %TEMP%\nodejs_installer.msi
