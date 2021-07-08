::@echo off

:READ THE PATH OF THE BATCH FILE

set cd=%~dp0

set Condaactivate="C:\Users\............\Miniconda3/Scripts/activate.bat"
set environment=hydrology38

set POpy="%cd%\PO_STATS.py"
set WSELpy="%cd%\WSEL_STATS.py"
set Depthpy="%cd%\DEPTH_STATS.py"

call  %Condaactivate% %environment%


python %POpy% %tcf% %resultsfolder%
python %WSELpy% %tcf% %resultsfolder% %asctoasc%
python %Depthpy% %tcf% %resultsfolder% %asctoasc%

pause
