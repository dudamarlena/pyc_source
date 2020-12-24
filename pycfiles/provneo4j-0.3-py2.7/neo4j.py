# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/provneo4j/connectors/neo4j_rest/neo4j.py
# Compiled at: 2016-10-26 07:49:18
import logging
from prov.model import QualifiedName, ProvRelation, ProvElement
from neo4jrestclient.client import GraphDatabase, StatusException, Node, Relationship
from prov.constants import PROV_MENTION, PROV_ATTR_BUNDLE, PROV_ATTR_GENERAL_ENTITY, PROV_ATTR_SPECIFIC_ENTITY
from provneo4j.prov_to_graph import prov_to_graph_flattern
from provneo4j.connectors.connector import *
from datetime import datetime
DOC_PROPERTY_NAME_ID = 'document:id'
DOC_PROPERTY_BUNDLE_ID = 'document:bundleId'
DOC_PROPERTY_NAME_LABEL = 'document:label'
DOC_RELATION_TYPE = 'relation:type'
DOC_PROPERTY_NAME_PROPERTIES_TYPES = 'document:properties_types'
DOC_PROPERTY_NAME_BUNDLES = 'document:bundles'
DOC_PROPERTY_NAME_NAMESPACE_URI = 'namespace:uri'
DOC_PROPERTY_NAME_NAMESPACE_PREFIX = 'namespace:prefix'
DOC_PROPERTY_MAP = [
 DOC_PROPERTY_NAME_ID,
 DOC_PROPERTY_NAME_BUNDLES,
 DOC_PROPERTY_NAME_NAMESPACE_URI,
 DOC_PROPERTY_NAME_NAMESPACE_PREFIX,
 DOC_PROPERTY_NAME_LABEL,
 DOC_RELATION_TYPE,
 DOC_PROPERTY_NAME_PROPERTIES_TYPES,
 DOC_PROPERTY_BUNDLE_ID]
DOC_GET_DOC_BY_ID = ' MATCH (d)-[r]-(x) WHERE not((d)-[:%s]-(x)) and (d.`document:id`)=%i\n                        RETURN d as from, r as rel, x as to\n                    '
DOC_GET_BUNDLES = ' MATCH (b:`prov:Bundle`) WHERE (b.`document:id`)=%i RETURN b '
DOC_GET_BUNDLE_BY_ID = ' MATCH (b:`prov:Bundle`) WHERE (b.`bundle:id`)=%i RETURN b '
DOC_GET_METTION_OF_TARGET = " MATCH (n:`prov:Bundle`)-[r]-(x)\n                                WHERE (n.`document:id`)=%i\n                                AND n.`document:label` = '%s'\n                                AND x.`document:label` = '%s'\n                                RETURN x\n                                LIMIT 1"
DOC_GET_DOC_BY_ID_WITHOUT_CONNECTIONS = '\n                        MATCH (a) WHERE (a.`document:id`)=%i AND NOT (a)<-[]->()\n                        RETURN a as alone\n                        UNION\n                        MATCH (a)-[r:includeIn]->()\n                        WITH a,count(r) as relation_count\n                        WHERE (a.`document:id`)=%i AND relation_count=1 RETURN a as alone\n                    '
DOC_DELETE_BY_ID = 'MATCH (d) WHERE (d.`document:id`)=%i DETACH DELETE d'
BUNDLE_LABEL_NAME = 'prov:Bundle'
BUNDLE_RELATION_NAME = 'includeIn'
logger = logging.getLogger(__name__)
from neo4j_serializer import Neo4jRestSerializer
from neo4j_deserializer import Neo4JRestDeserializer

class Neo4J(Connector):
    _base_url = None
    _user_name = None
    _user_password = None
    _connection = None

    def __init__(self):
        pass

    def connect(self, base_url=None, username=None, user_password=None):
        if base_url is None:
            raise InvalidCredentialsException('Please specify a base_url to connect to the database')
        else:
            self._base_url = base_url.rstrip('/')
        self._user_name = username
        self._user_password = user_password
        if self._user_name is not None and self._user_password is not None:
            auth = {'username': self._user_name, 'password': self._user_password}
        try:
            self._connection = GraphDatabase(self._base_url, **auth)
        except StatusException as e:
            if e.value == 401:
                raise InvalidCredentialsException('You used the username: %s and password %s ' % (user_password, user_password))
            else:
                raise e

        return

    def get_id_from_db_node(self, db_node):
        return db_node.properties.get(DOC_PROPERTY_NAME_ID)

    def get_document(self, document_id, prov_format=ProvDocument):
        prov_document = self.get_bundle(document_id, prov_format)
        results_bundles = self._connection.query(q=DOC_GET_BUNDLES % document_id, returns=Node)
        if len(results_bundles) > 0:
            for db_bundle in reduce(lambda x, y: x + y, results_bundles):
                bundle_id = db_bundle.get(DOC_PROPERTY_BUNDLE_ID)
                bundle_label = db_bundle.get(DOC_PROPERTY_NAME_LABEL)
                bundle = self.get_bundle(bundle_id=bundle_id, bundle_identifier=bundle_label, parent_prov_document=prov_document)

        return prov_document

    def get_bundles(self, document_id):
        results = self._connection.query(q=DOC_GET_BUNDLES % document_id, returns=Node)
        transformed_results = []
        if len(results) > 0:
            for db_bundle in reduce(lambda x, y: x + y, results):
                bundle_id = db_bundle.get(DOC_PROPERTY_BUNDLE_ID)
                bundle_label = db_bundle.get(DOC_PROPERTY_NAME_LABEL)
                transformed_results.append({'id': bundle_id, 
                   'identifier': bundle_label, 
                   'created_at': str(datetime(2012, 12, 12, 14, 7, 48))})

        return transformed_results

    def get_bundle(self, bundle_id, prov_format=ProvDocument, parent_prov_document=None, bundle_identifier=None):
        results = self._connection.query(q=DOC_GET_DOC_BY_ID % (BUNDLE_RELATION_NAME, bundle_id), returns=(
         Node, Relationship, Node))
        results_nodes_without_relations = None
        if len(results) == 0:
            results_nodes_without_relations = self._connection.query(q=DOC_GET_DOC_BY_ID_WITHOUT_CONNECTIONS % (bundle_id, bundle_id), returns=Node)
            if len(results_nodes_without_relations) == 0:
                raise NotFoundException("We can't find the document with the id %i" % bundle_id)
        if parent_prov_document is not None:
            bundle_document = parent_prov_document.bundle(bundle_identifier)
        else:
            bundle_document = ProvDocument()
        all_records = {}
        deserializer = Neo4JRestDeserializer()
        for db_from_node, db_relation, db_to_node in results:
            deserializer.add_namespace(db_from_node, bundle_document)
            deserializer.add_namespace(db_to_node, bundle_document)
            deserializer.add_namespace(db_relation, bundle_document)
            all_keys = all_records.keys()
            if db_from_node.id not in all_keys and self.get_id_from_db_node(db_from_node) == bundle_id:
                all_records.update({int(db_from_node.id): deserializer.create_record(bundle_document, db_from_node)})
            if db_to_node.id not in all_keys and self.get_id_from_db_node(db_to_node) == bundle_id:
                all_records.update({int(db_to_node.id): deserializer.create_record(bundle_document, db_to_node)})
            if db_relation.id not in all_keys and self.get_id_from_db_node(db_relation.start) == bundle_id:
                all_records.update({int(db_relation.id): deserializer.create_relation(bundle_document, db_relation)})

        if results_nodes_without_relations is None:
            results_nodes_without_relations = self._connection.query(q=DOC_GET_DOC_BY_ID_WITHOUT_CONNECTIONS % (bundle_id, bundle_id), returns=Node)
        if len(results_nodes_without_relations) > 0:
            for db_node in reduce(lambda x, y: x + y, results_nodes_without_relations):
                deserializer.add_namespace(db_node, bundle_document)
                all_records.update({int(db_node.id): deserializer.create_record(bundle_document, db_node)})

        if prov_format is ProvDocument:
            return bundle_document
        else:
            raise NotImplementedException('Neo4j connector only supports ProvDocument format for the get_document operation')
            return

    def _post_bundle_links(self, document_id, bundle):
        all_relations = bundle.get_records(ProvRelation)
        for relation in all_relations:
            if relation.get_type() == PROV_MENTION:
                attr_dict = dict(relation.attributes)
                target_bundle_label = attr_dict.get(PROV_ATTR_BUNDLE)
                target_label = attr_dict.get(PROV_ATTR_GENERAL_ENTITY)
                to_node_results = self._connection.query(q=DOC_GET_METTION_OF_TARGET % (document_id, target_bundle_label, target_label), returns=Node)
                if len(to_node_results) != 1:
                    InvalidDataException('The result of this query should be 1 node but the length was %i' % len(to_node_results))
                db_to_node = list(to_node_results).pop().pop()
                from_label = attr_dict.get(PROV_ATTR_SPECIFIC_ENTITY)
                from_node_results = self._connection.query(q=DOC_GET_METTION_OF_TARGET % (document_id, bundle.identifier, from_label), returns=Node)
                if len(from_node_results) != 1:
                    InvalidDataException('The result of this query should be 1 node but the length was %i' % len(from_node_results))
                db_from_node = list(from_node_results).pop().pop()
                serializer = Neo4jRestSerializer(self._connection)
                db_relation = serializer.create_relation(db_from_node, db_to_node, relation)
                serializer.add_namespaces(db_relation, relation)
                serializer.add_propety_map(db_relation, relation)

    def _post_bundle(self, bundle, parent_document_id=None, identifier=None):
        gdb = self._connection
        g = prov_to_graph_flattern(bundle)
        db_nodes = {}
        serializer = Neo4jRestSerializer(self._connection)
        nodes = bundle.get_records(ProvElement)
        nodes = list(set(nodes + g.nodes()))
        for node in nodes:
            db_nodes[node] = serializer.create_node(node)

        if parent_document_id is not None:
            if identifier is None:
                identifier = bundle.identifier
            if not isinstance(identifier, QualifiedName):
                identifier = Neo4JRestDeserializer.valid_qualified_name(bundle, identifier)
            else:
                identifier = bundle.identifier
            db_nodes[identifier] = serializer.create_bundle_node(bundle, identifier)
        if len(nodes) is not 0:
            bundle_id = db_nodes.values()[0]
        else:
            raise InvalidDataException('Please provide a document with at least one node')
        with gdb.transaction() as (tx):
            for from_node, to_node, relations in g.edges_iter(data=True):
                for key, relation in relations.iteritems():
                    if relation.get_type() != PROV_MENTION:
                        db_from_node = db_nodes[from_node]
                        db_to_node = db_nodes[to_node]
                        db_nodes[relation] = serializer.create_relation(db_from_node, db_to_node, relation)
                    else:
                        db_nodes[to_node].delete()
                        del db_nodes[to_node]

            if parent_document_id is not None:
                for record in bundle.get_records(ProvElement):
                    db_to_bundle = db_nodes[identifier]
                    db_from_node = db_nodes[record]
                    relation = serializer.create_bundle_relation(db_from_node, db_to_bundle)

        for graph_node, db_node in db_nodes.iteritems():
            if type(graph_node) is QualifiedName:
                serializer.add_bundle_id(db_node, bundle_id.id, parent_document_id)
                serializer.add_namespaces(db_node, graph_node)
            elif isinstance(graph_node, ProvElement):
                serializer.add_id(db_node, bundle_id.id)
                serializer.add_namespaces(db_node, graph_node)
                serializer.add_propety_map(db_node, graph_node)
            elif isinstance(graph_node, ProvRelation):
                serializer.add_namespaces(db_node, graph_node)
                serializer.add_propety_map(db_node, graph_node)
            else:
                raise InvalidDataException('unknown type: %s' % type(graph_node))

        return db_nodes

    def post_document(self, prov_document, name=None):
        if len(name) == 0:
            raise InvalidDataException('Please provide a name for the document')
        all_db_nodes = self._post_bundle(prov_document)
        all_db_nodes_list = filter(lambda value: isinstance(value, Node), all_db_nodes.values())
        doc_id = self.get_id_from_db_node(all_db_nodes_list[0])
        for bundle in prov_document.bundles:
            self._post_bundle(bundle, doc_id)

        for bundle in prov_document.bundles:
            self._post_bundle_links(doc_id, bundle)

        return doc_id

    def delete_doc(self, document_id):
        self._connection.query(q=DOC_DELETE_BY_ID % document_id)
        return True

    def add_bundle(self, document_id, bundle_document, identifier):
        bundle_doc_id = self._post_bundle(bundle_document, parent_document_id=document_id, identifier=identifier)
        print 'end'