import processing

#call the ownership parcel layer
layers = QgsProject.instance().mapLayersByName("Ownership Parcel_32617")
layer = layers[0]

features = layer.selectedFeatures()
for f in features:
    name = f['ASSESSME_3']

#set input and output file names
polyPath = layer
linePath = "C:/Users/Owner/OneDrive - Oak Ridges Moraine Land Trust (1)/GIS Data/3. Reference Layers/Natural Features/Rivers and Streams/Rivers and Streams Clipped.shp"
clipPath = "C:/Users/Owner/Desktop/Python Training Scripts/temp/temp_hydro.shp"

#run the clip tool
processing.run("native:clip", {'INPUT':linePath,'OVERLAY':polyPath,'OUTPUT':clipPath})

#add output to the qgis interface
iface.addVectorLayer(clipPath, '', 'ogr')

#add output to the qgis interface
iface.addVectorLayer(clipPath, '', 'ogr') 

#write to shape file
writer = QgsVectorFileWriter.writeAsVectorFormat(layer, fn, 'utf-8', driverName = 'ESRI Shapefile', onlySelected=True)

print(name)

del(writer)
