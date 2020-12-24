# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/models/counter.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
from django.db import connection, connections
from django.db.models.signals import post_syncdb
from sentry.db.models import FlexibleForeignKey, Model, sane_repr, BoundedBigIntegerField
from sentry.utils.db import is_postgres

class Counter(Model):
    __core__ = True
    project = FlexibleForeignKey('sentry.Project', unique=True)
    value = BoundedBigIntegerField()
    __repr__ = sane_repr('project')

    class Meta:
        app_label = 'sentry'
        db_table = 'sentry_projectcounter'

    @classmethod
    def increment(cls, project, delta=1):
        """Increments a counter.  This can never decrement."""
        return increment_project_counter(project, delta)


def increment_project_counter(project, delta=1):
    """This method primarily exists so that south code can use it."""
    if delta <= 0:
        raise ValueError("There is only one way, and that's up.")
    cur = connection.cursor()
    try:
        if is_postgres():
            cur.execute('\n                select sentry_increment_project_counter(%s, %s)\n            ', [
             project.id, delta])
            return cur.fetchone()[0]
        raise AssertionError('Not implemented database engine path')
    finally:
        cur.close()


def create_counter_function(db, created_models, app=None, **kwargs):
    if app and app.__name__ != 'sentry.models':
        return
    if not is_postgres(db):
        return
    if Counter not in created_models:
        return
    cursor = connections[db].cursor()
    try:
        cursor.execute('\n            create or replace function sentry_increment_project_counter(\n                project bigint, delta int) returns int as $$\n            declare\n            new_val int;\n            begin\n            loop\n                update sentry_projectcounter set value = value + delta\n                where project_id = project\n                returning value into new_val;\n                if found then\n                return new_val;\n                end if;\n                begin\n                insert into sentry_projectcounter(project_id, value)\n                    values (project, delta)\n                    returning value into new_val;\n                return new_val;\n                exception when unique_violation then\n                end;\n            end loop;\n            end\n            $$ language plpgsql;\n        ')
    finally:
        cursor.close()


post_syncdb.connect(create_counter_function, dispatch_uid='create_counter_function', weak=False)