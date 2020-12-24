# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\pyhardware\drivers\visa\tds2024b.py
# Compiled at: 2013-12-04 10:19:43
"""module to interface the TDS2024b scope (using VISA interface)"""
from pyhardware.drivers.visa import VisaDriver
from pyhardware.utils.guiwrappersutils import GuiWrapper
from pyhardware.utils.gui_fetch_utils import FetcherMixin
from curve import Curve
from pyivi.ivicom.iviscope import ShortCutScope
from pandas import Series
import pandas, visa, numpy

class TDS2024B(VisaDriver, GuiWrapper, FetcherMixin):
    _supported_models = [
     'TDS 2024B']
    _fields = ShortCutScope._fields + ['channel_idx'] + ['sample_modes', 'acquisition_types', 'ch_couplings']

    def __init__(self, *args, **keys):
        super(TDS2024B, self).__init__(*args, **keys)
        GuiWrapper.__init__(self)
        self.channel_idx = 1

    def _setupUi(self, widget):
        """sets up the graphical user interface"""
        widget._setup_vertical_layout()
        widget._setup_horizontal_layout()
        widget._setup_vertical_layout()
        for field in self._fields:
            if field == 'channel_idx':
                widget._exit_layout()
                widget._setup_vertical_layout()
            choices = None
            if hasattr(self, field + 's'):
                choices = self.__getattribute__(field + 's')
            widget._setup_gui_element(field, choices)

        widget._exit_layout()
        widget._exit_layout()
        self._setup_fetch_buttons(widget)
        return

    def recall(self, filename='1'):
        self.write('RECAll:SETUp ' + str(filename))

    def acquire(self):
        self.write('ACQuire:STATE RUN')

    def autoset(self):
        self.write('AUTOSet EXECute')

    @property
    def record_length(self):
        return int(self.ask('HORizontal:RECOrdlength?'))

    @record_length.setter
    def record_length(self, length=2500):
        pass

    @property
    def number_of_averages(self):
        return int(self.ask('ACQuire:NUMAVg?'))

    @number_of_averages.setter
    def number_of_averages(self, val=2):
        self.write('ACQuire:NUMAVg ' + str(val))

    @property
    def acquisition_type(self):
        return self.ask('ACQuire:MODe?')

    @acquisition_type.setter
    def acquisition_type(self, val='SAMple'):
        self.write('ACQuire:MODe ' + val)

    @property
    def ch_coupling(self):
        return self.ask('CH' + str(self.channel_idx) + ':COUPling?')

    @ch_coupling.setter
    def ch_coupling(self, val='DC'):
        self.write('CH' + str(self.channel_idx) + ':COUPling ' + str(val))

    @property
    def ch_range(self):
        return float(self.ask('CH' + str(self.channel_idx) + ':VOLts?'))

    @ch_range.setter
    def ch_range(self, val=1.0):
        self.write('CH' + str(self.channel_idx) + ':VOLts ' + str(val))

    @property
    def time_per_record(self):
        return 10 * float(self.ask('HORizontal:MAIn:SCAle?'))

    @time_per_record.setter
    def time_per_record(self, val=0.1):
        self.write('HORizontal:MAIn:SCAle ' + str(val / 10))

    @property
    def ch_input_frequency_max(self):
        bw = self.ask('CH' + str(self.channel_idx) + ':BANdwidth?')
        if bw == 'OFF':
            return 1000000000.0
        else:
            return float(bw)

    @ch_input_frequency_max.setter
    def ch_input_frequency_max(self, val=1000000000.0):
        self.write('CH' + str(self.channel_idx) + ':BANdwidth ' + str(val))

    def easy_waveform(self, ch=1):
        self.write('DATa:WIDth 1')
        self.write('DATa:ENCdg RPBinary')
        self.write('DATa:STARt 1')
        self.write('DATa:STOP 2500')
        self.write('SELect:CH%i ON' % ch)
        self.write('DATa:SOUrce CH%i' % ch)
        self.write('WFMPre:PT_Fmt Y')
        YZEro = float(self.ask('WFMPRe:YZEro?'))
        YMUlt = float(self.ask('WFMPRe:YMUlt?'))
        YOFf = float(self.ask('WFMPRe:YOFf?'))
        XZEro = float(self.ask('WFMPRe:XZEro?'))
        XINcr = float(self.ask('WFMPRe:XINcr?'))
        PT_OFf = float(self.ask('WFMPRe:PT_OFf?'))
        NR_Pt = int(self.ask('WFMPRe:NR_Pt?'))
        preamble = self.ask('WFMPRe?')
        print preamble
        rawdata = map(ord, tuple(self.ask('CURVe?')[-NR_Pt:]))
        tcol = XZEro + XINcr * (Series(range(NR_Pt)) - PT_OFf)
        trace = YZEro + YMUlt * (Series(rawdata, index=tcol) - YOFf)
        return trace

    def fetch(self):
        self.write('DATa:WIDth 1')
        self.write('DATa:ENCdg RPBinary')
        self.write('DATa:STARt 1')
        points = 2500
        self.write('DATa:STOP ' + str(points))
        self.write('SELect:CH%i ON' % self.channel_idx)
        self.write('DATa:SOUrce CH%i' % self.channel_idx)
        self.write('WFMOutpre:PT_Fmt Y')
        YZEro = float(self.ask('WFMPRe:YZEro?'))
        YMUlt = float(self.ask('WFMPRe:YMUlt?'))
        YOFf = float(self.ask('WFMPRe:YOFf?'))
        XZEro = float(self.ask('WFMPRe:XZEro?'))
        XINcr = float(self.ask('WFMPRe:XINcr?'))
        PT_OFf = float(self.ask('WFMPRe:PT_OFf?'))
        NR_Pt = int(self.ask('WFMPRe:NR_Pt?'))
        tr = self.ask('CURVe?')
        offsetByte = int(tr[1]) + 2
        rawdata = numpy.frombuffer(tr, dtype='B', offset=offsetByte)
        tcol = XZEro + XINcr * (numpy.array(range(NR_Pt), dtype=float) - PT_OFf)
        trace = YZEro + YMUlt * (rawdata - YOFf)
        return (tcol, trace)

    def _get_curve(self):
        x_y = self.fetch()
        meta = dict()
        meta['name'] = 'scope_curve'
        meta['acquisition_type'] = self.acquisition_type
        meta['averaging'] = self.number_of_averages
        meta['time_per_record'] = self.time_per_record
        meta['record_length'] = self.record_length
        meta['coupling'] = self.ch_coupling
        meta['full_range'] = self.ch_range
        meta['input_freq_max'] = self.ch_input_frequency_max
        meta['channel'] = 'CH' + str(self.channel_idx)
        meta['curve_type'] = 'ScopeCurve'
        meta['instrument_logical_name'] = self.logical_name
        curve = Curve()
        curve.set_data(pandas.Series(x_y[1], index=x_y[0]))
        curve.set_params(**meta)
        return curve


if __name__ == '__main__':
    ea = TDS2024B(sys.argv[1])