# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/engal/findcontroller.py
# Compiled at: 2006-09-19 15:41:13
import logging, cherrypy, turbogears
from turbogears import validate, redirect, expose
from turbogears import widgets, validators
from turbogears import error_handler, flash
from engal import json, model
log = logging.getLogger('engal.controllers')
from engal.ibox.widgets import Ibox
ibox = Ibox()
from resourcecontroller import Resource, expose_resource

class FindController(Resource):
    __module__ = __name__
    item_getter = model.TagAspect.byShort_name

    @expose(template='engal.templates.findwelcome')
    def index(self):
        return dict(aspects=model.TagAspect.select())

    @expose_resource
    @expose(template='engal.templates.findaspect')
    def show(self, tagaspect, tag=None):
        if tag:
            return self._showtag(tagaspect, tag)
        return dict(aspects=model.TagAspect.select(), aspect=tagaspect)

    @expose(template='engal.templates.findtag')
    def _showtag(self, tagaspect, tag):
        tag = model.Tag.byShort_name(tag)
        photos = tag.photos
        return dict(aspects=model.TagAspect.select(), aspect=tagaspect, tag=tag, photos=photos)

    @expose(template='engal.templates.findwelcome')
    def date(self):
        return dict(aspects=model.TagAspect.select())