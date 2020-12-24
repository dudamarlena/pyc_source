# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/ks/captcha/interfaces.py
# Compiled at: 2008-12-22 08:21:48
"""Interfaces for the Zope 3 based captcha package

$Id: interfaces.py 35228 2007-11-28 10:54:43Z anton $
"""
__author__ = ''
__license__ = '<undefined>'
__version__ = '$Revision: 35228 $'
__date__ = '$Date: 2007-11-28 12:54:43 +0200 (Wed, 28 Nov 2007) $'
from zope.interface import Interface
from zope.schema import Text, TextLine, Int
from zope.app.container.interfaces import IContained, IContainer
from zope.app.container.constraints import ItemTypePrecondition
from zope.app.container.constraints import ContainerTypesConstraint

class ICaptcha(Interface):
    __module__ = __name__
    width = Int(title='Image width', description='', min=0, max=1280, default=100)
    height = Int(title='Image height', description='', min=0, max=1024, default=100)
    noise = Int(title='Noise level', description='', min=0, max=100, default=20)
    secret = Int(title='Shared Secret', description='', default=2925)
    fontsize = Int(title='Font Size', description='', default=20)
    font = TextLine(title='Full path to truetype Font', description='', default='verdanai.ttf')
    mode = TextLine(title='Image mode', description='', default='RGB')
    format = TextLine(title='Image format', description='', default='PNG')
    mimetype = TextLine(title='MimeType', description='', default='image/png')
    min = Int(title='Minimal Key', description='', default=1000)
    max = Int(title='Maximum Key', description='', default=9999)
    interval = Int(title='Key lifetime', description='', min=600, max=7200, default=3600)

    def banner(key):
        u""" Генерирует картинку, на которой изображён указанный в параметре key
            (слово, набор цифр или нечто подобное)
        """
        pass

    def decrypt(key):
        u""" Принимает ключ в зашифрованном виде, расшифровывает его и
            возвращает результат расшифровки
        """
        pass

    def check(key, x):
        u""" Проверяет, соответствуют ли данные, введённые пользователем,
            данным, изображённым на картинке
        """
        pass

    def getkey(self):
        u""" Получает случайный ключ
        """
        pass