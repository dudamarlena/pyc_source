# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/kss/plugin/cns/plugins/autocomplete.py
# Compiled at: 2008-12-14 04:09:28


def autocomplete_escape(disp_list):
    esc_vocab = [ v.replace("'", "\\'") for v in disp_list.values() ]
    return "'" + ("','").join(esc_vocab) + "'"