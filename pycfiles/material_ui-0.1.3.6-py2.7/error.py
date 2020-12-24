# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/material_ui/navigation/error.py
# Compiled at: 2015-03-09 18:59:02
import sys
sys.path.append('..')
from kivy.app import App
from kivy.atlas import Atlas
from kivy.cache import Cache
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import *
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from material_ui.navigation.form import Form
from pkg_resources import resource_filename
path = resource_filename(__name__, 'error.kv')
icon = resource_filename(__name__, 'images/awsnap.png')
Builder.load_file(path)

class ErrorForm(Form):
    texth1 = StringProperty('Generic error')
    texth2 = StringProperty("We're sorry, but this is bad :(")
    strace = StringProperty('')
    icon = StringProperty(icon)
    details = StringProperty('\nIf you see this page the software got an error and causes are unknown.\n')

    def __init__(self, **kargs):
        super(ErrorForm, self).__init__(**kargs)
        if 'title' not in kargs.keys():
            self.title = 'Generic Error'