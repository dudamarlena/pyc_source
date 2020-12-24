# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/moses/GitHub/cassava_public/cassava/Automater/inputs.py
# Compiled at: 2015-08-04 20:17:17
__doc__ = '\nThe inputs.py module represents some form of all inputs\nto the Automater program to include target files, and\nthe standard config file - sites.xml. Any addition to\nAutomater that brings any other input requirement should\nbe programmed in this module.\n\nClass(es):\nTargetFile -- Provides a representation of a file containing target\n              strings for Automater to utilize.\nSitesFile -- Provides a representation of the sites.xml\n             configuration file.\n\nFunction(s):\nNo global exportable functions are defined.\n\nException(s):\nNo exceptions exported.\n'
from xml.etree.ElementTree import ElementTree
import os

class TargetFile(object):
    """
    TargetFile provides a Class Method to retrieve information from a file-
    based target when one is entered as the first parameter to the program.

    Public Method(s):
    (Class Method) TargetList

    Instance variable(s):
    No instance variables.
    """

    @classmethod
    def TargetList(self, filename):
        """
        Opens a file for reading.
        Returns each string from each line of a single or multi-line file.

        Argument(s):
        filename -- string based name of the file that will be retrieved and parsed.

        Return value(s):
        Iterator of string(s) found in a single or multi-line file.

        Restriction(s):
        This Method is tagged as a Class Method
        """
        try:
            target = ''
            with open(filename) as (f):
                li = f.readlines()
                for i in li:
                    target = str(i).strip()
                    yield target

        except IOError:
            pass


class SitesFile(object):
    """
    SitesFile represents an XML Elementree object representing the
    program's configuration file. Returns XML Elementree object.

    Method(s):
    (Class Method) getXMLTree
    (Class Method) fileExists

    Instance variable(s):
    No instance variables.
    """

    @classmethod
    def getXMLTree(self):
        """
        Opens a config file for reading.
        Returns XML Elementree object representing XML Config file.

        Argument(s):
        No arguments are required.

        Return value(s):
        ElementTree

        Restrictions:
        File must be named sites.xml and must be in same directory as caller.
        This Method is tagged as a Class Method
        """
        try:
            sites_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'sites.xml')
            with open(sites_path) as (f):
                sitetree = ElementTree()
                sitetree.parse(f)
                return sitetree
        except:
            pass

    @classmethod
    def fileExists(self):
        """
        Checks if a file exists. Returns boolean representing if file exists.

        Argument(s):
        No arguments are required.

        Return value(s):
        Boolean

        Restrictions:
        File must be named sites.xml and must be in same directory as caller.
        This Method is tagged as a Class Method
        """
        sites_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'sites.xml')
        return os.path.exists(sites_path) and os.path.isfile(sites_path)