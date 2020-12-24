# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jeanphix/www/Flask-Dashed/tests/flask_dashed/dashboard.py
# Compiled at: 2012-06-26 14:02:16
from admin import AdminModule
from views import DashboardView

class Dashboard(AdminModule):
    """A dashboard is a Widget holder usually used as admin entry point.
    """
    widgets = []

    @property
    def default_rules(self):
        return [
         ('/', 'show',
          DashboardView.as_view('dashboard', self))]


class DashboardWidget:
    """Dashboard widget builder.
    """

    def __init__(self, title):
        """Initialize a new widget instance.

        :param title: The widget title
        """
        self.title = title

    def render(self):
        """Returns html content to display.
        """
        raise NotImplementedError()


class HelloWorldWidget(DashboardWidget):

    def render(self):
        return '<p>Hello world!</p>'


class DefaultDashboard(Dashboard):
    """Default dashboard."""
    widgets = [
     HelloWorldWidget('my first dashboard widget')]