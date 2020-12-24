# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyslo/sli.py
# Compiled at: 2020-04-02 17:00:28
# Size of source mod 2**32: 8692 bytes
__doc__ = "SLI contains the logic needed to computed SLI/SLO metrics.\n\nCalculate service level objective measurements from metrics stored\nin common backends in accordance with the logic set out in the\n[SRE Workbook](https://landing.google.com/sre/workbook/toc/)\n\nTypical usage example::\n\n    from google.cloud import monitoring_v3\n    from pyslo.metric_client.stackdriver import StackdriverMetricClient\n    from pyslo.sli import Sli\n\n    PROJECT = <MY_GCP_PROJECT>\n\n    metric_client = StackdriverMetricClient(project=PROJECT)\n    metric_client.metric_type = 'composer.googleapis.com/environment/healthy'\n    metric_client.resource_type = 'cloud_composer_environment'\n    metric_client.value_type = monitoring_v3.enums.MetricDescriptor.ValueType.BOOL\n\n    sli = Sli(metric_client)\n\n    sli.window_length = 1  # days\n    sli.slo = 0.99\n\n    sli.get_metric_data()\n\n    # Calculate sli/slo doing no group bys.\n    sli.calculate()\n    sli.error_budget()\n\n    # Group by some metric labels\n    sli.group_by_resource_labels = ['environment_name', 'project_id']\n    sli.group_by_metric_labels = ['image_version']\n\n    sli.calculate()\n    sli.error_budget()\n    print(sli.slo_data)\n"
import time
from datetime import datetime
import pytz
from google.cloud import monitoring_v3
import pandas as pd
from .metric_client import MetricClient
MetricDescriptor = monitoring_v3.enums.MetricDescriptor

class SliException:
    """SliException"""

    class ValueNotSet(Exception):
        """SliException.ValueNotSet"""
        pass

    class UnsupportedMetricType(Exception):
        """SliException.UnsupportedMetricType"""
        pass


class Sli:
    """Sli"""

    def __init__(self, metric_client=MetricClient()):
        self.metric_client = metric_client
        self.metric_data = None
        self.window_end = time.time()
        self.window_length = 0
        self.slo = None
        self.slo_data = None
        self.group_by_resource_labels = []
        self.group_by_metric_labels = []

    @property
    def group_by_labels(self):
        """Combine the metric and resource labels

        Returns:
            A list of the resource and metric labels to group by, based on
            combining group_by_resource_labels and group_by_metric_labels.
            During the combination of the lists, the label names are prepended,
            according to the prepend_key function in the associated metric client.
        """
        resource_labels = [self.metric_client.prepend_key(l, 'resource') for l in self.group_by_resource_labels]
        metric_labels = [self.metric_client.prepend_key(l, 'metric') for l in self.group_by_metric_labels]
        return resource_labels + metric_labels

    @staticmethod
    def days_to_seconds(days):
        """Convert days into seconds

        Args:
            days: number of days

        Returns:
            The corresponding number of seconds
        """
        return days * 24 * 60 * 60

    @property
    def window_length_seconds(self):
        """Access the window_length in seconds

        Returns:
            The window length, stored in days, as seconds
        """
        return Sli.days_to_seconds(self.window_length)

    @property
    def window_start(self):
        """Derive window start from end and duration

        Returns:
            The start of the window in seconds from epoch
        """
        return self.window_end - self.window_length_seconds

    def get_metric_data(self):
        """Retrieve metric data from the metric_client

        Returns:
            None. Assigns timeseries data to attribute metric_data
        """
        if self.window_length is None:
            raise SliException.ValueNotSet('window_length cannot be None')
        self.metric_data = self.metric_client.timeseries_dataframe(end=(self.window_end),
          duration=(self.window_length_seconds))

    def calculate(self):
        """Calculate SLI based on metric type

        Only boolean is supported right now
        Returns:
            None. Assigns the calculate slo data to attribute slo_data
        """
        if self.metric_client.value_type == MetricDescriptor.ValueType.BOOL:
            self.calc_bool()
            self.add_period()
            self.add_slo()
            return self.slo_data
        elif self.metric_client.value_type == 'Some other type':
            pass
        else:
            raise SliException.UnsupportedMetricType

    def calc_bool(self):
        """Run the bool calculation depending on presence of group bys

        Returns:
            Dataframe of SLO data. Attribute slo_data is also assigned return value
        """
        if len(self.group_by_metric_labels) > 0 or len(self.group_by_resource_labels) > 0:
            return self.calc_bool_agg()
        return self.calc_bool_simple()

    def calc_bool_agg(self):
        """Calculate sli aggregating over the columns in group_by_labels

        Returns:
            Dataframe of SLO data. Attribute slo_data is also assigned return value
        """
        good_events = self.metric_data.groupby(self.group_by_labels).sum().reset_index().rename(columns={'value': 'count_good'})
        valid_events = self.metric_data.groupby(self.group_by_labels).count().reset_index().rename(columns={'value': 'count_valid'})['count_valid']
        slo_data = good_events.merge(valid_events,
          how='left',
          left_index=True,
          right_index=True)
        slo_data['sli'] = slo_data['count_good'] / slo_data['count_valid']
        self.slo_data = slo_data
        return self.slo_data

    def calc_bool_simple(self):
        """Calculate sli over the entire dataframe with no aggregation by labels

        Returns:
            Dataframe of SLO data. Attribute slo_data is also assigned return value
        """
        valid_events = self.metric_data.shape[0]
        good_events = self.metric_data['value'].sum()
        self.slo_data = pd.DataFrame([
         {'count_good':good_events, 
          'count_valid':valid_events, 
          'sli':good_events / valid_events}])
        return self.slo_data

    def error_budget(self):
        """Calculate error budgets

        Using previously calculated good event and valid event count,
        return the error budget, and budget remaining.

        Returns:
            Dataframe of SLO data that now includes error budget.
            Also adds error budget to attribute slo_data

        Raises:
            SliException.ValueNotSet if slo is not defined already
        """
        if not self.slo:
            raise SliException.ValueNotSet('slo has not been defined')
        data = self.slo_data
        data['error_budget'] = data['count_valid'] * (1 - self.slo)
        data['error_budget_remaining'] = data['error_budget'] - (data['count_valid'] - data['count_good'])
        self.slo_data = data
        return data

    def add_period(self):
        """Add the period_from and period_to to the slo_data attribute

        Returns:
            None
        """
        self.slo_data['period_from'] = datetime.fromtimestamp((self.window_end - self.window_length_seconds),
          tz=(pytz.UTC))
        self.slo_data['period_to'] = datetime.fromtimestamp((self.window_end), tz=(pytz.UTC))

    def add_slo(self):
        """Add the slo value to the slo_data attribute

        Returns:
            None
        """
        self.slo_data['slo'] = self.slo