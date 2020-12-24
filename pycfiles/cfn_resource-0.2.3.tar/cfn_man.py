# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/cfn_man/cfn_man.py
# Compiled at: 2018-09-13 13:48:06
import requests, urllib, sys, os, lxml.html as html
from random import randint
from subprocess import check_output
import pydoc

def build_search_url(query):
    """ Builds a Google search url

    Args:
        query (str): a query string to use when searching cloudformation docs

    Returns:
        str: the Google 'I'm feeling lucky' URL
    """
    google_url = []
    google_url.append('https://www.google.com/search?')
    google_url.append('btnI=1')
    google_url.append('&as_sitesearch=docs.aws.amazon.com')
    query = 'aws cloudformation ' + query
    query = urllib.quote_plus(query.strip())
    google_url.append('&q=')
    google_url.append(query)
    return ('').join(google_url)


def get_docs_html_content(url):
    """ Get a webpage and extract relevant HTML for cloudformation documentation

    Args:
        url (str): url for cloudformation docs

    Returns:
        str: HTML of the page, stripped down to a minimum
    """
    want_tags = [
     'p', 'h1', 'h2', 'h3', 'div']
    want_divs = [
     'variablelist', 'aws-note', 'YAML']
    response = requests.get(url, proxies=urllib.getproxies())
    parsed = html.fromstring(response.text)
    try:
        main_content = parsed.get_element_by_id('main-col-body')
    except KeyError:
        print 'Sorry! Did not find a document.'
        print url
        exit(1)

    content = []
    for el in main_content:
        if el.tag not in want_tags or el.tag == 'div' and not ('class' in el.attrib.keys() and el.attrib['class'] in want_divs or 'id' in el.attrib.keys() and el.attrib['id'] in want_divs):
            continue
        content.append(html.tostring(el))

    return ('').join(content)


def format_html_content(content):
    """ Given HTML, render for reading in a terminal

    Args:
        content (str): HTML as a string

    Returns:
        str: Rendered document, all HTML removed using 'links' command line utility
    """
    temp_file = str(randint(0, 10000000000)) + '-tmp-cfn-man.html'
    try:
        try:
            with open(temp_file, 'w') as (f):
                f.write(content)
            return check_output(['links', '-dump', temp_file])
        except OSError as e:
            if 'No such file or directory' in str(e):
                print "Please make sure the command line utility 'links' is installed"
                exit(1)
            raise e

    finally:
        os.remove(temp_file)


def main():
    if len(sys.argv) < 2:
        print 'usage:\ncfn_docs security group\ncfn_docs ec2'
        exit(1)
    query = []
    for arg in sys.argv[1:]:
        query.append(arg)
        query.append(' ')

    url = build_search_url(('').join(query))
    html_content = get_docs_html_content(url)
    doc = format_html_content(html_content)
    pydoc.pager(doc)