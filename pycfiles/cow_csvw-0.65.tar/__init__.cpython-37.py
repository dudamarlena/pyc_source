# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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
    __doc__ = '\n    Converter configuration object for **QBer**-style conversion. Is used to set parameters for a conversion,\n    and to initiate an actual conversion process (implemented in :class:`BurstConverter`)\n\n    Takes a dataset_description (in QBer format) and prepares:\n\n    * A dictionary for the :class:`BurstConverter` (either in one go, or in parallel)\n    * A nanopublication structure for publishing the converted data (using :class:`converter.util.Nanopublication`)\n    * A datastructure definition inside the nanopublication (using :class:`converter.util.DatastructureDefinition`)\n    '

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
    __doc__ = 'The actual converter, that processes the chunk of lines from the CSV file, and uses the instructions from the ``variables`` array to produce RDF.'
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

    def process(self, count, rows, chunksize):
        """Process the ``rows`` read from the CSV file, and use ``count * chunksize`` to determine the absolute row number of the first row in ``rows``."""
        obs_count = count * chunksize
        for row in rows:
            if row is None:
                continue
            elif self._number_observations:
                observation_uri = self.resource('observation/{}'.format(self._dataset_name), obs_count)
            else:
                observation_uri = self.resource('observation/{}'.format(self._dataset_name), uuid.uuid4())
            self.g.add((observation_uri, QB['dataSet'], self._dataset_uri))
            index = 0
            for col in row:
                variable = self._headers[index]
                col = col.decode('utf-8')
                if len(col) < 1:
                    index += 1
                    continue
                else:
                    if variable in self._variables:
                        category = self._variables[variable]['category']
                        variable_uri = URIRef(self._variables[variable]['uri'])
                        original_variable_uri = URIRef(self._variables[variable]['original']['uri'])
                        try:
                            if col == 'NA' or col == 'N/A':
                                value = SDR['NA']
                                self.g.add((observation_uri, variable_uri, value))
                                original_value = col
                                self.g.add((observation_uri, original_variable_uri, Literal(original_value)))
                            else:
                                if category == 'other':
                                    if 'transform_compiled' in self._variables[variable]:
                                        f = self._variables[variable]['transform_compiled']
                                        value = f(col)
                                    else:
                                        if 'transform' in self._variables[variable]:
                                            value = col
                                        else:
                                            value = self._variables[variable]['values_dictionary'][col]['label']
                                    if 'datatype' in self._variables[variable]:
                                        datatype = self._variables[variable]['datatype']
                                        self.g.add((observation_uri, variable_uri, Literal(value, datatype=(URIRef(datatype)))))
                                    else:
                                        self.g.add((observation_uri, variable_uri, Literal(value)))
                                    original_value = self._variables[variable]['values_dictionary'][col]['original']['label']
                                    self.g.add((observation_uri, original_variable_uri, Literal(original_value)))
                                else:
                                    if category == 'coded' or category == 'identifier':
                                        if 'valueUrl' in self._variables[variable]:
                                            format_args = dict(zip(self._headers, [c.decode('utf-8') for c in row]))
                                            value = to_iri((self._variables[variable]['valueUrl'].format)(**format_args))
                                        else:
                                            value = to_iri(self._variables[variable]['values_dictionary'][col]['uri'])
                                        self.g.add((observation_uri, variable_uri, URIRef(value)))
                                        if 'values_dictionary' in self._variables[variable] and col in self._variables[variable]['values_dictionary']:
                                            original_value = to_iri(self._variables[variable]['values_dictionary'][col]['original']['uri'])
                                            self.g.add((observation_uri, original_variable_uri, URIRef(original_value)))
                                    else:
                                        print('Category {} unknown'.format(category))
                        except KeyError:
                            pass

                    else:
                        if variable == '':
                            pass
                        else:
                            index += 1

            obs_count += 1

        return self.ds.serialize(format='nquads')

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