# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/extfile/namechooser/metaconfigure.py
# Compiled at: 2012-06-20 11:22:54
__docformat__ = 'restructuredtext'
from ztfy.extfile.namechooser.interfaces import IExtFileNameChooserConfig
from zope.component import queryUtility
from zope.component.zcml import utility
from config import ExtFileConfig

def configureExtFileNameChooser(temp_path, base_path, chooser, name=''):
    config = queryUtility(IExtFileNameChooserConfig, name)
    if config is not None:
        config.path = temp_path
        config.base_path = base_path
        config.chooser = chooser()
    return


def config(context, temp_path, base_path, chooser, name=''):
    utility(context, IExtFileNameChooserConfig, factory=ExtFileConfig, name=name)
    context.action(discriminator=('onf.component.extfile', 'config', name), callable=configureExtFileNameChooser, args=(
     temp_path, base_path, chooser, name))