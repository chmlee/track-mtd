from functions import *
import json
import datetime
import time

# read schedule files
with open('../data/reference_cleaned/I_SU.json', 'r') as fp:
    sch = json.load(fp)

sch_sum = sorted(sch, key = lambda sch: sch[0])
dat = []
for item in sch_sum:
    unix_time = int(time2unix(item[0]))
    entry = [2, unix_time-5*60, unix_time] + item[1:]
    dat.append(entry)

####################
# for testing only #
####################
dat0 = []
for item in dat: 
     arrival_time = item[2] 
     if arrival_time > now(): 
        dat0.append(item) 
dat = dat0
####################

it = 1
while True:
    print("==================== ITERATION", it, "====================")
    # count
    it += 1
    n_queue = 0
    n_update = 0
    n_query = 0
    n_arrive = 0

    
    # sort dat
    dat = sorted(dat)

    for entry in dat:
        flag = entry[0]
        next_query = entry[1]
        if flag == 1:
            if next_query < now():  
                n_query += 1
                flag, next_query, t = check_arrival(entry[-3:])
                entry[0] = flag
                entry[1] = next_query
                #print(t, entry[4], entry[2], entry[-1])
                #print(entry[5])

                # print output
                if flag == 0:
                    n_arrive += 1
                    print("")
                    print(entry[3], "has arrived at", entry[4])
                    print("The bus is", now()-entry[2], "late")
                    print("")
        elif flag == 2:                       # future stops
            n_queue += 1
            if next_query < (now() + 5*60): # srriving stops
                n_update +=1
                entry[0] = 1
            else:
                break


    # print output
    print("made", n_query, "queries")
    print(n_arrive, "buses arrive")
    print("updated", n_update, "to queue")
    print(n_queue, "in queue")
    time.sleep(5)
    


