# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: c:\files\research\databrowse\databrowse\plugins\db_mercurial_repository\db_mercurial_repository.py
# Compiled at: 2018-06-29 17:51:46
""" plugins/renderers/db_directory_image.py - Basic Output for Any Folder """
import databrowse.plugins.db_directory.db_directory as db_directory_module, subprocess, os, traceback

class db_mercurial_repository(db_directory_module.db_directory):
    """ Image Directory Renderer """
    _default_content_mode = 'title'
    _default_style_mode = 'view_repository'
    _default_recursion_depth = 1

    @classmethod
    def uncommittedlist(cls, path):
        """ Check a path for uncommitted files """
        try:
            return [ (item[0], item[2:]) for item in subprocess.Popen(['/usr/bin/hg', '--cwd', path, 'status'], stdout=subprocess.PIPE, stderr=open(os.devnull)).communicate()[0].split('\n') if len(item) > 2 ]
        except:
            traceback.print_exc()
            return []

    def __init__(self, relpath, fullpath, web_support, handler_support, caller, handlers, content_mode=_default_content_mode, style_mode=_default_style_mode, recursion_depth=_default_recursion_depth):
        if caller == 'databrowse':
            self._namespace_uri = 'http://thermal.cnde.iastate.edu/databrowse/hgdir'
            self._namespace_local = 'hgdir'
        else:
            self._namespace_uri = 'http://thermal.cnde.iastate.edu/databrowse/dir'
            self._namespace_local = 'dir'
            self._disable_load_style = True
        super(db_mercurial_repository, self).__init__(relpath, fullpath, web_support, handler_support, caller, handlers, content_mode, style_mode)
        if caller == 'databrowse':
            uncommitted = self.uncommittedlist(fullpath)
            if len(uncommitted) > 0:
                self._xml.set('uncommitted', '%s' % len(uncommitted))