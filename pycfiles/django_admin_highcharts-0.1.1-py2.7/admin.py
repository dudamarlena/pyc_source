# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/admin_highcharts/admin.py
# Compiled at: 2015-06-03 02:54:27
from django.contrib import admin
from django.utils.translation import ugettext as _

class HighchartsModelAdmin(admin.ModelAdmin):

    class Media:
        js = ('admin_highcharts/js/jquery-2.0.2.js', 'admin_highcharts/js/highcharts.js',
              'admin_highcharts/js/exporting.js')

    @property
    def chart_option(self):
        return {'credits': False, 
           'lang': {'contextButtonTitle': _('contextButtonTitle'), 
                    'downloadJPEG': _('downloadJPEG'), 
                    'downloadPDF': _('downloadPDF'), 
                    'downloadPNG': _('downloadPNG'), 
                    'downloadSVG': _('downloadSVG'), 
                    'printChart': _('printChart')}}

    @property
    def change_list_template(self):
        return 'admin_highcharts/change_list.html'