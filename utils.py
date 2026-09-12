import folium
from OSMPythonTools.nominatim import Nominatim

def show_map(lat, lon):
    m = folium.Map(location=[lat, lon], 
               zoom_start=18, 
               tiles='openstreetmap')
    folium.Marker(
        location=[lat, lon],
        tooltip="Click for details",
        icon=folium.Icon(color="red", icon="info-sign")).add_to(m)

    return m


nominatim = Nominatim(userAgent="Pujo_atlas/2.0")

def data_validator(lat,lon):
    result = nominatim.query(lat, lon, reverse=True)
    return result.displayName()
    time.sleep(1.5)