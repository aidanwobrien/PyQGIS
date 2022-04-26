import processing
import os
import time

tmStart = time.time()

#SAR CALL

#Set the layer to the active layer
layer = iface.activeLayer()
#Get the Selected Features from the Active Layer
for f in layer.getSelectedFeatures():
    #Get the ARN Feature and call it ARN
    arn = f['ARN']
    #Make ARN a string
    arn = str(arn)

#set input and output file names to a temporary file labelled with the ARN
tempPath = "C:/Users/Owner/Desktop/Python Scripts/temp/temp_select" + arn + ".shp"
clipPath = "C:/Users/Owner/Desktop/Python Scripts/temp/SAR_clip" + arn + ".shp"

#Set the Overlay Path from the Selection
for lyr in QgsProject.instance().mapLayers().values():
    if lyr.name() == "Updated NHMP 2022":
        parcelPath = lyr

#extract selected features from the Overlay Parcel Layer
selected = processing.run('native:saveselectedfeatures', {'INPUT': parcelPath,'OUTPUT': tempPath})

##Unselect selection
#parcelPath.removeSelection()

#Set the SAR layer to be clipped
for lyry in QgsProject.instance().mapLayers().values():
    if lyry.name() == "SAR_tracked":
        SARPath = lyry
        break

#Set the clipped SAR layer
for lyrz in QgsProject.instance().mapLayers().values():
    if lyrz.name() == "SAR_clip":
        clipPath = lyrz
        break

#run the clip tool
processing.run("native:clip", {'INPUT':SARPath,'OVERLAY':tempPath,'OUTPUT':clipPath})

#add SAR output to the qgis interface
iface.addVectorLayer(clipPath, '', 'ogr')
#add temporary selection to the qgis interface so it is removed from the qtr-ltr bin and can be deleted afterwards
iface.addVectorLayer(tempPath, '', 'ogr')

#Get the Features from the new SAR layer that was clipped to selection
sar_layer = QgsProject.instance().mapLayersByName('SAR_clip'+ arn)[0]
sar_features = sar_layer.getFeatures()

sar_list = []

#Iterate through the features and make them into a list
for sar_feat in sar_features:
    sar = sar_feat['ENGLISH_CO']
    sar_list.append(sar)

#Print the List of SAR on the selected Parcel
sar_list = set(sar_list)
print(list(sar_list))


#Remove the temporary selected layer from the interface
temp_to_be_deleted = QgsProject.instance().mapLayersByName('temp_select' + arn)[0]

#Remove the temporary selected layer from the interface
QgsProject.instance().removeMapLayer(temp_to_be_deleted.id())


#Remove the temporary clipped layer from the interface
sar_to_be_deleted = QgsProject.instance().mapLayersByName('SAR_clip'+ arn)[0]
QgsProject.instance().removeMapLayer(sar_to_be_deleted.id())

#Reset the active layer to the Parcel Layer
iface.setActiveLayer(parcelPath)

#Delete the temporary files from the directory
os.remove("C:/Users/Owner/Desktop/Python Scripts/temp/SAR_clip" + arn + ".shp")
os.remove("C:/Users/Owner/Desktop/Python Scripts/temp/SAR_clip" + arn + ".dbf")
os.remove("C:/Users/Owner/Desktop/Python Scripts/temp/SAR_clip" + arn + ".shx")
os.remove("C:/Users/Owner/Desktop/Python Scripts/temp/SAR_clip" + arn + ".prj")
#os.remove("C:/Users/Owner/Desktop/Python Scripts/temp/temp_select" + arn + ".shp")
#os.remove("C:/Users/Owner/Desktop/Python Scripts/temp/temp_select" + arn + ".dbf")
#os.remove("C:/Users/Owner/Desktop/Python Scripts/temp/temp_select" + arn + ".shx")
#os.remove("C:/Users/Owner/Desktop/Python Scripts/temp/temp_select" + arn + ".prj")


tmEnd = time.time()
print("Run time = {0:.3f} seconds".format(tmEnd-tmStart))