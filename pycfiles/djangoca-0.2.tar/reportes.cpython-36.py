# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\Archivos\Proyectos\Developer.pe\proyectos\base_django\aplicaciones\base\reportes.py
# Compiled at: 2019-07-22 00:05:00
# Size of source mod 2**32: 735 bytes
import time
from openpyxl import Workbook
from django.http.response import HttpResponse
from openpyxl.styles import Alignment
from openpyxl.styles import Border
from openpyxl.styles import Font
from openpyxl.styles import PatternFill
from openpyxl.styles import Side
from django.views.generic.base import View
from decimal import Decimal
from django.shortcuts import render
from .base_reportes import FormatoReporteExcel

class ReporteExcel(View):
    _model_name = ''
    _app_name = ''

    def get(self, request, *args, **kwargs):
        formato = FormatoReporteExcel(self._app_name, self._model_name)
        formato.cabecera_tabla_reporte_excel()
        formato.pintar_valores_excel()
        return formato.obtener_reporte_excel()