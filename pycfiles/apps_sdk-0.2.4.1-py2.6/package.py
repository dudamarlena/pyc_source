# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/apps/command/package.py
# Compiled at: 2010-08-10 18:55:20
import fnmatch, os, re, zipfile, apps.command.base

class package(apps.command.base.Command):
    help = 'Package the project into a .btapp file.'
    user_options = [
     ('path=', None, 'full path to place the package in.', None)]
    option_defaults = {'path': 'dist'}
    pre_commands = ['generate']

    def run(self):
        path = self.options['path']
        try:
            os.makedirs(path)
        except:
            pass

        extension = 'pkg' if self.project.metadata.get('bt:package', False) else 'btapp'
        btapp = zipfile.ZipFile(open(os.path.join(path, '%s.%s' % (
         self.project.metadata['name'], extension)), 'wb'), 'w')
        for f in self.file_list():
            fpath = os.path.split(f)
            arcname = os.path.join(*fpath[1:]) if re.match('\\..build', fpath[0]) else os.path.join(*fpath)
            btapp.write(f, arcname)

        btapp.close()