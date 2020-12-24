# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/dame/downloader.py
# Compiled at: 2020-05-04 13:31:17
# Size of source mod 2**32: 1309 bytes
import http, json, urllib3
from dame.utils import check_is_none
import certifi
http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED',
  ca_certs=(certifi.where()))
chunk_size = 65536

def check_size(url):
    r = http.request('GET', url, preload_content=False)
    content_bytes = r.headers.get('Content-Length')
    r.release_conn()
    return content_bytes


def parse_inputs(model, thread):
    inputs = []
    for input in thread.models[model]['input_files']:
        available_resources = check_is_none(check_is_none(input, 'value'), 'resources')
        for r in available_resources:
            if check_is_none(r, 'selected'):
                download_url = check_is_none(r, 'url')
                input['download_url'] = download_url

        inputs.append(input)

    return inputs


def parse_outputs(model, thread, results):
    outputs = []
    for output in thread.models[model]['output_files']:
        name = check_is_none(output, 'name')
        if name in results[0]:
            output['download_url'] = results[0][name]
            outputs.append(output)

    return outputs


def get_json(url):
    r = http.request('GET', url)
    data = json.loads(r.data.decode('utf-8'))
    r.release_conn()
    return data