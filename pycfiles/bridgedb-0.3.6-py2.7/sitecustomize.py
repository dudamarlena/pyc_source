# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bridgedb/sitecustomize.py
# Compiled at: 2015-11-05 10:40:17
"""sitecustomize ― Handles potential loading of extra code when Python starts.

**Module Usage:**

This is normally (this seems not to work with Twisted, for as-of-yet unknown
reasons) useful for using :mod:`coverage` to measure code execution in spawned
subprocesses in the following way:

 1. Set the environment variable ``COVERAGE_PROCESS_START`` to the absolute
    path of the coverage config file. If you are in the top-level of the
    bridgedb repo, do:

        $ export COVERAGE_PROCESS_START="${PWD}/.coveragerc"

 2. In that coverage config file, in the ``[run]`` section, set 
    ``parallel = True``.

 3. Run coverage. From the top-level of the bridgedb repo, try doing:

        $ make reinstall &&             coverage run $(which trial) ./bridgedb/test/test_* &&             coverage combine && coverage report && coverage html

If ``COVERAGE_PROCESS_START`` is not set, this code does nothing,
``[run] parallel`` should be set to ``False``, and coverage can be run by
leaving out the ``coverage combine`` portion of the above command.

To view the output HTML coverage data, open
``path/to/bridgedb_repo/doc/coverage_html/index.html`` in a browser.
"""
import coverage
coverage.process_startup()