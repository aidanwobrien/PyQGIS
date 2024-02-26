
## Query the Greenbelt Designation Layer - https://geohub.lio.gov.on.ca/datasets/lio::greenbelt-designation/about

# Define the URL of the Geojson service
greenbelt_geojson_url = "https://ws.lioservices.lrc.gov.on.ca/arcgis2/rest/services/LIO_OPEN_DATA/LIO_Open06/MapServer/15/query?outFields=*&where=1%3D1&f=geojson"

# Create the Geojson layer object
greenbelt_geojson_layer = QgsVectorLayer(greenbelt_geojson_url, 'Greenbelt')

# Check if the layer was loaded successfully
if not greenbelt_geojson_layer.isValid():
   print("Layer failed to load!")

# Add the Geojson layer to the map registry
QgsProject.instance().addMapLayer(greenbelt_geojson_layer)

#Refresh the map canvas
iface.mapCanvas().refresh()