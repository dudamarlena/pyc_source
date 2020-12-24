# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/oshane/Workspace/osoobe/packages/kotti/src/kotti_migration/kotti_migration/views/edit.py
# Compiled at: 2017-05-22 11:46:44
"""
Created on 2017-05-22
:author: Oshane Bailey (b4.oshany@gmail.com)
"""
import json, colander
from kotti.views.edit import ContentSchema
from kotti.views.form import AddFormView
from kotti.views.form import EditFormView
from pyramid.view import view_config, view_defaults
from kotti_migration import _, util

@view_defaults(name='export', context='kotti.resources.Content', permission='admin')
class ExportImportView(object):

    def __init__(self, context, request):
        """ Constructor.
        :param context: Container of the nodes that will be created from
                        uploads.
        :type context: :class:`kotti.resources.Content` or descendants.
        :param request: Current request.
        :type request: :class:`kotti.request.Request`
        """
        self.context = context
        self.request = request

    @view_config(request_method='GET', accept='application/json', renderer='json')
    def export_data(self):
        context_data = util.export(self.context)
        return context_data

    @view_config(name='import', renderer='kotti_migration:templates/import.pt')
    def import_data(self):
        if self.request.method == 'POST':
            filename = self.request.POST['file'].filename
            input_file = self.request.POST['file'].file
            filepath = '/tmp'
            temp_file_path = filepath + '~'
            input_file.seek(0)
            data = json.load(input_file)
            util.import_data(base=self.context, context_data=data)
            self.request.session.flash(_('Data has been imported'), 'success')
        return {}