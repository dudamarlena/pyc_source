# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/iw/recipe/pound/build.py
# Compiled at: 2008-07-02 13:21:38
"""Build Recipe pound"""
import os, zc, logging
from zc.recipe.cmmi import Recipe as CMMIRecipe
TEMPLATE = '#!/bin/sh\n\n%(pound)s -f %(cfg)s -p %(pid)s\n\n'

class BuildRecipe(CMMIRecipe):
    """This recipe is used by zc.buildout"""
    __module__ = __name__

    def __init__(self, buildout, name, options):
        CMMIRecipe.__init__(self, buildout, name, options)
        self.buildout = buildout
        self.logger = logging.getLogger(self.name)

    def install(self):
        """installer"""
        try:
            owner = self.options.get('owner', os.getlogin())
        except OSError:
            owner = os.environ['USER']

        group = self.options.get('group', owner)
        ssl_dir = self.options.get('ssl_dir', None)
        t_rsa = self.options.get('t_rsa', None)
        extra_options = self.options.get('extra-options', None)
        extra = '--with-owner=%s --with-group=%s' % (owner, group)
        if ssl_dir is not None:
            if os.path.isdir(ssl_dir):
                extra += ' --with-ssl=%s' % ssl_dir
            else:
                self.logger.error('You need to specify an valid directory for ssl directory')
                raise zc.buildout.UserError('ssl directory is invalid')
        if t_rsa is not None:
            try:
                t_rsa = int(t_rsa)
                extra += ' --with-t_rsa=%d' % (t_rsa,)
            except ValueError:
                self.logger.error('You need to specify an integer for timeout rsa')
                raise zc.buildout.UserError('Time out rsa is invalid')

        if extra_options is not None:
            extra += ' %s' % (extra_options,)
        self.logger.info('compilation option : %s' % (extra,))
        self.options['extra_options'] = extra
        installed = CMMIRecipe.install(self)
        command = os.path.join(self.options['location'], 'sbin', 'pound')
        var_dir = os.path.join(self.options['location'], 'var')
        pid = os.path.join(var_dir, 'pound.pid')
        script = TEMPLATE % {'pound': command, 'cfg': self.getFileNameConfig(), 'pid': pid}
        bin_dir = self.buildout['buildout']['bin-directory']
        script_name = os.path.join(bin_dir, self.name)
        f = open(script_name, 'wb')
        f.write(script)
        f.close()
        os.chmod(script_name, 493)
        return (installed, script_name)

    def getFileNameConfig(self):
        return 'pound.cfg'

    def update(self):
        pass