@echo off
REM Uninstall node from the Programs and Features
wmic product where "name like 'Node.js%%'" call uninstall /nointeractive
REM Delete the node and npm folders from the Program Files
rd /s /q "C:\Program Files\nodejs"
rd /s /q "C:\Program Files (x86)\nodejs"
REM Delete the node and npm folders from the AppData
rd /s /q "%AppData%\npm"
rd /s /q "%AppData%\npm-cache"
REM Delete the node and npm paths from the environment variables
for /f "tokens=2* delims= " %%a in ('reg query "HKCU\Environment" /v Path') do setx Path "%%b" /m
for /f "tokens=2* delims= " %%a in ('reg query "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" /v Path') do setx Path "%%b" /m
setx Path "%Path:;C:\Program Files\nodejs\=%" /m
setx Path "%Path:;C:\Program Files (x86)\nodejs\=%" /m
setx Path "%Path:;%AppData%\npm\=%" /m
REM Verify that node is deleted
node -v
npm -v