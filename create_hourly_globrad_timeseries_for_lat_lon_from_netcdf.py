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
from StringIO import StringIO
from datetime import date, datetime, timedelta
from collections import defaultdict
import sys
print sys.path

from netCDF4 import Dataset
import netCDF4
import numpy as np
import gzip
from pyproj import Proj, transform

def main():

    config = {
        "path_to_data": "A:/data/climate/dwd/grids/germany/", #hourly/",
        "path_to_output": "A:/data/climate/dwd/grids/germany/"
    }
    if len(sys.argv) > 1:
        for arg in sys.argv[1:]:
            k, v = arg.split("=")
            if k in config:
                config[k] = v

    path_to_data = config["path_to_data"]
    path_to_output = config["path_to_output"]
    path_to_outfile = path_to_output + "globrad_at_lat_53.1685_lon_12.9793.csv"

    #wgs84 = Proj(init="epsg:4326")
    #gk3 = Proj(init="epsg:31467")
    #gk5 = Proj(init="epsg:31469")
    #lat = 53.16305556
    #lon = 12.98833333
    #r_gk3, h_gk3 = transform(wgs84, gk3, lon, lat)
    #return

    #with gzip.open(path_to_data + "SIS_199501.nc.gz") as gz:
    #    with netCDF4.Dataset('dummy', mode='r', memory=gz.read()) as nc:
    #        print(nc.variables)
    #return

    x = 522 #lon = 12.9793
    y = 687 #lat = 53.1685

    files = os.listdir(path_to_data) #["SIS_199501.nc.gz"] #os.listdir(path_to_data)
    files.sort()
    for f in files: #[config["start"]-1:config["end"]]:

        print f
        with gzip.open(path_to_data + f) as gz:
            with netCDF4.Dataset('dummy', mode='r', memory=gz.read()) as nc:

                len_time = len(nc.variables["time"])

                rows = []
                for i in xrange(len_time):
                    rows.append([
                        datetime.strptime(str(nc.variables["datum"][i])[:10], "%Y%m%d%H").strftime("%Y-%m-%d %H:00"), 
                        float(nc.variables["SIS"][i, y, x]),
                        round(float(nc.variables["SIS"][i, y, x]*0.0036), 5)
                    ])

                if not os.path.isfile(path_to_outfile):
                    with open(path_to_outfile, "wb") as _:
                        writer = csv.writer(_, delimiter=",")
                        writer.writerow(["iso-date", "globrad", "globrad"])
                        writer.writerow(["[]", "[Wh m-2]", "[MJ m-2]"])

                with open(path_to_outfile, "ab") as _:
                    writer = csv.writer(_, delimiter=",")
                    for row in rows:
                        writer.writerow(row)

                #print(nc.variables)


main()