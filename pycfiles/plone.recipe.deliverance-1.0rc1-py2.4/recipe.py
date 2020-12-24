# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/plone/recipe/deliverance/recipe.py
# Compiled at: 2008-04-05 13:29:50
import logging, os, sys, shutil, tempfile, urllib2, urlparse, setuptools.archive_util, zc.buildout, zc.recipe.egg
from plone.recipe.deliverance import templates
WIN32 = False
if sys.platform[:3].lower() == 'win':
    WIN32 = True

def system(c):
    if os.system(c):
        raise SystemError('Failed', c)


class Recipe:
    __module__ = __name__

    def __init__(self, buildout, name, options):
        self.buildout = buildout
        self.name = name
        self.options = options
        options.setdefault('eggs', ('\n').join(['Deliverance', 'PasteScript']))
        options.setdefault('scripts', 'paster')
        options.setdefault('paster', os.path.join(buildout['buildout']['bin-directory'], 'paster'))
        self.egg = zc.recipe.egg.Egg(buildout, options['recipe'], options)
        self.libxml2_url = options.get('libxml2-url', 'http://xmlsoft.org/sources/libxml2-2.6.29.tar.gz')
        self.libxslt_url = options.get('libxslt-url', 'http://xmlsoft.org/sources/libxslt-1.1.21.tar.gz')
        python = buildout['buildout']['python']
        options['executable'] = buildout[python]['executable']
        options['location'] = os.path.join(buildout['buildout']['parts-directory'], self.name)

    def install(self):
        options = self.options
        location = options['location']
        if not os.path.exists(location):
            os.mkdir(location)
        here = os.getcwd()
        try:
            os.chdir(location)
            if not WIN32 and self.libxml2_url:
                self.cmmi(self.libxml2_url, '--without-python', location)
            if not WIN32 and self.libxslt_url:
                self.cmmi(self.libxslt_url, '--without-python --with-libxml-prefix=%s' % location, location)
            self.deliverance_layout()
            self.generate_wrapper()
        finally:
            os.chdir(here)
        self.egg.install()
        return location

    def update(self):
        self.deliverance_layout()
        self.generate_wrapper()

    def cmmi(self, url, extra_options, location):
        (_, _, urlpath, _, _, _) = urlparse.urlparse(url)
        tmp = tempfile.mkdtemp('buildout-' + self.name)
        tmp2 = tempfile.mkdtemp('buildout-' + self.name)
        try:
            fname = os.path.join(tmp2, urlpath.split('/')[(-1)])
            open(fname, 'w').write(urllib2.urlopen(url).read())
            setuptools.archive_util.unpack_archive(fname, tmp)
            here = os.getcwd()
            os.chdir(tmp)
            try:
                if not os.path.exists('configure'):
                    entries = os.listdir(tmp)
                    if len(entries) == 1:
                        os.chdir(entries[0])
                    else:
                        raise ValueError("Couldn't find configure")
                system('./configure --prefix=%s %s' % (location, extra_options))
                system('make')
                system('make install')
            finally:
                os.chdir(here)
        finally:
            shutil.rmtree(tmp)
            shutil.rmtree(tmp2)

    def deliverance_layout(self, force=False, update_settings=True):
        options = self.options
        directory = self.buildout['buildout']['directory']
        layout_directory = os.path.join(directory, self.name)
        if force and os.path.exists(layout_directory):
            shutil.rmtree(layout_directory)
        new = False
        if not os.path.exists(layout_directory):
            os.mkdir(layout_directory)
            new = True
        if not os.path.exists(os.path.join(layout_directory, 'static')):
            os.mkdir(os.path.join(layout_directory, 'static'))
            new = True
        if not os.path.exists(os.path.join(layout_directory, 'rules')):
            os.mkdir(os.path.join(layout_directory, 'rules'))
            new = True
        if not new and not update_settings:
            return
        ini_path = os.path.join(layout_directory, 'deliverance-proxy.ini')
        if os.path.exists(ini_path):
            os.unlink(ini_path)
        open(ini_path, 'w').write(templates.DELIVERANCE_INI % {'location': layout_directory, 'directory': directory, 'name': self.name, 'debug': options.get('debug', 'true'), 'host': options.get('host', '0.0.0.0'), 'port': options.get('port', '8000'), 'proxy': options.get('proxy', 'http://localhost:8080'), 'theme': options.get('theme', '/.deliverance/static/theme.html'), 'rules': options.get('rules', '/.deliverance/rules/rules.xml'), 'transparent': options.get('transparent', 'true'), 'rewrite': options.get('rewrite', 'true'), 'serializer': options.get('serializer', 'deliverance.serializers.HTML4')})
        if not os.path.exists(os.path.join(directory, 'var')):
            os.mkdir(os.path.join(directory, 'var'))
        if not os.path.exists(os.path.join(directory, 'var', 'run')):
            os.mkdir(os.path.join(directory, 'var', 'run'))
        if not os.path.exists(os.path.join(directory, 'var', 'log')):
            os.mkdir(os.path.join(directory, 'var', 'log'))
        if not os.path.exists(os.path.join(layout_directory, 'static', 'theme.html')):
            open(os.path.join(layout_directory, 'static', 'theme.html'), 'w').write(templates.DEFAULT_THEME)
        if not os.path.exists(os.path.join(layout_directory, 'rules', 'rules.xml')):
            open(os.path.join(layout_directory, 'rules', 'rules.xml'), 'w').write(templates.DEFAULT_RULES)
            if not os.path.exists(os.path.join(layout_directory, 'rules', 'standardrules.xml')):
                open(os.path.join(layout_directory, 'rules', 'standardrules.xml'), 'w').write(templates.STANDARD_RULES)

    def generate_wrapper(self):
        (requirements, ws) = self.egg.working_set(['plone.recipe.deliverance'])
        directory = self.buildout['buildout']['directory']
        lib_path = ''
        if not WIN32 and (self.libxml2_url or self.libxslt_url):
            lib_path = os.path.join(self.options['location'], 'lib')
        paster_path = self.options['paster']
        ini_path = os.path.join(directory, self.name, 'deliverance-proxy.ini')
        zc.buildout.easy_install.scripts([('deliverance', 'plone.recipe.deliverance.ctl', 'main')], ws, self.options['executable'], self.buildout['buildout']['bin-directory'], arguments='\n        [%r,\n         %r,\n         %r]\n        + sys.argv[1:]' % (lib_path, paster_path, ini_path))