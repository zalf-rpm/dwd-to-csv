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

from collections import defaultdict
import csv
from datetime import date, datetime, timedelta
import json
import math
import numpy as np
import os
import sys
import time

#remote debugging via commandline
#-m ptvsd --host 0.0.0.0 --port 14000 --wait

def main():

    monica_csv = False

    config = {
        #"path_to_dwd_data": "/beegfs/common/data/climate/dwd/csvs/germany",
        "path_to_dwd_data": "/beegfs/common/data/climate/dwd/csvs/germany_ubn_1901-2018_unzipped",
        #"path_to_dwd_data": "C:/Users/berg.ZALF-AD/Downloads",
        "path_to_append_data": "/beegfs/common/data/climate/dwd/grids/agrar_nachlieferung_y_2018_2019",
        #"path_to_append_data": "C:/Users/berg.ZALF-AD/Downloads/agrar_nachlieferung_y_2018_2019",
        "start_row": "1",
        "end_row": "1", #None,
        "start_col": "1", 
        "end_col": None, 
        "start_year": "2019",
        "start_day": "1",
        "end_year": "2019",
        "end_day": None
    }
    if len(sys.argv) > 1:
        for arg in sys.argv[1:]:
            kkk, vvv = arg.split("=")
            if kkk in config:
                config[kkk] = vvv
    print("config:", config)


    elems = {
        "tmin": {"folder": "D_TMIN", "pattern": "raster_out_D_TMIN_{year}__VAR03_0{:03d}.txt"},
        "tmax": {"folder": "D_TMAX", "pattern": "raster_out_D_TMAX_{year}__VAR03_0{:03d}.txt"},
        "precip": {"folder": "D_RRSUM", "pattern": "raster_out_D_RRSUM_{year}__VAR03_0{:03d}.txt"},
        "relhumid": {"folder": "D_RFMIT", "pattern": "raster_out_D_RFMIT_{year}__VAR03_0{:03d}.txt"},
        "wind": {"folder": "D_WINDMIT", "pattern": "raster_out_D_WINDMIT_{year}__VAR03_0{:03d}.txt"},
        "globrad": {"folder": "RGMIT", "pattern": "raster_out_RGMIT_{year}__VAR03_0{:03d}.txt"},
        #"precip": {"folder": "RADOLANSUM", "pattern": "raster_out_RADOLANSUM_{year}__VAR03_0{:03d}.txt"}
    }

    ncols = 654
    nrows = 866
    
    for year in range(int(config["start_year"]), int(config["end_year"]) + 1):

        cache = defaultdict(list)

        days_in_year = date(year, 12, 31).timetuple().tm_yday

        for day in range(1, days_in_year + 1):

            if day < int(config["start_day"]):
                continue
            if config["end_day"] and day > int(config["end_day"]):
                break

            current_date = date(year, 1, 1) + timedelta(days=day-1)

            elem_grids = {}
            for elem, meta in elems.items():
                path_to_file = config["path_to_append_data"] + "/" + meta["folder"] + "/" + meta["pattern"].format(day, year=year)
                elem_grids[elem] = np.loadtxt(path_to_file, dtype=int, skiprows=6)
            print("loaded files for year:", year, "day:", day, flush=True)

            ref_grid = elem_grids["tmin"]
                        
            for row in range(nrows):

                if row+1 < int(config["start_row"]):
                    continue
                if config["end_row"] and row + 1 > int(config["end_row"]):
                    break

                for col in range(ncols):

                    if col+1 < int(config["start_col"]):
                        continue
                    if config["end_col"] and col + 1 > int(config["end_col"]):
                        break

                    if ref_grid[row, col] == -9999:
                        continue

                    tmin = elem_grids["tmin"][row, col] / 10.0
                    tmax = elem_grids["tmax"][row, col] / 10.0

                    if monica_csv:
                        line = [
                            current_date.strftime("%Y-%m-%d"),
                            str(round(tmin, 1)),
                            str(round((tmin + tmax) / 2.0, 1)),
                            str(round(tmax, 1)),
                            str(round(elem_grids["precip"][row, col] / 10.0, 1)),
                            str(round(elem_grids["relhumid"][row, col] / 10.0, 1)),
                            str(round(elem_grids["globrad"][row, col] / 100.0, 2)),
                            str(round(elem_grids["wind"][row, col] / 10.0, 1))
                        ]
                    else:
                        line = [
                            current_date.strftime("%Y-%m-%d"),
                            str(round(elem_grids["precip"][row, col] / 10.0, 1)),
                            str(round(tmin, 1)),
                            str(round((tmin + tmax) / 2.0, 1)),
                            str(round(tmax, 1)),
                            str(int(elem_grids["globrad"][row, col] / 100.0 * 1000.0)),
                            str(round(elem_grids["wind"][row, col] / 10.0, 1)),
                            str(-99.9),
                            "C_{}:R_{}".format(col, row), 
                            str(round(elem_grids["relhumid"][row, col] / 10.0 / 100.0, 2)),
                        ]

                    cache[(row, col)].append(line)

        count = 0
        for (row, col), data in cache.items():
            print("writing row/col:", row, "/", col, " count:", count, flush=True)
            count += 1
            with open(config["path_to_dwd_data"] + "/row-" + str(row) + "/col-" + str(col) + ".csv", "a", newline="") as _:
                writer = csv.writer(_, delimiter=("," if monica_csv else "\t"))
                for line in data:
                    writer.writerow(line)
    

main()