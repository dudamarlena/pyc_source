# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/www_rbac/decorators.py
# Compiled at: 2019-09-11 03:47:35
# Size of source mod 2**32: 4549 bytes
import gzip, functools, pendulum
from io import BytesIO as IO
from flask import after_this_request, flash, redirect, request, url_for, g
from airflow.models import Log
from airflow.utils.db import create_session

def action_logging(f):
    """
    Decorator to log user actions
    """

    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        with create_session() as (session):
            if g.user.is_anonymous:
                user = 'anonymous'
            else:
                user = g.user.username
            log = Log(event=(f.__name__),
              task_instance=None,
              owner=user,
              extra=(str(list(request.args.items()))),
              task_id=(request.args.get('task_id')),
              dag_id=(request.args.get('dag_id')))
            if 'execution_date' in request.args:
                log.execution_date = pendulum.parse(request.args.get('execution_date'))
            session.add(log)
        return f(*args, **kwargs)

    return wrapper


def gzipped(f):
    """
    Decorator to make a view compressed
    """

    @functools.wraps(f)
    def view_func(*args, **kwargs):

        @after_this_request
        def zipper(response):
            accept_encoding = request.headers.get('Accept-Encoding', '')
            if 'gzip' not in accept_encoding.lower():
                return response
            else:
                response.direct_passthrough = False
                if response.status_code < 200 or response.status_code >= 300 or 'Content-Encoding' in response.headers:
                    return response
                gzip_buffer = IO()
                gzip_file = gzip.GzipFile(mode='wb', fileobj=gzip_buffer)
                gzip_file.write(response.data)
                gzip_file.close()
                response.data = gzip_buffer.getvalue()
                response.headers['Content-Encoding'] = 'gzip'
                response.headers['Vary'] = 'Accept-Encoding'
                response.headers['Content-Length'] = len(response.data)
                return response

        return f(*args, **kwargs)

    return view_func


def has_dag_access(**dag_kwargs):
    """
    Decorator to check whether the user has read / write permission on the dag.
    """

    def decorator(f):

        @functools.wraps(f)
        def wrapper(self, *args, **kwargs):
            has_access = self.appbuilder.sm.has_access
            dag_id = request.values.get('dag_id')
            can_dag_edit = dag_kwargs.get('can_dag_edit', False)
            if has_access('can_dag_edit', 'all_dags') or has_access('can_dag_edit', dag_id) or not can_dag_edit and (has_access('can_dag_read', 'all_dags') or has_access('can_dag_read', dag_id)):
                return f(self, *args, **kwargs)
            else:
                flash('Access is Denied', 'danger')
                return redirect(url_for(self.appbuilder.sm.auth_view.__class__.__name__ + '.login'))

        return wrapper

    return decorator