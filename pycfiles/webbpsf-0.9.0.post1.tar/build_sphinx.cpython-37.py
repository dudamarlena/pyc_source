# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rgeda/project/repo/webbpsf/astropy_helpers/astropy_helpers/commands/build_sphinx.py
# Compiled at: 2019-07-20 17:47:20
# Size of source mod 2**32: 10319 bytes
from __future__ import print_function
import inspect, os, pkgutil, re, shutil, subprocess, sys, textwrap, warnings
from distutils import log
from distutils.cmd import DistutilsOptionError
import sphinx
import sphinx.setup_command as SphinxBuildDoc
from ..utils import minversion, AstropyDeprecationWarning

class AstropyBuildDocs(SphinxBuildDoc):
    __doc__ = "\n    A version of the ``build_docs`` command that uses the version of Astropy\n    that is built by the setup ``build`` command, rather than whatever is\n    installed on the system.  To build docs against the installed version, run\n    ``make html`` in the ``astropy/docs`` directory.\n\n    This also automatically creates the docs/_static directories--this is\n    needed because GitHub won't create the _static dir because it has no\n    tracked files.\n    "
    description = 'Build Sphinx documentation for Astropy environment'
    user_options = SphinxBuildDoc.user_options[:]
    user_options.append(('warnings-returncode', 'w', 'Parses the sphinx output and sets the return code to 1 if there are any warnings. Note that this will cause the sphinx log to only update when it completes, rather than continuously as is normally the case.'))
    user_options.append(('clean-docs', 'l', 'Completely clean previous builds, including automodapi-generated files before building new ones'))
    user_options.append(('no-intersphinx', 'n', 'Skip intersphinx, even if conf.py says to use it'))
    user_options.append(('open-docs-in-browser', 'o', 'Open the docs in a browser (using the webbrowser module) if the build finishes successfully.'))
    boolean_options = SphinxBuildDoc.boolean_options[:]
    boolean_options.append('warnings-returncode')
    boolean_options.append('clean-docs')
    boolean_options.append('no-intersphinx')
    boolean_options.append('open-docs-in-browser')
    _self_iden_rex = re.compile('self\\.([^\\d\\W][\\w]+)', re.UNICODE)

    def initialize_options(self):
        SphinxBuildDoc.initialize_options(self)
        self.clean_docs = False
        self.no_intersphinx = False
        self.open_docs_in_browser = False
        self.warnings_returncode = False

    def finalize_options(self):
        SphinxBuildDoc.finalize_options(self)
        if self.clean_docs:
            dirstorm = [
             os.path.join(self.source_dir, 'api'),
             os.path.join(self.source_dir, 'generated')]
            if self.build_dir is None:
                dirstorm.append('docs/_build')
            else:
                dirstorm.append(self.build_dir)
            for d in dirstorm:
                if os.path.isdir(d):
                    log.info('Cleaning directory ' + d)
                    shutil.rmtree(d)
                else:
                    log.info('Not cleaning directory ' + d + ' because not present or not a directory')

    def run(self):
        import webbrowser
        from urllib.request import pathname2url
        retcode = None
        if self.build_dir is not None:
            basedir, subdir = os.path.split(self.build_dir)
            if subdir == '':
                basedir, subdir = os.path.split(basedir)
            staticdir = os.path.join(basedir, '_static')
            if os.path.isfile(staticdir):
                raise DistutilsOptionError('Attempted to build_docs in a location where' + staticdir + 'is a file.  Must be a directory.')
            self.mkpath(staticdir)
        build_cmd = self.reinitialize_command('build')
        build_cmd.inplace = 0
        self.run_command('build')
        build_cmd = self.get_finalized_command('build')
        build_cmd_path = os.path.abspath(build_cmd.build_lib)
        ah_importer = pkgutil.get_importer('astropy_helpers')
        ah_path = os.path.abspath(ah_importer.path)
        runlines, runlineno = inspect.getsourcelines(SphinxBuildDoc.run)
        subproccode = textwrap.dedent('\n            from sphinx.setup_command import *\n\n            os.chdir({srcdir!r})\n            sys.path.insert(0, {build_cmd_path!r})\n            sys.path.insert(0, {ah_path!r})\n\n        ').format(build_cmd_path=build_cmd_path, ah_path=ah_path, srcdir=(self.source_dir))
        subproccode += textwrap.dedent(''.join(runlines[1:]))
        subproccode = self._self_iden_rex.split(subproccode)
        for i in range(1, len(subproccode), 2):
            iden = subproccode[i]
            val = getattr(self, iden)
            if iden.endswith('_dir'):
                subproccode[i] = repr(os.path.abspath(val))
            else:
                subproccode[i] = repr(val)

        subproccode = ''.join(subproccode)
        optcode = textwrap.dedent('\n\n        class Namespace(object): pass\n        self = Namespace()\n        self.pdb = {pdb!r}\n        self.verbosity = {verbosity!r}\n        self.traceback = {traceback!r}\n\n        ').format(pdb=(getattr(self, 'pdb', False)), verbosity=(getattr(self, 'verbosity', 0)),
          traceback=(getattr(self, 'traceback', False)))
        subproccode = optcode + subproccode
        if minversion(sphinx, '1.3'):
            subproccode = 'from __future__ import print_function' + subproccode
        if self.no_intersphinx:
            subproccode = subproccode.replace('confoverrides = {}', "confoverrides = {'intersphinx_mapping':{}}")
        else:
            log.debug('Starting subprocess of {0} with python code:\n{1}\n[CODE END])'.format(sys.executable, subproccode))
            if self.warnings_returncode:
                proc = subprocess.Popen([sys.executable, '-c', subproccode], stdin=(subprocess.PIPE),
                  stdout=(subprocess.PIPE),
                  stderr=(subprocess.STDOUT))
                retcode = 1
                with proc.stdout:
                    for line in iter(proc.stdout.readline, b''):
                        line = line.strip(b'\r\n')
                        print(line.decode('utf-8'))
                        if 'build succeeded.' == line.decode('utf-8'):
                            retcode = 0

                proc.wait()
                if retcode != 0:
                    if os.environ.get('TRAVIS', None) == 'true':
                        msg = 'The build_docs travis build FAILED because sphinx issued documentation warnings (scroll up to see the warnings).'
                    else:
                        msg = 'build_docs returning a non-zero exit code because sphinx issued documentation warnings.'
                    log.warn(msg)
                else:
                    proc = subprocess.Popen([sys.executable], stdin=(subprocess.PIPE))
                    proc.communicate(subproccode.encode('utf-8'))
                if proc.returncode == 0:
                    if self.open_docs_in_browser:
                        if self.builder == 'html':
                            absdir = os.path.abspath(self.builder_target_dir)
                            index_path = os.path.join(absdir, 'index.html')
                            fileurl = 'file://' + pathname2url(index_path)
                            webbrowser.open(fileurl)
                        else:
                            log.warn('open-docs-in-browser option was given, but the builder is not html! Ignoring.')
            else:
                log.warn('Sphinx Documentation subprocess failed with return code ' + str(proc.returncode))
                retcode = proc.returncode
        if retcode is not None:
            sys.exit(retcode)


class AstropyBuildSphinx(AstropyBuildDocs):
    description = 'deprecated alias to the build_docs command'

    def run(self):
        warnings.warn('The "build_sphinx" command is now deprecated. Use"build_docs" instead.', AstropyDeprecationWarning)
        AstropyBuildDocs.run(self)