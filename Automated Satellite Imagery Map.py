from PyQt5.QtGui import *

parcel = iface.activeLayer()
#parcel = parcels[0]
name = parcel.name()


interest_node = QgsProject.instance().layerTreeRoot().findLayer(parcel)
if interest_node:
    interest_node.setItemVisibilityChecked(2)

parcel_node = QgsProject.instance().layerTreeRoot().findGroup('Land Securement')
if parcel_node:
    parcel_node.setItemVisibilityChecked(2)

basemaps = QgsProject.instance().mapLayersByName('Google Satellite')
basemap = basemaps[0]

roads = QgsProject.instance().mapLayersByName('Roads')
road = roads[0]

bm_node = QgsProject.instance().layerTreeRoot().findGroup('Satellite Imagery')
if bm_node:
  bm_node.setItemVisibilityChecked(True)
  
anthro_node = QgsProject.instance().layerTreeRoot().findGroup('Anthro Features')
if anthro_node:
  anthro_node.setItemVisibilityChecked(True)
  
road_node = QgsProject.instance().layerTreeRoot().findGroup('Roads')
if road_node:
  road_node.setItemVisibilityChecked(True)
  
d = QgsDistanceArea()
#d.setEllipsoid('WGS84')

features = parcel.getFeatures()

for f in features:
    geom = f.geometry()
    sqm = d.measureArea(geom)
    ha = (sqm/10000)
    acres = (ha*2.47105)
    ha = str(round(ha, 2))
    acres = str(round(acres,2))
    print("Hectares: " + ha)
    print("Acres: " + acres)

project = QgsProject.instance()
manager = project.layoutManager()
layoutName = 'Satellite_Layout1'
layouts_list = manager.printLayouts()

# Remove any duplicate layouts
for layout in layouts_list:
    if layout.name() == layoutName:
        manager.removeLayout(layout)
        
layout = QgsPrintLayout(project)
layout.initializeDefaults()
layout.setName(layoutName)
manager.addLayout(layout)

# create map item in the layout

map = QgsLayoutItemMap(layout)
map.setRect(60,60,60,60)

#set the map extent
ms = QgsMapSettings()
ms.setLayers([parcel]) #set layers to be mapped
rect = QgsRectangle(ms.fullExtent())
rect.scale(4)
ms.setExtent(rect)
map.setExtent(rect)


#add map to Layout
layout.addLayoutItem(map)

map.attemptMove(QgsLayoutPoint(5.5, 24, QgsUnitTypes.LayoutMillimeters))
map.attemptResize(QgsLayoutSize(286,165,QgsUnitTypes.LayoutMillimeters))

legend = QgsLayoutItemLegend(layout)
layerTree = QgsLayerTree()
layerTree.addLayer(parcel)
layerTree.addLayer(road)
legend.model().setRootGroup(layerTree)
layout.addLayoutItem(legend)
legend.setFrameEnabled(True)
legend.setFrameStrokeColor(QColor('black'))
legend.attemptMove(QgsLayoutPoint(27,183, QgsUnitTypes.LayoutMillimeters))

scalebar = QgsLayoutItemScaleBar(layout)
scalebar.setStyle('Single Box')
scalebar.setUnits(QgsUnitTypes.DistanceMeters)
scalebar.setNumberOfSegments(3)
scalebar.setNumberOfSegmentsLeft(0)
scalebar.setUnitsPerSegment(100)
scalebar.setLinkedMap(map)
scalebar.setUnitLabel('m')
scalebar.update()
layout.addLayoutItem(scalebar)
scalebar.attemptMove(QgsLayoutPoint(137,194,QgsUnitTypes.LayoutMillimeters))

map_info = QgsLayoutItemLabel(layout)
map_info.setText('Prepared by ORMLT on $CURRENT_DATE(yyyy-MM-dd). For illustrative purposes only. Some data may be omitted.')
map_info.currentText()
map_info.setFont(QFont('Arial', 7))
map_info.adjustSizeToText()
layout.addLayoutItem(map_info)
map_info.attemptMove(QgsLayoutPoint(226,197, QgsUnitTypes.LayoutMillimeters))
map_info.attemptResize(QgsLayoutSize(56.645, 9.398, QgsUnitTypes.LayoutMillimeters))

title = QgsLayoutItemLabel(layout)
title.setText(name + "\n" + 'Acres: ' + acres + ', ' + 'Hectares: ' + ha)
title.setFont(QFont('Arial', 16))
title.adjustSizeToText()
layout.addLayoutItem(title)
title.attemptMove(QgsLayoutPoint(95, 3, QgsUnitTypes.LayoutMillimeters))
title.attemptResize(QgsLayoutSize (196,17, QgsUnitTypes.LayoutMillimeters))
title.setFrameEnabled(True)
title.setFrameStrokeColor(QColor('black'))
title.setHAlign(Qt.AlignCenter)
title.setVAlign(Qt.AlignCenter)

ormlt = QgsLayoutItemPicture(layout)
ormlt.setPicturePath("C:/Users/Aidan/Desktop/ormltlogo.jpg")
layout.addLayoutItem(ormlt)
ormlt.attemptResize(QgsLayoutSize(81,17, QgsUnitTypes.LayoutMillimeters))
ormlt.attemptMove(QgsLayoutPoint(5.5,2.850, QgsUnitTypes.LayoutMillimeters))

north = QgsLayoutItemPicture(layout)
north.setPicturePath("C:/PROGRA~1/QGIS3~1.16/apps/qgis/./svg//arrows/NorthArrow_04.svg")
layout.addLayoutItem(north)
north.attemptResize(QgsLayoutSize(17, 14, QgsUnitTypes.LayoutMillimeters))
north.attemptMove(QgsLayoutPoint(102, 192, QgsUnitTypes.LayoutMillimeters))

