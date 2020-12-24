# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\GIS2CSV\gis2csv.py
# Compiled at: 2020-03-22 16:15:17
# Size of source mod 2**32: 2704 bytes
import os
from mmqgis import *

class gis2csv:
    __doc__ = ' A class to to convert .shp files into CSV formats using QGIS\n\n    :param Folder_path: A complete path to a folder containing .shp files\n    :type Folder_path: str\n    :param Output_Folder: A complete path to a folder where extracted CSV files will be stored\n    :type Outout_Folder: str\n\n    '

    def __init__(Folder_path, Output_Folder):
        """ gis2csv Constructor method"""
        list_of_files = os.listdir(Folder_path)
        for file in list_of_files:
            if file.endswith('.shp'):
                flag = 0
                file_path = os.path.join(Folder_path, file)
                layer = QgsVectorLayer(file_path, '', 'ogr')
                feat = layer.getFeature(0)
                geom = feat.geometry()
                geomSingleType = QgsWkbTypes.isSingleType(geom.wkbType())
                if geom.type() == QgsWkbTypes.PointGeometry:
                    if geomSingleType:
                        fieldname = [field.name() for field in layer.fields()]
                        if 'x' not in fieldname:
                            pr = layer.dataProvider()
                            pr.addAttributes([QgsField('x', QVariant.Double), QgsField('y', QVariant.Double)])
                            layer.updateFields()
                        feats = layer.getFeatures()
                        fieldname = [field.name() for field in layer.fields()]
                        for feat in feats:
                            geom = feat.geometry()
                            x1 = geom.asPoint()
                            x, y = x1.x(), x1.y()
                            layer.startEditing()
                            layer.changeAttributeValue(feat.id(), fieldname.index('x'), x)
                            layer.changeAttributeValue(feat.id(), fieldname.index('y'), y)
                            layer.commitChanges()

                        QgsVectorFileWriter.writeAsVectorFormat(layer, (os.path.join(Output_Folder, os.path.splitext(file)[0] + '.csv')), 'utf-8', driverName='CSV')
                if geom.type() == QgsWkbTypes.LineGeometry:
                    message = mmqgis_library.mmqgis_geometry_export_to_csv(layer, os.path.join(Output_Folder, os.path.splitext(file)[0] + '_node.csv'), os.path.join(Output_Folder, os.path.splitext(file)[0] + '_attribute.csv'), ',', '\n')


if __name__ == '__main__':
    Folder_path = 'C:\\Users\\KDUWADI\\Desktop\\NREL_Projects\\CIFF-TANGEDCO\\TANGEDCO\\FeedersShapeFiles\\TOWN'
    Output_Folder = 'C:\\Users\\KDUWADI\\Desktop\\NREL_Projects\\CIFF-TANGEDCO\\TANGEDCO\\FeedersExtractedCSVsFromShapeFiles\\TOWN'
    gis2csv(Folder_path, Output_Folder)