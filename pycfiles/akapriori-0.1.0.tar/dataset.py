# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Library/Python/2.6/site-packages/akamu/config/dataset.py
# Compiled at: 2013-06-13 09:04:13
__doc__ = '\nManage connection to and querying over an RDF dataset\nfor an Akara web application\n\nRequires a configuration section, for example:\n\nclass dataset:\n    mysqlDataset = {\n        \'type\'         : "MySQL",\n        \'mysqldb\'      : "[..]",\n        \'mysqluser\'    : "[..]",\n        \'mysqlhost\'    : "[..]",\n        \'mysqlpw\'      : "[..]",\n        \'mysqlStoreId\' : "[..]",\n        \'mysqlPort\'    : "[..]"\n    }\n\n    #result XSLT directory\n    result_xslt_directory = ".. /path/to/xslt/dir .."\n\n    #Graph store to back GSP\n    graph_store_name         = " .. dataset name .."\n    graph_store_url          = " .. URL of GSP .."\n    external_graph_store_url = ".. external URL of GSP (if different from above) .."\n\n    #Triclops configuration\n    datastore_owl = "/path/to/owl/file"\n    debugQuery = True|False\n    NO_BASE_RESOLUTION = True|False\n    IgnoreQueryDataset = True|False\n    endpointURL        = .. see: http://www.w3.org/TR/sparql11-service-description/#sd-endpoint ..\n\n    sparqlQueryFiles = "/path/to/query/files"\n    nsPrefixes       = { "..prefix.." : rdflib.Namespace  }\n\n    sqlLiteralProps  = [ .., .., .. ]\n    sqlResourceProps = [ .., .., .. ]\n'
import os, akara, time
from akara import registry
from rdflib import plugin, URIRef, OWL, RDFS, RDF, BNode
from rdflib.store import Store, NO_STORE
from rdflib.Graph import Graph, ConjunctiveGraph
from rdflib.store.SPARQL import GET, POST
OWL_PROPERTIES_QUERY = '\nSELECT ?literalProperty ?resourceProperty\nWHERE {\n    { ?literalProperty a owl:DatatypeProperty }\n                    UNION\n    { ?resourceProperty a ?propType\n      FILTER(\n        ?propType = owl:ObjectProperty ||\n        ?propType = owl:TransitiveProperty ||\n        ?propType = owl:SymmetricProperty ||\n        ?propType = owl:InverseFunctionalProperty )  }\n}'

def GetGraphStoreForProtocol():
    configDict = akara.module_config()
    return (
     configDict.get('graph_store_name'), configDict.get('graph_store_url'))


def GetExternalGraphStoreURL():
    configDict = akara.module_config()
    return configDict.get('external_graph_store_url')


def ConfigureTriclops(datasetName, nsBindings, litProps, resProps):
    """
    Adapts akara configuration to Triclops configuration
    """
    datasetConfig = akara.module_config().get(datasetName)
    connectStr = 'user=%s,password=%s,db=%s,port=%s,host=%s' % (
     datasetConfig.get('mysqluser'),
     datasetConfig.get('mysqlpw'),
     datasetConfig.get('mysqldb'),
     datasetConfig.get('mysqlPort', 3306),
     datasetConfig.get('mysqlhost'))
    triclopsConf = {'result_xslt_directory': akara.module_config().get('result_xslt_directory'), 
       'store_identifier': datasetConfig.get('mysqlStoreId'), 
       'connection': connectStr, 
       'store': datasetConfig.get('type'), 
       'debugQuery': akara.module_config().get('debugQuery', False), 
       'NO_BASE_RESOLUTION': akara.module_config().get('NO_BASE_RESOLUTION', False), 
       'IgnoreQueryDataset': akara.module_config().get('IgnoreQueryDataset', False), 
       'MYSQL_ORDER': datasetConfig.get('MYSQL_ORDER', False), 
       'endpointURL': akara.module_config().get('endpointURL')}
    proxy = None
    nsBindings = dict([ (k, URIRef(v)) for (k, v) in akara.module_config().get('nsPrefixes', {}).items() ])
    dataStoreOWL = akara.module_config().get('datastore_owl')
    dataStoreOntGraph = Graph()
    if not proxy and datasetConfig.get('type') == 'MySQL':
        litProps.update(OWL.literalProperties)
        litProps.update(RDFS.literalProperties)
        resProps.update(RDFS.resourceProperties)
        litProps.update(map(URIRef, akara.module_config().get('sqlLiteralProps', [])))
        resProps.update(map(URIRef, akara.module_config().get('sqlResourceProps', [])))
        if dataStoreOWL:
            for dsOwl in dataStoreOWL.split(','):
                dataStoreOntGraph.parse(dsOwl)

            for (litProp, resProp) in dataStoreOntGraph.query(OWL_PROPERTIES_QUERY, initNs={'owl': OWL_NS}):
                if litProp:
                    litProps.add(litProp)
                if resProp:
                    if (
                     resProp,
                     RDF.type,
                     OWL.DatatypeProperty) not in dataStoreOntGraph:
                        resProps.add(resProp)

        else:
            triclopsConf['datastore_owl'] = 'N/A'
        print 'Registered %s owl:DatatypeProperties' % len(litProps)
        print 'Registered %s owl:ObjectProperties' % len(resProps)
        if False:
            pass
    return triclopsConf


def ReplaceGraph(datasetOrName, graphUri, srcStream, format='xml', storeName=True, baseUri=None, smartDiff=False, debug=False):
    store = ConnectToDataset(datasetOrName) if storeName else datasetOrName
    g = Graph(store, graphUri)
    if smartDiff:

        def hasBNodes(triple):
            return filter(lambda term: isinstance(term, BNode), triple)

        new_graph = Graph().parse(srcStream, publicID=baseUri)
        stmsToAdd = [ s for s in new_graph if s not in g or hasBNodes(s)
                    ]
        stmsToDel = [ s for s in g if s not in new_graph or hasBNodes(s)
                    ]
        for s in stmsToDel:
            g.remove(s)

        for s in stmsToAdd:
            g.add(s)

        if debug:
            print 'Removed %s triples and added %s from/to %s' % (
             len(stmsToDel),
             len(stmsToAdd),
             graphUri)
    else:
        g.remove((None, None, None))
        g.parse(srcStream, publicID=baseUri)
    store.commit()
    return


def ClearGraph(datasetOrName, graphUri, storeName=True):
    store = ConnectToDataset(datasetOrName) if storeName else datasetOrName
    g = Graph(store, graphUri)
    g.remove((None, None, None))
    store.commit()
    return


def DestroyOrCreateDataset(datasetName):
    """
    Initialize dataset (if exists) or create it if it doesn't
    """
    datasetConfig = akara.module_config().get(datasetName)
    assert datasetConfig is not None, datasetName
    if datasetConfig['type'] == 'MySQL':
        configStr = 'user=%s,password=%s,db=%s,port=%s,host=%s' % (
         datasetConfig.get('mysqluser'),
         datasetConfig.get('mysqlpw'),
         datasetConfig.get('mysqldb'),
         datasetConfig.get('mysqlPort', 3306),
         datasetConfig.get('mysqlhost'))
        store = plugin.get('MySQL', Store)(datasetConfig.get('mysqlStoreId'))
        rt = store.open(configStr, create=False)
        if rt == NO_STORE:
            store.open(configStr, create=True)
        else:
            store.destroy(configStr)
            store.open(configStr, create=True)
        return store
    else:
        raise NotImplementedError('Only dataset supported by Akamu is MySQL')
        return


def ConnectToDataset(datasetName):
    """
    Return rdflib store corresponding to the named dataset, whose connection
    parameters are specified in the configuration file
    """
    datasetConfig = akara.module_config().get(datasetName)
    assert datasetConfig is not None
    if datasetConfig['type'] == 'MySQL':
        configStr = 'user=%s,password=%s,db=%s,port=%s,host=%s' % (
         datasetConfig.get('mysqluser'),
         datasetConfig.get('mysqlpw'),
         datasetConfig.get('mysqldb'),
         datasetConfig.get('mysqlPort', 3306),
         datasetConfig.get('mysqlhost'))
        store = plugin.get('MySQL', Store)(datasetConfig.get('mysqlStoreId'))
        store.open(configStr, create=False)
        store.literal_properties.update(map(URIRef, akara.module_config().get('sqlLiteralProps', [])))
        store.resource_properties.update(map(URIRef, akara.module_config().get('sqlResourceProps', [])))
        return store
    else:
        if datasetConfig['type'] == 'SPARQLService':
            if 'endpoint' not in datasetConfig:
                raise SyntaxError('Missing "endpoint" directive')
            sparql_store = plugin.get('SPARQL', Store)(datasetConfig.get('endpoint'))
            for (k, v) in datasetConfig.get('extraQueryParams', {}).items():
                sparql_store._querytext.append((k, v))

            sparql_store.method = POST if datasetConfig.get('method', 'GET').lower() == 'post' else GET
            return sparql_store
        raise NotImplementedError('Only dataset supported by Akamu is MySQL')
        return


def Ask(queryFile, datasetName, graphUri=None, params=None, debug=False):
    """
    Same as Query but where query is ASK (returns boolean)
    """
    store = ConnectToDataset(datasetName)
    g = ConjunctiveGraph(store) if graphUri is None else Graph(store, graphUri)
    qFile = os.path.join(akara.module_config().get('sparqlQueryFiles'), queryFile)
    query = open(qFile).read()
    query = query if params is None else query % params
    if debug:
        print query
    initNs = dict([ (k, URIRef(v)) for (k, v) in akara.module_config().get('nsPrefixes', {}).items() ])
    if debug:
        then = time.time()
        rt = g.query(query, initNs=initNs, DEBUG=debug).serialize(format='python')
        print 'Query time', time.time() - then
    else:
        rt = g.query(query, initNs=initNs, DEBUG=debug).serialize(format='python')
    return rt


def Query(queryFile, datasetName, graphUri=None, params=None, debug=False):
    """
    Evaluate a query (stored in a SPARQL file in the location indicated in the
    configuration) against the given dataset (and optional named graph within it)
    using the optional parameters given
    """
    store = ConnectToDataset(datasetName)
    g = ConjunctiveGraph(store) if graphUri is None else Graph(store, graphUri)
    qFile = os.path.join(akara.module_config().get('sparqlQueryFiles'), queryFile)
    query = open(qFile).read()
    query = query if params is None else query % params
    if debug:
        print query
    initNs = dict([ (k, URIRef(v)) for (k, v) in akara.module_config().get('nsPrefixes', {}).items() ])
    for rt in g.query(query, initNs=initNs, DEBUG=debug):
        yield rt

    return


def GetParameterizedQuery(queryFile, params=None):
    qFile = os.path.join(akara.module_config().get('sparqlQueryFiles'), queryFile)
    query = open(qFile).read()
    if params is None:
        return query
    else:
        return query % params