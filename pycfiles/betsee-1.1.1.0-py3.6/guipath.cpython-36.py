# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/betsee/util/path/guipath.py
# Compiled at: 2019-08-01 01:03:54
# Size of source mod 2**32: 20220 bytes
"""
**Pathname dialog** (i.e., :mod:`PySide2`-based modal dialog enabling end users
to interactively select arbitrary paths from the local filesystem that
optionally satisfy caller-defined constraints) functionality.
"""
from betse.util.path import dirs, pathnames, paths
from betse.util.type.iterable import sequences
from betse.util.type.numeric import bits
from betse.util.type.text.string import strjoin
from betse.util.type.types import type_check, CallableTypes, IntOrNoneTypes, MappingType, MappingOrNoneTypes, StrOrNoneTypes

@type_check
def select_path(dialog_callable: CallableTypes, dialog_title: str, dialog_options: IntOrNoneTypes=None, init_pathname: StrOrNoneTypes=None, parent_dirname: StrOrNoneTypes=None, is_subpaths: bool=False, label_to_filetypes: MappingOrNoneTypes=None) -> StrOrNoneTypes:
    """
    Absolute or relative pathname of a path interactively selected by the end
    user from a dialog displayed by calling the passed static getter of the
    :class:`QFileDialog` class (e.g., :func:`QFileDialog.getOpenFileName`)
    configured with the passed parameters if this user confirmed this dialog
    *or* ``None`` otherwise (i.e., if this user cancelled this dialog).

    Constraints
    ----------
    The type of path (e.g., directory, non-directory file) that this dialog
    permits the user to select is constrained *only* by the passed
    ``dialog_callable`` and ``dialog_options`` parameters.

    Similarly, whether the returned pathname is absolute or relative *and*
    whether the passed ``init_pathname`` parameter is required to be absolute
    or relative depends on which optional parameters are passed. Specifically:

    * If the ``parent_dirname`` parameter is non-``None``, the returned
      pathname will be either:

      * If this path resides in this parent directory or a subdirectory
        thereof, relative to the absolute dirname of this parent directory.
      * Else, absolute.

    * Else, the ``parent_dirname`` parameter is ``None``. In this case, the
      returned pathname will *always* be absolute.

    Likewise, if the ``init_pathname`` parameter is non-``None``:

    * If the ``parent_dirname`` parameter is also non-``None``, the
      ``init_pathname`` parameter may be either:

      * Relative, in which case ``init_pathname`` is interpreted as relative to
        the absolute dirname of this parent directory.
      * Absolute, in which case ``init_pathname`` is preserved as is.

    * Else, the ``parent_dirname`` parameter is ``None``. In this case, if the
      ``init_pathname`` parameter is:

      * A basename (i.e., contains no directory separator), ``init_pathname``
        is interpreted as relative to the absolute dirname of the **last
        selected directory** (i.e., the directory component of the pathname
        returned by the most recent call to this function).
      * Relative but *not* a basename (i.e., contains one or more directory
        separators), an exception is raised. While ``init_pathname`` could
        technically be interpreted as relative to the absolute dirname of the
        last selected directory as in the prior case, doing so would be
        unlikely to yield an existing directory and hence be practically
        guaranteed of raising an even less readable exception than this. Why?
        Since the last selected directory is an arbitrary directory,
        concatenating the arbitrary subdirectory defined by ``init_pathname``
        onto that directory is unlikely to yield a meaningful pathname.
      * Absolute, ``init_pathname`` is preserved as is.

    Parameters
    ----------
    dialog_callable : CallableTypes
        Static getter function of the :class:`QFileDialog` class to be called
        by this function (e.g., :func:`QFileDialog.getOpenFileName`).
    dialog_title : str
        Human-readable title of this dialog.
    dialog_options : IntOrNoneTypes
        **Bit field** (i.e., integer OR-ed together from mutually exclusive bit
        flags ala C-style enumeration types) of all :attr:`QFileDialog.Option`
        flags with which to configure this dialog. Note these flags are
        Qt-specific enumerations whose underlying implementations are
        integer-based bit masks. Since PySide2 offers no Python-centric API for
        handling such flags, callers *must* manually reduce the desired flags
        to a Pythonic bit field first. Although callers may technically do so
        by manually converting each Qt-specific enumeration member to an
        integer (e.g., with the :func:`int` builtin), usage of the global
        integer constants predefined by the :mod:`guipathenum` submodule is
        advised. If multiple integer constants are required, callers may OR
        each such constant together with the ``|`` operator (e.g., a
        ``dialog_options`` parameter whose value is
        ``guipathenum.SHOW_DIRS_ONLY | guipathenum.READ_ONLY``, configuring
        this dialog to select only directories in a read-only manner). Defaults
        to ``None``, in which case this dialog defaults to default options.
    init_pathname : StrOrNoneTypes
        Absolute or relative pathname of the path to initially display in this
        dialog. If this path is a directory, this directory is selected and the
        basename of the current selection is the empty string; else if this
        path is a file, this file is selected. If the directory component of
        this path does *not* exist, this directory component is implicitly
        reduced with a non-fatal warning to the last (i.e., most deeply nested)
        parent directory of this path that exists to ensure this dialog opens
        onto an existing directory. Defaults to ``None``, in which case the
        last selected directory is defaulted to.
    parent_dirname : StrOrNoneTypes
        Absolute pathname of the parent directory to select a path from.
        Defaults to ``None``, in which case no parental constraint is applied.
        See above for details.
    is_subpaths : bool
        ``True`` only if both the ``init_pathname`` parameter *and* the
        returned selected path are required to be children of the
        ``parent_dirname`` parameter (i.e., residing in either this directory
        itself *or* a subdirectory of this directory). Defaults to ``False``,
        in which case these paths may reside in any directory.
    label_to_filetypes : MappingOrNoneTypes
        Dictionary mapping from a human-readable label to be displayed for each
        iterable of related filetypes selectable by this dialog (e.g.,
        ``Images``) to that iterable (e.g., ``('jpg', 'png')``) if this dialog
        selects only files of specific filetypes *or* ``None`` otherwise. If
        this dialog only selects directories, this should be ``None``. Defaults
        to ``None``, in which case all paths of the requisite type (e.g., file,
        directory) regardless of filetype are selectable.

    Returns
    ----------
    StrOrNoneTypes
        Either:

        * If this dialog was confirmed, the absolute or relative pathname of
          the path confirmed by the end user.
        * If this dialog was cancelled, ``None``.
    """
    from betsee.util.app import guiappwindow
    from betsee.util.path import guipathenum
    is_selecting_dir = dialog_options is not None and bits.is_bit_on(bit_field=dialog_options,
      bit_mask=(guipathenum.SHOW_DIRS_ONLY))
    prior_dirname = _get_selected_prior_dirname()
    if init_pathname is None:
        init_pathname = prior_dirname
    if parent_dirname is None:
        if pathnames.is_basename(init_pathname):
            init_pathname = pathnames.join(prior_dirname, init_pathname)
        else:
            pathnames.die_if_relative(init_pathname)
    else:
        pathnames.die_if_relative(parent_dirname)
        dirs.die_unless_dir(parent_dirname)
    if pathnames.is_relative(init_pathname):
        init_pathname = pathnames.join(parent_dirname, init_pathname)
    else:
        if is_subpaths:
            pathnames.die_unless_parent(parent_dirname=parent_dirname,
              child_pathname=init_pathname)
        if not paths.is_path(init_pathname):
            if is_selecting_dir:
                init_pathname = dirs.get_parent_dir_last(init_pathname)
            else:
                init_dirname = pathnames.get_dirname(init_pathname)
                init_basename = pathnames.get_basename(init_pathname)
                init_dirname = dirs.get_parent_dir_last(init_dirname)
                init_pathname = pathnames.join(init_dirname, init_basename)
    dialog_args = [
     guiappwindow.get_main_window(),
     dialog_title,
     init_pathname]
    if label_to_filetypes is not None:
        filetypes_filter = _make_filetypes_filter(label_to_filetypes)
        dialog_args.append(filetypes_filter)
        dialog_args.append(None)
    if dialog_options is not None:
        dialog_args.append(dialog_options)
    selected_pathname = dialog_callable(*dialog_args)
    if sequences.is_sequence(selected_pathname):
        if len(selected_pathname) == 2:
            selected_pathname = selected_pathname[0]
        return selected_pathname or None
    else:
        if is_selecting_dir:
            _set_selected_prior_dirname(selected_pathname)
        else:
            selected_dirname = pathnames.get_dirname(selected_pathname)
            _set_selected_prior_dirname(selected_dirname)
        if parent_dirname is not None:
            if pathnames.is_parent(parent_dirname=parent_dirname,
              child_pathname=selected_pathname):
                selected_pathname = pathnames.relativize(src_dirname=parent_dirname,
                  trg_pathname=selected_pathname)
            elif is_subpaths:
                pathnames.die_unless_parent(parent_dirname=parent_dirname,
                  child_pathname=selected_pathname)
        return selected_pathname


@type_check
def _make_filetypes_filter(label_to_filetypes: MappingType) -> str:
    """
    ``;;``-delimited string of all filetypes (e.g.,
    ``All files (*);; YAML files (*.yaml *.yml)``) specified by the passed
    dictionary, syntactically conforming to the Qt-specific format supported by
    the :class:`QFileDialog` class.

    Parameters
    ----------
    label_to_filetypes : MappingType
        Dictionary mapping from a human-readable label to be displayed for each
        iterable of related filetypes selectable by this dialog (e.g.,
        ``Images``) to that iterable (e.g., ``('jpg', 'png')``).

    Returns
    ----------
    str
        ``;;``-delimited string of all filetypes specified by this dictionary.
    """
    filetypes_filter = ''
    for filetypes_label, filetypes_iterable in label_to_filetypes.items():
        filetypes_listed = strjoin.join_on_space((filetype if filetype == '*' else '*' + pathnames.dot_filetype(filetype)) for filetype in filetypes_iterable)
        filetypes_filter += '{} ({});;'.format(filetypes_label, filetypes_listed)

    return filetypes_filter


def _get_selected_prior_dirname() -> str:
    """
    Absolute dirname of the **last selected directory** (i.e., the directory
    component of the pathname returned by the most recent call to the
    :func:`select_path` function).

    Returns
    ----------
    str
        Absolute dirname of either:

        * If the current user has already successfully selected at least one
          path from a path dialog *and* the most recently selected such path
          still exists, the directory component of that path.
        * Else, a user-specific directory containing work-related files.
    """
    from betsee.util.io import guisettings
    from betsee.util.path import guipathsys
    selected_prior_dirname = guisettings.get_setting_or_none(setting_name='path_dialog/selected_prior_dirname')
    if selected_prior_dirname is None or not dirs.is_dir(selected_prior_dirname):
        selected_prior_dirname = guipathsys.get_user_documents_existing_dirname()
    return selected_prior_dirname


@type_check
def _set_selected_prior_dirname(dirname: str) -> None:
    """
    Set the absolute dirname of the **last selected directory** (i.e., the
    directory component of the pathname returned by the most recent call to the
    :func:`select_path` function) to the passed dirname.

    Parameters
    ----------
    dirname : str
        Absolute dirname of the last selected directory.
    """
    from betsee.util.io import guisettings
    return guisettings.set_setting(setting_name='path_dialog/selected_prior_dirname',
      setting_value=dirname)