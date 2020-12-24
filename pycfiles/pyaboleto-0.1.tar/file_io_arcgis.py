# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\pyabm\file_io_arcgis.py
# Compiled at: 2012-11-18 17:36:44
__doc__ = '\nFunctions for reading coordinate and segment files from ArcGIS, and for\nconverting generated networks into an ArcGIS coverage or shapefile. Also\nhandles writing network statistics fields to a given shapefile\n'
import sys, os, logging
logger = logging.getLogger(__name__)
import arcgisscripting
gp = arcgisscripting.create()

def convertToShpUnits(shapefile, input):
    """Converts input units to match linear units of datasource."""
    inputLength, inputUnits = input.split()
    inputUnits = inputUnits.lower()
    desc = gp.Describe(shapefile)
    shpUnits = desc.SpatialReference.LinearUnitName.lower()
    if shpUnits != inputUnits and shpUnits + 's' != inputUnits:
        logger.error('Shapefile units do not match input units')
        return 1
    else:
        return float(inputLength)


def getFieldType(fieldValue):
    """Returns ArcGIS field type appropriate for the given value"""
    if type(fieldValue) == float:
        return 'DOUBLE'
    if type(fieldValue) == int:
        return 'LONG'
    if type(fieldValue) == str:
        return 'TEXT'


def readNodesFromShp(shapefile):
    """Reads nodes and node weights from a point shapefile."""
    rows = gp.searchCursor(shapefile)
    desc = gp.describe(shapefile)
    nodes = {}
    row = rows.next()
    while row:
        feat = row.GetValue(desc.ShapeFieldName)
        weight = row.getValue('Weight')
        FID = row.getValue('FID')
        pt = feat.getPart(0)
        nodes[FID] = network.Node(FID, pt.x, pt.y, weight)
        row = rows.next()

    del rows
    return nodes


def readNetFromShp(inputShapefile):
    """Reads segs and nodes from the given shapefile"""
    rows = gp.searchCursor(inputShapefile)
    desc = gp.describe(inputShapefile)
    net = network.Network()
    row = rows.next()
    while row:
        feat = row.GetValue(desc.ShapeFieldName)
        ptIDs = [row.getValue('pt1'), row.getValue('pt2')]
        ptWeights = [row.getValue('pt1Weight'), row.getValue('pt2Weight')]
        length = row.getValue('Length')
        FID = row.getValue('FID')
        part = feat.getPart(0)
        part.reset()
        pt = part.next()
        nodes = []
        for n in xrange(2):
            nodes.append(network.Node(ptIDs[n], pt.x, pt.y, ptWeights[n]))
            pt = part.next()

        row = rows.next()
        net.addSeg(network.Seg(FID, nodes[0], nodes[1], length))

    del rows
    return net


def writeFieldToShp(shapefile, fieldValues, field):
    """Writes a field (provided as a dictionary by FID) to a shapefile."""
    fields = gp.listFields(shapefile, field)
    field_found = fields.next()
    if not field_found:
        fieldType = getFieldType(fieldValues.values()[0])
        gp.addField(shapefile, field, fieldType)
    rows = gp.updateCursor(shapefile)
    row = rows.next()
    while row:
        FID = row.getValue('FID')
        try:
            thisFID = fieldValues[FID]
        except KeyError:
            pass
        else:
            row.setValue(field, thisFID)
            rows.updateRow(row)

        row = rows.next()

    del rows
    return 0


def readFieldFromShp(shapefile, field):
    """Reads field values from a shapefile and returns them as a dictionary by FID."""
    rows = gp.searchCursor(shapefile)
    desc = gp.describe(shapefile)
    row = rows.next()
    fieldValues = {}
    while row:
        FID = row.getValue('FID')
        fieldValue = row.getValue(field)
        fieldValues[FID] = fieldValue
        row = rows.next()

    del rows
    return fieldValues


def genShapefile(network, projFile, outputShape):
    """Generates a shapefile from a network class instance."""
    if not os.path.exists(projFile):
        gp.addError(projFile + ' does not exist')
        return 1
    rootDir, fc = os.path.split(outputShape)
    gp.CreateFeatureclass_management(rootDir, fc, 'POLYLINE')
    lengthField = 'Length'
    gp.addfield(outputShape, lengthField, 'FLOAT')
    netIDField = 'netID'
    gp.addfield(outputShape, netIDField, 'LONG')
    pt1Field = 'pt1'
    gp.addfield(outputShape, pt1Field, 'LONG')
    pt2Field = 'pt2'
    gp.addfield(outputShape, pt2Field, 'LONG')
    pt1WeightField = 'pt1Weight'
    gp.addfield(outputShape, pt1WeightField, 'FLOAT')
    pt2WeightField = 'pt2Weight'
    gp.addfield(outputShape, pt2WeightField, 'FLOAT')
    gp.deleteField_management(outputShape, 'Id')
    outDesc = gp.describe(outputShape)
    shapefield = outDesc.ShapeFieldName
    lineArray = gp.createobject('Array')
    point = gp.createobject('Point')
    rows = gp.insertCursor(outputShape)
    row = rows.newrow()
    for segment in network.getEdges():
        node1, node2 = segment.getNodes()
        row.SetValue(netIDField, int(network.getNetID(node1)))
        row.SetValue(lengthField, segment.getWeight())
        row.SetValue(pt1Field, node1.getID())
        row.SetValue(pt2Field, node2.getID())
        row.SetValue(pt1WeightField, node1.getWeight())
        row.SetValue(pt2WeightField, node2.getWeight())
        for n, node in zip(xrange(2), [node1, node2]):
            point.id = n
            point.x = node.getX()
            point.y = node.getY()
            lineArray.add(point)

        row.SetValue(shapefield, lineArray)
        rows.insertrow(row)
        lineArray.removeall()
        row = rows.newrow()

    del rows
    gp.defineprojection_management(outputShape, projFile)
    return 0