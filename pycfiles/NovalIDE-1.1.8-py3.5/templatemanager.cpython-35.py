# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/noval/project/templatemanager.py
# Compiled at: 2019-08-16 02:55:35
# Size of source mod 2**32: 1076 bytes
import noval.util.singleton as singleton

@singleton.Singleton
class ProjectTemplateManager:
    __doc__ = 'description of class'

    def __init__(self):
        self.project_templates = []

    def AddProjectTemplate(self, template_catlog, template_name, pages):
        if template_catlog.find(' ') != -1:
            raise RuntimeError('catlog could not contain blank character')
        project_template = self.FindProjectTemplate(template_catlog)
        if not project_template:
            self.project_templates.append({template_catlog: [(template_name, pages)]})
        else:
            project_template[template_catlog].extend([(template_name, pages)])

    def FindProjectTemplate(self, template_catlog):
        for project_template in self.project_templates:
            if list(project_template.keys())[0] == template_catlog:
                return project_template

    @property
    def ProjectTemplates(self):
        return self.project_templates