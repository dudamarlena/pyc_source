# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/yuneta-dev/yuneta/^yuneta-v2/web-skeleton/web_skeleton/main.py
# Compiled at: 2015-12-31 07:41:37
"""
Utility for creating static html code.
"""
import argparse, sys, stat, os.path, shutil, datetime, envoy
try:
    from ConfigParser import ConfigParser
except:
    from configparser import ConfigParser

import logging
logging.basicConfig(level=logging.DEBUG)
from web_skeleton.getyesno import getyesno
from web_skeleton.getyesno import getstring
WEB_SKELETON_INI = 'web-skeleton.ini'
comandos = [
 'init', 'skeleton', 'render', 'gclass', 'rsync']

def yuno_js_code(yuno_name, yuno_role, root_name, root_gclass):
    code = ('/**************************************************************************\n *        - Create Yuno\n *        - Setup routes\n *        - Create the root gobj:\n **************************************************************************/\n(function(exports) {{\n    \'use strict\';\n\n    SMachine.set_machine_trace(true);   // global trace\n    if(false) {{ // Set the logger in a browser window\n        $(\'body\').append(\'<div id="logger"></div>\');\n\n        SMachine.logger = function(msg) {{ // Set new logger\n            $(\'#logger\').append(\'<div>\' + msg + \'</div>\');\n        }};\n    }}\n\n    console.log("CREATING {yuno_role} yuno");\n\n    var kw = {{\n        trace_creation: true,\n        trace_router: true\n    }};\n    var __yuno_gobj__ = new Yuno(\'\', \'{yuno_role}\', kw);\n    __yuno_gobj__.send_event(\n        __yuno_gobj__.router,\n        \'EV_ADD_STATIC_ROUTE\',\n        {{\n            name: \'\',\n            role: \'yuneta_agent\',\n            urls: [\n                \'ws://127.0.0.1:5995\'\n            ],\n        }}\n    );\n\n    $(function() {{\n        // Start at onload\n        console.log("======> Start RUNNING");\n        $(\'#loading-message\').remove();\n        __yuno_gobj__.root = __yuno_gobj__.gobj_create(\n           \'{root_name}\',\n           {root_gclass},\n           {{\n               parent_dom_id:\'body\'\n           }},\n           __yuno_gobj__\n        );\n    }});\n\n\n    /************************************************\n     *          Expose to the global object\n     ************************************************/\n    exports.__yuno_gobj__ = __yuno_gobj__;\n\n    if(typeof GLOBAL !== \'undefined\') {{\n        GLOBAL.__yuno_gobj__ = __yuno_gobj__;\n    }}\n}})(this);\n').format(yuno_name=yuno_name, yuno_role=yuno_role, root_name=root_name, root_gclass=root_gclass)
    return code


def get_gclass_code(name, page_dir=None):
    Name = name.capitalize()
    NAME = name.upper()
    code = ('/**************************************************************************\n *      {Name} GClass\n **************************************************************************/\n(function (exports) {{\n    \'use strict\';\n\n    /********************************************\n     *      Auxiliary\n     ********************************************/\n\n    /********************************************\n     *      Actions\n     ********************************************/\n    function ac_timeout(self, event, kw, src) {{\n        console.log("ac_timeout");\n        self.set_timeout(1*1000);\n        return 0;\n    }}\n\n    var {NAME}_FSM = {{\n        \'event_list\': [\n            \'EV_TIMEOUT\'\n        ],\n        \'state_list\': [\n            \'ST_IDLE\'\n        ],\n        \'machine\': {{\n            \'ST_IDLE\':\n            [\n                [\'EV_TIMEOUT\',              ac_timeout,             undefined]\n            ]\n        }}\n    }};\n\n    var {NAME}_CONFIG = {{\n        timeout_retry: 5,               // timeout retry, in seconds\n        timeout_idle: 5,                // idle timeout, in seconds\n        // Id of dom element parent. It has preference over parent gobj.\n        parent_dom_id: \'\'\n    }};\n\n    var {Name} = GObj.__makeSubclass__();\n    var proto = {Name}.prototype; // Easy access to the prototype\n    proto.__init__= function(name, kw) {{\n        this.name = name || \'\';  // set before super(), to put the same smachine name\n        this.gclass_name = \'{Name}\';\n        GObj.prototype.__init__.call(this, {NAME}_FSM, {NAME}_CONFIG);\n        __update_dict__(this.config, kw || {{}});\n        return this;\n    }};\n\n    /************************************************\n     *      Framework Method create\n     ************************************************/\n    proto.mt_create = function() {{\n        var self = this;\n        self.set_timeout(1*1000);\n    }}\n\n    /************************************************\n     *      Framework Method destroy\n     *      In this point, all childs\n     *      and subscriptions are already deleted.\n     ************************************************/\n    proto.mt_destroy= function() {{\n    }}\n\n\n    //=======================================================================\n    //      Expose the class via the global object\n    //=======================================================================\n    exports.{Name} = {Name};\n\n    if(typeof GLOBAL !== \'undefined\') {{\n        GLOBAL.{Name} = {Name};\n    }}\n\n}})(this);\n').format(Name=Name, NAME=NAME)
    return code


scss_page_code = '/*********************************************************\n *  Your scss code\n *********************************************************/\n'
setup_cfg_file = '[egg_info]\ntag_build =\ntag_svn_revision = false\ntag_date = 0\n\n[easy_install]\nzip_ok = false\n'
setup_py_file = '# -*- encoding: utf-8 -*-\n\nimport os\nimport sys\n\nfrom setuptools import setup, find_packages\n\nif sys.version_info[:2] < (2, 6):\n    raise RuntimeError(\'Requires Python 2.6 or better\')\n\nhere = os.path.abspath(os.path.dirname(__file__))\ntry:\n    README = open(os.path.join(here, \'README.rst\')).read()\n    CHANGES = open(os.path.join(here, \'CHANGES.txt\')).read()\nexcept IOError:\n    README = CHANGES = \'\'\n\nversion = \'0.0.0\'\n\nrequires = [\'web_skeleton\']\n\nsetup(name=\'{package}\',\n    version=version,\n    description=\'{package}\',\n    long_description=\'\',\n    classifiers=[\n        "Programming Language :: Python",\n    ],\n    author=\'\',\n    author_email=\'\',\n    url=\'\',\n    license=\'\',\n    keywords=\'web-skeleton yuneta\',\n    packages=find_packages(),\n    include_package_data=True,\n    zip_safe=False,\n    install_requires=requires,\n    tests_require=requires,\n    test_suite="{package}.tests",\n    entry_points=\'\'\'    \'\'\',\n)\n'
watch_file_sh = '#!/bin/sh\nmake\nwatchfs -f watch.json\n'
watch_json_file = '{\n    "global":{\n        "Fs.info": false,\n        "Watchfs.kw": {\n            "info": false,\n            "command":""rm -rf tags/0.00.aa/static/.sass-cache/ tags/0.00.aa/static/.webassets-cache/ tags/0.00.aa/.cache/; make"",\n            "path":".",\n            "recursive":true,\n            "patterns":".*\\\\.py;.*\\\\.mako;.*\\\\.js;.*\\\\.css;.*\\\\.scss;.*\\\\.rst;.*\\\\.json;",\n            "ignore_renamed_event":true\n        }\n    }\n}\n'
makefile_file = 'default: build\n\nbuild:\n\tweb-skeleton -vd render\n'
hgignore_file = 'syntax:regexp\n\n.directory\nbuild/\ndist/\ndata/\n_build/\n^\\.tox/\n\\.svn/\n^\\.komodotools/\n^\\.settings/\n\\.cache/\n\\.egg-info/\n\\.webassets-cache/\n\\.sass-cache/\n\\.webassets-manifest\n\n\\.komodoproject$\n\\.coverage$\n\\.pyc$\n\\.so$\n\\.scss\\.css$\n\\.egg$\n^\\.project$\n^\\.pydevproject$\n\n\\.tar\\.gz$\n'

def main(argv=sys.argv):
    command = WebSkeleton(argv)
    return command.run()


class WebSkeleton(object):
    description = 'Generate static html code.'
    parser = argparse.ArgumentParser(description=description, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('command', choices=comandos, help='Available commands (WARNING: to be executed in the web-skeleton.ini directory):\ninit {project} ==> create a .ini file and the directory structure.\nskeleton ==> create a new tag directory, copying a assets directory.\nrender ==> generate a new index.html, in tags/{version} directory.\ngclass {name} [sub-directory] ==> creat a new gclass (js/scss files) in main or path directory.\nrsync ==> syncronize the tag version with the remote host.\n')
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
        if not self.args.arguments:
            print '\nERROR: you must supply a project name!\n'
            return 2
        project = self.args.arguments[0].lower()
        output_dir = os.path.abspath(os.path.normpath(project))
        if os.path.exists(output_dir):
            print '\nERROR: directory "%s" already exists!\n' % output_dir
            return 2
        os.mkdir(output_dir)
        src_path = self.assets_dir()
        dst_path = os.path.join(output_dir, 'assets')
        shutil.copytree(src_path, dst_path, symlinks=True)
        src_path = self.code_dir()
        dst_path = os.path.join(output_dir, project, 'htmlrendercode')
        shutil.copytree(src_path, dst_path, ignore=shutil.ignore_patterns('*.pyc', '*~'), symlinks=True)
        init_py = os.path.join(output_dir, project, '__init__.py')
        with open(init_py, 'w') as (f):
            f.write('import htmlrendercode  # needed to dynamic import from web_skeleton')
        setup_cfg = os.path.join(output_dir, 'setup.cfg')
        with open(setup_cfg, 'w') as (f):
            f.write(setup_cfg_file)
        setup_py = os.path.join(output_dir, 'setup.py')
        with open(setup_py, 'w') as (f):
            f.write(setup_py_file.format(package=project))
        watch = os.path.join(output_dir, 'watch.sh')
        with open(watch, 'w') as (f):
            f.write(watch_file_sh)
        st = os.stat(watch)
        os.chmod(watch, st.st_mode | stat.S_IEXEC)
        watch = os.path.join(output_dir, 'watch.json')
        with open(watch, 'w') as (f):
            f.write(watch_json_file)
        makefile = os.path.join(output_dir, 'Makefile')
        with open(makefile, 'w') as (f):
            f.write(makefile_file)
        hgignore = os.path.join(output_dir, '.hgignore')
        with open(hgignore, 'w') as (f):
            f.write(hgignore_file)
        os.mkdir(os.path.join(output_dir, 'tags'))
        current_tag = '0.00.aa'
        config = ConfigParser()
        config.set('DEFAULT', 'current_tag', current_tag)
        config.add_section('tags')
        config.set('tags', current_tag, '')
        config.add_section(current_tag)
        config.set(current_tag, 'assets', os.path.join('assets', 'h5bp'))
        config.set(current_tag, 'remote-server', '')
        ini_file = os.path.join(output_dir, WEB_SKELETON_INI)
        with open(ini_file, 'w') as (configfile):
            config.write(configfile)
        print '\nOK: created new web-skeleton project in "%s".\n' % output_dir
        print 'Next steps:'
        print '   - Go to %s directory (cd %s)' % (project, project)
        print '   - Change definitions in base.py (page_data)'
        print '   - Check your settings in web-skeleton.ini file'
        print '   - Build a new h5bp structure (web-skeleton skeleton)'
        print ''
        return 0

    def load_ini(self):
        if not os.path.exists(WEB_SKELETON_INI):
            print '\nERROR: file "%s" NOT found.\n' % WEB_SKELETON_INI
            exit(2)
        here = os.path.dirname(os.path.abspath(WEB_SKELETON_INI))
        self.config = ConfigParser({'here': here})
        self.config.read(WEB_SKELETON_INI)
        self.config.here = here
        self.config.yuno_name = ''
        self.config.yuno_role = ''
        self.config.root_name = ''
        self.config.root_gclass = ''
        self.config.current_tag = self.config.get('DEFAULT', 'current_tag')

    def module_dir(self):
        mod = sys.modules[self.__class__.__module__]
        return os.path.dirname(mod.__file__)

    def assets_dir(self):
        return os.path.join(self.module_dir(), 'assets')

    def code_dir(self):
        return os.path.join(self.module_dir(), '_htmlrendercode')

    def current_tag_dir(self):
        return os.path.join(self.config.here, 'tags', self.config.current_tag)

    def skeleton(self):
        """ create a new tag directory, copying a assets directory
        """
        dst_path = self.current_tag_dir()
        if not os.path.exists(dst_path):
            pass
        else:
            resp = getyesno('WARNING: You are re-creating the skeleton "%s".\nYou will loose your data! Are you sure?' % dst_path, default='n')
            if not resp:
                print '\nOperation aborted.\n'
                return 2
            shutil.rmtree(dst_path)
        self.config.yuno_role = ''
        while not self.config.yuno_role:
            self.config.yuno_role = getstring('Enter yuno role (maximum 15 characters):', '')

        self.config.yuno_name = getstring("Enter yuno name ['']:", '')
        self.config.root_name = getstring("Enter root gobj name ['root']:", 'root')
        self.config.root_gclass = self.config.root_name.capitalize()
        self.config.author = getstring("Enter author ['']:", '')
        self.config.license = getstring("Enter license ['MIT']:", 'MIT')
        self.config.version = getstring("Enter version ['1.0.0']:", '1.0.0')
        assets = self.config.get(self.config.current_tag, 'assets')
        src_path = os.path.join(self.config.here, assets)
        shutil.copytree(src_path, dst_path, symlinks=True)
        self.gclass('base', None, yuno_js_code(self.config.yuno_name, self.config.yuno_role, self.config.root_name, self.config.root_gclass))
        print '\nOK: Created "%s" tag.\n' % dst_path
        print 'Next steps:'
        print '   - Create your root gclass (web-skeleton gclass {name} [sub-directory]'
        print '   - Update the assets.py file with new js file'
        print '   - Render (web-skeleton render)'
        print ''
        return 0

    def gclass(self, name=None, page_dir=None, gclass_code=None):
        """ creat a new gclass, set of js/scss files
        """
        if not name:
            if not self.args.arguments:
                print 'WARNING: You must supply a name!'
                return 2
            name = self.args.arguments[0].lower()
            if len(self.args.arguments) >= 2:
                page_dir = self.args.arguments[1]
        if not gclass_code:
            gclass_code = get_gclass_code(name)
        self._make_set(name, gclass_code, scss_page_code, page_dir)

    def _make_set(self, name, gclass_code, scss_page_code, page_dir=None):
        project = os.path.basename(self.config.here).lower()
        if page_dir:
            rendercode_path = os.path.join(self.config.here, project, 'htmlrendercode', page_dir)
        else:
            rendercode_path = os.path.join(self.config.here, project, 'htmlrendercode')
        if not os.path.exists(self.current_tag_dir()):
            print '\nWARNING: firstly you must create a tag skeleton.\n'
            exit(2)
        if not os.path.exists(rendercode_path):
            os.mkdir(rendercode_path)
        js_file = '%s.js' % name
        scss_file = '%s.scss' % name
        filename = os.path.join(rendercode_path, js_file)
        if not os.path.exists(filename):
            print 'Creating "%s" file...' % filename
            Name = name.capitalize()
            fd = open(filename, 'w')
            fd.write(gclass_code)
            fd.close()
        filename = os.path.join(rendercode_path, scss_file)
        if not os.path.exists(filename):
            print 'Creating "%s" file...' % filename
            fd = open(filename, 'w')
            fd.write(scss_page_code)
            fd.close()
        if not page_dir:
            ln_path = os.path.join(self.current_tag_dir(), 'static', 'css', 'app')
        else:
            ln_path = os.path.join(self.current_tag_dir(), 'static', 'css', page_dir)
        if not os.path.exists(ln_path):
            os.mkdir(ln_path)
        os.chdir(ln_path)
        if not page_dir:
            source_file = '../../../../../%s/htmlrendercode/%s' % (
             project, scss_file)
        else:
            source_file = '../../../../../%s/htmlrendercode/%s/%s' % (
             project,
             page_dir,
             scss_file)
        link_name = scss_file
        try:
            os.symlink(source_file, link_name)
            print 'Creating "%s" symbolic link...' % (ln_path + '/' + link_name)
            msg = "Remember to add to scss_content[] list (assets.py) the line:\n    'css/%s/%s.scss'\n" % (
             'app' if not page_dir else page_dir,
             name)
            print msg
        except OSError:
            pass

        if not page_dir:
            ln_path = os.path.join(self.current_tag_dir(), 'static', 'js', 'bottom', 'app')
        else:
            ln_path = os.path.join(self.current_tag_dir(), 'static', 'js', 'bottom', page_dir)
        if not os.path.exists(ln_path):
            os.mkdir(ln_path)
        os.chdir(ln_path)
        if not page_dir:
            source_file = '../../../../../../%s/htmlrendercode/%s' % (
             project, js_file)
        else:
            source_file = '../../../../../../%s/htmlrendercode/%s/%s' % (
             project,
             page_dir,
             js_file)
        link_name = js_file
        try:
            os.symlink(source_file, link_name)
            print 'Creating "%s" symbolic link...' % (ln_path + '/' + link_name)
            msg = "Remember to add to bottom_js_content[] list (assets.py) the line:\n    'js/bottom/%s/%s.js'\n" % (
             'app' if not page_dir else page_dir,
             name)
            print msg
        except OSError:
            pass

        return 0

    def render(self):
        """ generate a new index.html, in tags/{version} directory
        WebSkeleton will render using next call code:

        get_base(here, output_path, debug)
            is the only function being called from web_skeleton.
            The rest is up to you.
            This function must return a class with a `render` method.
            The `render` method must return a string with the html code.
            :param here: path where project web-skeleton resides.
            :param output_path: current output tag directory.
            :param debug: True if you want debug.
        """
        project = os.path.basename(self.config.here).lower()
        if self.args.verbose:
            print 'Rendering ' + project + '...'
        output_path = self.current_tag_dir()
        if not os.path.exists(output_path):
            print '\nWARNING: firstly you must create a tag skeleton.\n'
            exit(2)
        here = os.path.join(self.config.here)
        sys.path.append(here)
        os.chdir(self.config.here)
        package = __import__(project, globals(), locals(), [], -1)
        if not package:
            print "ERROR: package '%s' NOT FOUND" % project
            return
        if not hasattr(package, 'htmlrendercode'):
            print "ERROR: package '%s' has NOT htmlrendercode module" % project
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
        print '\nOK: Created "%s" file.\n' % (index_html,)
        return 0

    def rsync(self):
        """ syncronize the tag version with the remote host
        """
        src_path = os.path.join(self.current_tag_dir(), '')
        remote = self.config.get(self.config.current_tag, 'remote-server')
        if not remote:
            print '\nWARNING: Please specify a remote server path.\n'
            exit(2)
        print 'rsyncing...'
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