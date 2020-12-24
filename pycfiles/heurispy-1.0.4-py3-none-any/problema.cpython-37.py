# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\esuka\PycharmProjects\HeurisPy\heurispy\problema.py
# Compiled at: 2019-08-01 11:50:34
# Size of source mod 2**32: 2831 bytes
"""
 Copyright 2019, LANIA, A.C.

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""
from numbers import Number
from collections import Iterable

class Problema:
    __doc__ = '\n    Esta clase se encarga del manejo de las funciones que el usuiaro defina para plantear su\n    problema de optimización discreta.\n    '

    def __init__(self, dominio, funcion_objetivo, funcion_variacion_soluciones):
        self.solucion_inicial = None
        self.dominio = dominio
        self.cambia_solucion = funcion_variacion_soluciones
        self.funcion_objetivo = funcion_objetivo
        if not (callable(self.dominio) and callable(self.cambia_solucion) and callable(self.funcion_objetivo)):
            raise Exception('El problema de optimización no utiliza métodos para funcionar.')

    def __getstate__(self):
        return self.__dict__

    def genera_solucion(self):
        self.solucion_inicial = self.dominio()

    def comrpueba_problema(self):
        try:
            solucion_prueba = self.dominio()
            if not isinstance(solucion_prueba, Iterable):
                raise Exception('La solución no es discreta.')
            instancia_solucion_prueba = type(solucion_prueba)
            solucion_variada_prueba = self.cambia_solucion(solucion_prueba)
            if not isinstance(solucion_variada_prueba, Iterable):
                raise Exception('La solución no es discreta.')
            if not isinstance(solucion_variada_prueba, instancia_solucion_prueba):
                raise Exception('La solución variada no es del tipo de la solución original.')
            resultado_solucion_prueba = self.funcion_objetivo(solucion_prueba)
            resultado_solucion_variada_prueba = self.funcion_objetivo(solucion_variada_prueba)
            if not isinstance(resultado_solucion_prueba, Number):
                raise Exception('La función evaluada con la primer solución no regresa un número.')
            if not isinstance(resultado_solucion_variada_prueba, Number):
                raise Exception('La función evaluada con la solución variada no regresa un número.')
        except Exception as err:
            try:
                print(err.args[0])
            finally:
                err = None
                del err

        else:
            print('El p.o.d. está bien planteado.')