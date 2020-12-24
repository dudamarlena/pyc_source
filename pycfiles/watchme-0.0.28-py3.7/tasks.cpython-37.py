# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/watchme/watchers/urls/tasks.py
# Compiled at: 2020-04-10 14:08:50
# Size of source mod 2**32: 5413 bytes
"""

Copyright (C) 2019-2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
from watchme.logger import bot
from .helpers import get_params, get_results, get_headers, parse_success_response
import os, tempfile, requests

def get_task(url, **kwargs):
    """a simple task to use requests to get a url. By default, we return
       the raw response.

       Parameters
       ==========

       REQUIRED:
           url: a url to return the page for

       OPTIONAL
           regex: a regular expression to search the text for (not used w/ json)
           save_as: return the result to save as json
    """
    results = []
    paramsets = get_params(kwargs)
    headers = get_headers(kwargs)
    for params in paramsets:
        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 200:
            result = parse_success_response(response, kwargs)
            results.append(result)

    results = [x for x in results if x]
    if not results:
        results = None
    return results


def post_task(url, **kwargs):
    """a simple task to use requests to post to. By default, we return json.

       Parameters
       ==========

       REQUIRED:
           url: a url to post to
    """
    results = []
    jsonlist = get_params(kwargs, key='json_param_')
    headers = get_headers(kwargs)
    for params in jsonlist:
        response = requests.post(url, json=params, headers=headers)
        if response.status_code == 200:
            result = parse_success_response(response, kwargs)
            results.append(result)
        else:
            bot.error('%s: %s' % (response.status_code, response.reason))

    results = [x for x in results if x]
    if not results:
        results = None
    return results


def download_task(url, **kwargs):
    """a simple task to use requests to get a url. By default, we return
       the raw response.

       Parameters
       ==========

       REQUIRED:
           url: a url to download (stream)

       OPTIONAL:
           write_format: to change from default "w"
           disable_ssl_check: set to anything to not verify (not recommended)
    """
    result = None
    bot.verbose('Downloading %s' % url)
    file_name = kwargs.get('file_name', os.path.basename(url))
    destination = os.path.join(tempfile.gettempdir(), file_name)
    verify = True
    if 'disable_ssl_check' in kwargs:
        if kwargs['disable_ssl_check']:
            bot.warning('Verify of certificates disabled! ::TESTING USE ONLY::')
            verify = False
    fmt = kwargs.get('write_format', 'wb')
    headers = get_headers(kwargs)
    if requests.head(url, verify=verify, headers=headers).status_code in (200, 401):
        response = requests.get(url, verify=verify, stream=True, headers=headers)
        if response.status_code == 401:
            return result
        if response.status_code == 200:
            chunk_size = 1048576
            with open(destination, fmt) as (filey):
                for chunk in response.iter_content(chunk_size=chunk_size):
                    filey.write(chunk)

            result = destination
    return result


def get_url_selection(url, **kwargs):
    """select some content from a page dynamically, using selenium.

       Parameters
       ==========
       kwargs: a dictionary of key, value pairs provided by the user
    """
    results = None
    selector = kwargs.get('selection', None)
    headers = get_headers(kwargs)
    if selector is None:
        bot.error('You must define the selection (e.g., selection@.main')
        return results
    get_text = False
    if kwargs.get('get_text') is not None:
        get_text = True
    regex = kwargs.get('regex')
    attributes = kwargs.get('attributes', None)
    if attributes is not None:
        attributes = attributes.split(',')
    paramsets = get_params(kwargs)
    results = []
    for params in paramsets:
        results += get_results(url=url,
          selector=selector,
          headers=headers,
          attributes=attributes,
          params=params,
          get_text=get_text,
          regex=regex)

    if not results:
        results = None
    return results