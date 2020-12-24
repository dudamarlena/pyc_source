# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ben/dev/signalbox/ask/models/custom_widgets.py
# Compiled at: 2014-08-27 19:26:12
"""Customised widgets for use in Askers."""
import django, floppyforms

class InstructionWidget(floppyforms.widgets.HiddenInput):
    input_type = 'hidden'
    is_hidden = False


class InlineRadioSelect(floppyforms.widgets.RadioSelect):
    template_name = 'floppyforms/widgets/radio-list-inline.html'


class SliderInput(floppyforms.widgets.HiddenInput):
    template_name = 'floppyforms/widgets/slider.html'
    is_hidden = False


class RangeSliderInput(floppyforms.widgets.HiddenInput):
    template_name = 'floppyforms/widgets/range-slider.html'
    is_hidden = False


class InlineCheckboxSelectMultiple(floppyforms.widgets.CheckboxSelectMultiple):
    template_name = 'floppyforms/widgets/checkbox-list-inline.html'


class WebcamWidget(floppyforms.widgets.HiddenInput):
    template_name = 'floppyforms/widgets/webcam.html'
    input_type = 'hidden'
    is_hidden = False