::@echo off

:READ THE PATH OF THE BATCH FILE

set cd=%~dp0

set environment=hydrology38

set POpy="%cd%\PO_STATS.py"
set WSELpy="%cd%\WSEL_STATS.py"
set Depthpy="%cd%\DEPTH_STATS.py"
set python="\python-3.8.10.amd64\python.exe"

%python% %POpy% %tcf% %resultsfolder%
%python% %WSELpy% %tcf% %resultsfolder% %asctoasc%
%python% %Depthpy% %tcf% %resultsfolder% %asctoasc%
