import folium, pandas

#Map Object
map = folium.Map(location = [38.58, -99.09], zoom_start = 6, tiles='https://api.mapbox.com/styles/v1/mapbox/light-v10/tiles/{z}/{x}/{y}?access_token=pk.eyJ1IjoicmljaGFyZG1jYW1lcm9uOTciLCJhIjoiY2tpN3ZnamN4MHp6ZzJxb2w5d2F0ZzZ4OCJ9.iqWKPPqkMYhnJjSGXIUiFQ', attr='Mapbox Bright')

def chooseColor(elevation):
    if elevation < 1000:
        return 'green'
    elif 1000 <= elevation < 3000:
        return 'orange'
    else:
        return 'red'

#Volcanoe
FGV = folium.FeatureGroup(name = 'Volcanoes')
data = pandas.read_json('world_volcanoes.json')
lat = list(data['lat'])
lon = list(data['lon'])
elev = list(data['elevation'])
name = list(data['name'])


for lt, ln, el, na in zip(lat, lon, elev, name):
    FGV.add_child(folium.Marker(location=[lt, ln], popup=na + '\n' + str(el) + ' m', icon=folium.Icon(chooseColor(el))))

#World Population
FGP = folium.FeatureGroup(name = 'Population')
FGP.add_child(folium.GeoJson(data = open('worldpop.json', 'r', encoding = 'utf-8-sig').read(),
style_function = lambda x: {'fillColor': 'green' if int(x['properties']['POP2005']) < 10000000
else 'orange' if 10000000 <= int(x['properties']['POP2005']) < 20000000 else 'red'} ))

#United States Population
FGPUS = folium.FeatureGroup(name = 'U.S Population')
#FGPUS.add_child()



#Child object of map
map.add_child(FGV)
map.add_child(FGP)
map.add_child(FGPUS)
map.add_child((folium.LayerControl()))
#Save the map, Folium converts HTML, CSS
map.save("Map1.html")