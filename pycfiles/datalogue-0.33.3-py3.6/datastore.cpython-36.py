# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/datalogue/models/datastore.py
# Compiled at: 2020-04-14 15:37:55
# Size of source mod 2**32: 40146 bytes
from abc import ABC, abstractmethod
from typing import Dict, List, Set, Optional, Union
from uuid import UUID
from datalogue.errors import _enum_parse_error, DtlError
from datalogue.models.kinesis.shards import ShardAttributes
from datalogue.models.schema import AbstractDataSchema, SchemaNode, Classification
from datalogue.utils import _parse_list, _parse_string_list, SerializableStringEnum

class NodeClassification:
    __doc__ = '\n    The mapping of a class to a field, as applied using the add, remove, and override commands of the dtl.datastore client.\n\n    :param schema_node_id: the id of a schema field\n    :param ontology_node_id: the class of a schema field\n    :param score: the Confidence score for the classification, from 0.0 - 1.0 (defaults to 1.0)\n    '

    def __init__(self, schema_node_id: Union[(str, UUID)], ontology_node_id: Union[(str, UUID)], score: float=1.0):
        self.schema_node_id = schema_node_id
        self.ontology_node_id = ontology_node_id
        self.score = score

    def __repr__(self):
        return f"{self.__class__.__name__}(schema_node_id: {self.schema_node_id!r}, ontology_node_id: {self.ontology_node_id!r},score: {self.score!r}, "

    def _as_payload(self) -> Union[(DtlError, dict)]:
        """
        Dictionary representation of the object with camelCase keys
        :return:
        """
        return {'schemaNodeId':str(self.schema_node_id), 
         'classId':str(self.ontology_node_id), 
         'score':str(self.score)}


class CredentialType(SerializableStringEnum):
    S3 = 'S3'
    GCS = 'GCS'
    Azure = 'Azure'
    JDBC = 'Jdbc'
    Mongo = 'Mongo'
    Http = 'Http'
    Socrata = 'Socrata'
    FileSystem = 'FileSystem'
    Void = 'Void'
    Kinesis = 'Kinesis'
    Hadoop = 'Hadoop'
    Kafka = 'Kafka'
    Minio = 'Minio'
    HadoopAzure = 'HadoopAzure'

    @staticmethod
    def parse_error(s: str) -> DtlError:
        return DtlError(_enum_parse_error('store type', s))

    @staticmethod
    def credential_type_from_str(string: str) -> Union[(DtlError, 'CredentialType')]:
        return SerializableStringEnum.from_str(CredentialType)(string)


class EncryptionType(SerializableStringEnum):
    AES256 = 'AES256'
    KeyId = 'KeyId'
    CustomerKey = 'CustomerKey'

    @staticmethod
    def parse_error(s: str) -> DtlError:
        return DtlError(_enum_parse_error('encryption type', s))

    @staticmethod
    def encryption_type_from_str(string: str) -> Union[(DtlError, 'EncryptionType')]:
        return SerializableStringEnum.from_str(EncryptionType)(string)


class FileFormat(SerializableStringEnum):
    Json = 'Json'
    Csv = 'Csv'
    Text = 'Text'
    Xml = 'Xml'
    Html = 'Html'
    Excel = 'Excel'
    Avro = 'Avro'
    Parquet = 'Parquet'

    @staticmethod
    def parse_error(s: str) -> DtlError:
        return DtlError(_enum_parse_error('file format', s))

    @staticmethod
    def file_format_from_str(string: str) -> Union[(DtlError, 'FileFormat')]:
        return SerializableStringEnum.from_str(FileFormat)(string)


class DatastoreDef(ABC):
    type_field = 'type'
    id_field = 'id'

    def __init__(self, credential_type, datastore_id=None):
        self.type = credential_type
        self.datastore_id = datastore_id
        super().__init__()

    def __eq__(self, other: 'DatastoreDef'):
        if isinstance(self, other.__class__):
            return self._as_payload() == other._as_payload()
        else:
            return False

    def _base_payload(self) -> dict:
        base = [(DatastoreDef.type_field, self.type.value)]
        if self.datastore_id is not None:
            base.append((DatastoreDef.id_field, str(self.datastore_id)))
        return dict(base)

    @abstractmethod
    def _as_payload(self) -> dict:
        """
        Dictionary representation of the object
        :return:
        """
        pass


class Cell:
    __doc__ = '\n        Describes a cell in html table\n    '

    def __init__(self, label: str, span: int, index: int, total: int, tag: str, tagOverrides: []=None):
        """
        Builds a cell

        :param label: text to display
        :param span: the html column span attribute
        :param index: index of this cell in the row
        :param total: total number of cells in the row
        """
        self.label = label
        self.span = span
        self.index = index
        self.total = total
        self.tag = tag
        self.tagOverrides = tagOverrides

    def __repr__(self):
        return f"{self.__class__.__name__}(label: {self.label!r}, span: {self.span!r},                 index: {self.index!r}, total: {self.total!r}, tag: {self.tag!r}, tagOverrides: {self.tagOverrides!r})"


def _cell_from_payload(json: dict) -> Union[(DtlError, Cell)]:
    label = json.get('label')
    if label is None:
        return DtlError("Cell has to have a 'label' key")
    span = json.get('span')
    if span is None:
        return DtlError("Cell has to have a 'span' key")
    index = json.get('index')
    if index is None:
        return DtlError("Cell has to have an 'index' key")
    else:
        total = json.get('total')
        if total is None:
            return DtlError("Cell has to have a 'total' key")
        return Cell(label, span, index, total, json.get('tag'), json.get('tagOverrides'))


class Datastore:
    __doc__ = '\n    Represents a pointer to a datastore\n    '

    def __init__(self, name: str, definition: DatastoreDef, credential_id: Optional[UUID]=None, alias: Optional[str]=None, datastore_id: Optional[UUID]=None, samples: Optional[List[List[Cell]]]=None, schema_paths: Optional[List[List[str]]]=None, schema_classes: Optional[List[List[str]]]=None, schema_labels: Optional[Set[str]]=None, schema_nodes: Optional[List[SchemaNode]]=None, ads: Optional[AbstractDataSchema]=None):
        """
        Builds a pointer to a datastore

        :param name: name of the pointer
        :param alias: unique alias accross the organization for the pointer
        :param definition: definition on how to access the data
        :param credential_id: reference to the Credential to access the data
        :param datastore_id: defined if the object was persisted, otherwise None
        :param samples: list of samples that were found in the data source
        :param schema_paths: Used to replace paths options on the cli
        :param schema_classes: Used to replace classes options on the cli
        :param schema_labels: Set of labels that exists in schema
        """
        self.id = datastore_id
        self.name = name
        self.alias = alias
        self.definition = definition
        self.definition.datastore_id = datastore_id
        self.credential_id = credential_id
        self.samples = samples
        self.schema_paths = schema_paths
        self.schema_classes = schema_classes
        self.schema_labels = schema_labels
        self.schema_nodes = schema_nodes
        self.ads = ads

    def __eq__(self, other: 'Datastore'):
        if isinstance(self, other.__class__):
            return self._as_payload() == other._as_payload()
        else:
            return False

    def __repr__(self):
        return f"{self.__class__.__name__}(id: {self.id}, name: {self.name!r}, alias: {self.alias!r}, credential_id: {self.credential_id}, definition: {self.definition!r}, samples: {self.samples!r}, schema_paths: {self.schema_paths!r}, schema_labels: {self.schema_labels!r}, schema_nodes: {self.schema_nodes!r})"

    def _as_payload(self) -> dict:
        """
        Dictionary representation of the object
        :return:
        """
        base = {'name':self.name, 
         'gate':self.definition._as_payload()}
        if self.id is not None:
            base['id'] = str(self.id)
        if self.alias is not None:
            base['alias'] = self.alias
        if self.credential_id is not None:
            base['credentialsId'] = str(self.credential_id)
        return base


class S3DatastoreDef(DatastoreDef):
    type_str = CredentialType.S3

    def __init__(self, bucket: str, key: str, file_format: FileFormat, params: Optional[Dict[(str, str)]]=None, datastore_id: Optional[UUID]=None):
        DatastoreDef.__init__(self, S3DatastoreDef.type_str, datastore_id)
        self.bucket = bucket
        self.key = key
        self.file_format = file_format
        self.params = params

    def __repr__(self):
        return f"{self.__class__.__name__}(bucket: {self.bucket!r}, key: {self.key!r}, file_format: {self.file_format!r}, params: {self.params})"

    def _as_payload(self) -> dict:
        """
        Dictionary representation of the object with camelCase keys
        :return:
        """
        base = self._base_payload()
        base['bucket'] = self.bucket
        base['key'] = self.key
        base['format'] = self.file_format.value
        if self.params is not None:
            base['params'] = self.params
        return base


def _s3_datastore_def_from_payload(d: dict) -> Union[(DtlError, S3DatastoreDef)]:
    type_field = d.get(DatastoreDef.type_field)
    if not isinstance(type_field, str):
        return DtlError('string %s is missing from the json' % DatastoreDef.type_field)
    if type_field != S3DatastoreDef.type_str.value:
        return DtlError('The object %s is not an S3 definition' % str(d))
    bucket = d.get('bucket')
    if bucket is None:
        return DtlError("'bucket' needs to be defined in an S3 definition")
    key = d.get('key')
    if key is None:
        return DtlError("'key' needs to be defined in an S3 definition")
    file_format = d.get('format')
    if file_format is None:
        return DtlError("'file_format' needs to be defined in an S3 definition")
    else:
        file_format = FileFormat.file_format_from_str(file_format)
        if isinstance(file_format, DtlError):
            return file_format
        params = d.get('params')
        datastore_id = d.get(DatastoreDef.id_field)
        return S3DatastoreDef(bucket, key, file_format, params, datastore_id)


class GCSDatastoreDef(DatastoreDef):
    type_str = CredentialType.GCS

    def __init__(self, bucket: str, file_name: str, file_format: FileFormat, params: Optional[Dict[(str, str)]]=None, datastore_id: Optional[UUID]=None):
        DatastoreDef.__init__(self, GCSDatastoreDef.type_str, datastore_id)
        self.bucket = bucket
        self.file_name = file_name
        self.file_format = file_format
        self.params = params

    def __repr__(self):
        return f"{self.__class__.__name__}(bucket: {self.bucket!r}, file_name: {self.file_name!r}, file_format: {self.file_format!r}, params: {self.params})"

    def _as_payload(self) -> dict:
        """
        Dictionary representation of the object  with camelCase keys
        :return:
        """
        base = self._base_payload()
        base['bucket'] = self.bucket
        base['fileName'] = self.file_name
        base['format'] = self.file_format.value
        if self.params is not None:
            base['params'] = self.params
        return base


def _gcs_datastore_def_from_payload(d: dict) -> Union[(DtlError, GCSDatastoreDef)]:
    type_field = d.get(DatastoreDef.type_field)
    if not isinstance(type_field, str):
        return DtlError('string %s is missing from the json' % DatastoreDef.type_field)
    if type_field != GCSDatastoreDef.type_str.value:
        return DtlError('The object %s is not a GCS definition' % str(d))
    bucket = d.get('bucket')
    if bucket is None:
        return DtlError("'bucket' needs to be defined in a GCS definition")
    file_name = d.get('fileName')
    if file_name is None:
        return DtlError("'fileName' needs to be defined in a GCS definition")
    file_format = d.get('format')
    if file_format is None:
        return DtlError("'file_format' needs to be defined in a GCS definition")
    else:
        file_format = FileFormat.file_format_from_str(file_format)
        if isinstance(file_format, DtlError):
            return file_format
        params = d.get('params')
        store_id = d.get(DatastoreDef.id_field)
        return GCSDatastoreDef(bucket, file_name, file_format, params, store_id)


class AzureDatastoreDef(DatastoreDef):
    type_str = CredentialType.Azure

    def __init__(self, container: str, file_name: str, file_format: FileFormat, params: Optional[Dict[(str, str)]]=None, datastore_id: Optional[UUID]=None):
        DatastoreDef.__init__(self, AzureDatastoreDef.type_str, datastore_id)
        self.container = container
        self.file_name = file_name
        self.file_format = file_format
        self.params = params

    def __repr__(self):
        return f"{self.__class__.__name__}(container: {self.container!r}, file_name: {self.file_name!r}, file_format: {self.file_format!r}, params: {self.params})"

    def _as_payload(self) -> dict:
        """
        Dictionary representation of the object with camelCase keys
        :return:
        """
        base = self._base_payload()
        base['container'] = self.container
        base['fileName'] = self.file_name
        base['format'] = self.file_format.value
        if self.params is not None:
            base['params'] = self.params
        return base


def _azure_datastore_def_from_payload(d: dict) -> Union[(DtlError, AzureDatastoreDef)]:
    type_field = d.get(DatastoreDef.type_field)
    if not isinstance(type_field, str):
        return DtlError('string %s is missing from the json' % DatastoreDef.type_field)
    if type_field != AzureDatastoreDef.type_str.value:
        return DtlError('The object %s is not an Azure Datastore definition' % str(d))
    container = d.get('container')
    if container is None:
        return DtlError("'container' needs to be defined in an Azure Datastore definition")
    file_name = d.get('fileName')
    if file_name is None:
        return DtlError("'fileName' needs to be defined in an Azure Datastore definition")
    file_format = d.get('format')
    if file_format is None:
        return DtlError("'file_format' needs to be defined in an Azure Datastore definition")
    else:
        file_format = FileFormat.file_format_from_str(file_format)
        if isinstance(file_format, DtlError):
            return file_format
        params = d.get('params')
        datastore_id = d.get(DatastoreDef.id_field)
        return AzureDatastoreDef(container, file_name, file_format, params, datastore_id)


class DatalogueDatastoreDef(DatastoreDef):
    type_str = CredentialType.Minio

    def __init__(self, bucket: str, key: str, file_format: FileFormat, params: Optional[Dict[(str, str)]]=None, datastore_id: Optional[UUID]=None):
        DatastoreDef.__init__(self, DatalogueDatastoreDef.type_str, datastore_id)
        self.bucket = bucket
        self.key = key
        self.file_format = file_format
        self.params = params

    def __repr__(self):
        return f"{self.__class__.__name__}(bucket: {self.bucket!r}, key: {self.key!r}, file_format: {self.file_format!r}, params: {self.params})"

    def _as_payload(self) -> dict:
        """
        Dictionary representation of the object with camelCase keys
        :return:
        """
        base = self._base_payload()
        base['bucket'] = self.bucket
        base['key'] = self.key
        base['format'] = self.file_format.value
        if self.params is not None:
            base['params'] = self.params
        return base

    @staticmethod
    def _from_payload(d: dict) -> Union[(DtlError, 'DatalogueDatastoreDef')]:
        type_field = d.get(DatastoreDef.type_field)
        if not isinstance(type_field, str):
            return DtlError('string %s is missing from the json' % DatastoreDef.type_field)
        if type_field != DatalogueDatastoreDef.type_str.value:
            return DtlError('The object %s is not an Minio definition' % str(d))
        bucket = d.get('bucket')
        if bucket is None:
            return DtlError("'bucket' needs to be defined in an Minio definition")
        key = d.get('key')
        if key is None:
            return DtlError("'key' needs to be defined in an Minio definition")
        file_format = d.get('format')
        if file_format is None:
            return DtlError("'file_format' needs to be defined in an Minio definition")
        else:
            file_format = FileFormat.file_format_from_str(file_format)
            if isinstance(file_format, DtlError):
                return file_format
            params = d.get('params')
            datastore_id = d.get(DatastoreDef.id_field)
            return DatalogueDatastoreDef(bucket, key, file_format, params, datastore_id)


class HadoopDatastoreDef(DatastoreDef):
    type_str = CredentialType.Hadoop

    def __init__(self, location: str, file_format: FileFormat, params: Optional[Dict[(str, str)]]=None, datastore_id: Optional[UUID]=None):
        DatastoreDef.__init__(self, HadoopDatastoreDef.type_str, datastore_id)
        self.location = location
        self.file_format = file_format
        self.params = params

    def __repr__(self):
        return f"{self.__class__.__name__}(location: {self.location!r}, file_format: {self.file_format!r}, params: {self.params})"

    def _as_payload(self) -> dict:
        """
        Dictionary representation of the object with camelCase keys
        :return:
        """
        base = self._base_payload()
        base['location'] = self.location
        base['format'] = self.file_format.value
        if self.params is not None:
            base['params'] = self.params
        return base

    @staticmethod
    def _from_payload(d: dict) -> Union[(DtlError, 'HadoopDatastoreDef')]:
        type_field = d.get(DatastoreDef.type_field)
        if not isinstance(type_field, str):
            return DtlError('string %s is missing from the json' % DatastoreDef.type_field)
        if type_field != HadoopDatastoreDef.type_str.value:
            return DtlError('The object %s is not a Hadoop definition' % str(d))
        location = d.get('location')
        if location is None:
            return DtlError("'location' needs to be defined")
        file_format = d.get('format')
        if file_format is None:
            return DtlError("'format' needs to be defined")
        file_format = FileFormat.file_format_from_str(file_format)
        if isinstance(file_format, DtlError):
            return file_format
        else:
            if file_format != FileFormat.Parquet:
                if file_format != FileFormat.Avro:
                    return DtlError("'format' needs to be Avro or Parquet")
            params = d.get('params')
            resource_id = d.get(DatastoreDef.id_field)
            return HadoopDatastoreDef(location, file_format, params, resource_id)


class KafkaDatastoreDef(DatastoreDef):
    type_str = CredentialType.Kafka

    def __init__(self, topic: str, format: FileFormat, params: Optional[Dict[(str, str)]]=None, datastore_id: Optional[UUID]=None):
        DatastoreDef.__init__(self, KafkaDatastoreDef.type_str, datastore_id)
        self.topic = topic
        self.format = format
        self.params = params

    def __repr__(self):
        return f"{self.__class__.__name__}(topic: {self.topic!r}, format: {self.format!r}, params: {self.params})"

    def _as_payload(self) -> dict:
        """
        Dictionary representation of the object with camelCase keys
        :return:
        """
        base = self._base_payload()
        base['topic'] = self.topic
        base['format'] = self.format.value
        if self.params is not None:
            base['params'] = self.params
        return base

    @staticmethod
    def _from_payload(d: dict) -> Union[(DtlError, 'KafkaDatastoreDef')]:
        type_field = d.get(KafkaDatastoreDef.type_field)
        if not isinstance(type_field, str):
            return DtlError('string %s is missing from the json' % DatastoreDef.type_field)
        if type_field != KafkaDatastoreDef.type_str.value:
            return DtlError('The object %s is not a Kafka definition' % str(d))
        topic = d.get('topic')
        if topic is None:
            return DtlError("'topic' needs to be defined")
        format = d.get('format')
        if format is None:
            return DtlError("'format' needs to be defined")
        format = FileFormat.file_format_from_str(format)
        if isinstance(format, DtlError):
            return format
        else:
            if format not in (FileFormat.Csv, FileFormat.Text, FileFormat.Json):
                return DtlError("'format' needs to be CSV, TEXT, Json")
            params = d.get('params')
            resource_id = d.get(DatastoreDef.id_field)
            return KafkaDatastoreDef(topic, format, params, resource_id)


class JdbcDatastoreDef(DatastoreDef):
    type_str = CredentialType.JDBC

    def __init__(self, root_table: str, datastore_id: Optional[UUID]=None):
        DatastoreDef.__init__(self, JdbcDatastoreDef.type_str, datastore_id)
        self.root_table = root_table

    def _as_payload(self) -> dict:
        """Dictionary representation of the object with camelCase keys"""
        base = self._base_payload()
        base['rootTable'] = self.root_table
        return base


def _jdbc_datastore_def_from_payload(d: dict) -> Union[(DtlError, JdbcDatastoreDef)]:
    type_field = d.get(DatastoreDef.type_field)
    if not isinstance(type_field, str):
        return DtlError('string %s is missing from the json' % DatastoreDef.type_field)
    if type_field != JdbcDatastoreDef.type_str.value:
        return DtlError('The object %s is not a Jdbc definition' % str(d))
    else:
        root_table = d.get('rootTable')
        if root_table is None:
            return DtlError("'rootTable' needs to be defined in a Jdbc definition")
        datastore_id = d.get(DatastoreDef.id_field)
        return JdbcDatastoreDef(root_table, datastore_id)


class MongoDatastoreDef(DatastoreDef):
    type_str = CredentialType.Mongo

    def __init__(self, collection: str, datastore_id: Optional[UUID]=None):
        DatastoreDef.__init__(self, MongoDatastoreDef.type_str, datastore_id)
        self.collection = collection

    def _as_payload(self) -> dict:
        """Dictionary representation of the object with camelCase keys"""
        base = self._base_payload()
        base['collection'] = self.collection
        return base


def _mongo_datastore_def_from_payload(d: dict) -> Union[(DtlError, MongoDatastoreDef)]:
    type_field = d.get(DatastoreDef.type_field)
    if not isinstance(type_field, str):
        return DtlError('string %s is missing from the json' % DatastoreDef.type_field)
    if type_field != MongoDatastoreDef.type_str.value:
        return DtlError('The object %s is not a Mongo definition' % str(d))
    else:
        collection = d.get('collection')
        if collection is None:
            return DtlError("'collection' needs to be defined in a Mongo definition")
        datastore_id = d.get(DatastoreDef.id_field)
        return MongoDatastoreDef(collection, datastore_id)


class KinesisDatastoreDef(DatastoreDef):
    __doc__ = '\n    Creates a datastore that references a Kinesis dataset\n    '
    type_str = CredentialType.Kinesis

    def __init__(self, stream_name: str, file_format: FileFormat, shard_attributes: ShardAttributes=ShardAttributes(), params: Optional[Dict[(str, str)]]=None, datastore_id: Optional[UUID]=None):
        DatastoreDef.__init__(self, KinesisDatastoreDef.type_str, datastore_id)
        self.stream_name = stream_name
        self.file_format = file_format
        self.shard_attributes = shard_attributes
        self.params = params

    def __repr__(self):
        return f"{self.__class__.__name__}(stream_name: {self.stream_name!r}, file_format: {self.file_format!r}, shard_attributes: {self.shard_attributes!r}, params: {self.params})"

    def _as_payload(self) -> dict:
        """
        Dictionary representation of the object with camelCase keys
        :return:
        """
        base = self._base_payload()
        base['streamName'] = self.stream_name
        base['format'] = self.file_format.value
        base['shardAttributes'] = self.shard_attributes._as_payload()
        if self.params is not None:
            base['params'] = self.params
        return base

    @staticmethod
    def _from_payload(d: dict) -> Union[(DtlError, 'KinesisDatastoreDef')]:
        type_field = d.get(DatastoreDef.type_field)
        if not isinstance(type_field, str):
            return DtlError('string %s is missing from the json' % DatastoreDef.type_field)
        if type_field != KinesisDatastoreDef.type_str.value:
            return DtlError('The object %s is not an Kinesis definition' % str(d))
        stream_field = d.get('streamName')
        if stream_field is None:
            return DtlError("'streamName': needs to be defined")
        format_field = d.get('format')
        if format_field is None:
            return DtlError("'format': needs to be defined")
        format_field = FileFormat.file_format_from_str(format_field)
        if isinstance(format_field, DtlError):
            return format_field
        else:
            shard_attributes = d.get('shardAttributes')
            if shard_attributes is None:
                return DtlError("'shardAttributes': needs to be defined")
            shard_attributes = ShardAttributes._from_payload(shard_attributes)
            params = d.get('params')
            datastore_id = d.get(DatastoreDef.id_field)
            return KinesisDatastoreDef(stream_field, format_field, shard_attributes, params, datastore_id)


class KafkaDatastoreDef(DatastoreDef):
    type_str = CredentialType.Kafka

    def __init__(self, topic: str, format: FileFormat, params: Optional[Dict[(str, str)]]=None, datastore_id: Optional[UUID]=None):
        DatastoreDef.__init__(self, KafkaDatastoreDef.type_str, datastore_id)
        self.topic = topic
        self.format = format
        self.params = params

    def __repr__(self):
        return f"{self.__class__.__name__}(topic: {self.topic!r}, format: {self.format!r}, params: {self.params})"

    def _as_payload(self) -> dict:
        """
        Dictionary representation of the object with camelCase keys
        :return:
        """
        base = self._base_payload()
        base['topic'] = self.topic
        base['format'] = self.format.value
        if self.params is not None:
            base['params'] = self.params
        return base

    @staticmethod
    def _from_payload(d: dict) -> Union[(DtlError, 'KafkaDatastoreDef')]:
        type_field = d.get(KafkaDatastoreDef.type_field)
        if not isinstance(type_field, str):
            return DtlError('string %s is missing from the json' % DatastoreDef.type_field)
        if type_field != KafkaDatastoreDef.type_str.value:
            return DtlError('The object %s is not a Kafka definition' % str(d))
        topic = d.get('topic')
        if topic is None:
            return DtlError("'topic' needs to be defined")
        file_format = d.get('format')
        if file_format is None:
            return DtlError("'format' needs to be defined")
        file_format = FileFormat.file_format_from_str(file_format)
        if isinstance(file_format, DtlError):
            return file_format
        else:
            if file_format not in (FileFormat.Csv, FileFormat.Text, FileFormat.Json):
                return DtlError("'format' needs to be CSV, TEXT, Json")
            params = d.get('params')
            resource_id = d.get(DatastoreDef.id_field)
            return KafkaDatastoreDef(topic, file_format, params, resource_id)


class SocrataDatastoreDef(DatastoreDef):
    __doc__ = '\n    Creates a datastore that references a Socrata dataset\n    '
    type_str = CredentialType.Socrata

    def __init__(self, socrata_id: str, datastore_id: Optional[UUID]=None):
        """
        :param socrata_id: id of the dataset on socrata
        :param datastore_id: id of the datastore on the datalogue platform. This will only be set if the object was
         retrieved from the platform
        """
        DatastoreDef.__init__(self, SocrataDatastoreDef.type_str, datastore_id)
        self.socrata_id = socrata_id

    def _as_payload(self) -> dict:
        """Dictionary representation of the object with camelCase keys"""
        base = self._base_payload()
        base['socrataId'] = self.socrata_id
        return base

    @staticmethod
    def _from_payload(d: dict) -> Union[(DtlError, 'SocrataDatastoreDef')]:
        type_field = d.get(DatastoreDef.type_field)
        if not isinstance(type_field, str):
            return DtlError('string %s is missing from the json' % DatastoreDef.type_field)
        if type_field != SocrataDatastoreDef.type_str.value:
            return DtlError('The object %s is not a Socrata definition' % str(d))
        else:
            socrata_id = d.get('socrataId')
            if socrata_id is None:
                return DtlError("'socrata_id' needs to be defined in a Socrata definition")
            datastore_id = d.get(DatastoreDef.id_field)
            return SocrataDatastoreDef(socrata_id, datastore_id)


class HttpDatastoreDef(DatastoreDef):
    __doc__ = '\n    Creates a datastore that references a Http dataset\n    '
    type_str = CredentialType.Http

    def __init__(self, url: str, file_format: FileFormat, headers: Optional[dict]=None, query_params: Optional[dict]=None, datastore_id: Optional[UUID]=None):
        """
        :param url: given url to fetch the content
        :param file_format: format of the file (json, csv, etc.)
        :param headers: headers to be added to the request (Accept, X-App-Token, etc.). it's optional
        :param query_params: http request parameters. it's optional
        """
        DatastoreDef.__init__(self, HttpDatastoreDef.type_str, datastore_id)
        self.url = url
        self.file_format = file_format
        self.headers = headers
        self.query_params = query_params

    def _as_payload(self) -> dict:
        """Dictionary representation of the object with camelCase keys"""
        base = self._base_payload()
        base['url'] = self.url
        base['format'] = self.file_format.value
        if self.headers is not None:
            base['headers'] = self.headers
        if self.query_params is not None:
            base['queryParams'] = self.query_params
        return base


def _http_datastore_def_from_payload(d: dict) -> Union[(DtlError, HttpDatastoreDef)]:
    type_field = d.get(DatastoreDef.type_field)
    if not isinstance(type_field, str):
        return DtlError('string %s is missing from the json' % DatastoreDef.type_field)
    if type_field != HttpDatastoreDef.type_str.value:
        return DtlError('The object %s is not an HttpResource definition' % str(d))
    url = d.get('url')
    if url is None:
        return DtlError("'url' needs to be defined in an HttpResource definition")
    file_format = d.get('format')
    if file_format is None:
        return DtlError("'file_format' needs to be defined in an HttpResource definition")
    else:
        file_format = FileFormat.file_format_from_str(file_format)
        if isinstance(file_format, DtlError):
            return file_format
        datastore_id = d.get(DatastoreDef.id_field)
        return HttpDatastoreDef(url, file_format, d.get('headers'), d.get('queryParams'), datastore_id)


class FileDatastoreDef(DatastoreDef):
    type_str = CredentialType.FileSystem

    def __init__(self, location: str, file_format: FileFormat, params: Optional[Dict[(str, str)]]=None, datastore_id: Optional[UUID]=None):
        DatastoreDef.__init__(self, FileDatastoreDef.type_str, datastore_id)
        self.location = location
        self.file_format = file_format
        self.params = params

    def _as_payload(self) -> dict:
        """Dictionary representation of the object with camelCase keys"""
        base = self._base_payload()
        base['location'] = self.location
        base['format'] = self.file_format.value
        if self.params is not None:
            base['params'] = self.params
        return base


def _file_datastore_def_from_payload(d: dict) -> Union[(DtlError, FileDatastoreDef)]:
    type_field = d.get(DatastoreDef.type_field)
    if not isinstance(type_field, str):
        return DtlError('string %s is missing from the json' % DatastoreDef.type_field)
    if type_field != FileDatastoreDef.type_str.value:
        return DtlError('The object %s is not a FileSystem definition' % str(d))
    location = d.get('location')
    if location is None:
        return DtlError("'location' needs to be defined in a FileSystem definition")
    file_format = d.get('format')
    if file_format is None:
        return DtlError("'file_format' needs to be defined in a FileSystem definition")
    else:
        file_format = FileFormat.file_format_from_str(file_format)
        if isinstance(file_format, DtlError):
            return file_format
        params = d.get('params')
        datastore_id = d.get(DatastoreDef.id_field)
        return FileDatastoreDef(location, file_format, params, datastore_id)


class VoidDef(DatastoreDef):
    type_str = CredentialType.Void

    def __init__(self, datastore_id: Optional[UUID]=None):
        DatastoreDef.__init__(self, VoidDef.type_str, datastore_id)

    def _as_payload(self) -> dict:
        """Dictionary representation of the object with camelCase keys"""
        return self._base_payload()


def _void_def_from_payload(d: dict) -> Union[(DtlError, VoidDef)]:
    type_field = d.get(DatastoreDef.type_field)
    if not isinstance(type_field, str):
        return DtlError('string %s is missing from the json' % DatastoreDef.type_field)
    else:
        if type_field != VoidDef.type_str.value:
            return DtlError('The object %s is not a Void definition' % str(d))
        datastore_id = d.get(DatastoreDef.id_field)
        return VoidDef(datastore_id)


_data_definitions = dict([
 (
  S3DatastoreDef.type_str.value, _s3_datastore_def_from_payload),
 (
  GCSDatastoreDef.type_str.value, _gcs_datastore_def_from_payload),
 (
  AzureDatastoreDef.type_str.value, _azure_datastore_def_from_payload),
 (
  JdbcDatastoreDef.type_str.value, _jdbc_datastore_def_from_payload),
 (
  MongoDatastoreDef.type_str.value, _mongo_datastore_def_from_payload),
 (
  HttpDatastoreDef.type_str.value, _http_datastore_def_from_payload),
 (
  SocrataDatastoreDef.type_str.value, SocrataDatastoreDef._from_payload),
 (
  FileDatastoreDef.type_str.value, _file_datastore_def_from_payload),
 (
  VoidDef.type_str.value, _void_def_from_payload),
 (
  KinesisDatastoreDef.type_str.value, KinesisDatastoreDef._from_payload),
 (
  KafkaDatastoreDef.type_str.value, KafkaDatastoreDef._from_payload),
 (
  HadoopDatastoreDef.type_str.value, HadoopDatastoreDef._from_payload),
 (
  DatalogueDatastoreDef.type_str.value, DatalogueDatastoreDef._from_payload)])

def _datastore_def_from_payload(json: dict) -> Union[(DtlError, DatastoreDef)]:
    type_field = json.get(DatastoreDef.type_field)
    if type_field is None:
        return DtlError("The datastore definition object doesn't have a '%s' property" % DatastoreDef.type_field)
    else:
        parsing_function = _data_definitions.get(type_field)
        if parsing_function is None:
            return DtlError("Looks like '%s' datastore is not handled by the SDK" % type_field)
        return parsing_function(json)


def _datastore_from_payload(json: dict) -> Union[(DtlError, Datastore)]:
    name = json.get('name')
    if name is None:
        return DtlError("'name' for a datastore should be defined")
    else:
        definition = json.get('definition')
        gate = json.get('gate')
        if definition is None:
            if gate is None:
                return DtlError("Neither 'definition' nor 'gate' for a datastore is defined!'")
        if definition is not None:
            definition = _datastore_def_from_payload(definition)
        else:
            definition = _datastore_def_from_payload(gate)
        alias = json.get('alias')
        credential_id = json.get('credentialsId')
        if credential_id is not None:
            credential_id = UUID(credential_id)
        datastore_id = json.get('id')
        samples = json.get('samples')
        if samples is not None:
            samples = _parse_list(_parse_list(_cell_from_payload))(samples)
            if isinstance(samples, DtlError):
                return samples
        schema_paths = json.get('schemaPaths')
        if schema_paths is not None:
            schema_paths = _parse_list(_parse_string_list)(schema_paths)
            if isinstance(schema_paths, DtlError):
                return schema_paths
        schema_classes = []
        classifications_json = json.get('classifications')
        if classifications_json is not None:
            classifications = _parse_list(Classification._from_payload)(classifications_json)
            if isinstance(classifications, DtlError):
                return classifications
            schema_classes = classifications
        schema_labels = None
        if schema_paths is not None:
            schema_labels = set()
            for row in schema_paths:
                for col in row:
                    schema_labels.add(col)

            schema_labels = list(schema_labels)
        ads_json = json.get('ads')
        schema_nodes = None
        ads = None
        if ads_json is not None:
            schema_nodes = ads_json.get('nodes')
            if schema_nodes is not None:
                schema_nodes = _parse_list(SchemaNode._schema_node_from_payload)(schema_nodes)
                if isinstance(schema_nodes, DtlError):
                    return schema_nodes
            ads = AbstractDataSchema._from_payload(ads_json, AbstractDataSchema.node_decoder)
        return Datastore(name, definition, credential_id, alias, datastore_id, samples, schema_paths, schema_classes, schema_labels, schema_nodes, ads)