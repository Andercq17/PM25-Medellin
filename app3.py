import dash
from dash import html, dcc, Output, Input, callback
import plotly.graph_objects as go
datosmapalat=[6.24,6.40,6.1]
datosmapalon=[-75.37,-75.34,-75.49]
datosmapaaqui=[6.2,35.6,34.2]
fig=go.Figure(go.Densitymapbox(lat=[datosmapalat[1]],lon=[datosmapalon[1]],z=[datosmapaaqui[1]],
                               radius=40,opacity=0.8,zmin=0,zmax=500))
fig.update_layout(mapbox_style="stamen-terrain",mapbox_center_lon=100)
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

app=dash.Dash()

app.layout=html.Div([
    dcc.Graph(figure=fig,id="mimapa"),
    dcc.Slider(1,3,1,value=2,id="mislider")
])

@callback(Output('mimapa','figure'),Input('mislider','value'))
def funcioncambio(valorslider):
    figuraLocal=go.Figure(go.Densitymapbox(lat=[datosmapalat[valorslider-1]],lon=[datosmapalon[valorslider-1]]
                                           ,z=[datosmapaaqui[valorslider-1]],
                               radius=40,opacity=0.8,zmin=0,zmax=500))
    figuraLocal.update_layout(mapbox_style="stamen-terrain",mapbox_center_lon=100)
    figuraLocal.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return figuraLocal

app.run(debug=True,use_reloader=False)
