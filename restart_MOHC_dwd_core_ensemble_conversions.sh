#!/bin/bash

python=~/.conda/envs/py38/bin/python

#historical
#srun -l --job-name=berg_hist_MOH_CLM $python transform_daily_netcdf_to_csv_dwd_core_ensemble.py csvs=csvs/ \
#gcm=MOHC-HadGEM2-ES rcm=CLMcom-CCLM4-8-17 scen=historical ensmem=r1i1p1 version=v1 > out_hist_MOH_CLM_3 2> eout_hist_MOH_CLM_3 &

#srun -l --job-name=berg_hist_MOH_KNM $python transform_daily_netcdf_to_csv_dwd_core_ensemble.py csvs=csvs/ \
#gcm=MOHC-HadGEM2-ES rcm=KNMI-RACMO22E scen=historical ensmem=r1i1p1 version=v2 > out_hist_MOH_KNM_3 2> eout_hist_MOH_KNM_3 &

#RCP8.5
srun -l --job-name=berg_85_1MOH_CLM $python transform_daily_netcdf_to_csv_dwd_core_ensemble.py start_y=1 end_y=80 csvs=csvs/ \
gcm=MOHC-HadGEM2-ES rcm=CLMcom-CCLM4-8-17 scen=rcp85 ensmem=r1i1p1 version=v1 > out_85_MOH_CLM_13 2> eout_85_MOH_CLM_13 &

srun -l --job-name=berg_85_2MOH_CLM $python transform_daily_netcdf_to_csv_dwd_core_ensemble.py start_y=81 end_y=150 csvs=csvs/ \
gcm=MOHC-HadGEM2-ES rcm=CLMcom-CCLM4-8-17 scen=rcp85 ensmem=r1i1p1 version=v1 > out_85_MOH_CLM_23 2> eout_85_MOH_CLM_23 &

srun -l --job-name=berg_85_3MOH_CLM $python transform_daily_netcdf_to_csv_dwd_core_ensemble.py start_y=151 end_y=220 csvs=csvs/ \
gcm=MOHC-HadGEM2-ES rcm=CLMcom-CCLM4-8-17 scen=rcp85 ensmem=r1i1p1 version=v1 > out_85_MOH_CLM_33 2> eout_85_MOH_CLM_33 &

#RCP4.5
srun -l --job-name=berg_45_1MOH_CLM $python transform_daily_netcdf_to_csv_dwd_core_ensemble.py start_y=1 end_y=80 csvs=csvs/ \
gcm=MOHC-HadGEM2-ES rcm=CLMcom-CCLM4-8-17 scen=rcp45 ensmem=r1i1p1 version=v1 > out_45_MOH_CLM_13 2> eout_45_MOH_CLM_13 &

srun -l --job-name=berg_45_2MOH_CLM $python transform_daily_netcdf_to_csv_dwd_core_ensemble.py start_y=81 end_y=150 csvs=csvs/ \
gcm=MOHC-HadGEM2-ES rcm=CLMcom-CCLM4-8-17 scen=rcp45 ensmem=r1i1p1 version=v1 > out_45_MOH_CLM_23 2> eout_45_MOH_CLM_23 &

srun -l --job-name=berg_45_3MOH_CLM $python transform_daily_netcdf_to_csv_dwd_core_ensemble.py start_y=151 end_y=220 csvs=csvs/ \
gcm=MOHC-HadGEM2-ES rcm=CLMcom-CCLM4-8-17 scen=rcp45 ensmem=r1i1p1 version=v1 > out_45_MOH_CLM_33 2> eout_45_MOH_CLM_33 &

#RCP2.6
srun -l --job-name=berg_26_1MOH_KNM $python transform_daily_netcdf_to_csv_dwd_core_ensemble.py start_y=1 end_y=80 csvs=csvs/ \
gcm=MOHC-HadGEM2-ES rcm=KNMI-RACMO22E scen=rcp26 ensmem=r1i1p1 version=v2 > out_26_MOH_KNM_13 2> eout_26_MOH_KNM_13 &

srun -l --job-name=berg_26_2MOH_KNM $python transform_daily_netcdf_to_csv_dwd_core_ensemble.py start_y=81 end_y=150 csvs=csvs/ \
gcm=MOHC-HadGEM2-ES rcm=KNMI-RACMO22E scen=rcp26 ensmem=r1i1p1 version=v2 > out_26_MOH_KNM_23 2> eout_26_MOH_KNM_23 &

srun -l --job-name=berg_26_3MOH_KNM $python transform_daily_netcdf_to_csv_dwd_core_ensemble.py start_y=151 end_y=220 csvs=csvs/ \
gcm=MOHC-HadGEM2-ES rcm=KNMI-RACMO22E scen=rcp26 ensmem=r1i1p1 version=v2 > out_26_MOH_KNM_33 2> eout_26_MOH_KNM_33 &
