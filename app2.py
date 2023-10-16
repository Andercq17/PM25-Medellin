import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time
datos='datosTemperatura.csv'
data=pd.read_csv('PM25-Medellin\datosTemperatura.csv')
datalimpia=data.drop(data.query('valor==0').index)

timestamp=pd.to_datetime(datalimpia['timestamp'],unit='ms')
plt.plot(timestamp, datalimpia['valor'],'r')
plt.xlabel('timestamp')
plt.ylabel('valor')
plt.show()


#latitudes=data.latitud.values.tolist()
#longitudes=data.longitud.values.tolist()