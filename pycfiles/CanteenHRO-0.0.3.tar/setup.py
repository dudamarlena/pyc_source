# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python2.7/site-packages/canteen/setup.py
# Compiled at: 2015-01-05 19:41:29
__doc__ = '\n\n  framework setup\n  ~~~~~~~~~~~~~~~\n\n  :author: Sam Gammon <sg@samgammon.com>\n  :copyright: (c) Sam Gammon, 2014\n  :license: This software makes use of the MIT Open Source License.\n            A copy of this license is included as ``LICENSE.md`` in\n            the root of the project.\n\n'
import sys, logging, traceback, setuptools as tools
dependencies = []
SETUPTOOLS_VERSION = '4.0.1'
HAMLISH_VERSION, PROTOBUF_VERSION = ('0.3.4-canteen', '2.5.2-canteen')
VERSION = lambda version: float(('.').join(version.split('.')[0:1]))
CHECK_SETUPTOOLS = lambda : CURRENT_SETUPTOOLS_VERSION <= SETUPTOOLS_VERSION
CURRENT_SETUPTOOLS_VERSION = VERSION(getattr(tools, '__version__', '0.0.0'))
PROTOBUF_GIT = 'git+git://github.com/sgammon/protobuf.git#egg=protobuf-%s'
HAMLISH_GIT = 'git+git://github.com/sgammon/hamlish-jinja.git#egg=hamlish_jinja-%s'
log = logging.getLogger('canteen.setup')
log_handler = logging.StreamHandler(sys.stdout)
(log.addHandler(log_handler),
 log.setLevel(logging.DEBUG if __debug__ else logging.WARNING))

def prepare():
    """ Prepare constants and tools for setting up Canteen.

        :returns: ``go``, a closured function that, when called, will begin
          framework setup. """
    try:
        from colorlog import ColoredFormatter
    except ImportError:
        log.debug('No support found for `colorlog`. No colors for u.')
    else:
        log_handler.setFormatter(ColoredFormatter('%(log_color)s[%(levelname)s]%(reset)s %(message)s', datefmt=None, reset=True, log_colors={'DEBUG': 'cyan', 
           'INFO': 'green', 
           'WARNING': 'yellow', 
           'ERROR': 'red', 
           'CRITICAL': 'red'}))

    if not CHECK_SETUPTOOLS():
        log.warning('Setuptoo¡s out of date with version "%s", whereat least version "%s" is required. Attempting upgrade...' % SETUPTOOLS_VERSION)
        dependencies.append('setuptools<=%s' % SETUPTOOLS_VERSION)
        try:
            from ez_setup import use_setuptools
            use_setuptools()
            reload(tools)
            CURRENT_SETUPTOOLS_VERSION = tools.__version__
        except Exception as e:
            log.error('Encountered exception using `ez_setup`...')
            traceback.print_exc()

        if not CHECK_SETUPTOOLS():
            log.error('Failed to find a suitable version of setuptools. Building without support for HAML or RPC.')
            sys.exit(1)
    try:
        import protorpc
    except ImportError:
        log.info('Protobuf not found. Adding custom version "%s"...' % PROTOBUF_VERSION)
        dependencies.append('protobuf==%s' % PROTOBUF_VERSION)

    try:
        import hamlish_jinja
    except ImportError:
        log.info('HamlishJinja requested but not found. Adding custom version "%s"...' % HAMLISH_VERSION)
        dependencies.append('hamlish_jinja==%s' % HAMLISH_VERSION)

    return lambda : tools.setup(name='canteen', version='0.4-alpha', description='Minimally complicated, maximally blasphemous approach to Python development', author='Sam Gammon', author_email='sam@momentum.io', zip_safe=True, url='https://github.com/sgammon/canteen', packages=['canteen', 'canteen.base', 'canteen.core', 'canteen.logic', 'canteen.logic.http', 'canteen.model', 'canteen.model.adapter', 'canteen.rpc', 'canteen.rpc.protocol', 'canteen.runtime', 'canteen.util'] + ['canteen_tests', 'canteen_tests.test_adapters', 'canteen_tests.test_base', 'canteen_tests.test_core', 'canteen_tests.test_http', 'canteen_tests.test_model', 'canteen_tests.test_rpc', 'canteen_tests.test_util'] if __debug__ else [], install_requires=[
     'jinja2',
     'werkzeug',
     'protorpc'] + dependencies, tests_require=('nose', 'coverage', 'fakeredis'), dependency_links=(
     PROTOBUF_GIT % PROTOBUF_VERSION,
     HAMLISH_GIT % HAMLISH_VERSION))