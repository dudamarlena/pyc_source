# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/merzky/saga/troy/troy/session.py
# Compiled at: 2014-02-27 11:31:04
__author__ = 'TROY Development Team'
__copyright__ = 'Copyright 2013, RADICAL'
__license__ = 'MIT'
import radical.utils as ru, os, re, fnmatch, saga, logging, radical.utils as ru, troy, troy.utils as tu

def _format_log_level(log_level):
    return {'debug': logging.DEBUG, 
       'info': logging.INFO, 
       'warning': logging.WARNING, 
       'error': logging.ERROR, 
       'critical': logging.CRITICAL}[log_level.lower()]
    raise ValueError('%s is not a valid value for log_level.' % log_level)


_config_skeleton = {'log_level': int(0), 
   'resource_config': None, 
   'resources': dict(), 
   'planner': {'expand': dict(), 
               'derive': dict()}, 
   'overlay_manager': {'overlay_translator': dict(), 
                       'overlay_transformer': dict(), 
                       'overlay_scheduler': dict(), 
                       'overlay_provisioner': dict()}, 
   'workload_manager': {'workload_parser': dict(), 
                        'workload_translator': dict(), 
                        'workload_transformer': dict(), 
                        'workload_scheduler': dict(), 
                        'workload_dispatcher': dict()}, 
   'strategy': {'strategy': dict()}}
_resource_config_skeleton = {'type': list(), 
   'username': None, 
   'home': None, 
   'queue': None, 
   'walltime': int(1440)}

class Session(saga.Session, tu.Timed):

    def __init__(self, user_cfg=None, default=True):
        if not isinstance(user_cfg, list):
            user_cfg = [
             user_cfg]
        self._apitype = 'saga.Session'
        resource_cfg = '%s/resources.json' % os.path.dirname(troy.__file__)
        config_dir = '%s/.troy' % os.environ.get('HOME', '/etc/')
        config_env = '%s' % os.environ.get('TROY_CONFIG', None)
        self.cfg = tu.get_config([_config_skeleton,
         resource_cfg,
         config_dir,
         config_env] + user_cfg)
        for res_name in self.cfg['resources']:
            ru.dict_merge(self.cfg['resources'][res_name], _resource_config_skeleton, policy='preserve', logger=troy._logger)

        log_level = 'ERROR'
        log_level = self.cfg.get('log_level', log_level)
        log_level = os.environ.get('TROY_VERBOSE', log_level)
        troy._logger.setLevel(log_level)
        session_id_stub = self.cfg.get('session_id', 'session.')
        self.id = ru.generate_id(session_id_stub, mode=ru.ID_UNIQUE)
        troy._logger.info('session id: %s' % self.id)
        tu.Timed.__init__(self, 'troy.Session', self.id)
        self.timed_method('saga.Session', ['init'], saga.Session.__init__, [self, default])
        return

    def __deepcopy__(self, other):
        return self

    def get_config(self, path='troy'):
        if isinstance(path, basestring):
            path = path.split(':')
        if path[0] == 'troy':
            path = path[1:]
        current_cfg = self.cfg
        current_path = 'troy'
        for idx, elem in enumerate(path):
            if elem not in current_cfg:
                if idx == len(path) - 1:
                    return dict()
                raise RuntimeError('no config "%s" beneath %s' % (
                 (':').join(path), current_path))
            if not isinstance(current_cfg[elem], dict):
                raise TypeError('no config dict "%s" beneath %s' % (
                 (':').join(path), current_path))
            current_cfg = current_cfg[elem]
            current_path = '%s:%s' % (current_path, elem)

        return current_cfg

    def get_resource_config(self, resource):
        try:
            resource_url = saga.Url(resource)
            if resource_url.host:
                resource = resource_url.host
        except saga.SagaException as e:
            pass

        resource_cfg = self.get_config('resources')
        troy._logger.debug('create resource config for %s' % resource)
        ret = dict(_resource_config_skeleton)
        for resource_key in resource_cfg.keys():
            if '*' in resource_key:
                resource_pattern = re.compile(fnmatch.translate(resource_key))
                if resource_pattern.match(resource):
                    troy._logger.debug('merge resource pattern %s for %s' % (
                     resource_key, resource))
                    ru.dict_merge(ret, resource_cfg[resource_key], policy='overwrite', logger=troy._logger)

        if resource in resource_cfg:
            troy._logger.debug('merge resource config for %s' % resource)
            ru.dict_merge(ret, resource_cfg[resource], policy='overwrite', logger=troy._logger)
        ret['hostname'] = resource
        return ret

    def _dump(self):
        print ' -------------------------------------'
        import pprint
        pprint.pprint(self.cfg)
        print ' -------------------------------------'


class Context(saga.Context):

    def __init__(self, ctype):
        self._apitype = 'saga.Context'
        saga.Context.__init__(self, ctype)