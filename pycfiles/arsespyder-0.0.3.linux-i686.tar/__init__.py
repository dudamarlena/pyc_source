# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/pyarsespyder/__init__.py
# Compiled at: 2013-09-22 14:31:28
import sys
from geturl import get_url_list
from validateurl import url_is_http
DEPTH_LEVEL_CHARACTER = '*'

def exit_error(error, error_code):
    """ 
    exit_error function prints an error and exit with code specified
   
    Keyword arguments:
    error -- The error to print on the screen
    error_code -- The error_code returned by the program

    """
    print ''
    print error
    print ''
    sys.exit(error_code)


def print_links_to_level(url, max_depth):
    """ 
    arsespyder main function. Receives a URL and the crawling depth
    and prints on screen the links of the url, the links of the links
    of the url, etc. up to the max_depth
   
    Keyword arguments:
    url -- A string with the URL to analyze
    max_depth -- The maximum depth of link analysis

    """
    if not url_is_http(url):
        exit_error('ERROR: URL provided must have HTTP/HTTPS scheme', 1)
    else:
        print_child_list(url, 1)
        recursive_analyze_links(url, 2, max_depth)


def recursive_analyze_links(url, depth, max_depth):
    """ 
    Recursive function that prints the links of the url and at leven depth,
    and if the max_depth has not been reached, continues analyzing to the
    next level
   
    Keyword arguments:
    url -- A string with the URL to analyze
    depth -- The crawling depth being analyzed
    max_depth -- The maximum depth of link analysis

    """
    url_list = get_url_list(url)
    if depth <= max_depth:
        for l in url_list:
            print_child_list(l, depth)

        for l in url_list:
            recursive_analyze_links(l, depth + 1, max_depth)


def print_child_list(url, depth):
    """ 
    Function to print all the links contained in a url, together with a 
    series of characters indicating the depth level of the link 
    being printed
   
    Keyword arguments:
    url -- A string with the URL to analyze
    depth -- The crawling depth being analyzed, needed for printing stuff

    """
    url_list = get_url_list(url)
    for l in url_list:
        if url_is_http(l):
            print_depth_point(depth)
            print ' %s' % l


def print_depth_point(depth):
    """ 
    Function to print as many 'level characters'. Default character is '*'
   
    Keyword arguments:
    depth -- The amount of 'depth level characters' to print

    """
    counter = 0
    while counter < depth:
        sys.stdout.write(DEPTH_LEVEL_CHARACTER)
        sys.stdout.flush()
        counter += 1