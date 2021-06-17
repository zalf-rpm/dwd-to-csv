#!/bin/bash

python=~/.conda/envs/py38/bin/python

#hist
srun -l --job-name=b5hMPIUHO $python transform_daily_netcdf_to_csv_dwd_core_ensemble.py csvs=csvs/ \
gcm=MPI-M-MPI-ESM-LR rcm=UHOH-WRF361H scen=historical ensmem=r1i1p1 version=v1 > out_hist_MPI_UHO_5 2> eout_hist_MPI_UHO_5 &


#8.5
srun -l --job-name=b5185ICHKNM $python transform_daily_netcdf_to_csv_dwd_core_ensemble.py start_y=1 end_y=80 csvs=csvs/ \
gcm=ICHEC-EC-EARTH rcm=KNMI-RACMO22E scen=rcp85 ensmem=r1i1p1 version=v1 > out_85_ICH_KNM_15 2> eout_85_ICH_KNM_15 &

srun -l --job-name=b5285ICHKNM $python transform_daily_netcdf_to_csv_dwd_core_ensemble.py start_y=81 end_y=150 csvs=csvs/ \
gcm=ICHEC-EC-EARTH rcm=KNMI-RACMO22E scen=rcp85 ensmem=r1i1p1 version=v1 > out_85_ICH_KNM_25 2> eout_85_ICH_KNM_25 &

srun -l --job-name=b5385ICHKNM $python transform_daily_netcdf_to_csv_dwd_core_ensemble.py start_y=151 end_y=220 csvs=csvs/ \
gcm=ICHEC-EC-EARTH rcm=KNMI-RACMO22E scen=rcp85 ensmem=r1i1p1 version=v1 > out_85_ICH_KNM_35 2> eout_85_ICH_KNM_35 &


srun -l --job-name=b5185CCCCLM $python transform_daily_netcdf_to_csv_dwd_core_ensemble.py start_y=1 end_y=80 csvs=csvs/ \
gcm=CCCma-CanESM2 rcm=CLMcom-CCLM4-8-17 scen=rcp85 ensmem=r1i1p1 version=v1 > out_85_CCC_CLM_15 2> eout_85_CCC_CLM_15 &

srun -l --job-name=b5285CCCCLM $python transform_daily_netcdf_to_csv_dwd_core_ensemble.py start_y=81 end_y=150 csvs=csvs/ \
gcm=CCCma-CanESM2 rcm=CLMcom-CCLM4-8-17 scen=rcp85 ensmem=r1i1p1 version=v1 > out_85_CCC_CLM_25 2> eout_85_CCC_CLM_25 &

srun -l --job-name=b5385CCCCLM $python transform_daily_netcdf_to_csv_dwd_core_ensemble.py start_y=151 end_y=220 csvs=csvs/ \
gcm=CCCma-CanESM2 rcm=CLMcom-CCLM4-8-17 scen=rcp85 ensmem=r1i1p1 version=v1 > out_85_CCC_CLM_35 2> eout_85_CCC_CLM_35 &


srun -l --job-name=b5185MIRREM $python transform_daily_netcdf_to_csv_dwd_core_ensemble.py start_y=1 end_y=80 csvs=csvs/ \
gcm=MIROC-MIROC5 rcm=GERICS-REMO2015 scen=rcp85 ensmem=r1i1p1 version=v1 > out_85_MIR_REM_15 2> eout_85_MIR_REM_15 &

srun -l --job-name=b5285MIRREM $python transform_daily_netcdf_to_csv_dwd_core_ensemble.py start_y=81 end_y=150 csvs=csvs/ \
gcm=MIROC-MIROC5 rcm=GERICS-REMO2015 scen=rcp85 ensmem=r1i1p1 version=v1 > out_85_MIR_REM_25 2> eout_85_MIR_REM_25 &

srun -l --job-name=b5385MIRREM $python transform_daily_netcdf_to_csv_dwd_core_ensemble.py start_y=151 end_y=220 csvs=csvs/ \
gcm=MIROC-MIROC5 rcm=GERICS-REMO2015 scen=rcp85 ensmem=r1i1p1 version=v1 > out_85_MIR_REM_35 2> eout_85_MIR_REM_35 &


srun -l --job-name=b5185MPIUHO $python transform_daily_netcdf_to_csv_dwd_core_ensemble.py start_y=1 end_y=80 csvs=csvs/ \
gcm=MPI-M-MPI-ESM-LR rcm=UHOH-WRF361H scen=rcp85 ensmem=r1i1p1 version=v1 > out_85_MPI_UHO_15 2> eout_85_MPI_UHO_15 &

srun -l --job-name=b5285MPIUHO $python transform_daily_netcdf_to_csv_dwd_core_ensemble.py start_y=81 end_y=150 csvs=csvs/ \
gcm=MPI-M-MPI-ESM-LR rcm=UHOH-WRF361H scen=rcp85 ensmem=r1i1p1 version=v1 > out_85_MPI_UHO_25 2> eout_85_MPI_UHO_25 &

srun -l --job-name=b5385MPIUHO $python transform_daily_netcdf_to_csv_dwd_core_ensemble.py start_y=151 end_y=220 csvs=csvs/ \
gcm=MPI-M-MPI-ESM-LR rcm=UHOH-WRF361H scen=rcp85 ensmem=r1i1p1 version=v1 > out_85_MPI_UHO_35 2> eout_85_MPI_UHO_35 &

#4.5
srun -l --job-name=b5145ICHKNMr1 $python transform_daily_netcdf_to_csv_dwd_core_ensemble.py start_y=1 end_y=80 csvs=csvs/ \
gcm=ICHEC-EC-EARTH rcm=KNMI-RACMO22E scen=rcp45 ensmem=r1i1p1 version=v1 > out_45_ICH_KNM_r1_15 2> eout_45_ICH_KNM_r1_15 &

srun -l --job-name=b5245ICHKNMr1 $python transform_daily_netcdf_to_csv_dwd_core_ensemble.py start_y=81 end_y=150 csvs=csvs/ \
gcm=ICHEC-EC-EARTH rcm=KNMI-RACMO22E scen=rcp45 ensmem=r1i1p1 version=v1 > out_45_ICH_KNM_r1_25 2> eout_45_ICH_KNM_r1_25 &

srun -l --job-name=b5345ICHKNMr1 $python transform_daily_netcdf_to_csv_dwd_core_ensemble.py start_y=151 end_y=220 csvs=csvs/ \
gcm=ICHEC-EC-EARTH rcm=KNMI-RACMO22E scen=rcp45 ensmem=r1i1p1 version=v1 > out_45_ICH_KNM_r1_35 2> eout_45_ICH_KNM_r1_35 &


srun -l --job-name=b5145MPIMPIr1 $python transform_daily_netcdf_to_csv_dwd_core_ensemble.py start_y=1 end_y=80 csvs=csvs/ \
gcm=MPI-M-MPI-ESM-LR rcm=MPI-CSC-REMO2009 scen=rcp45 ensmem=r1i1p1 version=v1 > out_45_MPI_MPI_r1_15 2> eout_45_MPI_MPI_r1_15 &

srun -l --job-name=b5245MPIMPIr1 $python transform_daily_netcdf_to_csv_dwd_core_ensemble.py start_y=81 end_y=150 csvs=csvs/ \
gcm=MPI-M-MPI-ESM-LR rcm=MPI-CSC-REMO2009 scen=rcp45 ensmem=r1i1p1 version=v1 > out_45_MPI_MPI_r1_25 2> eout_45_MPI_MPI_r1_25 &

srun -l --job-name=b5345MPIMPIr1 $python transform_daily_netcdf_to_csv_dwd_core_ensemble.py start_y=151 end_y=220 csvs=csvs/ \
gcm=MPI-M-MPI-ESM-LR rcm=MPI-CSC-REMO2009 scen=rcp45 ensmem=r1i1p1 version=v1 > out_45_MPI_MPI_r1_35 2> eout_45_MPI_MPI_r1_35 &

#2.6
srun -l --job-name=b5126ICHCLM $python transform_daily_netcdf_to_csv_dwd_core_ensemble.py start_y=1 end_y=80 csvs=csvs/ \
gcm=ICHEC-EC-EARTH rcm=CLMcom-CCLM4-8-17 scen=rcp26 ensmem=r12i1p1 version=v1 > out_26_ICH_CLM_15 2> eout_26_ICH_CLM_15 &

srun -l --job-name=b5226ICHCLM $python transform_daily_netcdf_to_csv_dwd_core_ensemble.py start_y=81 end_y=150 csvs=csvs/ \
gcm=ICHEC-EC-EARTH rcm=CLMcom-CCLM4-8-17 scen=rcp26 ensmem=r12i1p1 version=v1 > out_26_ICH_CLM_25 2> eout_26_ICH_CLM_25 &

srun -l --job-name=b5326ICHCLM $python transform_daily_netcdf_to_csv_dwd_core_ensemble.py start_y=151 end_y=220 csvs=csvs/ \
gcm=ICHEC-EC-EARTH rcm=CLMcom-CCLM4-8-17 scen=rcp26 ensmem=r12i1p1 version=v1 > out_26_ICH_CLM_35 2> eout_26_ICH_CLM_35 &

