# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/herbert/dev/python/sctdev/simpleproject/simpleproject/../../communitytools/sphenecoll/sphene/sphboard/categorytypes.py
# Compiled at: 2012-03-17 12:42:14
from django.utils.safestring import mark_safe
from sphene.sphboard.models import ExtendedCategoryConfig
from sphene.sphboard.views import PostForm
from sphene.sphboard.categorytyperegistry import CategoryType

class DefaultCategoryType(CategoryType):
    """
    the "default" category type which is used if there
    is no 'category type' setting.
    """

    def get_post_form_class(self, replypost, editpost):
        return PostForm


class SeparatorCategoryType(CategoryType):
    """
    category type which is only a separator (ie. a root categry which
    cannot be used for posting, ..)
    """
    name = 'sphseparator'
    label = 'Separator'

    def is_separator(self):
        return True


class ExtendedPostForm(PostForm):

    def __init__(self, *args, **kwargs):
        super(ExtendedPostForm, self).__init__(*args, **kwargs)

    def __set_label(self, string, field):
        if string:
            field.label = string

    def init_for_category_type(self, category_type, post):
        super(ExtendedPostForm, self).init_for_category_type(category_type, post)
        self.__set_label(category_type.get_subject_label(), self.fields['subject'])
        self.__set_label(category_type.get_body_label(), self.fields['body'])
        initial = category_type.get_body_initial()
        if initial:
            self.fields['body'].initial = initial
        help_text = category_type.get_body_help_text()
        if help_text:
            self.fields['body'].help_text = help_text


class ExtendedCategoryType(CategoryType):
    name = 'extendedconfig'
    label = 'Extended Config'

    def get_subject_label(self):
        return self.get_extended_config().subject_label

    def get_body_label(self):
        return self.get_extended_config().body_label

    def get_body_initial(self):
        return self.get_extended_config().body_initial

    def get_body_help_text(self):
        return self.get_extended_config().body_help_text

    def get_post_new_thread_label(self):
        return self.get_extended_config().post_new_thread_label

    def get_above_thread_list_block(self):
        return mark_safe(self.get_extended_config().above_thread_list_block)

    def get_threadlist_template(self):
        return 'sphene/sphboard/extended_thread_list.html'

    def get_new_thread_link_template(self):
        return 'sphene/sphboard/_extended_new_thread_link.html'

    def get_extended_config(self):
        if hasattr(self, 'extended_config'):
            return self.extended_config
        try:
            config = ExtendedCategoryConfig.objects.get(category=self.category)
        except ExtendedCategoryConfig.DoesNotExist:
            config = ExtendedCategoryConfig(category=self.category)
            config.save()

        self.extended_config = config
        return config