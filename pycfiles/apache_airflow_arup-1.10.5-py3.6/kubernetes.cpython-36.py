# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/models/kubernetes.py
# Compiled at: 2019-09-11 02:44:38
# Size of source mod 2**32: 2785 bytes
import uuid
from sqlalchemy import Column, Boolean, true as sqltrue, String
from airflow.models.base import Base
from airflow.utils.db import provide_session

class KubeResourceVersion(Base):
    __tablename__ = 'kube_resource_version'
    one_row_id = Column(Boolean, server_default=(sqltrue()), primary_key=True)
    resource_version = Column(String(255))

    @staticmethod
    @provide_session
    def get_current_resource_version(session=None):
        resource_version, = session.query(KubeResourceVersion.resource_version).one()
        return resource_version

    @staticmethod
    @provide_session
    def checkpoint_resource_version(resource_version, session=None):
        if resource_version:
            session.query(KubeResourceVersion).update({KubeResourceVersion.resource_version: resource_version})
            session.commit()

    @staticmethod
    @provide_session
    def reset_resource_version(session=None):
        session.query(KubeResourceVersion).update({KubeResourceVersion.resource_version: '0'})
        session.commit()
        return '0'


class KubeWorkerIdentifier(Base):
    __tablename__ = 'kube_worker_uuid'
    one_row_id = Column(Boolean, server_default=(sqltrue()), primary_key=True)
    worker_uuid = Column(String(255))

    @staticmethod
    @provide_session
    def get_or_create_current_kube_worker_uuid(session=None):
        worker_uuid, = session.query(KubeWorkerIdentifier.worker_uuid).one()
        if worker_uuid == '':
            worker_uuid = str(uuid.uuid4())
            KubeWorkerIdentifier.checkpoint_kube_worker_uuid(worker_uuid, session)
        return worker_uuid

    @staticmethod
    @provide_session
    def checkpoint_kube_worker_uuid(worker_uuid, session=None):
        if worker_uuid:
            session.query(KubeWorkerIdentifier).update({KubeWorkerIdentifier.worker_uuid: worker_uuid})
            session.commit()