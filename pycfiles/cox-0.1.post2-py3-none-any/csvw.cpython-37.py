# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/amp/src/COW/src/converter/csvw.py
# Compiled at: 2019-11-22 10:42:37
# Size of source mod 2**32: 35978 bytes
import os, datetime, json, logging, iribaker, traceback, rfc3987
from chardet.universaldetector import UniversalDetector
import multiprocessing as mp, unicodecsv as csv
from jinja2 import Template
try:
    from util import get_namespaces, Nanopublication, CSVW, PROV, DC, SKOS, RDF
except ImportError:
    from .util import get_namespaces, Nanopublication, CSVW, PROV, DC, SKOS, RDF

from rdflib import URIRef, Literal, Graph, BNode, XSD, Dataset
from rdflib.resource import Resource
from rdflib.collection import Collection
from functools import partial
try:
    from itertools import zip_longest
except ImportError:
    from itertools import izip_longest as zip_longest

import io
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
extensions = {'xml':'xml', 
 'n3':'n3',  'turtle':'ttl',  'nt':'nt',  'pretty-xml':'xml',  'trix':'trix',  'trig':'trig',  'nquads':'nq'}

def build_schema(infile, outfile, delimiter=None, quotechar='"', encoding=None, dataset_name=None, base='https://iisg.amsterdam/'):
    """
    Build a CSVW schema based on the ``infile`` CSV file, and write the resulting JSON CSVW schema to ``outfile``.

    Takes various optional parameters for instructing the CSV reader, but is also quite good at guessing the right values.
    """
    url = os.path.basename(infile)
    today = datetime.datetime.utcnow().strftime('%Y-%m-%d')
    if dataset_name is None:
        dataset_name = url
    if encoding is None:
        detector = UniversalDetector()
        with open(infile, 'rb') as (f):
            for line in f.readlines():
                detector.feed(line)
                if detector.done:
                    break

        detector.close()
        encoding = detector.result['encoding']
        logger.info('Detected encoding: {} ({} confidence)'.format(detector.result['encoding'], detector.result['confidence']))
    if delimiter is None:
        try:
            with open(infile, 'r', errors='ignore') as (csvfile):
                dialect = csv.Sniffer().sniff(csvfile.readline())
                csvfile.seek(0)
        except TypeError:
            with open(infile, 'r') as (csvfile):
                dialect = csv.Sniffer().sniff(csvfile.readline())
                csvfile.seek(0)

        logger.info("Detected dialect: {} (delimiter: '{}')".format(dialect, dialect.delimiter))
        delimiter = dialect.delimiter
    logger.info('Delimiter is: {}'.format(delimiter))
    if base.endswith('/'):
        base = base[:-1]
    metadata = {'@id':iribaker.to_iri('{}/{}'.format(base, url)), 
     '@context':[
      'https://raw.githubusercontent.com/CLARIAH/COW/master/csvw.json',
      {'@language':'en', 
       '@base':'{}/'.format(base)},
      get_namespaces(base)], 
     'url':url, 
     'dialect':{'delimiter':delimiter, 
      'encoding':encoding, 
      'quoteChar':quotechar}, 
     'dc:title':dataset_name, 
     'dcat:keyword':[],  'dc:publisher':{'schema:name':'CLARIAH Structured Data Hub - Datalegend', 
      'schema:url':{'@id': 'http://datalegend.net'}}, 
     'dc:license':{'@id': 'http://opendefinition.org/licenses/cc-by/'}, 
     'dc:modified':{'@value':today, 
      '@type':'xsd:date'}, 
     'tableSchema':{'columns':[],  'primaryKey':None, 
      'aboutUrl':'{_row}'}}
    with io.open(infile, 'rb') as (infile_file):
        r = csv.reader(infile_file, delimiter=delimiter, quotechar=quotechar)
        try:
            header = r.next()
        except AttributeError:
            header = next(r)

        logger.info('Found headers: {}'.format(header))
        if '' in header:
            logger.warning('WARNING: You have one or more empty column headers in your CSV file. Conversion might produce incorrect results because of conflated URIs or worse')
        if len(set(header)) < len(header):
            logger.warning('WARNING: You have two or more column headers that are syntactically the same. Conversion might produce incorrect results because of conflated URIs or worse')
        metadata['tableSchema']['primaryKey'] = header[0]
        for head in header:
            col = {'@id':iribaker.to_iri('{}/{}/column/{}'.format(base, url, head)), 
             'name':head, 
             'titles':[
              head], 
             'dc:description':head, 
             'datatype':'string'}
            metadata['tableSchema']['columns'].append(col)

    with open(outfile, 'w') as (outfile_file):
        outfile_file.write(json.dumps(metadata, indent=True))
    logger.info('Done')


class Item(Resource):
    """Item"""

    def __getattr__(self, p):
        try:
            objects = list(self.objects((self._to_ref)(*p.split('_', 1))))
        except:
            super(Item, self).__getattr__(self, p)

        if len(objects) == 1:
            return objects[0]
        if len(objects) == 0:
            return
        return objects

    def _to_ref(self, pfx, name):
        """Concatenates the name with the expanded namespace prefix into a new URIRef"""
        return URIRef(self._graph.store.namespace(pfx) + name)


class CSVWConverter(object):
    """CSVWConverter"""

    def __init__(self, file_name, delimiter=',', quotechar='"', encoding='utf-8', processes=4, chunksize=5000, output_format='nquads'):
        logger.info('Initializing converter for {}'.format(file_name))
        self.file_name = file_name
        self.output_format = output_format
        self.target_file = self.file_name + '.' + extensions[self.output_format]
        schema_file_name = file_name + '-metadata.json'
        if not (os.path.exists(schema_file_name) and os.path.exists(file_name)):
            raise Exception('Could not find source or metadata file in path; make sure you called with a .csv file')
        self._processes = processes
        self._chunksize = chunksize
        logger.info('Processes: {}'.format(self._processes))
        logger.info('Chunksize: {}'.format(self._chunksize))
        self.np = Nanopublication(file_name)
        self.metadata_graph = Graph()
        with open(schema_file_name, 'rb') as (f):
            try:
                self.metadata_graph.load(f, format='json-ld')
            except ValueError as err:
                try:
                    err.message = err.message + ' ; please check the syntax of your JSON-LD schema file'
                    raise
                finally:
                    err = None
                    del err

        try:
            self.metadata_uri, _ = self.metadata_graph.subject_objects(CSVW.url).next()
        except AttributeError:
            self.metadata_uri, _ = next(self.metadata_graph.subject_objects(CSVW.url))

        self.metadata = Item(self.metadata_graph, self.metadata_uri)
        self.np.pg.add((self.np.ag.identifier,
         PROV['wasDerivedFrom'], self.metadata_uri))
        for o in self.metadata_graph.objects(self.metadata_uri, DC['creator']):
            self.np.pg.add((self.np.ag.identifier, PROV['wasAttributedTo'], o))
            self.np.add((self.np.uri, PROV['wasAttributedTo'], o))
            self.np.pig.add((self.np.ag.identifier, DC['creator'], o))

        self.schema = self.metadata.csvw_tableSchema
        self.delimiter = delimiter
        self.quotechar = quotechar
        self.encoding = encoding
        if self.metadata.csvw_dialect is not None:
            if self.metadata.csvw_dialect.csvw_delimiter is not None:
                self.delimiter = str(self.metadata.csvw_dialect.csvw_delimiter)
            if self.metadata.csvw_dialect.csvw_quotechar is not None:
                self.quotechar = str(self.metadata.csvw_dialect.csvw_quoteChar)
            if self.metadata.csvw_dialect.csvw_encoding is not None:
                self.encoding = str(self.metadata.csvw_dialect.csvw_encoding)
        logger.info('Quotechar: {}'.format(self.quotechar.__repr__()))
        logger.info('Delimiter: {}'.format(self.delimiter.__repr__()))
        logger.info('Encoding : {}'.format(self.encoding.__repr__()))
        logger.warning('Taking encoding, quotechar and delimiter specifications into account...')
        self.columns = Collection(self.metadata_graph, BNode(self.schema.csvw_column))
        if not self.columns:
            self.columns = [o for s, p, o in self.metadata_graph.triples((None, URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#first'), None))]

    def convert_info(self):
        """Converts the CSVW JSON file to valid RDF for serializing into the Nanopublication publication info graph."""
        results = self.metadata_graph.query('SELECT ?s ?p ?o\n                                               WHERE { ?s ?p ?o .\n                                                       FILTER(?p = csvw:valueUrl ||\n                                                              ?p = csvw:propertyUrl ||\n                                                              ?p = csvw:aboutUrl)}')
        for s, p, o in results:
            try:
                escaped_object = URIRef(iribaker.to_iri(unicode(o)))
            except NameError:
                escaped_object = URIRef(iribaker.to_iri(str(o)))
                print(escaped_object)

            if escaped_object != o:
                self.metadata_graph.set((s, p, escaped_object))
                try:
                    self.np.pg.add((escaped_object,
                     PROV.wasDerivedFrom,
                     Literal((unicode(o)), datatype=(XSD.string))))
                except NameError:
                    self.np.pg.add((escaped_object,
                     PROV.wasDerivedFrom,
                     Literal((str(o)), datatype=(XSD.string))))
                    print(str(o))

        for s, p, o in self.metadata_graph.triples((None, None, None)):
            if s.startswith('Resource('):
                self.metadata_graph.remove((s, p, o))
                self.metadata_graph.add((BNode(str(s)[9:-1]), p, o))
                logger.debug('removed a triple because it was not formatted right. (started with "Resource")')

        self.np.ingest(self.metadata_graph, self.np.pg.identifier)

    def convert(self):
        """Starts a conversion process (in parallel or as a single process) as defined in the arguments passed to the :class:`CSVWConverter` initialization"""
        logger.info('Starting conversion')
        if self._processes == 1:
            self._simple()
        elif self._processes > 1:
            try:
                self._parallel()
            except TypeError:
                logger.info('TypeError in multiprocessing... falling back to serial conversion')
                self._simple()
            except Exception:
                logger.error('Some exception occurred, falling back to serial conversion')
                traceback.print_exc()
                self._simple()

        else:
            logger.error('Incorrect process count specification')

    def _simple(self):
        """Starts a single process for converting the file"""
        with open(self.target_file, 'wb') as (target_file):
            with open(self.file_name, 'rb') as (csvfile):
                logger.info('Opening CSV file for reading')
                reader = csv.DictReader(csvfile, encoding=(self.encoding),
                  delimiter=(self.delimiter),
                  quotechar=(self.quotechar))
                logger.info('Starting in a single process')
                c = BurstConverter(self.np.ag.identifier, self.columns, self.schema, self.metadata_graph, self.encoding, self.output_format)
                out = c.process(0, reader, 1)
                try:
                    target_file.write(out)
                except TypeError:
                    target_file.write(out.decode('utf-8'))

            self.convert_info()
            target_file.write(self.np.serialize(format=(self.output_format)))

    def _parallel(self):
        """Starts parallel processes for converting the file. Each process will receive max ``chunksize`` number of rows"""
        with open(self.target_file, 'wb') as (target_file):
            with open(self.file_name, 'rb') as (csvfile):
                logger.info('Opening CSV file for reading')
                reader = csv.DictReader(csvfile, encoding=(self.encoding),
                  delimiter=(self.delimiter),
                  quotechar=(self.quotechar))
                pool = mp.Pool(processes=(self._processes))
                logger.info('Running in {} processes'.format(self._processes))
                burstConvert_partial = partial(_burstConvert, identifier=(self.np.ag.identifier),
                  columns=(self.columns),
                  schema=(self.schema),
                  metadata_graph=(self.metadata_graph),
                  encoding=(self.encoding),
                  chunksize=(self._chunksize),
                  output_format=(self.output_format))
                for out in pool.imap(burstConvert_partial, enumerate(grouper(self._chunksize, reader))):
                    target_file.write(out)

                pool.close()
                pool.join()
            self.convert_info()
            target_file.write(self.np.serialize(format=(self.output_format)))


def grouper(n, iterable, padvalue=None):
    """grouper(3, 'abcdefg', 'x') --> ('a','b','c'), ('d','e','f'), ('g','x','x')"""
    return zip_longest(*[iter(iterable)] * n, **{'fillvalue': padvalue})


def _burstConvert(enumerated_rows, identifier, columns, schema, metadata_graph, encoding, chunksize, output_format):
    """The method used as partial for the parallel processing initiated in :func:`_parallel`."""
    try:
        count, rows = enumerated_rows
        c = BurstConverter(identifier, columns, schema, metadata_graph, encoding, output_format)
        logger.info('Process {}, nr {}, {} rows'.format(mp.current_process().name, count, len(rows)))
        result = c.process(count, rows, chunksize)
        logger.info('Process {} done'.format(mp.current_process().name))
        return result
    except:
        traceback.print_exc()


class BurstConverter(object):
    """BurstConverter"""

    def __init__(self, identifier, columns, schema, metadata_graph, encoding, output_format):
        self.ds = Dataset()
        self.g = self.ds.graph(URIRef(identifier))
        self.columns = columns
        self.schema = schema
        self.metadata_graph = metadata_graph
        self.encoding = encoding
        self.output_format = output_format
        self.templates = {}
        self.aboutURLSchema = self.schema.csvw_aboutUrl

    def equal_to_null(self, nulls, row):
        """Determines whether a value in a cell matches a 'null' value as specified in the CSVW schema)"""
        for n in nulls:
            n = Item(self.metadata_graph, n)
            col = str(n.csvw_name)
            val = str(n.csvw_null)
            if row[col] == val:
                return True

        return False

    def process(self, count, rows, chunksize):
        """Process the rows fed to the converter. Count and chunksize are used to determine the
        current row number (needed for default observation identifiers)"""
        obs_count = count * chunksize
        mult_proc_counter = 0
        iter_error_counter = 0
        for row in rows:
            if row is None:
                mult_proc_counter += 1
                continue
            row['_row'] = obs_count
            count += 1
            for c in self.columns:
                c = Item(self.metadata_graph, c)
                s = self.expandURL(self.aboutURLSchema, row)
                try:
                    try:
                        value = row[unicode(c.csvw_name)]
                    except NameError:
                        value = row[str(c.csvw_name)]

                    if self.isValueNull(value, c):
                        continue
                    elif isinstance(c.csvw_null, Item):
                        nulls = Collection(self.metadata_graph, BNode(c.csvw_null))
                        if self.equal_to_null(nulls, row):
                            continue
                except:
                    iter_error_counter += 1
                    if isinstance(c.csvw_null, Item):
                        nulls = Collection(self.metadata_graph, BNode(c.csvw_null))
                        if self.equal_to_null(nulls, row):
                            continue

                try:
                    try:
                        csvw_virtual = unicode(c.csvw_virtual)
                        csvw_name = unicode(c.csvw_name)
                        csvw_value = unicode(c.csvw_value)
                        about_url = unicode(c.csvw_aboutUrl)
                        value_url = unicode(c.csvw_valueUrl)
                    except NameError:
                        csvw_virtual = str(c.csvw_virtual)
                        csvw_name = str(c.csvw_name)
                        csvw_value = str(c.csvw_value)
                        about_url = str(c.csvw_aboutUrl)
                        value_url = str(c.csvw_valueUrl)

                    if csvw_virtual == 'true':
                        if c.csvw_aboutUrl is not None:
                            s = self.expandURL(c.csvw_aboutUrl, row)
                        if c.csvw_valueUrl is not None:
                            p = self.expandURL(c.csvw_propertyUrl, row)
                            o = self.expandURL(c.csvw_valueUrl, row)
                            try:
                                if self.isValueNull(os.path.basename(unicode(o)), c):
                                    logger.debug('skipping empty value')
                                    continue
                            except NameError:
                                if self.isValueNull(os.path.basename(str(o)), c):
                                    logger.debug('skipping empty value')
                                    continue

                            if csvw_virtual == 'true':
                                if c.csvw_datatype is not None:
                                    if URIRef(c.csvw_datatype) == XSD.anyURI:
                                        value = row[unicode(c.csvw_name)].encode('utf-8')
                                        o = URIRef(iribaker.to_iri(value))
                            if csvw_virtual == 'true':
                                if c.csvw_datatype is not None:
                                    if URIRef(c.csvw_datatype) == XSD.linkURI:
                                        about_url = about_url[about_url.find('{'):about_url.find('}') + 1]
                                        s = self.expandURL(about_url, row)
                                        value_url = value_url[value_url.find('{'):value_url.find('}') + 1]
                                        o = self.expandURL(value_url, row)
                            if c.csvw_collectionUrl is not None:
                                collection = self.expandURL(c.csvw_collectionUrl, row)
                                self.g.add((collection, RDF.type, SKOS['Collection']))
                                self.g.add((o, RDF.type, SKOS['Concept']))
                                self.g.add((collection, SKOS['member'], o))
                            if c.csvw_schemeUrl is not None:
                                scheme = self.expandURL(c.csvw_schemeUrl, row)
                                self.g.add((scheme, RDF.type, SKOS['Scheme']))
                                self.g.add((o, RDF.type, SKOS['Concept']))
                                self.g.add((o, SKOS['inScheme'], scheme))
                    else:
                        if c.csvw_value is not None:
                            value = self.render_pattern(csvw_value, row)
                        elif c.csvw_name is not None:
                            value = row[csvw_name].encode('utf-8')
                        else:
                            raise Exception("No 'name' or 'csvw:value' attribute found for this column specification")
                        if c.csvw_propertyUrl is not None:
                            p = self.expandURL(c.csvw_propertyUrl, row)
                        else:
                            if '' in self.metadata_graph.namespaces():
                                propertyUrl = self.metadata_graph.namespaces()[''][csvw_name]
                            else:
                                propertyUrl = '{}{}'.format(get_namespaces()['sdv'], csvw_name)
                            p = self.expandURL(propertyUrl, row)
                        if c.csvw_datatype is not None:
                            if URIRef(c.csvw_datatype) == XSD.anyURI:
                                o = URIRef(iribaker.to_iri(value))
                            elif URIRef(c.csvw_datatype) == XSD.string and c.csvw_lang is not None:
                                o = Literal(value, lang=(self.render_pattern(c.csvw_lang, row)))
                            else:
                                try:
                                    csvw_datatype = unicode(c.csvw_datatype)
                                except NameError:
                                    csvw_datatype = str(c.csvw_datatype).split(')')[0].split('(')[(-1)]

                                o = Literal(value, datatype=csvw_datatype, normalize=False)
                        else:
                            o = Literal(value)
                    self.g.add((s, p, o))
                    if '@id' in c:
                        self.g.add((p, PROV['wasDerivedFrom'], URIRef(c['@id'])))
                except:
                    traceback.print_exc()

            obs_count += 1

        logger.debug('{} row skips caused by multiprocessing (multiple of chunksize exceeds number of rows in file)...'.format(mult_proc_counter))
        logger.debug('{} errors encountered while trying to iterate over a NoneType...'.format(mult_proc_counter))
        logger.info('... done')
        return self.ds.serialize(format=(self.output_format))

    def render_pattern(self, pattern, row):
        """Takes a Jinja or Python formatted string, and applies it to the row value"""
        if pattern in self.templates:
            template = self.templates[pattern]
        else:
            template = self.templates[pattern] = Template(pattern)
        print(pattern)
        print(type(pattern))
        print(row)
        print(type(row))
        rendered_template = (template.render)(**row)
        try:
            return (rendered_template.format)(**row)
        except:
            logger.warning("Could not apply python string formatting, probably due to mismatched curly brackets. IRI will be '{}'. ".format(rendered_template))
            return rendered_template

    def expandURL(self, url_pattern, row, datatype=False):
        """Takes a Jinja or Python formatted string, applies it to the row values, and returns it as a URIRef"""
        try:
            unicode_url_pattern = unicode(url_pattern)
        except NameError:
            unicode_url_pattern = str(url_pattern).split(')')[0].split('(')[(-1)]

        url = self.render_pattern(unicode_url_pattern, row)
        try:
            iri = iribaker.to_iri(url)
            rfc3987.parse(iri, rule='IRI')
        except:
            raise Exception('Cannot convert `{}` to valid IRI'.format(url))

        return URIRef(iri)

    def isValueNull--- This code section failed: ---

 L. 772         0  SETUP_EXCEPT        102  'to 102'

 L. 773         2  LOAD_GLOBAL              len
                4  LOAD_FAST                'value'
                6  CALL_FUNCTION_1       1  ''
                8  LOAD_CONST               0
               10  COMPARE_OP               ==
               12  POP_JUMP_IF_FALSE    32  'to 32'
               14  LOAD_GLOBAL              unicode
               16  LOAD_FAST                'c'
               18  LOAD_ATTR                csvw_parseOnEmpty
               20  CALL_FUNCTION_1       1  ''
               22  LOAD_STR                 'true'
               24  COMPARE_OP               ==
               26  POP_JUMP_IF_FALSE    32  'to 32'

 L. 775        28  LOAD_CONST               False
               30  RETURN_VALUE     
             32_0  COME_FROM            26  '26'
             32_1  COME_FROM            12  '12'

 L. 776        32  LOAD_GLOBAL              len
               34  LOAD_FAST                'value'
               36  CALL_FUNCTION_1       1  ''
               38  LOAD_CONST               0
               40  COMPARE_OP               ==
               42  POP_JUMP_IF_TRUE     94  'to 94'
               44  LOAD_FAST                'value'
               46  LOAD_GLOBAL              unicode
               48  LOAD_FAST                'c'
               50  LOAD_ATTR                csvw_null
               52  CALL_FUNCTION_1       1  ''
               54  COMPARE_OP               ==
               56  POP_JUMP_IF_TRUE     94  'to 94'
               58  LOAD_FAST                'value'
               60  LOAD_LISTCOMP            '<code_object <listcomp>>'
               62  LOAD_STR                 'BurstConverter.isValueNull.<locals>.<listcomp>'
               64  MAKE_FUNCTION_0          ''
               66  LOAD_FAST                'c'
               68  LOAD_ATTR                csvw_null
               70  GET_ITER         
               72  CALL_FUNCTION_1       1  ''
               74  COMPARE_OP               in
               76  POP_JUMP_IF_TRUE     94  'to 94'
               78  LOAD_FAST                'value'
               80  LOAD_GLOBAL              unicode
               82  LOAD_FAST                'self'
               84  LOAD_ATTR                schema
               86  LOAD_ATTR                csvw_null
               88  CALL_FUNCTION_1       1  ''
               90  COMPARE_OP               ==
               92  POP_JUMP_IF_FALSE    98  'to 98'
             94_0  COME_FROM            76  '76'
             94_1  COME_FROM            56  '56'
             94_2  COME_FROM            42  '42'

 L. 780        94  LOAD_CONST               True
               96  RETURN_VALUE     
             98_0  COME_FROM            92  '92'
               98  POP_BLOCK        
              100  JUMP_FORWARD        114  'to 114'
            102_0  COME_FROM_EXCEPT      0  '0'

 L. 781       102  POP_TOP          
              104  POP_TOP          
              106  POP_TOP          

 L. 783       108  POP_EXCEPT       
              110  JUMP_FORWARD        114  'to 114'
              112  END_FINALLY      
            114_0  COME_FROM           110  '110'
            114_1  COME_FROM           100  '100'

 L. 784       114  LOAD_CONST               False
              116  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_BLOCK' instruction at offset 98