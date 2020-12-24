# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-m_4qh6p6/pytest/_pytest/hookspec.py
# Compiled at: 2019-07-30 18:47:09
# Size of source mod 2**32: 10323 bytes
""" hook specifications for pytest plugins, invoked from main.py and builtin plugins.  """

def pytest_addhooks(pluginmanager):
    """called at plugin load time to allow adding new hooks via a call to
    pluginmanager.registerhooks(module)."""
    pass


def pytest_namespace():
    """return dict of name->object to be made globally available in
    the pytest namespace.  This hook is called before command line options
    are parsed.
    """
    pass


def pytest_cmdline_parse(pluginmanager, args):
    """return initialized config object, parsing the specified args. """
    pass


pytest_cmdline_parse.firstresult = True

def pytest_cmdline_preparse(config, args):
    """(deprecated) modify command line arguments before option parsing. """
    pass


def pytest_addoption(parser):
    """register argparse-style options and ini-style config values.

    This function must be implemented in a :ref:`plugin <pluginorder>` and is
    called once at the beginning of a test run.

    :arg parser: To add command line options, call
        :py:func:`parser.addoption(...) <_pytest.config.Parser.addoption>`.
        To add ini-file values call :py:func:`parser.addini(...)
        <_pytest.config.Parser.addini>`.

    Options can later be accessed through the
    :py:class:`config <_pytest.config.Config>` object, respectively:

    - :py:func:`config.getoption(name) <_pytest.config.Config.getoption>` to
      retrieve the value of a command line option.

    - :py:func:`config.getini(name) <_pytest.config.Config.getini>` to retrieve
      a value read from an ini-style file.

    The config object is passed around on many internal objects via the ``.config``
    attribute or can be retrieved as the ``pytestconfig`` fixture or accessed
    via (deprecated) ``pytest.config``.
    """
    pass


def pytest_cmdline_main(config):
    """ called for performing the main command line action. The default
    implementation will invoke the configure hooks and runtest_mainloop. """
    pass


pytest_cmdline_main.firstresult = True

def pytest_load_initial_conftests(args, early_config, parser):
    """ implements the loading of initial conftest files ahead
    of command line option parsing. """
    pass


def pytest_configure(config):
    """ called after command line options have been parsed
        and all plugins and initial conftest files been loaded.
    """
    pass


def pytest_unconfigure(config):
    """ called before test process is exited.  """
    pass


def pytest_runtestloop(session):
    """ called for performing the main runtest loop
    (after collection finished). """
    pass


pytest_runtestloop.firstresult = True

def pytest_collection(session):
    """ perform the collection protocol for the given session. """
    pass


pytest_collection.firstresult = True

def pytest_collection_modifyitems(session, config, items):
    """ called after collection has been performed, may filter or re-order
    the items in-place."""
    pass


def pytest_collection_finish(session):
    """ called after collection has been performed and modified. """
    pass


def pytest_ignore_collect(path, config):
    """ return True to prevent considering this path for collection.
    This hook is consulted for all files and directories prior to calling
    more specific hooks.
    """
    pass


pytest_ignore_collect.firstresult = True

def pytest_collect_directory(path, parent):
    """ called before traversing a directory for collection files. """
    pass


pytest_collect_directory.firstresult = True

def pytest_collect_file(path, parent):
    """ return collection Node or None for the given path. Any new node
    needs to have the specified ``parent`` as a parent."""
    pass


def pytest_collectstart(collector):
    """ collector starts collecting. """
    pass


def pytest_itemcollected(item):
    """ we just collected a test item. """
    pass


def pytest_collectreport(report):
    """ collector finished collecting. """
    pass


def pytest_deselected(items):
    """ called for test items deselected by keyword. """
    pass


def pytest_make_collect_report(collector):
    """ perform ``collector.collect()`` and return a CollectReport. """
    pass


pytest_make_collect_report.firstresult = True

def pytest_pycollect_makemodule(path, parent):
    """ return a Module collector or None for the given path.
    This hook will be called for each matching test module path.
    The pytest_collect_file hook needs to be used if you want to
    create test modules for files that do not match as a test module.
    """
    pass


pytest_pycollect_makemodule.firstresult = True

def pytest_pycollect_makeitem(collector, name, obj):
    """ return custom item/collector for a python object in a module, or None.  """
    pass


pytest_pycollect_makeitem.firstresult = True

def pytest_pyfunc_call(pyfuncitem):
    """ call underlying test function. """
    pass


pytest_pyfunc_call.firstresult = True

def pytest_generate_tests(metafunc):
    """ generate (multiple) parametrized calls to a test function."""
    pass


def pytest_itemstart(item, node):
    """ (deprecated, use pytest_runtest_logstart). """
    pass


def pytest_runtest_protocol(item, nextitem):
    """ implements the runtest_setup/call/teardown protocol for
    the given test item, including capturing exceptions and calling
    reporting hooks.

    :arg item: test item for which the runtest protocol is performed.

    :arg nextitem: the scheduled-to-be-next test item (or None if this
                   is the end my friend).  This argument is passed on to
                   :py:func:`pytest_runtest_teardown`.

    :return boolean: True if no further hook implementations should be invoked.
    """
    pass


pytest_runtest_protocol.firstresult = True

def pytest_runtest_logstart(nodeid, location):
    """ signal the start of running a single test item. """
    pass


def pytest_runtest_setup(item):
    """ called before ``pytest_runtest_call(item)``. """
    pass


def pytest_runtest_call(item):
    """ called to execute the test ``item``. """
    pass


def pytest_runtest_teardown(item, nextitem):
    """ called after ``pytest_runtest_call``.

    :arg nextitem: the scheduled-to-be-next test item (None if no further
                   test item is scheduled).  This argument can be used to
                   perform exact teardowns, i.e. calling just enough finalizers
                   so that nextitem only needs to call setup-functions.
    """
    pass


def pytest_runtest_makereport(item, call):
    """ return a :py:class:`_pytest.runner.TestReport` object
    for the given :py:class:`pytest.Item` and
    :py:class:`_pytest.runner.CallInfo`.
    """
    pass


pytest_runtest_makereport.firstresult = True

def pytest_runtest_logreport(report):
    """ process a test setup/call/teardown report relating to
    the respective phase of executing a test. """
    pass


def pytest_sessionstart(session):
    """ before session.main() is called. """
    pass


def pytest_sessionfinish(session, exitstatus):
    """ whole test run finishes. """
    pass


def pytest_assertrepr_compare(config, op, left, right):
    """return explanation for comparisons in failing assert expressions.

    Return None for no custom explanation, otherwise return a list
    of strings.  The strings will be joined by newlines but any newlines
    *in* a string will be escaped.  Note that all but the first line will
    be indented sligthly, the intention is for the first line to be a summary.
    """
    pass


def pytest_report_header(config, startdir):
    """ return a string to be displayed as header info for terminal reporting."""
    pass


def pytest_report_teststatus(report):
    """ return result-category, shortletter and verbose word for reporting."""
    pass


pytest_report_teststatus.firstresult = True

def pytest_terminal_summary(terminalreporter):
    """ add additional section in terminal summary reporting.  """
    pass


def pytest_logwarning(message, code, nodeid, fslocation):
    """ process a warning specified by a message, a code string,
    a nodeid and fslocation (both of which may be None
    if the warning is not tied to a partilar node/location)."""
    pass


def pytest_doctest_prepare_content(content):
    """ return processed content for a given doctest"""
    pass


pytest_doctest_prepare_content.firstresult = True

def pytest_plugin_registered(plugin, manager):
    """ a new pytest plugin got registered. """
    pass


def pytest_internalerror(excrepr, excinfo):
    """ called for internal errors. """
    pass


def pytest_keyboard_interrupt(excinfo):
    """ called for keyboard interrupt. """
    pass


def pytest_exception_interact(node, call, report):
    """ (experimental, new in 2.4) called when
    an exception was raised which can potentially be
    interactively handled.

    This hook is only called if an exception was raised
    that is not an internal exception like "skip.Exception".
    """
    pass


def pytest_enter_pdb():
    """ called upon pdb.set_trace()"""
    pass