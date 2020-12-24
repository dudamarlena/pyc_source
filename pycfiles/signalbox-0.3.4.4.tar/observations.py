# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ben/dev/signalbox/signalbox/templatetags/signalbox_tags/observations.py
# Compiled at: 2014-08-27 19:26:12
from datetime import timedelta
from datetime import datetime
from django import template
register = template.Library()
from signalbox import models

@register.tag(name='get_observations')
def get_observations(parser, token):
    tag_name, study_id, period, obtype = token.split_contents()
    return ObservationsCount(study_id, period[1:-1], obtype[1:-1])


class ObservationsCount(template.Node):

    def __init__(self, study_id, period, obtype):
        self.study_id = template.Variable(study_id)
        self.period = None
        if period == 'current':
            self.period = [
             datetime.today() - timedelta(days=7), datetime.today() + timedelta(days=7)]
        if period == 'lastmonth':
            self.period = [
             datetime.today() - timedelta(days=30), datetime.today()]
        self.obtype = obtype
        return

    def render(self, context):
        observations = models.Observation.objects.filter(dyad__study__id=self.study_id.resolve(context))
        if self.period:
            observations = observations.filter(due__range=self.period)
        if self.obtype == 'incomplete':
            observations = observations.filter(status__lt=1)
        return observations.count()