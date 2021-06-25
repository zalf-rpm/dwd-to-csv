#!/usr/bin/python
# -*- coding: UTF-8

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/. */

# Authors:
# Michael Berg-Mohnicke <michael.berg@zalf.de>
#
# Maintainers:
# Currently maintained by the authors.
#
# This file has been created at the Institute of
# Landscape Systems Analysis at the ZALF.
# Copyright (C: Leibniz Centre for Agricultural Landscape Research (ZALF)

import time
import os
import math
import json
import csv
import itertools
#import copy
from datetime import date, datetime, timedelta
from collections import defaultdict, OrderedDict
#import types
import sys

from netCDF4 import Dataset
import numpy as np

def main():

    config = {
        "path-to-dataset": "/beegfs/common/data/climate/dwd_core_ensemble/download/ICHEC-EC-EARTH_historical_r1i1p1_KNMI-RACMO22E_v1/tas/tasAdjustInterp_HYR-5_ICHEC-EC-EARTH_historical_r1i1p1_KNMI-RACMO22E_v1-DWD-MMBC-v1-HYRAS-v3-0-1951-2005_DWD-PCA-v1_day_19510101-19541231.nc"
    }
    if len(sys.argv) > 1:
        for arg in sys.argv[1:]:
            kkk, vvv = arg.split("=")
            if kkk in config:
                config[kkk] = vvv

    ds = Dataset(config["path-to-dataset"])
    lats = ds.variables["lat"]
    lons = ds.variables["lon"]
    tavg = ds.variables["tasAdjustInterp"][0]

    lat_lon_grid_file = open("lat-lon.grid", "w")
    data_no_data_grid_file = open("data-no-data.grid", "w")
    latlon_to_rowcol_json_file = open("latlon-to-rowcol.json", "w")
    rowcol_to_latlon_json_file = open("rowcol-to-latlon.json", "w")

    ncols = 240
    nrows = 220
    lat_lon_grid_file.write("ncols "+str(ncols)+"\nnrows "+str(nrows)+"\nnodata_value ---------------\n")
    data_no_data_grid_file.write("ncols "+str(ncols)+"\nnrows "+str(nrows)+"\nnodata_value -\n")
    ll_to_rc_json_data = []
    rc_to_ll_json_data = []

    for row in range(0, nrows):
        ll_line = []
        dnd_line = []
        for col in range(0, ncols):
            lat = round(float(lats[nrows-1-row, col]), 4)
            lon = round(float(lons[nrows-1-row, col]), 4)
            
            is_data = not tavg.mask[nrows-1-row, col]
            dnd_line.append("x" if is_data else "-")
            if is_data:
                ll_to_rc_json_data.append([[lat, lon], [row, col]])
                rc_to_ll_json_data.append([[row, col], [lat, lon]])
                ll_line.append("{:07.4f}|{:07.4f}".format(lat, lon))
            else:
                ll_line.append("---------------")

        lat_lon_grid_file.write(" ".join(ll_line))
        data_no_data_grid_file.write(" ".join(dnd_line))
        if row < nrows-1:
            lat_lon_grid_file.write("\n")
            data_no_data_grid_file.write("\n")

        if row % 10 == 0:
            print("wrote line", row)
    
    json.dump(ll_to_rc_json_data, latlon_to_rowcol_json_file)#, indent=2)
    json.dump(rc_to_ll_json_data, rowcol_to_latlon_json_file)#, indent=2)

    lat_lon_grid_file.close()
    data_no_data_grid_file.close()
    latlon_to_rowcol_json_file.close()
    rowcol_to_latlon_json_file.close()
    ds.close()


main()
