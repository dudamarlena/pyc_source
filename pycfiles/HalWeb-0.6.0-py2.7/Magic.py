# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/halicea/baseProject/lib/halicea/Magic.py
# Compiled at: 2011-12-23 04:19:50
import conf.settings as settings, os

class MagicSet(object):

    @staticmethod
    def getControllerClass(mvcItemInstance):
        return mvcItemInstance.__class__

    @staticmethod
    def getModelClass(mvcItemInstance):
        moduleBase, nameBase = MagicSet.baseName(mvcItemInstance, splitParts=True)
        name = nameBase + settings.MODEL_CLASS_SUFIX
        module = os.path.basename(settings.MODELS_DIR) + '.' + moduleBase + settings.MODEL_MODULE_SUFIX
        exec 'from %s import %s as nc' % (module, name)
        return nc

    @staticmethod
    def getViewDir(mvcItemInstance):
        moduleBase, nameBase = MagicSet.baseName(mvcItemInstance, splitParts=True)
        return moduleBase.replace('.', os.sep)

    @staticmethod
    def getFormClass(mvcItemInstance):
        moduleBase, nameBase = MagicSet.baseName(mvcItemInstance, splitParts=True)
        moduleBase = os.path.basename(settings.FORM_MODELS_DIR) + '.' + moduleBase + settings.MODEL_FORM_MODULE_SUFIX
        nameBase = nameBase + settings.MODEL_FORM_CLASS_SUFIX
        m = __import__(moduleBase)
        return getattr(m, nameBase)

    @staticmethod
    def baseName(mvcItemInstance, splitParts=False):
        modPart = mvcItemInstance.__class__.__module__
        clsPart = mvcItemInstance.__class__.__name__
        for t in [settings.CONTROLLER_MODULE_SUFIX,
         settings.MODEL_MODULE_SUFIX,
         settings.MODEL_FORM_MODULE_SUFIX]:
            if t and modPart.endswith(t):
                modPart = modPart[:-len(t)]
                break

        for t in [settings.CONTROLLER_CLASS_SUFIX,
         settings.MODEL_CLASS_SUFIX,
         settings.MODEL_FORM_CLASS_SUFIX]:
            if t and clsPart.endswith(t):
                clsPart = clsPart[:-len(t)]
                break

        if splitParts:
            return (modPart[modPart.index('.') + 1:], clsPart)
        else:
            return modPart[modPart.index('.') + 1:] + '.' + clsPart