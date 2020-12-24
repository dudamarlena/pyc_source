# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: C:\Users\dsx\Code\amaptor\amaptor\classes\layer.py
# Compiled at: 2018-05-18 17:01:18
# Size of source mod 2**32: 12027 bytes
import os, logging
log = logging.getLogger('amaptor.layer')
import arcpy
from amaptor.version_check import PRO, ARCMAP, mapping, mp
from amaptor.errors import NotSupportedError, EmptyFieldError, LayerNotFoundError
from amaptor.functions import get_workspace_type, get_workspace_factory_of_dataset
from amaptor.constants import _BLANK_FEATURE_LAYER, _BLANK_RASTER_LAYER

class Layer(object):
    """Layer"""

    def __init__(self, layer_object_or_file, name=None, map_object=None, template_layer=None):
        """
                        Create a Layer object by providing an ArcGIS layer instance, an ArcGIS layer file, or a data source.

                :param layer_object_or_file: an actual instance of a layer object, a valid data source (feature class, raster, etc) or a layer file path (layer file paths work best in Pro, which supports multiple layers in a single file - for cross platform usage, open the layer file and get the Layer object you need, then make an amaptor layer with that)
                :param name: used when loading from a file in Pro to select the layer of interest
                :param map_object: the map this layer belongs to - optional but used when updating symbology in ArcMap - not necessary if you plan to use map.add_layer or map.insert_layer before updating symbology
                :param template_layer: This is used in Pro when constructing a layer from a data source - it will start automatically
                                        with this layer's properties, symbology, etc. In future versions, we hope to have it autodetect the most appropriate
                                        template layer that comes with amaptor, but for now, this is an option so that you can get the right properties
                                        immediately.
                """
        self.init = False
        self.layer_object = None
        if PRO:
            if isinstance(layer_object_or_file, arcpy._mp.Layer):
                self.layer_object = layer_object_or_file
        if ARCMAP:
            if isinstance(layer_object_or_file, mapping.Layer):
                self.layer_object = layer_object_or_file
            else:
                if PRO:
                    if layer_object_or_file.endswith('.lyr') or layer_object_or_file.endswith('.lyrx'):
                        layer_file = mp.LayerFile(layer_object_or_file)
                        for layer in layer_file.listLayers():
                            self.layer_object = layer
                            if name:
                                if layer.name == name:
                                    break

                    else:
                        desc = arcpy.Describe(layer_object_or_file)
                        if template_layer or desc.dataType in ('FeatureClass', 'ShapeFile'):
                            layer_file = _BLANK_FEATURE_LAYER
                        else:
                            if desc.dataType in ('RasterDataset', 'RasterBand'):
                                layer_file = _BLANK_RASTER_LAYER
                            else:
                                raise NotSupportedError("This type of dataset isn't supported for initialization in amaptor via ArcGIS Pro")
                else:
                    layer_file = template_layer
                    avail_layer = arcpy.mp.LayerFile(layer_file)
                    arcgis_template_layer = avail_layer.listLayers()[0]
                if arcgis_template_layer is None:
                    raise LayerNotFoundError('No layer available for copying from layer file')
                else:
                    if not arcgis_template_layer.supports('DATASOURCE'):
                        raise NotSupportedError("Provided layer file doesn't support accessing or setting the data source")
                    self.layer_object = arcgis_template_layer
                    self._set_data_source(layer_object_or_file)
                    self.name = desc.name
                    del desc
        else:
            self.layer_object = mapping.Layer(layer_object_or_file)
        self.map = map_object

    @property
    def name(self):
        return self.layer_object.name

    @name.setter
    def name(self, value):
        self.layer_object.name = value

    @property
    def data_source(self):
        if not self.layer_object.supports('DATASOURCE'):
            raise NotSupportedError("Provided layer doesn't support accessing or setting the data source")
        return self.layer_object.dataSource

    @data_source.setter
    def data_source(self, new_source):
        self._set_data_source(new_source)

    def _set_data_source(self, new_source):
        if not self.layer_object.supports('DATASOURCE'):
            raise NotSupportedError("Provided layer file doesn't support accessing or setting the data source")
        else:
            desc = arcpy.Describe(new_source)
            if desc.extension:
                if desc.extension != '':
                    name = '{}.{}'.format(desc.baseName, desc.extension)
            else:
                name = desc.baseName
            if PRO:
                old_connection_properties = self.layer_object.connectionProperties
                new_factory_type = get_workspace_factory_of_dataset(new_source)
                self.layer_object.updateConnectionProperties(old_connection_properties, {'dataset':desc.name, 
                 'connection_info':{'database': desc.path}, 
                 'workspace_factory':new_factory_type})
            else:
                self.layer_object.replaceDataSource(desc.path, get_workspace_type(new_source), name)

    @property
    def symbology(self):
        """
                        Access symbology properties. If running from ArcMap and layer symbologyType is "OTHER" raises NotSupportedError
                        to flag that the symbology is unreadable and unreturnable. No equivalent check in Pro.
                :return:
                """
        if ARCMAP:
            if self.layer_object.symbologyType == 'OTHER':
                raise NotSupportedError('Unsupported symbology type in ArcMap')
        return self.layer_object.symbology

    @symbology.setter
    def symbology(self, symbology):
        """
                        Updates layer symbology based on copying from:
                         1) amaptor Layer object
                         2) arcpy.mapping/arcpy.mp Layer objects
                         3) A path to a layer file - if you pass in a string, it will be assumed to be a path to a layer file and symbology will be loaded from the file
                         4) symbology object. Symbology objects only exist in Pro, so take care when using them for cross-platform support.

                        raises NotSupportedError if the provided object cannot be copied from. If you wish to copy symbology from a Layer
                        file, open it and retrieve the appropriate Layer object and pass it here.

                        In ArcMap, it *may* require that the current layer and the symbology object (of whatever form) share the same
                        type of renderer (for example, on a raster, that they both use a classified renderer or both use a stretched
                        renderer, etc).

                        IMPORTANT: If you are setting symbology using this method in ArcMap, you MUST attach an amaptor.Map instance
                        representing the Data Frame that this layer is within as this_layer.map *before* doing any symbology operations.
                        amaptor functions handle this by default when finding layers and inserting them,  but if you are creating
                        your own amaptor layer objects and haven't yet inserted it into a map, you'll need to set the `map` attribute

                        ```
                                my_layer = amaptor.Layer("my_layer_name", template_layer="some_layer_file.lyr")
                                my_layer.map = my_map  # set the map attribute so it knows what data frame to use. Should be an amaptor.Map object, not an actual data frame.
                                my_layer.symbology = symbol_layer # copies symbology from symbol_layer to my_layer
                        ```
                        The step `my_layer.map` isn't necessary in the instance that you use map.add_layer or map.insert_layer before updating symbology

                :param symbology: Symbology can be a symbology object or a layer to copy it from, or a path to a layer file on disk
                :return:
                """
        if PRO:
            if isinstance(symbology, arcpy._mp.Symbology):
                new_symbology = symbology
            else:
                if isinstance(symbology, arcpy._mp.Layer) or isinstance(symbology, Layer):
                    new_symbology = symbology.symbology
                else:
                    if type(symbology) == str:
                        if not os.path.exists(symbology):
                            raise RuntimeError('Provided symbology was a string, but is not a valid file path. Please provide a valid file path, layer object, or symbology object')
                        new_symbology = arcpy.mp.LayerFile(symbology).symbology
                    else:
                        raise NotSupportedError('Cannot retrieve symbology from the object provided. Accepted types are amaptor.Layer, arcpy.mp.Symbology, and arcpy.mp.Layer. You provided {}'.format(type(symbology)))
            self.layer_object.symbology = new_symbology
        else:
            from amaptor.classes.map import Map
        if self.map is None or not isinstance(self.map, Map):
            raise EmptyFieldError('map', 'Layer is not attached to an amaptor.Map instance - cannot change symbology. See documentation.')
        if isinstance(symbology, Layer):
            source_data = symbology.layer_object
        else:
            if isinstance(symbology, arcpy.mapping.Layer):
                source_data = symbology
            else:
                if type(symbology) in (str, unicode):
                    if not os.path.exists(symbology):
                        raise RuntimeError('Provided symbology was a string, but is not a valid file path. Please provide a valid file path or layer object')
                    source_data = arcpy.mapping.Layer(symbology)
                else:
                    raise NotSupportedError('Cannot retrieve symbology from the object provided. Accepted types are amaptor.Layer and arcpy.mapping.Layer. You provided {}'.format(type(symbology)))
            if self.layer_object.symbologyType != source_data.symbologyType:
                log.warning('Trying to apply symboloy with a renderer of type {} to a layer with renderer of type {} - thismay fail in ArcMap'.format(source_data.symbologyType, self.layer_object.symbologyType))
            arcpy.mapping.UpdateLayer(data_frame=(self.map.map_object), update_layer=(self.layer_object),
              source_layer=source_data,
              symbology_only=True)

    def __getter__(self, key):
        """
                        Helps this to be a standin where layers were used before because it will behave as expected for attributes
                        of arcpy layers.
                :return:
                """
        return getattr(self.layer_object, key)

    def __setter__(self, key, value):
        """
                        Helps this to be a standin where layers were used before because it will behave as expected for attributes
                        of arcpy layers.
                :return:
                """
        return setattr(self.layer_object, key, value)