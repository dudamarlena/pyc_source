# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/acclaim_badges/forms.py
# Compiled at: 2017-06-02 15:35:20
from django import forms
from acclaim_badges.models import AcclaimToken
from acclaim_badges.models import BadgeCourse
from acclaim_badges.models import AcclaimApi
from openedx.core.djangoapps.content.course_overviews.models import CourseOverview

class BadgeCourseForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(BadgeCourseForm, self).__init__(*args, **kwargs)
        acclaim_api = AcclaimApi()
        template_list = acclaim_api.template_choices()
        badge_default = [('', 'Select Badge')]
        course_default = [('', 'Select Course')]
        self.fields['badge_template'] = forms.ChoiceField(choices=badge_default + template_list)
        make_tuple = lambda x: (
         str(x.id), x.display_name)
        courses = CourseOverview.objects.all()
        self.fields['edx_course'] = forms.ChoiceField(choices=course_default + map(make_tuple, courses))

    class Meta:
        model = BadgeCourse
        fields = ['badge_template', 'edx_course']


class AcclaimTokenForm(forms.ModelForm):
    auth_token = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = AcclaimToken
        fields = ['auth_token', 'organization_id', 'url']