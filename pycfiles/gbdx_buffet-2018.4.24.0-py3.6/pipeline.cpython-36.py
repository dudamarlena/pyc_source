# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/gbdx_buffet/pipeline.py
# Compiled at: 2018-03-13 00:36:21
# Size of source mod 2**32: 5550 bytes
import json, os, pandas as pd, regex, requests
from gbdxtools import Interface
from gbdx_buffet import launch_workflow
gbdx = Interface()

def post_slack(text):
    webhook_url = 'https://hooks.slack.com/services/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'
    response = requests.post(webhook_url,
      data=(json.dumps({'text': text})), headers={'Content-Type': 'application/json'})
    if response.status_code != 200:
        raise ValueError('Request to slack returned an error %s, the response is:\n%s' % (
         response.status_code, response.text))


class ProgressPercentageFile(object):

    def __init__(self, filename, size):
        self.filename = filename
        self.size = size
        self.total = 0
        self.percent = 0
        self.f = open(self.filename, 'w')

    def __call__(self, bytes_amount):
        self.total += bytes_amount
        self.percent = self.total * 100 // self.size
        if not self.f.closed:
            self.f.seek(0)
            self.f.write('{}'.format(self.total * 100 // self.size))
            self.f.flush()
        if self.total == self.size:
            self.f.close()


class ProgressPercentageSlack(object):

    def __init__(self, filename, size):
        self.filename = filename
        self.size = size
        self.total = 0
        self.percent = 0
        self.f = open(self.filename, 'w')

    def __call__(self, bytes_amount):
        self.total += bytes_amount
        last_percent = self.percent
        self.percent = self.total * 100 // self.size
        if self.percent // 10 - last_percent // 10 > 0:
            post_slack('{} is {}% processed'.format(self.filename, self.percent))
        if self.total == self.size:
            self.f.close()


def is_wv(platform):
    return platform.endswith('03') or platform.endswith('04')


def pipeline_order():
    images = pd.read_csv('/pipeline/images.csv')
    areas = pd.read_csv('/pipeline/areas.csv')
    new_images = []
    for area in areas[(areas.ordered == 0)].itertuples():
        results = gbdx.catalog.search(searchAreaWkt=(area.wkt))['results']
        for result in results:
            p = result['properties']
            if is_wv(p['platformName']):
                im_id = p['catalogID']
                new_images.append(im_id)
                w = launch_workflow(im_id, 'pipeline', pansharpen=True, dra=True)
                new_images.append({'id':im_id,  'wid':w.id,  'status':1,  'deepcore':[area.ml]})

    areas.ordered = 1
    images = pd.concat([images, new_images], axis=1, ignore_index=True)
    (
     images.to_csv('/pipeline/images.csv'), areas.to_csv('/pipeline/areas.csv'))


def pipeline_download():
    images = pd.read_csv('/pipeline/images.csv')
    running_images = images[(images.status == 1)]
    for image in running_images.itertuples():
        workflow = gbdx.workflow.get(image.wid)
        if workflow['state']['event'] == 'succeeded':
            download_single(['pipeline', image.id], ['pipeline', 'images'])
            images[(images.id == image.id)].status = 2

    images.to_csv('/pipeline/images.csv')


def deepcore(im_id, ml_tasks):
    pass


def pipeline_deepcore():
    images = pd.read_csv('/pipeline/images.csv')
    running_images = images[(images.status == 1)]
    for image in running_images.itertuples():
        workflow = gbdx.workflow.get(image.wid)
        if workflow['state']['event'] == 'succeeded':
            deepcore(image.id, image.ml)
            images[(images.id == image.id)].status = 2

    images.to_csv('/pipeline/images.csv')


def download_single(prefix, output, verbose=False, dryrun=False):
    gbdx = Interface()
    aws = gbdx.s3._load_info()
    os.environ['AWS_ACCESS_KEY_ID'] = aws['S3_access_key']
    os.environ['AWS_SECRET_ACCESS_KEY'] = aws['S3_secret_key']
    os.environ['AWS_SESSION_TOKEN'] = aws['S3_session_token']
    import boto3
    prefix = [aws['prefix']] + prefix
    prefix = (os.path.join)(*prefix)
    from boto3.s3.transfer import S3Transfer
    transfer = S3Transfer(boto3.client('s3'))
    bucket = boto3.resource('s3').Bucket(aws['bucket'])
    for objects in bucket.objects.filter(Prefix=prefix).pages():
        for obj in objects:
            if obj.key.lower().endswith('tif'):
                catid = regex.search('(?<=\\/pipeline\\/)([0-9\\-a-z]+)(?=\\/)', obj.key)[0]
                transfer.download_file((aws['bucket']), (obj.key), ('/pipeline/data/{}.tif'.format(catid)), callback=(ProgressPercentageFile('/pipeline/download/{}'.format(catid), obj.size)))
                bucket.download_file((obj.key), ('/pipeline/data/{}.tif'.format(catid)), callbacks=(ProgressPercentageFile('/pipeline/download/{}'.format(catid), obj.size)))
            else:
                if obj.key.lower().endswith('imd'):
                    catid = regex.search('(?<=\\/pipeline\\/)([0-9\\-a-z]+)(?=\\/)', obj.key)[0]
                    bucket.download_file(obj.key, '/pipeline/data/{}.imd'.format(catid))