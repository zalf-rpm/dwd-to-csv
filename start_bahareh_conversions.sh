#!/bin/bash

nohup python transform-daily-netcdf-to-csv-bahareh.py path_to_output=/beegfs/common/data/climate/dwd/cmip_cordex_reklies/csv2/ gcm=CCCma-CanESM2 > outCC 2> eoutCC &
nohup python transform-daily-netcdf-to-csv-bahareh.py path_to_output=/beegfs/common/data/climate/dwd/cmip_cordex_reklies/csv2/ gcm=IPSL-IPSL-CM5A-MR > outIP 2> eoutIP &
nohup python transform-daily-netcdf-to-csv-bahareh.py path_to_output=/beegfs/common/data/climate/dwd/cmip_cordex_reklies/csv2/ gcm=MIROC-MIROC5 > outMI 2> eoutMI &
nohup python transform-daily-netcdf-to-csv-bahareh.py path_to_output=/beegfs/common/data/climate/dwd/cmip_cordex_reklies/csv2/ gcm=MPI-M-MPI-ESM-LR scen=historial > outMPh 2> eoutMPh &
nohup python transform-daily-netcdf-to-csv-bahareh.py path_to_output=/beegfs/common/data/climate/dwd/cmip_cordex_reklies/csv2/ gcm=MPI-M-MPI-ESM-LR scen=rcp26 > outMP2 2> eoutMP2 &
nohup python transform-daily-netcdf-to-csv-bahareh.py path_to_output=/beegfs/common/data/climate/dwd/cmip_cordex_reklies/csv2/ gcm=MPI-M-MPI-ESM-LR scen=rcp85 > outMP8 2> eoutMP8 &
