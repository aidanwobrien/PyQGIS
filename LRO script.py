import decimal
from qgis.core import *

#set the layer to the active layer
layer = iface.activeLayer()
#set the features to the selected features
features = layer.selectedFeatures()

#Iterate through the features
for f in features:
    
    #make a geometry of the feature
    d = QgsDistanceArea()
    d.setEllipsoid('WGS84')
    geom = f.geometry()
    
    #call the int feature ARN = iarn
    ilro = f['REG_OFFICE']
    
    #convert the integers to strings and add hyphens
    slro = str(ilro)
    
#Print the LRO
print("The LRO is:" + "    " + (slro))
