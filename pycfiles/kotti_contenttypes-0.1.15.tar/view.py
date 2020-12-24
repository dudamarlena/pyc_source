# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/oshane/Workspace/osoobe/packages/kotti/src/kotti_contenttypes/kotti_contenttypes/views/view.py
# Compiled at: 2017-01-26 14:24:36
"""
Created on 2016-10-18
:author: Oshane Bailey (b4.oshany@gmail.com)
"""
from pyramid.view import view_config
from pyramid.view import view_defaults
from kotti_contenttypes import _, fanstatic
from kotti_contenttypes.resources import Folder
from kotti_contenttypes.views import BaseView

@view_defaults(context=Folder, permission='view')
class FolderViews(BaseView):
    """ Views for :class:`kotti_contenttypes.resources.Folder` """

    @view_config(name='view', permission='view', renderer='kotti_contenttypes:templates/folder.pt')
    def default_view(self):
        """ Default view for :class:`kotti_contenttypes.resources.Folder`

        :result: Dictionary needed to render the template.
        :rtype: dict
        """
        fanstatic.folder_js.need()
        return {}