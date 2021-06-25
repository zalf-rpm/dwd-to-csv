#!/bin/bash

python=~/.conda/envs/py38/bin/python

#8.5
srun -l --job-name=b685MPIUHO $python transform_daily_netcdf_to_csv_dwd_core_ensemble.py restart=true start_year=2095 csvs=csvs/ \
gcm=MPI-M-MPI-ESM-LR rcm=UHOH-WRF361H scen=rcp85 ensmem=r1i1p1 version=v1 > out_85_MPI_UHO_6 2> eout_85_MPI_UHO_6 &

#8.5
srun -l --job-name=b6185MOHCLM $python transform_daily_netcdf_to_csv_dwd_core_ensemble.py start_y=1 end_y=80 csvs=csvs/ \
gcm=MOHC-HadGEM2-ES rcm=CLMcom-CCLM4-8-17 scen=rcp85 ensmem=r1i1p1 version=v1 > out_85_MOH_CLM_16 2> eout_85_MOH_CLM_16 &

srun -l --job-name=b6285MOHCLM $python transform_daily_netcdf_to_csv_dwd_core_ensemble.py start_y=81 end_y=110 csvs=csvs/ \
gcm=MOHC-HadGEM2-ES rcm=CLMcom-CCLM4-8-17 scen=rcp85 ensmem=r1i1p1 version=v1 > out_85_MOH_CLM_26 2> eout_85_MOH_CLM_26 &

srun -l --job-name=b6385MOHCLM $python transform_daily_netcdf_to_csv_dwd_core_ensemble.py start_y=111 end_y=140 csvs=csvs/ \
gcm=MOHC-HadGEM2-ES rcm=CLMcom-CCLM4-8-17 scen=rcp85 ensmem=r1i1p1 version=v1 > out_85_MOH_CLM_36 2> eout_85_MOH_CLM_36 &

srun -l --job-name=b6485MOHCLM $python transform_daily_netcdf_to_csv_dwd_core_ensemble.py start_y=141 end_y=170 csvs=csvs/ \
gcm=MOHC-HadGEM2-ES rcm=CLMcom-CCLM4-8-17 scen=rcp85 ensmem=r1i1p1 version=v1 > out_85_MOH_CLM_46 2> eout_85_MOH_CLM_46 &

srun -l --job-name=b6585MOHCLM $python transform_daily_netcdf_to_csv_dwd_core_ensemble.py start_y=171 end_y=220 csvs=csvs/ \
gcm=MOHC-HadGEM2-ES rcm=CLMcom-CCLM4-8-17 scen=rcp85 ensmem=r1i1p1 version=v1 > out_85_MOH_CLM_56 2> eout_85_MOH_CLM_56 &



srun -l --job-name=b6185CCCCLM $python transform_daily_netcdf_to_csv_dwd_core_ensemble.py start_y=1 end_y=80 csvs=csvs/ \
gcm=CCCma-CanESM2 rcm=CLMcom-CCLM4-8-17 scen=rcp85 ensmem=r1i1p1 version=v1 > out_85_CCC_CLM_16 2> eout_85_CCC_CLM_16 &

srun -l --job-name=b6285CCCCLM $python transform_daily_netcdf_to_csv_dwd_core_ensemble.py start_y=81 end_y=110 csvs=csvs/ \
gcm=CCCma-CanESM2 rcm=CLMcom-CCLM4-8-17 scen=rcp85 ensmem=r1i1p1 version=v1 > out_85_CCC_CLM_26 2> eout_85_CCC_CLM_26 &

srun -l --job-name=b6385CCCCLM $python transform_daily_netcdf_to_csv_dwd_core_ensemble.py start_y=111 end_y=140 csvs=csvs/ \
gcm=CCCma-CanESM2 rcm=CLMcom-CCLM4-8-17 scen=rcp85 ensmem=r1i1p1 version=v1 > out_85_CCC_CLM_36 2> eout_85_CCC_CLM_36 &

srun -l --job-name=b6485CCCCLM $python transform_daily_netcdf_to_csv_dwd_core_ensemble.py start_y=141 end_y=170 csvs=csvs/ \
gcm=CCCma-CanESM2 rcm=CLMcom-CCLM4-8-17 scen=rcp85 ensmem=r1i1p1 version=v1 > out_85_CCC_CLM_46 2> eout_85_CCC_CLM_46 &

srun -l --job-name=b6585CCCCLM $python transform_daily_netcdf_to_csv_dwd_core_ensemble.py start_y=171 end_y=220 csvs=csvs/ \
gcm=CCCma-CanESM2 rcm=CLMcom-CCLM4-8-17 scen=rcp85 ensmem=r1i1p1 version=v1 > out_85_CCC_CLM_56 2> eout_85_CCC_CLM_56 &

