# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/awsglue/context.py
# Compiled at: 2019-08-21 04:11:21
# Size of source mod 2**32: 15193 bytes
from pyspark.sql import SQLContext
from pyspark.sql import SparkSession
from py4j.java_gateway import java_import
from awsglue.data_source import DataSource
from awsglue.data_sink import DataSink
from awsglue.dynamicframe import DynamicFrame, DynamicFrameReader, DynamicFrameWriter, DynamicFrameCollection
from awsglue.gluetypes import DataType
from awsglue.utils import makeOptions, callsite
import pyspark, os, re, uuid
from py4j.java_gateway import JavaClass

def register(sc):
    java_import(sc._jvm, 'com.amazonaws.services.glue.*')
    java_import(sc._jvm, 'com.amazonaws.services.glue.schema.*')
    java_import(sc._jvm, 'com.amazonaws.services.glue.util.JsonOptions')
    java_import(sc._jvm, 'org.apache.spark.sql.glue.util.SparkUtility')
    java_import(sc._jvm, 'com.amazonaws.services.glue.util.Job')
    java_import(sc._jvm, 'com.amazonaws.services.glue.util.AWSConnectionUtils')
    java_import(sc._jvm, 'com.amazonaws.services.glue.util.GluePythonUtils')
    java_import(sc._jvm, 'com.amazonaws.services.glue.errors.CallSite')


class GlueContext(SQLContext):
    Spark_SQL_Formats = {
     'parquet', 'orc'}

    def __init__(self, sparkContext, **options):
        super(GlueContext, self).__init__(sparkContext)
        register(sparkContext)
        self._glue_scala_context = (self._get_glue_scala_context)(**options)
        self.create_dynamic_frame = DynamicFrameReader(self)
        self.write_dynamic_frame = DynamicFrameWriter(self)
        self.spark_session = SparkSession(sparkContext, self._glue_scala_context.getSparkSession())

    @property
    def _ssql_ctx(self):
        if not hasattr(self, '_glue_scala_context'):
            self._glue_scala_context = self._get_glue_scala_context()
        return self._glue_scala_context

    def _get_glue_scala_context(self, **options):
        min_partitions = target_partitions = None
        if 'minPartitions' in options:
            min_partitions = options['minPartitions']
            target_partitions = options.get('targetPartitions', min_partitions)
        else:
            if 'targetPartitions' in options:
                min_partitions = target_partitions = options.get('targetPartitions')
        if min_partitions is None:
            return self._jvm.GlueContext(self._jsc.sc())
        return self._jvm.GlueContext(self._jsc.sc(), min_partitions, target_partitions)

    def getSource(self, connection_type, format=None, transformation_ctx='', push_down_predicate='', **options):
        """Creates a DataSource object.

        This can be used to read DynamicFrames from external sources.

        Example:
        >>> data_source = context.getSource("file", paths=["/in/path"])
        >>> data_source.setFormat("json")
        >>> myFrame = data_source.getFrame()
        """
        options['callSite'] = callsite()
        if format:
            if format.lower() in self.Spark_SQL_Formats:
                connection_type = format
        j_source = self._ssql_ctx.getSource(connection_type, makeOptions(self._sc, options), transformation_ctx, push_down_predicate)
        prefix = None
        if 'paths' in options:
            if options['paths'] != None:
                paths = options['paths']
                prefix = os.path.commonprefix(paths)
                if prefix != None:
                    prefix = prefix.split(':')[(-1)]
                    prefix = re.sub('[:/.]', '', prefix)
        if prefix == None:
            prefix = str(uuid.uuid1())
            prefix = re.sub('[-]', '_', prefix)
        return DataSource(j_source, self, prefix)

    def create_dynamic_frame_from_rdd(self, data, name, schema=None, sample_ratio=None, transformation_ctx=''):
        """Creates a DynamicFrame from an RDD.
        """
        df = super(GlueContext, self).createDataFrame(data, schema, sample_ratio)
        return DynamicFrame.fromDF(df, self, name)

    def create_dynamic_frame_from_catalog(self, database=None, table_name=None, redshift_tmp_dir='', transformation_ctx='', push_down_predicate='', additional_options={}, catalog_id=None, **kwargs):
        """
        Creates a DynamicFrame with catalog database, table name and an optional catalog id
        :param database: database in catalog
        :param table_name: table name
        :param redshift_tmp_dir: tmp dir
        :param transformation_ctx: transformation context
        :param push_down_predicate
        :param additional_options
        :param catalog_id catalog id of the DataCatalog being accessed (account id of the data catalog).
                Set to None by default (None defaults to the catalog id of the calling account in the service)
        :return: dynamic frame with potential errors
        """
        if database is not None and 'name_space' in kwargs:
            raise Exception('Parameter name_space and database are both specified, choose one.')
        else:
            if database is None and 'name_space' not in kwargs:
                raise Exception('Parameter name_space or database is missing.')
            else:
                if 'name_space' in kwargs:
                    db = kwargs.pop('name_space')
                else:
                    db = database
        if table_name is None:
            raise Exception('Parameter table_name is missing.')
        source = DataSource(self._ssql_ctx.getCatalogSource(db, table_name, redshift_tmp_dir, transformation_ctx, push_down_predicate, makeOptions(self._sc, additional_options), catalog_id), self, table_name)
        return (source.getFrame)(**kwargs)

    def create_dynamic_frame_from_options(self, connection_type, connection_options={}, format=None, format_options={}, transformation_ctx='', push_down_predicate='', **kwargs):
        """Creates a DynamicFrame with the specified connection and format.

        Example:
        >>> myFrame = context.createDynamicFrame(connection_type="file",
        >>>                                      connection_options={"paths": ["/in/path"]},
        >>>                                      format="json")

        """
        source = (self.getSource)(connection_type, format, transformation_ctx, push_down_predicate, **connection_options)
        if format:
            if format not in self.Spark_SQL_Formats:
                (source.setFormat)(format, **format_options)
        return (source.getFrame)(**kwargs)

    def getSink(self, connection_type, format=None, transformation_ctx='', **options):
        """Gets a DataSink object.

        This can be used to write DynamicFrames to external targets.
        Check SparkSQL format first to make sure to return the expected sink

        Example:
        >>> data_sink = context.getSink("s3")
        >>> data_sink.setFormat("json"),
        >>> data_sink.writeFrame(myFrame)
        """
        if format:
            if format.lower() in self.Spark_SQL_Formats:
                connection_type = format
        j_sink = self._ssql_ctx.getSink(connection_type, makeOptions(self._sc, options), transformation_ctx)
        return DataSink(j_sink, self)

    def write_dynamic_frame_from_options(self, frame, connection_type, connection_options={}, format=None, format_options={}, transformation_ctx=''):
        """
        Writes a DynamicFrame using the specified connection and format
        :param frame:
        :param connection_type: s3, redshift, jdbc, dynamo and so on
        :param connection_options: like path, dbtable
        :param format: json, csv or other format, this is used for s3 or tape connection which supports multiple format
        :param format_options: delimiter and so on
        :return: dynamic_frame with potential errors

        >>> data_sink = context.write_dynamic_frame_by_options(frame,
        >>>                                                    connection_type="s3",
        >>>                                                    path="/out/path",
        >>>                                                    format="json")
        """
        return self.write_from_options(frame, connection_type, connection_options, format, format_options, transformation_ctx)

    def write_from_options(self, frame_or_dfc, connection_type, connection_options={}, format={}, format_options={}, transformation_ctx='', **kwargs):
        if isinstance(frame_or_dfc, DynamicFrameCollection):
            new_options = dict(connection_options.items() + [
             ('useFrameName', True)])
        else:
            if isinstance(frame_or_dfc, DynamicFrame):
                new_options = connection_options
            else:
                raise TypeError('frame_or_dfc must be DynamicFrame orDynamicFrameCollection. Got ' + str(type(frame_or_dfc)))
        sink = (self.getSink)(connection_type, format, transformation_ctx, **new_options)
        if format:
            if format not in self.Spark_SQL_Formats:
                (sink.setFormat)(format, **format_options)
        if 'accumulator_size' in kwargs:
            if kwargs['accumulator_size'] > 0:
                sink.setAccumulableSize(kwargs['accumulator_size'])
        return sink.write(frame_or_dfc)

    def write_dynamic_frame_from_catalog(self, frame, database=None, table_name=None, redshift_tmp_dir='', transformation_ctx='', additional_options={}, catalog_id=None, **kwargs):
        """
        Writes a DynamicFrame to a location defined in the catalog's database, table name and an optional catalog id
        :param frame: dynamic frame to be written
        :param database: database in catalog
        :param table_name: table name
        :param redshift_tmp_dir: tmp dir
        :param transformation_ctx: transformation context
        :param additional_options
        :param catalog_id catalog_id catalog id of the DataCatalog being accessed (account id of the data catalog).
                Set to None by default (None defaults to the catalog id of the calling account in the service)
        :return: dynamic frame with potential errors
        """
        if database is not None and 'name_space' in kwargs:
            raise Exception('Parameter name_space and database are both specified, choose one.')
        else:
            if database is None and 'name_space' not in kwargs:
                raise Exception('Parameter name_space or database is missing.')
            else:
                if 'name_space' in kwargs:
                    db = kwargs.pop('name_space')
                else:
                    db = database
        if table_name is None:
            raise Exception('Parameter table_name is missing.')
        j_sink = self._ssql_ctx.getCatalogSink(db, table_name, redshift_tmp_dir, transformation_ctx, makeOptions(self._sc, additional_options), catalog_id)
        return DataSink(j_sink, self).write(frame)

    def write_dynamic_frame_from_jdbc_conf(self, frame, catalog_connection, connection_options={}, redshift_tmp_dir='', transformation_ctx='', catalog_id=None):
        """
        :param frame: dynamic frame to be written
        :param catalog_connection: catalog connection name, used to access JDBC configuration
        :param connection_options: dbtable and so on
        :param redshift_tmp_dir: tmp dir
        :param transformation_ctx: transformation context
        :param catalog_id catalog id of the DataCatalog being accessed (account id of the data catalog).
                Set to None by default (None defaults to the catalog id of the calling account in the service)
        :return: dynamic frame with potential errors
        """
        self.write_from_jdbc_conf(frame, catalog_connection, connection_options, redshift_tmp_dir, transformation_ctx, catalog_id)

    def write_from_jdbc_conf(self, frame_or_dfc, catalog_connection, connection_options={}, redshift_tmp_dir='', transformation_ctx='', catalog_id=None):
        if isinstance(frame_or_dfc, DynamicFrameCollection):
            new_options = dict(connection_options.items() + [
             ('useFrameName', True)])
        else:
            if isinstance(frame_or_dfc, DynamicFrame):
                new_options = connection_options
            else:
                raise TypeError('frame_or_dfc must be DynamicFrame orDynamicFrameCollection. Got ' + str(type(frame_or_dfc)))
        j_sink = self._ssql_ctx.getJDBCSink(catalog_connection, makeOptions(self._sc, new_options), redshift_tmp_dir, transformation_ctx, catalog_id)
        return DataSink(j_sink, self).write(frame_or_dfc)

    def convert_resolve_option(self, path, action, target):
        if action.upper() == 'KEEPASSTRUCT':
            return self._jvm.ResolveSpec.apply(path, 'make_struct')
        if action.upper() == 'PROJECT':
            if not (target is None or isinstance(target, DataType)):
                raise ValueError('Target type must be specified with project action.')
            return self._jvm.ResolveSpec.apply(path, 'project:{}'.format(target.typeName()))
        raise ValueError('Invalid resolve action {}. '.format(action) + 'Action must be one of KeepAsStruct and Project.')

    def extract_jdbc_conf(self, connection_name, catalog_id=None):
        """
        Get the username, password, vendor and url from the connection object in the catalog
        :param connection_name: name of the connection in the catalog
        :param catalog_id: catalog id of the DataCatalog being accessed (account id of the data catalog).
                Set to None by default (None defaults to the catalog id of the calling account in the service)
        :return: dict with keys "user", "password", "vendor", "url"
        """
        return self._ssql_ctx.extractJDBCConf(connection_name, catalog_id)