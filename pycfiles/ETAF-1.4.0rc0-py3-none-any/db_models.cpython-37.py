# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sage/fatedoc/FATE/fate_flow/db/db_models.py
# Compiled at: 2020-05-06 02:27:06
# Size of source mod 2**32: 9186 bytes
import datetime, inspect, os, sys, __main__
from peewee import Model, CharField, IntegerField, BigIntegerField, TextField, CompositeKey, BigAutoField
from playhouse.apsw_ext import APSWDatabase
from playhouse.pool import PooledMySQLDatabase
from arch.api.utils import log_utils
from arch.api.utils.core_utils import current_timestamp
from fate_flow.entity.constant_config import WorkMode
from fate_flow.settings import DATABASE, WORK_MODE, stat_logger, USE_LOCAL_DATABASE
from fate_flow.entity.runtime_config import RuntimeConfig
LOGGER = log_utils.getLogger()

def singleton(cls, *args, **kw):
    instances = {}

    def _singleton():
        key = str(cls) + str(os.getpid())
        if key not in instances:
            instances[key] = cls(*args, **kw)
        return instances[key]

    return _singleton


@singleton
class BaseDataBase(object):

    def __init__(self):
        database_config = DATABASE.copy()
        db_name = database_config.pop('name')
        if WORK_MODE == WorkMode.STANDALONE:
            if USE_LOCAL_DATABASE:
                self.database_connection = APSWDatabase('fate_flow_sqlite.db')
                RuntimeConfig.init_config(USE_LOCAL_DATABASE=True)
                stat_logger.info('init sqlite database on standalone mode successfully')
            else:
                self.database_connection = PooledMySQLDatabase(db_name, **database_config)
                stat_logger.info('init mysql database on standalone mode successfully')
                RuntimeConfig.init_config(USE_LOCAL_DATABASE=False)
        elif WORK_MODE == WorkMode.CLUSTER:
            self.database_connection = PooledMySQLDatabase(db_name, **database_config)
            stat_logger.info('init mysql database on cluster mode successfully')
            RuntimeConfig.init_config(USE_LOCAL_DATABASE=False)
        else:
            raise Exception('can not init database')


if __main__.__file__.endswith('fate_flow_server.py') or __main__.__file__.endswith('task_executor.py'):
    DB = BaseDataBase().database_connection
else:
    DB = None

def close_connection(db_connection):
    try:
        if db_connection:
            db_connection.close()
    except Exception as e:
        try:
            LOGGER.exception(e)
        finally:
            e = None
            del e


class DataBaseModel(Model):

    class Meta:
        database = DB

    def to_json(self):
        return self.__dict__['__data__']

    def save(self, *args, **kwargs):
        if hasattr(self, 'update_date'):
            self.update_date = datetime.datetime.now()
        if hasattr(self, 'update_time'):
            self.update_time = current_timestamp()
        (super(DataBaseModel, self).save)(*args, **kwargs)


def init_database_tables():
    with DB.connection_context():
        members = inspect.getmembers(sys.modules[__name__], inspect.isclass)
        table_objs = []
        for name, obj in members:
            if obj != DataBaseModel and issubclass(obj, DataBaseModel):
                table_objs.append(obj)

        DB.create_tables(table_objs)


class Queue(DataBaseModel):
    f_job_id = CharField(max_length=100)
    f_event = CharField(max_length=500)
    f_is_waiting = IntegerField(default=1)

    class Meta:
        db_table = 't_queue'


class Job(DataBaseModel):
    f_job_id = CharField(max_length=25)
    f_name = CharField(max_length=500, null=True, default='')
    f_description = TextField(null=True, default='')
    f_tag = CharField(max_length=50, null=True, index=True, default='')
    f_role = CharField(max_length=10, index=True)
    f_party_id = CharField(max_length=10, index=True)
    f_roles = TextField()
    f_work_mode = IntegerField()
    f_initiator_party_id = CharField(max_length=50, index=True, default=(-1))
    f_is_initiator = IntegerField(null=True, index=True, default=(-1))
    f_dsl = TextField()
    f_runtime_conf = TextField()
    f_train_runtime_conf = TextField(null=True)
    f_run_ip = CharField(max_length=100)
    f_status = CharField(max_length=50)
    f_current_steps = CharField(max_length=500, null=True)
    f_current_tasks = CharField(max_length=500, null=True)
    f_progress = IntegerField(null=True, default=0)
    f_create_time = BigIntegerField()
    f_update_time = BigIntegerField(null=True)
    f_start_time = BigIntegerField(null=True)
    f_end_time = BigIntegerField(null=True)
    f_elapsed = BigIntegerField(null=True)

    class Meta:
        db_table = 't_job'
        primary_key = CompositeKey('f_job_id', 'f_role', 'f_party_id')


class Task(DataBaseModel):
    f_job_id = CharField(max_length=25)
    f_component_name = TextField()
    f_task_id = CharField(max_length=100)
    f_role = CharField(max_length=10, index=True)
    f_party_id = CharField(max_length=10, index=True)
    f_operator = CharField(max_length=100, null=True)
    f_run_ip = CharField(max_length=100, null=True)
    f_run_pid = IntegerField(null=True)
    f_status = CharField(max_length=50)
    f_create_time = BigIntegerField()
    f_update_time = BigIntegerField(null=True)
    f_start_time = BigIntegerField(null=True)
    f_end_time = BigIntegerField(null=True)
    f_elapsed = BigIntegerField(null=True)

    class Meta:
        db_table = 't_task'
        primary_key = CompositeKey('f_job_id', 'f_task_id', 'f_role', 'f_party_id')


class DataView(DataBaseModel):
    f_job_id = CharField(max_length=25)
    f_role = CharField(max_length=10, index=True)
    f_party_id = CharField(max_length=10, index=True)
    f_table_name = CharField(max_length=500, null=True)
    f_table_namespace = CharField(max_length=500, null=True)
    f_component_name = TextField()
    f_create_time = BigIntegerField()
    f_update_time = BigIntegerField(null=True)
    f_table_count_upload = IntegerField(null=True)
    f_table_count_actual = IntegerField(null=True)
    f_partition = IntegerField(null=True)
    f_task_id = CharField(max_length=100)
    f_type = CharField(max_length=50, null=True)
    f_ttl = IntegerField(default=0)
    f_party_model_id = CharField(max_length=100, null=True)
    f_model_version = CharField(max_length=100, null=True)
    f_size = BigIntegerField(default=0)
    f_description = TextField(null=True, default='')
    f_tag = CharField(max_length=50, null=True, index=True, default='')

    class Meta:
        db_table = 't_data_view'
        primary_key = CompositeKey('f_job_id', 'f_task_id', 'f_role', 'f_party_id')


class MachineLearningModelMeta(DataBaseModel):
    f_id = BigIntegerField(primary_key=True)
    f_role = CharField(max_length=10, index=True)
    f_party_id = CharField(max_length=10, index=True)
    f_roles = TextField()
    f_job_id = CharField(max_length=25)
    f_model_id = CharField(max_length=100, index=True)
    f_model_version = CharField(max_length=100, index=True)
    f_size = BigIntegerField(default=0)
    f_create_time = BigIntegerField(default=0)
    f_update_time = BigIntegerField(default=0)
    f_description = TextField(null=True, default='')
    f_tag = CharField(max_length=50, null=True, index=True, default='')

    class Meta:
        db_table = 't_machine_learning_model_meta'


class TrackingMetric(DataBaseModel):
    _mapper = {}

    @classmethod
    def model(cls, table_index=None, date=None):
        if not table_index:
            table_index = date.strftime('%Y%m%d') if date else datetime.datetime.now().strftime('%Y%m%d')
        class_name = 'TrackingMetric_%s' % table_index
        ModelClass = TrackingMetric._mapper.get(class_name, None)
        if ModelClass is None:

            class Meta:
                db_table = '%s_%s' % ('t_tracking_metric', table_index)

            attrs = {'__module__':cls.__module__, 
             'Meta':Meta}
            ModelClass = type('%s_%s' % (cls.__name__, table_index), (cls,), attrs)
            TrackingMetric._mapper[class_name] = ModelClass
        return ModelClass()

    f_id = BigAutoField(primary_key=True)
    f_job_id = CharField(max_length=25)
    f_component_name = TextField()
    f_task_id = CharField(max_length=100)
    f_role = CharField(max_length=10, index=True)
    f_party_id = CharField(max_length=10, index=True)
    f_metric_namespace = CharField(max_length=180, index=True)
    f_metric_name = CharField(max_length=180, index=True)
    f_key = CharField(max_length=200)
    f_value = TextField()
    f_type = IntegerField(index=True)
    f_create_time = BigIntegerField()
    f_update_time = BigIntegerField(null=True)