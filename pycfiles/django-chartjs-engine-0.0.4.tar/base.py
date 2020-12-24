# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Jeff/Development/python/chartjs_engine/chartjs_engine/views/base.py
# Compiled at: 2016-12-29 17:38:09
"""
The base chart class that all the chart type cublcasses inherits from

TODO:

1. Construct the data in JSON and make it accpet all types of charts.
2. Move [chartjs] markup splitting to the model so chart engine can be agnostic,
   and just take chart settings as input
3. split each chart type class into smaller methods
"""
import random

class Chart(object):
    """A base class for charts, init will store all the data needed for subclasses"""

    def __init__(self, chart_type=None, chart_name=None, options=None, chart_labels=None, datasets=None):
        """
                Setting all of the settings that will be needed in the charts subclasses
                """
        self.chart_type = chart_type
        self.datasets = datasets
        self.chart_name = chart_name
        self.options = options
        self.data = {'labels': chart_labels}
        if not all([self.chart_type, self.chart_name, self.data['labels'],
         self.datasets]):
            raise Exception('Chart class needs to have all keyword arguments specified')

    def random_color(self):
        """Generates a random javascript valid rgba color for each set in datasets
                return: tuple of javascript rgba color strings."""
        red, green, blue = random.randint(0, 255), random.randint(0, 255), random.randint(0, 150)
        return (
         'rgba(%s, %s, %s, .4)' % (red, green, blue),
         'rgba(%s, %s, %s, 1)' % (red, green, blue))

    def to_string(self):
        """
                This method is meant to be overridden in the child chart type classes
                """
        raise Exception('to_string method has not been overridden')