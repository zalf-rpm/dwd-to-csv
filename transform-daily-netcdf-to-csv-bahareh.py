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
from datetime import date, datetime, timedelta
from collections import defaultdict
import sys

from netCDF4 import Dataset
import numpy as np
from scipy.interpolate import NearestNDInterpolator
from pyproj import Proj, Transformer

LOCAL_RUN = True

def transform_netcdfs():

    config = {
        "path_to_data": "/beegfs/common/data/climate/bahareh/",
        "path_to_output": "/beegfs/common/data/climate/dwd/cmip_cordex_reklies/csv/",
        "gcm": None,
        "rcm": None,
        "scen": None,
        "start_y": "1",
        "end_y": None,
        "start_x": "1", 
        "end_x": None, 
        "start_year": None,
        "end_year": None,
    }
    if len(sys.argv) > 1:
        for arg in sys.argv[1:]:
            kkk, vvv = arg.split("=")
            if kkk in config:
                config[kkk] = vvv
    
    elem_to_varname = {
        "tasmax": "tasmaxAdjustInterp",
        "tas": "tasAdjustInterp",
        "tasmin": "tasminAdjustInterp",
        "pr": "prAdjustInterp",
        "hurs": "hursAdjustInterp",
        "rsds": "rsdsAdjustInterp",
        "sfcWind": "sfcWindAdjustInterp"
    }

    files = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(list))))
    for d1 in os.listdir(config["path_to_data"]):
        path_1 = config["path_to_data"] + d1
        if d1.startswith("-"):
            continue

        if os.path.isdir(path_1):
            gcm, scen, _1, rcm, _v = str(d1).split("_")

            elems = set(elem_to_varname.keys())
            for d2 in os.listdir(path_1):
                path_2 = path_1 + "/" + d2
                if os.path.isdir(path_2):
                    elem = str(d2)
                    elems.remove(elem)

                    for f in os.listdir(path_2):
                        path_3 = path_2 + "/" + f
                        if os.path.isfile(path_3):
                            _var, _2, _gcm, _scen, _22, _rcm, _incl_full_time_range, _3, _4, incl_time_range = str(f).split("_")
                            starty, endy = incl_time_range[:-3].split("-")
                            start_year = int(starty[:4])
                            end_year = int(endy[:4])
                            files[gcm][rcm][scen][elem].append([start_year, end_year, path_3])
                            files[gcm][rcm][scen][elem].sort()

            if len(elems) > 0:
                print(path_1, str(elems), "missing")


    def write_files(cache, nrows, gcm, rcm, scen):
        "write files"

        no_of_files = len(cache)
        count = 0
        for (y, x), rows in cache.items():
            path_to_outdir = config["path_to_output"] + gcm + "/" + rcm + "/" + scen + "/" + "row-" + str(nrows - y - 1) + "/"
            if not os.path.isdir(path_to_outdir):
                os.makedirs(path_to_outdir)

            path_to_outfile = path_to_outdir + "col-" + str(x) + ".csv"
            if not os.path.isfile(path_to_outfile):
                with open(path_to_outfile, "w", newline="") as _:
                    writer = csv.writer(_, delimiter=",")
                    writer.writerow(["iso-date", "tmin", "tavg", "tmax", "precip", "relhumid", "globrad", "windspeed"])
                    writer.writerow(["[]", "[°C]", "[°C]", "[°C]", "[mm]", "[%]", "[MJ m-2]", "[m s-1]"])

            with open(path_to_outfile, "a", newline="") as _:
                writer = csv.writer(_, delimiter=",")
                for row in rows:
                    writer.writerow(row)

            count = count + 1
            if count % 1000 == 0:
                print(count, "/", no_of_files, "written")


    wgs84 = Proj(init="epsg:4326")
    gk5 = Proj(init="epsg:31469")
    transformer = Transformer.from_proj(wgs84, gk5) 

    def create_elem_interpolator(elem_arr, lat_arr, lon_arr, wgs84, gk5):
        "read an ascii grid into a map, without the no-data values"

        points = []
        values = []

        nrows = elem_arr.shape[0]
        ncols = elem_arr.shape[1]
        
        for row in range(nrows):
            for col in range(ncols):
                #if int(elem_arr[row, col]) == -999:
                if elem_arr.mask[row, col]:
                    continue
                lat = lat_arr[row, col]
                lon = lon_arr[row, col]
                r_gk5, h_gk5 = transformer.transform(lon, lat)
                points.append([r_gk5, h_gk5])
                values.append((row, col))
                #print "row:", row, "col:", col, "lat:", lat, "lon:", lon, "val:", values[i]
            #print row,

        return NearestNDInterpolator(points, values)


    write_rows_threshold = 1
    for gcm, rest1 in files.items():
        if config["gcm"] and gcm != config["gcm"]:
            continue

        for rcm, rest2 in rest1.items():
            if config["rcm"] and rcm != config["rcm"]:
                continue

            for scen, rest3 in rest2.items():
                if config["scen"] and scen != config["scen"]:
                    continue

                time_range_count = len(rest3["tas"])
                for time_range_index in range(time_range_count):
                    print("gcm:", gcm, "rcm:", rcm, "scen:", scen, "time_range_index:", time_range_index)
                    
                    start_years = set()
                    end_years = set()
                    #find smallest common denominator for start/end year
                    for elem, rest4 in rest3.items():
                        starty, endy, _ = rest4[time_range_index]
                        start_years.add(starty)
                        end_years.add(endy)
                    
                    start_year, end_year = (list(start_years)[-1], list(end_years)[0])
                    if config["start_year"] and start_year < int(config["start_year"]):
                        continue

                    data = {}
                    ref_elem = None
                    rsds_interpolate = None
                    datasets = []
                    #open all files for the first time range
                    for elem, rest4 in rest3.items():
                        elem_starty, elem_endy, file_path = rest4[time_range_index]

                        ds = Dataset(file_path)
                        datasets.append(ds)

                        #calculate the offset needed when copying the data to the temp arrays,
                        #because some seldom arrays start a year earlier (rsds)
                        if (start_year - elem_starty) > 0:
                            start_day_delta = (date(start_year, 1, 1) - date(elem_starty, 1, 1)).days
                        else:
                            start_day_delta = 0
                        if (elem_endy - end_year) > 0:
                            end_day_delta = (date(elem_endy, 12, 31) - date(end_year, 12, 31)).days
                        else:
                            end_day_delta = 0

                        #store the name of a reference element which has the correct shape 
                        if not ref_elem and start_day_delta == 0 and end_day_delta == 0:
                            ref_elem = elem

                        var = ds.variables[elem_to_varname[elem]]
                        
                        if end_day_delta == 0:
                            #data[elem] = np.copy(var[start_day_delta:,:,:])
                            data[elem] = var[start_day_delta:,:,:]
                        else:
                            #data[elem] = np.copy(var[start_day_delta:-end_day_delta,:,:])
                            data[elem] = var[start_day_delta:-end_day_delta,:,:]

                        if elem == "rsds":
                            #data["lat"] = np.copy(ds.variables["lat"])
                            data["lat"] = ds.variables["lat"]
                            #data["lon"] = np.copy(ds.variables["lon"])
                            data["lon"] = ds.variables["lon"]
                            rsds_interpolate = create_elem_interpolator(data["rsds"][0], data["lat"], data["lon"], wgs84, gk5)

                        #ds.close()    

                    ref_data = data[ref_elem]   
                    no_of_days = ref_data.shape[0]
                    nrows = ref_data.shape[1]
                    ncols = ref_data.shape[2]

                    cache = defaultdict(list)
                    for y in range(int(config["start_y"]) - 1, int(config["end_y"]) if config["end_y"] else nrows):
                        #print "y: ", y, "->"
                        start_time_y = time.clock()
                        #print(y, end=" ", flush=True)
                        
                        #for x in range(ncols): #ref_data.shape[2]):
                        for x in range(int(config["start_x"]) - 1, int(config["end_x"]) if config["end_x"] else ncols):
                            #print(x, end=" ", flush=True)
                        
                            #if int(ref_data[0, y, x]) == -999:
                            if ref_data.mask[0, y, x]:
                                continue

                            # for some reason the rsds data don't fit exactly to the other 6 variables,
                            # but the datacells have the same lat/lon, so if a valid ref_data cell has 
                            # no data in an rsds data cell, we choose the closest rsds cell
                            #interpol_rsds = int(data["rsds"][0, y, x]) == -999
                            interpol_rsds = data["rsds"].mask[0, y, x]
                            if interpol_rsds:
                                lat = data["lat"][y, x]
                                lon = data["lon"][y, x]
                                r_gk5, h_gk5 = transformer.transform(lon, lat)
                                closest_row, closest_col = rsds_interpolate(r_gk5, h_gk5)
                            
                            for i in range(no_of_days):
                                if interpol_rsds:
                                    rsds = data["rsds"][i, closest_row, closest_col]
                                else:
                                    rsds = data["rsds"][i, y, x]
                                pr = round(data["pr"][i, y, x] * 60*60*24, 1)
                                if pr > 100:
                                    print("gcm:", gcm, "rcm:", rcm, "scen:", scen, "tri:", time_range_index, "y:", y, "x:", x, "pr:", pr, flush=True)
                                row = [
                                    (date(start_year, 1, 1)+timedelta(days=i)).strftime("%Y-%m-%d"),
                                    str(round(data["tasmin"][i, y, x] - 273.15, 2)),
                                    str(round(data["tas"][i, y, x] - 273.15, 2)),
                                    str(round(data["tasmax"][i, y, x] - 273.15, 2)),
                                    str(pr),
                                    str(round(data["hurs"][i, y, x], 1)),
                                    str(round(rsds * 60 * 60 * 24 / 1000000, 4)),
                                    str(round(data["sfcWind"][i, y, x], 1))
                                ]
                                cache[(y,x)].append(row)
                        
                        end_time_y = time.clock()
                        print(y, "|" + str(int(end_time_y - start_time_y)) + "s", sep="", flush=True, end=" ")
                    
                        if y > int(config["start_y"]) and y % write_rows_threshold == 0:
                            print()
                            s = time.clock()
                            write_files(cache, nrows, gcm, rcm, scen)
                            cache = defaultdict(list)
                            e = time.clock()
                            print("wrote", write_rows_threshold, "ys in", (e-s), "seconds")

                    print()

                    #write remaining cache items
                    write_files(cache, nrows, gcm, rcm, scen)

                    for ds in datasets:
                        ds.close()


if __name__ == "__main__":
    transform_netcdfs()