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
#import copy
from StringIO import StringIO
from datetime import date, datetime, timedelta
from collections import defaultdict
#import types
import sys
print sys.path
#import zmq
#print "pyzmq version: ", zmq.pyzmq_version(), " zmq version: ", zmq.zmq_version()

from netCDF4 import Dataset
import numpy as np

def main():

    config = {
        "path_to_data": "m:/data/climate/dwd/grids/germany/hourly/",
        "path_to_output": "m:/data/climate/dwd/grids/germany/hourly-aggregated-to-daily/",
        "start": 1,
        "end": 218
    }
    if len(sys.argv) > 1:
        for arg in sys.argv[1:]:
            kkk, vvv = arg.split("=")
            if kkk in config:
                config[kkk] = int(vvv)

    path_to_data = config["path_to_data"]
    path_to_output = config["path_to_output"]

    files = os.listdir(path_to_data)
    files.sort()
    for f in files[config["start"]-1:config["end"]]:
        hourly_grp = Dataset(path_to_data + f)
        len_time = len(hourly_grp.variables["time"])

        #print hourly_grp
        #print [v for v in hourly_grp.variables.values()]

        daily_grps = {
            "tmin": Dataset(path_to_output + "tmin/" + f, "w"),
            "tmax": Dataset(path_to_output + "tmax/" + f, "w"),
            "tavg": Dataset(path_to_output + "tavg/" + f, "w")
        }

        for grp in daily_grps.values():
            grp.createDimension("x", 720)
            grp.createDimension("y", 938)
            grp.createDimension("time", None)

            grp.createVariable("lon", "f8", ("y", "x"), fill_value=9999.0)
            grp.variables["lon"][:,:] = hourly_grp.variables["lon"][:,:]
            
            grp.createVariable("lat", "f8", ("y", "x"), fill_value=9999.0)
            grp.variables["lat"][:,:] = hourly_grp.variables["lat"][:,:]
            
            grp.createVariable("time", "i4", ("time"))
            grp.variables["time"][:] = np.arange(len_time // 24)
            
            grp.createVariable("temperature", "i2", ("time", "y", "x"), fill_value=9999)
            grp.variables["temperature"].scale_factor = 0.1

        temp = hourly_grp.variables["temperature"]

        for i in range(0, len_time, 24):
            #temp_min0 = min(temp[i:i+24, 500, 300])
            #temp_max0 = max(temp[i:i+24, 500, 300])
            #temp_sum0 = sum(temp[i:i+24, 500, 300])
            temp_sum = sum(temp[i:i+24])
            temp_min = reduce(np.minimum, temp[i:i+24])
            temp_max = reduce(np.maximum, temp[i:i+24])
            temp_avg = temp_sum / 24.0
            daily_grps["tmin"].variables["temperature"][i // 24,:,:] = temp_min
            daily_grps["tmax"].variables["temperature"][i // 24,:,:] = temp_max
            daily_grps["tavg"].variables["temperature"][i // 24,:,:] = temp_avg
            print "day: ", (i//24), "of file: ", f


        hourly_grp.close()
        for grp in daily_grps.values():
            grp.close()


main()