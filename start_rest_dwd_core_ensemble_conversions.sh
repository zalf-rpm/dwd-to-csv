#!/bin/bash

python=~/.conda/envs/py38/bin/python

#historical
srun -l --job-name=b7hCCGE $python transform_daily_netcdf_to_csv_dwd_core_ensemble.py csvs=csvs/ \
gcm=CCCma-CanESM2 rcm=GERICS-REMO2015 scen=historical ensmem=r1i1p1 version=v1 > out_7_hist_CCC_GER 2> eout_7_hist_CCC_GER &

srun -l --job-name=b7hICGE $python transform_daily_netcdf_to_csv_dwd_core_ensemble.py csvs=csvs/ \
gcm=ICHEC-EC-EARTH rcm=GERICS-REMO2015 scen=historical ensmem=r12i1p1 version=v1 > out_7_hist_CCC_GER 2> eout_7_hist_CCC_GER &

srun -l --job-name=b7hMOSM $python transform_daily_netcdf_to_csv_dwd_core_ensemble.py csvs=csvs/ \
gcm=MOHC-HadGEM2-ES rcm=SMHI-RCA4 scen=historical ensmem=r1i1p1 version=v1 > out_7_hist_MOH_SMH 2> eout_7_hist_MOH_SMH &

srun -l --job-name=b7hMOUH $python transform_daily_netcdf_to_csv_dwd_core_ensemble.py csvs=csvs/ \
gcm=MOHC-HadGEM2-ES rcm=UHOH-WRF361H scen=historical ensmem=r1i1p1 version=v1 > out_7_hist_MOH_UHO 2> eout_7_hist_MOH_UHO &

srun -l --job-name=b7hMOGE $python transform_daily_netcdf_to_csv_dwd_core_ensemble.py csvs=csvs/ \
gcm=MOHC-HadGEM2-ES rcm=GERICS-REMO2015 scen=historical ensmem=r1i1p1 version=v1 > out_7_hist_MOH_GER 2> eout_7_hist_MOH_GER &

srun -l --job-name=b7hMPSM $python transform_daily_netcdf_to_csv_dwd_core_ensemble.py csvs=csvs/ \
gcm=MPI-M-MPI-ESM-LR rcm=SMHI-RCA4 scen=historical ensmem=r1i1p1 version=v1a > out_7_hist_MPI_SMH 2> eout_7_hist_MPI_SMH &

srun -l --job-name=b7hMPCL $python transform_daily_netcdf_to_csv_dwd_core_ensemble.py csvs=csvs/ \
gcm=MPI-M-MPI-ESM-LR rcm=CLMcom-CCLM4-8-17 scen=historical ensmem=r1i1p1 version=v1 > out_7_hist_MPI_CLM 2> eout_7_hist_MPI_CLM &

srun -l --job-name=b7hIPSM $python transform_daily_netcdf_to_csv_dwd_core_ensemble.py csvs=csvs/ \
gcm=IPSL-IPSL-CM5A-MR rcm=SMHI-RCA4 scen=historical ensmem=r1i1p1 version=v1 > out_7_hist_IPS_SMH 2> eout_7_hist_IPS_SMH &


#RCP8.5
srun -l --job-name=b785MICL $python transform_daily_netcdf_to_csv_dwd_core_ensemble.py csvs=csvs/ \
gcm=MIROC-MIROC5 rcm=CLMcom-CCLM4-8-17 scen=rcp85 ensmem=r1i1p1 version=v1 > out_7_85_MIR_CLM 2> eout_7_85_MIR_CLM &

srun -l --job-name=b785CCGE $python transform_daily_netcdf_to_csv_dwd_core_ensemble.py csvs=csvs/ \
gcm=CCCma-CanESM2 rcm=GERICS-REMO2015 scen=rcp85 ensmem=r1i1p1 version=v1 > out_7_85_CCC_GER 2> eout_7_85_CCC_GER &

srun -l --job-name=b785ICSM $python transform_daily_netcdf_to_csv_dwd_core_ensemble.py csvs=csvs/ \
gcm=ICHEC-EC-EARTH rcm=SMHI-RCA4 scen=rcp85 ensmem=r12i1p1 version=v1 > out_7_85_ICH_SMH 2> eout_7_85_ICH_SMH &

srun -l --job-name=b785ICKN $python transform_daily_netcdf_to_csv_dwd_core_ensemble.py csvs=csvs/ \
gcm=ICHEC-EC-EARTH rcm=KNMI-RACMO22E scen=rcp85 ensmem=r12i1p1 version=v1 > out_7_85_ICH_KNM 2> eout_7_85_ICH_KNM &

srun -l --job-name=b785ICGE $python transform_daily_netcdf_to_csv_dwd_core_ensemble.py csvs=csvs/ \
gcm=ICHEC-EC-EARTH rcm=GERICS-REMO2015 scen=rcp85 ensmem=r12i1p1 version=v1 > out_7_85_ICH_GER 2> eout_7_85_ICH_GER &

srun -l --job-name=b785ICCL $python transform_daily_netcdf_to_csv_dwd_core_ensemble.py csvs=csvs/ \
gcm=ICHEC-EC-EARTH rcm=CLMcom-CCLM4-8-17 scen=rcp85 ensmem=r12i1p1 version=v1 > out_7_85_ICH_CLM 2> eout_7_85_ICH_CLM &

srun -l --job-name=b785MOSM $python transform_daily_netcdf_to_csv_dwd_core_ensemble.py csvs=csvs/ \
gcm=MOHC-HadGEM2-ES rcm=SMHI-RCA4 scen=rcp85 ensmem=r1i1p1 version=v1 > out_7_85_MOH_SMH 2> eout_7_85_MOH_SMH &

srun -l --job-name=b785MOUH $python transform_daily_netcdf_to_csv_dwd_core_ensemble.py csvs=csvs/ \
gcm=MOHC-HadGEM2-ES rcm=UHOH-WRF361H scen=rcp85 ensmem=r1i1p1 version=v1 > out_7_85_MOH_UHO 2> eout_7_85_MOH_UHO &

srun -l --job-name=b785MOKN $python transform_daily_netcdf_to_csv_dwd_core_ensemble.py csvs=csvs/ \
gcm=MOHC-HadGEM2-ES rcm=KNMI-RACMO22E scen=rcp85 ensmem=r1i1p1 version=v2 > out_7_85_MOH_KNM 2> eout_7_85_MOH_KNM &

srun -l --job-name=b785MOGE $python transform_daily_netcdf_to_csv_dwd_core_ensemble.py csvs=csvs/ \
gcm=MOHC-HadGEM2-ES rcm=GERICS-REMO2015 scen=rcp85 ensmem=r1i1p1 version=v1 > out_7_85_MOH_GER 2> eout_7_85_MOH_GER &

srun -l --job-name=b785MPSM $python transform_daily_netcdf_to_csv_dwd_core_ensemble.py csvs=csvs/ \
gcm=MPI-M-MPI-ESM-LR rcm=SMHI-RCA4 scen=rcp85 ensmem=r1i1p1 version=v1a > out_7_85_MPI_SMH 2> eout_7_85_MPI_SMH &

srun -l --job-name=b785MPMP $python transform_daily_netcdf_to_csv_dwd_core_ensemble.py csvs=csvs/ \
gcm=MPI-M-MPI-ESM-LR rcm=MPI-CSC-REMO2009 scen=rcp85 ensmem=r1i1p1 version=v1 > out_7_85_MPI_MPI 2> eout_7_85_MPI_MPI &

srun -l --job-name=b785MPCL $python transform_daily_netcdf_to_csv_dwd_core_ensemble.py csvs=csvs/ \
gcm=MPI-M-MPI-ESM-LR rcm=CLMcom-CCLM4-8-17 scen=rcp85 ensmem=r1i1p1 version=v1 > out_7_85_MPI_CLM 2> eout_7_85_MPI_CLM &

srun -l --job-name=b785IPSM $python transform_daily_netcdf_to_csv_dwd_core_ensemble.py csvs=csvs/ \
gcm=IPSL-IPSL-CM5A-MR rcm=SMHI-RCA4 scen=rcp85 ensmem=r1i1p1 version=v1 > out_7_85_IPS_SMH 2> eout_7_85_IPS_SMH &


#RCP4.5
srun -l --job-name=b745ICCL $python transform_daily_netcdf_to_csv_dwd_core_ensemble.py csvs=csvs/ \
gcm=ICHEC-EC-EARTH rcm=CLMcom-CCLM4-8-17 scen=rcp45 ensmem=r12i1p1 version=v1 > out_7_45_ICH_CLM 2> eout_7_45_ICH_CLM &

srun -l --job-name=b745MOSM $python transform_daily_netcdf_to_csv_dwd_core_ensemble.py csvs=csvs/ \
gcm=MOHC-HadGEM2-ES rcm=SMHI-RCA4 scen=rcp45 ensmem=r1i1p1 version=v1 > out_7_45_MOH_SMH 2> eout_7_45_MOH_SMH &

srun -l --job-name=b745MOKN $python transform_daily_netcdf_to_csv_dwd_core_ensemble.py csvs=csvs/ \
gcm=MOHC-HadGEM2-ES rcm=KNMI-RACMO22E scen=rcp45 ensmem=r1i1p1 version=v2 > out_7_45_MOH_KNM 2> eout_7_45_MOH_KNM &

srun -l --job-name=b745MPSM $python transform_daily_netcdf_to_csv_dwd_core_ensemble.py csvs=csvs/ \
gcm=MPI-M-MPI-ESM-LR rcm=SMHI-RCA4 scen=rcp45 ensmem=r1i1p1 version=v1a > out_7_45_MPI_SMH 2> eout_7_45_MPI_SMH &

srun -l --job-name=b745MPCL $python transform_daily_netcdf_to_csv_dwd_core_ensemble.py csvs=csvs/ \
gcm=MPI-M-MPI-ESM-LR rcm=CLMcom-CCLM4-8-17 scen=rcp45 ensmem=r1i1p1 version=v1 > out_7_45_MPI_CLM 2> eout_7_45_MPI_CLM &

srun -l --job-name=b745IPSM $python transform_daily_netcdf_to_csv_dwd_core_ensemble.py csvs=csvs/ \
gcm=IPSL-IPSL-CM5A-MR rcm=SMHI-RCA4 scen=rcp45 ensmem=r1i1p1 version=v1 > out_7_45_IPS_SMH 2> eout_7_45_IPS_SMH &


#RCP2.6
srun -l --job-name=b726ICSM $python transform_daily_netcdf_to_csv_dwd_core_ensemble.py csvs=csvs/ \
gcm=ICHEC-EC-EARTH rcm=SMHI-RCA4 scen=rcp26 ensmem=r12i1p1 version=v1 > out_7_26_ICH_SMH 2> eout_7_26_ICH_SMH &

srun -l --job-name=b726MOSM $python transform_daily_netcdf_to_csv_dwd_core_ensemble.py csvs=csvs/ \
gcm=MOHC-HadGEM2-ES rcm=SMHI-RCA4 scen=rcp26 ensmem=r1i1p1 version=v1 > out_7_26_MOH_SMH 2> eout_7_26_MOH_SMH &

srun -l --job-name=b726MPSM $python transform_daily_netcdf_to_csv_dwd_core_ensemble.py csvs=csvs/ \
gcm=MPI-M-MPI-ESM-LR rcm=SMHI-RCA4 scen=rcp26 ensmem=r1i1p1 version=v1a > out_7_26_MPI_SMH 2> eout_7_26_MPI_SMH &

srun -l --job-name=b726MPUH $python transform_daily_netcdf_to_csv_dwd_core_ensemble.py csvs=csvs/ \
gcm=MPI-M-MPI-ESM-LR rcm=UHOH-WRF361H scen=rcp26 ensmem=r1i1p1 version=v1 > out_7_26_MPI_UHO 2> eout_7_26_MPI_UHO &

srun -l --job-name=b726MPMP $python transform_daily_netcdf_to_csv_dwd_core_ensemble.py csvs=csvs/ \
gcm=MPI-M-MPI-ESM-LR rcm=MPI-CSC-REMO2009 scen=rcp26 ensmem=r1i1p1 version=v1 > out_7_26_MPI_MPI 2> eout_7_26_MPI_MPI &

srun -l --job-name=b726MPCL $python transform_daily_netcdf_to_csv_dwd_core_ensemble.py csvs=csvs/ \
gcm=MPI-M-MPI-ESM-LR rcm=CLMcom-BTU-CCLM4-8-17 scen=rcp26 ensmem=r1i1p1 version=v1 > out_7_26_MPI_CLM 2> eout_7_26_MPI_CLM &


