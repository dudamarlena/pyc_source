# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\esuka\PycharmProjects\HeurisPy\heurispy\heuristicas\heuristica.py
# Compiled at: 2019-10-20 15:32:02
# Size of source mod 2**32: 4328 bytes
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

class Heuristica:

    def __init__(self, problema, lista_nombres_parametros):
        self.nombre = None
        self.lista_nombres_parametros = lista_nombres_parametros
        self.problema_optimizacion = problema
        self.funcion_busqueda = None
        self._bandera_busqueda = False
        self._bandera_parada = False
        self.genera_pdf_final = None
        self.problema_optimizacion_validado = False
        self.contador_llamadas_funcion_objetivo = 0

        def funcion_con_contador(solucion):
            self.contador_llamadas_funcion_objetivo = self.contador_llamadas_funcion_objetivo + 1
            return self.problema_optimizacion.funcion_objetivo(solucion)

        self.funcion_objetivo = funcion_con_contador
        self.cambia_solucion = problema.cambia_solucion
        self.problema_optimizacion.comrpueba_problema()
        self.problema_optimizacion_validado = True

    def __getstate__(self):
        return self.__dict__

    def iniciar_busqueda(self, parametros):
        from time import time
        tiempo_inicial = time()
        if not self._bandera_busqueda:
            self._bandera_busqueda = True
        resultado = self.funcion_busqueda(parametros)
        resultado_tiempo = time() - tiempo_inicial
        diccionario_resultados = resultado[1]
        diccionario_resultados['tiempo_ejecucion'] = resultado_tiempo
        return resultado

    def interrumpir_busqueda(self):
        if self._bandera_busqueda:
            self._bandera_parada = True
        else:
            print('No se ha iniciado la búsqueda heurística')

    def comprobar_parametros(self, parametros):
        if len(parametros) > len(self.lista_nombres_parametros):
            print('Advertencia: Se tienen más parámetros de los necesarios.')
        contador_parametros_correctos = 0
        for i in range(len(self.lista_nombres_parametros)):
            if self.lista_nombres_parametros[i] in parametros:
                contador_parametros_correctos += 1

        if contador_parametros_correctos == len(self.lista_nombres_parametros):
            return True
        print('Los parámetros no son correctos')
        x = 1 / 0