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
    iarn = f['ARN']
    
    #convert the integers to strings and add hyphens
    sarn = str(iarn)
    final_arn = sarn[0:2] + '-' + sarn[2:4] + '-' + sarn[4:7] + '-' + sarn[7:10] + '-' + sarn[10:15]+ '-' + sarn[15:19]
    
    # Convert the geometry to Ha
    ha = d.convertAreaMeasurement(d.measureArea(geom), QgsUnitTypes.AreaHectares)
    ha_rounded = decimal.Decimal(ha)
    
    # Convert the geometry to Acres
    ac = d.convertAreaMeasurement(d.measureArea(geom), QgsUnitTypes.AreaAcres)
    ac_rounded = decimal.Decimal(ac)
      
print("The ARN is:" + "    " + (final_arn))
