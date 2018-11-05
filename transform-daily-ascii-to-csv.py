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

import numpy as np
from pyproj import Proj, transform

def ascii_to_csv():

    config = {
        "path_to_data": "Daily/",
        "path_to_output": "out/",
        "start_y": "1",
        "end_y": "50",
        "start_x": "1", 
        "end_x": "-1", 
        "start_year": "1990",
        "start_doy": "1",
        "end_year": "2017",
        "end_doy": "366"
    }
    if len(sys.argv) > 1:
        for arg in sys.argv[1:]:
            kkk, vvv = arg.split("=")
            if kkk in config:
                config[kkk] = vvv

    nrows = 866
    ncols = 654
    xllcorner = 3280415
    yllcorner = 5237501
    cellsize = 1000

    wgs84 = Proj(init="epsg:4326")
    gk3 = Proj(init="epsg:31467")
    gk5 = Proj(init="epsg:31469")
    #r_gk5, h_gk5 = transform(wgs84, gk5, lon, lat)

    elem_to_filepath = {
        "tmin": "Min_TMP(C)/agrar_nachlieferung_D_TMIN_{:04d}/raster_out_D_TMIN_03_{:04d}.txt",
        #"tavg": "temperature",
        "tmax": "Max_TMP(C)/agrar_nachlieferung_D_TMAX_{:04d}/raster_out_D_TMAX_03_{:04d}.txt",
        "precip": "Precipitation(mm)/agrar_nachlieferung_D_RRSUM_{:04d}/raster_out_D_RRSUM_03_{:04d}.txt",
        "relhumid": "Relative humidity(mean %)/agrar_nachlieferung_D_RFMIT_{:04d}/raster_out_D_RFMIT_03_{:04d}.txt",
        "globrad": "Radiation(mean %)/agrar_nachlieferung_RGMIT_{:04d}/raster_out_RGMIT_03_{:04d}.txt",
        "wind": "Windspeed(m per s)/agrar_nachlieferung_D_WINDMIT_{:04d}/raster_out_D_WINDMIT_03_{:04d}.txt",
    }

    def write_files(cache, nrows):
        "write files"

        no_of_files = len(cache)
        count = 0
        for (y, x), rows in cache.iteritems():
            path_to_outdir = config["path_to_output"] + "row-" + str(y+1) + "/"
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

    
    write_days_threshold = 367 #ys
    for year in range(1990, 2017+1):
        if year < int(config["start_year"]):
            continue
        if year > int(config["end_year"]):
            break

        start_of_year_date = date(year, 1, 1)

        start_year_timer = time.clock()
        cache = defaultdict(list)    

        for doy in range(1, 365 + (1 if year % 4 == 0 else 0) + 1):
            if year == int(config["start_year"]) and doy < int(config["start_doy"]):
                continue
            if year == int(config["end_year"]) and doy > int(config["end_doy"]):
                break

            print "year:", year, "doy:", doy, "ys ->",
            data = {}
            for elem, filepath in elem_to_filepath.iteritems():
                ds = np.loadtxt(config["path_to_data"] + filepath.format(year, doy), skiprows=6, dtype=int)
                data[elem] = ds

            ref_data = data["tmin"]

            for y in range(int(config["start_y"]) - 1, nrows if int(config["end_y"]) < 0 else int(config["end_y"])):
                #print "y: ", y, "->"
                #start_y = time.clock()
                if y % 100 == 0:
                    print y,

                #for x in range(ncols): #ref_data.shape[2]):
                for x in range(int(config["start_x"]) - 1, ncols if int(config["end_x"]) < 0 else int(config["end_x"])):
                    #print x,
                   
                    if int(ref_data[y, x]) == -9999:
                        continue

                    r_gk3 = xllcorner + (x*cellsize) + (cellsize / 2)
                    h_gk3 = yllcorner + ((nrows - y)*cellsize) - (cellsize / 2)

                    lon, lat = transform(gk3, wgs84, r_gk3, h_gk3)
                    r_gk5, h_gk5 = transform(gk3, gk5, r_gk3, h_gk3)

                    current_date = start_of_year_date + timedelta(days=doy-1)

                    row = [
                        current_date.strftime("%Y-%m-%d"),
                        str(round(data["tmin"][y, x] / 10.0, 1)),
                        str(round((data["tmin"][y, x] + data["tmax"][y, x]) / 2.0 / 10.0, 1)),
                        str(round(data["tmax"][y, x] / 10.0)),
                        str(round(data["precip"][y, x] / 10.0, 1)),
                        str(data["relhumid"][y, x]),
                        str(round(data["globrad"][y, x] / 100.0, 2)),
                        str(round(data["wind"][y, x] / 10.0, 1))
                    ]
                    cache[(y,x)].append(row)
                
                #end_y = time.clock()
                #print y, #str(y) + "|" + str(int(end_y - start_y)) + "s ",
               
            if doy > int(config["start_doy"]) and doy % write_days_threshold == 0:
                print ""
                s = time.clock()
                write_files(cache, nrows)
                cache = defaultdict(list)
                e = time.clock()
                print "wrote in year:", year, write_days_threshold, " days in", (e - s), "seconds"

            #for dataset in data.values():
            #    dataset.close()
            print ""

        #write remaining cache items
        print ""
        s = time.clock()
        write_files(cache, nrows)
        cache = defaultdict(list)
        e = time.clock()
        print "wrote in year:", year, " remaining data in", (e-s), "seconds"

        end_year_timer = time.clock()
        print "running", (int(config["end_doy"]) - int(config["start_doy"]) + 1), " doys took", (end_year_timer - start_year_timer), "seconds"

if __name__ == "#__main__": 
    ascii_to_csv()


def create_latlon_rowcol_files():
    nrows = 866
    ncols = 654
    xllcorner = 3280415
    yllcorner = 5237501
    cellsize = 1000

    wgs84 = Proj(init="epsg:4326")
    gk3 = Proj(init="epsg:31467")
    gk5 = Proj(init="epsg:31469")

    lat_lon_grid_file = open("lat_lon.grid", "w")
    data_no_data_grid_file = open("data_no-data.grid", "w")
    latlon_to_rowcol_json_file = open("latlon_to_rowcol.json", "w")
    rowcol_to_latlon_json_file = open("rowcol_to_latlon.json", "w")
    rowcol_to_gk5_rh_json_file = open("rowcol_to_gk5_rh.json", "w")
    rowcol_to_gk3_rh_json_file = open("rowcol_to_gk3_rh.json", "w")

    path_to_template_file = "A:/data/climate/dwd/grids/germany/daily_from_bahareh/daily/Max_TMP(C)/agrar_nachlieferung_D_TMAX_1990/raster_out_D_TMAX_03_0001.txt"
    header = ""
    with open(path_to_template_file, "r") as _:
        for i in range(6):
            header = header + _.readline()
    ds = np.loadtxt(path_to_template_file, skiprows=6, dtype=int)

    lat_lon_grid_file.write(header.replace("-9999", "---------------"))
    data_no_data_grid_file.write(header.replace("-9999", "0"))
    ll_to_rc_json_data = []
    rc_to_ll_json_data = []
    rc_to_gk5_json_data = []
    rc_to_gk3_json_data = []

    for row in range(0, nrows):
        ll_line = []
        dnd_line = []
        for col in range(0, ncols):
            
            r_gk3 = xllcorner + (col*cellsize) + (cellsize / 2)
            h_gk3 = yllcorner + ((nrows - row)*cellsize) - (cellsize / 2)
            lon, lat = transform(gk3, wgs84, r_gk3, h_gk3)
            r_gk5, h_gk5 = transform(gk3, gk5, r_gk3, h_gk3)
            
            is_data = ds[row, col] != -9999

            dnd_line.append("1" if is_data else "0")
            if is_data:
                ll_to_rc_json_data.append([[lat, lon], [row, col]])
                rc_to_ll_json_data.append([[row, col], [lat, lon]])
                rc_to_gk5_json_data.append([[row, col], [r_gk5, h_gk5]])
                rc_to_gk3_json_data.append([[row, col], [r_gk3, h_gk3]])
                ll_line.append("{:07.4f}|{:07.4f}".format(lat, lon))
            else:
                ll_line.append("---------------")

        lat_lon_grid_file.write(" ".join(ll_line))
        data_no_data_grid_file.write(" ".join(dnd_line))
        if row < 865:
            lat_lon_grid_file.write("\n")
            data_no_data_grid_file.write("\n")

        if row % 10 == 0:
            print "wrote line", row

    json.dump(ll_to_rc_json_data, latlon_to_rowcol_json_file)#, indent=2)
    json.dump(rc_to_ll_json_data, rowcol_to_latlon_json_file)#, indent=2)
    json.dump(rc_to_gk5_json_data, rowcol_to_gk5_rh_json_file)#, indent=2)
    json.dump(rc_to_gk3_json_data, rowcol_to_gk3_rh_json_file)#, indent=2)

    lat_lon_grid_file.close()
    data_no_data_grid_file.close()
    latlon_to_rowcol_json_file.close()
    rowcol_to_latlon_json_file.close()
    rowcol_to_gk5_rh_json_file.close()
    rowcol_to_gk3_rh_json_file.close()

if __name__ == "__main__": 
    create_latlon_rowcol_files()