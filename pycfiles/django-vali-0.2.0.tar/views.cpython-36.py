# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/anyi/workspace/svn/xunjian_client/vali/views.py
# Compiled at: 2018-02-09 10:12:00
# Size of source mod 2**32: 2210 bytes
from django.shortcuts import render
from django.views.generic import TemplateView

class ValiDashboardView(TemplateView):
    template_name = 'vali/dashboard.html'
    top_icons = [
     {'title':'demo1', 
      'value':5,  'style':'primary',  'icon':'fa-users'},
     {'title':'demo2', 
      'value':15,  'style':'info',  'icon':'fa-thumbs-o-up'},
     {'title':'demo3', 
      'value':80,  'style':'warning',  'icon':'fa-files-o'},
     {'title':'demo4', 
      'value':500,  'style':'danger',  'icon':'fa-star'}]
    charts = [
     {'name':'linechart1', 
      'title':'linechart',  'type':'Line',  'labels':['2018-03-01', '2018-03-02', '2018-03-03', '2018-03-04', '2018-03-05'],  'datasets':[
       {'label':'dataset 1', 
        'fillColor':'rgba(220,220,220,0.2)', 
        'strokeColor':'rgba(220,220,220,1)', 
        'pointColor':'rgba(220,220,220,1)', 
        'pointStrokeColor':'#fff', 
        'pointHighlightFill':'#fff', 
        'pointHighlightStroke':'rgba(220,220,220,1)', 
        'data':[
         65, 59, 80, 81, 80]},
       {'label':'dataset 2', 
        'fillColor':'rgba(151,187,205,0.2)', 
        'strokeColor':'rgba(151,187,205,1)', 
        'pointColor':'rgba(151,187,205,1)', 
        'pointStrokeColor':'#fff', 
        'pointHighlightFill':'#fff', 
        'pointHighlightStroke':'rgba(151,187,205,1)', 
        'data':[
         28, 48, 40, 19, 69]}]},
     {'name':'piechart1', 
      'title':'piechart',  'type':'Pie',  'datasets':[
       {'value':300, 
        'color':'#46BFBD',  'highlight':'#5AD3D1',  'label':'progress'},
       {'value':50, 
        'color':'#F7464A',  'highlight':'#FF5A5E',  'label':'finish'}]}]

    def get_context_data(self, **kwargs):
        context = (super().get_context_data)(**kwargs)
        context['icons'] = self.top_icons
        context['charts'] = self.charts
        return context