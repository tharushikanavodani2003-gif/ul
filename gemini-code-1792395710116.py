import os
from qgis.core import (
    QgsProject, 
    QgsVectorLayer, 
    QgsRasterLayer, 
    QgsSymbol, 
    QgsRendererRange, 
    QgsGraduatedSymbolRenderer, 
    QgsCategorizedSymbolRenderer, 
    QgsRendererCategory,
    QgsPalLayerSettings, 
    QgsVectorLayerSimpleLabeling
)

# ==========================================
# 0. SET YOUR FILE PATHS HERE
# ==========================================
# Oyaage data files thiyena thana paths mekata denna:
study_area_path = "C:/path/to/your/study_area.shp"
forest_layer_path = "C:/path/to/your/forest_layer.shp"
flood_layer_path = "C:/path/to/your/flood_zones.shp"
crop_layer_path = "C:/path/to/your/crops_landuse.shp"

# ==========================================
# 1. LOAD STUDY AREA & SETUP LABELS (GND / DSD)
# ==========================================
study_layer = QgsVectorLayer(study_area_path, "Study Area", "ogr")
if study_layer.isValid():
    QgsProject.instance().addMapLayer(study_layer)
    
    # Enable Labels (Gramadewini / DSD wise name display)
    settings = QgsPalLayerSettings()
    settings.readFromLayer(study_layer)
    settings.enabled = True
    # 'NAME' column eka oyaage shapefile eke name eka thiyena column name eken maru karanna
    settings.fieldName = "NAME" 
    
    textFormat = settings.format()
    textFormat.setSize(10)
    settings.setFormat(textFormat)
    
    layer_settings = QgsVectorLayerSimpleLabeling(settings)
    study_layer.setLabeling(layer_settings)
    study_layer.setLabelsEnabled(True)
    study_layer.triggerRepaint()
    print("Study Area loaded and labeled successfully!")
else:
    print("Error loading Study Area layer. Check path.")

# ==========================================
# 2. POPULATION DENSITY (Graduated Symbology)
# ==========================================
# Population density data thiyena layer eka load karala colors wenas kirima
pop_layer_path = "C:/path/to/your/population_density.shp"
pop_layer = QgsVectorLayer(pop_layer_path, "Population Density", "ogr")
if pop_layer.isValid():
    QgsProject.instance().addMapLayer(pop_layer)
    
    # Graduated renderer setup ('pop_dens' column eka use karamin)
    field_name = "pop_dens"
    # Classes / Ranges hadanna (Low to High colors: Yellow to Red)
    ranges = [
        QgsRendererRange(0, 100, QgsSymbol.defaultSymbol(pop_layer.geometryType()), "Low (<100)"),
        QgsRendererRange(100, 500, QgsSymbol.defaultSymbol(pop_layer.geometryType()), "Medium (100-500)"),
        QgsRendererRange(500, 5000, QgsSymbol.defaultSymbol(pop_layer.geometryType()), "High (>500)")
    ]
    renderer = QgsGraduatedSymbolRenderer(field_name, ranges)
    pop_layer.setRenderer(renderer)
    pop_layer.triggerRepaint()
    print("Population density graduated styling applied!")

# ==========================================
# 3. LAND & AGRICULTURE (Categorized Symbology)
# ==========================================
crop_layer = QgsVectorLayer(crop_layer_path, "Land and Agriculture", "ogr")
if crop_layer.isValid():
    QgsProject.instance().addMapLayer(crop_layer)
    
    # 'landuse' or 'all crops' column eka base karala categorise kirima
    category_field = "landuse" 
    unique_values = crop_layer.uniqueValues(crop_layer.fields().indexFromName(category_field))
    
    categories = []
    for val in unique_values:
        symbol = QgsSymbol.defaultSymbol(crop_layer.geometryType())
        category = QgsRendererCategory(val, symbol, str(val))
        categories.append(category)
        
    cat_renderer = QgsCategorizedSymbolRenderer(category_field, categories)
    crop_layer.setRenderer(cat_renderer)
    crop_layer.triggerRepaint()
    print("Land & Agriculture categorized styling applied!")

# ==========================================
# 4. PHYSICAL ENVIRONMENT & DRAINAGE ISSUES
# ==========================================
forest_layer = QgsVectorLayer(forest_layer_path, "Forest Cover", "ogr")
if forest_layer.isValid():
    QgsProject.instance().addMapLayer(forest_layer)
    # Green color for forest
    forest_layer.renderer().symbol().setColor(QColor(34, 139, 34))
    forest_layer.triggerRepaint()

flood_layer = QgsVectorLayer(flood_layer_path, "Flood Risk Zones", "ogr")
if flood_layer.isValid():
    QgsProject.instance().addMapLayer(flood_layer)
    # Transparent Blue for flood risk zones
    flood_layer.renderer().symbol().setColor(QColor(0, 191, 255, 120))
    flood_layer.triggerRepaint()

print("All layers loaded and configured successfully!")