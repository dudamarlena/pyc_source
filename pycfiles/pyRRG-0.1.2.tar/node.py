# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\pyrrd\node.py
# Compiled at: 2014-01-13 03:56:47
__doc__ = "\nThis module's classes are used to represent RRD data in XML format. The mapper\nmodule uses this format to establish a relationship between RRD files (and\ntheir exports) and Python objects.\n"

class XMLNode(object):
    """
    A base class. Not used directly.
    """

    def __init__(self, tree, attribute_names):
        self.tree = tree
        self.attributes = {}
        for (name, cast, default) in attribute_names:
            try:
                value = cast(self.getAttribute(name))
            except ValueError:
                value = default

            if not value:
                value = default
            self.attributes[name] = value

    def getAttribute(self, attrName):
        """
        """
        node = self.tree.find(attrName)
        if node != None:
            return node.text.strip()
        else:
            raise ValueError()
            return


class DSXMLNode(XMLNode):
    """
    An object abstraction for the <ds> node in the XML RRD export. This is a
    child of the <rrd> node, and thus this class is used in the RRDXMLNode
    class.

    Currently provides no featres beyond those of the base XML node class.
    """


class CDPPrepXMLNode(XMLNode):
    """
    An object abstraction for the <cd_prep> node in the XML RRD export. The
    <cd_prep> nodes are children node of an <rra> node.
    """

    def __init__(self, node):
        self.ds = []
        dsAttributes = [
         (
          'primary_value', float, 0.0),
         (
          'secondary_value', float, 0.0),
         (
          'value', float, 0.0),
         (
          'unknown_datapoints', int, 0)]
        for ds in node.findall('ds'):
            self.ds.append(DSXMLNode(ds, dsAttributes))


class DatabaseNode(XMLNode):
    """
    An object abstraction for the <database> node in the XML RRD export.
    Currently unimplemented.
    """

    def __init__(self, node):
        super(DatabaseNode, self).__init__(node, [])
        self.row = []


class RRAXMLNode(XMLNode):
    """
    An object abstraction for the <rra> node in the XML RRD export. The <rra>
    nodes are children of the <rrd> node.
    """

    def __init__(self, tree, attributes, includeData=False):
        super(RRAXMLNode, self).__init__(tree, attributes)
        self.database = None
        xff = self.tree.find('params').find('xff')
        if xff != None:
            xff = float(xff.text)
            self.attributes['xff'] = xff
        self.cdp_prep = CDPPrepXMLNode(self.tree.find('cdp_prep'))
        if includeData:
            db = self.tree.get('database')
            self.database = DatabaseNode(db)
        return

    def getAttribute(self, attrName):
        """
        """
        if attrName.lower() == 'xff':
            return self.tree.findtext('params/xff').strip()
        else:
            return super(RRAXMLNode, self).getAttribute(attrName)


class RRDXMLNode(XMLNode):
    """
    An object abstraction for the <rrd> node in the XML RRD export. This is the
    top-level node in the XML RRD export.
    """

    def __init__(self, tree, includeData=False):
        attributes = [
         (
          'version', int, 0),
         (
          'step', int, 300),
         (
          'lastupdate', int, 0)]
        super(RRDXMLNode, self).__init__(tree, attributes)
        dsAttributes = [
         (
          'name', str, ''),
         (
          'type', str, 'GAUGE'),
         (
          'minimal_heartbeat', int, 300),
         (
          'min', int, 'NaN'),
         (
          'max', int, 'NaN'),
         (
          'last_ds', int, 0),
         (
          'value', float, 0.0),
         (
          'unknown_sec', int, 0)]
        rraAttributes = [
         (
          'cf', str, 'AVERAGE'),
         (
          'pdp_per_row', int, 0)]
        self.ds = []
        self.rra = []
        for ds in self.getDataSources():
            self.ds.append(DSXMLNode(ds, dsAttributes))

        for rra in self.getRRAs():
            self.rra.append(RRAXMLNode(rra, rraAttributes, includeData))

    def getDataSources(self):
        """
        """
        return self.tree.findall('ds')

    def getRRAs(self):
        """
        """
        return self.tree.findall('rra')