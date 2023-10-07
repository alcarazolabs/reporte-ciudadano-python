import sqlalchemy
from sqlalchemy import text
import numpy
import pandas as pd
import warnings

from folium import Map, Marker, Popup
from folium.plugins import HeatMap

# Crear cadena de conexión a la base de datos
userdb = "freddy"
password = "password"
bdname = "latlonregister"
engine_mysql = sqlalchemy.create_engine('mysql+pymysql://'+userdb+':'+password+'@192.168.18.42:3306/'+bdname)
# Conectarse a la base de datos
con_mysql = engine_mysql.connect()

# Consulta SQL Simple.
query = text("SELECT * FROM reports")
df_mysql = pd.read_sql_query(query, con_mysql)
#print(df_mysql)

#Hacer consulta
query = text("SELECT latitude, longitude, b.name as TipoReporte, a.created_at as Fecha FROM reports a LEFT JOIN report_types b ON a.report_type_id=b.id")
df_mysql = pd.read_sql_query(query, con_mysql)


#preprocesamiento del dataframe

#dejar solo la fecha y borrar tiempo en la columna Fecha

df_mysql["Fecha"] =  pd.to_datetime(df_mysql['Fecha']).dt.date
print(df_mysql)


#Crear mapa de calor con marcadores:
# Hacer un mapa fijo de interes
hmap = Map(location=[-6.7818639, -79.8490405], zoom_start=8,) #Chiclayo

# Agregar puntos de calor
hm_wide = HeatMap(
    list(zip(df_mysql.latitude.values, df_mysql.longitude.values)),
    min_opacity=0.2,
    radius=17, 
    blur=15, 
    max_zoom=1,
)

# Agrgegar marcadores
for idx, row in df_mysql.iterrows():
    # Obtener los valores de latitud y longitud de cada fila
    lat = row['latitude']
    lon = row['longitude']
    
    # Crear una cadena de texto con la descripción del punto
    descripcion = f"Fecha: {row['Fecha']}, Tipo: {row['TipoReporte']}"
    # Crear el marcador y agregarlo al mapa
    Marker([lat, lon], popup=descripcion, clustered_marker=True).add_to(hmap)
    
    

hmap.add_child(hm_wide)
mapFname = '/var/www/html/reporte.html'
hmap.save(mapFname)
