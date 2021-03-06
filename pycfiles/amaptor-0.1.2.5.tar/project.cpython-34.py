# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\dsx.AD3\Code\amaptor\amaptor\classes\project.py
# Compiled at: 2017-03-17 20:48:32
# Size of source mod 2**32: 13548 bytes
import os, logging
log = logging.getLogger('amaptor')
import arcpy
from amaptor.version_check import PRO, ARCMAP, mapping, mp
from amaptor.classes.map import Map
from amaptor.classes.layout import Layout
from amaptor.classes.map_frame import MapFrame
from amaptor.constants import _TEMPLATES, _PRO_BLANK_LAYOUT
from amaptor.functions import _import_mxd_to_new_pro_project
from amaptor.errors import *

class Project(object):
    __doc__ = '\n\t\tAn ArcGIS Pro Project or an ArcMap map document - maps in ArcGIS Pro and data frames in ArcMap are Map class attached to this project\n\t\tAccess to the underlying object is provided using name ArcGISProProject and ArcMapDocument\n\t'

    def __init__(self, path):
        self.maps = []
        self.layouts = []
        self.path = None
        self.map_document = None
        self.arcgis_pro_project = None
        self.primary_document = None
        if PRO:
            if path == 'CURRENT':
                self.path = 'CURRENT'
            else:
                if path.endswith('aprx'):
                    self.path = path
                else:
                    if path.endswith('mxd'):
                        self.path = _import_mxd_to_new_pro_project(path)
                    else:
                        raise ValueError('Project or MXD path not recognized as an ArcGIS compatible file (.aprx or .mxd)')
            self._pro_setup()
        else:
            if path == 'CURRENT':
                self.path = 'CURRENT'
                self._arcmap_setup()
            else:
                if path.endswith('mxd'):
                    self.path = path
                    self._arcmap_setup()
                else:
                    if path.endswith('aprx'):
                        raise MapNotImplementedError('Support for Pro Projects in ArcMap is not possible. Please provide an MXD template to work with.')
                    else:
                        raise ValueError('Project or MXD path not recognized as an ArcGIS compatible file (.aprx or .mxd)')
        if path == 'CURRENT':
            self.path = self.primary_document.filePath

    def _pro_setup(self):
        """
                        Sets up the data based on the ArcGIS Pro Project. Only called if working with arcpy.mp and after any needed
                        conversion from Map Document to Pro Project is done.
                :return: None
                """
        self.arcgis_pro_project = mp.ArcGISProject(self.path)
        self.primary_document = self.arcgis_pro_project
        for l_map in self.arcgis_pro_project.listMaps():
            self.maps.append(Map(self, l_map))

        for layout in self.primary_document.listLayouts():
            self.layouts.append(Layout(layout, self))

        for map in self.maps:
            map._index_frames()

    def _arcmap_setup(self):
        """
                        Sets up data based on an ArcGIS Map Document. Only called if working with arcpy.mapping and after any
                        needed conversion from Pro Project to map docusment is done (can we go that way?)
                :return: None
                """
        self.map_document = mapping.MapDocument(self.path)
        self.primary_document = self.map_document
        for l_map in mapping.ListDataFrames(self.map_document):
            self.maps.append(Map(self, l_map))

    def list_maps(self):
        """
                        Provided to give a similar interface to ArcGIS Pro - Project.maps is also publically accessible
                :return:
                """
        return self.maps

    def find_layer(self, path, find_all=True):
        """
                        Finds a layer in all maps by searching for the path. By default finds all, but can find just the first one too
                :param path: the full path of the data source for the layer
                :param find_all: When True, reutrns a list of amaptor.Map instances that match. When false, returns only the first match
                :return: list of amaptor.map instances or a single amaptor.map instance.
                """
        layers = []
        for map in self.maps:
            try:
                new_layers = map.find_layer(path=path, find_all=find_all)
            except LayerNotFoundError:
                continue

            if find_all:
                layers += new_layers
            else:
                return new_layers

        if len(layers) == 0:
            raise LayerNotFoundError()
        return layers

    @property
    def active_map(self):
        """
                        Returns the active map object or data frame as determined by get_active_map()
                :return:
                """
        return self.get_active_map()

    @property
    def map_names(self):
        """
                        A convenience function to get a list of map names
                :return:
                """
        return [l_map.name for l_map in self.maps]

    def find_map(self, name):
        """
                        Given a map name, returns the map object or raises MapNotFoundError
                :param name: name of map to find.
                :return: amaptor.Map instance
                """
        for l_map in self.maps:
            if l_map.name == name:
                return l_map
        else:
            raise MapNotFoundError(name)

    def check_map_name(self, name):
        """
                        Checks to see if the project or map document already has a map or data frame with a given name.
                        Since names must be unique in ArcGIS Pro, this code helps check before adding new maps
                :param name: name of map to check for
                :return: None. Raises an error if name is taken
                """
        try:
            self.find_map(name)
            raise MapExists(name)
        except MapNotFoundError:
            pass

    def new_map(self, name, template_map=os.path.join(_TEMPLATES, 'arcmap', 'pro_import_map_template.mxd'), template_df_name='_rename_template_amaptor'):
        """
                        PRO ONLY. Creates a new map in the current project using a hack (importing a blank map document, and renaming data frame)
                        Warning: Only works in Pro due to workaround.
                :param name: The name to give the imported map
                :param template_map: The map document to import. If we're just going with a blank new map, leave as default. To
                                                        import some other template as your base, provide a path to a document importable to ArcGIS Pro'
                                                        .importDocument function for projects.
                :param template_df_name: The current name of the imported map document for renaming. Only needs to be set if template_map is overridden
                :return: amaptor.Map instance - also added to the map document, but returned for immediate use.
                """
        if ARCMAP:
            raise MapNotImplementedError("ArcMap doesn't suppport adding data frames to map documents from Python")
        self.check_map_name(name)
        self.primary_document.importDocument(template_map)
        for l_map in self.primary_document.listMaps():
            if l_map.name == template_df_name:
                l_map.name = name
                new_map = Map(self, l_map)
                self.maps.append(new_map)
                return new_map
        else:
            raise MapNotFoundError('Map was inserted, but could not be found after insertion. If you provided a customtemplate, check that the name you provided for template_df_name matches the name of the data frame you want to use from the map document.')

    def check_layout_name(self, name):
        """
                        PRO ONLY. Given the name of a layout, confirms it doesn't exist and raised amaptor.LayoutExists if it's found
                :param name: the case sensitive name of an existing layout to find
                :return: None. Raises amaptor.LayoutExists if layout with name exists.
                """
        try:
            self.find_layout(name)
            raise LayoutExists(name)
        except LayoutNotFoundError:
            pass

    def find_layout(self, name):
        """
                        PRO ONLY. Given a layout name, returns the amaptor.Layout object or raises LayoutNotFoundError
                :param name: the name of the layout to find.
                :return: amaptor.Layout instance with given name.
                """
        for layout in self.layouts:
            if layout.name == name:
                return layout
        else:
            raise LayoutNotFoundError(name)

    def new_layout(self, name, template_layout=_PRO_BLANK_LAYOUT, template_name='_pro_blank_layout_template'):
        """
                        PRO ONLY. Adds a new layout to an ArcGIS Pro Project by importing a saved blank layout. Alternatively,
                         you can provide an importable layout document (.pagx) for ArcGIS Pro, and then provide that layout's name
                         as template_name so that it can be renamed, and the provided template will be used instead of a blank.
                :param name: The name to give the new layout
                :param template_layout: The template to use for creating the layout (an ArcGIS Pro .pagx file).
                        If none is provided, uses a blank template
                :param template_name: The name of the layout in the template. Only define this value if you also provide a new
                        template layout and the name should match the layout name in the template. This parameter is used to find
                        the inserted template and rename it. Strange things will happen if this value does not match the name of the
                        layout in the template_layout.
                :return: amaptor.Layout instance. This layout will already have been added to the project, but is returned for
                        convenience.
                """
        if ARCMAP:
            raise MapNotImplementedError("ArcMap doesn't suppport adding data frames to map documents from Python")
        self.primary_document.importDocument(template_layout)
        for layout in self.primary_document.listLayouts():
            if layout.name == template_name:
                layout.name = name
                new_layout = Layout(layout, self)
                self.layouts.append(new_layout)
                return new_layout
        else:
            raise LayoutNotFoundError("Layout was inserted, but could not be found after insertion. If you provided a customtemplate, check that the name you provided for template_name matches the name of the original mxd file from which you derived the layout you're importing")

    def get_active_map(self, use_pro_backup=True):
        """
                        Emulates functionality of arcpy.mapping(mxd).activeDataFrame. In ArcMap, it returns the amaptor.Map object
                        that corresponds to that active Data Frame. In Pro, which doesn't have the concept of active maps, it by
                        default returns the first map in the document. If use_pro_backup is set to False, it will instead
                        raise amaptor.MapNotImplementedError
                :param use_pro_backup: When True, it uses the first map in the ArcGIS Pro project, since Pro doesn't have a way
                 to get the active map.
                :return: amaptor.Map instance
                """
        if ARCMAP:
            for each_map in self.maps:
                if each_map.name == self.primary_document.activeDataFrame.name:
                    return each_map

        else:
            if use_pro_backup:
                return self.maps[0]
            raise MapNotImplementedError('ArcGIS Pro does not provide an interface to the active map')

    def save(self):
        """
                        Saves the project or map document in place.
                :return: None
                """
        self.primary_document.save()

    def save_a_copy(self, path):
        """
                        Saves the project or map document to the provided path.
                :param path: the new path to save the copy of the document to.
                :return: None
                """
        self.primary_document.saveACopy(path)

    def to_package(self, output_file, summary, tags, **kwargs):
        """
                        Though it's not normally a mapping method, packaging concepts need translation between the two versions, so
                        we've included to_package for maps and projects. In ArcGIS Pro, project.to_package will create a Project Package
                        and map.to_package will create a map package. In ArcMap, both will create a map package. Extra **kwargs beyond
                        output path are only passed through to Pro Package command, not to map packages. To pass kwargs through to a map
                        package, use a map object's to_package method.
                :param output_file: the path to output the package to
                :param kwargs: dictionary of kwargs to pass through to project packaging in Pro.
                :return: None
                """
        log.warning('Warning: Saving project to export package')
        self.save()
        if PRO:
            arcpy.PackageProject_management(self.path, output_file, summary=summary, tags=tags, **kwargs)
        else:
            arcpy.PackageMap_management(self.path, output_file, summary=summary, tags=tags)

    def replace_text(self, text, replacement):
        """
                        Given a string and a replacement value, finds all instances (in the current map document or project)
                        of that text in text elements and titles, and replaces those instances with the new value.
                        Useful for creating your own variables like {species} or {field_id} in map templates.
                        Careful when using this - in Pro, it will search all Layouts and replace the string.
                        If you are concerned and want single layout behavior, use the same function on the Layout class.
                :param text:
                :param replacement:
                :return:
                """
        if ARCMAP:
            for elm in arcpy.mapping.ListLayoutElements(self.primary_document, 'TEXT_ELEMENT'):
                elm.text = elm.text.replace(text, replacement)

        else:
            for layout in self.layouts:
                layout.replace_text(text, replacement)