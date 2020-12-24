# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\ResultDashboard\Dashboard\CIFFDashboard.py
# Compiled at: 2020-03-15 13:03:53
# Size of source mod 2**32: 2914 bytes
"""
author: Kapil Duwadi
version: 0.0.1
"""
from dash.dependencies import Input, Output, State
import dash_html_components as html
from ResultDashboard.Dashboard.DashContent import *
from ResultDashboard.Dashboard.DistMetricPVTab import *
from ResultDashboard.Dashboard.PVConnectionTab import *
from ResultDashboard.Dashboard.DistMetricTabAdvancedPV import *
from ResultDashboard.Dashboard.InitialAssessmentTab import *

class CreateApp:

    def __init__(self, app, DashboardSettings, DataObject, PVDataObject, InitialAssessmentObject):
        self.app = app
        self.DataObject = DataObject
        self.DataObjectforAdvancedPV = PVDataObject
        self.InitialAssessmentObject = InitialAssessmentObject
        self.DashboardSettings = DashboardSettings
        self.DistMetricAdvancedPVObject = DistMetricAdvancedPVTab(self.app, self.DataObjectforAdvancedPV)
        self.DisMetricPVObject = DistMetricPVTab(self.app, self.DataObject)
        self.PVConnectionObject = PVConnectionTab(self.app, self.DataObject, self.DashboardSettings)
        self.InitialAssessmentObject = InitialAssessmentTab(self.app, self.InitialAssessmentObject)
        self.app.layout = html.Div(children=[
         self.TopBanner(),
         self.CreateTabs(),
         self.Content()])

    def Content(self):
        return html.Div(id='Tab-content', children=[])

    def Callbacks(self):
        self.UpdateOnTab()
        self.DisMetricPVObject.Callbacks()
        self.PVConnectionObject.Callbacks()
        self.InitialAssessmentObject.Callbacks()

    def UpdateOnTab(self):

        @self.app.callback(Output('Tab-content', 'children'), [Input('DashTab', 'value')])
        def Update_Render(tab):
            print(tab)
            if tab == 'Classical PV':
                return self.DisMetricPVObject.layout()
            if tab == 'PV Connection Request':
                return self.PVConnectionObject.layout()
            if tab == 'Advanced PV':
                return self.DistMetricAdvancedPVObject.layout()
            if tab == 'Initial Assessment':
                return self.InitialAssessmentObject.layout()

    def TopBanner(self):
        TopContent = '{} : Distribution System Analysis Dashboard'.format(self.DashboardSettings['Active Project'])
        BottomContent = 'Framework to visualize system level and asset level metrics to inform decision making '
        return Banner(self.app, TopContent, BottomContent, 'logo.png').layout()

    def CreateTabs(self):
        TabNames = [
         'Initial Assessment', 'PV Connection Request', 'Classical PV', 'Advanced PV', 'EV']
        return Tabs(TabNames, 'DashTab').layout()

    def layout(self):
        return self.app.layout