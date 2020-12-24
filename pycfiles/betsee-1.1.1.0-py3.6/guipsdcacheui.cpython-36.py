# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/betsee/lib/pyside2/cache/guipsdcacheui.py
# Compiled at: 2019-09-27 02:43:45
# Size of source mod 2**32: 27320 bytes
"""
High-level support facilities for integrating :mod:`PySide2` widget classes
with XML-formatted user interface (UI) files exported by the external Qt
Designer application.
"""
import PySide2
from PySide2 import QtWidgets
from PySide2.QtCore import QCoreApplication, QObject
from betse.util.io import iofiles
from betse.util.io.log import logs
from betse.util.path import files, pathnames, paths
from betse.util.py import pyident, pys
from betse.util.py.pyident import IDENTIFIER_UNQUALIFIED_REGEX
from betse.util.type.cls import classes
from betse.util.type.text import regexes
from betse.util.type.types import type_check, MappingType
from betsee.guiexception import BetseeCacheException
from io import StringIO

@type_check
def convert_ui_to_py_file(ui_filename: str, py_filename: str, promote_obj_name_to_class: MappingType) -> None:
    """
    Convert the XML-formatted file with the passed ``.ui``-suffixed filename
    exported by the external Qt Designer GUI into the :mod:`PySide2`-based
    Python module with the passed ``.py``-suffixed filename if capable of doing
    so *or* log a non-fatal warning and return otherwise.

    This function requires the optional third-party dependency
    ``pyside2-tools`` distributed by The Qt Company. Specifically, this
    high-level function wraps the low-level
    :meth:`pyside2uic.Compiler.compiler.UICompiler.compileUi` method installed
    by that dependency with a human-usable API.

    Design
    ----------
    This function silently overwrites this output file with the dynamically
    compiled contents of a pure-Python model declaring:

    * A custom helper class defining the following methods:

      * ``setupUi()``, accepting an instance of the :mod:`PySide2` widget base
        class listed as the last item of the global sequence described below
        and customizing this widget as specified by this input UI file.
      * ``retranslateUi()``, accepting a similar instance and translating all
        strings displayed by this widget from their default language
        (typically, English) into the locale of the current user.

    * A global sequence variable whose:

      * Name is the value of the
        :data:`BASE_CLASSES_GLOBAL_NAME` global string variable,
      * Value is the sequence of all base classes that the main Qt window
        widget class for this application *must* subclass (in order):

        #. The custom helper class described above.
        #. The :mod:`PySide2` widget base class of the object to be passed to
           all methods defined by this class (e.g., ``setupUi()``). These
           methods do *not* validate this to be the case but do raise
           non-human-readable exceptions when passed objects that are *not*
           instances of this base class. This base class is defined by this
           input UI file and is typically one of the following:

           * :class:`PySide2.QWidget.QDialog`.
           * :class:`PySide2.QWidget.QWidget`.
           * :class:`PySide2.QWidget.QMainWindow`.

    This function provides a :mod:`PySide2`-specific implementation of the
    PyQt-specific :func:`PyQt5.uic.loadUiType` function, albeit with a more
    typesafe API. For unknown reasons (presumably laziness), :mod:`PySide2`
    lacks an analogue to this function.

    For equally unknown reasons, the class returned by that function is
    commonly referred to as the "form class" in most Qt documentation. This
    class has no relation to the :class:`PySide2.QLayout.QFormLayout` base
    class and is thus arguably *not* a "form class." For disambiguity, we
    prefer to refer to this class as simply the "generated UI class."

    Parameters
    ----------
    ui_filename : str
        Absolute or relative path of the input ``.ui``-suffixed file.
    py_filename : str
        Absolute or relative path of the output ``.py``-suffixed file.
    promote_obj_name_to_class : MappingType
        Dictionary mapping from the name of each instance variable of the main
        window to manually reinstantiate to the application-specific widget
        subclass to declare that variable to be an instance of. This dictionary
        facilitates the manual "promotion" of widgets for which the Qt
        (Creator|Designer) GUI currently provides no means of official
        promotion, notably including :class:`QButtonGroup` widgets.

    Returns
    ----------
    type
        UI class generated from the XML-formatted file with this filename
        exported by the external Qt Designer application.

    Raises
    ----------
    BetseeCacheException
        If the currently installed version of :mod:`PySide2` targets the
        Qt 5.6.* (LTS) line of stable releases or older. In this case, the
        :mod:`pyside2uic` package is well-known to be fundamentally broken in
        numerous critical ways *not* trivially resolvable with a monkey-patch.

        Under Qt 5.6, for example, the core
        :meth:`pyside2uic.uiparser.UIParser.createWidget` method raises
        non-human-readable exceptions on iterating button group labels: e.g.,

            AttributeError: 'str' object has no attribute 'string'

            Traceback (most recent call last):
            File "/home/eric/anaconda3/lib/python3.6/site-packages/betse/util/cli/cliabc.py", line 180, in run profile_filename=self._profile_filename,
            File "", line 65, in func_type_checked
            File "/home/eric/anaconda3/lib/python3.6/site-packages/betse/util/py/pyprofile.py", line 114, in profile_callable
            profile_filename=profile_filename,
            File "/home/eric/anaconda3/lib/python3.6/site-packages/betse/util/py/pyprofile.py", line 130, in _profile_callable_none
            return call(*args, **kwargs)
            File "/home/eric/anaconda3/lib/python3.6/site-packages/betsee/cli/guicli.py", line 236, in _do
            app_gui = BetseeGUI(sim_conf_filename=self._sim_conf_filename)
            File "", line 15, in func_type_checked
            File "/home/eric/anaconda3/lib/python3.6/site-packages/betsee/gui/guimain.py", line 255, in init
            guicache.cache_py_files()
            File "/home/eric/anaconda3/lib/python3.6/site-packages/betsee.lib.pyside2.cache.guipsdcache.py", line 64, in cache_py_files
            _cache_py_ui_file()
            File "/home/eric/anaconda3/lib/python3.6/site-packages/betsee.lib.pyside2.cache.guipsdcache.py", line 198, in _cache_py_ui_file
            promote_obj_name_to_class=_PROMOTE_OBJ_NAME_TO_CLASS,
            File "", line 35, in func_type_checked
            File "/home/eric/anaconda3/lib/python3.6/site-packages/betsee/util/io/xml/guiui.py", line 280, in convert_ui_to_py_file_if_able
            from_imports=False,
            File "/home/eric/anaconda3/lib/python3.6/site-packages/pyside2uic/Compiler/compiler.py", line 91, in compileUi
            w = self.parse(input_stream)
            File "/home/eric/anaconda3/lib/python3.6/site-packages/pyside2uic/uiparser.py", line 871, in parse
            actor(elem)
            File "/home/eric/anaconda3/lib/python3.6/site-packages/pyside2uic/uiparser.py", line 714, in createUserInterface
            self.traverseWidgetTree(elem)
            File "/home/eric/anaconda3/lib/python3.6/site-packages/pyside2uic/uiparser.py", line 692, in traverseWidgetTree
            handler(self, child)
            File "/home/eric/anaconda3/lib/python3.6/site-packages/pyside2uic/uiparser.py", line 197, in createWidget
            self.traverseWidgetTree(elem)
            File "/home/eric/anaconda3/lib/python3.6/site-packages/pyside2uic/uiparser.py", line 692, in traverseWidgetTree
            handler(self, child)
            File "/home/eric/anaconda3/lib/python3.6/site-packages/pyside2uic/uiparser.py", line 427, in createLayout
            self.traverseWidgetTree(elem)
            File "/home/eric/anaconda3/lib/python3.6/site-packages/pyside2uic/uiparser.py", line 692, in traverseWidgetTree
            handler(self, child)
            File "/home/eric/anaconda3/lib/python3.6/site-packages/pyside2uic/uiparser.py", line 464, in handleItem
            self.traverseWidgetTree(elem)
            File "/home/eric/anaconda3/lib/python3.6/site-packages/pyside2uic/uiparser.py", line 692, in traverseWidgetTree
            handler(self, child)
            File "/home/eric/anaconda3/lib/python3.6/site-packages/pyside2uic/uiparser.py", line 197, in createWidget
            self.traverseWidgetTree(elem)
            File "/home/eric/anaconda3/lib/python3.6/site-packages/pyside2uic/uiparser.py", line 692, in traverseWidgetTree
            handler(self, child)
            File "/home/eric/anaconda3/lib/python3.6/site-packages/pyside2uic/uiparser.py", line 197, in createWidget
            self.traverseWidgetTree(elem)
            File "/home/eric/anaconda3/lib/python3.6/site-packages/pyside2uic/uiparser.py", line 692, in traverseWidgetTree
            handler(self, child)
            File "/home/eric/anaconda3/lib/python3.6/site-packages/pyside2uic/uiparser.py", line 197, in createWidget
            self.traverseWidgetTree(elem)
            File "/home/eric/anaconda3/lib/python3.6/site-packages/pyside2uic/uiparser.py", line 692, in traverseWidgetTree
            handler(self, child)
            File "/home/eric/anaconda3/lib/python3.6/site-packages/pyside2uic/uiparser.py", line 427, in createLayout
            self.traverseWidgetTree(elem)
            File "/home/eric/anaconda3/lib/python3.6/site-packages/pyside2uic/uiparser.py", line 692, in traverseWidgetTree
            handler(self, child)
            File "/home/eric/anaconda3/lib/python3.6/site-packages/pyside2uic/uiparser.py", line 464, in handleItem
            self.traverseWidgetTree(elem)
            File "/home/eric/anaconda3/lib/python3.6/site-packages/pyside2uic/uiparser.py", line 692, in traverseWidgetTree
            handler(self, child)
            File "/home/eric/anaconda3/lib/python3.6/site-packages/pyside2uic/uiparser.py", line 197, in createWidget
            self.traverseWidgetTree(elem)
            File "/home/eric/anaconda3/lib/python3.6/site-packages/pyside2uic/uiparser.py", line 692, in traverseWidgetTree
            handler(self, child)
            File "/home/eric/anaconda3/lib/python3.6/site-packages/pyside2uic/uiparser.py", line 427, in createLayout
            self.traverseWidgetTree(elem)
            File "/home/eric/anaconda3/lib/python3.6/site-packages/pyside2uic/uiparser.py", line 692, in traverseWidgetTree
            handler(self, child)
            File "/home/eric/anaconda3/lib/python3.6/site-packages/pyside2uic/uiparser.py", line 464, in handleItem
            self.traverseWidgetTree(elem)
            File "/home/eric/anaconda3/lib/python3.6/site-packages/pyside2uic/uiparser.py", line 692, in traverseWidgetTree
            handler(self, child)
            File "/home/eric/anaconda3/lib/python3.6/site-packages/pyside2uic/uiparser.py", line 197, in createWidget
            self.traverseWidgetTree(elem)
            File "/home/eric/anaconda3/lib/python3.6/site-packages/pyside2uic/uiparser.py", line 692, in traverseWidgetTree
            handler(self, child)
            File "/home/eric/anaconda3/lib/python3.6/site-packages/pyside2uic/uiparser.py", line 427, in createLayout
            self.traverseWidgetTree(elem)
            File "/home/eric/anaconda3/lib/python3.6/site-packages/pyside2uic/uiparser.py", line 692, in traverseWidgetTree
            handler(self, child)
            File "/home/eric/anaconda3/lib/python3.6/site-packages/pyside2uic/uiparser.py", line 464, in handleItem
            self.traverseWidgetTree(elem)
            File "/home/eric/anaconda3/lib/python3.6/site-packages/pyside2uic/uiparser.py", line 692, in traverseWidgetTree
            handler(self, child)
            File "/home/eric/anaconda3/lib/python3.6/site-packages/pyside2uic/uiparser.py", line 197, in createWidget
            self.traverseWidgetTree(elem)
            File "/home/eric/anaconda3/lib/python3.6/site-packages/pyside2uic/uiparser.py", line 692, in traverseWidgetTree
            handler(self, child)
            File "/home/eric/anaconda3/lib/python3.6/site-packages/pyside2uic/uiparser.py", line 427, in createLayout
            self.traverseWidgetTree(elem)
            File "/home/eric/anaconda3/lib/python3.6/site-packages/pyside2uic/uiparser.py", line 692, in traverseWidgetTree
            handler(self, child)
            File "/home/eric/anaconda3/lib/python3.6/site-packages/pyside2uic/uiparser.py", line 464, in handleItem
            self.traverseWidgetTree(elem)
            File "/home/eric/anaconda3/lib/python3.6/site-packages/pyside2uic/uiparser.py", line 692, in traverseWidgetTree
            handler(self, child)
            File "/home/eric/anaconda3/lib/python3.6/site-packages/pyside2uic/uiparser.py", line 214, in createWidget
            bg_name = bg_i18n.string

        While monkey-patching that specific issue is technically feasible,
        doing so uncovers additional issues in other :mod:`pyside2uic`
        callables whose resolution is *not* technically feasible.

    See Also
    ----------
    http://pyqt.sourceforge.net/Docs/PyQt5/designer.html
        :mod:`PyQt5`-specific documentation detailing this conversion. Although
        :mod:`PyQt5`-specific, this documentation probably serves as the
        canonical resource for understanding this function's internal
        behaviour.
    """
    from betse.lib import libs
    from betsee.lib.pyside2 import guipsd
    from betsee.lib.pyside2.guipsdui import BASE_CLASSES_GLOBAL_NAME
    logs.log_info('Synchronizing PySide2 module "%s" from "%s"...', pathnames.get_basename(py_filename), pathnames.get_basename(ui_filename))
    if guipsd.is_version_5_6_or_older():
        raise BetseeCacheException('Broken "pyside2uic" package bundled with PySide2 < 5.7.0 detected.')
    files.die_unless_file(ui_filename)
    paths.die_unless_writable(py_filename)
    pathnames.die_unless_filetype_equals(pathname=ui_filename, filetype='ui')
    pathnames.die_unless_filetype_equals(pathname=py_filename, filetype='py')
    ui_code_str_buffer = StringIO()
    pyside2uic = libs.import_runtime_optional('pyside2uic')
    try:
        ui_compiler = pyside2uic.Compiler.compiler.UICompiler(PySide2.__all__)
    except TypeError:
        ui_compiler = pyside2uic.Compiler.compiler.UICompiler()

    ui_code_metadata = ui_compiler.compileUi(input_stream=ui_filename,
      output_stream=ui_code_str_buffer,
      from_imports=False)
    ui_form_class_name = ui_code_metadata['uiclass']
    ui_base_class_name = ui_code_metadata['baseclass']
    ui_base_class = getattr(QtWidgets, ui_base_class_name, None)
    if ui_base_class is None:
        raise BetseeCacheException(title=(QCoreApplication.translate('convert_ui_to_py_file', 'PySide2 UI Compiler Error')),
          synopsis=(QCoreApplication.translate('convert_ui_to_py_file', 'PySide2 widget base class "{0}" not found.'.format(ui_base_class_name))))
    ui_code_str_buffer.write('\nfrom PySide2.QtWidgets import {base_class}\n{var_name} = ({form_class}, {base_class})\n'.format(var_name=BASE_CLASSES_GLOBAL_NAME,
      form_class=ui_form_class_name,
      base_class=ui_base_class_name))
    ui_code_str = _munge_ui_code(ui_code_str=(ui_code_str_buffer.getvalue()),
      promote_obj_name_to_class=promote_obj_name_to_class)
    iofiles.write_str_to_filename(text=ui_code_str,
      output_filename=py_filename,
      is_overwritable=True)


@type_check
def _munge_ui_code(ui_code_str: str, promote_obj_name_to_class: MappingType) -> str:
    """
    Munge (i.e., modify) the passed string of Python code comprising the
    contents of the current ``.ui``-suffixed file to be subsequently written.

    Specifically, this function:

    * Prepends this code by a shebang line unambiguously running the executable
      binary for the active Python interpreter and machine architecture.
    * Globally replaces all lines of this code reducing vector SVG icons to
      non-vector in-memory pixmaps with lines preserving these icons as is. See
      this function's body for detailed commentary.
    * For the name of each instance variable of the main window and
      application-specific subclass to instantiate that variable to in the
      passed dictonary, replaces the single line of this code instantiating
      this variable to a non-promoted stock Qt widget class with a line instead
      instantiating this variable to this application-specific widget subclass.

    Parameters
    ----------
    ui_code_str : str
        String of Python code comprising the original contents of this file.
    promote_obj_name_to_class : MappingType
        See the :func:`convert_ui_to_py_file_if_able` function for comments.

    Returns
    ----------
    str
        String of Python code comprising the modified contents of this file.
    """
    ui_code_str = regexes.replace_substrs_line(text=ui_code_str,
      regex='^(\\s*icon\\d*\\.add)Pixmap\\(QtGui\\.QPixmap\\(("[^"]+\\.svg")\\)(.*)$',
      replacement='\\1File(\\2, QtCore.QSize()\\3')
    for promote_obj_name, promote_class in promote_obj_name_to_class.items():
        pyident.die_unless_unqualified(promote_obj_name)
        classes.die_unless_subclass(subclass=promote_class,
          superclass=QObject)
        promote_class_name = classes.get_name_unqualified(promote_class)
        promote_class_module_name = classes.get_module_name_qualified(promote_class)
        ui_code_str += '\nfrom {} import {}\n'.format(promote_class_module_name, promote_class_name)
        promote_regex = '^(\\s*self\\.{promote_obj_name}\\s*=\\s*)QtWidgets\\.{widget_class_name}(\\([^)]*\\))$'.format(promote_obj_name=promote_obj_name,
          widget_class_name=IDENTIFIER_UNQUALIFIED_REGEX)
        ui_code_str = regexes.replace_substrs_line(text=ui_code_str,
          regex=promote_regex,
          replacement=('\\1{}\\2'.format(promote_class_name)))

    ui_code_str = '{}\n{}'.format(pys.get_shebang(), ui_code_str)
    return ui_code_str