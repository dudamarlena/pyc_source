# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/netlogger/analysis/schema/stampede_schema.py
# Compiled at: 2012-03-07 16:22:22
"""
Contains the code to create and map objects to the Stampede DB schema
via a SQLAlchemy interface.
"""
__rcsid__ = '$Id: stampede_schema.py 30421 2012-02-21 21:20:02Z mgoode $'
__author__ = 'Monte Goode MMGoode@lbl.gov'
from netlogger.analysis.schema._base import SABase, SchemaIntegrityError
try:
    from sqlalchemy import *
    from sqlalchemy import orm, exceptions, func, exc
    from sqlalchemy.orm import relation, backref
except ImportError, e:
    print '** SQLAlchemy library needs to be installed: http://www.sqlalchemy.org/ **\n'
    raise ImportError, e

import time, warnings
CURRENT_SCHEMA_VERSION = 4.0

class Host(SABase):
    pass


class Workflow(SABase):
    pass


class Workflowstate(SABase):
    pass


class Job(SABase):
    pass


class JobEdge(SABase):
    pass


class JobInstance(SABase):
    pass


class Jobstate(SABase):
    pass


class Task(SABase):
    pass


class TaskEdge(SABase):
    pass


class Invocation(SABase):
    pass


class File(SABase):
    pass


class SchemaInfo(SABase):
    pass


def initializeToPegasusDB(db, metadata, kw={}):
    """
    Function to create the Stampede schema if it does not exist,
    if it does exist, then connect and set up object mappings.
    
    @type   db: SQLAlch db/engine object.
    @param  db: Engine object to initialize.
    @type   metadata: SQLAlch metadata object.
    @param  metadata: Associated metadata object to initialize.
    @type   kw: dict
    @param  kw: Keywords to pass to Table() functions
    """
    KeyInt = Integer
    if db.name == 'mysql':
        KeyInt = BigInteger
        kw['mysql_charset'] = 'latin1'
    if db.name == 'sqlite':
        warnings.filterwarnings('ignore', '.*does \\*not\\* support Decimal*.')
    st_workflow = Table('workflow', metadata, Column('wf_id', KeyInt, primary_key=True, nullable=False), Column('wf_uuid', VARCHAR(255), nullable=False), Column('dag_file_name', VARCHAR(255), nullable=True), Column('timestamp', NUMERIC(precision=16, scale=6), nullable=True), Column('submit_hostname', VARCHAR(255), nullable=True), Column('submit_dir', TEXT, nullable=True), Column('planner_arguments', TEXT, nullable=True), Column('user', VARCHAR(255), nullable=True), Column('grid_dn', VARCHAR(255), nullable=True), Column('planner_version', VARCHAR(255), nullable=True), Column('dax_label', VARCHAR(255), nullable=True), Column('dax_version', VARCHAR(255), nullable=True), Column('dax_file', VARCHAR(255), nullable=True), Column('parent_wf_id', KeyInt, ForeignKey('workflow.wf_id'), nullable=True), Column('root_wf_id', KeyInt, nullable=True), **kw)
    Index('wf_id_KEY', st_workflow.c.wf_id, unique=True)
    Index('wf_uuid_UNIQUE', st_workflow.c.wf_uuid, unique=True)
    try:
        wf_props = {'child_wf': relation(Workflow, cascade='all'), 
           'child_wfs': relation(Workflowstate, backref='st_workflow', cascade='all'), 
           'child_host': relation(Host, backref='st_workflow', cascade='all'), 
           'child_task': relation(Task, backref='st_workflow', cascade='all'), 
           'child_job': relation(Job, backref='st_workflow', cascade='all'), 
           'child_invocation': relation(Invocation, backref='st_workflow', cascade='all'), 
           'child_task_e': relation(TaskEdge, backref='st_workflow', cascade='all'), 
           'child_job_e': relation(JobEdge, backref='st_workflow', cascade='all')}
        orm.mapper(Workflow, st_workflow, properties=wf_props)
    except exc.ArgumentError:
        pass

    st_workflowstate = Table('workflowstate', metadata, Column('wf_id', KeyInt, ForeignKey('workflow.wf_id'), nullable=False, primary_key=True), Column('state', Enum('WORKFLOW_STARTED', 'WORKFLOW_TERMINATED'), nullable=False, primary_key=True), Column('timestamp', NUMERIC(precision=16, scale=6), nullable=False, primary_key=True, default=time.time()), Column('restart_count', INT, nullable=False), Column('status', INT, nullable=True), **kw)
    Index('UNIQUE_WORKFLOWSTATE', st_workflowstate.c.wf_id, st_workflowstate.c.state, st_workflowstate.c.timestamp, unique=True)
    try:
        orm.mapper(Workflowstate, st_workflowstate)
    except exc.ArgumentError:
        pass

    st_host = Table('host', metadata, Column('host_id', KeyInt, primary_key=True, nullable=False), Column('wf_id', KeyInt, ForeignKey('workflow.wf_id'), nullable=False), Column('site', VARCHAR(255), nullable=False), Column('hostname', VARCHAR(255), nullable=False), Column('ip', VARCHAR(255), nullable=False), Column('uname', VARCHAR(255), nullable=True), Column('total_memory', KeyInt, nullable=True), **kw)
    Index('UNIQUE_HOST', st_host.c.wf_id, st_host.c.site, st_host.c.hostname, st_host.c.ip, unique=True)
    try:
        orm.mapper(Host, st_host)
    except exc.ArgumentError:
        pass

    st_job = Table('job', metadata, Column('job_id', KeyInt, primary_key=True, nullable=False), Column('wf_id', KeyInt, ForeignKey('workflow.wf_id'), nullable=False), Column('exec_job_id', VARCHAR(255), nullable=False), Column('submit_file', VARCHAR(255), nullable=False), Column('type_desc', Enum('unknown', 'compute', 'stage-in-tx', 'stage-out-tx', 'registration', 'inter-site-tx', 'create-dir', 'staged-compute', 'cleanup', 'chmod', 'dax', 'dag'), nullable=False), Column('clustered', BOOLEAN, nullable=False), Column('max_retries', INT, nullable=False), Column('executable', TEXT, nullable=False), Column('argv', TEXT, nullable=True), Column('task_count', INT, nullable=False), **kw)
    Index('job_id_KEY', st_job.c.job_id, unique=True)
    Index('job_type_desc_COL', st_job.c.type_desc)
    Index('job_exec_job_id_COL', st_job.c.exec_job_id)
    Index('UNIQUE_JOB', st_job.c.wf_id, st_job.c.exec_job_id, unique=True)
    try:
        orm.mapper(Job, st_job, properties={'child_job_instance': relation(JobInstance, backref='st_job', cascade='all', lazy=False)})
    except exc.ArgumentError:
        pass

    st_job_edge = Table('job_edge', metadata, Column('wf_id', KeyInt, ForeignKey('workflow.wf_id'), primary_key=True, nullable=False), Column('parent_exec_job_id', VARCHAR(255), primary_key=True, nullable=False), Column('child_exec_job_id', VARCHAR(255), primary_key=True, nullable=False), **kw)
    Index('UNIQUE_JOB_EDGE', st_job_edge.c.wf_id, st_job_edge.c.parent_exec_job_id, st_job_edge.c.child_exec_job_id, unique=True)
    try:
        orm.mapper(JobEdge, st_job_edge)
    except exc.ArgumentError:
        pass

    st_job_instance = Table('job_instance', metadata, Column('job_instance_id', KeyInt, primary_key=True, nullable=False), Column('job_id', KeyInt, ForeignKey('job.job_id'), nullable=False), Column('host_id', KeyInt, ForeignKey('host.host_id', ondelete='SET NULL'), nullable=True), Column('job_submit_seq', INT, nullable=False), Column('sched_id', VARCHAR(255), nullable=True), Column('site', VARCHAR(255), nullable=True), Column('user', VARCHAR(255), nullable=True), Column('work_dir', TEXT, nullable=True), Column('cluster_start', NUMERIC(16, 6), nullable=True), Column('cluster_duration', NUMERIC(10, 3), nullable=True), Column('local_duration', NUMERIC(10, 3), nullable=True), Column('subwf_id', KeyInt, ForeignKey('workflow.wf_id', ondelete='SET NULL'), nullable=True), Column('stdout_file', VARCHAR(255), nullable=True), Column('stdout_text', TEXT, nullable=True), Column('stderr_file', VARCHAR(255), nullable=True), Column('stderr_text', TEXT, nullable=True), Column('stdin_file', VARCHAR(255), nullable=True), Column('multiplier_factor', INT, nullable=False, default=1), Column('exitcode', INT, nullable=True), **kw)
    Index('job_instance_id_KEY', st_job_instance.c.job_instance_id, unique=True)
    Index('UNIQUE_JOB_INSTANCE', st_job_instance.c.job_id, st_job_instance.c.job_submit_seq, unique=True)
    try:
        orm.mapper(JobInstance, st_job_instance, properties={'child_tsk': relation(Invocation, backref='st_job_instance', cascade='all', lazy=False), 
           'child_jst': relation(Jobstate, backref='st_job_instance', cascade='all', lazy=False)})
    except exc.ArgumentError:
        pass

    st_jobstate = Table('jobstate', metadata, Column('job_instance_id', KeyInt, ForeignKey('job_instance.job_instance_id'), nullable=False, primary_key=True), Column('state', VARCHAR(255), nullable=False, primary_key=True), Column('timestamp', NUMERIC(precision=16, scale=6), nullable=False, primary_key=True, default=time.time()), Column('jobstate_submit_seq', INT, nullable=False, primary_key=True), **kw)
    Index('UNIQUE_JOBSTATE', st_jobstate.c.job_instance_id, st_jobstate.c.state, st_jobstate.c.timestamp, st_jobstate.c.jobstate_submit_seq, unique=True)
    try:
        orm.mapper(Jobstate, st_jobstate)
    except exc.ArgumentError:
        pass

    st_task = Table('task', metadata, Column('task_id', KeyInt, primary_key=True, nullable=False), Column('job_id', KeyInt, ForeignKey('job.job_id', ondelete='SET NULL'), nullable=True), Column('wf_id', KeyInt, ForeignKey('workflow.wf_id'), nullable=False), Column('abs_task_id', VARCHAR(255), nullable=False), Column('transformation', TEXT, nullable=False), Column('argv', TEXT, nullable=True), Column('type_desc', VARCHAR(255), nullable=False), **kw)
    Index('task_id_KEY', st_task.c.task_id, unique=True)
    Index('task_abs_task_id_COL', st_task.c.abs_task_id)
    Index('task_wf_id_COL', st_task.c.wf_id)
    Index('UNIQUE_TASK', st_task.c.wf_id, st_task.c.abs_task_id, unique=True)
    try:
        orm.mapper(Task, st_task, properties={'child_file': relation(File, backref='st_task', cascade='all')})
    except exc.ArgumentError:
        pass

    st_task_edge = Table('task_edge', metadata, Column('wf_id', KeyInt, ForeignKey('workflow.wf_id'), primary_key=True, nullable=False), Column('parent_abs_task_id', VARCHAR(255), primary_key=True, nullable=True), Column('child_abs_task_id', VARCHAR(255), primary_key=True, nullable=True), **kw)
    Index('UNIQUE_TASK_EDGE', st_task_edge.c.wf_id, st_task_edge.c.parent_abs_task_id, st_task_edge.c.child_abs_task_id, unique=True)
    try:
        orm.mapper(TaskEdge, st_task_edge)
    except exc.ArgumentError:
        pass

    st_invocation = Table('invocation', metadata, Column('invocation_id', KeyInt, primary_key=True, nullable=False), Column('job_instance_id', KeyInt, ForeignKey('job_instance.job_instance_id'), nullable=False), Column('task_submit_seq', INT, nullable=False), Column('start_time', NUMERIC(16, 6), nullable=False, default=time.time()), Column('remote_duration', NUMERIC(10, 3), nullable=False), Column('remote_cpu_time', NUMERIC(10, 3), nullable=True), Column('exitcode', INT, nullable=False), Column('transformation', TEXT, nullable=False), Column('executable', TEXT, nullable=False), Column('argv', TEXT, nullable=True), Column('abs_task_id', VARCHAR(255), nullable=True), Column('wf_id', KeyInt, ForeignKey('workflow.wf_id'), nullable=False), **kw)
    Index('invocation_id_KEY', st_invocation.c.invocation_id, unique=True)
    Index('invoc_abs_task_id_COL', st_invocation.c.abs_task_id)
    Index('invoc_wf_id_COL', st_invocation.c.wf_id)
    Index('UNIQUE_INVOCATION', st_invocation.c.job_instance_id, st_invocation.c.task_submit_seq, unique=True)
    try:
        orm.mapper(Invocation, st_invocation)
    except exc.ArgumentError:
        pass

    st_file = Table('file', metadata, Column('file_id', KeyInt, primary_key=True, nullable=False), Column('task_id', KeyInt, ForeignKey('task.task_id'), nullable=True), Column('lfn', VARCHAR(255), nullable=True), Column('estimated_size', INT, nullable=True), Column('md_checksum', VARCHAR(255), nullable=True), Column('type', VARCHAR(255), nullable=True), **kw)
    Index('file_id_UNIQUE', st_file.c.file_id, unique=True)
    Index('FK_FILE_TASK_ID', st_task.c.task_id, unique=False)
    try:
        orm.mapper(File, st_file)
    except exc.ArgumentError:
        pass

    st_schema_info = Table('schema_info', metadata, Column('version_number', NUMERIC(2, 1), primary_key=True, nullable=False), Column('version_timestamp', NUMERIC(16, 6), primary_key=True, nullable=False, default=time.time()))
    try:
        orm.mapper(SchemaInfo, st_schema_info)
    except exc.ArgumentError:
        pass

    metadata.create_all(db)


def main():
    """
    Example of how to creat SQLAlch object and initialize/create
    to Stampede DB schema.
    """
    db = create_engine('sqlite:///pegasusTest.db', echo=True)
    metadata = MetaData()
    initializeToPegasusDB(db, metadata)
    metadata.bind = db
    sm = orm.sessionmaker(bind=db, autoflush=True, autocommit=False, expire_on_commit=True)
    session = orm.scoped_session(sm)


if __name__ == '__main__':
    main()