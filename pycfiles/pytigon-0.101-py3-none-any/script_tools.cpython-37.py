# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sch/prj/setup/pytigon/pytigon/prj/_schtools/schsimplescripts/script_tools.py
# Compiled at: 2020-05-02 15:32:44
# Size of source mod 2**32: 650 bytes
from pytigon_lib.schdjangoext.django_ihtml import ihtml_to_html

def _transform_view(name, txt1, txt2):
    fun = ''
    for row in txt2.split('\n'):
        fun = fun + '    ' + row + '\n'

    x2 = 'def scripts_%s(request, argv):\n%s\n' % (name, fun)
    return txt1 + '\n' + x2


def _transform_template(txt):
    return ihtml_to_html(None, txt)


def decode_script(name, code):
    elements = code.split('===')
    if len(elements) >= 4:
        _form = elements[1]
        _view = _transform_view(name, elements[0], elements[2])
        _template = _transform_template(elements[3])
        return [_form, _view, _template]