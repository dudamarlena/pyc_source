# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyrpl/software_modules/curve_viewer.py
# Compiled at: 2017-08-29 09:44:06
import logging
logger = logging.getLogger(name=__name__)
from ..attributes import SelectProperty, StringProperty, TextProperty, CurveProperty, CurveSelectProperty, CurveSelectListProperty
from ..memory import MemoryTree
from ..modules import Module
from ..widgets.module_widgets.curve_viewer_widget import CurveViewerWidget
from ..curvedb import CurveDB
MAX_CURVES = 100

def all_curves(instance=None):
    return CurveDB.all()[:MAX_CURVES]


class CurveViewer(Module):
    """
    This Module allows to browse through curves that were taken with pyrpl
    """
    _widget_class = CurveViewerWidget
    _gui_attributes = ['curve_name', 'pk', 'curve', 'params', 'save_params',
     'delete_curve', 'refresh_curve_list']
    pk = CurveSelectListProperty(doc='the pk of the currently viewed curve', call_setup=True)
    curve = CurveProperty(default=None, show_childs=True)
    params = TextProperty()
    curve_name = StringProperty(doc='Name of the currently viewed curve')

    def _setup(self):
        self.m = MemoryTree()
        self.curve = self.pk
        if self._curve_object is None:
            self.params = ''
            self.curve_name = ''
        else:
            self.params = self.m._get_yml(self._curve_object.params)
            self.curve_name = self._curve_object.params['name']
        return

    def save_params(self):
        self.m = MemoryTree()
        self.m._set_yml(self.params)
        if self._curve_object is not None:
            self._curve_object.params = self.self.m._data
            self._curve_object.save()
        return

    def delete_curve(self):
        if self._curve_object is not None:
            self._logger.info('Curve with id %s will be deleted!', self._curve_object.pk)
            del_pk = self._curve_object.pk
            del_index = self.pk_options.index(del_pk)
            self._curve_object.delete()
            new_options = list(self.__class__.pk.options(self).keys())
            new_index = max(0, min(del_index, len(new_options) - 2))
            new_option = new_options[new_index]
            if new_option != del_pk:
                self.pk = new_option
        return

    def refresh_curve_list(self):
        self.__class__.pk.options(self)