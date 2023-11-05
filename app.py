import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

json='PM25-Medellin\Datos_SIATA_Aire_pm25.json'
data=pd.read_json(json,convert_dates=True)
latitudes=data.latitud.values.tolist()
longitudes=data.longitud.values.tolist()
#fecha=[]
#temperatura=[]
#contaminacion=[]
#for i in range(21):
#  contaminacion.append(data.datos[i][-1].get('valor'))
#  fecha.append(data.datos[i][i].get("fecha"))
#importando la libreria​

import numpy as np

#creo mi funcion base (es la que conozco, es mi modelo conocido)​

def func(x, y):
 return x*(1-x)*np.cos(4*np.pi*x) * np.sin(4*np.pi*y**2)**2

#creo una malla de 100 x 200
grid_x, grid_y=np.meshgrid(np.linspace(min(longitudes),max(longitudes),200),np.linspace(min(latitudes),max(latitudes),300))

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
'''
import geopandas as gpd
import matplotlib.pyplot as plt
map_data = gpd.read_file(json)

# Control del tamaño de la figura del mapa
fig, ax = plt.subplots(figsize=(10, 10))
 
# Control del título y los ejes
ax.set_title('contaminacion en medellin', 
             pad = 20, 
             fontdict={'fontsize':20, 'color': '#4873ab'})
ax.set_xlabel('Longitud')
ax.set_ylabel('Latitud')
 
# Mostrar el mapa finalizado
map_data.plot(column='contaminacion', cmap='plasma', ax=ax, zorder=5)
'''

'''
import folium
m = folium.Map( 
    location=[40.965, -5.664], 
    zoom_start=12, 
    tiles='Stamen Terrain' 
) 
tooltip = 'plaza Mayor'
folium.Marker([40.965, -5.664], popup='Plaza Mayor', tooltip=tooltip).add_to(m) 

m
'''