# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/cameronlowe/Development/django-zencoder/zencoder/models.py
# Compiled at: 2017-01-17 17:04:11
# Size of source mod 2**32: 5267 bytes
import json, requests
from django.db import models
from json_field import JSONField
from .conf import settings

def sort_video(source):
    try:
        weight = settings.VIDEO_PREFERENCES.index(source.content_type)
    except:
        weight = len(settings.VIDEO_PREFERENCES) + 1

    return weight * (source.width or 1)


class Video(models.Model):
    __doc__ = 'This is a very lightweight model that basically wraps an externally available set of sources\n    for a given video.'
    name = models.CharField(max_length=255)
    poster = models.URLField(null=True, blank=True)
    input = models.URLField(null=True, blank=True)
    duration = models.PositiveIntegerField(blank=True, default=0)

    def __unicode__(self):
        return self.name

    def ordered_sources(self):
        return sorted(list(self.sources.all()), key=sort_video)

    def make_formatted_duration(self):
        if self.duration == 0 or self.duration is None:
            return '00:00:00'
        one_second = 1000
        one_minute = 60 * one_second
        one_hour = 60 * one_minute
        hours, _minutes = divmod(self.duration, one_hour)
        minutes, _seconds = divmod(_minutes, one_minute)
        seconds, _ = divmod(_seconds, one_second)
        return '{:02}:{:02}:{:02}'.format(hours, minutes, seconds)


class Source(models.Model):
    video = models.ForeignKey(Video, related_name='sources')
    url = models.URLField()
    content_type = models.CharField(max_length=100)
    width = models.IntegerField(null=True, blank=True)
    bitrate = models.IntegerField(null=True, blank=True, help_text='In kilobits per second')

    class Meta:
        ordering = ('width', 'bitrate')


class JobManager(models.Manager):

    def start(self, video, host=None):
        job = self.model(video=video)
        job.start()
        if job.data.get('test', False) is False:
            job.save()
        return job


class Job(models.Model):
    NOT_STARTED = 0
    COMPLETE = 1
    IN_PROGRESS = 2
    FAILED = 3
    STATUSES = (
     (
      NOT_STARTED, 'Not started'),
     (
      COMPLETE, 'Complete'),
     (
      IN_PROGRESS, 'In Progress'),
     (
      FAILED, 'Failed'))

    class Meta:
        ordering = ('-created', )

    objects = JobManager()
    AUTH_HEADERS = {'Zencoder-Api-Key': settings.ZENCODER_API_KEY}
    video = models.ForeignKey(Video)
    created = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUSES, default=NOT_STARTED, help_text='The encoding status')
    job_id = models.IntegerField()
    data = JSONField()

    def start(self):
        payload = settings.ZENCODER_JOB_PAYLOAD
        base_url = 's3://{}/{}/{}/'.format(settings.VIDEO_ENCODING_BUCKET, settings.VIDEO_ENCODING_DIRECTORY, self.video.pk)
        for output in payload['outputs']:
            output['base_url'] = base_url
            if 'thumbnails' in output:
                output['thumbnails']['base_url'] = base_url
                continue

        payload['input'] = self.video.input
        response = requests.post('https://app.zencoder.com/api/v2/jobs', data=json.dumps(payload), headers=self.AUTH_HEADERS)
        if response.status_code != 201:
            raise Exception('Zencoder response <{}>'.format(response.status_code))
        try:
            self.data = response.json()
        except TypeError:
            self.data = json.loads(response.content)

        self.job_id = self.data.get('id')
        self.status = Job.IN_PROGRESS

    def cancel(self):
        url = 'https://app.zencoder.com/api/v2/jobs/{}/cancel.json'.format(self.job_id)
        response = requests.put(url, headers=self.AUTH_HEADERS)
        if response.status_code != 204:
            raise Exception("Couldn't cancel the job!")
        self.status = Job.FAILED

    def notify(self, data):
        """Recieves a notification about the job completion, and adds video sources"""
        for output in data.get('outputs'):
            content_type = output.get('label')
            if content_type:
                url = output.get('url')
                if settings.VIDEO_URL_PROCESSOR:
                    url = settings.VIDEO_URL_PROCESSOR(url)
                Source.objects.create(video=self.video, content_type=content_type, width=output.get('width'), bitrate=output.get('video_bitrate_in_kbps'), url=url)
                continue

        self.status = Job.COMPLETE

    def encode_status_endpoints(self):
        if self.status == Job.NOT_STARTED:
            return
        fmt = {'base_url': 'https://app.zencoder.com/api/v2/jobs/{}/progress'.format(self.job_id), 
         'api_key': settings.ZENCODER_API_KEY}
        return {'json': '{base_url}.json?api_key={api_key}'.format(**fmt), 
         'xml': '{base_url}.xml?api_key={api_key}'.format(**fmt), 
         'js': '{base_url}.js?api_key={api_key}'.format(**fmt)}