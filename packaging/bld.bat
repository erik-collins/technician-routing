mkdir %PREFIX%\lib
mkdir %PREFIX%\lib\technician_routing

echo %RECIPE_DIR%
echo %PREFIX%

xcopy %RECIPE_DIR%\..\technician_routing\applications %PREFIX%\lib\technician_routing\applications\ /f /s /e
xcopy %RECIPE_DIR%\..\technician_routing\data_management %PREFIX%\lib\technician_routing\data_management\ /f /s /e
xcopy %RECIPE_DIR%\..\technician_routing\routing_toolkit %PREFIX%\lib\technician_routing\routing_toolkit\ /f /s /e