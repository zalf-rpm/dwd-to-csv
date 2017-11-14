echo off
set start_y=%1
set end_y=%2
set start_year=%3
set start_year2=%3
set start_month=%4
if %start_month% neq 1 (
    echo running rest of year %start_year% starting with month %start_month%
    set /a start_year2+=1
    rem echo start_year=%start_year%
    for /l %%m in (%start_month%,1,12) do (
        rem echo month=%%m
        python transform-daily-netcdf-to-csv.py start-y=%start_y% end-y=%end_y% start-year=%start_year% end-year=%start_year% start-month=%%m end-month=%%m
    )
) 

echo running years starting at %start_year2%
for /l %%y in (%start_year2%,1,2012) do (
    rem echo year=%%y
    for /l %%m in (1,1,12) do (
        rem echo month=%%m
        python transform-daily-netcdf-to-csv.py start-y=%start_y% end-y=%end_y% start-year=%%y end-year=%%y start-month=%%m end-month=%%m
    )
)