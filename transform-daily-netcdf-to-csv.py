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
from StringIO import StringIO
from datetime import date, datetime, timedelta
from collections import defaultdict, OrderedDict
#import types
import sys
print sys.path
#import zmq
#print "pyzmq version: ", zmq.pyzmq_version(), " zmq version: ", zmq.zmq_version()

from netCDF4 import Dataset
import numpy as np
from scipy.interpolate import NearestNDInterpolator
from pyproj import Proj, transform

LOCAL_RUN = True

def main():

    config = {
        "path_to_data": "A:/data/climate/dwd/grids/germany/daily/" if LOCAL_RUN else "/archiv-daten/md/data/climate/dwd/grids/germany/daily/",
        #"path_to_output": "m:/data/climate/dwd/csvs/germany/" if LOCAL_RUN else "/archiv-daten/md/data/climate/dwd/csvs/germany/",
        "path_to_output": "out/" if LOCAL_RUN else "/archiv-daten/md/data/climate/dwd/csvs/germany/",
        "start-y": "1",
        "end-y": "-1",
        "start-x": "1", 
        "end-x": "132", 
        "start-year": "1995",
        "start-month": "1",
        "end-year": "2012",
        "end-month": "12"
    }
    if len(sys.argv) > 1:
        for arg in sys.argv[1:]:
            kkk, vvv = arg.split("=")
            if kkk in config:
                config[kkk] = vvv

    reg_nrows = 971
    reg_ncols = 611

    nrows = 938
    ncols = 720

    def read_daily_regnie_ascii_grid(path_to_file):
        "read an ascii grid into a map, without the no-data values"
        with open(path_to_file) as file_:
            data = np.empty((971, 611), dtype=np.int16)
            for y in range(971):
                for x in range(611):
                    data[y, x] = int(file_.read(4))
                file_.read(1)
            return data

    def create_regnie_interpolator(regnie_template, nrows, ncols, wgs84, gk5):
        "read an ascii grid into a map, without the no-data values"

        ydelta_grad = 1.0 / 120.0
        xdelta_grad = 1.0 / 60.0

        points = []
        values = []

        for row in xrange(0, nrows):
            lat = (55.0 + 10.0 * ydelta_grad) - row * ydelta_grad
            for col in xrange(0, ncols):
                if regnie_template[row, col] == -999:
                    continue
                lon = (6.0 - 10.0 * xdelta_grad) + col * xdelta_grad
                r_gk5, h_gk5 = transform(wgs84, gk5, lon, lat)
                points.append([r_gk5, h_gk5])
                values.append((row, col))
                #print "row:", row, "col:", col, "lat:", lat, "lon:", lon, "val:", values[i]
            #print row,

        return NearestNDInterpolator(points, values)

    wgs84 = Proj(init="epsg:4326")
    #gk3 = Proj(init="epsg:31467")
    gk5 = Proj(init="epsg:31469")
    regnie_template = read_daily_regnie_ascii_grid(config["path_to_data"] + "../daily-regnie/ra1995m/ra950101")
    regnie_gk5_interpolate = create_regnie_interpolator(regnie_template, reg_nrows, reg_ncols, wgs84, gk5)

    files = defaultdict(lambda: defaultdict(lambda: defaultdict(dict)))
    for f in os.listdir(config["path_to_data"]):
        elem, year_month, _ = str(f).split("_")
        year = int(year_month[:4])
        month = int(year_month[4:])
        files[year][month][elem] = config["path_to_data"] + f

    elem_to_varname = {
        "tmin": "temperature",
        "tavg": "temperature",
        "tmax": "temperature",
        "precip": "precipitation",
        "RH": "humidity",
        "SIS": "SIS",
        "FF": "FF"
    }

    def write_files(cache, nrows):
        "write files"

        no_of_files = len(cache)
        count = 0
        for (y, x), rows in cache.iteritems():
            path_to_outdir = config["path_to_output"] + "row-" + str(nrows - y - 1) + "/"
            if not os.path.isdir(path_to_outdir):
                os.makedirs(path_to_outdir)

            path_to_outfile = path_to_outdir + "col-" + str(x) + ".csv"
            if not os.path.isfile(path_to_outfile):
                with open(path_to_outfile, "wb") as _:
                    writer = csv.writer(_, delimiter=",")
                    writer.writerow(["iso-date", "tmin", "tavg", "tmax", "precip", "relhumid", "globrad", "windspeed"])
                    writer.writerow(["[]", "[°C]", "[°C]", "[°C]", "[mm]", "[%]", "[MJ m-2]", "[m s-1]"])

            with open(path_to_outfile, "ab") as _:
                writer = csv.writer(_, delimiter=",")
                for row in rows:
                    writer.writerow(row)

            count = count + 1
            if count % 1000 == 0:
                print count, "/", no_of_files, "written"

    
    write_files_threshold = 50 #ys
    for year, months in files.iteritems():
        if year < int(config["start-year"]):
            continue
        if year > int(config["end-year"]):
            break

        #print "year: ", year, "months: ",
        for month, elems in months.iteritems():
            if year == int(config["start-year"]) and month < int(config["start-month"]):
                continue
            if year == int(config["end-year"]) and month > int(config["end-month"]):
                break

            print "year:", year, "month:", month, "ys ->",
            data = {}
            lat_lon_once = False
            for elem, filepath in elems.iteritems():
                ds = Dataset(filepath)
                data[elem] = np.copy(ds.variables[elem_to_varname[elem]])
                if not lat_lon_once:
                    data["lat"] = np.copy(ds.variables["lat"])
                    data["lon"] = np.copy(ds.variables["lon"])
                    lat_lon_once = True
                ds.close()

            ref_data = data["tavg"]
            #no_of_days = len(ref_data.variables["time"])
            no_of_days = ref_data.shape[0]

            start_month = time.clock()
            cache = defaultdict(list)

            #open and read regnie grids for current month, but we do it lazily
            regnie_np_grids = []
            for day in range(1, no_of_days + 1):
                filename = "{}../daily-regnie/ra{}m/ra{}{:02d}{:02d}".format(config["path_to_data"], year, str(year)[2:4], month, day)
                regnie_np_grids.append(read_daily_regnie_ascii_grid(filename))

            #ref_data.shape[1]
            for y in range(int(config["start-y"]) - 1, nrows if int(config["end-y"]) < 0 else int(config["end-y"])):
                #print "y: ", y, "->"
                start_y = time.clock()
                #print y,

                #for x in range(ncols): #ref_data.shape[2]):
                for x in range(int(config["start-x"]) - 1, ncols if int(config["end-x"]) < 0 else int(config["end-x"])):
                    #print x,
                   
                    if int(ref_data[0, y, x]) == 9999:
                        continue

                    lat = data["lat"][y, x]
                    lon = data["lon"][y, x]

                    r_gk5, h_gk5 = transform(wgs84, gk5, lon, lat)
                    rrow, rcol = regnie_gk5_interpolate(r_gk5, h_gk5)

                    for i in range(no_of_days):
                        row = [
                            date(year, month, i+1).strftime("%Y-%m-%d"),
                            str(data["tmin"][i, y, x]),
                            str(data["tavg"][i, y, x]),
                            str(data["tmax"][i, y, x]),
                            #str(data["precip"][i, y, x]),
                            str(regnie_np_grids[i][rrow, rcol] / 10.0),
                            str(data["RH"][i, y, x]),
                            str(round(data["SIS"][i, y, x] * 60 * 60 * 24 / 1000000, 4)),
                            str(data["FF"][i, y, x])
                        ]
                        cache[(y,x)].append(row)
                
                end_y = time.clock()
                print y, #str(y) + "|" + str(int(end_y - start_y)) + "s ",
               
                if y > int(config["start-y"]) and y % write_files_threshold == 0:
                    print ""
                    s = time.clock()
                    write_files(cache, nrows)
                    cache = defaultdict(list)
                    e = time.clock()
                    print "wrote", write_files_threshold, "ys in", (e-s), "seconds"

            #for dataset in data.values():
            #    dataset.close()
            print ""

            #write remaining cache items
            write_files(cache, nrows)

            end_month = time.clock()
            print "running month", month, "took", (end_month - start_month), "seconds"

main()