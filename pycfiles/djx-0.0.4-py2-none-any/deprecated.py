# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-zr3xXj/pytest/_pytest/deprecated.py
# Compiled at: 2019-02-14 00:35:47
"""
This module contains deprecation messages and bits of code used elsewhere in the codebase
that is planned to be removed in the next pytest release.

Keeping it in a central location makes it easy to track what is deprecated and should
be removed when the time comes.

All constants defined in this module should be either PytestWarning instances or UnformattedWarning
in case of warnings which need to format their messages.
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from _pytest.warning_types import PytestDeprecationWarning
from _pytest.warning_types import RemovedInPytest4Warning
YIELD_TESTS = 'yield tests were removed in pytest 4.0 - {name} will be ignored'
FIXTURE_FUNCTION_CALL = 'Fixture "{name}" called directly. Fixtures are not meant to be called directly,\nbut are created automatically when test functions request them as parameters.\nSee https://docs.pytest.org/en/latest/fixture.html for more information about fixtures, and\nhttps://docs.pytest.org/en/latest/deprecations.html#calling-fixtures-directly about how to update your code.'
FIXTURE_NAMED_REQUEST = PytestDeprecationWarning("'request' is a reserved name for fixtures and will raise an error in future versions")
CFG_PYTEST_SECTION = '[pytest] section in {filename} files is no longer supported, change to [tool:pytest] instead.'
GETFUNCARGVALUE = RemovedInPytest4Warning('getfuncargvalue is deprecated, use getfixturevalue')
RAISES_MESSAGE_PARAMETER = PytestDeprecationWarning("The 'message' parameter is deprecated.\n(did you mean to use `match='some regex'` to check the exception message?)\nPlease comment on https://github.com/pytest-dev/pytest/issues/3974 if you have concerns about removal of this parameter.")
RESULT_LOG = PytestDeprecationWarning('--result-log is deprecated and scheduled for removal in pytest 5.0.\nSee https://docs.pytest.org/en/latest/deprecations.html#result-log-result-log for more information.')
MARK_INFO_ATTRIBUTE = RemovedInPytest4Warning('MarkInfo objects are deprecated as they contain merged marks which are hard to deal with correctly.\nPlease use node.get_closest_marker(name) or node.iter_markers(name).\nDocs: https://docs.pytest.org/en/latest/mark.html#updating-code')
RAISES_EXEC = PytestDeprecationWarning("raises(..., 'code(as_a_string)') is deprecated, use the context manager form or use `exec()` directly\n\nSee https://docs.pytest.org/en/latest/deprecations.html#raises-warns-exec")
WARNS_EXEC = PytestDeprecationWarning("warns(..., 'code(as_a_string)') is deprecated, use the context manager form or use `exec()` directly.\n\nSee https://docs.pytest.org/en/latest/deprecations.html#raises-warns-exec")
PYTEST_PLUGINS_FROM_NON_TOP_LEVEL_CONFTEST = "Defining 'pytest_plugins' in a non-top-level conftest is no longer supported because it affects the entire directory tree in a non-explicit way.\n  {}\nPlease move it to a top level conftest file at the rootdir:\n  {}\nFor more information, visit:\n  https://docs.pytest.org/en/latest/deprecations.html#pytest-plugins-in-non-top-level-conftest-files"
PYTEST_CONFIG_GLOBAL = PytestDeprecationWarning("the `pytest.config` global is deprecated.  Please use `request.config` or `pytest_configure` (if you're a pytest plugin) instead.")
PYTEST_ENSURETEMP = RemovedInPytest4Warning('pytest/tmpdir_factory.ensuretemp is deprecated, \nplease use the tmp_path fixture or tmp_path_factory.mktemp')
PYTEST_LOGWARNING = PytestDeprecationWarning('pytest_logwarning is deprecated, no longer being called, and will be removed soon\nplease use pytest_warning_captured instead')