# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/pypagseguro/retornotest.py
# Compiled at: 2011-01-06 19:06:57
import retorno, twill
b = twill.get_browser()
b._browser._factory.is_html = True
twill.browser = b
t = twill.shell.commands

def base(uri=''):
    return 'http://0.0.0.0:8080/' + uri


t.go(base())
t.fv(1, 'id', '1')
t.submit()
t.fv(2, 'submit', '')
t.submit('submit')
t.fv(1, 'TipoPagamento', 'Boleto')
t.fv(1, 'StatusTransacao', 'Aprovado')
t.submit()
t.show()