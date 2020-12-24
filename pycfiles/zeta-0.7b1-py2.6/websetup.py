# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/zeta/websetup.py
# Compiled at: 2010-07-05 00:40:23
"""Setup the zeta application"""
import logging, os, sys
from os.path import basename, join
import pylons.test, zeta.config.environment as environment
from zeta.config.environment import setup_environment, setup_models
from zeta.model import meta
from zeta.auth.users import UsersFromZetaDB
log = logging.getLogger(__name__)
virtualenv_pkgs = "\nALLDIRS = ['%s']\n\nimport sys\nimport site\n\n# Remember original sys.path.\nprev_sys_path = list( sys.path )\n\n# Add each new site-packages directory.\nfor directory in ALLDIRS:\n    site.addsitedir( directory )\n\n# Reorder sys.path so new directories at the front.\nnew_sys_path = []\nfor item in list( sys.path ) :\n    if item not in prev_sys_path:\n        new_sys_path.append( item )\n        sys.path.remove( item )\n\nsys.path[:0] = new_sys_path\n\n"

def setup_app(command, conf, vars):
    """Place any commands to setup zeta here"""
    userscomp = UsersFromZetaDB('zeta.model')
    print 'Loading environment and Creating database ... '
    config = setup_environment(conf.global_conf, conf.local_conf)
    print 'ok'
    environment.websetupconfig = config
    print 'Copying the environment directory ...'
    cmd = 'cp -r %s %s' % (join(config['zeta.pkg_path'], 'defenv'), config['zeta.envpath'])
    print cmd
    os.system(cmd)
    datadir = join('.', basename(config['zeta.envpath']), 'data')
    if not os.path.isdir(datadir):
        os.mkdir(datadir)
    print 'ok'
    setup_models(config, userscomp=userscomp)
    try:
        wsgi_file = os.path.abspath('defenv/mod_wsgi/dispatch.wsgi')
        sitepkgs = os.path.dirname(config['zeta.pkg_path'])
        eggcache = os.path.abspath('egg-cache')
        prodini = os.path.abspath('production.ini')
        text = []
        print 'Updating %s ... ' % wsgi_file,
        for l in open(wsgi_file).readlines():
            l = l.strip('\n\r')
            if l == '#add-virtualenv-packages':
                text.append(virtualenv_pkgs % sitepkgs)
            elif l == '#add-sitedir-here':
                text.append("site.addsitedir('%s')" % sitepkgs)
            elif l == '#add-eggcache-here':
                text.append("os.environ['PYTHON_EGG_CACHE'] = '" + eggcache + "'")
            elif l == '#add-config-here':
                text.append("application = loadapp('config:" + prodini + "')")
            else:
                text.append(l)

        open(wsgi_file, 'w').write(('\n').join(text))
        print 'ok'
    except:
        print sys.exc_info()
        raise