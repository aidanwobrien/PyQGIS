import decimal
from qgis.core import *

#set the layer to the active layer
layer = iface.activeLayer()
#set the features to the selected features
features = layer.selectedFeatures()

#Iterate through the features
for f in features:
    #call the int feature lro = ilro
    ilro = f['REG_OFFICE']
    #convert the integers to strings of only the first two digits
    slro = str(ilro)
    final_lro = slro[0:2]
    #call the int feature ARN = iarn
    ipin = f['IDENT']
    #convert the integers to strings and add hyphens
    spin = str(ipin)
    final_pin = spin[0:5] + '-' + spin[5:9]

#Print the LRO, PIN, and sizes in ha and acres
print("The LRO is:" + "    " + (final_lro))
print("The PIN is:" + "    " + (final_pin))
