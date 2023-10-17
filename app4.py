import dash
from dash import html,dcc, Input, Output
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from scipy.interpolate import griddata

# Cargar datos desde el archivo JSON
json_file = 'PM25-Medellin\Datos_SIATA_Aire_pm25.json'
data = pd.read_json(json_file, convert_dates=True)

# Extraer latitudes y longitudes
latitudes = data.latitud.values.tolist()
longitudes = data.longitud.values.tolist()

# Crear la malla para el gráfico
grid_x, grid_y = np.meshgrid(np.linspace(min(longitudes), max(longitudes), 200), np.linspace(min(latitudes), max(latitudes), 200))

# Inicializar la aplicación Dash
app = dash.Dash(__name__)
colorscale_semaforo = [
    [0, 'green'],
    [0.25, 'yellow'],
    [0.5, 'orange'],
    [0.75, 'red'],
    [1, 'purple']
]
# Define la función para generar un gráfico a partir de los datos de una simulación
def generate_simulation(k):
    fecha = data.datos[1][k].get("fecha")
    m = []
    for i in range(21):
        m.append(data.datos[i][k].get("valor"))
    m = np.array(m)
    gridz = griddata((latitudes, longitudes), m, (grid_y, grid_x), method='cubic')
    
    fig = go.Figure()
    fig.add_trace(go.Contour(z=gridz, colorscale=colorscale_semaforo))
    fig.add_trace(go.Scatter(x=longitudes, y=latitudes, mode='markers', marker=dict(size=5, color='red')))
    fig.update_layout(title=fecha)
    return fig

# Diseño de la aplicación Dash
app.layout = html.Div([
    dcc.Graph(id='simulation-graph'),
    dcc.Interval(id='simulation-interval', interval=500, n_intervals=0),
])

# Callback para actualizar el gráfico de la simulación
@app.callback(Output('simulation-graph', 'figure'), Input('simulation-interval', 'n_intervals'))
def update_simulation(n):
    k = n % 40  # Asegúrate de que 'k' esté dentro del rango de simulaciones
    return generate_simulation(k)

if __name__ == '__main__':
    app.run_server(debug=True)
