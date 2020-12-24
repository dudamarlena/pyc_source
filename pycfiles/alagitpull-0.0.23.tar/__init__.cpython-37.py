# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/c/Users/tony/source/repos/python/alagitpull/alagitpull/__init__.py
# Compiled at: 2019-05-18 13:06:25
# Size of source mod 2**32: 1768 bytes
import os
from alagitpull import _version as version
from writers.external import GitPullHTMLTranslator, ALLOWED_HOSTS
projects = [
 {'name':'unihan-etl', 
  'url':'https://unihan-etl.git-pull.com', 
  'subprojects':[
   {'name':'db', 
    'url':'https://unihan-db.git-pull.com'}]},
 {'name':'cihai', 
  'url':'https://cihai.git-pull.com', 
  'subprojects':[
   {'name':'cli', 
    'url':'https://cihai-cli.git-pull.com'}]},
 {'name':'tmuxp', 
  'url':'https://tmuxp.git-pull.com', 
  'subprojects':[
   {'name':'libtmux', 
    'url':'https://libtmux.git-pull.com'}]},
 {'name':'vcspull', 
  'url':'https://vcspull.git-pull.com', 
  'subprojects':[
   {'name':'libvcs', 
    'url':'https://libvcs.git-pull.com'}]}]

def get_path():
    """
    Shortcut for users whose theme is next to their conf.py.
    """
    return os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


def update_context(app, pagename, templatename, context, doctree):
    context['alagitpull_version'] = version.__version__


def setup(app):
    app.connect('html-page-context', update_context)
    app.set_translator('html', GitPullHTMLTranslator)
    app.set_translator('readthedocs', GitPullHTMLTranslator)
    app.add_config_value('alagitpull_internal_hosts', ALLOWED_HOSTS, 'html')
    app.add_config_value('alagitpull_external_hosts_new_window', False, 'html')
    return {'version':version.__version__, 
     'parallel_read_safe':True}