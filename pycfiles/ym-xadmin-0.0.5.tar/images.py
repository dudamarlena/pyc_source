# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: G:\python\hhwork\extra_apps\xadmin\plugins\images.py
# Compiled at: 2019-01-06 19:47:42
from django.db import models
from django import forms
from django.utils.translation import ugettext as _
from django.utils.safestring import mark_safe
from xadmin.sites import site
from xadmin.views import BaseAdminPlugin, ModelFormAdminView, DetailAdminView, ListAdminView

def get_gallery_modal():
    return '\n        <!-- modal-gallery is the modal dialog used for the image gallery -->\n        <div id="modal-gallery" class="modal modal-gallery fade" tabindex="-1">\n          <div class="modal-dialog">\n            <div class="modal-content">\n              <div class="modal-header">\n                <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>\n                <h4 class="modal-title"></h4>\n              </div>\n              <div class="modal-body"><div class="modal-image"><h1 class="loader"><i class="fa-spinner fa-spin fa fa-large loader"></i></h1></div></div>\n              <div class="modal-footer">\n                  <a class="btn btn-info modal-prev"><i class="fa fa-arrow-left"></i> <span>%s</span></a>\n                  <a class="btn btn-primary modal-next"><span>%s</span> <i class="fa fa-arrow-right"></i></a>\n                  <a class="btn btn-success modal-play modal-slideshow" data-slideshow="5000"><i class="fa fa-play"></i> <span>%s</span></a>\n                  <a class="btn btn-default modal-download" target="_blank"><i class="fa fa-download"></i> <span>%s</span></a>\n              </div>\n            </div><!-- /.modal-content -->\n          </div><!-- /.modal-dialog -->\n        </div>\n    ' % (_('Previous'), _('Next'), _('Slideshow'), _('Download'))


class AdminImageField(forms.ImageField):

    def widget_attrs(self, widget):
        return {'label': self.label}


class AdminImageWidget(forms.FileInput):
    """
    A ImageField Widget that shows its current value if it has one.
    """

    def __init__(self, attrs={}):
        super(AdminImageWidget, self).__init__(attrs)

    def render(self, name, value, attrs=None):
        output = []
        if value and hasattr(value, 'url'):
            label = self.attrs.get('label', name)
            output.append('<a href="%s" target="_blank" title="%s" data-gallery="gallery"><img src="%s" class="field_img"/></a><br/>%s ' % (
             value.url, label, value.url, _('Change:')))
        output.append(super(AdminImageWidget, self).render(name, value, attrs))
        return mark_safe(('').join(output))


class ModelDetailPlugin(BaseAdminPlugin):

    def __init__(self, admin_view):
        super(ModelDetailPlugin, self).__init__(admin_view)
        self.include_image = False

    def get_field_attrs(self, attrs, db_field, **kwargs):
        if isinstance(db_field, models.ImageField):
            attrs['widget'] = AdminImageWidget
            attrs['form_class'] = AdminImageField
            self.include_image = True
        return attrs

    def get_field_result(self, result, field_name):
        if isinstance(result.field, models.ImageField):
            if result.value:
                img = getattr(result.obj, field_name)
                result.text = mark_safe('<a href="%s" target="_blank" title="%s" data-gallery="gallery"><img src="%s" class="field_img"/></a>' % (img.url, result.label, img.url))
                self.include_image = True
        return result

    def get_media(self, media):
        if self.include_image:
            media = media + self.vendor('image-gallery.js', 'image-gallery.css')
        return media

    def block_before_fieldsets(self, context, node):
        if self.include_image:
            return '<div id="gallery" data-toggle="modal-gallery" data-target="#modal-gallery">'

    def block_after_fieldsets(self, context, node):
        if self.include_image:
            return '</div>'

    def block_extrabody(self, context, node):
        if self.include_image:
            return get_gallery_modal()


class ModelListPlugin(BaseAdminPlugin):
    list_gallery = False

    def init_request(self, *args, **kwargs):
        return bool(self.list_gallery)

    def get_media(self, media):
        return media + self.vendor('image-gallery.js', 'image-gallery.css')

    def block_results_top(self, context, node):
        return '<div id="gallery" data-toggle="modal-gallery" data-target="#modal-gallery">'

    def block_results_bottom(self, context, node):
        return '</div>'

    def block_extrabody(self, context, node):
        return get_gallery_modal()


site.register_plugin(ModelDetailPlugin, DetailAdminView)
site.register_plugin(ModelDetailPlugin, ModelFormAdminView)
site.register_plugin(ModelListPlugin, ListAdminView)