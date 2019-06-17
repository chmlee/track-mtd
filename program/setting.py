import os
import csv
import time
import datetime
from functions import *
import json

# create dictionary for stop - url
stop_file = open(os.getcwd() + "/../data/reference/stops.txt")
stop = stop_file.read()
stop_file.close()
stop_list = stop.split("\n")
stop_dict = {}
for line in stop_list[:-1]:
    key = line.split(",")[0]
    url0 = line.split(",")[7]
    value_list = ["https://www.mtd.org"]
    for item in url0.split('/')[3:]:
        value_list.append(item)
    value = "/".join(value_list)

    
    #######################
    # found errors in url #
    #######################
    if value == "https://www.mtd.org/maps-and-schedules/bus-stops/info/uniave":
        value = "https://mtd.org/maps-and-schedules/bus-stops/info/campuscir/"
    
    ####################### 
    stop_dict[key] = value
with open('../data/reference_cleaned/stop_dict.json', 'w') as fp:
    json.dump(stop_dict, fp)
                                        

# create list of trips
st_file = open(os.getcwd() + "/../data/reference/stop_times.txt")
st = st_file.read()
st_file.close()
st_list = st.split('\n')
for n in range(len(st_list)):
    st_list[n] = st_list[n].split(',')


# ILLINI Saturday (I1_SA)
sch = []
route = "220"
for trip_stop in st_list[:-1]:
    trip_fullname = trip_stop[0]
    trip_route = trip_fullname.split('_')[-2]
    trip_day = trip_fullname.split('_')[-1]
    trip_name = "_".join([trip_route, trip_day])
    if trip_name == "I1_SA":
        if trip_stop[5] != "":
            sch_terminal = trip_stop[5]
            if sch_terminal == "Transit Plaza":
                sch_dest = "South"
            else:
                sch_dest = "North"
        sch_time = trip_stop[1]
        #sch_sec = time2second(sch_time)
        sch_stop = trip_stop[3]
        sch_stop_url = stop_dict[sch_stop]
        entry = [sch_time, sch_stop, sch_stop_url, route, sch_dest]
        sch.append(entry)



#with open('../data/reference_cleaned/I_SA.json', 'w') as fp:
#    json.dump(sch, fp)
            








