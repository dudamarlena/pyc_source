# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.cygwin-1.7.35-i686/egg/seedbox/common/tools.py
# Compiled at: 2015-06-14 13:30:57
"""Holds a group of tools useful by all modules."""
import copy, itertools, logging, os, six
LOG = logging.getLogger(__name__)

def verify_path(path_entry):
    """Verify a path

    if it exists make sure it is an absolute path and return. else None

    :param path_entry: path to file or directory on host
    """
    if path_entry and os.path.exists(path_entry):
        if os.path.isabs(path_entry):
            return path_entry
        else:
            return os.path.realpath(path_entry)

    else:
        return
    return


def format_file_ext(filetypes):
    """Format file extensions

    Verifies that each item in the list of filetypes is a string
    and starts with a '.'

    :param list filetypes: a list of extensions representing types of files
    """
    result_list = []
    if filetypes and isinstance(filetypes, list):
        for filetype in filetypes:
            if not isinstance(filetype, six.string_types):
                continue
            filetype = filetype.strip()
            if not filetype:
                continue
            if not filetype.startswith('.'):
                result_list.append('.' + filetype)
            else:
                result_list.append(filetype)

    return result_list


def make_opt_list(opts, group):
    """Generate a list of tuple containing group, options

    :param opts: option lists associated with a group
    :type opts: list
    :param group: name of an option group
    :type group: str
    :return: a list of (group_name, opts) tuples
    :rtype: list
    """
    _opts = [
     (
      group, list(itertools.chain(*opts)))]
    return [ (g, copy.deepcopy(o)) for g, o in _opts ]