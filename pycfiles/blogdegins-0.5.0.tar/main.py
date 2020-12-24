# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/gines/midesarrollo/hg-projects/blogdegins/blogdegins/main.py
# Compiled at: 2014-05-14 07:04:19
"""
Utility for creating static html code.
"""
import argparse, sys, os.path, stat, shutil, envoy
try:
    from ConfigParser import ConfigParser
except:
    from configparser import ConfigParser

import logging
logging.basicConfig(level=logging.DEBUG)
from blogdegins.getyesno import getyesno
BLOGDEGINS_INI = 'blogdegins.ini'
comandos = [
 'init', 'skeleton', 'render', 'page', 'widget', 'rsync']

def get_python_page_code(Content, content, is_widget=False, widget_dir=None):
    if is_widget:
        widget_path = os.path.join('widgets' if not widget_dir else widget_dir, content, '')
    else:
        widget_path = ''
    package = "__package__.split('.')[0]"
    python_page_code = ("# -*- encoding: utf-8 -*-\nfrom ghtml.c_ghtml import GHtml\nfrom ginsfsm.gconfig import add_gconfig\n\n{content}_data = {{\n    'myname': 'Blogdegins.',\n}}\n\n{Content}_CONFIG = {{\n    'gaplic_namespace': [\n        str, '', 0, None,\n        'namespace of gaplic, to store callbacks.',\n    ],\n    '{content}_options': [\n        dict,\n        {{\n            # See default values in the partner javascript file.\n        }},\n        0,\n        None,\n        'A dictionary containing the javascript options.'\n    ],\n}}\n\n\nclass {Content}(GHtml):\n    def __init__(self, fsm=None, gconfig=None):\n        gconfig = add_gconfig(gconfig, {Content}_CONFIG)\n        super({Content}, self).__init__(fsm=fsm, gconfig=gconfig)\n\n    def start_up(self):\n        pass\n\n    def render(self, **kw):\n        kw.update(**{content}_data)\n        return super({Content}, self).render(**kw)\n\n\ndef create_{content}(name, parent, **kw):\n    ''' Remember put in parent python code:\n\n        from ?.{content} import create_{content}\n        create_{content}(\n            '{content}',  # the name you have to put in parent mako: ${{content}}\n            self,\n        )\n    '''\n    {content} = parent.create_gobj(\n        name,\n        {Content},\n        parent,\n        template='/%s/htmlrendercode/{widget_path}{content}.mako' % (\n            __package__.split('.')[0]),\n        **kw\n    )\n    return {content}\n\n").format(Content=Content, content=content, package=package, widget_path=widget_path)
    return python_page_code


def get_init_py_widget_code(content):
    init_py_widget_code = ('from {content} import create_{content}\n').format(content=content)
    return init_py_widget_code


mako_page_code = ''
javascript_page_code = 'jQuery(function($) {\n    // Your code using failsafe $ alias here...\n\n    $(function() {\n        // Document is ready\n    });\n\n});\n'
scss_page_code = ''
setup_cfg_file = '[egg_info]\ntag_build =\ntag_svn_revision = false\ntag_date = 0\n\n[easy_install]\nzip_ok = false\n'
setup_py_file = '# -*- encoding: utf-8 -*-\n\nimport os\nimport sys\n\nfrom setuptools import setup, find_packages\n\nif sys.version_info[:2] < (2, 6):\n    raise RuntimeError(\'Requires Python 2.6 or better\')\n\nhere = os.path.abspath(os.path.dirname(__file__))\ntry:\n    README = open(os.path.join(here, \'README.rst\')).read()\n    CHANGES = open(os.path.join(here, \'CHANGES.txt\')).read()\nexcept IOError:\n    README = CHANGES = \'\'\n\nversion = \'0.0.0\'\n\nrequires = [\'blogdegins\']\n\nsetup(name=\'{package}\',\n    version=version,\n    description=\'{package}\',\n    long_description=\'\',\n    classifiers=[\n        "Programming Language :: Python",\n    ],\n    author=\'\',\n    author_email=\'\',\n    url=\'\',\n    license=\'\',\n    keywords=\'blogdegins\',\n    packages=find_packages(),\n    include_package_data=True,\n    zip_safe=False,\n    install_requires=requires,\n    tests_require=requires,\n    test_suite="{package}.tests",\n    entry_points=\'\'\'    \'\'\',\n)\n'
watch_file = '#!/bin/sh\nfind tags/0.00.aa/static -type f -name \'*.scss.css\' -exec rm {} \\;\nrm -rf tags/0.00.aa/static/.sass-cache/ tags/0.00.aa/static/.webassets-cache/ tags/0.00.aa/.cache/ ;\nmake\n\n# force remove scss cache\nwatchmedo shell-command     --patterns="*.py;*.mako;*.js;*.css;*.scss"     --recursive     --command=\'find tags/0.00.aa/static -type f -name \'*.scss.css\' -exec rm {} \\;rm -rf tags/0.00.aa/static/.sass-cache/ tags/0.00.aa/static/.webassets-cache/ tags/0.00.aa/.cache/ ; make\'     .\n'

def main(argv=sys.argv):
    command = Blogdegins(argv)
    return command.run()


class Blogdegins(object):
    description = 'Generate static html code.'
    parser = argparse.ArgumentParser(description=description, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('command', choices=comandos, help='Available commands:\ninit {project} ==> create a .ini file and the directory structure.\nskeleton ==> create a new tag directory, copying a assets directory.\nrender ==> generate a new index.html, in tags/{version} directory.\npage {name} ==> creat a new set of py/js/mako/scss files in main directory.\nwidget {name} [widget_path] ==> creat a new wigdet directory with their set of py/js/mako/scss files in the widgets directory\nrsync ==> syncronize the tag version with the remote host.\n')
    parser.add_argument('arguments', nargs=argparse.REMAINDER, help='Arguments to command.')
    parser.add_argument('-d', '--debug', dest='debug', action='store_true', help='True if render in development mode, False in production mode.')
    parser.add_argument('-v', '--verbose', help='Increase output verbosity', action='store_true')

    def __init__(self, argv=sys.argv):
        self.args = self.parser.parse_args(argv[1:])
        if self.args.debug:
            self.args.verbose = True

    def run(self):
        cmd = self.args.command
        fn = getattr(self, cmd)
        if cmd != 'init':
            self.load_ini()
        return fn()

    def init(self):
        """ create a .ini file and the directory structure
        """
        print '====> init'
        if not self.args.arguments:
            print '<---- * You must supply a project name!'
            return 2
        project = self.args.arguments[0].lower()
        output_dir = os.path.abspath(os.path.normpath(project))
        if os.path.exists(output_dir):
            print '<---- * Directory "%s" already exists!' % output_dir
            return 2
        print '<---- * Creating blogdegins project in "%s".' % output_dir
        os.mkdir(output_dir)
        src_path = self.assets_dir()
        dst_path = os.path.join(output_dir, 'assets')
        shutil.copytree(src_path, dst_path, symlinks=True)
        src_path = self.code_dir()
        dst_path = os.path.join(output_dir, project, 'htmlrendercode')
        shutil.copytree(src_path, dst_path, ignore=shutil.ignore_patterns('*.pyc', '*~'), symlinks=True)
        init_py = os.path.join(output_dir, project, '__init__.py')
        with open(init_py, 'w') as (f):
            f.write('import htmlrendercode  # needed to dynamic import from blogdegins')
        setup_cfg = os.path.join(output_dir, 'setup.cfg')
        with open(setup_cfg, 'w') as (f):
            f.write(setup_cfg_file)
        setup_py = os.path.join(output_dir, 'setup.py')
        with open(setup_py, 'w') as (f):
            f.write(setup_py_file.format(package=project))
        watch = os.path.join(output_dir, 'watch.sh')
        with open(watch, 'w') as (f):
            f.write(watch_file)
        st = os.stat(output_dir)
        os.chmod(output_dir, st.st_mode | stat.S_IEXEC)
        os.mkdir(os.path.join(output_dir, 'tags'))
        current_tag = '0.00.aa'
        config = ConfigParser()
        config.set('DEFAULT', 'current_tag', current_tag)
        config.add_section('tags')
        config.set('tags', current_tag, '')
        config.add_section(current_tag)
        config.set(current_tag, 'assets', os.path.join('assets', 'h5bp-moderm-browsers-2014-05-14'))
        config.set(current_tag, 'remote-server', '')
        ini_file = os.path.join(output_dir, BLOGDEGINS_INI)
        with open(ini_file, 'w') as (configfile):
            config.write(configfile)
        util_names = os.listdir(self.utils_dir())
        for name in util_names:
            srcname = os.path.join(self.utils_dir(), name)
            shutil.copy2(srcname, output_dir)

        return 0

    def load_ini(self):
        if not os.path.exists(BLOGDEGINS_INI):
            print 'File "%s" NOT found.' % BLOGDEGINS_INI
            exit(2)
        here = os.path.dirname(os.path.abspath(BLOGDEGINS_INI))
        self.config = ConfigParser({'here': here})
        self.config.read(BLOGDEGINS_INI)
        self.config.here = here
        self.config.current_tag = self.config.get('DEFAULT', 'current_tag')

    def module_dir(self):
        mod = sys.modules[self.__class__.__module__]
        return os.path.dirname(mod.__file__)

    def assets_dir(self):
        return os.path.join(self.module_dir(), 'assets')

    def code_dir(self):
        return os.path.join(self.module_dir(), '_htmlrendercode')

    def utils_dir(self):
        return os.path.join(self.module_dir(), 'utils')

    def current_tag_dir(self):
        return os.path.join(self.config.here, 'tags', self.config.current_tag)

    def skeleton(self):
        """ create a new tag directory, copying a assets directory
        """
        print '====> skeleton'
        dst_path = self.current_tag_dir()
        if not os.path.exists(dst_path):
            print '<---- * Creating "%s" directory.' % dst_path
        else:
            resp = getyesno('You are re-creating the skeleton "%s".\nYou will loose your data! Are you sure?' % dst_path, default='n')
            if not resp:
                print '<---- * Operation aborted.'
                return 2
            print '<---- * Re-creating "%s" directory.' % dst_path
            shutil.rmtree(dst_path)
        assets = self.config.get(self.config.current_tag, 'assets')
        src_path = os.path.join(self.config.here, assets)
        shutil.copytree(src_path, dst_path, symlinks=True)
        return 0

    def widget(self):
        """ creat a new widget directory
        with their set of py/js/mako/scss files in the widgets directory
        """
        print '====> widget'
        if not self.args.arguments:
            print '<---- * You must supply a name!'
            return 2
        else:
            name = self.args.arguments[0].lower()
            Name = name.capitalize()
            if len(self.args.arguments) >= 2:
                widget_dir = self.args.arguments[1]
            else:
                widget_dir = None
            self._make_set(name, get_python_page_code(Name, name, True, widget_dir), mako_page_code, javascript_page_code, scss_page_code, True, widget_dir)
            return

    def page(self):
        """ creat a new set of py/js/mako/scss files in the main directory
        """
        print '====> page'
        if not self.args.arguments:
            print '<---- * You must supply a name!'
            return 2
        else:
            name = self.args.arguments[0].lower()
            Name = name.capitalize()
            if len(self.args.arguments) >= 2:
                page_dir = self.args.arguments[1]
            else:
                page_dir = None
            self._make_set(name, get_python_page_code(Name, name), mako_page_code, javascript_page_code, scss_page_code)
            return

    def _make_set(self, name, python_page_code, mako_page_code, javascript_page_code, scss_page_code, is_widget=False, widget_dir=None):
        project = os.path.basename(self.config.here).lower()
        if not is_widget:
            rendercode_path = os.path.join(self.config.here, project, 'htmlrendercode')
        else:
            rendercode_path = os.path.join(self.config.here, project, 'htmlrendercode', 'widgets' if not widget_dir else widget_dir, name)
        if not os.path.exists(self.current_tag_dir()):
            print '<---- * First you must create a tag skeleton.'
            exit(2)
        if not os.path.exists(rendercode_path):
            os.mkdir(rendercode_path)
        py_file = '%s.py' % name
        js_file = '%s.js' % name
        scss_file = '%s.scss' % name
        mako_file = '%s.mako' % name
        widget_path = os.path.join(rendercode_path)
        if not os.path.exists(widget_path):
            os.mkdir(widget_path)
        filename = os.path.join(rendercode_path, '__init__.py')
        if not os.path.exists(filename):
            fd = open(filename, 'w')
            if is_widget:
                fd.write(get_init_py_widget_code(name))
            else:
                fd.write('')
            fd.close()
        filename = os.path.join(rendercode_path, py_file)
        if not os.path.exists(filename):
            print '<---- * Creating "%s" file.' % filename
            fd = open(filename, 'w')
            fd.write(python_page_code)
            fd.close()
        filename = os.path.join(rendercode_path, mako_file)
        if not os.path.exists(filename):
            print '<---- * Creating "%s" file.' % filename
            fd = open(filename, 'w')
            fd.write(mako_page_code)
            fd.close()
        filename = os.path.join(rendercode_path, js_file)
        if not os.path.exists(filename):
            print '<---- * Creating "%s" file.' % filename
            fd = open(filename, 'w')
            fd.write(javascript_page_code)
            fd.close()
        filename = os.path.join(rendercode_path, scss_file)
        if not os.path.exists(filename):
            print '<---- * Creating "%s" file.' % filename
            fd = open(filename, 'w')
            fd.write(scss_page_code)
            fd.close()
        if not is_widget:
            ln_path = os.path.join(self.current_tag_dir(), 'static', 'js', 'bottom', 'app')
        else:
            if not widget_dir:
                ln_path = os.path.join(self.current_tag_dir(), 'static', 'js', 'bottom', 'widgets')
            else:
                ln_path = os.path.join(self.current_tag_dir(), 'static', 'js', 'bottom', widget_dir)
                if not os.path.exists(ln_path):
                    os.mkdir(ln_path)
                os.chdir(ln_path)
                if not is_widget:
                    source_file = '../../../../../../%s/htmlrendercode/%s' % (
                     project, js_file)
                else:
                    source_file = '../../../../../../%s/htmlrendercode/%s/%s/%s' % (
                     project,
                     'widgets' if not widget_dir else widget_dir,
                     name,
                     js_file)
                link_name = js_file
                try:
                    os.symlink(source_file, link_name)
                    print '<---- * Creating "%s" symbolic link.' % (ln_path + '/' + link_name)
                    msg = "Remember to add to bottom_js_content[] list (assets.py) the line:\n    'js/bottom/%s/%s.js'" % (
                     'app' if not is_widget else ('widgets' if not widget_dir else widget_dir),
                     name)
                    print msg
                except OSError:
                    pass

            if not is_widget:
                ln_path = os.path.join(self.current_tag_dir(), 'static', 'css', 'app')
            elif not widget_dir:
                ln_path = os.path.join(self.current_tag_dir(), 'static', 'css', 'widgets')
            else:
                ln_path = os.path.join(self.current_tag_dir(), 'static', 'css', widget_dir)
                if not os.path.exists(ln_path):
                    os.mkdir(ln_path)
            os.chdir(ln_path)
            if not is_widget:
                source_file = '../../../../../%s/htmlrendercode/%s' % (
                 project, scss_file)
            else:
                source_file = '../../../../../%s/htmlrendercode/%s/%s/%s' % (
                 project,
                 'widgets' if not widget_dir else widget_dir,
                 name,
                 scss_file)
            link_name = scss_file
            try:
                os.symlink(source_file, link_name)
                print '<---- * Creating "%s" symbolic link.' % (ln_path + '/' + link_name)
                msg = "Remember to add to scss_content[] list (assets.py) the line:\n    'css/%s/%s.scss'" % (
                 'app' if not is_widget else ('widgets' if not widget_dir else widget_dir),
                 name)
                print msg
            except OSError:
                pass

        return 0

    def render(self):
        """ generate a new index.html, in tags/{version} directory
        Blogdegins will render using next call code:

        get_base(here, output_path, debug)
            is the only function being called from blogdegins.
            The rest is up to you.
            This function must return a class with a `render` method.
            The `render` method must return a string with the html code.
            :param here: path where project blogdegins resides.
            :param output_path: current output tag directory.
            :param debug: True if you want debug.
        """
        project = os.path.basename(self.config.here).lower()
        if self.args.verbose:
            print '====> render ' + project
        output_path = self.current_tag_dir()
        if not os.path.exists(output_path):
            print '<---- * First you must create a tag skeleton.'
            exit(2)
        here = os.path.join(self.config.here)
        sys.path.append(here)
        os.chdir(self.config.here)
        package = __import__(project, globals(), locals(), [], -1)
        if not package:
            print "ERROR package '%s' NOT FOUND" % project
            return
        if not hasattr(package, 'htmlrendercode'):
            print "ERROR package '%s' has NOT htmlrendercode module" % project
            return
        try:
            base = package.htmlrendercode.base.get_base(here, output_path, self.args.debug)
        except AttributeError:
            raise

        html = base.render()
        if self.args.verbose:
            print html
        index_html = os.path.join(output_path, 'index.html')
        fd = open(index_html, 'w')
        fd.write(html)
        fd.close()
        return 0

    def rsync(self):
        """ syncronize the tag version with the remote host
        """
        print '====> rsync'
        src_path = os.path.join(self.current_tag_dir(), '')
        remote = self.config.get(self.config.current_tag, 'remote-server')
        if not remote:
            print '<---- * Please specify a remote server path.'
            exit(2)
        command = 'rsync -avzL --delete --exclude \\.webassets-cache --exclude \\.sass-cache --exclude \\.cache %s %s' % (
         src_path,
         remote)
        if self.args.verbose:
            print command
        response = envoy.run(command)
        print response.std_out
        return 0


if __name__ == '__main__':
    main()