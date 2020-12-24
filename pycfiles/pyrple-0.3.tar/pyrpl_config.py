# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyrpl/software_modules/pyrpl_config.py
# Compiled at: 2017-08-29 09:44:06
import logging
logger = logging.getLogger(name=__name__)
from ..attributes import SelectProperty, StringProperty, TextProperty
from ..memory import MemoryTree
from ..modules import Module
from ..widgets.module_widgets.pyrpl_config_widget import PyrplConfigWidget

class PyrplConfig(Module):
    """
    This Module allows the Gui to configure the global settins, such as redpitaya and pyrpl
    """
    _widget_class = PyrplConfigWidget
    _gui_attributes = ['configfile', 'module', 'refresh', 'save', 'text']
    configfile = StringProperty()

    def __init__(self, parent, name=None):
        super(PyrplConfig, self).__init__(parent, name=name)
        self.configfile = self.pyrpl.c._filename or ''

    text = TextProperty()
    module = SelectProperty(default='pyrpl', options=lambda inst: [
     'pyrpl', 'redpitaya'] + [ m.name for m in inst.pyrpl.software_modules ], doc='this selector allows to choose which module is configured', call_setup=True)

    @property
    def current_branch(self):
        if self.configfile == self.pyrpl.c._filename or self.configfile == '' and self.pyrpl.c._filename is None:
            self.config = self.pyrpl.c
        else:
            self._logger.info('Creating new MemoryTree for file %s...', self.configfile)
            self.config = MemoryTree(self.configfile)
        return self.config._get_or_create(self.module)

    def _setup(self):
        self.text = self.current_branch._get_yml()

    def save(self):
        self.current_branch._set_yml(self.text)
        try:
            module = getattr(self.pyrpl, self.module)
        except AttributeError:
            pass
        else:
            module._load_setup_attributes()

    def refresh(self):
        self._setup()