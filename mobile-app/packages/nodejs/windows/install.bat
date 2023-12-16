@echo off
REM Download the node js installer from the official website
bitsadmin /transfer nodejs https://nodejs.org/dist/v16.13.0/node-v16.13.0-x64.msi %temp%\node-v16.13.0-x64.msi
REM Run the installer with default options
msiexec /i %temp%\node-v16.13.0-x64.msi /qn
REM Delete the installer file
del %temp%\node-v16.13.0-x64.msi
REM Verify that node js is installed
node -v
