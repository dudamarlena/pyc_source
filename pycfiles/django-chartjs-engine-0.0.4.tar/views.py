# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Jeff/Development/jrwillette/jrwillette/charts/views.py
# Compiled at: 2016-12-27 00:31:42
import random, json
from django.shortcuts import render
from django.template.loader import render_to_string

class Chart:
    """A base class for charts, init will store all the data needed for subclasses"""

    def __init__(self, chart_type=None, chart_name=None, options=None, chart_labels=None, datasets=None):
        """
                Setting all of the settings that will be needed in the charts subclasses
                """
        self.chart_type = chart_type
        self.chart_labels = chart_labels
        self.datasets = datasets
        self.chart_name = chart_name
        self.options = options
        if not all([self.chart_type, self.chart_name, self.options,
         self.chart_labels, self.datasets]):
            raise Exception('Chart class needs to have all keyword arguments specified')

    def random_color(self):
        """Generates a random javascript valid rgba color for each set in datasets
                return: tuple of javascript rgba color strings."""
        red, green, blue = random.randint(0, 255), random.randint(0, 255), random.randint(0, 150)
        return (
         'rgba(%s, %s, %s, .4)' % (red, green, blue),
         'rgba(%s, %s, %s, 1)' % (red, green, blue))

    def render_template(self):
        """
                This method is meant to be overridden in the child chart type classes
                """
        raise Exception('make_js method has not been overridden')


class LineChart(Chart):
    """
        Making the JSON data necessary for line charts.
        DOCS: http://www.chartjs.org/docs/#line-chart-introduction
        """

    def render_template(self):
        """Generating the javascript needed for a line chart."""
        self.options = {'scales': {'yAxes': [
                              {'ticks': {'beginAtZero': True}}]}}
        self.data = {'labels': self.chart_labels, 
           'datasets': []}
        self.colors = [ self.random_color() for sets in self.datasets ]
        for i, name in enumerate(self.datasets):
            self.data['datasets'].append({'label': name, 
               'fill': False, 
               'lineTension': 0.1, 
               'borderCapStyle': 'butt', 
               'borderDash': [], 'borderDashOffset': 0.0, 
               'borderJoinStyle': 'miter', 
               'pointBorderColor': 'rgba(75,192,192,1)', 
               'pointBackgroundColor': '#fff', 
               'pointBorderWidth': 1, 
               'pointHoverRadius': 5, 
               'pointHoverBackgroundColor': 'rgba(75,192,192,1)', 
               'pointHoverBorderColor': 'rgba(220,220,220,1)', 
               'pointHoverBorderWidth': 2, 
               'pointRadius': 1, 
               'pointHitRadius': 10, 
               'spanGaps': False, 
               'backgroundColor': self.colors[i][0], 
               'borderColor': self.colors[i][1], 
               'data': self.datasets[name]})

        self.context = {'chart_type': self.chart_type, 
           'chart_name': self.chart_name, 
           'data': json.dumps(self.data), 
           'options': json.dumps(self.options)}
        return render_to_string('charts/chart.html', self.context)


class BarChart(Chart):
    """
        Making the JSON data necessary for a bar chart
        DOCS: http://www.chartjs.org/docs/#bar-chart-introduction
        """

    def render_template(self):
        """Rendering bar chart data to a template"""
        self.options = {'scales': {'yAxes': [
                              {'ticks': {'beginAtZero': True}}]}}
        self.data = {'labels': self.chart_labels, 
           'datasets': []}
        for i, name in enumerate(self.datasets):
            if len(self.datasets) == 1:
                self.colors = [ self.random_color() for d in self.datasets[name] ]
            else:
                self.rand_color = self.random_color()
                self.colors = [ self.rand_color for d in self.datasets[name] ]
            self.data['datasets'].append({'label': name, 
               'backgroundColor': [ color[0] for color in self.colors ], 'borderColor': [ color[1] for color in self.colors ], 'borderWidth': 3, 
               'data': self.datasets[name]})

        self.context = {'chart_type': self.chart_type, 
           'chart_name': self.chart_name, 
           'data': json.dumps(self.data), 
           'options': json.dumps(self.options)}
        return render_to_string('charts/chart.html', self.context)


class PieDoughnutChart(Chart):
    """
        Making the JSON necessary for a pie or doughnut chart
        DOCS: http://www.chartjs.org/docs/#doughnut-pie-chart-introduction
        """

    def render_template(self):
        """Rendering pie or doughnut chart data to a template"""
        self.data = {'labels': self.chart_labels, 
           'datasets': []}
        for i, name in enumerate(self.datasets):
            if len(self.datasets) == 1:
                self.colors = [ self.random_color() for d in self.datasets[name] ]
            else:
                self.error = 'Pie/Doughnut charts support one dataset at this time'
                return self.error
            self.data['datasets'].append({'label': name, 
               'backgroundColor': [ color[0] for color in self.colors ], 'hoverBackGroundColor': [ color[1] for color in self.colors ], 'borderWidth': 3, 
               'data': self.datasets[name]})

        self.context = {'chart_type': self.chart_type, 
           'chart_name': self.chart_name, 
           'data': json.dumps(self.data), 
           'options': json.dumps(self.options)}
        return render_to_string('charts/chart.html', self.context)


class ChartEngine(object):
    """An engine to make all of the charts necessary"""

    def __init__(self, **kwargs):
        """take in chart options and decide what kind of chart to make"""
        charts = {'line': LineChart, 
           'bar': BarChart, 
           'pie': PieDoughnutChart, 
           'doughnut': PieDoughnutChart}
        self.chart = charts[kwargs['chart_type']](chart_name=kwargs['chart_name'], chart_type=kwargs['chart_type'], chart_labels=kwargs['chart_labels'], options=kwargs['options'], datasets=kwargs['datasets'])

    def make_chart(self):
        """Render the proper chart from the given"""
        return self.chart.render_template()