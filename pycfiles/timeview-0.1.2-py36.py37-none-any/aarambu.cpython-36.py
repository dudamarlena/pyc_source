# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\tikon\Interfaz\aarambu.py
# Compiled at: 2017-08-25 13:07:47
# Size of source mod 2**32: 1130 bytes
import डिब्बा
பக்கம்_ஆரம்பு = डिब्बा.पन्ना.पन्ना()
botón_inic = डिब्बा.botón.botón_tx(texto='', acción=None, स्थान=(0.5, 0.4),
  आपेक्षिक_स्थान=True,
  माप=(10, 30),
  आपेक्षिक_माप=False)
botón_ayuda = डिब्बा.botón.botón_tx(texto='', acción=(lambda : பக்கம்_ஆரம்பு.हटाना('उपर')), स्थान=(0.5,
                                                                                                   0.4),
  आपेक्षिक_स्थान=True,
  माप=(10, 30),
  आपेक्षिक_माप=False)
logo = डिब्बा.कला.चित्र.चित्र("Logo_Tiko'n", स्थान=(0.5, 0.4), आपेक्षिक_स्थान=True, माप=(10,
                                                                                         30), आपेक्षिक_माप=False)
பக்கம்_ஆரம்பு.जोड़ना(logo)
பக்கம்_ஆரம்பு.जोड़ना(botón_ayuda)
பக்கம்_ஆரம்பு.जोड़ना(botón_inic)