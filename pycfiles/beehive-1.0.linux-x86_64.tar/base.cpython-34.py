# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.4/site-packages/beehive/reporter/base.py
# Compiled at: 2014-10-30 08:03:31
# Size of source mod 2**32: 1389 bytes


class Reporter(object):
    __doc__ = '\n    Base class for all reporters.\n    A reporter provides an extension point (variant point) for the runner logic.\n    A reporter is called after a model element is processed\n    (and its result status is known).\n    Otherwise, a reporter is similar to a formatter, but it has a simpler API.\n\n    Processing Logic (simplified)::\n\n        config.reporters = ...  #< Configuration (and provision).\n        runner.run():\n            for feature in runner.features:\n                feature.run()     # And feature scenarios, too.\n                for reporter in config.reporters:\n                    reporter.feature(feature)\n            # -- FINALLY:\n            for reporter in config.reporters:\n                reporter.end()\n\n    An existing formatter can be reused as reporter by using\n    :class:`beehive.report.formatter_reporter.FormatterAsReporter`.\n    '

    def __init__(self, config):
        self.config = config

    def feature(self, feature):
        """
        Called after a feature was processed.

        :param feature:  Feature object (as :class:`beehive.model.Feature`)
        """
        assert feature.status in ('skipped', 'passed', 'failed')
        raise NotImplementedError

    def end(self):
        """
        Called after all model elements are processed (optional-hook).
        """
        pass