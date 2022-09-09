@echo off

echo :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
echo ::       Clear the project of artifacts from past builds       ::
echo :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
call clean.bat
echo Done

:: Запускаем установочник
echo :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
echo ::                  Building CAN Library installer             ::
echo :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
iscc.exe /q .\\SetupScripts\\vscan_build_setup.iss
echo Done

goto :EOF

:ERROR
cd %currentDir%
echo "FAILED. Errors were during building"
exit /B 1