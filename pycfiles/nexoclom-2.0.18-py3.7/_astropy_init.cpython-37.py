# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mburger/Work/Research/NeutralCloudModel/nexoclom/build/lib/nexoclom/_astropy_init.py
# Compiled at: 2018-10-25 15:03:17
# Size of source mod 2**32: 1997 bytes
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
    __all__ += ['test']
    config_dir = None
    config_dir = os.environ.get('ASTROPY_SKIP_CONFIG_UPDATE', False) or os.path.dirname(__file__)
    config_template = os.path.join(config_dir, __package__ + '.cfg')
    if os.path.isfile(config_template):
        try:
            update_default_config(__package__,
              config_dir, version=__version__)
        except TypeError as orig_error:
            try:
                try:
                    update_default_config(__package__, config_dir)
                except ConfigurationDefaultMissingError as e:
                    try:
                        wmsg = e.args[0] + ' Cannot install default profile. If you are importing from source, this is expected.'
                        warn(ConfigurationDefaultMissingWarning(wmsg))
                        del e
                    finally:
                        e = None
                        del e

                except Exception:
                    raise orig_error

            finally:
                orig_error = None
                del orig_error