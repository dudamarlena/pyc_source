# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/cytomine/models/project.py
# Compiled at: 2017-09-05 05:52:58
__author__ = 'Stévens Benjamin <b.stevens@ulg.ac.be>'
__contributors__ = ['Marée Raphaël <raphael.maree@ulg.ac.be>', 'Rollus Loïc <lrollus@ulg.ac.be']
__copyright__ = 'Copyright 2010-2015 University of Liège, Belgium, http://www.cytomine.be/'
from model import Model
from collection import Collection

class Project(Model):

    def __init__(self, params=None):
        super(Project, self).__init__(params)
        self._callback_identifier = 'project'

    def to_url(self):
        if hasattr(self, 'id'):
            return 'project/%d.json' % self.id
        else:
            return 'project.json'

    def __str__(self):
        return '%s : %s ' % (self.id, self.name)


class ProjectCollection(Collection):

    def __init__(self, params=None):
        super(ProjectCollection, self).__init__(Project, params)

    def to_url(self):
        return 'project.json'


class ProjectProperty(Model):

    def __init__(self, params=None):
        super(ProjectProperty, self).__init__(params)
        self._callback_identifier = 'property'

    def to_url(self):
        if hasattr(self, 'domainIdent') and not hasattr(self, 'id'):
            return 'project/%d/property.json' % self.domainIdent
        if hasattr(self, 'domainIdent') and hasattr(self, 'id'):
            return 'project/%d/property/%d.json' % (self.domainIdent, self.id)

    def __str__(self):
        return 'Project Property %d,%d ' % (self.project, self.id)