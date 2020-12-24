# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/runner/runners/2.166.2/work/1/s/build/lib.macosx-10.9-x86_64-3.5/pycraf/_astropy_init.py
# Compiled at: 2020-04-16 04:29:51
# Size of source mod 2**32: 2023 bytes
__all__ = [
 '__version__', '__githash__']
try:
    _ASTROPY_SETUP_
except NameError:
    from sys import version_info
    if version_info[0] >= 3:
        import builtins
    else:
        import __builtin__ as builtins
    builtins._ASTROPY_SETUP_ = False

try:
    from .version import version as __version__
except ImportError:
    __version__ = ''

try:
    from .version import githash as __githash__
except ImportError:
    __githash__ = ''

if not _ASTROPY_SETUP_:
    import os
    from warnings import warn
    from astropy.config.configuration import update_default_config, ConfigurationDefaultMissingError, ConfigurationDefaultMissingWarning
    from astropy.tests.runner import TestRunner
    test = TestRunner.make_test_runner_in(os.path.dirname(__file__))
    test.__test__ = False
    __all__ += ['test']
    config_dir = None
    if not os.environ.get('ASTROPY_SKIP_CONFIG_UPDATE', False):
        config_dir = os.path.dirname(__file__)
        config_template = os.path.join(config_dir, __package__ + '.cfg')
        if os.path.isfile(config_template):
            try:
                update_default_config(__package__, config_dir, version=__version__)
            except TypeError as orig_error:
                try:
                    update_default_config(__package__, config_dir)
                except ConfigurationDefaultMissingError as e:
                    wmsg = e.args[0] + ' Cannot install default profile. If you are importing from source, this is expected.'
                    warn(ConfigurationDefaultMissingWarning(wmsg))
                    del e
                except Exception:
                    raise orig_error