import decimal
from qgis.core import *
import pandas as pd
import numpy as np

#set the layer to the active layer

layer = iface.activeLayer()

#set the features to the selected features

features = layer.selectedFeatures()

address_list = []
town_list = []
arn_list = []
acres_list = []
ha_list = []
score_list = []

#Iterate through the features
for f in features:
    #call the int feature ARN = iarn
    address = str(f['ASSESSMENT_ADDRESS_32617_ASSESSME_3'])
    address_list.append(address)
    town = str(f['ASSESSMENT_ADDRESS_32617_ASSESSME_4'])
    town_list.append(town)
    arn = str(f['ARN'])
    arn_list.append(arn)
    score = str(f['Total_Scor'])
    score_list.append(score)
    
    #Make geometries for sizes
    d = QgsDistanceArea()
    geom = f.geometry()
    sqm = (geom.area())
    ha = (sqm/10000)
    acres = (ha*2.4715)
    ha = round(ha,2)
    ha = str(ha)
    ha_list.append(ha)
    acres = round(acres, 2)
    acres = str(acres)
    acres_list.append(acres)
    
data_dict = dict(ARN = np.asarray(arn_list), Address = np.asarray(address_list), Town = np.asarray(town_list), Hectares = np.asarray(ha_list), Acres = np.asarray(acres_list), Score = np.asarray(score_list))

#Convert the dictionary into a dataframe

df = pd.DataFrame.from_dict(data_dict, orient = 'index')
#df = df.iloc[1: , :]
df = df.transpose()

df.to_csv("C:/Users/Owner/Desktop/Python Scripts/outputs/selected_addresses.csv")
    
    
    
print(df)
