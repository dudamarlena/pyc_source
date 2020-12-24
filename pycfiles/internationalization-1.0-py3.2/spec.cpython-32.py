# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/internationalization/core/spec.py
# Compiled at: 2013-04-24 04:53:27
"""
Created on Mar 13, 2012

@package: internationalization
@copyright: 2012 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Mugur Rus

API specifications for PO file management.
"""
import abc

class InvalidLocaleError(Exception):
    """
    Raise whenever there is a invalid locale provided.
    """
    pass


class IPOFileManager(metaclass=abc.ABCMeta):
    """
    The PO file manager: processes and returns the PO global, component or plugin
    PO files.
    """

    @abc.abstractmethod
    def getGlobalPOTimestamp(self, locale):
        """
        Returns the timestamp of the last update for the PO file identified by
        the given locale.

        @param locale: string
            The locale identifying the translation file.
        @return: datetime
            The last modification.
        """
        pass

    @abc.abstractmethod
    def getComponentPOTimestamp(self, component, locale):
        """
        Returns the timestamp of the last update for the PO file identified by
        the given component and locale.

        @param component: string
            The component id identifying the translation file.
        @param locale: string
            The locale identifying the translation file.
        @return: datetime
            The last modification.
        """
        pass

    @abc.abstractmethod
    def getPluginPOTimestamp(self, plugin, locale):
        """
        Returns the timestamp of the last update for the PO file identified by
        the given plugin and locale.

        @param plugin: string
            The plugin id identifying the translation file.
        @param locale: string
            The locale identifying the translation file.
        @return: datetime
            The last modification.
        """
        pass

    @abc.abstractmethod
    def getGlobalPOFile(self, locale):
        """
        Provides the messages for the whole application and the given locale.

        @param locale: string
            The locale for which to return the translation.
        @return: bytes file like object
            The PO file containing the translation.
        """
        pass

    @abc.abstractmethod
    def getGlobalAsDict(self, locale):
        """
        Provides the messages for the whole application and the given locale in the
        form of a dictionary. The dictionary has the following structure:
        {
            "mydomain" : {
                // po header fields
                "" : {
                    "plural-forms" : "...",
                    "lang" : "en",
                },
                // all the msgid strings and translations
                "context:msgid" : [ "msgid_plural", "translation", "plural_translation" ],
            },
        }

        @param locale: string
            The locale for which to return the translation.
        @return: dict
            The dictionary containing the translation.
        """
        pass

    @abc.abstractmethod
    def getComponentPOFile(self, component, locale):
        """
        Provides the messages for the given component and the given locale.

        @param component: string
            The component id for which to return the translation.
        @param locale: string
            The locale for which to return the translation.
        @return: bytes file like object
            The PO file containing the translation.
        """
        pass

    @abc.abstractmethod
    def getComponentAsDict(self, component, locale):
        """
        Provides the messages for the given component and the given locale in the
        form of a dictionary. For dictionary structure:
        @see IPOFileManager.getGlobalAsDict

        @param component: string
            The component id for which to return the translation.
        @param locale: string
            The locale for which to return the translation.
        @return: bytes file like object
            The dictionary containing the translation.
        """
        pass

    @abc.abstractmethod
    def getPluginPOFile(self, plugin, locale):
        """
        Provides the messages for the given plugin and the given locale.

        @param plugin: string
            The plugin id for which to return the translation.
        @param locale: string
            The locale for which to return the translation.
        @return: bytes  file like object
            The PO file containing the translation.
        """
        pass

    @abc.abstractmethod
    def getPluginAsDict(self, plugin, locale):
        """
        Provides the messages for the given component and the given locale in the
        form of a dictionary. For dictionary structure:
        @see IPOFileManager.getGlobalAsDict

        @param plugin: string
            The plugin id for which to return the translation.
        @param locale: string
            The locale for which to return the translation.
        @return: bytes file like object
            The dictionary containing the translation.
        """
        pass

    @abc.abstractmethod
    def updateGlobalPOFile(self, locale, poFile):
        """
        Updates the messages for all components / plugins and the given locale.
        
        @param locale: string
            The locale for which to update the translation.
        @param poFile: text file like object
            The source PO file from which to read the translation.
        """
        pass

    @abc.abstractmethod
    def updateComponentPOFile(self, component, locale, poFile):
        """
        Updates the messages for the given component and the given locale.

        @param component: Component.Id
            The component for which to update the translation.
        @param locale: string
            The locale for which to update the translation.
        @param poFile: text file like object
            The source PO file from which to read the translation.
        """
        pass

    @abc.abstractmethod
    def updatePluginPOFile(self, plugin, locale, poFile):
        """
        Updates the messages for the given plugin and the given locale.
        
        @param plugin: string
            The plugin id for which to update the translation.
        @param locale: string
            The locale for which to update the translation.
        @param poFile: text file like object
            The source PO file from which to read the translation.
        """
        pass