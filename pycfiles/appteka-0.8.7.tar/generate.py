# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/apps/command/generate.py
# Compiled at: 2010-09-24 15:52:30
import json, logging, mako.template, os, pkg_resources, urlparse, apps.command.base

class generate(apps.command.base.Command):
    help = 'Generate `index.html` for the project.'
    user_options = [
     ('update=', None, 'Auto-update url to use in package.json', None)]
    excludes = [os.path.join('packages', 'firebug.js'),
     os.path.join('lib', 'index.js')]

    def run(self):
        update_json = True
        if self.options.get('update', False):
            self.project.metadata['bt:update_url'] = self.options['update']
            update_json = False
        self.write_metadata(update_json)
        if not os.path.exists('packages/'):
            self.update_deps()
        if self.project.metadata.get('bt:package', False):
            return
        logging.info('\tcreating index.html')
        self.flist = [ x[2:] for x in self.file_list() ]
        template = mako.template.Template(filename=pkg_resources.resource_filename('apps.data', 'index.html'), cache_enabled=False)
        if not os.path.exists(os.path.join(self.project.path, 'build')):
            os.mkdir(os.path.join(self.project.path, 'build'))
        index = open(os.path.join(self.project.path, 'build', 'index.html'), 'wb')
        index.write(template.render(scripts=self._scripts_list(self.project.metadata), styles=self._styles_list(), title=self.project.metadata['name'], debug=self.vanguard.options.debug))
        index.close()

    def _styles_list(self):
        path = os.path.join(self.project.path, 'css')
        if os.path.exists(path):
            return [ os.path.join('css', x).replace('\\', '/') for x in filter(lambda x: os.path.splitext(x)[1] == '.css', os.listdir(path))
                   ]
        return []

    def filter(self, existing, lst):
        return filter(lambda x: x not in existing and x not in self.excludes and x in self.flist, lst)

    def _scripts_list(self, metadata):
        handlers = {'.js': self._list_lib, '.pkg': self._list_pkg}
        scripts = []
        for lib in metadata.get('bt:libs', []):
            ext = os.path.splitext(urlparse.urlsplit(lib['url']).path)[(-1)]
            scripts += self.filter(scripts, [ x.replace('/', os.path.sep) for x in handlers[ext](lib)
                                            ])

        if metadata == self.project.metadata:
            scripts += self.filter(scripts, [ os.path.join('lib', x) for x in sorted(filter(lambda x: os.path.splitext(x)[1] == '.js', os.listdir(os.path.join(self.project.path, 'lib'))))
                                            ])
            scripts.append(os.path.join('lib', 'index.js'))
        scripts = [ x.replace('\\', '/') for x in scripts ]
        return scripts

    def _list_lib(self, lib):
        name = os.path.split(urlparse.urlsplit(lib['url']).path)[(-1)]
        return [
         os.path.join('packages', name)]

    def _list_pkg(self, pkg):
        pkg_scripts = self._scripts_list(json.load(open(os.path.join(self.project.path, 'packages', pkg['name'], 'package.json'))))
        pkg_scripts += sorted([ os.path.join('packages', pkg['name'], x) for x in filter(lambda x: x != 'package.json', os.listdir(os.path.join(self.project.path, 'packages', pkg['name'])))
                              ])
        return pkg_scripts