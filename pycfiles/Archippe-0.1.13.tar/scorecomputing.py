# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/archipelagenthypervisorplatformrequest/scorecomputing.py
# Compiled at: 2013-03-20 13:50:16


class TNBasicPlatformScoreComputing(object):
    """
    This class is a basic score computing. If you want to provide
    your own score computing unit, you can subclass this and implement
    your own computing system.
    """

    def __init__(self):
        """
        Put custom initialization here.
        """
        pass

    @staticmethod
    def plugin_info():
        """
        Return informations about the plugin.
        @rtype: dict
        @return: dictionary contaning plugin informations
        """
        plugin_friendly_name = 'Platform Request Base Score Computing Unit'
        plugin_identifier = 'basecomputingunit'
        plugin_configuration_section = None
        plugin_configuration_tokens = []
        return {'common-name': plugin_friendly_name, 'identifier': plugin_identifier, 
           'configuration-section': plugin_configuration_section, 
           'configuration-tokens': plugin_configuration_tokens}

    def score(self, action=None):
        """
        Perform the score. The highest score is, the highest chance
        you got to perform the action. If you want to decline
        the performing of the action, return 0.0 or None. the max score
        you can return is 1.0 (so basically see it as a percentage).
        @type action: string
        @param action: the name of the action if you want to use it to compute the score (optionnal)
        @rtype: float
        @return: the score
        """
        import random
        return random.random()