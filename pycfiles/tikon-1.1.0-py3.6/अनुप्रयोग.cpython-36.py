# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tikon\Interfaz\अनुप्रयोग.py
# Compiled at: 2017-09-07 13:58:50
# Size of source mod 2**32: 534 bytes
import डिब्बा
डिब्बा_शुरू = डिब्बा.caja()
botón_inic = डिब्बा.botón()
botón_ayuda = डिब्बा.botón()
logo = डिब्बा.चित्र('')
डिब्बा_शुरू.जोड़ना(logo)
डिब्बा_शुरू.जोड़ना(botón_ayuda, texto='', acción='')
डिब्बा_शुरू.जोड़ना(botón_inic, texto='', acción=(lambda : डिब्बा_शुरू.हटाना('उपर')))