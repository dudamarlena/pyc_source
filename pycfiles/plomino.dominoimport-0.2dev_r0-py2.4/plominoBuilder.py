# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/plomino/dominoimport/plominoBuilder.py
# Compiled at: 2009-07-06 10:08:57
"""
Created on 22 June 2009

@author: Emmanuelle Helly

"""
__author__ = 'Emmanuelle Helly'
__docformat__ = 'plaintext'
from binascii import a2b_base64
import mimetypes

class PlominoBuilder(object):
    """
    create all elements in the correct database from a dict 
    """
    __module__ = __name__

    def __init__(self, plominoDatabase):
        self.plominoDatabase = plominoDatabase

    def createForm(self, formInfos):
        """
        Create form in the database

        @param dict formInfos : 
        @return string :
        @author
        """
        formId = self.plominoDatabase.invokeFactory(formInfos['type'], id=formInfos['id'])
        if formId is not None:
            form = self.plominoDatabase.getForm(formId)
            form.setTitle(formInfos['title'])
            form.setFormLayout(formInfos['formLayout'])
            for fieldInfos in formInfos['fields']:
                self.createField(fieldInfos, form)

            form.at_post_create_script()
            self.plominoDatabase.getIndex().refresh()
        return

    def createField(self, fieldInfos, container):
        """
        Create field in the database

        @param dict fieldInfos : 
        @param plomino object container : 
        @return string :
        """
        fieldId = container.invokeFactory(fieldInfos['type'], id=fieldInfos['id'])
        if fieldId is not None:
            field = container.getFormField(fieldId)
            field.setTitle(fieldInfos['title'])
            field.setFieldType(fieldInfos['FieldType'])
            field.setFieldMode(fieldInfos['FieldMode'])
            field.setFormula(fieldInfos['formula'])
            field.setValidationFormula(fieldInfos['ValidationFormula'])
            adapt = field.getSettings()
            for key in fieldInfos['settings'].keys():
                v = fieldInfos['settings'][key]
                if v is not None:
                    setattr(adapt, key, v)

            field.at_post_create_script()
            self.plominoDatabase.getIndex().refresh()
        return

    def createView(self, viewInfos):
        """
        Create view in the database

        @param dict viewInfos : 
        @return string :
        """
        viewId = self.plominoDatabase.invokeFactory(viewInfos['type'], id=viewInfos['id'])
        if viewId is not None:
            view = self.plominoDatabase.getView(viewId)
            view.setTitle(viewInfos['title'])
            view.setSelectionFormula(viewInfos['SelectionFormula'])
            view.setFormFormula(viewInfos['FormFormula'])
            for columnInfos in viewInfos['columns']:
                self.createColumn(columnInfos, view)

            view.at_post_create_script()
            self.plominoDatabase.getIndex().refresh()
        return

    def createColumn(self, columnInfos, container):
        """
        Create column in the database

        @param dict columnInfos : 
        @param dict viewId : 
        @return string :
        """
        columnId = container.invokeFactory(columnInfos['type'], id=columnInfos['id'])
        if columnId is not None:
            column = container.getColumn(columnId)
            column.setTitle(columnInfos['title'])
            column.setFormula(columnInfos['formula'])
            column.setPosition(columnInfos['position'])
            column.at_post_create_script()
        return

    def createDoc(self, docInfos):
        """
        Create document in the database

        @param dict docInfos : 
        @return string :
        """
        if docInfos['id'] != '':
            newDocId = self.plominoDatabase.invokeFactory(docInfos['type'], id=docInfos['id'])
            newDoc = self.plominoDatabase.getDocument(docInfos['id'])
        else:
            newDoc = self.plominoDatabase.createDocument()
        if newDoc is not None:
            if self.plominoDatabase.getForm(docInfos['form']) is not None:
                newDoc.setItem('Form', docInfos['form'])
                for itemInfos in docInfos['items']:
                    newDoc.setItem(itemInfos['name'], itemInfos['value'])

                if docInfos['files'] != []:
                    if not hasattr(newDoc.getForm(), 'imported_files'):
                        fieldId = newDoc.getForm().invokeFactory('PlominoField', id='imported_files', title='Imported Files', FieldType='ATTACHMENT')
                        newDoc.getForm().setFormLayout(newDoc.getForm().getFormLayout() + '<p>Imported files: <span class="plominoFieldClass">imported_files</span></p>')
                    for fileInfos in docInfos['files']:
                        newDoc.setfile(a2b_base64(str(fileInfos['content'])), fileInfos['name'])

                newDoc.save()
            else:
                raise Exception
        self.plominoDatabase.getIndex().refresh()
        return

    def createAgent(self, agentInfos):
        """
        Create agent in the database

        @param dict agentInfos : 
        @return string :
        """
        agentId = self.plominoDatabase.invokeFactory(agentInfos['type'], id=agentInfos['id'])
        if agentId is not None:
            agent = getattr(self.plominoDatabase, agentId)
            agent.setContent(agentInfos['content'])
            agent.setScheduled(agentInfos['scheduled'])
            agent.at_post_create_script()
        return

    def createResource(self, resourceInfos):
        """
        Add files into the database "resources" folder
        @param dict resourceInfos : 
        @return string :
        """
        if not hasattr(self.plominoDatabase, resourceInfos['name']):
            self.plominoDatabase.resources.manage_addFile(resourceInfos['name'])
        obj = getattr(self.plominoDatabase.resources, resourceInfos['name'])
        obj.update_data(resourceInfos['content'].decode('base64'), content_type=resourceInfos['type'])