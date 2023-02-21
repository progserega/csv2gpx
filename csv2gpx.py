#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import csv
import sys
import re
from datetime import datetime

arg = 2

def grad2deg(grad_str):
  # 25˚2′0.69564″ -> 25.3242453
  print("in=%s"%grad_str)
  grad=grad_str.split('˚')[0]
  min_str=grad_str.split('˚')[1]
  minutes=min_str.split("′")[0]
  #print(min_str)
  sec=re.sub(r'″$',r'',min_str.split("′")[1])
  #print("grad=%s, minutes=%s, seconds=%s"%(grad,minutes,sec))
  result=int(grad)
  result+=int(minutes)/60
  result+=float(sec)/3600
  print("result=%f"%result)
  return result

def csv2gpx(file_name_csv, file_name_gpx):
    # CSV route file
    csvfile = open(file_name_csv, "r")
    gpxfile = open(file_name_gpx, 'w')

    # read a CSV and establish the header (name of header)
    csv_reader = csv.DictReader(csvfile)
    trk = ""
    coord_list = []
    for row in csv_reader:
        if "˚" in row['lat'] or "'" in row['lat'] or "′" in row["lat"]:
          # конвертируем grad->deg:
          lat=grad2deg(row['lat'])
          lon=grad2deg(row['lon'])
        else:
          lat=row['lat']
          lon=row['lon']

        if 'ele' in row:
          coord_list.append([lat, lon, row['ele']])
        elif 'alt' in row:
          coord_list.append([lat, lon, row['alt']])
        else:
          coord_list.append([lat, lon, "0"])
        # create a segment track (point)
        trk += '<wpt lat ="' + "%f"%lat + '" lon ="' + "%f"%lon + '">'
        trk += '\n'
        if 'ele' in row:
          trk += '<ele>' + row['ele'] + '</ele>'
          trk += '\n'
        if 'alt' in row:
          trk += '<ele>' + row['alt'] + '</ele>'
          trk += '\n'
        trk+='<name>' + row['name'] + '</name>'
        trk+='\n'
        trk += '</wpt>'
        trk += '\n'
    min_coord = min(coord_list)
    max_coord = max(coord_list)

    # metada GPX
    def metada_gpx():
        gpxfile.write('<metadata>')
        gpxfile.write('\n')
        gpxfile.write('<bounds minlat="' + "%f"%min_coord[0] + '" minlon = "' + "%f"%min_coord[1] + '" maxlat = "' + "%f"%max_coord[
            0] + '" maxlon = "' + "%f"%max_coord[1] + '"/>')
        gpxfile.write('\n')
        gpxfile.write('</metadata>')
        gpxfile.write('\n')

    # header GPX
    def header_gpx():
        gpxfile.write('<?xml version="1.0" encoding="UTF-8"?>')
        gpxfile.write('\n')
        gpxfile.write(
            '<gpx version="1.1" creator="David Frias - dfrias88@gmail.com" xmlns="http://www.topografix.com/GPX/1/1" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">')
        gpxfile.write('\n')
        metada_gpx()

    # Establish header GPX
    header_gpx()
    # waypoints:
    gpxfile.write(trk)

    # close file GPX
    def finish_header_gpx():
        gpxfile.write('</gpx>')

    # close track GPX
    finish_header_gpx()

    print("File created!!")


if __name__ == "__main__":
    if len(sys.argv) != arg + 1:
        print("Error - You must put correctly the arguments")
        sys.exit(1)
    csv2gpx(sys.argv[1], sys.argv[2])
