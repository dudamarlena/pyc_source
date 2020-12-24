# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-zr3xXj/pytest/_pytest/stepwise.py
# Compiled at: 2019-02-14 00:35:47
import pytest

def pytest_addoption(parser):
    group = parser.getgroup('general')
    group.addoption('--sw', '--stepwise', action='store_true', dest='stepwise', help='exit on test fail and continue from last failing test next time')
    group.addoption('--stepwise-skip', action='store_true', dest='stepwise_skip', help='ignore the first failing test but stop on the next failing test')


@pytest.hookimpl
def pytest_configure(config):
    config.pluginmanager.register(StepwisePlugin(config), 'stepwiseplugin')


class StepwisePlugin:

    def __init__(self, config):
        self.config = config
        self.active = config.getvalue('stepwise')
        self.session = None
        if self.active:
            self.lastfailed = config.cache.get('cache/stepwise', None)
            self.skip = config.getvalue('stepwise_skip')
        return

    def pytest_sessionstart(self, session):
        self.session = session

    def pytest_collection_modifyitems(self, session, config, items):
        if not self.active or not self.lastfailed:
            return
        already_passed = []
        found = False
        for item in items:
            if item.nodeid == self.lastfailed:
                found = True
                break
            else:
                already_passed.append(item)

        if not found:
            already_passed = []
        for item in already_passed:
            items.remove(item)

        config.hook.pytest_deselected(items=already_passed)

    def pytest_collectreport(self, report):
        if self.active and report.failed:
            self.session.shouldstop = 'Error when collecting test, stopping test execution.'

    def pytest_runtest_logreport(self, report):
        if not self.active or 'xfail' in report.keywords:
            return
        if report.failed:
            if self.skip:
                if report.nodeid == self.lastfailed:
                    self.lastfailed = None
                self.skip = False
            else:
                self.lastfailed = report.nodeid
                self.session.shouldstop = 'Test failed, continuing from this test next run.'
        elif report.when == 'call':
            if report.nodeid == self.lastfailed:
                self.lastfailed = None
        return

    def pytest_sessionfinish(self, session):
        if self.active:
            self.config.cache.set('cache/stepwise', self.lastfailed)
        else:
            self.config.cache.set('cache/stepwise', [])