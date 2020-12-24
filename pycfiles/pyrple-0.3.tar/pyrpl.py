# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyrpl/pyrpl.py
# Compiled at: 2017-08-29 09:44:06
__doc__ = ' # DEPRECATED DOCSTRING - KEEP UNTIL DOCUMENTATION IS READY\npyrpl.py - high-level lockbox functionality\n\nA lockbox is a device that converts a number of input signals into a number of\noutput signals suitable to stabilize a physical system in a desired state. This\ntask is generally divided into two steps:\n1) bring the system close the desired state where it can be linearized\n2) keep it there using linear control.\n\nThe task is further divided into several subtasks:\n0a) Condition the input signals so that they are suitable for the next steps\n - offset removal\n - input filters\n - demodulation / lockin\n - inversion\n0b) Estimate the system state from the past and present history of input and\noutput signals.\n0c) Build a filter for the output signals such that they can be conveniently\naddressed with higher-level lockbox logic.\n\n1) As above: apply reasonable action to the outputs to approach the system to\nthe desired state. We generally call this the \'search\' step.\n- provide a number of algorithms/recipes to do this\n\n2) As above: Turn on linear feedback. We call this the \'lock\' step.\n- connect the input signals with appropriate gain to the outputs\n- the gain depends on the state of the system, so internal state representation\nwill remain useful here\n\nThis naturally divides the lockbox object into 3 subcomponents:\na) inputs\nb) internal model\nc) outputs\n\nwhich will be interconnected by the algorithms that come with the model and\nmake optimal use of the available inputs and outputs. The job of the\nconfiguration file is to provide a maximum of information about the inputs,\noutputs and the physical system (=internal model) so that the lockbox is\neffective and robust. The lockbox will usually require both a coarse-tuning\nand an optimization step for optimum performance, which will both adjust the\nvarious parameters for the best match between model and real system.\n\nLet\'s make this reasoning more clear with an example:\n\nA Fabry-Perot cavity is to be locked near resonance using a PDH scheme. The\nincident laser beam goes through a phase modulator. The cavity contains a piezo\nwith estimated bandwidth 10 kHz (appearance of first resonance) and\na displacement of 350 nm/V that goes into the piezo amplifier. To limit the\neffect of amplifier noise, we have inserted an RC lowpass between amplifier and\npiezo with a cutoff frequency of 100 Hz. The laser contains another piezo with\nestimated bandwidth of 50 kHz that changes the laser frequency by 5 MHz/V. An\nRC filter provides a lowpass with 1kHz cutoff. Finally, the cavity can be tuned\nthrough its temperature with a bandwidth slower than 0.1 Hz. We estimate from\nthermal expansion coefficients that 1 V to the Peltier amplifier leading to 3 K\nheating of the cavity spacer should lead to 30ppm/K*20cm*3K/V = 18 micron/V\nlength change. Both reflection and transmission of the cavity are available\nerror signals. The finesse of the cavity is 5000, and therefore there are\nlarge regions of output signals where no useful error signal can be obtained.\n\nWe first generate a clean list of available inputs and outputs and some\nparameters of the cavity that we know already:\n\ninputs:\n  in1:\n    reflection\n  in2:\n    transmission\n  # also possible\n  # in2: pdh # for externally generated pdh\noutputs:\n  out1:\n    # we insert a bias-T with separation frequency around 1 MHz behind out1\n    # this allows us to use the fast output for both the piezo and PDH\n    modulator:\n      amplitude: 0.1\n      frequency: 50e6\n    cavitypiezo:\n      # piezo specification: 7 micron/1000V\n      # amplifier gain: 50\n      # therefore effective DC gain: 350nm/V\n      m_per_V: 350e-9\n      bandwidth: 100.0\n  out2:\n    laserpiezo:\n      Hz_per_V: 5e6\n      bandwidth: 1e3\n  pwm1:\n    temperature:\n      m_per_V: 18e-6\n      bandwidth: 0.1\nmodel:\n  type: fabryperot\n  wavelength: 1064e-9\n  finesse: 5000\n  # round-trip length in m (= twice the length for ordinary Fabry-Perot)\n  length: 0.72\n  lock: # lock methods in order of preferrence\n    order:\n      pdh\n      reflection\n      transmission\n    # when approaching a resonance, we can either abruptly jump or smoothly\n    # ramp from one error signal to another. We specify our preferrence with\n    # the order of keywords after transition\n    transition: [ramp, jump]\n    # target value for our lock. The API provides many ways to adjust this at\n    # runtime\n    target:\n      detuning: 0\n  # search algorithms to use in order of preferrence, as available in model\n  search:\n    drift\n    bounce\n\nHaving selected fabryperot as modeltype, the code will automatically search\nfor a class named fabryperot in the file model.py to provide for the internal\nstate representation and all algorithms. You can create your own model by\nadding other classes to this file, or by inheriting from existing ones and\nadding further functionality. The naming of all other configuration parameters\nis linked to the model, since all functionality that makes use of these para-\nmeters is implemented there. Another very often used model type is\n"interferometer". The only difference is here that\n\n'
from __future__ import print_function
import logging, os, os.path as osp
from shutil import copyfile
from qtpy import QtCore, QtWidgets
from .widgets.pyrpl_widget import PyrplWidget
from . import software_modules
from .memory import MemoryTree
from .redpitaya import RedPitaya
from . import pyrpl_utils
from .software_modules import get_module
from .async_utils import sleep as async_sleep
from .software_modules import lockbox
from .software_modules.lockbox import models
from . import user_config_dir
try:
    raw_input
except NameError:
    raw_input = input

try:
    basestring
except:
    basestring = (
     str, bytes)

default_pyrpl_config = {'name': 'default_pyrpl_instance', 'gui': True, 
   'loglevel': 'info', 
   'background_color': '', 
   'modules': [
             'NetworkAnalyzer',
             'SpectrumAnalyzer',
             'CurveViewer',
             'PyrplConfig',
             'Lockbox']}

class Pyrpl(object):
    """
    Higher level object, in charge of loading the right hardware and software
    module, depending on the configuration described in a config file.

    Parameters
    ----------
    config: str
        Name of the config file. No .yml extension is needed. The file
        should be located in the config directory.
    source: str
        If None, it is ignored. Else, the file 'source' is taken as a
        template config file and copied to 'config' if that file does
        not exist.
    **kwargs: dict
        Additional arguments can be passed and will be written to the
        redpitaya branch of the config file. See class definition of
        RedPitaya for possible keywords.
    """

    def __init__(self, config=None, source=None, **kwargs):
        self.logger = logging.getLogger(name='pyrpl')
        gui = 'gui' not in kwargs or kwargs['gui']
        if config is None:
            if gui:
                self.logger.info('Please select or create a configuration file in the file selector window!')
                config = QtWidgets.QFileDialog.getSaveFileName(directory=user_config_dir, caption="Pick or create a configuration file, or hit 'cancel' for no file (all configuration will be discarded after restarting)!", options=QtWidgets.QFileDialog.DontConfirmOverwrite, filter='*.yml')
                if not isinstance(config, basestring):
                    config = config[0]
            else:
                configfiles = [ name for name in os.listdir(user_config_dir) if name.endswith('.yml')
                              ]
                configfiles = [ name[:-4] if name.endswith('.yml') else name for name in configfiles
                              ]
                print('Existing config files are:')
                for name in configfiles:
                    print('    %s' % name)

                config = raw_input('\nEnter an existing or new config file name: ')
        if config is None or config == '' or config.endswith('/.yml'):
            config = None
        self.c = MemoryTree(filename=config, source=source)
        if self.c._filename is not None:
            self.logger.info('All your PyRPL settings will be saved to the config file\n    %s\nIf you would like to restart PyRPL with these settings, type "pyrpl.exe %s" in a windows terminal or \n    from pyrpl import Pyrpl\n    p = Pyrpl(\'%s\')\nin a python terminal.', self.c._filename, self.c._filename_stripped, self.c._filename_stripped)
        pyrplbranch = self.c._get_or_create('pyrpl')
        for k in default_pyrpl_config:
            if k not in pyrplbranch._keys():
                if k == 'name':
                    pyrplbranch[k] = self.c._filename_stripped
                else:
                    pyrplbranch[k] = default_pyrpl_config[k]

        pyrpl_utils.setloglevel(level=self.c.pyrpl.loglevel, loggername='pyrpl')
        self.c._get_or_create('redpitaya')
        self.c.redpitaya._update(kwargs)
        self.name = pyrplbranch.name
        self.rp = RedPitaya(config=self.c)
        self.rp.parent = self
        self.widgets = []
        self.load_software_modules()
        for module in self.software_modules + self.hardware_modules:
            if module.owner is None:
                module._load_setup_attributes()

        if self.c.pyrpl.gui:
            self.show_gui()
        return

    def show_gui(self):
        if len(self.widgets) == 0:
            widget = self._create_widget()
            widget.show()
        else:
            for w in self.widgets:
                w.show()

    def hide_gui(self):
        for w in self.widgets:
            w.hide()

    def load_software_modules(self):
        """
        load all software modules defined as root element of the config file.
        """
        self.software_modules = []
        soft_mod_names = [
         'Asgs', 'Iqs', 'Pids', 'Scopes', 'Iirs', 'Trigs'] + self.c.pyrpl.modules
        module_classes = [ get_module(cls_name) for cls_name in soft_mod_names
                         ]
        module_names = pyrpl_utils.get_unique_name_list_from_class_list(module_classes)
        for cls, name in zip(module_classes, module_names):
            try:
                if hasattr(cls, '_make_' + cls.__name__):
                    module = getattr(cls, '_make_' + cls.__name__)(self, name)
                else:
                    module = cls(self, name)
            except BaseException as e:
                self.logger.error('Something went wrong when loading the software module "%s": %s', name, e)
                raise e
            else:
                setattr(self, module.name, module)
                self.software_modules.append(module)
                self.logger.debug('Created software module %s', name)

    @property
    def hardware_modules(self):
        """
        List of all hardware modules loaded in this configuration.
        """
        if self.rp is not None:
            return list(self.rp.modules.values())
        else:
            return []
            return

    @property
    def modules(self):
        return self.hardware_modules + self.software_modules

    def _create_widget(self):
        """
        Creates the top-level widget
        """
        widget = PyrplWidget(self)
        self.widgets.append(widget)
        return widget

    def _clear(self):
        """
        kill all timers and closes the connection to the redpitaya
        """
        for module in self.modules:
            module._clear()

        for widget in self.widgets:
            widget._clear()

        while len(self.widgets) > 0:
            w = self.widgets.pop()
            del w

        async_sleep(0.1)
        self.c._write_to_file()
        self.rp.end_all()
        async_sleep(0.1)