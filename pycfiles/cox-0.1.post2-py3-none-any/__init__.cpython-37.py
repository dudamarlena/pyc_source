# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/amp/src/COW/src/converter/__init__.py
# Compiled at: 2019-11-22 09:26:38
# Size of source mod 2**32: 20116 bytes
import os
from os import listdir
from os.path import isfile, join
import csv, logging, multiprocessing as mp, uuid, datetime, json
from iribaker import to_iri
from functools import partial
try:
    from itertools import zip_longest
except ImportError:
    from itertools import izip_longest as zip_longest

from rdflib import Graph, Dataset, URIRef, Literal
try:
    from util import Nanopublication, Profile, DatastructureDefinition, apply_default_namespaces, QB, RDF, XSD, SDV, SDR, PROV
except ImportError:
    from .util import Nanopublication, Profile, DatastructureDefinition, apply_default_namespaces, QB, RDF, XSD, SDV, SDR, PROV

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
logger.addHandler(ch)

def grouper(n, iterable, padvalue=None):
    """grouper(3, 'abcdefg', 'x') --> ('a','b','c'), ('d','e','f'), ('g','x','x')"""
    return izip_longest(*[iter(iterable)] * n, **{'fillvalue': padvalue})


class Converter(object):
    """Converter"""

    def __init__(self, dataset, dirname, author_profile, source=None, target='output.nq'):
        """
        Initialization
        """
        self._processes = 4
        self._chunksize = 1000
        self._delimiter = ','
        self._quotechar = '"'
        if source is None:
            self._source = os.path.join(dirname, dataset['file'])
        else:
            self._source = source
        self._target = target
        self._dataset = dataset
        self.dataset_name = dataset['name']
        self.dataset_uri = URIRef(dataset['uri'])
        self._variables = {}
        for variable, variable_definition in dataset['variables'].items():
            self._variables[variable] = variable_definition
            if 'values' in self._variables[variable]:
                self._variables[variable]['values_dictionary'] = dict([(unicode(v.get('label', '')), v) for v in variable_definition['values']])

        self.publication = Nanopublication(self._source)
        self.addProfile(author_profile)
        self.addDatastructureDefinition()

    def setDelimiter(self, delimiter):
        """Sets the delimiter for the CSV reader to ``delimiter`` """
        self._delimiter = delimiter

    def setQuotechar(self, quotechar):
        """Sets the quote character for the CSV reader to ``quotechar``"""
        self._quotechar = quotechar

    def setProcesses(self, processes):
        """Sets the number of processes to use for (parallel) conversion of the data"""
        self._processes = processes

    def setChunksize(self, chunksize):
        """Sets the number of lines to pass to each process"""
        self._chunksize = chunksize

    def setTarget(self, target):
        """Sets the output file to write the resulting RDF to (should be an N-Quads file)"""
        self._target = target

    def addProfile(self, author_profile):
        """Adds an author profile to the nanopublication"""
        print('Adding profile')
        profile_graph = Profile(author_profile)
        self.publication.ingest(profile_graph)
        self.publication.pg.add((self.publication.ag.identifier, PROV['wasAttributedTo'], profile_graph.author_uri))
        self.publication.pig.add((self.publication.uri, PROV['wasAttributedTo'], profile_graph.author_uri))

    def addDatastructureDefinition(self):
        """Adds a datastructure definition to the nanopublication based on what we know about the current dataset"""
        print('Adding datastructure definition')
        self.publication.ingest(DatastructureDefinition(self.dataset_uri, self.dataset_name, self._variables), self.publication.ag.identifier)
        self.publication.pg.add((self.dataset_uri, PROV['wasDerivedFrom'], self.publication.dataset_version_uri))

    def convert(self):
        """Starts the conversion process based on the parameters passed to the :class:``Converter`` initalization."""
        logger.info('Using {} processes'.format(self._processes))
        with open(self._target, 'w') as (target_file):
            target_file.write(self.publication.serialize(format='nquads'))
            with open(self._source, 'r') as (source_file):
                reader = csv.reader(source_file, delimiter=(self._delimiter),
                  quotechar=(self._quotechar),
                  strict=True)
                headers = reader.next()
                if self._processes > 1:
                    self._parallel(reader, headers, target_file)
                else:
                    self._simple(reader, headers, target_file)

    def _simple(self, reader, headers, target_file):
        """Starts a converter in a single process"""
        c = BurstConverter(self.publication.ag.identifier, self._dataset, self._variables, headers)
        out = c.process(0, reader, 1)
        target_file.write(out)

    def _parallel(self, reader, headers, target_file):
        """Starts the converter using multiple processes"""
        pool = mp.Pool(processes=(self._processes))
        burstConvert_partial = partial(_burstConvert, graph_identifier=(self.publication.ag.identifier),
          dataset=(self._dataset),
          variables=(self._variables),
          headers=headers,
          chunksize=(self._chunksize))
        for out in pool.imap(burstConvert_partial, enumerate(grouper(self._chunksize, reader))):
            target_file.write(out)

        pool.close()
        pool.join()


def _burstConvert(enumerated_rows, graph_identifier, dataset, variables, headers, chunksize):
    """The method used as partial for the parallel processing initiated in :func:`_parallel`."""
    count, rows = enumerated_rows
    c = BurstConverter(graph_identifier, dataset, variables, headers)
    print(mp.current_process().name, count, len(rows))
    result = c.process(count, rows, chunksize)
    print(mp.current_process().name, 'done')
    return result


class BurstConverter(object):
    """BurstConverter"""
    _VOCAB_BASE = str(SDV)
    _RESOURCE_BASE = str(SDR)

    def __init__(self, graph_identifier, dataset, variables, headers):
        self._headers = headers
        self._variables = variables
        self._family = None
        self._number_observations = True
        self._stop = None
        if self._family is None:
            self._VOCAB_URI_PATTERN = '{0}{{}}/{{}}'.format(self._VOCAB_BASE)
            self._RESOURCE_URI_PATTERN = '{0}{{}}/{{}}'.format(self._RESOURCE_BASE)
        else:
            self._VOCAB_URI_PATTERN = '{0}{1}/{{}}/{{}}'.format(self._VOCAB_BASE, self._family)
            self._RESOURCE_URI_PATTERN = '{0}{1}/{{}}/{{}}'.format(self._RESOURCE_BASE, self._family)
        self.ds = apply_default_namespaces(Dataset())
        self.g = self.ds.graph(URIRef(graph_identifier))
        self._dataset_name = dataset['name']
        self._dataset_uri = URIRef(dataset['uri'])

    def process--- This code section failed: ---

 L. 272         0  LOAD_FAST                'count'
                2  LOAD_FAST                'chunksize'
                4  BINARY_MULTIPLY  
                6  STORE_FAST               'obs_count'

 L. 273      8_10  SETUP_LOOP          852  'to 852'
               12  LOAD_FAST                'rows'
               14  GET_ITER         
            16_18  FOR_ITER            850  'to 850'
               20  STORE_FAST               'row'

 L. 275        22  LOAD_FAST                'row'
               24  LOAD_CONST               None
               26  COMPARE_OP               is
               28  POP_JUMP_IF_FALSE    32  'to 32'

 L. 276        30  CONTINUE             16  'to 16'
             32_0  COME_FROM            28  '28'

 L. 278        32  LOAD_FAST                'self'
               34  LOAD_ATTR                _number_observations
               36  POP_JUMP_IF_FALSE    60  'to 60'

 L. 279        38  LOAD_FAST                'self'
               40  LOAD_METHOD              resource
               42  LOAD_STR                 'observation/{}'
               44  LOAD_METHOD              format
               46  LOAD_FAST                'self'
               48  LOAD_ATTR                _dataset_name
               50  CALL_METHOD_1         1  ''
               52  LOAD_FAST                'obs_count'
               54  CALL_METHOD_2         2  ''
               56  STORE_FAST               'observation_uri'
               58  JUMP_FORWARD         84  'to 84'
             60_0  COME_FROM            36  '36'

 L. 281        60  LOAD_FAST                'self'
               62  LOAD_METHOD              resource
               64  LOAD_STR                 'observation/{}'
               66  LOAD_METHOD              format
               68  LOAD_FAST                'self'
               70  LOAD_ATTR                _dataset_name
               72  CALL_METHOD_1         1  ''
               74  LOAD_GLOBAL              uuid
               76  LOAD_METHOD              uuid4
               78  CALL_METHOD_0         0  ''
               80  CALL_METHOD_2         2  ''
               82  STORE_FAST               'observation_uri'
             84_0  COME_FROM            58  '58'

 L. 283        84  LOAD_FAST                'self'
               86  LOAD_ATTR                g
               88  LOAD_METHOD              add
               90  LOAD_FAST                'observation_uri'
               92  LOAD_GLOBAL              QB
               94  LOAD_STR                 'dataSet'
               96  BINARY_SUBSCR    
               98  LOAD_FAST                'self'
              100  LOAD_ATTR                _dataset_uri
              102  BUILD_TUPLE_3         3 
              104  CALL_METHOD_1         1  ''
              106  POP_TOP          

 L. 285       108  LOAD_CONST               0
              110  STORE_FAST               'index'

 L. 286   112_114  SETUP_LOOP          840  'to 840'
              116  LOAD_FAST                'row'
              118  GET_ITER         
          120_122  FOR_ITER            838  'to 838'
              124  STORE_FAST               'col'

 L. 288       126  LOAD_FAST                'self'
              128  LOAD_ATTR                _headers
              130  LOAD_FAST                'index'
              132  BINARY_SUBSCR    
              134  STORE_FAST               'variable'

 L. 289       136  LOAD_FAST                'col'
              138  LOAD_METHOD              decode
              140  LOAD_STR                 'utf-8'
              142  CALL_METHOD_1         1  ''
              144  STORE_FAST               'col'

 L. 291       146  LOAD_GLOBAL              len
              148  LOAD_FAST                'col'
              150  CALL_FUNCTION_1       1  ''
              152  LOAD_CONST               1
              154  COMPARE_OP               <
              156  POP_JUMP_IF_FALSE   172  'to 172'

 L. 292       158  LOAD_FAST                'index'
              160  LOAD_CONST               1
              162  INPLACE_ADD      
              164  STORE_FAST               'index'

 L. 294       166  CONTINUE            120  'to 120'
          168_170  JUMP_FORWARD        828  'to 828'
            172_0  COME_FROM           156  '156'

 L. 299       172  LOAD_FAST                'variable'
              174  LOAD_FAST                'self'
              176  LOAD_ATTR                _variables
              178  COMPARE_OP               in
          180_182  POP_JUMP_IF_FALSE   816  'to 816'

 L. 303       184  LOAD_FAST                'self'
              186  LOAD_ATTR                _variables
              188  LOAD_FAST                'variable'
              190  BINARY_SUBSCR    
              192  LOAD_STR                 'category'
              194  BINARY_SUBSCR    
              196  STORE_FAST               'category'

 L. 306       198  LOAD_GLOBAL              URIRef
              200  LOAD_FAST                'self'
              202  LOAD_ATTR                _variables
              204  LOAD_FAST                'variable'
              206  BINARY_SUBSCR    
              208  LOAD_STR                 'uri'
              210  BINARY_SUBSCR    
              212  CALL_FUNCTION_1       1  ''
              214  STORE_FAST               'variable_uri'

 L. 309       216  LOAD_GLOBAL              URIRef
              218  LOAD_FAST                'self'
              220  LOAD_ATTR                _variables
              222  LOAD_FAST                'variable'
              224  BINARY_SUBSCR    
              226  LOAD_STR                 'original'
              228  BINARY_SUBSCR    
              230  LOAD_STR                 'uri'
              232  BINARY_SUBSCR    
              234  CALL_FUNCTION_1       1  ''
              236  STORE_FAST               'original_variable_uri'

 L. 311   238_240  SETUP_EXCEPT        792  'to 792'

 L. 312       242  LOAD_FAST                'col'
              244  LOAD_STR                 'NA'
              246  COMPARE_OP               ==
          248_250  POP_JUMP_IF_TRUE    262  'to 262'
              252  LOAD_FAST                'col'
              254  LOAD_STR                 'N/A'
              256  COMPARE_OP               ==
          258_260  POP_JUMP_IF_FALSE   318  'to 318'
            262_0  COME_FROM           248  '248'

 L. 317       262  LOAD_GLOBAL              SDR
              264  LOAD_STR                 'NA'
              266  BINARY_SUBSCR    
              268  STORE_FAST               'value'

 L. 319       270  LOAD_FAST                'self'
              272  LOAD_ATTR                g
              274  LOAD_METHOD              add
              276  LOAD_FAST                'observation_uri'
              278  LOAD_FAST                'variable_uri'
              280  LOAD_FAST                'value'
              282  BUILD_TUPLE_3         3 
              284  CALL_METHOD_1         1  ''
              286  POP_TOP          

 L. 323       288  LOAD_FAST                'col'
              290  STORE_FAST               'original_value'

 L. 325       292  LOAD_FAST                'self'
              294  LOAD_ATTR                g
              296  LOAD_METHOD              add
              298  LOAD_FAST                'observation_uri'
              300  LOAD_FAST                'original_variable_uri'
              302  LOAD_GLOBAL              Literal
              304  LOAD_FAST                'original_value'
              306  CALL_FUNCTION_1       1  ''
              308  BUILD_TUPLE_3         3 
              310  CALL_METHOD_1         1  ''
              312  POP_TOP          
          314_316  JUMP_FORWARD        788  'to 788'
            318_0  COME_FROM           258  '258'

 L. 327       318  LOAD_FAST                'category'
              320  LOAD_STR                 'other'
              322  COMPARE_OP               ==
          324_326  POP_JUMP_IF_FALSE   546  'to 546'

 L. 332       328  LOAD_STR                 'transform_compiled'
              330  LOAD_FAST                'self'
              332  LOAD_ATTR                _variables
              334  LOAD_FAST                'variable'
              336  BINARY_SUBSCR    
              338  COMPARE_OP               in
          340_342  POP_JUMP_IF_FALSE   368  'to 368'

 L. 334       344  LOAD_FAST                'self'
              346  LOAD_ATTR                _variables
              348  LOAD_FAST                'variable'
              350  BINARY_SUBSCR    
              352  LOAD_STR                 'transform_compiled'
              354  BINARY_SUBSCR    
              356  STORE_FAST               'f'

 L. 335       358  LOAD_FAST                'f'
              360  LOAD_FAST                'col'
              362  CALL_FUNCTION_1       1  ''
              364  STORE_FAST               'value'
              366  JUMP_FORWARD        412  'to 412'
            368_0  COME_FROM           340  '340'

 L. 336       368  LOAD_STR                 'transform'
              370  LOAD_FAST                'self'
              372  LOAD_ATTR                _variables
              374  LOAD_FAST                'variable'
              376  BINARY_SUBSCR    
              378  COMPARE_OP               in
          380_382  POP_JUMP_IF_FALSE   390  'to 390'

 L. 342       384  LOAD_FAST                'col'
              386  STORE_FAST               'value'
              388  JUMP_FORWARD        412  'to 412'
            390_0  COME_FROM           380  '380'

 L. 346       390  LOAD_FAST                'self'
              392  LOAD_ATTR                _variables
              394  LOAD_FAST                'variable'
              396  BINARY_SUBSCR    
              398  LOAD_STR                 'values_dictionary'
              400  BINARY_SUBSCR    
              402  LOAD_FAST                'col'
              404  BINARY_SUBSCR    
              406  LOAD_STR                 'label'
              408  BINARY_SUBSCR    
              410  STORE_FAST               'value'
            412_0  COME_FROM           388  '388'
            412_1  COME_FROM           366  '366'

 L. 348       412  LOAD_STR                 'datatype'
              414  LOAD_FAST                'self'
              416  LOAD_ATTR                _variables
              418  LOAD_FAST                'variable'
              420  BINARY_SUBSCR    
              422  COMPARE_OP               in
          424_426  POP_JUMP_IF_FALSE   474  'to 474'

 L. 349       428  LOAD_FAST                'self'
              430  LOAD_ATTR                _variables
              432  LOAD_FAST                'variable'
              434  BINARY_SUBSCR    
              436  LOAD_STR                 'datatype'
              438  BINARY_SUBSCR    
              440  STORE_FAST               'datatype'

 L. 351       442  LOAD_FAST                'self'
              444  LOAD_ATTR                g
              446  LOAD_METHOD              add
              448  LOAD_FAST                'observation_uri'
              450  LOAD_FAST                'variable_uri'
              452  LOAD_GLOBAL              Literal
              454  LOAD_FAST                'value'
              456  LOAD_GLOBAL              URIRef
              458  LOAD_FAST                'datatype'
              460  CALL_FUNCTION_1       1  ''
              462  LOAD_CONST               ('datatype',)
              464  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              466  BUILD_TUPLE_3         3 
              468  CALL_METHOD_1         1  ''
              470  POP_TOP          
              472  JUMP_FORWARD        496  'to 496'
            474_0  COME_FROM           424  '424'

 L. 354       474  LOAD_FAST                'self'
              476  LOAD_ATTR                g
              478  LOAD_METHOD              add
              480  LOAD_FAST                'observation_uri'
              482  LOAD_FAST                'variable_uri'
              484  LOAD_GLOBAL              Literal
              486  LOAD_FAST                'value'
              488  CALL_FUNCTION_1       1  ''
              490  BUILD_TUPLE_3         3 
              492  CALL_METHOD_1         1  ''
              494  POP_TOP          
            496_0  COME_FROM           472  '472'

 L. 358       496  LOAD_FAST                'self'
              498  LOAD_ATTR                _variables
              500  LOAD_FAST                'variable'
              502  BINARY_SUBSCR    
              504  LOAD_STR                 'values_dictionary'
              506  BINARY_SUBSCR    
              508  LOAD_FAST                'col'
              510  BINARY_SUBSCR    
              512  LOAD_STR                 'original'
              514  BINARY_SUBSCR    
              516  LOAD_STR                 'label'
              518  BINARY_SUBSCR    
              520  STORE_FAST               'original_value'

 L. 360       522  LOAD_FAST                'self'
              524  LOAD_ATTR                g
              526  LOAD_METHOD              add
              528  LOAD_FAST                'observation_uri'
              530  LOAD_FAST                'original_variable_uri'
              532  LOAD_GLOBAL              Literal
              534  LOAD_FAST                'original_value'
              536  CALL_FUNCTION_1       1  ''
              538  BUILD_TUPLE_3         3 
              540  CALL_METHOD_1         1  ''
              542  POP_TOP          
              544  JUMP_FORWARD        788  'to 788'
            546_0  COME_FROM           324  '324'

 L. 362       546  LOAD_FAST                'category'
              548  LOAD_STR                 'coded'
              550  COMPARE_OP               ==
          552_554  POP_JUMP_IF_TRUE    566  'to 566'
              556  LOAD_FAST                'category'
              558  LOAD_STR                 'identifier'
              560  COMPARE_OP               ==
          562_564  POP_JUMP_IF_FALSE   774  'to 774'
            566_0  COME_FROM           552  '552'

 L. 365       566  LOAD_STR                 'valueUrl'
              568  LOAD_FAST                'self'
              570  LOAD_ATTR                _variables
              572  LOAD_FAST                'variable'
              574  BINARY_SUBSCR    
              576  COMPARE_OP               in
          578_580  POP_JUMP_IF_FALSE   636  'to 636'

 L. 370       582  LOAD_GLOBAL              dict
              584  LOAD_GLOBAL              zip
              586  LOAD_FAST                'self'
              588  LOAD_ATTR                _headers
              590  LOAD_LISTCOMP            '<code_object <listcomp>>'
              592  LOAD_STR                 'BurstConverter.process.<locals>.<listcomp>'
              594  MAKE_FUNCTION_0          ''
              596  LOAD_FAST                'row'
              598  GET_ITER         
              600  CALL_FUNCTION_1       1  ''
              602  CALL_FUNCTION_2       2  ''
              604  CALL_FUNCTION_1       1  ''
              606  STORE_FAST               'format_args'

 L. 371       608  LOAD_GLOBAL              to_iri
              610  LOAD_FAST                'self'
              612  LOAD_ATTR                _variables
              614  LOAD_FAST                'variable'
              616  BINARY_SUBSCR    
              618  LOAD_STR                 'valueUrl'
              620  BINARY_SUBSCR    
              622  LOAD_ATTR                format
              624  BUILD_TUPLE_0         0 
              626  LOAD_FAST                'format_args'
              628  CALL_FUNCTION_EX_KW     1  'keyword args'
              630  CALL_FUNCTION_1       1  ''
              632  STORE_FAST               'value'
              634  JUMP_FORWARD        662  'to 662'
            636_0  COME_FROM           578  '578'

 L. 376       636  LOAD_GLOBAL              to_iri
              638  LOAD_FAST                'self'
              640  LOAD_ATTR                _variables
              642  LOAD_FAST                'variable'
              644  BINARY_SUBSCR    
              646  LOAD_STR                 'values_dictionary'
              648  BINARY_SUBSCR    
              650  LOAD_FAST                'col'
              652  BINARY_SUBSCR    
              654  LOAD_STR                 'uri'
              656  BINARY_SUBSCR    
              658  CALL_FUNCTION_1       1  ''
              660  STORE_FAST               'value'
            662_0  COME_FROM           634  '634'

 L. 378       662  LOAD_FAST                'self'
              664  LOAD_ATTR                g
              666  LOAD_METHOD              add
              668  LOAD_FAST                'observation_uri'
              670  LOAD_FAST                'variable_uri'
              672  LOAD_GLOBAL              URIRef
              674  LOAD_FAST                'value'
              676  CALL_FUNCTION_1       1  ''
              678  BUILD_TUPLE_3         3 
              680  CALL_METHOD_1         1  ''
              682  POP_TOP          

 L. 380       684  LOAD_STR                 'values_dictionary'
              686  LOAD_FAST                'self'
              688  LOAD_ATTR                _variables
              690  LOAD_FAST                'variable'
              692  BINARY_SUBSCR    
              694  COMPARE_OP               in
          696_698  POP_JUMP_IF_FALSE   788  'to 788'
              700  LOAD_FAST                'col'
              702  LOAD_FAST                'self'
              704  LOAD_ATTR                _variables
              706  LOAD_FAST                'variable'
              708  BINARY_SUBSCR    
              710  LOAD_STR                 'values_dictionary'
              712  BINARY_SUBSCR    
              714  COMPARE_OP               in
          716_718  POP_JUMP_IF_FALSE   788  'to 788'

 L. 383       720  LOAD_GLOBAL              to_iri
              722  LOAD_FAST                'self'
              724  LOAD_ATTR                _variables
              726  LOAD_FAST                'variable'
              728  BINARY_SUBSCR    
              730  LOAD_STR                 'values_dictionary'
              732  BINARY_SUBSCR    
              734  LOAD_FAST                'col'
              736  BINARY_SUBSCR    
              738  LOAD_STR                 'original'
              740  BINARY_SUBSCR    
              742  LOAD_STR                 'uri'
              744  BINARY_SUBSCR    
              746  CALL_FUNCTION_1       1  ''
              748  STORE_FAST               'original_value'

 L. 385       750  LOAD_FAST                'self'
              752  LOAD_ATTR                g
              754  LOAD_METHOD              add
              756  LOAD_FAST                'observation_uri'
              758  LOAD_FAST                'original_variable_uri'
              760  LOAD_GLOBAL              URIRef
              762  LOAD_FAST                'original_value'
              764  CALL_FUNCTION_1       1  ''
              766  BUILD_TUPLE_3         3 
              768  CALL_METHOD_1         1  ''
              770  POP_TOP          
              772  JUMP_FORWARD        788  'to 788'
            774_0  COME_FROM           562  '562'

 L. 387       774  LOAD_GLOBAL              print
              776  LOAD_STR                 'Category {} unknown'
              778  LOAD_METHOD              format
              780  LOAD_FAST                'category'
              782  CALL_METHOD_1         1  ''
              784  CALL_FUNCTION_1       1  ''
              786  POP_TOP          
            788_0  COME_FROM           772  '772'
            788_1  COME_FROM           716  '716'
            788_2  COME_FROM           696  '696'
            788_3  COME_FROM           544  '544'
            788_4  COME_FROM           314  '314'
              788  POP_BLOCK        
              790  JUMP_FORWARD        814  'to 814'
            792_0  COME_FROM_EXCEPT    238  '238'

 L. 389       792  DUP_TOP          
              794  LOAD_GLOBAL              KeyError
              796  COMPARE_OP               exception-match
          798_800  POP_JUMP_IF_FALSE   812  'to 812'
              802  POP_TOP          
              804  POP_TOP          
              806  POP_TOP          

 L. 390       808  POP_EXCEPT       
              810  JUMP_FORWARD        814  'to 814'
            812_0  COME_FROM           798  '798'
              812  END_FINALLY      
            814_0  COME_FROM           810  '810'
            814_1  COME_FROM           790  '790'
              814  JUMP_FORWARD        828  'to 828'
            816_0  COME_FROM           180  '180'

 L. 396       816  LOAD_FAST                'variable'
              818  LOAD_STR                 ''
              820  COMPARE_OP               ==
          822_824  POP_JUMP_IF_FALSE   828  'to 828'

 L. 398       826  JUMP_FORWARD        828  'to 828'
            828_0  COME_FROM           826  '826'
            828_1  COME_FROM           822  '822'
            828_2  COME_FROM           814  '814'
            828_3  COME_FROM           168  '168'

 L. 403       828  LOAD_FAST                'index'
              830  LOAD_CONST               1
              832  INPLACE_ADD      
              834  STORE_FAST               'index'
              836  JUMP_BACK           120  'to 120'
              838  POP_BLOCK        
            840_0  COME_FROM_LOOP      112  '112'

 L. 405       840  LOAD_FAST                'obs_count'
              842  LOAD_CONST               1
              844  INPLACE_ADD      
              846  STORE_FAST               'obs_count'
              848  JUMP_BACK            16  'to 16'
              850  POP_BLOCK        
            852_0  COME_FROM_LOOP        8  '8'

 L. 418       852  LOAD_FAST                'self'
              854  LOAD_ATTR                ds
              856  LOAD_ATTR                serialize
              858  LOAD_STR                 'nquads'
              860  LOAD_CONST               ('format',)
              862  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              864  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_BACK' instruction at offset 836

    def resource(self, resource_type, resource_name):
        """Produce a resource-URI based on the ``_RESOURCE_URI_PATTERN`` constant"""
        raw_iri = self._RESOURCE_URI_PATTERN.format(resource_type, resource_name)
        iri = to_iri(raw_iri)
        return URIRef(iri)

    def vocab(self, concept_type, concept_name):
        """Produce a vocab-URI based on the ``_VOCAB_URI_PATTERN`` constant"""
        raw_iri = self._VOCAB_URI_PATTERN.format(concept_type, concept_name)
        iri = to_iri(raw_iri)
        return URIRef(iri)