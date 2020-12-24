# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/robograph/datamodel/tests/test_console_printer.py
# Compiled at: 2016-07-13 17:51:17
from robograph.datamodel.nodes.lib import printer

def test_requirements():
    expected = [
     'message']
    instance = printer.ConsolePrinter()
    assert instance.requirements == expected


def test_input():
    msg = 'Hello world'
    instance = printer.ConsolePrinter()
    instance.input(dict(message=msg))
    instance.set_output_label('any')
    assert instance.output() == msg


def test_output():
    msg = 'Hello world'
    instance = printer.ConsolePrinter(message=msg)
    instance.set_output_label('any')
    assert instance.output() == msg