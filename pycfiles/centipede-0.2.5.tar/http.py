# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/centinel/primitives/http.py
# Compiled at: 2015-10-26 01:27:01
import logging, threading, time
from urlparse import urlparse
from http_helper import ICHTTPConnection

def _get_http_request(host, path='/', headers=None, ssl=False):
    """
    Actually gets the http. Moved this to it's own private method since
    it is called several times for following redirects

    :param host:
    :param path:
    :param headers:
    :param ssl:
    :return:
    """
    request = {'host': host, 'path': path, 
       'method': 'GET'}
    response = {}
    try:
        request['ssl'] = ssl
        conn = ICHTTPConnection(host=host, timeout=10)
        conn.request(path, headers, ssl, timeout=10)
        response['status'] = conn.getStatus()
        response['reason'] = conn.getReason()
        response['headers'] = conn.getHeaders()
        try:
            body = conn.getBody()
            response['body'] = body.encode('utf-8')
        except UnicodeDecodeError:
            response['body.b64'] = body.encode('base64')

    except Exception as err:
        response['failure'] = str(err)

    result = {'response': response, 'request': request}
    return result


def get_request(host, path='/', headers=None, ssl=False, external=None, url=None, log_prefix=''):
    http_results = {}
    first_response = _get_http_request(host, path, headers, ssl)
    if 'failure' in first_response['response']:
        if external is not None and type(external) is dict:
            external[url] = first_response
        return first_response
    logging.debug('%sSending HTTP GET request for %s.' % (log_prefix, url))
    stat_starts_with_3 = str(first_response['response']['status']).startswith('3')
    response_headers_contains_location = 'location' in first_response['response']['headers']
    is_redirecting = stat_starts_with_3 and response_headers_contains_location
    if is_redirecting:
        http_results['request'] = first_response['request']
        http_results['redirects'] = {}
        first_response_information = {'response': first_response['response'], 'host': host, 
           'path': path}
        http_results['redirects']['0'] = first_response_information
        redirect_http_result = None
        redirect_number = 1
        while redirect_http_result is None or stat_starts_with_3 and response_headers_contains_location and redirect_number < 6:
            if redirect_http_result is None:
                redirect_url = first_response['response']['headers']['location']
            else:
                redirect_url = redirect_http_result['response']['headers']['location']
            use_ssl = redirect_url.startswith('https://')
            parsed_url = urlparse(redirect_url)
            redirect_http_result = _get_http_request(parsed_url.netloc, parsed_url.path, ssl=use_ssl)
            del redirect_http_result['request']
            if 'failure' in redirect_http_result['response']:
                http_results['response'] = redirect_http_result['response']
                break
            stat_starts_with_3 = str(redirect_http_result['response']['status']).startswith('3')
            response_headers_contains_location = 'location' in redirect_http_result['response']['headers']
            if not stat_starts_with_3 or not response_headers_contains_location:
                http_results['response'] = redirect_http_result['response']
            else:
                redirect_information = {'host': parsed_url.netloc, 'path': parsed_url.path, 
                   'full_url': redirect_url, 
                   'response': redirect_http_result['response']}
                http_results['redirects'][str(redirect_number)] = redirect_information
            redirect_number += 1

    else:
        if external is not None and type(external) is dict:
            external[url] = first_response
        return first_response
    if external is not None and type(external) is dict:
        external[url] = http_results
    return http_results


def get_requests_batch(input_list, delay_time=0.5, max_threads=100):
    """
    This is a parallel version of the HTTP GET primitive.

    Params:
    input_list- the input is a list of either dictionaries containing
                query information, or just domain names (and NOT URLs).
    delay_time- delay before starting each thread
    max_threads- maximum number of concurrent threads

    Note: the input list can look like this:
    [
        { "host": "www.google.com",   "path": "/", "headers": [],
          "ssl": False, "url": "http://www.google.com/" },
        "www.twitter.com",
        "www.youtube.com",
        { "host": "www.facebook.com", "path": "/", "headers": [],
          "ssl": True, "url": "http://www.facebook.com" },
        ...
    ]

    """
    results = {}
    threads = []
    thread_error = False
    thread_wait_timeout = 200
    ind = 1
    total_item_count = len(input_list)
    for row in input_list:
        headers = []
        path = '/'
        ssl = False
        theme = 'http'
        if type(row) is dict:
            if 'host' not in row:
                continue
            host = row['host']
            if 'path' in row:
                path = row['path']
            if 'headers' in row:
                if type(row['headers']) is list:
                    headers = row['headers']
            if 'ssl' in row:
                ssl = row['ssl']
                theme = 'https'
            if 'url' in row:
                url = row['url']
            else:
                url = '%s://%s%s' % (theme, host, path)
        else:
            host = row
            url = '%s://%s%s' % (theme, host, path)
        wait_time = 0
        while threading.active_count() > max_threads:
            time.sleep(1)
            wait_time += 1
            if wait_time > thread_wait_timeout:
                thread_error = True
                break

        if thread_error:
            results['error'] = 'Threads took too long to finish.'
            break
        time.sleep(delay_time)
        log_prefix = '%d/%d: ' % (ind, total_item_count)
        thread = threading.Thread(target=get_request, args=(
         host, path, headers, ssl,
         results, url, log_prefix))
        ind += 1
        thread.setDaemon(1)
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join(thread_wait_timeout)

    return results