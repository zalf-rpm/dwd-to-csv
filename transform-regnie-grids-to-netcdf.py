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

#pylint: disable=C0103

#%%
import time
import os
import math
import json
import pickle
import csv
import itertools
#import copy
from StringIO import StringIO
from datetime import date, datetime, timedelta
import calendar
from collections import defaultdict, OrderedDict
#import types
import sys
print sys.path
#import zmq
#print "pyzmq version: ", zmq.pyzmq_version(), " zmq version: ", zmq.zmq_version()

from netCDF4 import Dataset
import numpy as np

#%%
def create_regnie_dicts():
    "create a nested ordered dicts which map regnie lat/lon coordinates to y/x coordinates"
    ydelta_grad = 1.0 / 120.0
    xdelta_grad = 1.0 / 60.0
    regnie_lat_lon = defaultdict(dict)
    for y in range(1, 971 + 1):
        lat = (55.0 + 10.0 * ydelta_grad) - (y - 1) * ydelta_grad
        for x in range(1, 611 + 1):
            lon = (6.0 - 10.0 * xdelta_grad) + (x - 1) * xdelta_grad
            regnie_lat_lon[lat][lon] = (y - 1, x - 1)
    return regnie_lat_lon

#%%
def convert_regnie_pixel_to_geographic_coordinates(cartesian_point_regnie): # y, x
    " Berechnungsfunktion"
    xdelta_grad = 1.0 /  60.0
    ydelta_grad = 1.0 / 120.0
    lat = (55.0 + 10.0 * ydelta_grad) - (cartesian_point_regnie[0] - 1) * ydelta_grad
    lon = ( 6.0 - 10.0 * xdelta_grad) + (cartesian_point_regnie[1] - 1) * xdelta_grad
    return lat, lon

#%%
def read_daily_regnie_ascii_grid(path_to_file):
    "read an ascii grid into a map, without the no-data values"
    with open(path_to_file) as file_:
        data = {}
        for y in range(971):
            for x in range(611):
                val = int(file_.read(4))
                if val < 0:
                    continue
                data[(y, x)] = val / 10.0
            file_.read(1)
        return data


#%%
def main():

    #%%
    config = {
        "path_to_data": "m:/data/climate/dwd/grids/germany/daily/",
        "path_to_output": "m:/data/climate/dwd/csvs/germany/daily-regnie/",
        "start-year": 1995,
        "end-year": 2012,
        "start-month": 1,
        "end-month": 12
    }

    #%%
    if len(sys.argv) > 1:
        for arg in sys.argv[1:]:
            kkk, vvv = arg.split("=")
            if kkk in config:
                config[kkk] = int(vvv)

    #%%
    path_to_data = config["path_to_data"]
    path_to_output = config["path_to_output"]

    #%%
    ref_data = Dataset(path_to_data + "tavg_199501_daymean.nc")
    #no_of_days = len(ref_data.variables["time"])

    #%%
    # first create a mapping of regnie cells to netcdf cells based on lat/lon proximity
    nc_to_regnie = {}
    with open("nc_to_regnie_1-938.pickle") as _:
        nc_to_regnie = pickle.load(_)

    #%%
    len_ys = len(ref_data.dimensions["y"])
    len_xs = len(ref_data.dimensions["x"])

    for year in range(config["start-year"], config["end-year"]+1):
        for month in range(config["start-month"], config["end-month"]+1):

            days_in_month = calendar.monthrange(year, month)[1]
            path_to_file = path_to_data + "../daily-precip3/precip_" + date(year, month, 1).strftime("%Y%m") + "_daymean.nc"
            #path_to_file = "out/precip_" + date(year, month, 1).strftime("%Y%m") + "_daymean.nc"

            daily = Dataset(path_to_file, "w")

            daily.createDimension("x", 720)
            daily.createDimension("y", 938)
            daily.createDimension("time", None)

            daily.createVariable("lon", "f8", ("y", "x"), fill_value=9999.0)
            daily.variables["lon"][:, :] = ref_data.variables["lon"][:, :]

            daily.createVariable("lat", "f8", ("y", "x"), fill_value=9999.0)
            daily.variables["lat"][:, :] = ref_data.variables["lat"][:, :]

            daily.createVariable("time", "i4", ("time"))
            daily.variables["time"][:] = np.arange(days_in_month)

            daily.createVariable("precipitation", "i2", ("time", "y", "x"), fill_value=9999)
            daily.variables["precipitation"].scale_factor = 0.1

            nc = daily.variables["precipitation"]

            for day in range(days_in_month):
                path_to_regniefile = path_to_data + "../daily-regnie/ra" + str(year) + "m/ra" + date(year, month, day+1).strftime("%y%m%d")
                regnie_ascii = read_daily_regnie_ascii_grid(path_to_regniefile)

                #path_to_file = "out/precip_" + date(year, month, day+1).strftime("%Y%m%d") + ".nc"
                #daily = Dataset(path_to_file, "w")

                #daily.createDimension("x", 720)
                #daily.createDimension("y", 938)

                #daily.createVariable("lon", "f8", ("y", "x"), fill_value=9999.0)
                #daily.variables["lon"][:, :] = ref_data.variables["lon"][:, :]

                #daily.createVariable("lat", "f8", ("y", "x"), fill_value=9999.0)
                #daily.variables["lat"][:, :] = ref_data.variables["lat"][:, :]

                #daily.createVariable("precipitation", "i2", ("y", "x"), fill_value=9999)
                #daily.variables["precipitation"].scale_factor = 0.1

                #nc_day = daily.variables["precipitation"]

                for y in range(len_ys):
                    for x in range(len_xs):

                        #lat = ref_data.variables["lat"][y, x]
                        #lon = ref_data.variables["lon"][y, x]
                        reg_coord = nc_to_regnie[(y, x)]
                        if not reg_coord or reg_coord not in regnie_ascii:
                            nc[day, y, x] = 9999
                            #print "nc(", y, "/", x, "): None"
                            continue

                        reg_val = regnie_ascii[(reg_coord)]
                        nc[day, y, x] = reg_val
                        #print "nc(", y, "/", x, "): ", reg_val

                    print date(year, month, day+1), " nc.y: ", y, " done"

                #daily.close()

            daily.close()

    ref_data.close()

main()


def main_write_nc_to_regnie():

    config = {
        "path_to_data": "m:/data/climate/dwd/grids/germany/daily/",
        "path_to_output": "m:/data/climate/dwd/csvs/germany/",
        "start": 1,
        "end": 938
    }
    if len(sys.argv) > 1:
        for arg in sys.argv[1:]:
            kkk, vvv = arg.split("=")
            if kkk in config:
                config[kkk] = int(vvv)

    path_to_data = config["path_to_data"]
    path_to_output = config["path_to_output"]


    def find_closest_value(ord_dict, val, obey_borders=True):
        "find the closest key to value val in ordered dict ord_dict"
        if obey_borders:
            vals = ord_dict.keys()
            if val < vals[0] or vals[-1] < val:
                return None

        it1 = ord_dict.iterkeys()
        it2 = ord_dict.iterkeys()
        next(it2, None)

        for (cur, nex) in itertools.izip_longest(it1, it2, fillvalue=None):
            if cur and not nex:
                return cur
            elif cur <= val and nex and val <= nex:
                cur_dist = val - cur
                nex_dist = nex - val
                return cur if cur_dist <= nex_dist else nex

        return None


    def find_closest_lat_lon(regdic, lat, lon):
        "find the (row, col) of the closest lat/lon value in dictionary regdic"
        closest_lat = find_closest_value(regdic, lat)
        if closest_lat:
            lons = regdic[closest_lat]
            closest_lon = find_closest_value(lons, lon)
            if closest_lon:
                return lons[closest_lon]

        return (None, None)


    ref_data = Dataset(path_to_data + "tavg_199501_daymean.nc")
    #no_of_days = len(ref_data.variables["time"])

    regnie_lat_lon = OrderedDict()
    regnie_lat_lon_unsorted = create_regnie_dicts()
    for lat in sorted(regnie_lat_lon_unsorted.keys()):
        regnie_lat_lon[lat] = OrderedDict()
        ulons = regnie_lat_lon_unsorted[lat]
        lons = regnie_lat_lon[lat]
        for lon in sorted(ulons.keys()):
            lons[lon] = regnie_lat_lon_unsorted[lat][lon]

    # first create a mapping of regnie cells to netcdf cells based on lat/lon proximity
    nc_to_regnie = {}
    #len_ys = len(ref_data.dimensions["y"])
    len_xs = len(ref_data.dimensions["x"])

    yc = 1
    for y in range(config["start"]-1, config["end"]):
        for x in range(len_xs):

            lat = ref_data.variables["lat"][y, x]
            lon = ref_data.variables["lon"][y, x]
            reg_y, reg_x = find_closest_lat_lon(regnie_lat_lon, lat, lon)
            nc_to_regnie[(y,x)] = (reg_y, reg_x) if reg_y and reg_x else None

        print yc, " of ", (config["end"] - config["start"] + 1), " done"
        yc = yc + 1


    with open("out/nc_to_regnie_" + str(config["start"]) + "-" + str(config["end"]) + ".pickle", "w") as _:
        pickle.dump(nc_to_regnie, _)

    ref_data.close()
    return

#main_write_nc_to_regnie()