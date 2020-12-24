# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.4/dist-packages/pynetics/gggp/main.py
# Compiled at: 2016-03-12 06:09:25
# Size of source mod 2**32: 2893 bytes
from pprint import pprint
from pynetics.gggp import grammar
awesome_grammar = grammar.Grammar(start_symbol='frase', productions=[
 grammar.Production('frase', grammar.And(grammar.Multiplier('sujeto', upper=1), 'predicado', grammar.Multiplier(grammar.And('conjuncion', grammar.Multiplier('sujeto', upper=1), 'predicado')))),
 grammar.Production('conjuncion', grammar.Or(('y', 4), ('o', 6))),
 grammar.Production('sujeto', grammar.Or('sujeto_masc', 'sujeto_fem')),
 grammar.Production('sujeto_masc', grammar.Or(grammar.And('el', 'nombre_comun_masc'), grammar.And(grammar.Multiplier('el', upper=1), 'nombre_propio_masc'))),
 grammar.Production('sujeto_fem', grammar.Or(grammar.And('la', 'nombre_comun_fem'), grammar.And(grammar.Multiplier('la', upper=1), 'nombre_propio_fem'))),
 grammar.Production('nombre_comun_masc', grammar.Or('chico', 'chatarrero', 'profesor', 'mutante', 'zombie')),
 grammar.Production('nombre_propio_masc', grammar.Or('Pepe', 'Paco Pil', 'Richal')),
 grammar.Production('nombre_comun_fem', grammar.Or('camionera', 'guitarrista', 'prestituta', 'tabernera')),
 grammar.Production('nombre_propio_fem', grammar.Or('Juani', 'Pepi', 'Lili')),
 grammar.Production('predicado', grammar.And('verbo', grammar.Multiplier('complemento', upper=1))),
 grammar.Production('verbo', grammar.Or('corre', 'habla', 'ríe', 'tiene', 'va', 'come', 'dice', 'canta', 'caga', 'mea', 'micciona', 'excreta', 'evacúa')),
 grammar.Production('complemento', grammar.Or('la comida', 'como puede', 'que se las pela', 'soy una rumbera', 'abriendo puertas', 'a las barricadas', 'algo', 'siempre', 'a dos manos'))])
pprint(' '.join(awesome_grammar.random_tree().word()))