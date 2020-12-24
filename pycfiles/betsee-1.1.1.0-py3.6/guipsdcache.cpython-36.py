# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/betsee/lib/pyside2/cache/guipsdcache.py
# Compiled at: 2019-08-01 01:03:55
# Size of source mod 2**32: 17508 bytes
"""
High-level caching functionality for this application's graphical user
interface (GUI), persisting external resources required by this GUI to
user-specific files on the local filesystem.
"""
import PySide2
from betse.util.app.meta import appmetaone
from betse.util.io.log import logs
from betse.util.path import files, paths, pathnames
from betse.util.path.command import cmdpath
from betse.util.py import pys
from betse.util.py.module import pymodule
from betse.util.type.enums import make_enum
from betse.util.type.types import type_check, IterableTypes
from betsee.guiexception import BetseeCacheException
from betsee.gui.simconf.stack.widget.guisimconfradiobtn import QBetseeSimConfEnumRadioButtonGroup
CachePolicy = make_enum(class_name='CachePolicy',
  member_names=('AUTO', 'DEV', 'USER'),
  doc="\n    Enumeration of all supported types of **cache policy** (i.e., procedure for\n    generating and reusing pure-Python submodules from their input\n    XML-formatted files at application runtime).\n\n    Attributes\n    ----------\n    AUTO : enum\n        **Automatic cache policy.** When enabled, this policy defers to either\n        the :attr:`DEV` or :attr:`USER` cache policies conditionally depending\n        on whether this application is currently under developer-specific\n        version control or not. Specifically:\n\n        * If this application has a **Git-based working tree** (i.e., top-level\n          directory containing this application's ``.git`` subdirectory and\n          ``setup.py`` install script), this application is assumed to have\n          been installed for developer usage. In this case, the :attr:`DEV`\n          cache policy is deferred to.\n        * Else, this application is assumed to have been installed for end user\n          usage. In this case, the :attr:`USER` cache policy is deferred to.\n    DEV : enum\n        **Developer cache policy.** When enabled, application-wide submodules\n        (e.g., :meth:`betsee.guiappmeta.BetseeAppMeta.data_py_qrc_filename`)\n        are generated and copied over all equivalent user-specific submodules\n        (e.g., :meth:`betsee.guiappmeta.BetseeAppMeta.dot_py_qrc_filename`),\n        guaranteeing the latter to *always* exist. Exceptions raised while\n        doing so are treated as fatal.\n    USER : enum\n        **End user cache policy.** When enabled, only user-specific submodules\n        are generated. Application-wide submodules are commonly installed into\n        system directories unwritable by end users (e.g.,\n        ``/usr/lib64/python3.6/site-packages/betsee/data/py``). Ergo, this\n        policy *never* attempts to regenerate these submodules. If an exception\n        is raised when regenerating a user-specific submodule:\n\n        * This exception is treated as non-fatal and hence merely logged rather\n          than prematurely halting the active Python process.\n        * The corresponding application-wide submodule is copied over that\n          user-specific submodule, guaranteeing the latter to *always* exist.\n    ")
_PROMOTE_OBJ_NAME_TO_CLASS = {'sim_conf_space_intra_lattice_type': QBetseeSimConfEnumRadioButtonGroup}

@type_check
def init(cache_policy: CachePolicy) -> None:
    """
    Initialize this submodule and hence the on-disk cache of :mod:`PySide2`
    submodules required by this application at runtime.

    Specifically, this function either creates and caches *or* reuses each
    pure-Python :mod:`PySide2`-based submodule converted from a source
    XML-formatted file and zero or more binary resources exported by the
    external Qt (Creator|Designer) GUI. For efficiency, previously cached
    submodules are regenerated *only* as needed (i.e., if older than the
    underlying paths from which these submodules are generated).

    Parameters
    ----------
    cache_policy : CachePolicy
        Type of :mod:`PySide2`-based submodule caching to be performed.
    """
    app_meta = appmetaone.get_app_meta()
    if cache_policy is CachePolicy.AUTO:
        if app_meta.is_git_worktree:
            _init_dev()
        else:
            _init_user()
    else:
        if cache_policy is CachePolicy.DEV:
            _init_dev()
        else:
            if cache_policy is CachePolicy.USER:
                _init_user()
            else:
                raise BetseeCacheException('Cache policy {!r} unrecognized.'.format(cache_policy))
    pys.add_import_dirname(app_meta.dot_py_dirname)


def _init_dev() -> None:
    """
    Either create and cache *or* reuse each previously cached pure-Python
    submodule required at runtime by this GUI, including both application-wide
    submodules bundled in this application's package *and* user-specific
    submodules residing in a dot directory under this user's home directory.

    Caveats
    ----------
    **This function should only be called if this application has a Git-based
    working tree,** in which case this application is assumed to be under
    development by a non-end user developer.
    """
    logs.log_info('Synchronizing cached PySide2 submodules for development...')
    app_meta = appmetaone.get_app_meta()
    _cache_py_qrc_file(qrc_filename=(app_meta.data_qrc_filename),
      py_filename=(app_meta.data_py_qrc_filename))
    _cache_py_ui_file(ui_filename=(app_meta.data_ui_filename),
      py_filename=(app_meta.data_py_ui_filename))
    files.copy_overwritable(src_filename=(app_meta.data_py_qrc_filename),
      trg_filename=(app_meta.dot_py_qrc_filename))
    files.copy_overwritable(src_filename=(app_meta.data_py_ui_filename),
      trg_filename=(app_meta.dot_py_ui_filename))


def _init_user() -> None:
    """
    Either create and cache *or* reuse each previously cached pure-Python
    submodule required at runtime by this GUI, including only user-specific
    submodules residing in a dot directory under this user's home directory but
    *not* application-wide submodules bundled in this application's package.

    Caveats
    ----------
    For safety, this function only logs non-fatal warnings rather than raising
    exceptions. This function only creates optional user-specific submodules
    rather than mandatory application-wide submodules. While lamentable, any
    issues in this function (e.g., an inability to write user-specific
    submodules due to petty ownership or permission conflicts) should be
    confined to this function rather than halting the entire application.
    """
    logs.log_info('Synchronizing cached PySide2 submodules...')
    app_meta = appmetaone.get_app_meta()
    try:
        _cache_py_qrc_file(qrc_filename=(app_meta.data_qrc_filename),
          py_filename=(app_meta.dot_py_qrc_filename))
    except Exception as exception:
        logs.log_exception(exception)
        logs.log_warning('Synchronization failed due to uncaught exception!')
        files.copy_overwritable(src_filename=(app_meta.data_py_qrc_filename),
          trg_filename=(app_meta.dot_py_qrc_filename))

    try:
        _cache_py_ui_file(ui_filename=(app_meta.data_ui_filename),
          py_filename=(app_meta.dot_py_ui_filename))
    except Exception as exception:
        logs.log_exception(exception)
        logs.log_warning('Synchronization failed due to uncaught exception!')
        files.copy_overwritable(src_filename=(app_meta.data_py_ui_filename),
          trg_filename=(app_meta.dot_py_ui_filename))


@type_check
def _cache_py_qrc_file(qrc_filename: str, py_filename: str) -> None:
    """
    Reuse the previously cached pure-Python :mod:`PySide2`-based submodule
    embedding all binary resources in this application's main Qt resource
    collection (QRC) with the passed filename if that submodule is sufficiently
    up-to-date (i.e., at least as new as all input paths required to regenerate
    that submodule) *or* regenerate this submodule from these input paths
    otherwise, principally including the input QRC file with the passed
    filename.

    Parameters
    ----------
    qrc_filename : str
        Absolute or relative filename of the input ``.qrc``-suffixed file.
    py_filename : str
        Absolute or relative filename of the output ``.py``-suffixed file.

    Raises
    ----------
    BetseCommandException
        If the ``pyside2-rcc`` command installed by the optional third-party
        dependency ``pyside2-tools`` is *not* in the current ``${PATH}``.

    See Also
    ----------
    :func:`guipsdcacheqrc.convert_qrc_to_py_file`
        Further details.
    """
    from betsee.lib.pyside2.cache import guipsdcacheqrc
    src_pathnames = [
     qrc_filename,
     pymodule.get_filename(guipsdcacheqrc),
     cmdpath.get_filename('pyside2-rcc')]
    if not _is_trg_file_stale(src_pathnames=src_pathnames,
      trg_filename=py_filename):
        return
    guipsdcacheqrc.convert_qrc_to_py_file(qrc_filename=qrc_filename,
      py_filename=py_filename)


@type_check
def _cache_py_ui_file(ui_filename: str, py_filename: str) -> None:
    """
    Reuse the previously cached pure-Python :mod:`PySide2`-based submodule
    implementing the superficial construction of this application's main window
    if that submodule is sufficiently up-to-date (i.e., at least as new as all
    input paths required to regenerate that submodule) *or* regenerate that
    submodule from these input paths otherwise, principally including the input
    UI file with the passed filename.

    Parameters
    ----------
    ui_filename : str
        Absolute or relative filename of the input ``.ui``-suffixed file.
    py_filename : str
        Absolute or relative filename of the output ``.py``-suffixed file.

    Raises
    ----------
    ImportError
        If the :mod:`pyside2uic` package installed by the optional third-party
        dependency ``pyside2-tools`` is *not* importable.

    See Also
    ----------
    :func:`guipsdcacheui.convert_ui_to_py_file`
        Further details.
    """
    from betse.lib import libs
    from betsee.lib.pyside2.cache import guipsdcacheui
    pyside2uic = libs.import_runtime_optional('pyside2uic')
    src_pathnames = [
     ui_filename,
     pymodule.get_filename(guipsdcacheui),
     pymodule.get_dirname(PySide2),
     pymodule.get_dirname(pyside2uic)]
    if not _is_trg_file_stale(src_pathnames=src_pathnames,
      trg_filename=py_filename):
        return
    guipsdcacheui.convert_ui_to_py_file(ui_filename=ui_filename,
      py_filename=py_filename,
      promote_obj_name_to_class=_PROMOTE_OBJ_NAME_TO_CLASS)


@type_check
def _is_trg_file_stale(src_pathnames: IterableTypes, trg_filename: str) -> bool:
    """
    ``True`` only if the passed target file either does not exist, does exist
    but is a directory, does exist but is **empty** (i.e., zero-byte), *or*
    does exist but is older than all source paths in the passed iterable.

    If this function returns ``True``, the caller is expected to explicitly
    (re)create this target file from these source paths.

    Parameters
    ----------
    src_pathnames: IterableTypes[str]
        Iterable of the absolute or relative pathnames of all source paths
        required to (re)create this target file. For efficiency, these paths
        should be ordered according to the heuristic discussed by the
        :func:`paths.is_mtime_recursive_older_than_paths` function.
    trg_filename : str
        Absolute or relative filename of the target file.

    Returns
    ----------
    bool
        ``True`` only if this target file either:

        * Does *not* exist.
        * Does exist but is a directory.
        * Does exist but is an **empty file** (i.e., zero-byte).
        * Does exist but is older than all such source paths.
    """
    logs.log_info('Synchronizing cached PySide2 submodule "%s"...', pathnames.get_basename(trg_filename))
    return not files.is_file(trg_filename) or files.is_empty(trg_filename) or paths.is_mtime_recursive_older_than_paths(trg_filename, src_pathnames)