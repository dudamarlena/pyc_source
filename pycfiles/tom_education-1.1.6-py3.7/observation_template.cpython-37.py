# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/tom_education/models/observation_template.py
# Compiled at: 2019-10-01 09:52:31
# Size of source mod 2**32: 2007 bytes
from datetime import datetime
from urllib.parse import urlparse, parse_qs, urlunparse
from django.db import models
from django.utils.http import urlencode
from tom_targets.models import Target

class ObservationTemplate(models.Model):
    name = models.CharField(max_length=255, null=False)
    target = models.ForeignKey(Target, on_delete=(models.CASCADE), null=False)
    facility = models.CharField(max_length=255, null=False)
    fields = models.TextField()

    class Meta:
        unique_together = ('name', 'target', 'facility')

    def get_create_url(self, base_url):
        """
        Return URL for instantiating this template by adding 'template_id' GET
        parameter to base create URL
        """
        parsed_url = urlparse(base_url)
        params = parse_qs(parsed_url.query)
        for key, val in params.items():
            params[key] = val[0]

        params['template_id'] = self.pk
        parts = list(parsed_url)
        parts[4] = urlencode(params)
        return urlunparse(parts)

    def get_identifier(self):
        """
        Return an identifier for an instantiation of this template, based on
        the template name and current date and time
        """
        now = datetime.now()
        fmt = '%Y-%m-%d-%H%M%S'
        return '{}-{}'.format(self.name, now.strftime(fmt))

    @staticmethod
    def get_identifier_field(facility):
        """
        Return name of the field used to extract template name when creating a
        template. This field is also used to store the identifier for
        instantiated templates
        """
        if facility == 'LCO':
            return 'name'
        raise NotImplementedError

    @staticmethod
    def get_date_fields(facility):
        """
        Return a sequence of field names whose type is datetime
        """
        if facility == 'LCO':
            return [
             'start', 'end']
        return []