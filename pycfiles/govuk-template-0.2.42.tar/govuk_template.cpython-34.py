# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/bitnami/apps/jenkins/jenkins_home/jobs/Publish python-govuk-template/workspace/govuk_template/flask/mustache/govuk_template.py
# Compiled at: 2015-05-21 11:37:03
# Size of source mod 2**32: 372 bytes
from pystache.renderer import Renderer
from os import path

def thisDir():
    return path.dirname(path.abspath(__file__))


class GovukTemplate(object):

    def render(self, *context, **kwargs):
        renderer = Renderer(search_dirs=[thisDir()])
        template = renderer.load_template('govuk_template')
        return renderer.render(template, *context, **kwargs)