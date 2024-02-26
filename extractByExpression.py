## Input a layer already loaded into the Map Registry (update the name)

layer = QgsProject.instance().mapLayersByName('ORM Planning Area')[0]

# modify the expression .. in this case DESIGNATION = 'Protected Countryside'
pc_params = {
            'EXPRESSION': "DESIGNATION = 'Protected Countryside'",
            'INPUT': layer,
            'OUTPUT': 'memory:'
    }
    
# run the tool and get the output 

pc_layer = processing.run("qgis:extractbyexpression", pc_params)['OUTPUT']

# Set the name of the output layer
pc_layer.setName('Protected Countryside')

# Add the output layer to the Map
QgsProject.instance().addMapLayer(pc_layer)