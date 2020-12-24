# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/pyfc4/models.py
# Compiled at: 2018-11-13 09:35:33
# Size of source mod 2**32: 58662 bytes
import copy, datetime, io, json, pdb, rdflib
from rdflib.compare import to_isomorphic, graph_diff
import rdflib_jsonld, requests, time
from types import SimpleNamespace
import uuid, logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class Repository(object):
    __doc__ = '\n\tClass for Fedora Commons 4 (FC4), LDP server instance\n\n\tArgs:\n\t\troot (str): Full URL of repository REST endpoint (e.g. http://localhost:8080/rest)\n\t\tusername (str): username for authorization and roles\n\t\tpassword (str): password authorziation and roles\n\t\tcontext (dict): dictionary of namespace prefixes and namespace URIs that propagate\n\t\t\tto Resources\n\t\tdefault_serialization (str): mimetype of default Accept and Content-Type headers\n\t\tdefault_auto_refresh (bool): if False, resource create/update, and graph modifications\n\t\t\twill not retrieve or parse updates automatically.  Dramatically improves performance.\n\n\tAttributes:\n\t\tcontext (dict): Default dictionary of namespace prefixes and namespace URIs\n\t'
    context = {'premis': 'http://www.loc.gov/premis/rdf/v1#', 
     'test': 'info:fedora/test/', 
     'rdfs': 'http://www.w3.org/2000/01/rdf-schema#', 
     'dbpedia': 'http://dbpedia.org/ontology/', 
     'xsi': 'http://www.w3.org/2001/XMLSchema-instance', 
     'xmlns': 'http://www.w3.org/2000/xmlns/', 
     'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#', 
     'fedora': 'http://fedora.info/definitions/v4/repository#', 
     'xml': 'http://www.w3.org/XML/1998/namespace', 
     'ebucore': 'http://www.ebu.ch/metadata/ontologies/ebucore/ebucore#', 
     'ldp': 'http://www.w3.org/ns/ldp#', 
     'xs': 'http://www.w3.org/2001/XMLSchema', 
     'fedoraconfig': 'http://fedora.info/definitions/v4/config#', 
     'foaf': 'http://xmlns.com/foaf/0.1/', 
     'dc': 'http://purl.org/dc/elements/1.1/', 
     'pcdm': 'http://pcdm.org/models#', 
     'ore': 'http://www.openarchives.org/ore/terms/'}

    def __init__(self, root, username, password, context=None, default_serialization='application/rdf+xml', default_auto_refresh=False, custom_resource_type_parser=None):
        self.root = root
        if not self.root.endswith('/'):
            self.root += '/'
        self.username = username
        self.password = password
        self.default_serialization = default_serialization
        self.default_auto_refresh = default_auto_refresh
        self.api = API(self)
        self.namespace_manager = rdflib.namespace.NamespaceManager(rdflib.Graph())
        for ns_prefix, ns_uri in self.context.items():
            self.namespace_manager.bind(ns_prefix, ns_uri, override=False)

        if context:
            logger.debug('context provided, merging with defaults')
            self.context.update(context)
        self.txns = {}
        self.custom_resource_type_parser = custom_resource_type_parser

    def parse_uri(self, uri=None):
        """
                parses and cleans up possible uri inputs, return instance of rdflib.term.URIRef

                Args:
                        uri (rdflib.term.URIRef,str): input URI

                Returns:
                        rdflib.term.URIRef
                """
        if not uri:
            return rdflib.term.URIRef(self.root)
        if type(uri) == str:
            if type(uri) == str and not uri.startswith('http'):
                return rdflib.term.URIRef('%s%s' % (self.root, uri))
            else:
                return rdflib.term.URIRef(uri)
        else:
            if type(uri) == rdflib.term.URIRef:
                return uri
            raise TypeError('invalid URI input')

    def create_resource(self, resource_type=None, uri=None):
        """
                Convenience method for creating a new resource

                Note: A Resource is instantiated, but is not yet created.  Still requires resource.create().

                Args:
                        uri (rdflib.term.URIRef, str): uri of resource to create
                        resource_type (NonRDFSource (Binary), BasicContainer, DirectContainer, IndirectContainer):  resource type to create

                Returns:
                        (NonRDFSource (Binary), BasicContainer, DirectContainer, IndirectContainer): instance of appropriate type
                """
        if resource_type in [NonRDFSource, Binary, BasicContainer, DirectContainer, IndirectContainer]:
            return resource_type(self, uri)
        raise TypeError('expecting Resource type, such as BasicContainer or NonRDFSource')

    def get_resource(self, uri, resource_type=None, response_format=None):
        """
                Retrieve resource:
                        - Issues an initial GET request
                        - If 200, continues, 404, returns False, otherwise raises Exception
                        - Parse resource type
                                - If custom resource type parser provided, this fires
                                - Else, or if custom parser misses, fire HEAD request and parse LDP resource type from Link header
                        - Return instantiated pyfc4 resource

                Args:
                        uri (rdflib.term.URIRef,str): input URI
                        resource_type (): resource class e.g. BasicContainer, NonRDFSource, or extensions thereof
                        response_format (str): expects mimetype / Content-Type header such as 'application/rdf+xml', 'text/turtle', etc.

                Returns:
                        Resource
                """
        uri = self.parse_uri(uri)
        if uri.toPython().endswith('/fcr:metadata'):
            uri = rdflib.term.URIRef(uri.toPython().rstrip('/fcr:metadata'))
        get_response = self.api.http_request('GET', '%s/fcr:metadata' % uri, response_format=response_format)
        if get_response.status_code == 404:
            logger.debug('resource uri %s not found, returning False' % uri)
            return False
        if get_response.status_code == 200:
            if not resource_type:
                if self.custom_resource_type_parser:
                    logger.debug('custom resource type parser provided, attempting')
                    resource_type = self.custom_resource_type_parser(self, uri, get_response)
                if not resource_type:
                    head_response = self.api.http_request('HEAD', uri)
                    resource_type = self.api.parse_resource_type(head_response)
                logger.debug('using resource type: %s' % resource_type)
                return resource_type(self, uri, response=get_response)
        raise Exception('HTTP %s, error retrieving resource uri %s' % (get_response.status_code, uri))

    def start_txn(self, txn_name=None):
        """
                Request new transaction from repository, init new Transaction,
                store in self.txns

                Args:
                        txn_name (str): human name for transaction

                Return:
                        (Transaction): returns intance of newly created transaction
                """
        if not txn_name:
            txn_name = uuid.uuid4().hex
        txn_response = self.api.http_request('POST', '%s/fcr:tx' % self.root, data=None, headers=None)
        if txn_response.status_code == 201:
            txn_uri = txn_response.headers['Location']
            logger.debug('spawning transaction: %s' % txn_uri)
            txn = Transaction(self, txn_name, txn_uri, expires=txn_response.headers['Expires'])
            self.txns[txn_name] = txn
            return txn

    def get_txn(self, txn_name, txn_uri):
        """
                Retrieves known transaction and adds to self.txns.

                TODO:
                        Perhaps this should send a keep-alive request as well?  Obviously still needed, and would reset timer.

                Args:
                        txn_prefix (str, rdflib.term.URIRef): uri of the transaction. e.g. http://localhost:8080/rest/txn:123456789
                        txn_name (str): local, human name for transaction

                Return:
                        (Transaction) local instance of transactions from self.txns[txn_uri]
                """
        txn_uri = self.parse_uri(txn_uri)
        txn_response = self.api.http_request('GET', txn_uri, data=None, headers=None)
        if txn_response.status_code == 200:
            logger.debug('transactoin found: %s' % txn_uri)
            txn = Transaction(self, txn_name, txn_uri, expires=None)
            self.txns[txn_name] = txn
            return txn
        if txn_response.status_code in (404, 410):
            logger.debug('transaction does not exist: %s' % txn_uri)
            return False
        raise Exception('HTTP %s, could not retrieve transaction' % txn_response.status_code)


class Transaction(Repository):
    __doc__ = '\n\tClass to represent open transactions.  Spawned by repository instance, these are stored in\n\trepo.txns.\n\n\tInherits:\n\t\tRepository\n\n\tArgs:\n\t\ttxn_name (str): human name for transaction\n\t\ttxn_uri (rdflib.term.URIRef, str): URI of transaction, also to be used as Transaction root path\n\t\texpires (str): expires information from headers\n\t'

    def __init__(self, repo, txn_name, txn_uri, expires=None):
        super().__init__(txn_uri, repo.username, repo.password, context=repo.context, default_serialization=repo.default_serialization)
        self.name = txn_name
        self.expires = expires
        self.active = True

    def keep_alive(self):
        """
                Keep current transaction alive, updates self.expires

                Args:
                        None

                Return:
                        None: sets new self.expires
                """
        txn_response = self.api.http_request('POST', '%sfcr:tx' % self.root, data=None, headers=None)
        if txn_response.status_code == 204:
            logger.debug('continuing transaction: %s' % self.root)
            self.active = True
            self.expires = txn_response.headers['Expires']
            return True
        if txn_response.status_code == 410:
            logger.debug('transaction does not exist: %s' % self.root)
            self.active = False
            return False
        raise Exception('HTTP %s, could not continue transaction' % txn_response.status_code)

    def _close(self, close_type):
        """
                Ends transaction by committing, or rolling back, all changes during transaction.

                Args:
                        close_type (str): expects "commit" or "rollback"

                Return:
                        (bool)
                """
        txn_response = self.api.http_request('POST', '%sfcr:tx/fcr:%s' % (self.root, close_type), data=None, headers=None)
        if txn_response.status_code == 204:
            logger.debug('%s for transaction: %s, successful' % (close_type, self.root))
            self.active = False
            return True
        if txn_response.status_code in (404, 410):
            logger.debug('transaction does not exist: %s' % self.root)
            self.active = False
            return False
        raise Exception('HTTP %s, could not commit transaction' % txn_response.status_code)

    def commit(self):
        """
                Fire self._close() method

                Args:
                        None
                Returns:
                        bool
                """
        return self._close('commit')

    def rollback(self):
        """
                Fire self._close() method

                Args:
                        None
                Returns:
                        bool
                """
        return self._close('rollback')


class API(object):
    __doc__ = '\n\tAPI for making requests and parsing responses from repository endpoint\n\n\tArgs:\n\t\trepo (Repository): instance of Repository class\n\t'

    def __init__(self, repo):
        self.repo = repo

    def http_request(self, verb, uri, data=None, headers=None, files=None, response_format=None, is_rdf=True, stream=False):
        """
                Primary route for all HTTP requests to repository.  Ability to set most parameters for requests library,
                with some additional convenience parameters as well.

                Args:
                        verb (str): HTTP verb to use for request, e.g. PUT, POST, GET, HEAD, PATCH, etc.
                        uri (rdflib.term.URIRef,str): input URI
                        data (str,file): payload of data to send for request, may be overridden in preperation of request
                        headers (dict): optional dictionary of headers passed directly to requests.request
                        files (dict): optional dictionary of files passed directly to requests.request
                        response_format (str): desired response format for resource's payload, e.g. 'application/rdf+xml', 'text/turtle', etc.
                        is_rdf (bool): if True, set Accept header based on combination of response_format and headers
                        stream (bool): passed directly to requests.request for stream parameter

                Returns:
                        requests.models.Response
                """
        if is_rdf and verb == 'GET':
            if not response_format:
                response_format = self.repo.default_serialization
            if headers and 'Accept' not in headers.keys():
                headers['Accept'] = response_format
            else:
                headers = {'Accept': response_format}
            if type(uri) == rdflib.term.URIRef:
                uri = uri.toPython()
            logger.debug('%s request for %s, format %s, headers %s' % (
             verb, uri, response_format, headers))
            session = requests.Session()
            request = requests.Request(verb, uri, auth=(self.repo.username, self.repo.password), data=data, headers=headers, files=files)
            prepped_request = session.prepare_request(request)
            response = session.send(prepped_request, stream=stream)
            return response

    def parse_resource_type(self, response):
        """
                parse resource type from self.http_request()

                Note: uses isinstance() as plugins may extend these base LDP resource type.

                Args:
                        response (requests.models.Response): response object

                Returns:
                        [NonRDFSource, BasicContainer, DirectContainer, IndirectContainer]
                """
        links = [link.split(';')[0].lstrip('<').rstrip('>') for link in response.headers['Link'].split(', ') if link.startswith('<http://www.w3.org/ns/ldp#')]
        ldp_resource_types = [self.repo.namespace_manager.compute_qname(resource_type)[2] for resource_type in links]
        logger.debug('Parsed LDP resource types from LINK header: %s' % ldp_resource_types)
        if 'NonRDFSource' in ldp_resource_types:
            return NonRDFSource
        else:
            if 'BasicContainer' in ldp_resource_types:
                return BasicContainer
            if 'DirectContainer' in ldp_resource_types:
                return DirectContainer
            if 'IndirectContainer' in ldp_resource_types:
                return IndirectContainer
            logger.debug('could not determine resource type from Link header, returning False')
            return False

    def parse_rdf_payload(self, data, headers):
        """
                small function to parse RDF payloads from various repository endpoints

                Args:
                        data (response.data): data from requests response
                        headers (response.headers): headers from requests response

                Returns:
                        (rdflib.Graph): parsed graph
                """
        if headers['Content-Type'].startswith('text/plain'):
            logger.debug('text/plain Content-Type detected, using application/n-triples for parser')
            parse_format = 'application/n-triples'
        else:
            parse_format = headers['Content-Type']
        if ';charset' in parse_format:
            parse_format = parse_format.split(';')[0]
        graph = rdflib.Graph().parse(data=data.decode('utf-8'), format=parse_format)
        return graph


class SparqlUpdate(object):
    __doc__ = '\n\tClass to handle the creation of Sparql updates via PATCH request.\n\tAccepts prefixes and graphs from resource, computes diff of graphs, and builds sparql query for update.\n\n\tArgs:\n\t\tprefixes (types.SimpleNamespace): prefixes from resource at self.rdf.prefixes\n\t\tdiffs (types.SimpleNamespace): diffs is comprised of three graphs that are derived from self._diff_graph(), at self.rdf.diffs\n\t'

    def __init__(self, prefixes, diffs):
        self.prefixes = prefixes
        self.diffs = diffs
        self.update_namespaces = set()
        self.update_prefixes = {}

    def _derive_namespaces(self):
        """
                Small method to loop through three graphs in self.diffs, identify unique namespace URIs.
                Then, loop through provided dictionary of prefixes and pin one to another.

                Args:
                        None: uses self.prefixes and self.diffs

                Returns:
                        None: sets self.update_namespaces and self.update_prefixes
                """
        for graph in [self.diffs.overlap, self.diffs.removed, self.diffs.added]:
            for s, p, o in graph:
                try:
                    ns_prefix, ns_uri, predicate = graph.compute_qname(p)
                    self.update_namespaces.add(ns_uri)
                except:
                    logger.debug('could not parse Object URI: %s' % ns_uri)

                try:
                    ns_prefix, ns_uri, predicate = graph.compute_qname(o)
                    self.update_namespaces.add(ns_uri)
                except:
                    logger.debug('could not parse Object URI: %s' % ns_uri)

        logger.debug(self.update_namespaces)
        for ns_uri in self.update_namespaces:
            for k in self.prefixes.__dict__:
                if str(ns_uri) == str(self.prefixes.__dict__[k]):
                    logger.debug('adding prefix %s for uri %s to unique_prefixes' % (k, str(ns_uri)))
                    self.update_prefixes[k] = self.prefixes.__dict__[k]

    def build_query(self):
        """
                Using the three graphs derived from self._diff_graph(), build a sparql update query in the format:

                PREFIX foo: <http://foo.com>
                PREFIX bar: <http://bar.com>

                DELETE {...}
                INSERT {...}
                WHERE {...}

                Args:
                        None: uses variables from self

                Returns:
                        (str) sparql update query as string

                """
        self._derive_namespaces()
        sparql_query = ''
        for ns_prefix, ns_uri in self.update_prefixes.items():
            sparql_query += 'PREFIX %s: <%s>\n' % (ns_prefix, str(ns_uri))

        removed_serialized = self.diffs.removed.serialize(format='nt').decode('utf-8')
        sparql_query += '\nDELETE {\n%s}\n\n' % removed_serialized
        added_serialized = self.diffs.added.serialize(format='nt').decode('utf-8')
        sparql_query += '\nINSERT {\n%s}\n\n' % added_serialized
        sparql_query += 'WHERE {}'
        return sparql_query


class Resource(object):
    __doc__ = '\n\tLinked Data Platform Resource (LDPR)\n\tA HTTP resource whose state is represented in any way that conforms to the simple lifecycle patterns and conventions in section 4. Linked Data Platform Resources.\n\thttps://www.w3.org/TR/ldp/\n\n\tIn the LDP hierarchy, this class represents the most abstract entity of "Resource".\n\n\tSub-classed by:\n\t\tNonRDFSource, Container\n\n\tArgs:\n\t\trepo (Repository): instance of Repository class\n\t\turi (rdflib.term.URIRef,str): input URI\n\t\tresponse (requests.models.Response): defaults None, but if passed, populate self.data, self.headers, self.status_code\n\t\trdf_prefixes_mixins (dict): optional rdf prefixes and namespaces\n\t'

    def __init__(self, repo, uri=None, response=None, rdf_prefixes_mixins=None):
        self.repo = repo
        self.uri = self.repo.parse_uri(uri)
        if response:
            self.response = response
            self.data = self.response.content
            self.headers = self.response.headers
            self.status_code = self.response.status_code
            if self.status_code == 200:
                self.exists = True
        else:
            self.response = None
            self.data = None
            self.headers = {}
            self.status_code = None
            self.exists = False
        self._build_rdf(data=self.data)
        self.versions = SimpleNamespace()

    def __repr__(self):
        return '<%s Resource, uri: %s>' % (self.__class__.__name__, self.uri)

    def uri_as_string(self):
        """
                return rdflib.term.URIRef URI as string

                Returns:
                        (str)
                """
        return self.uri.toPython()

    def check_exists(self):
        """
                Check if resource exists, update self.exists, returns

                Returns:
                        None: sets self.exists
                """
        response = self.repo.api.http_request('HEAD', self.uri)
        self.status_code = response.status_code
        if self.status_code == 200:
            self.exists = True
        else:
            if self.status_code == 410:
                self.exists = False
            elif self.status_code == 404:
                self.exists = False
        return self.exists

    def create(self, specify_uri=False, ignore_tombstone=False, serialization_format=None, stream=False, auto_refresh=None):
        """
                Primary method to create resources.

                Args:
                        specify_uri (bool): If True, uses PUT verb and sets the URI during creation.  If False, uses POST and gets repository minted URI
                        ignore_tombstone (bool): If True, will attempt creation, if tombstone exists (409), will delete tombstone and retry
                        serialization_format(str): Content-Type header / mimetype that will be used to serialize self.rdf.graph, and set headers for PUT/POST requests
                        auto_refresh (bool): If True, refreshes resource after update. If left None, defaults to repo.default_auto_refresh
                """
        if self.exists:
            raise Exception('resource exists attribute True, aborting')
        else:
            if specify_uri:
                verb = 'PUT'
            else:
                verb = 'POST'
            logger.debug('creating resource %s with verb %s' % (self.uri, verb))
            if issubclass(type(self), NonRDFSource):
                self.binary._prep_binary()
                data = self.binary.data
            else:
                if not serialization_format:
                    serialization_format = self.repo.default_serialization
                data = self.rdf.graph.serialize(format=serialization_format)
                logger.debug('Serialized graph used for resource creation:')
                logger.debug(data.decode('utf-8'))
                self.headers['Content-Type'] = serialization_format
            response = self.repo.api.http_request(verb, self.uri, data=data, headers=self.headers, stream=stream)
            return self._handle_create(response, ignore_tombstone, auto_refresh)

    def _handle_create(self, response, ignore_tombstone, auto_refresh):
        """
                Handles response from self.create()

                Args:
                        response (requests.models.Response): response object from self.create()
                        ignore_tombstone (bool): If True, will attempt creation, if tombstone exists (409), will delete tombstone and retry
                """
        if response.status_code == 201:
            self.uri = self.repo.parse_uri(response.text)
            if auto_refresh:
                self.refresh()
            else:
                if auto_refresh == None and self.repo.default_auto_refresh:
                    self.refresh()
                if hasattr(self, '_post_create'):
                    self._post_create(auto_refresh=auto_refresh)
        else:
            if response.status_code == 404:
                raise Exception('HTTP 404, for this POST request target location does not exist')
            else:
                if response.status_code == 409:
                    raise Exception('HTTP 409, resource already exists')
                else:
                    if response.status_code == 410:
                        if ignore_tombstone:
                            response = self.repo.api.http_request('DELETE', '%s/fcr:tombstone' % self.uri)
                            if response.status_code == 204:
                                logger.debug('tombstone removed, retrying create')
                                self.create()
                            else:
                                raise Exception('HTTP %s, Could not remove tombstone for %s' % (response.status_code, self.uri))
                        else:
                            raise Exception('tombstone for %s detected, aborting' % self.uri)
                    else:
                        if response.status_code == 415:
                            raise Exception('HTTP 415, unsupported media type')
                        else:
                            raise Exception('HTTP %s, unknown error creating resource' % response.status_code)
        return self

    def options(self):
        """
                Small method to return headers of an OPTIONS request to self.uri

                Args:
                        None

                Return:
                        (dict) response headers from OPTIONS request
                """
        response = self.repo.api.http_request('OPTIONS', self.uri)
        return response.headers

    def move(self, destination, remove_tombstone=True):
        """
                Method to move resource to another location.
                Note: by default, this method removes the tombstone at the resource's original URI.
                Can use optional flag remove_tombstone to keep tombstone on successful move.

                Note: other resource's triples that are managed by Fedora that point to this resource,
                *will* point to the new URI after the move.

                Args:
                        destination (rdflib.term.URIRef, str): URI location to move resource
                        remove_tombstone (bool): defaults to False, set to True to keep tombstone

                Returns:
                        (Resource) new, moved instance of resource
                """
        destination_uri = self.repo.parse_uri(destination)
        response = self.repo.api.http_request('MOVE', self.uri, data=None, headers={'Destination': destination_uri.toPython()})
        if response.status_code == 201:
            self.exists = False
            if remove_tombstone:
                tombstone_response = self.repo.api.http_request('DELETE', '%s/fcr:tombstone' % self.uri)
            self.uri = destination_uri
            self.refresh()
            return destination_uri
        raise Exception('HTTP %s, could not move resource %s to %s' % (response.status_code, self.uri, destination_uri))

    def copy(self, destination):
        """
                Method to copy resource to another location

                Args:
                        destination (rdflib.term.URIRef, str): URI location to move resource

                Returns:
                        (Resource) new, moved instance of resource
                """
        destination_uri = self.repo.parse_uri(destination)
        response = self.repo.api.http_request('COPY', self.uri, data=None, headers={'Destination': destination_uri.toPython()})
        if response.status_code == 201:
            return destination_uri
        raise Exception('HTTP %s, could not move resource %s to %s' % (response.status_code, self.uri, destination_uri))

    def delete(self, remove_tombstone=True):
        """
                Method to delete resources.

                Args:
                        remove_tombstone (bool): If True, will remove tombstone at uri/fcr:tombstone when removing resource.

                Returns:
                        (bool)
                """
        response = self.repo.api.http_request('DELETE', self.uri)
        if response.status_code == 204:
            self._empty_resource_attributes()
        if remove_tombstone:
            self.repo.api.http_request('DELETE', '%s/fcr:tombstone' % self.uri)
        return True

    def refresh(self, refresh_binary=True):
        """
                Performs GET request and refreshes RDF information for resource.

                Args:
                        None

                Returns:
                        None
                """
        updated_self = self.repo.get_resource(self.uri)
        if not isinstance(self, type(updated_self)):
            raise Exception('Instantiated %s, but repository reports this resource is %s' % (type(updated_self), type(self)))
        if updated_self:
            self.status_code = updated_self.status_code
            self.rdf.data = updated_self.rdf.data
            self.headers = updated_self.headers
            self.exists = updated_self.exists
            if type(self) != NonRDFSource:
                self._parse_graph()
            self.versions = SimpleNamespace()
            if type(updated_self) == NonRDFSource and refresh_binary:
                self.binary.refresh(updated_self)
            if hasattr(self, '_post_refresh'):
                self._post_refresh()
            del updated_self
        else:
            logger.debug('resource %s not found, dumping values')
            self._empty_resource_attributes()

    def _build_rdf(self, data=None):
        """
                Parse incoming rdf as self.rdf.orig_graph, create copy at self.rdf.graph

                Args:
                        data (): payload from GET request, expected RDF content in various serialization formats

                Returns:
                        None
                """
        self.rdf = SimpleNamespace()
        self.rdf.data = data
        self.rdf.prefixes = SimpleNamespace()
        self.rdf.uris = SimpleNamespace()
        for prefix, uri in self.repo.context.items():
            setattr(self.rdf.prefixes, prefix, rdflib.Namespace(uri))

        self._parse_graph()

    def _parse_graph(self):
        """
                use Content-Type from headers to determine parsing method

                Args:
                        None

                Return:
                        None: sets self.rdf by parsing data from GET request, or setting blank graph of resource does not yet exist
                """
        if self.exists:
            self.rdf.graph = self.repo.api.parse_rdf_payload(self.rdf.data, self.headers)
        else:
            self.rdf.graph = rdflib.Graph()
        self.rdf.namespace_manager = rdflib.namespace.NamespaceManager(self.rdf.graph)
        for ns_prefix, ns_uri in self.rdf.prefixes.__dict__.items():
            self.rdf.namespace_manager.bind(ns_prefix, ns_uri, override=False)

        for ns_prefix, ns_uri in self.rdf.graph.namespaces():
            setattr(self.rdf.prefixes, ns_prefix, rdflib.Namespace(ns_uri))
            setattr(self.rdf.uris, rdflib.Namespace(ns_uri), ns_prefix)

        self.rdf._orig_graph = copy.deepcopy(self.rdf.graph)
        self.parse_object_like_triples()

    def parse_object_like_triples(self):
        """
                method to parse triples from self.rdf.graph for object-like
                access

                Args:
                        None

                Returns:
                        None: sets self.rdf.triples
                """
        self.rdf.triples = SimpleNamespace()
        for s, p, o in self.rdf.graph:
            ns_prefix, ns_uri, predicate = self.rdf.graph.compute_qname(p)
            if not hasattr(self.rdf.triples, ns_prefix):
                setattr(self.rdf.triples, ns_prefix, SimpleNamespace())
            if not hasattr(getattr(self.rdf.triples, ns_prefix), predicate):
                setattr(getattr(self.rdf.triples, ns_prefix), predicate, [])
            getattr(getattr(self.rdf.triples, ns_prefix), predicate).append(o)

    def _diff_graph(self):
        """
                Uses rdflib.compare diff, https://github.com/RDFLib/rdflib/blob/master/rdflib/compare.py
                When a resource is retrieved, the graph retrieved and parsed at that time is saved to self.rdf._orig_graph,
                and all local modifications are made to self.rdf.graph.  This method compares the two graphs and returns the diff
                in the format of three graphs:

                        overlap - triples SHARED by both
                        removed - triples that exist ONLY in the original graph, self.rdf._orig_graph
                        added - triples that exist ONLY in the modified graph, self.rdf.graph

                These are used for building a sparql update query for self.update.

                Args:
                        None

                Returns:
                        None: sets self.rdf.diffs and adds the three graphs mentioned, 'overlap', 'removed', and 'added'
                """
        overlap, removed, added = graph_diff(to_isomorphic(self.rdf._orig_graph), to_isomorphic(self.rdf.graph))
        diffs = SimpleNamespace()
        diffs.overlap = overlap
        diffs.removed = removed
        diffs.added = added
        self.rdf.diffs = diffs

    def add_namespace(self, ns_prefix, ns_uri):
        """
                preferred method is to instantiate with repository under 'context',
                but prefixes / namespaces can be added for a Resource instance

                adds to self.rdf.prefixes which will endure through create/update/refresh,
                and get added back to parsed graph namespaces

                Args:
                        ns_prefix (str): prefix for namespace, e.g. 'dc', 'foaf'
                        ns_uri (str): string of namespace / ontology. e.g. 'http://purl.org/dc/elements/1.1/', 'http://xmlns.com/foaf/0.1/'

                Returns:
                        None: binds this new prefix:namespace combination to self.rdf.prefixes for use, and self.rdf.graph for serialization
                """
        setattr(self.rdf.prefixes, ns_prefix, rdflib.Namespace(ns_uri))
        self.rdf.namespace_manager.bind(ns_prefix, ns_uri, override=False)

    def _empty_resource_attributes(self):
        """
                small method to empty values if resource is removed or absent

                Args:
                        None

                Return:
                        None: empties selected resource attributes
                """
        self.status_code = 404
        self.headers = {}
        self.exists = False
        self.rdf = self._build_rdf()
        if type(self) == NonRDFSource:
            self.binary.empty()

    def _handle_object(self, object_input):
        """
                Method to handle possible values passed for adding, removing, modifying triples.
                Detects type of input and sets appropriate http://www.w3.org/2001/XMLSchema# datatype

                Args:
                        object_input (str,int,datetime,): many possible inputs

                Returns:
                        (rdflib.term.Literal): with appropriate datatype attribute
                """
        if type(object_input) == str:
            return rdflib.term.Literal(object_input, datatype=rdflib.XSD.string)
        else:
            if type(object_input) == int:
                return rdflib.term.Literal(object_input, datatype=rdflib.XSD.int)
            if type(object_input) == float:
                return rdflib.term.Literal(object_input, datatype=rdflib.XSD.float)
            if type(object_input) == datetime.datetime:
                return rdflib.term.Literal(object_input, datatype=rdflib.XSD.date)
            return object_input

    def add_triple(self, p, o, auto_refresh=True):
        """
                add triple by providing p,o, assumes s = subject

                Args:
                        p (rdflib.term.URIRef): predicate
                        o (): object
                        auto_refresh (bool): whether or not to update object-like self.rdf.triples

                Returns:
                        None: adds triple to self.rdf.graph
                """
        self.rdf.graph.add((self.uri, p, self._handle_object(o)))
        self._handle_triple_refresh(auto_refresh)

    def set_triple(self, p, o, auto_refresh=True):
        """
                Assuming the predicate or object matches a single triple, sets the other for that triple.

                Args:
                        p (rdflib.term.URIRef): predicate
                        o (): object
                        auto_refresh (bool): whether or not to update object-like self.rdf.triples

                Returns:
                        None: modifies pre-existing triple in self.rdf.graph
                """
        self.rdf.graph.set((self.uri, p, self._handle_object(o)))
        self._handle_triple_refresh(auto_refresh)

    def remove_triple(self, p, o, auto_refresh=True):
        """
                remove triple by supplying p,o

                Args:
                        p (rdflib.term.URIRef): predicate
                        o (): object
                        auto_refresh (bool): whether or not to update object-like self.rdf.triples

                Returns:
                        None: removes triple from self.rdf.graph
                """
        self.rdf.graph.remove((self.uri, p, self._handle_object(o)))
        self._handle_triple_refresh(auto_refresh)

    def _handle_triple_refresh(self, auto_refresh):
        """
                method to refresh self.rdf.triples if auto_refresh or defaults set to True
                """
        if auto_refresh:
            self.parse_object_like_triples()
        elif auto_refresh == None and self.repo.default_auto_refresh:
            self.parse_object_like_triples()

    def update(self, sparql_query_only=False, auto_refresh=None, update_binary=True):
        """
                Method to update resources in repository.  Firing this method computes the difference in the local modified graph and the original one,
                creates an instance of SparqlUpdate and builds a sparql query that represents these differences, and sends this as a PATCH request.

                Note: send PATCH request, regardless of RDF or NonRDF, to [uri]/fcr:metadata

                If the resource is NonRDF (Binary), this also method also updates the binary data.

                Args:
                        sparql_query_only (bool): If True, returns only the sparql query string and does not perform any actual updates
                        auto_refresh (bool): If True, refreshes resource after update. If left None, defaults to repo.default_auto_refresh
                        update_binary (bool): If True, and resource is NonRDF, updates binary data as well

                Returns:
                        (bool)
                """
        self._diff_graph()
        sq = SparqlUpdate(self.rdf.prefixes, self.rdf.diffs)
        if sparql_query_only:
            return sq.build_query()
        response = self.repo.api.http_request('PATCH', '%s/fcr:metadata' % self.uri, data=sq.build_query(), headers={'Content-Type': 'application/sparql-update'})
        if response.status_code != 204:
            logger.debug(response.content)
            raise Exception('HTTP %s, expecting 204' % response.status_code)
        if type(self) == NonRDFSource and update_binary and type(self.binary.data) != requests.models.Response:
            self.binary._prep_binary()
            binary_data = self.binary.data
            binary_response = self.repo.api.http_request('PUT', self.uri, data=binary_data, headers={'Content-Type': self.binary.mimetype})
            if not auto_refresh and not self.repo.default_auto_refresh:
                logger.debug('not refreshing resource RDF, but updated binary, so must refresh binary data')
                updated_self = self.repo.get_resource(self.uri)
                self.binary.refresh(updated_self)
            if hasattr(self, '_post_update'):
                self._post_update()
            if auto_refresh:
                self.refresh(refresh_binary=update_binary)
        elif auto_refresh == None and self.repo.default_auto_refresh:
            self.refresh(refresh_binary=update_binary)
        return True

    def children(self, as_resources=False):
        """
                method to return hierarchical  children of this resource

                Args:
                        as_resources (bool): if True, opens each as appropriate resource type instead of return URI only

                Returns:
                        (list): list of resources
                """
        children = [o for s, p, o in self.rdf.graph.triples((None, self.rdf.prefixes.ldp.contains, None))]
        if as_resources:
            logger.debug('retrieving children as resources')
            children = [self.repo.get_resource(child) for child in children]
        return children

    def parents(self, as_resources=False):
        """
                method to return hierarchical parents of this resource

                Args:
                        as_resources (bool): if True, opens each as appropriate resource type instead of return URI only

                Returns:
                        (list): list of resources
                """
        parents = [o for s, p, o in self.rdf.graph.triples((None, self.rdf.prefixes.fedora.hasParent, None))]
        if as_resources:
            logger.debug('retrieving parent as resource')
            parents = [self.repo.get_resource(parent) for parent in parents]
        return parents

    def siblings(self, as_resources=False):
        """
                method to return hierarchical siblings of this resource.

                Args:
                        as_resources (bool): if True, opens each as appropriate resource type instead of return URI only

                Returns:
                        (list): list of resources
                """
        siblings = set()
        for parent in self.parents(as_resources=True):
            for sibling in parent.children(as_resources=as_resources):
                siblings.add(sibling)

        if as_resources:
            siblings.remove(self)
        if not as_resources:
            siblings.remove(self.uri)
        return list(siblings)

    def _affix_version(self, version_uri, version_label):
        version_resource = self.repo.get_resource(version_uri)
        rv = ResourceVersion(self, version_resource, version_uri, version_label)
        setattr(self.versions, version_label, rv)

    def create_version(self, version_label):
        """
                method to create a new version of the resource as it currently stands

                        - Note: this will create a version based on the current live instance of the resource,
                        not the local version, which might require self.update() to update.

                Args:
                        version_label (str): label to be used for version

                Returns:
                        (ResourceVersion): instance of ResourceVersion, also appended to self.versions
                """
        version_response = self.repo.api.http_request('POST', '%s/fcr:versions' % self.uri, data=None, headers={'Slug': version_label})
        if version_response.status_code == 201:
            logger.debug('version created: %s' % version_response.headers['Location'])
            self._affix_version(version_response.headers['Location'], version_label)

    def get_versions(self):
        """
                retrieves all versions of an object, and stores them at self.versions

                Args:
                        None

                Returns:
                        None: appends instances
                """
        versions_response = self.repo.api.http_request('GET', '%s/fcr:versions' % self.uri)
        versions_graph = self.repo.api.parse_rdf_payload(versions_response.content, versions_response.headers)
        for version_uri in versions_graph.objects(self.uri, self.rdf.prefixes.fedora.hasVersion):
            version_label = versions_graph.value(version_uri, self.rdf.prefixes.fedora.hasVersionLabel, None).toPython()
            self._affix_version(version_uri, version_label)

    def dump(self, format='ttl'):
        """
                Convenience method to return RDF data for resource,
                optionally selecting serialization format.
                Inspired by .dump from Samvera.

                Args:
                        format (str): expecting serialization formats accepted by rdflib.serialization(format=)
                """
        return self.rdf.graph.serialize(format=format).decode('utf-8')


class ResourceVersion(Resource):
    __doc__ = '\n\tClass to represent versions of a resource.\n\n\tVersions are spawned by the Resource class method resource.create_version(), or retrieved by resource.get_versions().\n\tVersions are stored in the resource instance at resource.versions\n\n\tArgs:\n\t\tversion_resource (Resource): retrieved and prased resource version\n\t\tversion_uri (rdflib.term.URIRef, str): uri of version\n\t\tversion_label (str): lable for version\n\t'

    def __init__(self, current_resource, version_resource, version_uri, version_label):
        self._current_resource = current_resource
        self.resource = version_resource
        self.uri = version_uri
        self.label = version_label

    def revert_to(self):
        """
                method to revert resource to this version by issuing PATCH

                Args:
                        None

                Returns:
                        None: sends PATCH request, and refreshes parent resource
                """
        response = self.resource.repo.api.http_request('PATCH', self.uri)
        if response.status_code == 204:
            logger.debug('reverting to previous version of resource, %s' % self.uri)
            self._current_resource.refresh()
        else:
            raise Exception('HTTP %s, could not revert to resource version, %s' % (response.status_code, self.uri))

    def delete(self):
        """
                method to remove version from resource's history
                """
        response = self.resource.repo.api.http_request('DELETE', self.uri)
        if response.status_code == 204:
            logger.debug('deleting previous version of resource, %s' % self.uri)
            delattr(self._current_resource.versions, self.label)
        else:
            if response.status_code == 400:
                raise Exception('HTTP 400, likely most recent resource version which cannot be removed')
            else:
                raise Exception('HTTP %s, could not delete resource version: %s' % (response.status_code, self.uri))


class BinaryData(object):
    __doc__ = '\n\tClass to handle binary data for NonRDFSource (Binary) resources\n\tBuilds out self.binary, and provides some method for setting/accessing binary data\n\n\tArgs:\n\t\tresource (NonRDFSource): instance of NonRDFSource resource\n\t'

    def __init__(self, resource, binary_data, binary_mimetype):
        self.resource = resource
        self.delivery = None
        self.data = binary_data
        self.stream = False
        self.mimetype = binary_mimetype
        self.location = None
        if self.resource.exists:
            self.parse_binary()

    def empty(self):
        """
                Method to empty attributes, particularly for use when
                object is deleted but remains as variable
                """
        self.resource = None
        self.delivery = None
        self.data = None
        self.stream = False
        self.mimetype = None
        self.location = None

    def refresh(self, updated_self):
        """
                method to refresh binary attributes and data

                Args:
                        updated_self (Resource): resource this binary data attaches to

                Returns:
                        None: updates attributes
                """
        logger.debug('refreshing binary attributes')
        self.mimetype = updated_self.binary.mimetype
        self.data = updated_self.binary.data

    def parse_binary(self):
        """
                when retrieving a NonRDF resource, parse binary data and make available
                via generators
                """
        self.mimetype = self.resource.rdf.graph.value(self.resource.uri, self.resource.rdf.prefixes.ebucore.hasMimeType).toPython()
        self.data = self.resource.repo.api.http_request('GET', self.resource.uri, data=None, headers={'Content-Type': self.resource.mimetype}, is_rdf=False, stream=True)

    def _prep_binary(self):
        """
                method is used to check/prep data and headers for NonRDFSource create or update

                Args:
                        None

                Returns:
                        None: sets attributes in self.binary and headers
                """
        logger.debug('preparing NonRDFSource data for create/update')
        self._prep_binary_mimetype()
        self._prep_binary_content()

    def _prep_binary_mimetype(self):
        """
                Sets Content-Type header based on headers and/or self.binary.mimetype values
                Implicitly favors Content-Type header if set

                Args:
                        None

                Returns:
                        None: sets attributes in self.binary and headers
                """
        if not self.mimetype and 'Content-Type' not in self.resource.headers.keys():
            raise Exception('to create/update NonRDFSource, mimetype or Content-Type header is required')
        elif self.mimetype and 'Content-Type' not in self.resource.headers.keys():
            logger.debug('setting Content-Type header with provided mimetype: %s' % self.mimetype)
            self.resource.headers['Content-Type'] = self.mimetype

    def _prep_binary_content(self):
        """
                Sets delivery method of either payload or header
                Favors Content-Location header if set

                Args:
                        None

                Returns:
                        None: sets attributes in self.binary and headers
                """
        if not self.data and not self.location and 'Content-Location' not in self.resource.headers.keys():
            raise Exception('creating/updating NonRDFSource requires content from self.binary.data, self.binary.location, or the Content-Location header')
        else:
            if 'Content-Location' in self.resource.headers.keys():
                logger.debug('Content-Location header found, using')
                self.delivery = 'header'
            else:
                if 'Content-Location' not in self.resource.headers.keys():
                    if self.location:
                        self.resource.headers['Content-Location'] = self.location
                        self.delivery = 'header'
                else:
                    if self.data:
                        if isinstance(self.data, io.BufferedIOBase):
                            logger.debug('detected file-like object')
                            self.delivery = 'payload'
                    else:
                        logger.debug('detected bytes')
                        self.delivery = 'payload'

    def range(self, byte_start, byte_end, stream=True):
        """
                method to return a particular byte range from NonRDF resource's binary data
                https://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html

                Args:
                        byte_start(int): position of range start
                        byte_end(int): position of range end

                Returns:
                        (requests.Response): streamable response
                """
        response = self.resource.repo.api.http_request('GET', self.resource.uri, data=None, headers={'Content-Type': self.mimetype, 
         'Range': 'bytes=%s-%s' % (byte_start, byte_end)}, is_rdf=False, stream=stream)
        if response.status_code == 206:
            return response
        raise Exception('HTTP %s, but was expecting 206' % response.status_code)


class NonRDFSource(Resource):
    __doc__ = '\n\tLinked Data Platform Non-RDF Source (LDP-NR)\n\tAn LDPR whose state is not represented in RDF. For example, these can be binary or text documents that do not have useful RDF representations.\n\thttps://www.w3.org/TR/ldp/\n\n\tNote: When a pre-existing NonRDFSource is retrieved, the binary data is stored under self.binary.data as a\n\tstreamable requests object.\n\n\tInherits:\n\t\tResource\n\n\tArgs:\n\t\trepo (Repository): instance of Repository class\n\t\turi (rdflib.term.URIRef,str): input URI\n\t\tresponse (requests.models.Response): defaults None, but if passed, populate self.data, self.headers, self.status_code\n\t\tbinary_data: optional, file data, accepts file-like object, raw data, or URL\n\t\tbinary_mimetype: optional, mimetype for provided data\n\t'

    def __init__(self, repo, uri=None, response=None, binary_data=None, binary_mimetype=None):
        self.mimetype = None
        super().__init__(repo, uri=uri, response=response)
        self.binary = BinaryData(self, binary_data, binary_mimetype)

    def fixity(self, response_format=None):
        """
                Issues fixity check, return parsed graph

                Args:
                        None

                Returns:
                        (dict): ('verdict':(bool): verdict of fixity check, 'premis_graph':(rdflib.Graph): parsed PREMIS graph from check)
                """
        if not response_format:
            response_format = self.repo.default_serialization
        response = self.repo.api.http_request('GET', '%s/fcr:fixity' % self.uri)
        fixity_graph = self.repo.api.parse_rdf_payload(response.content, response.headers)
        for outcome in fixity_graph.objects(None, self.rdf.prefixes.premis.hasEventOutcome):
            if outcome.toPython() == 'SUCCESS':
                verdict = True
            else:
                verdict = False

        return {'verdict': verdict, 
         'premis_graph': fixity_graph}


Binary = NonRDFSource

class RDFResource(Resource):
    __doc__ = '\n\tLinked Data Platform RDF Source (LDP-RS)\n\tAn LDPR whose state is fully represented in RDF, corresponding to an RDF graph. See also the term RDF Source from [rdf11-concepts].\n\thttps://www.w3.org/TR/ldp/\n\n\tSub-classed by:\n\t\tContainer\n\n\tInherits:\n\t\tResource\n\n\tArgs:\n\t\trepo (Repository): instance of Repository class\n\t\turi (rdflib.term.URIRef,str): input URI\n\t\tresponse (requests.models.Response): defaults None, but if passed, populate self.data, self.headers, self.status_code\n\t'

    def __init__(self, repo, uri=None, response=None):
        super().__init__(repo, uri=uri, response=response)


class Container(RDFResource):
    __doc__ = '\n\tLinked Data Platform Container (LDPC)\n\tA LDP-RS representing a collection of linked documents (RDF Document [rdf11-concepts] or information resources [WEBARCH]) that responds to client requests for creation, modification, and/or enumeration of its linked members and documents, and that conforms to the simple lifecycle patterns and conventions in section 5. Linked Data Platform Containers.\n\thttps://www.w3.org/TR/ldp/\n\n\tSub-classed by:\n\t\tBasicContainer, IndirectContainer, DirectContainer\n\n\tInherits:\n\t\tRDFResource\n\n\tArgs:\n\t\trepo (Repository): instance of Repository class\n\t\turi (rdflib.term.URIRef,str): input URI\n\t\tresponse (requests.models.Response): defaults None, but if passed, populate self.data, self.headers, self.status_code\n\t'

    def __init__(self, repo, uri=None, response=None):
        super().__init__(repo, uri=uri, response=response)


class BasicContainer(Container):
    __doc__ = '\n\tLinked Data Platform Basic Container (LDP-BC)\n\tAn LDPC that defines a simple link to its contained documents (information resources) [WEBARCH].\n\thttps://www.w3.org/TR/ldp/\n\n\thttps://gist.github.com/hectorcorrea/dc20d743583488168703\n\t\t- "The important thing to notice is that by posting to a Basic Container, the LDP server automatically adds a triple with ldp:contains predicate pointing to the new resource created."\n\n\tInherits:\n\t\tContainer\n\n\tArgs:\n\t\trepo (Repository): instance of Repository class\n\t\turi (rdflib.term.URIRef,str): input URI\n\t\tresponse (requests.models.Response): defaults None, but if passed, populate self.data, self.headers, self.status_code\n\t'

    def __init__(self, repo, uri=None, response=None):
        super().__init__(repo, uri=uri, response=response)


class DirectContainer(Container):
    __doc__ = '\n\tLinked Data Platform Direct Container (LDP-DC)\n\tAn LDPC that adds the concept of membership, allowing the flexibility of choosing what form its membership triples take, and allows members to be any resources [WEBARCH], not only documents.\n\thttps://www.w3.org/TR/ldp/\n\n\tWhen adding children, can also write relationships to another resource\n\n\tInherits:\n\t\tContainer\n\n\tArgs:\n\t\trepo (Repository): instance of Repository class\n\t\turi (rdflib.term.URIRef,str): input URI\n\t\tresponse (requests.models.Response): defaults None, but if passed, populate self.data, self.headers, self.status_code\n\t\tmembershipResource (rdflib.term.URIRef): resource that will accumlate triples as children are added\n\t\thasMemberRelation (rdflib.term.URIRef): predicate that will be used when pointing from URI in ldp:membershipResource to children\n\t'

    def __init__(self, repo, uri=None, response=None, membershipResource=None, hasMemberRelation=None):
        super().__init__(repo, uri=uri, response=response)
        self.add_triple(self.rdf.prefixes.rdf.type, self.rdf.prefixes.ldp.DirectContainer)
        self.membershipResource = membershipResource
        self.hasMemberRelation = hasMemberRelation
        if membershipResource:
            self.add_triple(self.rdf.prefixes.ldp.membershipResource, membershipResource)
        if hasMemberRelation:
            self.add_triple(self.rdf.prefixes.ldp.hasMemberRelation, hasMemberRelation)


class IndirectContainer(Container):
    __doc__ = '\n\tLinked Data Platform Indirect Container (LDP-IC)\n\tAn LDPC similar to a LDP-DC that is also capable of having members whose URIs are based on the content of its contained documents rather than the URIs assigned to those documents.\n\thttps://www.w3.org/TR/ldp/\n\n\tInherits:\n\t\tContainer\n\n\tArgs:\n\t\trepo (Repository): instance of Repository class\n\t\turi (rdflib.term.URIRef,str): input URI\n\t\tresponse (requests.models.Response): defaults None, but if passed, populate self.data, self.headers, self.status_code\n\t\tmembershipResource (rdflib.term): resource that will accumlate triples as children are added\n\t\thasMemberRelation (rdflib.term): predicate that will be used when pointing from URI in ldp:membershipResource to ldp:insertedContentRelation\n\t\tinsertedContentRelation (rdflib.term): destination for ldp:hasMemberRelation from ldp:membershipResource\n\t'

    def __init__(self, repo, uri=None, response=None, membershipResource=None, hasMemberRelation=None, insertedContentRelation=None):
        super().__init__(repo, uri=uri, response=response)
        self.add_triple(self.rdf.prefixes.rdf.type, self.rdf.prefixes.ldp.IndirectContainer)
        self.membershipResource = membershipResource
        self.hasMemberRelation = hasMemberRelation
        self.insertedContentRelation = insertedContentRelation
        if membershipResource:
            self.add_triple(self.rdf.prefixes.ldp.membershipResource, membershipResource)
        if hasMemberRelation:
            self.add_triple(self.rdf.prefixes.ldp.hasMemberRelation, hasMemberRelation)
        if insertedContentRelation:
            self.add_triple(self.rdf.prefixes.ldp.insertedContentRelation, insertedContentRelation)