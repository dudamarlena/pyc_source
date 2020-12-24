# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/clue/app/environinit.py
# Compiled at: 2008-06-27 12:03:50
from clue.app import utils

class EnvironInitFilter(object):
    """Middleware setting up the environ container with information
    from global_conf.

      >>> gf = {'cluemapper.templateloader': None,
      ...       'cluemapper.config': None,
      ...       'cluemapper.workingdir': None}
      >>> f = EnvironInitFilter(lambda x,y: None, gf)
      >>> f({'SCRIPT_NAME': '', 'PATH_INFO': ''}, None)
    """

    def __init__(self, app, global_conf):
        self.app = app
        self.global_conf = global_conf

    def _sync_environ(self, environ):
        for x in ('templateloader', 'config', 'workingdir'):
            name = 'cluemapper.' + x
            if name not in environ:
                environ[name] = self.global_conf[name]

        prjid = utils.get_prjid(environ)
        if prjid:
            cluemapperconfig = self.global_conf['cluemapper.config']
            if 'project:' + prjid in cluemapperconfig.keys():
                prjconfig = cluemapperconfig[('project:' + prjid)]
                if 'theme' in prjconfig:
                    environ['cluemapper.themeid'] = prjconfig['theme']

    def __call__(self, environ, start_response):
        self._sync_environ(environ)
        return self.app(environ, start_response)


make_filter = EnvironInitFilter