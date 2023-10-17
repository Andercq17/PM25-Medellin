import dash
from dash import html, dcc, Output, Input, callback
import plotly.graph_objects as go
import pandas as pd
import numpy as np
datosmapalat=[]
datosmapalon=[]
datosmapaaqui=[]


json='PM25-Medellin\Datos_SIATA_Aire_pm25.json'
data=pd.read_json(json,convert_dates=True)
latitudes=data.latitud.values.tolist()
longitudes=data.longitud.values.tolist()
for k in range(len(data.datos[0])):
    for i in range(21):
        if data.datos[i][k].get("valor")>500 or data.datos[i][k].get("valor")<0:
            data.datos[i][k]["valor"]=0

pm25enFecha=[]
def encontrarPM25EnFecha(fecha):
    pm25enFecha.clear()
      
    for i in range(21):
        pm25enFecha.append(data.datos[i][int(fecha)].get("valor"))
# def indiceCalidad(valor):
#   if 0 < valor < 50:
#     return 0, "Good"
#   elif 51 < valor < 100:
#     return 1, "Moderate"
#   elif 101 < valor < 150:
#     return 2, "Unhealthy for sensitive groups"
#   elif 151 < valor < 200:
#     return 3, "Unhealthy"
#   elif 201 < valor < 300:
#     return 4, "Very unhealthy"
#   elif 301 < valor < 500:
#     return 5, "Hazardous"
#   else:
#     return 6, "Error"


# criticos=[]

# for k in range(21):
#   for i in range(len(data.datos[0])):
#     indiceCalidadDatos=indiceCalidad(data.datos[k][i].get("valor"))
#     indice=indiceCalidadDatos[0]
#     categoria=indiceCalidadDatos[1]
#     if indice >= 4 and indice < 6:
#       dato={'sensor':k,
#             'fecha':data.datos[k][i].get("fecha"),
#             'valor':data.datos[k][i].get("valor"),
#             'nombreValor':categoria,
#             'longitud':longitudes[k],
#             'latitud':latitudes[k]
#       }
#       criticos.append(dato)





colorscale_semaforo = [
    [0, 'green'],
    [0.25, 'yellow'],
    [0.5, 'orange'],
    [0.75, 'red'],
    [1, 'purple']
]
encontrarPM25EnFecha(0)

datosmapalat=latitudes
datosmapalon=longitudes
datosmapaaqui=pm25enFecha
print(datosmapaaqui)
fig=go.Figure(go.Densitymapbox(lat=datosmapalat,lon=datosmapalon,z=datosmapaaqui,
                               radius=40,zmin=min(pm25enFecha),zmax=max(pm25enFecha),colorscale=colorscale_semaforo))

fig.update_layout(mapbox={
        'style': "open-street-map",
        'center': { 'lon': -75.56, 'lat': 6.24},
        'zoom': 10
    })
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
app=dash.Dash()

app.layout=html.Div([
    dcc.Graph(figure=fig,id="mimapa"),
    dcc.Slider(0,(len(data.datos[0])-1),100,value=1,id="mislider")
])

@callback(Output('mimapa','figure'),Input('mislider','value'))
def funcioncambio(valorslider):
    encontrarPM25EnFecha(valorslider)
    # figuraLocal=go.Figure(go.Densitymapbox(lat=[datosmapalat[valorslider]],lon=[datosmapalon[valorslider]]
    #                                        ,z=[datosmapaaqui[valorslider]],
    #                            radius=40,opacity=0.8,zmin=0,zmax=500),)
    
    figuraLocal=go.Figure(go.Densitymapbox(lat=datosmapalat,lon=datosmapalon
                                           ,z=pm25enFecha,
                               radius=40,zmin=min(pm25enFecha),zmax=max(pm25enFecha),colorscale=colorscale_semaforo))
    
    figuraLocal.update_layout(mapbox={
        'style': "open-street-map",
        'center': { 'lon': -75.56, 'lat': 6.24},
        'zoom': 10
        
    })
    print(pm25enFecha)
        
    
    figuraLocal.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return figuraLocal

app.run(debug=True,use_reloader=False)
