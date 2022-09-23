#Input modules
from qgis.core import *
from PyQt5.QtGui import *

#Create the Dialog Box
qid = QInputDialog()
address = "Enter the Address"
label = "Address: "
mode = QLineEdit.Normal
default = "<address here in ALL CAPS>"
text, ok = QInputDialog.getText(qid, address, label, mode, default)


#Set the Temp Path
tempPath = "C:/Users/Aidan/Desktop/Python Scripts/temp/" + text + ".shp"

#set the layer to the active layer
for parcel_layer in QgsProject.instance().mapLayers().values():
    if parcel_layer.name() == "Assessment Parcels":
        layer = parcel_layer

#layer = iface.activeLayer()

#Select the features based on the user input
layer.selectByExpression( "ASSESSME_3 LIKE '%{}%' ".format(text) )

#Save the Selected Features of the Layer
processing.run('native:saveselectedfeatures', {'INPUT': layer,'OUTPUT': tempPath})

#Add in the newly selected and saved layer
new_layer = iface. addVectorLayer(tempPath, "", "ogr") 

print ("All done!")