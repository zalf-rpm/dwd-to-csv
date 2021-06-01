#!/bin/bash

python=~/.conda/envs/py38/bin/python

#historical
srun -l --job-name=berg_hist_ICH_KNM_r1 $python transform_daily_netcdf_to_csv_dwd_core_ensemble.py csvs=csvs/ \
gcm=ICHEC-EC-EARTH rcm=KNMI-RACMO22E scen=historical ensmem=r1i1p1 version=v1 > out_hist_ICH_KNM_r1 2> eout_hist_ICH_KNM_r1 &

srun -l --job-name=berg_hist_MOH_CLM $python transform_daily_netcdf_to_csv_dwd_core_ensemble.py csvs=csvs/ \
gcm=MOHC-HadGEM2-ES rcm=CLMcom-CCLM4-8-17 scen=historical ensmem=r1i1p1 version=v1 > out_hist_MOH_CLM 2> eout_hist_MOH_CLM &

srun -l --job-name=berg_hist_CCC_CLM $python transform_daily_netcdf_to_csv_dwd_core_ensemble.py csvs=csvs/ \
gcm=CCCma-CanESM2 rcm=CLMcom-CCLM4-8-17 scen=historical ensmem=r1i1p1 version=v1 > out_hist_CCC_CLM 2> eout_hist_CCC_CLM &

srun -l --job-name=berg_hist_MIR_REM $python transform_daily_netcdf_to_csv_dwd_core_ensemble.py csvs=csvs/ \
gcm=MIROC-MIROC5 rcm=GERICS-REMO2015 scen=historical ensmem=r1i1p1 version=v1 > out_hist_MIR_REM 2> eout_hist_MIR_REM &

srun -l --job-name=berg_hist_MPI_MPI_r2 $python transform_daily_netcdf_to_csv_dwd_core_ensemble.py csvs=csvs/ \
gcm=MPI-M-MPI-ESM-LR rcm=MPI-CSC-REMO2009 scen=historical ensmem=r2i1p1 version=v1 > out_hist_MPI_MPI_r2 2> eout_hist_MPI_MPI_r2 &

srun -l --job-name=berg_hist_MPI_UHO $python transform_daily_netcdf_to_csv_dwd_core_ensemble.py csvs=csvs/ \
gcm=MPI-M-MPI-ESM-LR rcm=UHOH-WRF361H scen=historical ensmem=r1i1p1 version=v1 > out_hist_MPI_UHO 2> eout_hist_MPI_UHO &

srun -l --job-name=berg_hist_ICH_SMH $python transform_daily_netcdf_to_csv_dwd_core_ensemble.py csvs=csvs/ \
gcm=ICHEC-EC-EARTH rcm=SMHI-RCA4 scen=historical ensmem=r12i1p1 version=v1 > out_hist_ICH_SMH 2> eout_hist_ICH_SMH &

srun -l --job-name=berg_hist_MPI_MPI_r1 $python transform_daily_netcdf_to_csv_dwd_core_ensemble.py csvs=csvs/ \
gcm=MPI-M-MPI-ESM-LR rcm=MPI-CSC-REMO2009 scen=historical ensmem=r1i1p1 version=v1 > out_hist_MPI_MPI_r1 2> eout_hist_MPI_MPI_r1 &

srun -l --job-name=berg_hist_ICH_KNM_r12 $python transform_daily_netcdf_to_csv_dwd_core_ensemble.py csvs=csvs/ \
gcm=ICHEC-EC-EARTH rcm=KNMI-RACMO22E scen=historical ensmem=r12i1p1 version=v1 > out_hist_ICH_KNM_r12 2> eout_hist_ICH_KNM_r12 &

srun -l --job-name=berg_hist_MOH_KNM $python transform_daily_netcdf_to_csv_dwd_core_ensemble.py csvs=csvs/ \
gcm=MOHC-HadGEM2-ES rcm=KNMI-RACMO22E scen=historical ensmem=r1i1p1 version=v2 > out_hist_MOH_KNM 2> eout_hist_MOH_KNM &

srun -l --job-name=berg_hist_MIR_CLM $python transform_daily_netcdf_to_csv_dwd_core_ensemble.py csvs=csvs/ \
gcm=MIROC-MIROC5 rcm=CLMcom-CCLM4-8-17 scen=historical ensmem=r1i1p1 version=v1 > out_hist_MIR_CLM 2> eout_hist_MIR_CLM &

srun -l --job-name=berg_hist_ICH_CLM $python transform_daily_netcdf_to_csv_dwd_core_ensemble.py csvs=csvs/ \
gcm=ICHEC-EC-EARTH rcm=CLMcom-CCLM4-8-17 scen=historical ensmem=r12i1p1 version=v1 > out_hist_ICH_CLM 2> eout_hist_ICH_CLM &

#RCP8.5
srun -l --job-name=berg_85_ICH_KNM $python transform_daily_netcdf_to_csv_dwd_core_ensemble.py csvs=csvs/ \
gcm=ICHEC-EC-EARTH rcm=KNMI-RACMO22E scen=rcp85 ensmem=r1i1p1 version=v1 > out_85_ICH_KNM 2> eout_85_ICH_KNM &

srun -l --job-name=berg_85_MOH_CLM $python transform_daily_netcdf_to_csv_dwd_core_ensemble.py csvs=csvs/ \
gcm=MOHC-HadGEM2-ES rcm=CLMcom-CCLM4-8-17 scen=rcp85 ensmem=r1i1p1 version=v1 > out_85_MOH_CLM 2> eout_85_MOH_CLM &

srun -l --job-name=berg_85_CCC_CLM $python transform_daily_netcdf_to_csv_dwd_core_ensemble.py csvs=csvs/ \
gcm=CCCma-CanESM2 rcm=CLMcom-CCLM4-8-17 scen=rcp85 ensmem=r1i1p1 version=v1 > out_85_CCC_CLM 2> eout_85_CCC_CLM &

srun -l --job-name=berg_85_MIR_REM $python transform_daily_netcdf_to_csv_dwd_core_ensemble.py csvs=csvs/ \
gcm=MIROC-MIROC5 rcm=GERICS-REMO2015 scen=rcp85 ensmem=r1i1p1 version=v1 > out_85_MIR_REM 2> eout_85_MIR_REM &

srun -l --job-name=berg_85_MPI_MPI $python transform_daily_netcdf_to_csv_dwd_core_ensemble.py csvs=csvs/ \
gcm=MPI-M-MPI-ESM-LR rcm=MPI-CSC-REMO2009 scen=rcp85 ensmem=r2i1p1 version=v1 > out_85_MPI_MPI 2> eout_85_MPI_MPI &

srun -l --job-name=berg_85_MPI_UHO $python transform_daily_netcdf_to_csv_dwd_core_ensemble.py csvs=csvs/ \
gcm=MPI-M-MPI-ESM-LR rcm=UHOH-WRF361H scen=rcp85 ensmem=r1i1p1 version=v1 > out_85_MPI_UHO 2> eout_85_MPI_UHO &

#RCP4.5
srun -l --job-name=berg_45_MOH_CLM $python transform_daily_netcdf_to_csv_dwd_core_ensemble.py csvs=csvs/ \
gcm=MOHC-HadGEM2-ES rcm=CLMcom-CCLM4-8-17 scen=rcp45 ensmem=r1i1p1 version=v1 > out_45_MOH_CLM 2> eout_45_MOH_CLM &

srun -l --job-name=berg_45_ICH_KNM_r1 $python transform_daily_netcdf_to_csv_dwd_core_ensemble.py csvs=csvs/ \
gcm=ICHEC-EC-EARTH rcm=KNMI-RACMO22E scen=rcp45 ensmem=r1i1p1 version=v1 > out_45_ICH_KNM_r1 2> eout_45_ICH_KNM_r1 &

srun -l --job-name=berg_45_ICH_SMH $python transform_daily_netcdf_to_csv_dwd_core_ensemble.py csvs=csvs/ \
gcm=ICHEC-EC-EARTH rcm=SMHI-RCA4 scen=rcp45 ensmem=r12i1p1 version=v1 > out_45_ICH_SMH 2> eout_45_ICH_SMH &

srun -l --job-name=berg_45_MPI_MPI_r1 $python transform_daily_netcdf_to_csv_dwd_core_ensemble.py csvs=csvs/ \
gcm=MPI-M-MPI-ESM-LR rcm=MPI-CSC-REMO2009 scen=rcp45 ensmem=r1i1p1 version=v1 > out_45_MPI_MPI_r1 2> eout_45_MPI_MPI_r1 &

srun -l --job-name=berg_45_MPI_MPI_r2 $python transform_daily_netcdf_to_csv_dwd_core_ensemble.py csvs=csvs/ \
gcm=MPI-M-MPI-ESM-LR rcm=MPI-CSC-REMO2009 scen=rcp45 ensmem=r2i1p1 version=v1 > out_45_MPI_MPI_r2 2> eout_45_MPI_MPI_r2 &

srun -l --job-name=berg_45_ICH_KNM_r12 $python transform_daily_netcdf_to_csv_dwd_core_ensemble.py csvs=csvs/ \
gcm=ICHEC-EC-EARTH rcm=KNMI-RACMO22E scen=rcp45 ensmem=r12i1p1 version=v1 > out_45_ICH_KNM_r12 2> eout_45_ICH_KNM_r12 &

#RCP2.6
srun -l --job-name=berg_26_MOH_KNM $python transform_daily_netcdf_to_csv_dwd_core_ensemble.py csvs=csvs/ \
gcm=MOHC-HadGEM2-ES rcm=KNMI-RACMO22E scen=rcp26 ensmem=r1i1p1 version=v2 > out_26_MOH_KNM 2> eout_26_MOH_KNM &

srun -l --job-name=berg_26_MPI_MPI $python transform_daily_netcdf_to_csv_dwd_core_ensemble.py csvs=csvs/ \
gcm=MPI-M-MPI-ESM-LR rcm=MPI-CSC-REMO2009 scen=rcp26 ensmem=r2i1p1 version=v1 > out_26_MPI_MPI 2> eout_26_MPI_MPI &

srun -l --job-name=berg_26_MIR_CLM $python transform_daily_netcdf_to_csv_dwd_core_ensemble.py csvs=csvs/ \
gcm=MIROC-MIROC5 rcm=CLMcom-CCLM4-8-17 scen=rcp26 ensmem=r1i1p1 version=v1 > out_26_MIR_CLM 2> eout_26_MIR_CLM &

srun -l --job-name=berg_26_ICH_CLM $python transform_daily_netcdf_to_csv_dwd_core_ensemble.py csvs=csvs/ \
gcm=ICHEC-EC-EARTH rcm=CLMcom-CCLM4-8-17 scen=rcp26 ensmem=r12i1p1 version=v1 > out_26_ICH_CLM 2> eout_26_ICH_CLM &

srun -l --job-name=berg_26_ICH_KNM $python transform_daily_netcdf_to_csv_dwd_core_ensemble.py csvs=csvs/ \
gcm=ICHEC-EC-EARTH rcm=KNMI-RACMO22E scen=rcp26 ensmem=r12i1p1 version=v1 > out_26_ICH_KNM 2> eout_26_ICH_KNM &
