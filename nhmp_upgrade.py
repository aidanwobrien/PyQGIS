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
orm_list = []
gb_list = []
sec_list = []
nhiclist = []
sargridlist = []

#Extract Selected Features and ARN
for f in layer.getSelectedFeatures():
    
    
    #get the address, arn and township
    arn = str(f['ARN'])
    address = str(f['Address'])
    address = str(address)
    township = str(f['Township'])
    
    #Get the acres and hectares
    Hectares = str(f['Ha'])
    Acres = str(f['Ac'])
    
    #get the woodland scores and sizes
    woodland_score = str(f['Wood_Scor'])
    woodland_ac = str(f['Wood_Ac_su'])
    
    #get the greenbelt scores and sizes
    gb_score = str(f['GB_Scor'])
    gb_ac = str(f['GB_Ac_sum'])

    #get the orm scores and sizes
    orm_score = str(f['ORM_Scor'])
    orm_ac = str(f['ORM_ac_sum'])
    
    #get the ANSI count, score and sizes
    ansi_count = str(f['ANSI_count'])
    ansi_ac = str(f['ANSI_ac_su'])
    ansi_score = str(f['ANSI_Scor'])
    
    #Get the PSW score and sizes
    psw_score = str(f['PSW_Scor'])
    psw_ac = str(f['PSW_ac_sum'])
    
    #Get the Wetland score and sizes
    wet_score = str(f['Wet_Scor'])
    wet_ac = str(f['Wet_ac_sum'])
    
    #Get the drumlin score and sizes
    drum_score = str(f['Drum_Scor'])
    drum_ac = str(f['drum_ac_su'])
    
    #Get the Kettle Lake Score
    kettle_score = str(f['Kettle_Sco'])
    
    #Get the Archaeological Site Score
    arch_score = str(f['Arch_Scor'])
    
    #Get the size score
    size_score = str(f['Size_Score'])
    
    #Get the PA Adjacencies and scores
    pa_near_score = str(f['PA_near_sc'])
    pa_near_ac = str(f['PA_near_ac'])
    pa_far_score = str(f['PA_far_sco'])
    pa_far_ac = str(f['PA_far_ac_'])
    
    #Get the Wildlife Concentration Area Score
    wca_score = str(f['WCA_Scor'])
    
    #Get the Significant Ecological Community Score
    sec_score = str(f['SEC_Scor'])
    
    #Get the Stream score and length
    stream_score = str(f['Stream_Sco'])
    stream_length = str(f['Stream_len'])
    
    #Get the Species at Risk occurences and scores
    sar_count = str(f['SAR_count'])
    sar_score = f['SAR_Scor']
    
    #Get the ORTA Score
    orta_score = str(f['ORTA_Scor'])
    
    #Get the Lake Scores and Sizes
    lake_score = str(f['Lake_Sco'])
    lake_size = str(f['Lake_Ac_su'])
    
    #Get total scores and priorities
#    weight_score = str(f['Weight_Sco'])
    total_score = f['Total_Scor']
    priority = str(f['Priority'])
    
print("Ha: " + Hectares)
print("Ac: " + Acres)
print("ARN: " + arn)
print("Address: " + address)

tempPath = "C:/Users/Aidan/Desktop/Python Scripts/temp/temp_select" + arn + ".shp"

for nhmplyr in QgsProject.instance().mapLayers().values():
    if nhmplyr.name() == "Upgraded_NHMP_2022_V1":
        parcelPath = nhmplyr

processing.run('native:saveselectedfeatures', {'INPUT': parcelPath,'OUTPUT': tempPath})

#Extract EcoDistrict
for ecolyr in QgsProject.instance().mapLayers().values():
    if ecolyr.name() == "Ecodistrict":
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
print("Ecodistrict" + eco_comb)
ecoPath.removeSelection()

#Extract Conservation Authority
for calyr in QgsProject.instance().mapLayers().values():
    if calyr.name() == "Conservation Authority Areas":
        caPath = calyr

processing.run("qgis:selectbylocation", {"INPUT":caPath,"PREDICATE":[1],"INTERSECT":tempPath,"METHOD":1,"OUTPUT":tempPath})

for f in caPath.getSelectedFeatures():
    ca_name = f['COMMON_NAM']
#    ca_name = str(ca_name)
print("CA: " + ca_name)
caPath.removeSelection()

#Extract Primary Watershed
for primwtrlyr in QgsProject.instance().mapLayers().values():
    if primwtrlyr.name() == "ONT_WSHED_BDRY_PRI_DERIVED":
        primwtrPath = primwtrlyr

processing.run("qgis:selectbylocation", {"INPUT":primwtrPath,"PREDICATE":[1],"INTERSECT":tempPath,"METHOD":1,"OUTPUT":tempPath})

for f in primwtrPath.getSelectedFeatures():
    primwtr_name = f['NAME']
    primwtr_name = str(primwtr_name)
print("Primary Watershed: " + primwtr_name)
primwtrPath.removeSelection()

#Extract Secondary Watershed
for scdwtrlyr in QgsProject.instance().mapLayers().values():
    if scdwtrlyr.name() == "OntarioSecondaryWatersheds":
        scdwtrPath = scdwtrlyr

processing.run("qgis:selectbylocation", {"INPUT":scdwtrPath,"PREDICATE":[1],"INTERSECT":tempPath,"METHOD":1,"OUTPUT":tempPath})

for f in scdwtrPath.getSelectedFeatures():
    scdwtr_name = f['NAME']
    scdwtr_name = str(scdwtr_name)
print("Secondary Watershed: " + scdwtr_name)
scdwtrPath.removeSelection()

#Extract Tertiary Watershed
for trtwtrlyr in QgsProject.instance().mapLayers().values():
    if trtwtrlyr.name() == "OntarioTertiaryWatersheds":
        trtwtrPath = trtwtrlyr

processing.run("qgis:selectbylocation", {"INPUT":trtwtrPath,"PREDICATE":[1],"INTERSECT":tempPath,"METHOD":1,"OUTPUT":tempPath})

for f in trtwtrPath.getSelectedFeatures():
    trtwtr_name = f['NAME']
    trtwtr_name = str(trtwtr_name)
print("Tertiary Watershed: " + trtwtr_name)
trtwtrPath.removeSelection()

#Extract GB Designation
for gblyr in QgsProject.instance().mapLayers().values():
    if gblyr.name() == "Greenbelt Designation":
        gbPath = gblyr

processing.run("qgis:selectbylocation", {"INPUT":gbPath,"PREDICATE":[0],"INTERSECT":tempPath,"METHOD":1,"OUTPUT":tempPath})

for f in gbPath.getSelectedFeatures():
    gb_name = f['DESIG']
    gb_list.append(gb_name)
print("GB_DESIG: ", gb_list)
gbPath.removeSelection()

#Extract ORM Designation
for ormlyr in QgsProject.instance().mapLayers().values():
    if ormlyr.name() == "ORM Land Use Designation":
        ormPath = ormlyr

processing.run("qgis:selectbylocation", {"INPUT":ormPath,"PREDICATE":[0],"INTERSECT":tempPath,"METHOD":1,"OUTPUT":tempPath})

for f in ormPath.getSelectedFeatures():
    orm_name = f['USE_DESIG']
    orm_list.append(orm_name)
print("ORM_DESIGN: ", orm_list)
ormPath.removeSelection()

#Extract Upper Tier Municipality
for utlyr in QgsProject.instance().mapLayers().values():
    if utlyr.name() == "MUNICIPAL_BOUNDARY_UPPER_TIER_AND_DISTRICT":
        utPath = utlyr

processing.run("qgis:selectbylocation", {"INPUT":utPath,"PREDICATE":[1],"INTERSECT":tempPath,"METHOD":1,"OUTPUT":tempPath})

for f in utPath.getSelectedFeatures():
    ut_name = f['LEGAL_NAME']
print("UT: " + ut_name)
utPath.removeSelection()

#Extract Lower Tier Municipality
for ltlyr in QgsProject.instance().mapLayers().values():
    if ltlyr.name() == "MUNICIPAL_BOUNDARY_LOWER_AND_SINGLE_TIER":
        ltPath = ltlyr

processing.run("qgis:selectbylocation", {"INPUT":ltPath,"PREDICATE":[1],"INTERSECT":tempPath,"METHOD":1,"OUTPUT":tempPath})

for f in ltPath.getSelectedFeatures():
    lt_name = f['LEGAL_NAME']
print("LT: " + lt_name)
ltPath.removeSelection()

#Extract Soil Types
for soillyr in QgsProject.instance().mapLayers().values():
    if soillyr.name() == "Soil Survey Complex":
        soilPath = soillyr

processing.run("qgis:selectbylocation", {"INPUT":soilPath,"PREDICATE":[0],"INTERSECT":tempPath,"METHOD":1,"OUTPUT":tempPath})

for f in soilPath.getSelectedFeatures():
    soil_types = f['SOIL_NAME1']
    soil_list.append(soil_types)
soilPath.removeSelection()

#Extract SAR

for sarlyr in QgsProject.instance().mapLayers().values():
    if sarlyr.name() == "SARcentroids3":
        sarPath = sarlyr

processing.run("qgis:selectbylocation", {"INPUT":sarPath,"PREDICATE":[6],"INTERSECT":tempPath,"METHOD":1,"OUTPUT":tempPath})

for f in sarPath.getSelectedFeatures():
    sar_name = str(f['ENGLISH_CO'])
    sar_date = str(f['OBSERVATIO'])
    sar = sar_name + ' - ' + sar_date
    sar_list.append(sar)
sar_list = set(sar_list)
sarPath.removeSelection()

# Extract SAR in 1km Grids 
for nhicgrid in QgsProject.instance().mapLayers().values():
    if nhicgrid.name() == "NHIC 1km Grid":
        nhicpath = nhicgrid

processing.run("qgis:selectbylocation", {"INPUT":nhicpath,"PREDICATE":[0],"INTERSECT":tempPath,"METHOD":1,"OUTPUT":tempPath})

gridPath = "C:/Users/Aidan/Desktop/Python Scripts/temp/grid_select.shp"
sarresults = "C:/Users/Aidan/Desktop/Python Scripts/temp/SARresults.shp"

processing.run('native:saveselectedfeatures', {'INPUT': nhicpath,'OUTPUT': gridPath})

for sargridlyr in QgsProject.instance().mapLayers().values():
    if sargridlyr.name() == "PTS_Observations":
        sargridPath = sargridlyr
        
processing.run('native:clip', {'INPUT': sargridPath, 'OVERLAY': gridPath, 'OUTPUT': sarresults})

for f in nhicpath.getSelectedFeatures():
    nhiccode = str(f['ATLAS_83'])
    nhiclist.append(nhiccode)
nhiclist = set(nhiclist)

sarresults = iface.addVectorLayer("C:/Users/Aidan/Desktop/Python Scripts/temp/SARresults.shp", "clipped", "ogr")

for f in sarresults.getFeatures():
    sar = str(f['ENGLISH_CO'])
    obs = int(f['OBSERVATIO'][:4])
    if obs >= 2002:
        sargridlist.append(sar)
    
sargridlist = set(sargridlist)

if len(sargridlist) == 0:
    sargridscore = 0
if len(sargridlist) == 1:
    sargridscore = 1
if len(sargridlist) in range(2,6):
    sargridscore = 2
if len(sargridlist) in range (5,10):
    sargridscore = 3
if len(sargridlist) >= 10:
    sargridscore = 4
    
QgsProject.instance().removeMapLayers([sarresults.id()])

#Extract Significant Ecological Communities

for seclyr in QgsProject.instance().mapLayers().values():
    if seclyr.name() == "PC_Observation":
        secPath = seclyr
        
processing.run("qgis:selectbylocation", {"INPUT":secPath,"PREDICATE":[6],"INTERSECT":tempPath,"METHOD":1,"OUTPUT":tempPath})

for f in secPath.getSelectedFeatures():
    sec_name = f['General Community Structure']
    sec_list.append(sec_name)
sec_list = set(sec_list)
secPath.removeSelection()

# Distance to ORM

for orm_plan_lyr in QgsProject.instance().mapLayers().values():
    if orm_plan_lyr.name() == "ORM Planning Area":
        orm_plan_path = orm_plan_lyr

orm_near = 'C:/Users/Aidan/Desktop/Python Scripts/temp/nearestjoin.shp'

processing.run("native:joinbynearest", {"INPUT": tempPath, "INPUT_2": orm_plan_path, "OUTPUT": orm_near})

iface.addVectorLayer(orm_near, '', 'ogr')

for orm_near in QgsProject.instance().mapLayers().values():
    if orm_near.name() == "nearestjoin":
        orm_near_path = orm_near

for f in orm_near_path.getFeatures():
    orm_dist = f['distance']
    orm_dist_km = round((orm_dist / 1000),2)
    str_orm_dist_km = str(orm_dist_km) + "km"

to_be_deleted = QgsProject.instance().mapLayersByName('nearestjoin')[0]
QgsProject.instance().removeMapLayer(to_be_deleted.id())

#Distance to Priority Area

for priority_plan in QgsProject.instance().mapLayers().values():
    if priority_plan.name() == "PriorityAreas_ALL":
        priority_plan_path = priority_plan

prior_near = 'C:/Users/Aidan/Desktop/Python Scripts/temp/nearestpriorityjoin.shp'

processing.run("native:joinbynearest", {"INPUT": tempPath, "INPUT_2": priority_plan_path, "OUTPUT": prior_near})

iface.addVectorLayer(prior_near, '', 'ogr')

for prior_near in QgsProject.instance().mapLayers().values():
    if prior_near.name() == "nearestpriorityjoin":
        prior_near_path = prior_near

for f in prior_near_path.getFeatures():
    prior_name = f['layer']
    prior_dist = f['distance']
    prior_dist_km = round((prior_dist / 1000),2)
    str_prior_dist_km = str(prior_dist_km) + "km"
    
prior_to_be_deleted = QgsProject.instance().mapLayersByName('nearestpriorityjoin')[0]
QgsProject.instance().removeMapLayer(prior_to_be_deleted.id())

real_sar_score = sargridscore - sar_score
new_total = total_score + real_sar_score

# Print Scores
#print("Weighted Score: ", weight_score)
print("Total Score: ", new_total)
#print ("Old Total: ", total_score)
#print("Priority: " + priority)
print ("GB_Plan: " + gb_score)
print ("GB_Ac: ", gb_ac, "ac")
print("ORM_Plan: ", orm_score)
print("ORM_Ac: ", orm_ac, "ac")
print("Distance to ORM: " + str_orm_dist_km)
print("ANSI: " + ansi_score)
print("ANSI_Ac: ", ansi_ac)
print("ANSI_Count: ", ansi_count)
print("Woodland Score: " + woodland_score)
print("Woodland_Size: ", woodland_ac, "ac")
print("PSW Score: ", psw_score)
print("PSW_Ac: ", psw_ac, "ac")
print("Wetland Score: ", wet_score)
print("Wetland_Ac: ", wet_ac, "ac")
print("Stream Score: ", stream_score)
print("Stream Length: ", stream_length, 'm')
print("Lake Score: ", lake_score)
print("Lake_Ac: ", lake_size, 'ac')
print("Drumlin Score", drum_score)
print("Drumlin acres", drum_ac)
print("SAR Count", sar_count)
print("SAR Score: ", sar_score)
print ("NHIC Grids: ", nhiclist)
print("List of SAR in 1km Grid: ", sargridlist)
print("# of SAR in 1km Grid: ", len(sargridlist))
print("SAR Grid Score: ", sargridscore)
print("SAR: ", sar_list)
print("ORTA Score", orta_score)
print("Kettle Score: "+ kettle_score)
print("Size Score: " + size_score)
print("Arch: " + arch_score)
print("WCA: ", wca_score)
print ("SEC: ", sec_list)
print ("SEC Score: ", sec_score)
print("PA in 500m: ", pa_near_score)
print("PA acres in 500m: ", pa_near_ac)
print("PA 500-1000m: ", pa_far_score)
print("PA acres in 500-1000m: ", pa_far_ac)
print("Soil Types: ", soil_list)
print("Distance to Priority Area: " + str_prior_dist_km)
print("Closest Priority Area: " + prior_name)

#Convery to a dictionary
data_dict = dict(ARN = np.array(arn), Address = np.array(address), Hectares = np.array(Hectares), Acres = np.array(Acres), Eco_District = np.array(eco_comb), Primary_Watershed = np.array(primwtr_name), Secondary_Watershed = np.array(scdwtr_name), Tertiary_Watershed = np.array(trtwtr_name), GB_DESIG = np.array(gb_list), ORM_DESIG = np.array(orm_list), ORM_Dist = np.array(str_orm_dist_km), Priority_Area_Dist = np.array(str_prior_dist_km), Closest_Priority_Area = np.array(prior_name), CA = np.array(ca_name) , Upper_Tier = np.array(ut_name), Lower_Tier = np.array(lt_name), Soil_Types = np.array(soil_list), SAR_observations = np.array([sar_list]), Woodland_Score = np.array(woodland_score), Woodland_Size = np.array(woodland_ac), Wildlife_Conc_Area = np.array(wca_score), Kettle_Lake_Score = np.array(kettle_score), Lake_Score = np.array(lake_score), Lake_Acres = np.array(lake_size), GB_Score = np.array(gb_score), GB_Size = np.array(gb_ac), ORM_Score = np.array(orm_score), ORM_Size = np.array(orm_ac), Arch_Score = np.array(arch_score), ANSI = np.array(ansi_score), ANSI_Size = np.array(ansi_ac), ANSI_Count = np.array(ansi_count), Stream_Score = np.array(stream_score), Stream_Length = np.array(stream_length), PSW_Score = np.array(psw_score), PSW_Size = np.array(psw_ac), Wetland_Score = np.array(wet_score), Wetland_Size = np.array(wet_ac), PA_Near_Score = np.array(pa_near_score), PA_Near_Size = np.array(pa_near_ac), PA_Far_Score = np.array(pa_far_score), PA_Far_Size = np.array(pa_far_ac), Size_Score = np.array(size_score), SAR_Score = np.array(sargridscore), Total_Score = np.array(new_total))

#Convert the dictionary into a dataframe
df = pd.DataFrame.from_dict(data_dict, orient = 'index')

#Save to a CSV
df.to_csv("C:/Users/Aidan/Desktop/Python Scripts/outputs/nhmp_selected_new" + "_" + address + ".csv")

print("All done!")

tmEnd = time.time()
print("Run time = {0:.3f} seconds".format(tmEnd-tmStart))