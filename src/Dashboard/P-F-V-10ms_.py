import pandas as pd
import matplotlib.pyplot as plt
import itertools
import time
import datetime
import psycopg2


#outputs mock values for pressure for one respiratory cycle, about 7 seconds
def pres(freq='100ms'):

    #mock values for pressure, to be interpolated if higher frequency is needed
    pressure = [6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6.2,9,14,14.25,14.5,14.75,15,15.25,15.5,15.75,
                16,16.25,16.5,16.75,17,17.25,17.5,17.75,18,18.25,18.5,18.75,19,19.25,19.5,19.75,20,
                10,9.75,9.5,9.25,9,8.75,8.5,8.25,8,7.75,7.5,7.25,7,6.75,6.5,6.25,6,6,6,6,6,6,6,6,6,6,6,6]


    #create dataframe based on these values
    rng = pd.date_range("00:00",periods=len(pressure), freq='100ms')
    df = pd.DataFrame({'Val' : pressure}, index=rng)

    #resample only if freq is different from the standard 10hz
    if freq != '100ms':
        df=df.resample(freq).mean().interpolate(method='linear')

    #smooth curve to make it more realistic
    mov= df.rolling(5).mean()
    mov = mov.fillna(6)
    return mov

#outputs mock values for flow rate for one respiratory cycle, about 7 seconds
def flow(freq='100ms'):
    #mock values for flow rate, to be interpolated if higher frequency is needed
    flow_rate = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,50,50,50,50,50,50,50,50,50,
                 50,50,50,50,
                 50,50,50,50,50,50,50,50,50,0,-50,-40,-35,-30,-26,-23,-20,-18,
                 -16,-14,-12,-10,-8,-6,-4,-3,-2,-1,-0.5,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

    #create dataframe based on these values
    rng = pd.date_range("00:00",periods=len(flow_rate), freq='100ms')
    df = pd.DataFrame({'Val' : flow_rate}, index=rng)

    #resample only if freq is different from the standard 10hz
    if freq != '100ms':
        df=df.resample(freq).mean().interpolate(method='linear')

    #smooth curve to make it more realistic
    mov= df.rolling(5).mean()
    mov = mov.fillna(0)
    return mov

#outputs mock values for volume for one respiratory cycle, about 7 seconds
def vol(freq='100ms'):
    #mock values for volume, to be interpolated if higher frequency is needed
    volume = [20,20,20,20,20,20,20,20,20,20,20,20,20,20,50,100,150,200,250,300,350,400,450,500,475,
                 450,425,400,375,350,325,300,275,250,237.5,225,212.5,200,187.5,175,162.5,150,137.5,
              125,112.5,100,87.5,81,75,68,62.5,56,50,43.5,37.5,31,25,23,20,20,20,20,20,20,20,20,20,20,20,20]

    #create dataframe based on these values
    rng = pd.date_range("00:00",periods=len(volume), freq='100ms')
    df = pd.DataFrame({'Val' : volume}, index=rng)

    #resample only if freq is different from the standard 10hz
    if freq != '100ms':
        df=df.resample(freq).mean().interpolate(method='linear')

    #smooth curve to make it more realistic
    mov= df.rolling(3).mean()
    mov = mov.fillna(20)
    return

###TURN EVERYTHING INTO ITERABLE LISTS

pres=pres()
flow = flow()
vol = vol()

pres = pres['Val'].values.tolist()
flow = flow['Val'].values.tolist()
vol = vol['Val'].values.tolist()


#### START POSTGRESQL QUERY

connection = psycopg2.connect(user="pi",
                                  password="INSERT PASSWORD",
                                  host="INSERT IP",
                                  port="5432",
                                  database="INSERTDB NAME")
cursor = connection.cursor()


for i in itertools.cycle(range(len(vol))):
           now = datetime.datetime.now()
           timestamp = now.timestamp()
           postgres_insert_query = ' INSERT INTO paziente0("time","PRESSURE", "VOLUME", "FLOW") VALUES (%s,%s,%s,%s)'
           record_to_insert = (timestamp, pres[i], vol[i], flow[i])
           print(record_to_insert)
           cursor.execute(postgres_insert_query, record_to_insert)

           connection.commit()
           count = cursor.rowcount
           print (count, "Record inserted successfully into mobile table")
           time.sleep(.1)
