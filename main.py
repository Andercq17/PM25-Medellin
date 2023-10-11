import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

json='Datos_SIATA_Aire_pm25.json'
data=pd.read_json(json,convert_dates=True)
latitudes=data.latitud.values.tolist()
longitudes=data.longitud.values.tolist()

import numpy as np

#creo mi funcion base (es la que conozco, es mi modelo conocido)​

def func(x, y):
 return x*(1-x)*np.cos(4*np.pi*x) * np.sin(4*np.pi*y**2)**2

#creo una malla de 100 x 200
grid_x, grid_y=np.meshgrid(np.linspace(min(longitudes),max(longitudes),200),np.linspace(min(latitudes),max(latitudes),200))
#me invento un grupo de puntos aleatorios​
# ejecuto las interpolaciones, uso tres metodos para comparar su desempeno​
from scipy.interpolate import griddata

import matplotlib.pyplot as plt

for k in range(40):
  fecha=data.datos[1][k].get("fecha")
  m=[]
  for i in range(21):
    m.append(data.datos[i][k].get("valor"))
  m=np.array(m)
  #la malla los valores que deseo calcular para mi modelo de deduccion real​
  gridz=griddata((latitudes,longitudes),m, (grid_y,grid_x),method='cubic')
  plt.contourf(grid_x,grid_y,gridz)
  plt.plot(longitudes,latitudes,'r.',ms=1)
  plt.title(fecha)
  plt.pause(0.01)
plt.colorbar()
plt.show()