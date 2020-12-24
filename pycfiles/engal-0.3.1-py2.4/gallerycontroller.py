# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/engal/gallerycontroller.py
# Compiled at: 2006-09-20 17:02:41
import cherrypy, turbogears
from turbogears import controllers, expose, validate, redirect
from turbogears import identity, widgets, validators, mochikit
from turbogears import error_handler, flash
from engal import json, model
import logging
log = logging.getLogger('engal.gallerycontroller')
from engal.ibox.widgets import Ibox
ibox = Ibox()
from resourcecontroller import Resource, expose_resource
from engal.util import getTagIconDirectory

class PhotoSetFields(widgets.WidgetsList):
    __module__ = __name__
    name = widgets.TextField(validator=validators.NotEmpty)
    title = widgets.TextField(validator=validators.NotEmpty)
    description = widgets.TextArea()
    return_path = widgets.HiddenField()


photoset_form = widgets.TableForm(fields=PhotoSetFields(), submit_text='Add set')

class PhotoFields(widgets.WidgetsList):
    __module__ = __name__
    file = widgets.FileField()
    name = widgets.TextField(validator=validators.NotEmpty)
    description = widgets.TextArea()
    return_path = widgets.HiddenField()
    photoset_id = widgets.HiddenField(validator=validators.Int)


photo_form = widgets.TableForm(fields=PhotoFields(), submit_text='Add Photo')

class EditPhotoFields(widgets.WidgetsList):
    __module__ = __name__
    name = widgets.TextField(validator=validators.NotEmpty)
    description = widgets.TextArea()
    return_path = widgets.HiddenField()
    photo_id = widgets.HiddenField(validator=validators.Int)


editphoto_form = widgets.TableForm(fields=EditPhotoFields(), submit_text='Edit Photo')

class DefinitionForm(widgets.Form):
    __module__ = __name__
    template = '\n    <form xmlns:py="http://purl.org/kid/ns#"\n        name="${name}"\n        action="${action}"\n        method="${method}"\n        class="tableform"\n        py:attrs="form_attrs"\n    >\n        <div py:for="field in hidden_fields"\n            py:replace="field.display(value_for(field), **params_for(field))"\n        />\n        <dl>\n            <div py:for="i, field in enumerate(fields)"\n                class="${i%2 and \'odd\' or \'even\'}"\n            >\n                <dt>\n                    <label class="fieldlabel" for="${field.field_id}" py:content="field.label" />\n                </dt>\n                <dd>\n                    <span py:replace="field.display(value_for(field), **params_for(field))" />\n                    <span py:if="error_for(field)" class="fielderror" py:content="error_for(field)" />\n                    <span py:if="field.help_text" class="fieldhelp" py:content="field.help_text" />\n                </dd>\n            </div>\n            <div>\n                <dt>&#160;</dt>\n                <dd py:content="submit.display(submit_text)" />\n            </div>\n        </dl>\n    </form>\n    '


class TagField(widgets.SingleSelectField):
    __module__ = __name__
    params = ['aspect', 'photo', 'tag']
    aspect = None
    photo = None
    tag = None

    def _extend_options(self, d):
        if not self.aspect:
            d = [ (tag.id, tag.name) for tag in model.Tag.select() if tag.depth if tag != self.tag ]
        elif not self.photo:
            d = [ (tag.id, tag.name) for tag in self.aspect.tags if tag.depth if tag != self.tag ]
        else:
            d = [ (tag.id, tag.name) for tag in self.aspect.tags if tag.depth if tag not in self.photo.tags if tag != self.tag ]
        d.insert(0, (0, ''))
        return d


class TagWidgets(widgets.FieldSet):
    __module__ = __name__
    template = '\n    <fieldset xmlns:py="http://purl.org/kid/ns#"\n        class="${field_class}"\n        id="${field_id}"\n    >\n        <legend py:if="legend" py:content="legend" />\n        <div py:for="field in hidden_fields"\n            py:replace="field.display(value_for(field), **params_for(field))"\n        />\n        <table>\n        <tr py:for="field in fields">\n            <td><label class="fieldlabel" for="${field.field_id}" py:content="field.label" /></td>\n            <td>\n            <span py:content="field.display(value_for(field), **params_for(field))" />\n            <span py:if="error_for(field)" class="fielderror" py:content="error_for(field)" />\n            <span py:if="field.help_text" class="fieldhelp" py:content="field.help_text" />\n            </td>\n        </tr>\n        </table>\n    </fieldset>\n    '

    def iter_member_widgets(self):
        aspects = model.TagAspect.select()
        for aspect in aspects:
            yield TagField(label=aspect.name, aspect=aspect, name=aspect.short_name)

    def update_params(self, d):
        super(TagWidgets, self).update_params(d)
        d['fields'] = self.iter_member_widgets()
        log.info(str(d))


class TagFields(widgets.WidgetsList):
    __module__ = __name__
    tags = TagWidgets(label='Add new tags')
    photo_id = widgets.HiddenField()
    return_url = widgets.HiddenField()


tag_form = DefinitionForm(fields=TagFields(), submit_text='Change tags')
widgets.register_static_directory('engal.tagicons', getTagIconDirectory())

class TagCSS(widgets.CSSSource):
    __module__ = __name__
    src = '.engal_tag {\n    padding-left: 25px;\n    font-size: smaller;\n    background-position: top left;\n    background-repeat: no-repeat;\n    background-color: transparent;\n    background-image: url(%(root)s/tg_widgets/engal.tagicons/default.png);\n    }\n\n    .engal_tags {\n        padding-bottom: 1em;\n    }\n\n    '
    src_aspect = '.engal_tag.engal_tagaspect_%(name)s {\n        background-image: url(%(root)s/tg_widgets/engal.tagicons/%(id)s);\n    }'

    def __init__(self, *args, **kw):
        super(TagCSS, self).__init__(self.src, *args, **kw)

    def update_params(self, d):
        d['src'] = self.buildSource()

    def buildSource(self):
        ret = []
        ret.append(self.src % dict(root=turbogears.url('')))
        for aspect in model.TagAspect.select():
            if aspect.hasIcon():
                ret.append(self.src_aspect % dict(name=aspect.short_name, root=turbogears.url(''), id=aspect.id))

        return ('\n').join(ret)


class TagInfo(widgets.Widget):
    __module__ = __name__
    css = [TagCSS()]

    def __init__(self, tag_info, *args, **kw):
        self.tag_info = tag_info
        super(TagInfo, self).__init__(*args, **kw)

    def items(self):
        return self.tag_info


class Gallery(Resource):
    __module__ = __name__
    item_getter = model.User.by_user_name
    friendly_item_name = 'user'

    @expose(template='engal.templates.gallery_frontpage')
    def index(self):
        users = model.User.select()
        if not users.count():
            raise redirect('/firstuser')
        return dict(users=users)

    @expose(template='engal.templates.userpage')
    def show(self, user, *args, **kw):
        tg_errors = kw.get('tg_errors', None)
        photosets = model.PhotoSet.select(user == user)
        if tg_errors:
            flash('There was a problem with the form!')
        return dict(photosets=photosets, ibox=ibox, photoset_form=photoset_form, mochikit=mochikit, user=user)

    @expose_resource
    @expose(template='engal.templates.photosets')
    def sets(self, user, name=None, tg_errors=None):
        if not name:
            return self.show(user)
        s = model.PhotoSet.select(model.PhotoSet.q.name == name)[0]
        return dict(photoset=s, ibox=ibox, mochikit=mochikit, photo_form=photo_form, user=user)

    @expose(template='engal.templates.standardform')
    def saveTagsError(self, user, photo_id, tags, return_url, *args, **kw):
        return dict(form=tag_form, form_action=turbogears.url('/gallery/%s/saveTags' % (user.user_name,)), form_values={})

    @expose_resource
    @expose()
    @validate(form=tag_form)
    @error_handler(saveTagsError)
    def saveTags(self, user, photo_id, tags, return_url, *args, **kw):
        log.info('args are: %s' % (str(args),))
        log.info('kw are: %s' % (str(kw),))
        log.info('photo_id is: %s' % (str(photo_id),))
        log.info('tags are: %s' % (str(tags),))
        photo = model.Photo.get(photo_id)
        if tags:
            tags = [ model.Tag.get(t) for t in tags.values() if t ]
            for tag in tags:
                photo.addTag(tag)

        raise redirect(return_url)
        return 'saveTags'

    @expose_resource
    @expose(template='engal.templates.photo')
    def images(self, user, image_name, *args, **kw):
        log.info(cherrypy.request)
        log.info(dir(cherrypy.request))
        return_url = cherrypy.request.browserUrl
        if not image_name:
            raise NotFound
        photo = model.Photo.byName(image_name)
        user = photo.owner
        photoset = None
        for arg in args:
            if arg.startswith('set-'):
                try:
                    photoset_name = arg[4:]
                    print photoset_name
                    photoset = model.PhotoSet.select(model.PhotoSet.q.name == photoset_name)[0]
                except:
                    pass
                else:
                    break

        if not photoset:
            if photo.sets:
                photoset = photo.sets[0]
        return dict(photo=photo, user=user, ibox=ibox, photoset=photoset, editphoto_form=editphoto_form, tag_form=tag_form, return_url=return_url, taginfo=TagInfo(photo.taginfo))