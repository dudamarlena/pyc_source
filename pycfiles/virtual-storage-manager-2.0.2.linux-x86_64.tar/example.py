# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vsm/diamond/collectors/example/example.py
# Compiled at: 2016-06-13 14:11:03
import diamond.collector

class ExampleCollector(diamond.collector.Collector):

    def get_default_config_help(self):
        config_help = super(ExampleCollector, self).get_default_config_help()
        config_help.update({})
        return config_help

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        config = super(ExampleCollector, self).get_default_config()
        config.update({'path': 'example'})
        return config

    def collect(self):
        """
        Overrides the Collector.collect method
        """
        metric_name = 'metric1'
        metric_value = 343
        self.publish(metric_name, metric_value)