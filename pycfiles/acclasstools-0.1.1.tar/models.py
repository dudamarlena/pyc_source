# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/acclaim_badges/models.py
# Compiled at: 2017-06-05 13:39:32
__doc__ = b'\nDatabase models for acclaim_badges.\n'
from __future__ import absolute_import, unicode_literals
from django.db import models
from django.dispatch import receiver
from openedx.core.djangoapps.signals.signals import COURSE_GRADE_CHANGED
from django.contrib.auth.models import User
import requests, json, datetime
from django.core.urlresolvers import reverse
from django.utils.encoding import python_2_unicode_compatible
from model_utils.models import TimeStampedModel
from openedx.core.djangoapps.content.course_overviews.models import CourseOverview
from opaque_keys.edx.keys import CourseKey, UsageKey
from openedx.core.djangoapps.content.course_overviews.models import CourseOverview
from django.core.exceptions import ObjectDoesNotExist
from encrypted_fields import EncryptedTextField
from logging import getLogger
log = getLogger(__name__)

@receiver(COURSE_GRADE_CHANGED)
def my_callback(sender, user, course_grade, course_key, deadline, **kwargs):
    log.info(b'Grade change trigger recieved.  Checking to see if earner is qualified for badging.')
    for usr in User.objects.filter(username=user):
        if course_grade.summary[b'grade'] == b'Pass':
            log.info(b'Earner earned a passing score.')
            courses = BadgeCourse.objects.filter(edx_course=str(course_key))
            if courses.exists():
                acclaim_api = AcclaimApi()
                for course in courses:
                    badge_template_id = json.loads(course.badge_template)[0]
                    acclaim_api.issue_badge(usr, badge_template_id)


class SingletonModel(models.Model):

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.__class__.objects.exclude(id=self.id).delete()
        super(SingletonModel, self).save(*args, **kwargs)

    @classmethod
    def load(cls):
        try:
            return cls.objects.get()
        except cls.DoesNotExist:
            return cls()


class AcclaimToken(SingletonModel, TimeStampedModel):
    auth_token = EncryptedTextField()
    organization_id = models.UUIDField()
    PROD = b'youracclaim.com [Production]'
    SANDBOX = b'jefferson-sandbox.herokuapp.com [Sandbox]'
    ENVIRONMENTS = (
     (
      b'https://jefferson-sandbox.herokuapp.com/', SANDBOX),
     (
      b'https://youracclaim.com/', PROD))
    url = models.CharField(max_length=200, choices=ENVIRONMENTS)

    def get_absolute_url(self):
        return reverse(b'acclaim-tokens')


class AcclaimApi:

    def __init__(self):
        abstract = True

    def get_token(self):
        token = AcclaimToken.objects.all()
        if token.exists():
            return AcclaimToken.objects.all()[0]
        else:
            return False

    def parse_acclaim_response(self, response):
        templates = []
        if response is not None:
            if response.status_code == 200:
                templates = json.loads(response.text)[b'data']
        return templates

    def is_badge_duplicate(self, badge_template_id, recipient_email):
        log.info((b'Checking badge duplicate email: {}, template: {}').format(recipient_email, badge_template_id))
        duplicate = False
        params = (b'?filter=query::{}|badge_template_id::{}').format(recipient_email, badge_template_id)
        token = self.get_token()
        if token:
            url = (b'{}/v1/organizations/{}/badges').format(str(token.url), str(token.organization_id))
            query = url + params
            try:
                response = requests.get(query, auth=(token.auth_token, b''))
                json = response.json()
                existing_badge_count = json[b'metadata'][b'count']
                log.info((b'user badge count: {}').format(existing_badge_count))
                if existing_badge_count > 0:
                    log.info(b'user already has a badge with the given template ID and email')
                    duplicate = True
                else:
                    log.info(b'No badge yet exists for earner.')
            except (ConnectionError, requests.exceptions.MissingSchema) as e:
                log.warning(b'Unable to connect to Acclaim')

        return duplicate

    def get_templates(self):
        from requests.exceptions import ConnectionError
        templates = []
        token = self.get_token()
        if token:
            url = (b'{}v1/organizations/{}/badge_templates').format(str(token.url), str(token.organization_id))
            try:
                response = requests.get(url, auth=(token.auth_token, b''))
                templates = self.parse_acclaim_response(response)
            except (ConnectionError, requests.exceptions.MissingSchema) as e:
                log.warning(b'Unable to connect to Acclaim')

        return templates

    def issue_badge(self, usr, template_id):
        log.info((b'Issue Acclaim Badge with template: {}.').format(template_id))
        if not self.is_badge_duplicate(template_id, usr.email):
            token = self.get_token()
            if token:
                date = str(datetime.datetime.now().strftime(b'%Y-%m-%dT%H:%M:%S')) + b' Z'
                payload = {b'recipient_email': usr.email, b'badge_template_id': template_id, b'issued_at': date}
                url = (b'{}/v1/organizations/{}/badges').format(str(token.url), str(token.organization_id))
                r = requests.post(url, data=payload, auth=(token.auth_token, b''))
                log.info(b'Acclaim badge payload: ' + str(payload))
                log.info((b'Acclaim badge issue: {}').format(str(r)))
                if r.status_code != 201:
                    log.warning(b'Unable to connect to Acclaim to issue badge')

    def template_choices(self):
        templates = self.get_templates()
        make_tuple = lambda x: (json.dumps([x[b'id'], x[b'name']]), x[b'name'])
        return map(make_tuple, templates)


class BadgeCourse(models.Model):

    @property
    def course_name(self):
        course_display_name = b'Does not exist'
        try:
            course_obj = CourseOverview.objects.get(pk=CourseKey.from_string(self.edx_course))
            course_display_name = course_obj.display_name
        except ObjectDoesNotExist:
            log.warning((b'Course:{} does not exist').format(str(self.edx_course)))

        return course_display_name

    badge_template = models.CharField(max_length=200)
    edx_course = models.CharField(max_length=200)

    def get_absolute_url(self):
        return reverse(b'badge-courses')