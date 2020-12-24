# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/betsee/guiappmeta.py
# Compiled at: 2019-08-22 00:24:35
# Size of source mod 2**32: 16858 bytes
"""
High-level **application metadata singleton** (i.e., application-wide object
synopsizing application metadata via read-only properties).
"""
from betse.appmeta import BetseAppMeta
from betse.util.path import dirs, files, pathnames
from betse.util.type.decorator.decmemo import property_cached
from betse.util.type.types import type_check, ModuleType
from betsee import guimetadata
from betsee.lib.pyside2.cache.guipsdcache import CachePolicy
from betsee.util.app import guiappwindow

class BetseeAppMeta(BetseAppMeta):
    __doc__ = '\n    **Application metadata singleton** (i.e., application-wide object\n    synopsizing application metadata via read-only properties) subclass.\n\n    Caveats\n    ----------\n    **This subclass must not be accessed from the top-level ``setup.py`` script\n    of this or any other application.** This application and hence this\n    subclass is *not* guaranteed to exist at setuptools-based installation-time\n    for downstream consumers (e.g., BETSEE).\n\n    See Also\n    ----------\n    :mod:`betsee.util.path.guipathsys`\n        Collection of the absolute paths of numerous core files and\n        directories describing the structure of the local filesystem.\n    '

    @type_check
    def init_libs(self, cache_policy):
        """
        Initialize all mandatory runtime dependencies of this application with
        sane defaults, including those required by both BETSE *and* BETSEE.

        Parameters
        ----------
        cache_policy : CachePolicy
            Type of :mod:`PySide2`-based submodule caching to perform.
        """
        from betsee.lib.pyside2 import guipsd
        from betsee.util.app import guiapp
        guiapp.init()
        guipsd.init(cache_policy=cache_policy)
        super().init_libs(matplotlib_backend_name='Qt5Agg')

    def deinit(self):
        super().deinit()
        guiappwindow.unset_main_window()

    @property
    def _module_metadata(self) -> ModuleType:
        return guimetadata

    @property
    def _module_metadeps(self) -> ModuleType:
        """
        **Application-wide dependency metadata submodule** (i.e., submodule
        publishing lists of version-pinned dependencies as global constants
        synopsizing all requirements of the current application).

        Design
        ----------
        This property dynamically creates and returns a new in-memory submodule
        that does *not* physically exist on-disk. Rather, this high-level
        submodule merges *all* dependency metadata defined by lower-level
        submodules that do actually exist on-disk. This means:

        * BETSE's :mod:`betse.metadeps` submodule.
        * BETSEE's :mod:`betsee.guimetadeps` submodule.

        This submodule satisfies all requirements of both BETSE and BETSEE,
        thus safeguarding usage of the :mod:`betse.lib.libs` API -- notably
        calls to the :func:`betse.lib.libs.import_runtime_optional` function
        distributed throughout the BETSE and BETSEE codebases, regardless of
        the codebase in which they reside.

        See Also
        ----------
        :meth:`module_metadeps`
            Concrete public property validating the module returned by this
            abstract private property to expose the expected attributes.
        """
        from betse import metadeps as betse_metadeps
        from betse.util.app.meta import appmetamod
        from betsee import guimetadeps as betsee_metadeps
        module_metadeps_merged = appmetamod.merge_module_metadeps(module_name='betsee.__betse_plus_betsee_metadeps__',
          modules_metadeps=(
         betse_metadeps, betsee_metadeps))
        return module_metadeps_merged

    @property_cached
    def data_py_dirname(self) -> str:
        """
        Absolute dirname of this application's data subdirectory containing
        pure-Python modules and packages generated at runtime by this
        application if found *or* raise an exception otherwise (i.e., if this
        directory is *not* found).
        """
        return dirs.join_or_die(self.data_dirname, 'py')

    @property_cached
    def data_qrc_dirname(self) -> str:
        """
        Absolute dirname of this application's data subdirectory containing
        XML-formatted Qt resource collection (QRC) files exported by the
        external Qt Designer application and all binary resource files listed
        in these files if found *or* raise an exception otherwise (i.e., if
        this directory is *not* found).
        """
        return dirs.join_or_die(self.data_dirname, 'qrc')

    @property_cached
    def data_ui_dirname(self) -> str:
        """
        Absolute dirname of this application's data subdirectory containing
        XML-formatted user interface (UI) files exported by the external Qt
        Designer application if found *or* raise an exception otherwise (i.e.,
        if this directory is *not* found).
        """
        return dirs.join_or_die(self.data_dirname, 'ui')

    @property_cached
    def dot_py_dirname(self) -> str:
        """
        Absolute dirname of this application's dot subdirectory containing
        pure-Python modules and packages generated at runtime by this
        application if found *or* raise an exception otherwise (i.e., if this
        directory is *not* found).
        """
        return dirs.join_and_make_unless_dir(self.dot_dirname, 'py')

    @property_cached
    def data_qrc_filename(self) -> str:
        """
        Absolute filename of the XML-formatted Qt resource collection (QRC)
        file exported by the external Qt Designer application structuring all
        external resources (e.g., icons) required by this application's main
        window if found *or* raise an exception otherwise (i.e., if this file
        is *not* found).
        """
        return files.join_or_die(self.data_qrc_dirname, self.package_name + '.qrc')

    @property_cached
    def data_ui_filename(self) -> str:
        """
        Absolute filename of the XML-formatted user interface (UI) file
        exported by the external Qt Designer application structuring this
        application's main window if found *or* raise an exception otherwise
        (i.e., if this file is *not* found).
        """
        return files.join_or_die(self.data_ui_dirname, self.package_name + '.ui')

    @property_cached
    def data_py_qrc_filename(self) -> str:
        """
        Absolute filename of the pure-Python application-wide module generated
        from the XML-formatted Qt resource collection (QRC) file exported by
        the external Qt Designer application structuring all external resources
        (e.g., icons) required by this application's main window.

        If this module exists, this module is guaranteed to be importable but
        *not* necessarily up-to-date with the input paths from which this
        module is dynamically regenerated at runtime; else, the caller is
        assumed to explicitly regenerate this module.

        See Also
        ----------
        :meth:`dot_py_qrc_filename`
            User-specific equivalent of this file.
        :mod:`betsee.lib.pyside2.cache.guipsdcache`
            Submodule dynamically generating this module.
        """
        return pathnames.join(self.data_py_dirname, guimetadata.MAIN_WINDOW_QRC_MODULE_NAME + '.py')

    @property_cached
    def data_py_ui_filename(self) -> str:
        """
        Absolute filename of the pure-Python application-wide module generated
        from the XML-formatted user interface (UI) file exported by the
        external Qt Designer application structuring this application's main
        window if found *or* raise an exception otherwise (i.e., if this
        directory is *not* found).

        If this module exists, this module is guaranteed to be importable but
        *not* necessarily up-to-date with the input paths from which this
        module is dynamically regenerated at runtime; else, the caller is
        assumed to explicitly regenerate this module.

        See Also
        ----------
        :meth:`dot_py_ui_filename`
            User-specific equivalent of this file.
        :mod:`betsee.lib.pyside2.cache.guipsdcache`
            Submodule dynamically generating this module.
        """
        return pathnames.join(self.data_py_dirname, guimetadata.MAIN_WINDOW_UI_MODULE_NAME + '.py')

    @property_cached
    def dot_py_qrc_filename(self) -> str:
        """
        Absolute filename of the pure-Python user-specific module generated
        from the XML-formatted Qt resource collection (QRC) file exported by
        the external Qt Designer application structuring all external resources
        (e.g., icons) required by this application's main window.

        See Also
        ----------
        :meth:`data_py_qrc_filename`
            Application-wide equivalent of this file.
        """
        return pathnames.join(self.dot_py_dirname, pathnames.get_basename(self.data_py_qrc_filename))

    @property_cached
    def dot_py_ui_filename(self) -> str:
        """
        Absolute filename of the pure-Python user-specific module generated
        from the XML-formatted user interface (UI) file exported by the
        external Qt Designer application structuring this application's main
        window if found *or* raise an exception otherwise (i.e., if this
        directory is *not* found).

        See Also
        ----------
        :mod:`betsee.lib.pyside2.cache.guipsdcache`
            Submodule dynamically generating this module.
        """
        return pathnames.join(self.dot_py_dirname, pathnames.get_basename(self.data_py_ui_filename))