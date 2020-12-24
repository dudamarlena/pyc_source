# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sdmpy/sdm.py
# Compiled at: 2019-04-03 11:16:08
from __future__ import print_function, division, absolute_import, unicode_literals
from builtins import bytes, dict, object, range, map, input
from future.utils import itervalues, viewitems, iteritems, listvalues, listitems
from io import open
import os.path
from lxml import etree, objectify
from operator import attrgetter
from .scan import Scan
from .mime import MIMEPart
_install_dir = os.path.abspath(os.path.dirname(__file__))
_xsd_dir = os.path.join(_install_dir, b'xsd')
_sdm_xsd = os.path.join(_xsd_dir, b'sdm_all.xsd')
_sdm_parser = objectify.makeparser(schema=etree.XMLSchema(file=_sdm_xsd))

class SDM(object):
    """
    Top-level class to represent an SDM.

    Init arguments:
      path = path to SDM directory
      bdfdir = different directory to search for bdfs
      (optional, for pre-archive SDMs)
      lazy = only read tables when requested

    Attributes:
      tables = list of tables
      path   = full path to SDM directory

    SDM['TableName'] returns the relevant SDMTable object.
    """

    def __init__(self, path=b'.', use_xsd=True, bdfdir=b'', lazy=False):
        parser = _sdm_parser if use_xsd else None
        self._tables = {}
        self._schemaVersion = {}
        self.path = os.path.abspath(path)
        assert os.path.exists(self.path), (b'No SDM at {0}').format(self.path)
        self.bdfdir = bdfdir
        self._asdmtree = objectify.parse(path + b'/ASDM.xml', parser)
        self.asdm = self._asdmtree.getroot()
        self.use_xsd = use_xsd
        self._asdmtables = []
        for tab in self.asdm.Table:
            tabname = str(tab.Name)
            self._schemaVersion[tabname] = tab.Entity.attrib[b'schemaVersion']
            self._asdmtables.append(tabname)
            if not lazy:
                self._tables[tabname] = sdmtable(tabname, path, use_xsd=use_xsd)

        return

    @property
    def tables(self):
        """Return the list of table names"""
        return self._asdmtables

    def __getitem__(self, key):
        if key in self._asdmtables and key not in self._tables.keys():
            self._tables[key] = sdmtable(key, self.path, use_xsd=self.use_xsd)
        return self._tables[key]

    def scan(self, idx, subidx=1):
        """Return a Scan object for the given scan/subscan number."""
        return Scan(self, str(idx), str(subidx))

    def scans(self, hasbdf=False):
        """Iterate over scans.  Set hasbdf=True to only return scans
        for which BDFs exist.
        """
        if hasbdf:
            scanidx = [ (s.scanNumber, s.subscanNumber) for s in self[b'Main'] if os.path.exists(self.scan(s.scanNumber, s.subscanNumber).bdf_fname)
                      ]
        else:
            scanidx = [ (s.scanNumber, s.subscanNumber) for s in self[b'Main'] ]
        for idx in scanidx:
            yield self.scan(*idx)

    def _update_ASDM(self):
        """Updates the ASDM table with the current number of rows."""
        for tab in self.asdm.Table:
            try:
                nrow = len(self[tab.Name])
                tab.NumberRows = nrow
            except TypeError:
                pass

    def write(self, newpath):
        """Write the SDM out to the new path location.  Currently does not
        copy the BDFs or anything else under ASDMBinary."""
        self._update_ASDM()
        if not os.path.exists(newpath):
            os.mkdir(newpath)
        objectify.deannotate(self._asdmtree, cleanup_namespaces=True)
        self._asdmtree.write(newpath + b'/ASDM.xml', encoding=b'utf-8', pretty_print=True, standalone=True)
        for tab in self.tables:
            self[tab].write(newpath)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass


def sdmtable(name, path, *args, **kwargs):
    """
    Return the correct type of SDM table object (binary or XML).
    """
    fnamebase = os.path.join(path, str(name))
    if os.path.exists(fnamebase + b'.xml'):
        return SDMTable(name, path, *args, **kwargs)
    else:
        if os.path.exists(fnamebase + b'.bin'):
            return SDMBinaryTable(name, path, *args, **kwargs)
        return


def decap(s):
    if s:
        return s[:1].lower() + s[1:]
    return b''


class SDMTable(object):
    """
    Class for an individual SDM table.

    Generally this should not be used directly, but as part of a full
    SDM via the SDM class.

    Init arguments:
      name = Name of table (not including .xml extension)
      path = Path to SDM directory

    SDMTable[i] returns the i-th row as an lxml objectify object
    """
    _idtags = {b'Main': ('scanNumber', 'subscanNumber'), 
       b'Scan': ('scanNumber', ), 
       b'Subscan': ('scanNumber', 'subscanNumber'), 
       b'CalDevice': ('antennaId', 'spectralWindowId'), 
       b'Receiver': ('spectralWindowId', )}

    def __init__(self, name, path=b'.', use_xsd=True):
        self.name = name
        try:
            self.idtag = attrgetter(*self._idtags[name])
        except KeyError:
            self.idtag = attrgetter(decap(str(name)) + b'Id')

        if use_xsd:
            parser = _sdm_parser
        else:
            parser = None
        self._tree = objectify.parse(path + b'/' + name + b'.xml', parser)
        self._table = self._tree.getroot()
        return

    @property
    def entityId(self):
        """Shortcut to entityId"""
        return self._table.Entity.get(b'entityId')

    @property
    def containerId(self):
        """Shortcut to ContainerEntity entityId"""
        return self._table.ContainerEntity.get(b'entityId')

    def __getitem__(self, key):
        if self.__len__() == 0:
            raise IndexError(key)
        if type(key) == int:
            return self._table.row[key]
        for r in self._table.row:
            try:
                tag = self.idtag(r)
                if isinstance(tag, tuple):
                    if isinstance(key, tuple) and list(map(str, tag)) == list(map(str, key)):
                        return r
                elif str(tag) == str(key):
                    return r
            except AttributeError:
                pass

        raise KeyError(key)

    def __len__(self):
        try:
            return len(self._table.row)
        except AttributeError:
            return 0

    def write(self, newpath, fname=None):
        """
        Write the updated XML file to the specified path.  Will be named
        TableName.xml unless overridden via the fname argument.
        """
        objectify.deannotate(self._tree, cleanup_namespaces=True)
        if fname is None:
            outf = os.path.join(newpath, self.name + b'.xml')
        else:
            outf = os.path.join(newpath, fname)
        self._tree.write(outf, encoding=b'utf-8', pretty_print=True, standalone=True)
        return


class SDMBinaryTable(object):
    """
    Represents an SDM binary table.  Not really implemented yet, but will
    read the data and write it back out when asked to do so by the main
    SDM class.
    """

    def __init__(self, name, path, use_xsd=None):
        self.name = name
        fp = open(path + b'/' + name + b'.bin', mode=b'rb')
        self._data = fp.read()
        fp.seek(0)
        try:
            mimetmp = MIMEPart(fp, recurse=True)
            self.header = objectify.fromstring(bytes(mimetmp.body[0].body, b'utf-8'))
            self._doffs = mimetmp.body[1].body
            self._dsize = mimetmp.body[1].size
        except RuntimeError:
            pass

        fp.close()

    def write(self, newpath, fname=None):
        if fname is None:
            outf = os.path.join(newpath, self.name + b'.bin')
        else:
            outf = os.path.join(newpath, fname)
        open(outf, b'wb').write(self._data)
        return

    def get_bytes(self, offs, nbytes):
        return self._data[self._doffs + offs:self._doffs + offs + nbytes]