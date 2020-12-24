# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-intel/egg/snipsskills/models/skilldef.py
# Compiled at: 2017-10-30 11:57:58
""" Skill definition from a YAML config. """

class SkillDef:
    """ Skill definition from a YAML config. """

    def __init__(self, name, package_name, class_name, url, params, intent_defs, requires_tts, addons):
        """ Initialisation.

        :param name: skill name.
        :param package_name: the name of the Python module.
        :param class_name: the name of the Python class.
        :param url: the url package (name or url).
        :param params: the parameters to pass to the skills constructor.
        :param intent_defs: a list of intent definitions.
        :param requires_tts: whether the skill requires TTS.
        :param addons: addon modules.
        """
        self.name = name
        self.package_name = package_name
        self.class_name = class_name
        self.url = url
        self.params = params
        self.intent_defs = intent_defs
        self.requires_tts = requires_tts
        self.addons = addons

    def find(self, intent):
        """ Find an intent definition in the list of intents that the skill
            declares.

        :param intent: the intent object to look for.
        :return: an intent definition, from the skill definition, if found,
                 or None.
        """
        for intent_def in self.intent_defs:
            if intent_def.name == intent.intentName:
                return intent_def

        return