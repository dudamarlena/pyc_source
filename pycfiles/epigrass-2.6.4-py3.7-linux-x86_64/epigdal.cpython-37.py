# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/Epigrass/epigdal.py
# Compiled at: 2020-04-04 10:01:37
# Size of source mod 2**32: 27178 bytes
"""
This module uses the GDAL and OGR Library to read maps in various formats and
export the results of Epigrass simulations to the formats supported by these libraries

copyright 2007,2012 by Flavio Codeco Coelho
Licensed under the GPL.
"""
from __future__ import absolute_import
from __future__ import print_function
import locale, os, pylab
from osgeo import ogr, osr, gdal
from xml.dom import minidom, Node
from matplotlib.colors import rgb2hex, LogNorm
from matplotlib.colors import Normalize
from matplotlib import cm
from numpy import array
import geopandas as gpd
from zipfile import ZipFile
import json, six
from six.moves import range
from six.moves import zip

class NewWorld:

    def __init__(self, filename, namefield, geocfield, outdir='.'):
        """
        Open Shapefile, and load it into a geopandas dataframe
        :param filename:
        :param namefield: name of the field containing locality name
        :param geocfield: name of the field containing geocode
        :param outdir: directory for data output
        """
        self.geocfield = geocfield
        self.namefield = namefield
        self.outdir = outdir
        self.map = gpd.read_file(filename)


class World:

    def __init__(self, filename, namefield, geocfield, outdir='.'):
        """
        Instantiate a world object.
        Filename points to a file supported by OGR
        namefield - name of the field containing polygon name
        geocfield - name of the field containing geocode
        """
        self.geocfield = geocfield
        self.namefield = namefield
        self.outdir = outdir
        try:
            self.ds = ogr.Open(filename)
        except AttributeError:
            raise AttributeError('Could not open the Shapefile {}. Please check if the path is correct.'.format(filename))

        self.name = self.ds.GetName()
        self.driver = self.ds.GetDriver()
        layer = self.ds.GetLayer()
        if layer.GetSpatialRef() is None:
            self.in_spatial_ref = osr.SpatialReference()
            self.in_spatial_ref.ImportFromEPSG(4326)
        else:
            epsg = layer.GetEPSG()
            self.in_spatial_ref = osr.SpatialReference()
            self.in_spatial_ref.ImportFromEPSG(epsg)
        self.out_spatial_ref = osr.SpatialReference()
        self.out_spatial_ref.ImportFromEPSG(4326)
        self.coord_trans = osr.CoordinateTransformation(self.in_spatial_ref, self.out_spatial_ref)
        self.centroids = []
        self.centdict = {}
        self.geomdict = {}
        self.namedict = {}
        self.nlist = []
        self.nodesource = False
        self.edgesource = False
        self.datasource = False
        self.layerlist = self.get_layer_list()

    def get_layer_list(self):
        """
        returns a list with the
        available layers by name
        """
        nlay = self.ds.GetLayerCount()
        ln = []
        for i in range(nlay):
            l = self.ds.GetLayer(i)
            ln.append(l.GetName())

        return ln

    def draw_layer(self, L):
        """
        Draws a polygon layer using pylab
        """
        N = 0
        L.ResetReading()
        feat = L.GetNextFeature()
        while feat is not None:
            field_count = L.GetLayerDefn().GetFieldCount()
            geo = feat.GetGeometryRef()
            if geo.GetGeometryCount() < 2:
                g1 = geo.GetGeometryRef(0)
                x = [g1.GetX(i) for i in range(g1.GetPointCount())]
                y = [g1.GetY(i) for i in range(g1.GetPointCount())]
                pylab.plot(x, y, '-', hold=True)
            for c in range(geo.GetGeometryCount()):
                ring = geo.GetGeometryRef(c)
                for cnt in range(ring.GetGeometryCount()):
                    g1 = ring.GetGeometryRef(cnt)
                    x = [g1.GetX(i) for i in range(g1.GetPointCount())]
                    y = [g1.GetY(i) for i in range(g1.GetPointCount())]
                    pylab.plot(x, y, '-', hold=True)

            feat = L.GetNextFeature()

        pylab.xlabel('Longitude')
        pylab.ylabel('Latitude')
        pylab.grid(True)
        pylab.show()

    def get_node_list(self, l):
        """
        Updates self.centdict with centroid coordinates and self.nlist with layer features
        l is an OGR layer.
        """
        self.nlist = []
        f = l.GetNextFeature()
        while f is not None:
            g = f.GetGeometryRef()
            g.Transform(self.coord_trans)
            self.geomdict[f.GetFieldAsInteger(self.geocfield)] = g
            try:
                c = g.Centroid()
                self.nlist.append(f)
                self.centdict[f.GetFieldAsInteger(self.geocfield)] = (c.GetX(), c.GetY(), c.GetZ())
                self.namedict[f.GetFieldAsInteger(self.geocfield)] = f.GetField(self.namefield)
            except:
                print(f.GetFID(), g.GetGeometryType())

            f = l.GetNextFeature()

    def create_node_layer(self):
        """
        Creates a new shape file to represent network nodes.
        The node layer will be based on the centroids of the
        polygons belonging to the map layer associated with this
        world instance.
        """
        if os.path.exists(os.path.join(self.outdir, 'Nodes.shp')):
            os.remove(os.path.join(self.outdir, 'Nodes.shp'))
            os.remove(os.path.join(self.outdir, 'Nodes.shx'))
            os.remove(os.path.join(self.outdir, 'Nodes.dbf'))
        if not self.nodesource:
            dsn = self.driver.CreateDataSource(os.path.join(self.outdir, 'Nodes.shp'))
            self.nodesource = dsn
            nl = dsn.CreateLayer('nodes', geom_type=(ogr.wkbPoint))
        fi1 = ogr.FieldDefn('name')
        fi2 = ogr.FieldDefn('geocode', field_type=(ogr.OFTInteger))
        fi3 = ogr.FieldDefn('x', field_type=(ogr.OFTString))
        fi4 = ogr.FieldDefn('y', field_type=(ogr.OFTString))
        nl.CreateField(fi1)
        nl.CreateField(fi2)
        nl.CreateField(fi3)
        nl.CreateField(fi4)
        for f in self.nlist:
            gc = f.GetFieldAsInteger(self.geocfield)
            x = self.centdict[gc][0]
            y = self.centdict[gc][1]
            fe = ogr.Feature(nl.GetLayerDefn())
            try:
                fe.SetField('name', f.GetField(self.namefield).decode('utf8', 'surrogateescape'))
            except AttributeError:
                fe.SetField('name', '')
            except UnicodeEncodeError:
                fe.SetField('name', '')

            fe.SetField('geocode', gc)
            fe.SetField('x', str(x))
            fe.SetField('y', str(y))
            pt = ogr.Geometry(type=(ogr.wkbPoint))
            pt.AddPoint(x, y)
            fe.SetGeometryDirectly(pt)
            nl.CreateFeature(fe)

        nl.SyncToDisk()
        self.out_spatial_ref.MorphToESRI()
        with open('Nodes.prj', 'w') as (fobj):
            fobj.write(self.out_spatial_ref.ExportToWkt())

    def create_edge_layer(self, elist):
        """
        Creates a new layer with edge information.
        elist is a list of tuples:
        (sgeoc,dgeoc,fsd,fds)
        """
        if os.path.exists(os.path.join(self.outdir, 'Edges.shp')):
            os.remove(os.path.join(self.outdir, 'Edges.shp'))
            os.remove(os.path.join(self.outdir, 'Edges.shx'))
            os.remove(os.path.join(self.outdir, 'Edges.dbf'))
        if not self.edgesource:
            dse = self.driver.CreateDataSource(os.path.join(self.outdir, 'Edges.shp'))
            self.edgesource = dse
            el = dse.CreateLayer('edges', geom_type=(ogr.wkbLineString))
        fi1 = ogr.FieldDefn('s_geocode', field_type=(ogr.OFTInteger))
        fi2 = ogr.FieldDefn('d_geocode', field_type=(ogr.OFTInteger))
        fi3 = ogr.FieldDefn('flowSD', field_type=(ogr.OFTReal))
        fi3.SetPrecision(12)
        fi4 = ogr.FieldDefn('flowDS', field_type=(ogr.OFTReal))
        fi4.SetPrecision(12)
        el.CreateField(fi1)
        el.CreateField(fi2)
        el.CreateField(fi3)
        el.CreateField(fi4)
        for e in elist:
            fe = ogr.Feature(el.GetLayerDefn())
            fe.SetField('s_geocode', e[0])
            fe.SetField('d_geocode', e[1])
            fe.SetField('flowSD', float(e[2]))
            fe.SetField('flowSD', float(e[3]))
            line = ogr.Geometry(type=(ogr.wkbLineString))
            try:
                line.AddPoint(self.centdict[int(e[0])][0], self.centdict[int(e[0])][1])
                line.AddPoint(self.centdict[int(e[1])][0], self.centdict[int(e[1])][1])
                fe.SetGeometryDirectly(line)
                el.CreateFeature(fe)
            except:
                pass

        el.SyncToDisk()
        self.out_spatial_ref.MorphToESRI()
        with open('Edges.prj', 'w') as (fobj):
            fobj.write(self.out_spatial_ref.ExportToWkt())

    def create_data_layer(self, varlist, data):
        """
        Creates a new shape to contain data about nodes.
        varlist is the list of fields names associated with
        the nodes.
        data is a list of lists whose first element is the geocode
        and the remaining elements are values of the fields, in the
        same order as they appear in varlist.
        """
        data = array(data)
        norms = [Normalize(c.min(), c.max()) for c in data[:, 1:].T]
        if os.path.exists(os.path.join(self.outdir, 'Data.shp')):
            os.remove(os.path.join(self.outdir, 'Data.shp'))
            os.remove(os.path.join(self.outdir, 'Data.shx'))
            os.remove(os.path.join(self.outdir, 'Data.dbf'))
        if not self.datasource:
            dsd = self.driver.CreateDataSource(os.path.join(self.outdir, 'Data.shp'))
            self.datasource = dsd
            dl = dsd.CreateLayer('sim_results', geom_type=(ogr.wkbPolygon))
        fi1 = ogr.FieldDefn('geocode', field_type=(ogr.OFTInteger))
        fin = ogr.FieldDefn('name', field_type=(ogr.OFTString))
        fic = ogr.FieldDefn('colors', field_type=(ogr.OFTString))
        dl.CreateField(fi1)
        dl.CreateField(fin)
        dl.CreateField(fic)
        for v in varlist:
            fi = ogr.FieldDefn(v, field_type=(ogr.OFTReal))
            fi.SetPrecision(12)
            dl.CreateField(fi)

        for l in data:
            hexcolors = [self.get_hex_color(norms[i](v)) for i, v in enumerate(l[1:])]
            gc = int(l[0])
            try:
                geom = self.geomdict[gc]
            except KeyError:
                raise KeyError('Geocode %s not in polygon dictionary\n' % gc)

            if geom.GetGeometryType() != 3:
                continue
            fe = ogr.Feature(dl.GetLayerDefn())
            fe.SetField('geocode', gc)
            fe.SetField('name', self.namedict[gc])
            fe.SetField('colors', str(hexcolors))
            for v, d in zip(varlist, l[1:]):
                fe.SetField(v, float(d))

            clone = geom.Clone()
            fe.SetGeometry(clone)
            dl.CreateFeature(fe)

        dl.SyncToDisk()
        self.out_spatial_ref.MorphToESRI()
        with open('Data.prj', 'w') as (fobj):
            fobj.write(self.out_spatial_ref.ExportToWkt())
        self.save_data_geojson(dl)

    def get_hex_color(self, value):
        cols = cm.get_cmap('YlOrRd', 256)
        rgba = cols(value * 256)
        bgrcol = list(rgba[:-1])
        bgrcol.reverse()
        hexcol = '#80' + rgb2hex(bgrcol)[1:]
        return hexcol

    def save_data_geojson(self, dl, namefield=None):
        """
        Creates a GeoJSON file containin the polygon layer and results of the simulation
        :Parameters:
        :parameter dl: datalayer to save
        """
        print('==> saving to GeoJSON')
        spatial_reference = dl.GetSpatialRef()
        feature_collection = {'type':'FeatureCollection', 
         'features':[]}
        if namefield is None:
            namefield = self.namefield
        dl.ResetReading()
        fe = dl.GetNextFeature()
        while fe is not None:
            fi = fe.GetField(namefield)
            try:
                fi = fi.decode('utf8', 'ignore')
            except AttributeError:
                fi = ''

            fe.SetField(namefield, str(fi))
            feature = json.loads(fe.ExportToJson())
            feature['properties']['colors'] = eval(feature['properties']['colors'])
            feature_collection['features'].append(feature)
            fe = dl.GetNextFeature()

        with open(os.path.join(self.outdir, 'data.json'), 'w') as (f):
            json.dump(feature_collection, f)

    def gen_sites_file(self, fname):
        """
        This method generate a sites
        csv file from the nodes extracted from the
        map.
        """
        with open(fname, 'w') as (f):
            for fe in self.nlist:
                gc = fe.GetFieldAsInteger(self.geocfield)
                x = self.centdict[gc][0]
                y = self.centdict[gc][1]
                name = fe.GetField(self.namefield)
                line = '%s,%s,%s,%s\n' % (x, y, name, gc)
                f.write(line)

    def close_sources(self):
        """
        Close the data sources so that data is flushed and and files are closed
        """
        if self.nodesource:
            self.nodesource.Destroy()
        if self.edgesource:
            self.edgesource.Destroy()
        if self.datasource:
            self.datasource.Destroy()


class AnimatedKML(object):
    __doc__ = '\n    Creates animated KML based on layer given\n    '

    def __init__(self, kmlfile, extrude=1):
        """
        kmlfile: File containing the layer over which the animation will be built. it must contain polygons. Placemarks should contain a tag <name> geocode</name>
        extrude: if True the polygons will be extruded according to values in the timeseries data.
        """
        self.extrude = extrude
        self.fname = kmlfile
        self.kmlDoc = minidom.parse(kmlfile)
        self.doc = self.kmlDoc.getElementsByTagName('Document')[0]
        ufElems = self.kmlDoc.getElementsByTagName('Placemark')
        self.pmdict = {}
        for e in ufElems:
            nel = e.getElementsByTagName('name')[0]
            name = self._get_text(nel.childNodes).split('-')[0]
            self.pmdict[name] = e

    def _get_text(self, nodelist):
        """
        Returns  the text of a xml text node
        """
        rc = []
        for node in nodelist:
            if node.nodeType == node.TEXT_NODE:
                rc.append(node.data)

        return ''.join(rc)

    def add_data(self, data):
        """
        Add time-series data for the localities: [(geocode,time,value),...]
        """
        vals = array([i[2] for i in data])
        norm = Normalize(vals.min(), vals.max())
        for i, d in enumerate(data):
            pm = self.pmdict[d[0]]
            pm_newtime = pm.cloneNode(1)
            on = pm_newtime.getElementsByTagName('name')[0]
            nn = self.kmlDoc.createElement('name')
            nn.appendChild(self.kmlDoc.createTextNode(d[0] + '-' + str(d[1])))
            pm_newtime.replaceChild(nn, on)
            nl = pm_newtime.childNodes
            pol = pm_newtime.getElementsByTagName('Polygon')[0]
            alt = self.kmlDoc.createElement('altitudeMode')
            alt.appendChild(self.kmlDoc.createTextNode('relativeToGround'))
            ex = self.kmlDoc.createElement('extrude')
            ex.appendChild(self.kmlDoc.createTextNode('1'))
            ts = self.kmlDoc.createElement('tessellate')
            ts.appendChild(self.kmlDoc.createTextNode('1'))
            pol.appendChild(alt)
            pol.appendChild(ex)
            pol.appendChild(ts)
            lr = pm_newtime.getElementsByTagName('LinearRing')[0]
            nlr = self.extrude_polygon(lr, d[2])
            ob = pm_newtime.getElementsByTagName('outerBoundaryIs')[0]
            ob.removeChild(lr)
            ob.appendChild(nlr)
            col = rgb2hex(cm.jet(norm(d[2]))[:3]) + 'ff'
            st = pm_newtime.getElementsByTagName('Style')[0]
            nst = self.set_polygon_style(st, col)
            pm_newtime.removeChild(st)
            pm_newtime.appendChild(nst)
            ts = self.kmlDoc.createElement('TimeStamp')
            w = self.kmlDoc.createElement('when')
            w.appendChild(self.kmlDoc.createTextNode(str(d[1])))
            ts.appendChild(w)
            pm_newtime.appendChild(ts)
            self.doc.appendChild(pm_newtime)

        for pm in six.itervalues(self.pmdict):
            self.doc.removeChild(pm)

        self.pmdict = {}

    def extrude_polygon(self, lr, alt):
        """
        Adds altitude to the coordinates of the linear ring.
        """
        c = lr.getElementsByTagName('coordinates')[0]
        nc = self.kmlDoc.createElement('coordinates')
        ctext = self._get_text(c.childNodes)
        nctext = ' '.join([p + ',' + str(alt * 100) for p in ctext.split(' ')])
        nc.appendChild(self.kmlDoc.createTextNode(nctext))
        alt = self.kmlDoc.createElement('altitudeMode')
        alt.appendChild(self.kmlDoc.createTextNode('relativeToGround'))
        ex = self.kmlDoc.createElement('extrude')
        ex.appendChild(self.kmlDoc.createTextNode('1'))
        ts = self.kmlDoc.createElement('tessellate')
        ts.appendChild(self.kmlDoc.createTextNode('1'))
        lr.replaceChild(nc, c)
        lr.appendChild(alt)
        if self.extrude:
            lr.appendChild(ex)
            lr.appendChild(ts)
        return lr

    def set_polygon_style(self, style, color):
        st = style
        pst = st.getElementsByTagName('PolyStyle')[0]
        pst1 = self.kmlDoc.createElement('PolyStyle')
        pfill = self.kmlDoc.createElement('fill')
        pcol = self.kmlDoc.createElement('color')
        pfill.appendChild(self.kmlDoc.createTextNode('1'))
        pcol.appendChild(self.kmlDoc.createTextNode(color))
        pst1.appendChild(pfill)
        pst1.appendChild(pcol)
        st.replaceChild(pst1, pst)
        return st

    def save(self, fname=''):
        """
        saves the new document
        """
        dir = os.path.split(self.fname)[0]
        if not fname:
            fname = self.fname.split('.')[0] + '_animation'
        else:
            fname = os.path.join(dir, fname)
        with open(fname + '.kml', 'w') as (f):
            f.write(self.kmlDoc.toprettyxml(indent='  ', encoding='utf-8'))
        with ZipFile((fname + '.kmz'), 'w', allowZip64=True) as (kmz):
            kmz.write(fname + '.kml')
        os.unlink(fname + '.kml')


class KmlGenerator:
    __doc__ = '\n        Generate a KML file for displaying data on \n        Google Maps/Earth\n    '

    def __init__(self):
        self.doc = None
        self.dnode = None
        self.genRoot()

    def genRoot(self):
        """
        Generate a KML file root.
        """
        self.kmldoc = doc = minidom.Document()
        kml = doc.createElement('kml')
        kml.setAttribute('xmlns', 'http://earth.google.com/kml/2.1')
        doc.appendChild(kml)
        d = doc.createElement('Document')
        kml.appendChild(d)
        nel = doc.createElement('name')
        name = doc.createTextNode('KML Epigrass data file')
        nel.appendChild(name)
        d.appendChild(nel)
        desc = doc.createElement('description')
        d.appendChild(desc)
        desc.appendChild(doc.createTextNode('Polygons with data'))
        self.dnode = d

    def get_hex_color(self, value):
        jet = cm.get_cmap('jet', 50)
        rgba = jet(value * 50)
        bgrcol = list(rgba[:-1])
        bgrcol.reverse()
        hexcol = '#80' + rgb2hex(bgrcol)[1:]
        return hexcol

    def addNodes(self, layer, names=None):
        """
        Adds a node to the document.
        d is the document element KML dom object.
        layer is a data layer with polygons and the results of a simulation as features
        names is a dictionary of names indexed by geocode(int)
        """
        doc = self.dnode
        layer.ResetReading()
        while 1:
            f = layer.GetNextFeature()
            if not f:
                break
            prevalence = float(f.GetField('prevalence'))
            hexcol = self.get_hex_color(prevalence)
            g = f.GetGeometryRef()
            if g.GetGeometryType() == 3:
                geoc = f.GetFieldAsInteger('geocode')
                if not names:
                    name = ''
                else:
                    try:
                        name = str(geoc) + '-' + names[geoc]
                    except KeyError:
                        print(geoc)
                        name = ''

                    description = 'Prevalence: %s;\nTotal cases: %s;\nImported Cases: %s;' % (
                     prevalence, f.GetField('totalcases'), f.GetField('arrivals'))
                    locale.setlocale(locale.LC_ALL, 'C')
                    gml = g.ExportToGML()
                    coords = gml.split('<gml:coordinates>')[1].split('</gml:coordinates>')[0]
                    coords = ' '.join([i + ',0' for i in coords.split(' ')])
                    pm = self.kmldoc.createElement('Placemark')
                    nm = self.kmldoc.createElement('name')
                    nm.appendChild(self.kmldoc.createTextNode(name))
                    desc = self.kmldoc.createElement('description')
                    desc.appendChild(self.kmldoc.createTextNode(description))
                    pm.appendChild(nm)
                    pm.appendChild(desc)
                    st = self.kmldoc.createElement('Style')
                    pm.appendChild(st)
                    ps = self.kmldoc.createElement('PolyStyle')
                    color = self.kmldoc.createElement('color')
                    color.appendChild(self.kmldoc.createTextNode(hexcol))
                    ps.appendChild(color)
                    fill = self.kmldoc.createElement('fill')
                    fill.appendChild(self.kmldoc.createTextNode('1'))
                    ps.appendChild(fill)
                    outline = self.kmldoc.createElement('outline')
                    outline.appendChild(self.kmldoc.createTextNode('1'))
                    ps.appendChild(outline)
                    st.appendChild(ps)
                    doc.appendChild(pm)
                    mg = self.kmldoc.createElement('MultiGeometry')
                    pm.appendChild(mg)
                    polygon = self.kmldoc.createElement('Polygon')
                    mg.appendChild(polygon)
                    ob = self.kmldoc.createElement('outerBoundaryIs')
                    polygon.appendChild(ob)
                    linr = self.kmldoc.createElement('LinearRing')
                    ob.appendChild(linr)
                    coordin = self.kmldoc.createElement('coordinates')
                    linr.appendChild(coordin)
                    coordin.appendChild(self.kmldoc.createTextNode(coords))

    def writeToFile(self, dir):
        """
        Writes the kml file to disk
        """
        fullpath = os.path.join(dir, 'Data.kml')
        f = open(fullpath, 'w')
        f.write(self.kmldoc.toxml())
        f.close()


def gdal_error_handler(err_class, err_num, err_msg):
    errtype = {gdal.CE_None: 'None', 
     gdal.CE_Debug: 'Debug', 
     gdal.CE_Warning: 'Warning', 
     gdal.CE_Failure: 'Failure', 
     gdal.CE_Fatal: 'Fatal'}
    err_msg = err_msg.replace('\n', ' ')
    err_class = errtype.get(err_class, 'None')
    print('Error Number: %s' % err_num)
    print('Error Type: %s' % err_class)
    print('Error Message: %s' % err_msg)


gdal.PushErrorHandler(gdal_error_handler)
if __name__ == '__main__':
    w = World('riozonas_LatLong.shp', 'nome_zonas', 'zona_trafe')
    layer = w.ds.GetLayerByName(w.layerlist[0])
    w.get_node_list(layer)
    w.draw_layer(layer)
    w.save_data_geojson(layer)
    w.create_node_layer()
    w.nodesource.Destroy()