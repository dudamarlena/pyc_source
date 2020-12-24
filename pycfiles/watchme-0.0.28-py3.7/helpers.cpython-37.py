# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/watchme/watchers/urls/helpers.py
# Compiled at: 2020-04-10 14:08:50
# Size of source mod 2**32: 5295 bytes
"""

Copyright (C) 2019-2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
import requests, re

def get_params(kwargs, key='url_param_'):
    """a general function to get parameter sets based on a user input. 
       Returns a list of dictionaries, one per set.

       Parameters
       ==========
       kwargs: the dictionary of keyword arguments that may contain url
               parameters (format is url_param_<name>
       key: the string that the parameters start with (defaults to url_param)
    """
    params = {}
    names = [x for x in kwargs if x.startswith(key)]
    for _, name in enumerate(names):
        paramlist = kwargs.get(name).split(',')
        name = name.replace(key, '', 1)
        for i, _ in enumerate(paramlist):
            if i not in params:
                params[i] = {}
            if paramlist[i] != '':
                params[i][name] = paramlist[i]

    params = [x for x in params.values()]
    if len(params) == 0:
        params = [{}]
    return params


def parse_success_response(response, kwargs):
    """parse a successful response of 200, meaning we honor the user
       request to return json, search for a regular expression, or return
       raw text. This is used by the basic GET/POST functions. For parsing
       with beautiful soup, see "get_results" and "get_url_selection"

       Parameters
       ==========
       response: the requests (200) response
       kwargs: dictionary of keyword arguments provided to function
    """
    result = None
    save_as = kwargs.get('save_as', 'json')
    regex = kwargs.get('regex')
    if save_as == 'json':
        result = response.json()
    else:
        if regex not in ('', None):
            match = re.search(regex, response.text)
            result = match.group()
        else:
            result = response.text
    return result


def get_headers(kwargs):
    """Get a single set of headers from the kwargs dict. A user agent is added
       as it is helpful in most cases.

       Parameters
       ==========
       kwargs: the dictionary of keyword arguments that may contain url
               parameters (format is url_param_<name>
    """
    headers = {'User-Agent': 'Mozilla/5.0'}
    for key, value in kwargs.items():
        if key.startswith('header_'):
            name = key.replace('header_', '', 1)
            if value is not None:
                headers[name] = value
            elif value is None and name in headers:
                del headers[name]

    return headers


def get_results(url, selector, func=None, attributes=None, params=None, get_text=False, headers=None, regex=None):
    """given a url, a function, an optional selector, optional attributes, 
       and a set (dict) of parameters, perform a request. This function is
       used if the calling function needs special parsing of the html with
       beautiful soup. If only a post/get is needed, this is not necessary.

       Parameters
       ==========
       url: the url to get (required)
       func: the function to use, defaults to requests.get
       selector:  selection for the html response
       attributes: optional, a list of attributes
       params: a dictionary of parameters
       headers: a dictionary of header key value pairs
    """
    from bs4 import BeautifulSoup
    if params is None:
        params = {}
    if headers is None:
        headers = {}
    if func is None:
        func = requests.get
    response = func(url, params=params, headers=headers)
    results = []
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'lxml')
        for entry in soup.select(selector):
            if attributes is not None:
                [results.append(entry.get(x)) for x in attributes]
            elif regex not in (None, ''):
                match = re.search(regex, entry.text)
                results.append(match.group())
            elif get_text:
                results.append(entry.text)
            else:
                results.append(str(entry))

    results = [x for x in results if x]
    return results