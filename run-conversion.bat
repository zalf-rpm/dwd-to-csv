@echo off
set from_row=0
set to_row=499
set read_path=f:/
set write_path=f:/climate-data-out-%from_row%-%to_row%

cd f:

call :run 2013 2 false
for /L %%i in (2016,3,2039) do call :run %%i 2 true
call :run 2040 0 true

GOTO :eof

:run
set /a to_year=%1+%2
echo from-year:%1 to-year:%to_year%
java -Xms2g -Xmx4g -jar cluster-test-0.1.0-SNAPSHOT-standalone.jar test conversion read-path %read_path% write-path %write_path% from-year %1 to-year %to_year% from-row %from_row% to-row %to_row% skip-header? %3
GOTO :eof