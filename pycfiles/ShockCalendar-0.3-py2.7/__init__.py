# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\ShockCalendar\__init__.py
# Compiled at: 2016-12-28 23:35:27
"""

Calendar.py para usar como modulo en Tkinter

Descripcion y funcionalidad:
 Un calendario que muestra dias de meses, la fecha actual,
 incluye funciones utiles para seleccionar fechas, marcar eventos,
 recuperar seleccion, eventos...
 
 El usuario puede elegir fechas, y la aplicacion puede recuperar esa
 seleccion con metodos del objeto Calendar.

 Ademas, se puede marcar una fecha (evento) la cual sera
 una fecha con informacion que sera marcada en color para el usuario.

 El usuario puede recorrer los meses con botones hacia atras '<' o hacia adelante '>'.
 Ademas de esos botones, tambien puede cambiar de mes seleccionando dias de antes o dias
 despues del mes mostrado.

 Se puede modificar el diccionario "colors" antes de crear la instancia Calendar
 para mostrar un calendario con otros colores. Asi tambien se puede cambiar
 las variables "monthnames" y "days" por si fuese necesario pasar a otros idiomas.

Ejemplo:

from Tkinter import *;
import ShockCalendar;

win = Tk();
win.title("Test ShockCalendar");
win.geometry("330x250");

width, height = 170, 170;
cal = ShockCalendar.Calendar(win, width, height);
cal.place(x=0, y=0, width=width, height=height);

win.mainloop();

"""
from ShockCalendar import Calendar
from ShockCalendar import monthnames, days
from ShockCalendar import colors
__version__ = '0.3'
__author__ = 'adrian_leonardo_05@hotmail.com.ar'
__license__ = 'MIT'