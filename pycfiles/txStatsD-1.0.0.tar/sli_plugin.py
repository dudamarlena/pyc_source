# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sidnei/src/txstatsd/trunk/twisted/plugins/sli_plugin.py
# Compiled at: 2012-06-28 13:21:26
import fnmatch, re
from zope.interface import implements
from twisted.plugin import IPlugin
from txstatsd.itxstatsd import IMetricFactory
from txstatsd.metrics.slimetric import SLIMetricReporter, BetweenCondition, AboveCondition, BelowCondition

class SLIMetricFactory(object):
    implements(IMetricFactory, IPlugin)
    name = 'SLI'
    metric_type = 'sli'

    def __init__(self):
        self.config = {}

    def build_metric(self, prefix, name, wall_time_func=None):
        if prefix:
            if not prefix[(-1)] == '.':
                prefix = prefix + '.'
            path = prefix + name
        else:
            path = name
        result = {}
        for (pattern, conditions) in self.config.items():
            if fnmatch.fnmatch(path, pattern):
                result.update(conditions)

        return SLIMetricReporter(path, result)

    def configure(self, options):
        self.section = dict(options.get('plugin_sli', {}))
        rules = self.section.get('rules', None)
        if rules is None:
            return
        else:
            rules = rules.strip()
            regexp = '([\\w\\.\\*\\?\\_\\-]+) => (\\w+) IF (\\w+)(.*)'
            mo = re.compile(regexp)
            for (line_no, rule) in enumerate(rules.split('\n')):
                result = mo.match(rule)
                if result is None:
                    raise TypeError('Did not match rule spec: %s (rule %d: %s)' % (
                     regexp, line_no, rule))
                (head, label, cname, cparams) = result.groups()
                cparams = cparams[1:]
                self.config.setdefault(head, {})
                method = getattr(self, 'build_' + cname, None)
                if method is None:
                    raise TypeError('cannot build condition: %s %s' % (
                     cname, cparams))
                cobj = method(*cparams.split(' '))
                self.config[head][label] = cobj

            return

    def build_above(self, value, slope=0):
        return AboveCondition(float(value), float(slope))

    def build_below(self, value, slope=0):
        return BelowCondition(float(value), float(slope))

    def build_between(self, low, hi):
        return BetweenCondition(float(low), float(hi))


sli_metric_factory = SLIMetricFactory()