# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bas/dev/django-dmarc/dmarc/models.py
# Compiled at: 2018-06-18 17:00:55
# Size of source mod 2**32: 4168 bytes
"""
DMARC models for managing Aggregate Reports
http://dmarc.org/resources/specification/
"""
from django.db import models

class Reporter(models.Model):
    __doc__ = 'DMARC reporter'
    org_name = models.CharField('Organisation', unique=True, max_length=100)
    email = models.EmailField()

    def __unicode__(self):
        return self.org_name


class Report(models.Model):
    __doc__ = 'DMARC report metadata'
    report_id = models.CharField(max_length=100)
    reporter = models.ForeignKey(Reporter, on_delete=(models.CASCADE))
    date_begin = models.DateTimeField(db_index=True)
    date_end = models.DateTimeField()
    policy_domain = models.CharField(max_length=100)
    policy_adkim = models.CharField('DKIM alignment mode', max_length=1)
    policy_aspf = models.CharField('SPF alignment mode', max_length=1)
    policy_p = models.CharField('Requested handling policy', max_length=10)
    policy_sp = models.CharField('Requested handling policy for subdomains', max_length=10)
    policy_pct = models.SmallIntegerField('Sampling rate')
    report_xml = models.TextField(blank=True)

    def __unicode__(self):
        return self.report_id

    class Meta(object):
        __doc__ = 'Model constraints'
        unique_together = (('reporter', 'report_id', 'date_begin'), )


class Record(models.Model):
    __doc__ = 'DMARC report record'
    report = models.ForeignKey(Report, related_name='records', on_delete=(models.CASCADE))
    source_ip = models.CharField(max_length=39)
    recordcount = models.IntegerField()
    policyevaluated_disposition = models.CharField(max_length=10)
    policyevaluated_dkim = models.CharField(max_length=4)
    policyevaluated_spf = models.CharField(max_length=4)
    policyevaluated_reasontype = models.CharField(blank=True, max_length=75)
    policyevaluated_reasoncomment = models.CharField(blank=True, max_length=100)
    identifier_headerfrom = models.CharField(max_length=100)

    def __unicode__(self):
        return self.source_ip


class Result(models.Model):
    __doc__ = 'DMARC report record result'
    record = models.ForeignKey(Record, related_name='results', on_delete=(models.CASCADE))
    record_type = models.CharField(max_length=4)
    domain = models.CharField(max_length=100)
    result = models.CharField(max_length=9)

    def __unicode__(self):
        return '%s:%s-%s' % (str(self.id), self.record_type, self.domain)


class FBReporter(models.Model):
    __doc__ = 'DMARC feedback reporter'
    org_name = models.CharField('Organisation', unique=True, max_length=100)
    email = models.EmailField()

    def __unicode__(self):
        return self.email

    def save(self, *args, **kwargs):
        if not self.org_name:
            self.org_name = self.email
        (super(FBReporter, self).save)(*args, **kwargs)


class FBReport(models.Model):
    __doc__ = 'DMARC feedback report'
    reporter = models.ForeignKey(FBReporter, on_delete=(models.CASCADE))
    date = models.DateTimeField(db_index=True)
    source_ip = models.CharField(max_length=39)
    domain = models.CharField(max_length=100)
    email_from = models.CharField(max_length=100, blank=True)
    email_subject = models.CharField(max_length=100, blank=True)
    spf_alignment = models.CharField(max_length=10, blank=True)
    dkim_alignment = models.CharField(max_length=10, blank=True)
    dmarc_result = models.CharField(max_length=10, blank=True)
    description = models.TextField('human readable feedback', blank=True)
    email_source = models.TextField('source email including rfc822 headers', blank=True)
    feedback_report = models.TextField(blank=True)
    feedback_source = models.TextField()

    def __unicode__(self):
        msg = '{} {} {} {} {}'.format(self.data, self.domain, self.source_ip, self.email_from, self.email_subject)
        return msg