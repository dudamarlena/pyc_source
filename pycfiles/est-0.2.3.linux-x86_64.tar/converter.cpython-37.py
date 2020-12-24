# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/est_venv/lib/python3.7/site-packages/orangecontrib/est/widgets/utils/converter.py
# Compiled at: 2020-03-05 02:52:24
# Size of source mod 2**32: 2677 bytes
__authors__ = [
 'H. Payno']
__license__ = 'MIT'
__date__ = '08/08/2019'
from Orange.widgets.widget import OWWidget
from Orange.widgets.widget import Input, Output
from est.core.types import XASObject
from orangecontrib.est.utils import Converter
import Orange.data

class ConverterOW(OWWidget):
    __doc__ = '\n    Offer a conversion from XASObject to Orange.data.Table, commonly used\n    from Orange widget\n    '
    name = 'converter xas_obj -> Table'
    id = 'orange.widgets.xas.utils.converter'
    description = 'convert a XASObject to a Orange.data.Table'
    icon = 'icons/converter.png'
    priority = 5
    category = 'esrfWidgets'
    keywords = ['spectroscopy', 'signal', 'output', 'file']
    want_main_area = False
    resizing_enabled = False

    class Inputs:
        xas_obj = Input('xas_obj', XASObject, default=True)

    class Outputs:
        res_data_table = Output('Data', Orange.data.Table)

    @Inputs.xas_obj
    def process(self, xas_object):
        if xas_object is None:
            return
        data_table = Converter.toDataTable(xas_object=xas_object)
        self.Outputs.res_data_table.send(data_table)