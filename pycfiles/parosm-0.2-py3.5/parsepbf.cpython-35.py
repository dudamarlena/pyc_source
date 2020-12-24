# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/parosm/parse/parsepbf.py
# Compiled at: 2018-04-09 15:30:20
# Size of source mod 2**32: 6574 bytes
import os.path, zlib, lzma
from parosm.parse.parsebase import BaseParser
from parosm.parse import fileformat_pb2 as pbf_fformat
from parosm.parse import osmformat_pb2 as pbf_oformat
from parosm.types import *

class PBFParser(BaseParser):
    __doc__ = '\n    PBFParser parses the osm-pbf format\n    '

    def __init__(self, file, callback=None):
        """
        Initialize PBFParser

        The callback-method is called when a osm object is found

        def callback(element):
            pass

        :param file: Path to file
        :param callback: Callback for read osm objects
        """
        super().__init__(file, callback)
        self._PBFParser__file = file
        if not os.path.isfile(file):
            raise Exception('is not a file')
        self._PBFParser__callback = self._PBFParser__default_callback if callback is None else callback

    @staticmethod
    def __default_callback(element):
        """
        Default callback when no callback is given in init method
        :param element: osm object
        """
        print(str(element))

    def parse(self):
        """
        Starts the parser
        """
        with open(self._PBFParser__file, 'rb') as (f):
            while self._PBFParser__parse_blob(f):
                pass

    def __parse_blob(self, file):
        """
        Internal parsing function
        parses a full blob
        :param file: open file object
        :return: False when EOF, True if not
        """
        blob_header_length_raw = file.read(4)
        if len(blob_header_length_raw) == 0:
            return False
        blob_header_length = int.from_bytes(blob_header_length_raw, 'big')
        blob_header_raw = file.read(blob_header_length)
        blob_header = pbf_fformat.BlobHeader()
        blob_header.ParseFromString(blob_header_raw)
        blob_raw = file.read(blob_header.datasize)
        blob = pbf_fformat.Blob()
        blob.ParseFromString(blob_raw)
        max_blob_len = max(len(blob.raw), len(blob.zlib_data), len(blob.lzma_data))
        data = None
        if len(blob.raw) == max_blob_len:
            data = blob.raw
        else:
            if len(blob.zlib_data) == max_blob_len:
                data = zlib.decompress(blob.zlib_data)
            elif len(blob.lzma_data) == max_blob_len:
                dec = lzma.LZMADecompressor()
                data = dec.decompress(blob.lzma_data)
        if blob_header.type == 'OSMHeader':
            header = pbf_oformat.HeaderBlock()
            header.ParseFromString(data)
            osm = OSM(header.source)
            bounds = {'minlat': header.bbox.bottom * 1e-09, 
             'maxlat': header.bbox.top * 1e-09, 
             'minlon': header.bbox.left * 1e-09, 
             'maxlon': header.bbox.right * 1e-09}
            osm.set_bounds(**bounds)
            self._PBFParser__callback(osm)
        elif blob_header.type == 'OSMData':
            odata = pbf_oformat.PrimitiveBlock()
            odata.ParseFromString(data)
            strings = [s.decode('utf-8') for s in odata.stringtable.s]
            for pg in odata.primitivegroup:
                for ID, lat, lon, kv in self._PBFParser__parse_dense_nodes(pg.dense):
                    lat += odata.lat_offset
                    lon += odata.lon_offset
                    lat *= odata.granularity * 1e-09
                    lon *= odata.granularity * 1e-09
                    tags = {strings[x[0]]:strings[x[1]] for x in kv}
                    self._PBFParser__callback(Node(ID, lat, lon, tags=tags))

                for node in pg.nodes:
                    lat = node.lat + odata.lat_offset
                    lon = node.lon + odata.lon_offset
                    lat *= odata.granularity * 1e-09
                    lon *= odata.granularity * 1e-09
                    tags = {strings[k]:strings[v] for k, v in zip(node.keys, node.vals)}
                    self._PBFParser__callback(Node(node.id, lat, lon, tags=tags))

                for way in pg.ways:
                    tags = {strings[k]:strings[v] for k, v in zip(way.keys, way.vals)}
                    old_ref = None
                    refs = []
                    for ref in way.refs:
                        if old_ref is not None:
                            ref += old_ref
                        old_ref = ref
                        refs.append(ref)

                    self._PBFParser__callback(Way(way.id, nodes=refs, tags=tags))

                for rel in pg.relations:
                    tags = {strings[k]:strings[v] for k, v in zip(rel.keys, rel.vals)}
                    old_memid = None
                    memids = []
                    mtype = []
                    for t in rel.types:
                        if t == 0:
                            mtype.append('node')
                        else:
                            if t == 1:
                                mtype.append('way')
                            elif t == 2:
                                mtype.append('relation')

                    for memid in rel.memids:
                        if old_memid is not None:
                            memid += old_memid
                        old_memid = memid
                        memids.append(memid)

                    members = {mid:(mtype, strings[role]) for mid, mtype, role in zip(memids, mtype, rel.roles_sid)}
                    self._PBFParser__callback(Relation(rel.id, members=members, tags=tags))

        return True

    @staticmethod
    def __parse_dense_nodes(dense):
        """
        Parse dense node

        yields a tuple of the node ID, latitude, longitude and a
        tuple with key value attribute values

        :param dense: the dense node object
        :return: Tuple[ID, Latitude, Longitude, Tuple[Key, Value]]
        """
        last_id = None
        last_lat = None
        last_lon = None
        kv_temp = [str(x) for x in dense.keys_vals]
        kvs = [x.strip() for x in ' '.join(kv_temp).split(' 0')]
        for ID, lat, lon, kv in zip(dense.id, dense.lat, dense.lon, kvs):
            if kv != '':
                ks = [int(k) for i, k in enumerate(kv.split(' ')) if i % 2 == 0]
                vs = [int(v) for i, v in enumerate(kv.split(' ')) if (i + 1) % 2 == 0]
                kv = [(k, v) for k, v in zip(ks, vs)]
            else:
                kv = []
            if last_id is not None:
                ID += last_id
            if last_lat is not None:
                lat += last_lat
            if last_lon is not None:
                lon += last_lon
            last_id = ID
            last_lat = lat
            last_lon = lon
            yield (ID, lat, lon, kv)