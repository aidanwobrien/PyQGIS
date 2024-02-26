
# The WMS is constructed based on which layer you want to load in and the format of the image.
# Consult the URL xml file which will point you to the layer name. In this case layer = 1 references the ORM Planning Area layer of the service.
# When loading WMS we have to define the layer - cant just be the whole WMS package. 

# Define the URL of the WMS service
wms_url = "crs=EPSG:4326&format=image/png&layers=1&styles&url=https://ws.lioservices.lrc.gov.on.ca/arcgis2/services/LIO_OPEN_DATA/LIO_Open06/MapServer/WMSServer?request=GetCapabilities&service=WMS"

# The url is constructed from these components, found in the WMS XML file
# crs = 
# format = 
# layers =
# styles = 
# url = 
## good resource here https://www.e-education.psu.edu/geog585/node/699
## bbox could be useful for calling only features within a bbox


# Create the WMS raster layer object
wms_layer = QgsRasterLayer(wms_url, 'ORM Planning Area', 'WMS')

# Check if the layer was loaded successfully
if not wms_layer.isValid():
    print("Layer failed to load!")

# Add the WMS raster layer to the map registry
QgsProject.instance().addMapLayer(wms_layer)

# Refresh the map canvas
iface.mapCanvas().refresh()
