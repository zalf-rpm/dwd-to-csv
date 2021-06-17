#!/bin/bash

python=~/.conda/envs/py38/bin/python

#historical
#srun -l --job-name=berg_3hist_CCC_CLM $python transform_daily_netcdf_to_csv_dwd_core_ensemble.py csvs=csvs/ \
#gcm=CCCma-CanESM2 rcm=CLMcom-CCLM4-8-17 scen=historical ensmem=r1i1p1 version=v1 > out_hist_CCC_CLM_3 2> eout_hist_CCC_CLM_3 &

srun -l --job-name=berg_4hist_MIR_CLM $python transform_daily_netcdf_to_csv_dwd_core_ensemble.py csvs=csvs/ \
gcm=MIROC-MIROC5 rcm=CLMcom-CCLM4-8-17 scen=historical ensmem=r1i1p1 version=v1 > out_hist_MIR_CLM_4 2> eout_hist_MIR_CLM_4 &

#RCP8.5
#srun -l --job-name=berg_385_CCC_CLM $python transform_daily_netcdf_to_csv_dwd_core_ensemble.py start_y=1 end_y=80 csvs=csvs/ \
#gcm=CCCma-CanESM2 rcm=CLMcom-CCLM4-8-17 scen=rcp85 ensmem=r1i1p1 version=v1 > out_85_CCC_CLM_13 2> eout_85_CCC_CLM_13 &

#srun -l --job-name=berg_385_CCC_CLM $python transform_daily_netcdf_to_csv_dwd_core_ensemble.py start_y=81 end_y=150 csvs=csvs/ \
#gcm=CCCma-CanESM2 rcm=CLMcom-CCLM4-8-17 scen=rcp85 ensmem=r1i1p1 version=v1 > out_85_CCC_CLM_23 2> eout_85_CCC_CLM_23 &

#srun -l --job-name=berg_385_CCC_CLM $python transform_daily_netcdf_to_csv_dwd_core_ensemble.py start_y=151 end_y=220 csvs=csvs/ \
#gcm=CCCma-CanESM2 rcm=CLMcom-CCLM4-8-17 scen=rcp85 ensmem=r1i1p1 version=v1 > out_85_CCC_CLM_33 2> eout_85_CCC_CLM_33 &


#RCP2.6
#srun -l --job-name=berg_426_MIR_CLM $python transform_daily_netcdf_to_csv_dwd_core_ensemble.py start_y=1 end_y=80 csvs=csvs/ \
#gcm=MIROC-MIROC5 rcm=CLMcom-CCLM4-8-17 scen=rcp26 ensmem=r1i1p1 version=v1 > out_26_MIR_CLM_14 2> eout_26_MIR_CLM_14 &

#srun -l --job-name=berg_426_MIR_CLM $python transform_daily_netcdf_to_csv_dwd_core_ensemble.py start_y=81 end_y=150 csvs=csvs/ \
#gcm=MIROC-MIROC5 rcm=CLMcom-CCLM4-8-17 scen=rcp26 ensmem=r1i1p1 version=v1 > out_26_MIR_CLM_24 2> eout_26_MIR_CLM_24 &

#srun -l --job-name=berg_426_MIR_CLM $python transform_daily_netcdf_to_csv_dwd_core_ensemble.py start_y=151 end_y=220 csvs=csvs/ \
#gcm=MIROC-MIROC5 rcm=CLMcom-CCLM4-8-17 scen=rcp26 ensmem=r1i1p1 version=v1 > out_26_MIR_CLM_34 2> eout_26_MIR_CLM_34 &
