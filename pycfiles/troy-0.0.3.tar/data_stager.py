# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/merzky/saga/troy/troy/workload/data_stager.py
# Compiled at: 2014-02-27 11:31:04
__author__ = 'TROY Development Team'
__copyright__ = 'Copyright 2013, RADICAL'
__license__ = 'MIT'
import os, saga, radical.utils as ru, troy.utils as tu
from troy.constants import *
import troy

class DataStager(object):
    """
    staging directives

       [local_path] [operator] [remote_path]

    local path: 
        * interpreted as relative to the application's working directory
        * must point to local storage (localhost)
    
    remote path
        * interpreted as relative to the task's working directory

    operator :
        * >  : stage to remote target, overwrite if exists
        * >> : stage to remote target, append    if exists
        * <  : stage to local  target, overwrite if exists
        * << : stage to local  target, append    if exists

    """

    def __init__(self, session):
        """
        FIXME
        """
        self.session = session
        self._dir_cache = dict()

    def _parse_staging_directive(self, txt):
        """
        returns [src, tgt, op] as relative or absolute paths or URLs.  This
        parsing is backward compatible with the simple staging directives used
        in troy previously -- any strings which do not contain staging operators
        will be interpreted as simple paths (identical for src and tgt,
        operation set to '=', which is interpreted as ).

        Supported directives:

           src >  tgt -- stage  task input ./src to remote remote.host as ./tgt
           src >> tgt -- append task input ./src to remote remote.host    ./tgt
           tgt <  src -- stage  task output from remote host ./src to     ./tgt
           tgt << src -- append task output from remote host ./src to     ./tgt
        """
        rs = ru.ReString(txt)
        if rs // '^(?P<one>.+?)\\s*(?P<op><|<<|>|>>)\\s*(?P<two>.+)$':
            res = rs.get()
            return (
             res['one'], res['two'], res['op'])
        else:
            return (
             txt, txt, '=')

    def stage_in_workload(self, workload):
        for task_id in workload.tasks:
            self._stage_in_task(workload.tasks[task_id])

    def _stage_in_task(self, task):
        for unit_id in task.units:
            self._stage_in_unit(task.units[unit_id])

    def _stage_in_unit(self, unit):
        if unit.staged_in:
            return
        else:
            if not len(unit.inputs):
                return
            pilot = troy.Pilot(unit.session, unit.pilot_id)
            resource = pilot.resource
            resource_cfg = unit.session.get_resource_config(resource)
            unit.merge_description(resource_cfg)
            workdir = unit.working_directory
            username = None
            if 'username' in unit.as_dict():
                username = unit.username
            if not workdir:
                raise RuntimeError('no working directory defined for %s - cannot stage-in' % unit.id)
            if not pilot:
                raise RuntimeError('unit %s not bound  - cannot stage-in' % unit.id)
            if not resource:
                raise RuntimeError('pilot not bound %s - cannot stage-in' % unit.id)
            for fin in unit.inputs:
                if not isinstance(fin, basestring):
                    raise TypeError('Input specs need to be strings, not %s' % type(fin))
                one, two, op = self._parse_staging_directive(fin)
                if op in ('>>', ):
                    raise ValueError("op '>>' not yet supported for input staging")
                if op not in ('>', '='):
                    raise ValueError("'%s' not supported for input staging" % op)
                troy._logger.info('staging_in %s < %s / %s / %s' % (
                 one, pilot.resource, workdir, two))
                self._stage_in_file(one, pilot.resource, workdir, two, username)

            unit.staged_in = True
            return

    def _stage_in_file(self, src, resource, workdir, tgt, username=None):
        """
        src file element can contain wildcards.  
        tgt can not contain wildcards -- but must be a directory URL.
        """
        if workdir[0] != '/':
            raise ValueError('target directory must have absolute path, not %s' % workdir)
        if tgt[0] != '/':
            tgt = os.path.normpath('%s/%s' % (workdir, tgt))
        if src[0] != '/':
            src = os.path.normpath('%s/%s' % (os.getcwd(), src))
        src_url = saga.Url(src)
        if not src_url.host and not src_url.schema:
            src_url = saga.Url('file://localhost%s' % src)
        resource_url = saga.Url(resource)
        if resource_url.schema.endswith('ssh+'):
            resource_url.schema = 'ssh'
        if resource_url.schema.endswith('+ssh'):
            resource_url.schema = 'ssh'
        if resource_url.schema.endswith('fork'):
            resource_url.schema = 'file'
        if username:
            resource_url.username = username
        troy._logger.debug('copy %s -> %s / %s' % (src_url, resource_url, tgt))
        if str(resource) not in self._dir_cache:
            self._dir_cache[str(resource)] = saga.filesystem.Directory(resource_url, session=self.session)
        tgt_dir = self._dir_cache[str(resource)]
        tgt_dir.change_dir(os.path.dirname(tgt), saga.filesystem.CREATE_PARENTS)
        tgt_dir.copy(src_url, tgt)

    def stage_out_workload(self, workload):
        for task_id in workload.tasks:
            self._stage_out_task(workload.tasks[task_id])

    def _stage_out_task(self, task):
        for unit_id in task.units:
            self._stage_out_unit(task.units[unit_id])

    def _stage_out_unit(self, unit):
        if unit.staged_out:
            return
        else:
            if not len(unit.outputs):
                return
            pilot = troy.Pilot(unit.session, unit.pilot_id)
            resource = pilot.resource
            workdir = unit.working_directory
            username = None
            if 'username' in unit.as_dict():
                username = unit.username
            if not workdir:
                raise RuntimeError('no working directory defined for %s - cannot stage-out' % unit.id)
            if not pilot:
                raise RuntimeError('unit %s not bound  - cannot stage-out' % unit.id)
            if not resource:
                raise RuntimeError('pilot not bound %s - cannot stage-out' % unit.id)
            for fout in unit.outputs:
                if not isinstance(fout, basestring):
                    raise TypeError('Input specs need to be strings, not %s' % type(fout))
                one, two, op = self._parse_staging_directive(fout)
                if op in ('<<', ):
                    raise ValueError("'<<' not yet supported for output staging")
                if op not in ('<', '='):
                    raise ValueError("'%s' not supported for output staging" % op)
                troy._logger.info('staging_out %s < %s / %s / %s' % (
                 one, pilot.resource, workdir, two))
                self._stage_out_file(one, pilot.resource, workdir, two, username)

            unit.staged_out = True
            return

    def _stage_out_file(self, tgt, resource, srcdir, src, username=None):
        """
        src file element can contain wildcards.  
        tgt can not contain wildcards -- but it can be a directory URL (and, in
        fact, is interpreted as such if src contains wildcard chars).
        """
        if tgt[0] != '/':
            tgt = '%s/%s' % (os.getcwd(), tgt)
        while srcdir[0] == '/':
            srcdir = srcdir[1:]

        while srcdir[(-1)] == '/':
            srcdir = srcdir[0:-1]

        while resource[(-1)] == '/':
            resource = resource[0:-1]

        src_url = saga.Url('/%s/%s' % (srcdir, src))
        tgt_url = saga.Url('file://localhost%s' % tgt)
        src_dir_url = saga.Url(src_url)
        src_dir_url.path = os.path.dirname(src_url.path)
        resource_url = saga.Url(resource)
        if resource_url.schema.startswith('ssh+') or resource_url.schema.startswith('gsissh+') or resource_url.schema.endswith('+ssh') or resource_url.schema.endswith('+gsissh'):
            resource_url.schema = 'ssh'
        if resource_url.schema.endswith('fork'):
            resource_url.schema = 'file'
        if username:
            resource_url.username = username
        troy._logger.debug('copy %s <- %s' % (tgt_url, src_url))
        if str(resource) not in self._dir_cache:
            self._dir_cache[str(resource)] = saga.filesystem.Directory(resource_url, session=self.session)
        src_dir = self._dir_cache[str(resource)]
        src_dir.change_dir(src_dir_url.path)
        src_dir.copy(src_url, tgt_url, saga.filesystem.CREATE_PARENTS)