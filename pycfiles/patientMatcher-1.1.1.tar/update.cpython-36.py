# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/chiararasi/Documents/work/GITs/patientMatcher/patientMatcher/cli/update.py
# Compiled at: 2019-04-24 05:47:57
# Size of source mod 2**32: 1426 bytes
import requests
from clint.textui import progress
import click
from patientMatcher.constants import PHENOTYPE_TERMS

@click.group()
def update():
    """Update patientMatcher resources"""
    pass


@update.command()
@click.option('--test', help='Use this flag to test the function',
  is_flag=True)
def resources(test):
    """Updates HPO terms and disease ontology from the web.
    Specifically collect files from:
    http://purl.obolibrary.org/obo/hp.obo
    http://compbio.charite.de/jenkins/job/hpo.annotations/lastStableBuild/artifact/misc/phenotype_annotation.tab
    """
    files = {}
    for key, item in PHENOTYPE_TERMS.items():
        url = item['url']
        destination = item['resource_path']
        r = requests.get(url, stream=True)
        total_length = int(r.headers.get('content-length'))
        if test:
            files[key] = total_length
            if total_length:
                click.echo('file {} found at the requested URL'.format(key))
                continue
                with open(destination, 'wb') as (f):
                    for chunk in progress.bar(r.iter_content(chunk_size=1024), expected_size=(total_length / 1024 + 1)):
                        if chunk:
                            f.write(chunk)
                            f.flush()