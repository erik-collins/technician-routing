mkdir %PREFIX%\lib
mkdir %PREFIX%\lib\technician_routing

echo %RECIPE_DIR%
echo %PREFIX%

xcopy %RECIPE_DIR%\..\technician_routing %PREFIX%\lib\technician_routing\ /f /s /e