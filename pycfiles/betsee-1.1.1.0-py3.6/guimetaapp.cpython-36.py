# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/betsee/guimetaapp.py
# Compiled at: 2019-04-13 01:37:52
# Size of source mod 2**32: 12662 bytes
"""
High-level **application metadata singleton** (i.e., application-wide object
synopsizing application metadata via read-only properties).
"""
from betse.metaapp import BetseMetaApp
from betse.util.path import dirs, files, pathnames
from betse.util.type.decorator.decmemo import property_cached
from betse.util.type.types import type_check
from betsee import guimetadata
from betsee.lib.pyside2.cache.guipsdcache import CachePolicy

class BetseeMetaApp(BetseMetaApp):
    __doc__ = '\n    **Application metadata singleton** (i.e., application-wide object\n    synopsizing application metadata via read-only properties) subclass.\n\n    Caveats\n    ----------\n    **This subclass must not be accessed from the top-level ``setup.py`` script\n    of this or any other application.** This application and hence this\n    subclass is *not* guaranteed to exist at setuptools-based installation-time\n    for downstream consumers (e.g., BETSEE).\n\n    See Also\n    ----------\n    :mod:`betsee.util.path.guipathsys`\n        Collection of the absolute paths of numerous core files and\n        directories describing the structure of the local filesystem.\n    '

    def init_sans_libs(self):
        """
        Initialize this application *except* mandatory third-party dependencies
        of this application, which requires external resources (e.g.,
        command-line options, configuration files) to have been parsed.

        Specifically, this method (in order):

        #. Initializes BETSE itself by calling the superclass method.
        #. Validates but does *not* initialize all mandatory third-party
           dependencies of this application, which the :meth:`init_libs` method
           does so subsequently.
        #. Validates the active Python interpreter to support multithreading.
        """
        from betsee.lib import guilib
        super().init_sans_libs()
        guilib.die_unless_runtime_mandatory_all()

    @type_check
    def init_libs(self, cache_policy):
        """
        Initialize all mandatory runtime dependencies of this application with
        sane defaults, including those required by both BETSE *and* BETSEE.

        Parameters
        ----------
        cache_policy : CachePolicy
            Type of :mod:`PySide2`-based submodule caching to be performed.
        """
        from betsee.lib.pyside2 import guipsd
        from betsee.util.app import guiapp
        guiapp.init()
        guipsd.init(cache_policy=cache_policy)
        super().init_libs(matplotlib_backend_name='Qt5Agg')

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