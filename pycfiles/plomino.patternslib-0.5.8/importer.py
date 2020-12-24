# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/plomino/dominoimport/importer.py
# Compiled at: 2009-07-06 10:06:10
__doc__ = '\nCreated on 20 may 2009\n\n@author: Emmanuelle Helly\n\nFile DxlConfig.py is required\n'
__author__ = 'Emmanuelle Helly'
__docformat__ = 'plaintext'
from zope.interface import Interface, implements
from interfaces import IDominoImporter
from exceptions import ImportDXLException
from dxlParser import DXLParser
from plominoBuilder import PlominoBuilder
import logging
logger = logging.getLogger('Plomino')

class DominoImporter(object):
    """
    Class used to import a DXL file from Domino to Plomino
    """
    __module__ = __name__
    implements(IDominoImporter)

    def __init__(self, context):
        """Initialize adapter."""
        self.context = context

    def processImportDXL(self, fileToImport):
        """
        Process import of the file
        """
        results = {'resources': [0, 0], 'agents': [0, 0], 'forms': [0, 0], 'views': [0, 0], 'docs': [0, 0]}
        myDxlParser = DXLParser()
        myDxlParser.parseDXLFile(fileToImport)
        myPlominoBuilder = PlominoBuilder(self.context)
        for resource in myDxlParser.getResources():
            try:
                myPlominoBuilder.createResource(resource)
                results['resources'][0] += 1
            except Exception, inst:
                results['resources'][1] += 1

        for form in myDxlParser.getForms():
            try:
                myPlominoBuilder.createForm(form)
                results['forms'][0] += 1
            except Exception, inst:
                results['forms'][1] += 1
                print type(inst), inst

        for view in myDxlParser.getViews():
            try:
                myPlominoBuilder.createView(view)
                results['views'][0] += 1
            except Exception, inst:
                results['views'][1] += 1
                print type(inst), inst

        for doc in myDxlParser.getDocs():
            try:
                myPlominoBuilder.createDoc(doc)
                results['docs'][0] += 1
            except Exception, inst:
                results['docs'][1] += 1
                print type(inst), inst

        for agent in myDxlParser.getAgents():
            try:
                myPlominoBuilder.createAgent(agent)
                results['agents'][0] += 1
            except Exception, inst:
                results['agents'][1] += 1
                print type(inst), inst

        self.context.getIndex().refresh()
        print results
        return results