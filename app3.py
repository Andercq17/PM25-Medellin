import dash
from dash import html, dcc, Output, Input, callback
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from scipy.interpolate import griddata
datosmapalat=[]
datosmapalon=[]
datosmapaaqui=[]


json='PM25-Medellin\Datos_SIATA_Aire_pm25.json'
data=pd.read_json(json,convert_dates=True)
latitudes=data.latitud.values.tolist()
longitudes=data.longitud.values.tolist()
pm25enFecha=[]

for k in range(len(data.datos[0])):
    for i in range(21):
        if data.datos[i][k].get("valor")>500 or data.datos[i][k].get("valor")<0:
            data.datos[i][k]["valor"]=0


def colorscaleespeccific(max):
    if max<12:
       return [[0,'green'],[1,'green']]
    elif 12<max<35:
       return [[0,'green'],[0.34,'yellow'],[1,'yellow']]
    elif 35<max<55:
       return [[0,'green'],[0.21,'yellow'],[0.63,'orange'],[1,'orange']]
    elif 55<max<150:
       return [[0,'green'],[0.08,'yellow'],[0.23,'orange'],[0.36,'red'],[1,'red']]
    elif 150<max<250:
       return [[0,'green'],[0.048,'yellow'],[0.13,'orange'],[0.22,'red'],[0.6,'purple'],[1,'purple']]
    elif 150<max<600:
       return [[0.03,'green'],[0.07,'yellow'],[0.11,'orange'],[0.3,'red'],[0.5,'purple'],[1,'purple']]
    
def encontrarPM25EnFecha(fecha):
    pm25enFecha.clear()
    for i in range(21):
        if 0.0 <=data.datos[i][int(fecha)].get("valor")<=12:
            pm25enFecha.append((50/12)*data.datos[i][int(fecha)].get("valor"))
        elif 12.1 <=data.datos[i][int(fecha)].get("valor")<=35.4:
            pm25enFecha.append((((100-51)/(35.4-12.1))*(data.datos[i][int(fecha)].get("valor")-12.1)+51))
        elif 35.5 <=data.datos[i][int(fecha)].get("valor")<=55.4:
            pm25enFecha.append((((150-101)/(55.4-35.5))*(data.datos[i][int(fecha)].get("valor")-35.5)+101))
        elif 55.5 <=data.datos[i][int(fecha)].get("valor")<=150.4:
            pm25enFecha.append((((200-151)/(150.4-55.5))*(data.datos[i][int(fecha)].get("valor")-55.5)+151))
        elif 150.5 <=data.datos[i][int(fecha)].get("valor")<=250.4:
            pm25enFecha.append((((300-201)/(250.4-150.5))*(data.datos[i][int(fecha)].get("valor")-150.5)+201))
        elif 250.5 <=data.datos[i][int(fecha)].get("valor")<=350.4:
            pm25enFecha.append((((400-301)/(350.4-250.5))*(data.datos[i][int(fecha)].get("valor")-250.5)+301))
        elif 350.5 <=data.datos[i][int(fecha)].get("valor")<=500.4:
            pm25enFecha.append((((500-401)/(500.4-350.5))*(data.datos[i][int(fecha)].get("valor")-350.5)+401))
        else:
            pm25enFecha.append(500)
        
def func(x, y):
 return x*(1-x)*np.cos(4*np.pi*x) * np.sin(4*np.pi*y**2)**2


grid_x, grid_y = np.meshgrid(np.linspace(min(longitudes), max(longitudes), 200), np.linspace(min(latitudes), max(latitudes), 200))

encontrarPM25EnFecha(0)

maximo=max(pm25enFecha)
datosmapalat=latitudes
datosmapalon=longitudes
datosmapaaqui=pm25enFecha
fig=go.Figure(go.Densitymapbox(lat=datosmapalat,lon=datosmapalon,z=datosmapaaqui,
                               radius=40,zmin=min(pm25enFecha),zmax=max(pm25enFecha),colorscale=colorscaleespeccific(maximo)))

fig.update_layout(mapbox={
        'style':'stamen-terrain',
        'center': { 'lon': -75.56, 'lat': 6.24},
        'zoom': 10
    })
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
app=dash.Dash()

app.layout=html.Div([
    html.H1("Calidad Aire Medellin cada dia de Marzo a las 4 am"),
    html.H1(data.datos[0][200].get("fecha"), id='titulo-h1'),
    dcc.Graph(figure=fig,id="mimapa"),
    dcc.Slider(200,944,24,value=200,id="mislider")
])
@app.callback(
    Output('titulo-h1', 'children'),
    [Input('mislider', 'value')]  
)
def actualizar_titulo_h1(valor):
    return data.datos[0][int(valor)].get("fecha")

@callback(Output('mimapa','figure'),Input('mislider','value'))
def funcioncambio(valorslider):
    encontrarPM25EnFecha(valorslider)
    maximo=max(pm25enFecha)
    figuraLocal=go.Figure(go.Densitymapbox(lat=datosmapalat,lon=datosmapalon,z=pm25enFecha,
                               radius=40,zmin=min(pm25enFecha),zmax=max(pm25enFecha),colorscale=colorscaleespeccific(maximo)))
    
    figuraLocal.update_layout(mapbox={
        'style':'stamen-terrain', 
        'center': { 'lon': -75.56, 'lat': 6.24},
        'zoom': 10
        
    })
    figuraLocal.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return figuraLocal

app.run(debug=True,use_reloader=False)
