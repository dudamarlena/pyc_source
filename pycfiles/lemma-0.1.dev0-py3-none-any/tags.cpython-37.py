# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jovyan/lemma/lemma/tags.hy
# Compiled at: 2020-04-05 16:31:26
# Size of source mod 2**32: 464 bytes
from hy import HyExpression, HySymbol
from lemma.lang import LeOperator, gen_latex, gen_hy
bare = LeOperator(lambda body: LatexString(gen_latex(body), 0), lambda body: gen_hy(body))
bare.name = 'bare'
parens = LeOperator(lambda body: latexstr('\\left(' + gen_latex(body) + '\\right)', 0), lambda body: gen_hy(body))
parens.name = 'parens'
import hy
hy.macros.tag('b')(lambda form: HyExpression([] + [HySymbol('do')] + [
 HyExpression([] + [HySymbol('quote')] + [HyExpression([] + [bare] + [HyExpression([] + [HySymbol('quote')] + [form])])])]))
import hy
hy.macros.tag('p')(lambda form: HyExpression([] + [HySymbol('do')] + [
 HyExpression([] + [HySymbol('quote')] + [HyExpression([] + [parens] + [HyExpression([] + [HySymbol('quote')] + [form])])])]))