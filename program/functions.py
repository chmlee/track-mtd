from urllib.request import urlopen
from bs4 import BeautifulSoup
import datetime
import time
import json
import os

sch_future = []
sch_queue = []    
result = []    
warning = []

def now():
    return int(time.time())

def time_remaining(X): 
    url = X[0]
    number_check = str(X[1])
    destination_check = X[2]
    number = str(number_check)
    html = urlopen(url) 
    bs = BeautifulSoup(html.read(), features="html5lib") 
    info = bs.findAll("div", {"class":["number", "destination", "not-soon"]}) 
    n = 0
    t = 98
    while n < (len(info) - 2):
        number = info[n].contents[0]
        if number == number_check:
            destination = info[n+1].contents[0]
            if destination == destination_check:
                time_remaining_str = info[n+2].contents[0]
                if ":" not in time_remaining_str:
                    time_remaining_list = time_remaining_str.split(" ")
                    if len(time_remaining_list) == 1:
                        t = 0
                    else:
                        t = int(time_remaining_list[0])
                else:
                    t = 99 #invalid input ":"
                break
        else:
            t = 98 #bus does not stop
        n += 1
    return t

def time2unix(hms):
    hms_list = hms.split(":")
    hour = hms_list[0]
    minute = hms_list[1]
    second = hms_list[2]
    year = str(datetime.datetime.now().year)
    month = str(datetime.datetime.now().month)
    day = str(datetime.datetime.now().day)
    if hour == 24:      #convert to valid format 24->00
        hour = 0
    time_join = "-".join([year, month, day, hour, minute, second])
    unix_time = time.mktime(datetime.datetime.strptime(time_join, "%Y-%m-%d-%H-%M-%S").timetuple())
    if int(hour) <= 5:  #add 24 hours to early morning trips
        unix_time += 24*60*60
    return unix_time

def check_arrival(item):
    info  = item[-3:] 
    t = time_remaining(info)
    flag = 1
    if t == 99:
        next_query = now()
    elif t == 98:
        next_query = now()
        flag = -98
    elif t >= 10:
        next_query = now() + 5*60
    elif t >= 5:
        next_query = now() + 3*60
    elif t >= 3:
        next_query = now() + 1*60
    elif t == 2:
        next_query = now() + 30
    elif t == 1:
        next_query = now() + 15
    else:
        next_query = now()
        flag = 0
    return flag, next_query, t 

def print_route(X):
    # load stop-url dictionary
    with open('../data/reference_cleaned/stop_dict.json', 'r') as fp:
        stop_dict = json.load(fp)
    sch = []

    # read stop-time file
    st_file = open(os.getcwd() + "/../data/reference/stop_times.txt")    
    st = st_file.read()    
    st_file.close()    
    st_list = st.split('\n')    
    for n in range(len(st_list)):    
        st_list[n] = st_list[n].split(',')    

    # extract information
    route_name = X[0]               # str
    route_number = X[1]             # str
    trip_max_num = X[2]             # int
    trip_suffix = X[3]              # str
    default_terminal_list = X[4]    # list
    default_direction = X[5]        # str
    alt_direction = X[6]            # str

    # find all valid trip name
    trip_name_check_list = []
    for trip_num in range(1, trip_max_num+1):
        trip_name_check = str(route_name) + str(trip_num) + "_" + trip_suffix 
        trip_name_check_list.append(trip_name_check)

    # find all trip in st_list
    for trip_stop in st_list[:-1]:
        trip_fullname = trip_stop[0]
        trip_route = trip_fullname.split('_')[-2]
        trip_day = trip_fullname.split('_')[-1]
        trip_name = "_".join([trip_route, trip_day])
        if trip_name in trip_name_check_list:
            if trip_stop[5] != "":      # update terminal
                sch_terminal = trip_stop[5]
            if sch_terminal in default_terminal_list:
                sch_dest = default_direction
            else:
                sch_dest = alt_direction
            print(sch_dest)
            sch_time = trip_stop[1]
            sch_stop = trip_stop[3]
            sch_stop_url = stop_dict[sch_stop]
            entry = [sch_time, trip_name, sch_stop, sch_stop_url, route_number, sch_dest]
            sch.append(entry)
    # create list in json
    file_name = str(route_name) + "_" + trip_suffix 
    with open("../data/reference_cleaned/" + file_name + ".json", "w") as fp:
        json.dump(sch, fp)

