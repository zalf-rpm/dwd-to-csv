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

import mysql.connector

def main():

    config = {
        "path_to_data": "Daily/",
        "path_to_output": "out/",
        "start_y": "1",
        "end_y": "-1",
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

    db = mysql.connector.connect(host="localhost", user="guest", passwd="guest", database="climate_data")

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

    def write_into_db(cache):
        "write into db"

        cursor = db.cursor(prepared=True)
        sql = """INSERT INTO dwd_germany_raw_data (id, date, tmin_times_10, tmax_times_10, precip_times_10, globrad_times_100, relhumid_times_10, windspeed_times_10) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
        result  = cursor.executemany(sql, cache)
        db.commit()
        cursor.close()
    
    write_days_threshold = 31 #ys
    for year in range(1990, 2017+1):
        if year < int(config["start_year"]):
            continue
        if year > int(config["end_year"]):
            break

        start_of_year_date = date(year, 1, 1)

        start_year_timer = time.clock()
        cache = [] 

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
                if y % 100 == 0:
                    print y,

                for x in range(int(config["start_x"]) - 1, ncols if int(config["end_x"]) < 0 else int(config["end_x"])):
                   
                    if int(ref_data[y, x]) == -9999:
                        continue

                    #r_gk3 = xllcorner + (x*cellsize) + (cellsize / 2)
                    #h_gk3 = yllcorner + ((nrows - y)*cellsize) - (cellsize / 2)

                    #lon, lat = transform(gk3, wgs84, r_gk3, h_gk3)
                    #r_gk5, h_gk5 = transform(gk3, gk5, r_gk3, h_gk3)

                    current_date = start_of_year_date + timedelta(days=doy-1)

                    row = (
                        (y+1)*10000 + (x+1),
                        current_date.strftime("%Y-%m-%d"),
                        data["tmin"][y, x],
                        data["tmax"][y, x],
                        data["precip"][y, x],
                        data["relhumid"][y, x],
                        data["globrad"][y, x],
                        data["wind"][y, x]
                    )
                    cache.append(row)
                    #print row
                    #write_into_db(cache)  
                    #cache = []

                
            if doy > int(config["start_doy"]) and doy % write_days_threshold == 0:
                print ""
                s = time.clock()
                write_into_db(cache)
                cache = []
                e = time.clock()
                print "wrote in year:", year, write_days_threshold, " days in", (e - s), "seconds"

            print ""

        #write remaining cache items
        print ""
        s = time.clock()
        write_into_db(cache)
        cache = []
        e = time.clock()
        print "wrote in year:", year, " remaining data in", (e-s), "seconds"

        end_year_timer = time.clock()
        print "running", (int(config["end_doy"]) - int(config["start_doy"]) + 1), " doys took", (end_year_timer - start_year_timer), "seconds"

main()