from qgis.core import *
import decimal
import processing
import os
import time
import numpy as np
import pandas as pd

tmStart = time.time()

layer = iface.activeLayer()

soil_list = []
sar_list = []

#Extract Selected Features and ARN
for f in layer.getSelectedFeatures():
    
    #get the ARN
    arn = f['ARN']
    arn = str(arn)
    
    #get the nhmp scores
    forest_score = str(f['For_Score'])
    natural_shoreline = str(f['NatShore_S'])
    kettle_score = str(f['Kettle_Sco'])
    lake_score = str(f['LA_Score'])
    plan_score = str(f['Score_Gree'])
    arch_score = str(f['Score_Arch'])
    ansi_score = str(f['ANSI'])
    cws_score = str(f['Score_CWS'])
    riparian_score = str(f['Score_Ripa'])
    psw_score = str(f['Score_PSW'])
    wetland_score = str(f['Score_Wetl'])
    pa_adjacent_score = str(f['Score_PA'])
    size_score = str(f['Score_100a'])
    sar_score = str(f['Score_Spec'])
    wca_score = str(f['Wildlife_C'])
    total_score = str(f['Total_Scor'])
    priority = str(f['Priority'])
    
    #make a geometry of the feature
    d = QgsDistanceArea()
    geom = f.geometry()
    sqm = (geom.area())
    ha = (sqm/10000)
    acres = (ha*2.4715)
    ha = round(ha,2)
    ha = str(ha)
    acres = round(acres, 2)
    acres = str(acres)
    
print("Ha: " + ha)
print("Ac: " + acres)
print("ARN: " + arn)

tempPath = "C:/Users/Owner/Desktop/Python Scripts/temp/temp_select" + arn + ".shp"

for nhmplyr in QgsProject.instance().mapLayers().values():
    if nhmplyr.name() == "Updated NHMP 2022":
        parcelPath = nhmplyr

processing.run('native:saveselectedfeatures', {'INPUT': parcelPath,'OUTPUT': tempPath})

#Extract EcoDistrict
for ecolyr in QgsProject.instance().mapLayers().values():
    if ecolyr.name() == "ECODISTRICT":
        ecoPath = ecolyr

processing.run("qgis:selectbylocation", {"INPUT":ecoPath,"PREDICATE":[1],"INTERSECT":tempPath,"METHOD":1,"OUTPUT":tempPath})

for f in ecoPath.getSelectedFeatures():
    eco_dis_name = f['DIST_NAME']
    eco_dis_code = f['DIST_CODE']
    eco_zone_name = f['ZONE_NAME']
    eco_dis_name = str(eco_dis_name)
    eco_dis_code = str(eco_dis_code)
    eco_zone_name = str(eco_zone_name)
    eco_comb = eco_dis_name + '-' + eco_dis_code + '-' + eco_zone_name
print(eco_comb)
ecoPath.removeSelection()

#Extract Conservation Authority
for calyr in QgsProject.instance().mapLayers().values():
    if calyr.name() == "Conservation Authority Areas":
        caPath = calyr

processing.run("qgis:selectbylocation", {"INPUT":caPath,"PREDICATE":[1],"INTERSECT":tempPath,"METHOD":1,"OUTPUT":tempPath})

for f in caPath.getSelectedFeatures():
    ca_name = f['COMMON_NAM']
#    ca_name = str(ca_name)
print(ca_name)
caPath.removeSelection()

#Extract Primary Watershed
for primwtrlyr in QgsProject.instance().mapLayers().values():
    if primwtrlyr.name() == "ONT_WSHED_BDRY_PRI_DERIVED":
        primwtrPath = primwtrlyr

processing.run("qgis:selectbylocation", {"INPUT":primwtrPath,"PREDICATE":[1],"INTERSECT":tempPath,"METHOD":1,"OUTPUT":tempPath})

for f in primwtrPath.getSelectedFeatures():
    primwtr_name = f['NAME']
    primwtr_name = str(primwtr_name)
print(primwtr_name)
primwtrPath.removeSelection()

#Extract Secondary Watershed
for scdwtrlyr in QgsProject.instance().mapLayers().values():
    if scdwtrlyr.name() == "OntarioSecondaryWatersheds":
        scdwtrPath = scdwtrlyr

processing.run("qgis:selectbylocation", {"INPUT":scdwtrPath,"PREDICATE":[1],"INTERSECT":tempPath,"METHOD":1,"OUTPUT":tempPath})

for f in scdwtrPath.getSelectedFeatures():
    scdwtr_name = f['NAME']
    scdwtr_name = str(scdwtr_name)
print(scdwtr_name)
scdwtrPath.removeSelection()

#Extract Tertiary Watershed
for trtwtrlyr in QgsProject.instance().mapLayers().values():
    if trtwtrlyr.name() == "OntarioTertiaryWatersheds":
        trtwtrPath = trtwtrlyr

processing.run("qgis:selectbylocation", {"INPUT":trtwtrPath,"PREDICATE":[1],"INTERSECT":tempPath,"METHOD":1,"OUTPUT":tempPath})

for f in trtwtrPath.getSelectedFeatures():
    trtwtr_name = f['NAME']
    trtwtr_name = str(trtwtr_name)
print(trtwtr_name)
trtwtrPath.removeSelection()

#Extract Upper Tier Municipality
for utlyr in QgsProject.instance().mapLayers().values():
    if utlyr.name() == "MUNICIPAL_BOUNDARY_UPPER_TIER_AND_DISTRICT":
        utPath = utlyr

processing.run("qgis:selectbylocation", {"INPUT":utPath,"PREDICATE":[1],"INTERSECT":tempPath,"METHOD":1,"OUTPUT":tempPath})

for f in utPath.getSelectedFeatures():
    ut_name = f['LEGAL_NAME']
#    ut_name = str(ut_name)
print(ut_name)
utPath.removeSelection()

#Extract Lower Tier Municipality
for ltlyr in QgsProject.instance().mapLayers().values():
    if ltlyr.name() == "MUNICIPAL_BOUNDARY_LOWER_AND_SINGLE_TIER":
        ltPath = ltlyr

processing.run("qgis:selectbylocation", {"INPUT":ltPath,"PREDICATE":[1],"INTERSECT":tempPath,"METHOD":1,"OUTPUT":tempPath})

for f in ltPath.getSelectedFeatures():
    lt_name = f['LEGAL_NAME']
#    lt_name = str(lt_name)
print(lt_name)
ltPath.removeSelection()

#Extract Soil Types
for soillyr in QgsProject.instance().mapLayers().values():
    if soillyr.name() == "Soil_Survey_Complex":
        soilPath = soillyr

processing.run("qgis:selectbylocation", {"INPUT":soilPath,"PREDICATE":[0],"INTERSECT":tempPath,"METHOD":1,"OUTPUT":tempPath})

for f in soilPath.getSelectedFeatures():
    soil_types = f['SOIL_NAME1']
    soil_list.append(soil_types)
#    soil_types = str(soil_types)
#soil_types = set(soil_types)
print(soil_list)
soilPath.removeSelection()

#Extract SAR

for sarlyr in QgsProject.instance().mapLayers().values():
    if sarlyr.name() == "SAR_tracked":
        sarPath = sarlyr

processing.run("qgis:selectbylocation", {"INPUT":sarPath,"PREDICATE":[6],"INTERSECT":tempPath,"METHOD":1,"OUTPUT":tempPath})

for f in sarPath.getSelectedFeatures():
    sar = f['ENGLISH_CO']
    sar_list.append(sar)
#    soil_types = str(soil_types)
sar_list = set(sar_list)
print(sar_list)
sarPath.removeSelection()

print("Total Score: " + total_score)
print("Priority: " + priority)
print("Forest Score: " + forest_score + '\n' + "Shoreline: " + natural_shoreline + '\n' + "Kettle Lake: " + kettle_score + '\n' + "Lake: " + lake_score + '\n' + "Plan: " + plan_score + '\n' + "Arch: " + arch_score + '\n' + "ANSI: " + ansi_score + '\n' + "CWS: " + cws_score + '\n' + "Riparian: " + riparian_score + '\n' + "PSW: " + psw_score + '\n' +  "Wetland: " + wetland_score + '\n' +  "PA Adj: " + pa_adjacent_score + '\n' + "100+ac: " + size_score + '\n' +  "SAR: " + sar_score + '\n' +  "WCA: " + wca_score)

data_dict = dict(ARN = np.array(arn), Hectares = np.array(ha), Acres = np.array(acres), Eco_District = np.array(eco_comb), Primary_Watershed = np.array(primwtr_name), Secondary_Watershed = np.array(scdwtr_name), Tertiary_Watershed = np.array(trtwtr_name),CA = np.array(ca_name) , Upper_Tier = np.array(ut_name), Lower_Tier = np.array(lt_name), Soil_Types = np.array(soil_list), SAR_observations = np.array([sar_list]), Forest_Score = np.array(forest_score), Wildlife_Conc_Area = np.array(wca_score), Shoreline_Score = np.array(natural_shoreline), Kettle_Lake_Score = np.array(kettle_score), Lake_Score = np.array(lake_score), Plan_Score = np.array(plan_score), Arch_Score = np.array(arch_score), ANSI = np.array(ansi_score), CWS_Score = np.array(cws_score), Riparian_Score = np.array(riparian_score), PSW_Score = np.array(psw_score), Wetland_Score = np.array(wetland_score), PA_Adjacent_Score = np.array(pa_adjacent_score), Size_Score = np.array(size_score), SAR_Score = np.array(sar_score), Total_Score = np.array(total_score), Priority = np.array(priority))

#Convert the dictionary into a dataframe
df = pd.DataFrame.from_dict(data_dict, orient = 'index')
#df = df.iloc[1: , :]
#df = df.transpose()

df.to_csv("C:/Users/Owner/Desktop/Python Scripts/outputs/nhmp_selected" + arn + ".csv")

print("All done!")

tmEnd = time.time()
print("Run time = {0:.3f} seconds".format(tmEnd-tmStart))