# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/link_validator/link_validator.py
# Compiled at: 2015-05-29 10:33:01
import urllib2, urlparse, argparse, requests, json
from bs4 import BeautifulSoup
from termcolor import colored
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from requests.packages.urllib3.exceptions import InsecurePlatformWarning
broken_link_list = []
visited_links = {}

def print_colored_status(link, status):
    if status == 200:
        print '%s => %s' % (link, colored(status, 'green'))
    elif status < 400:
        print '%s => %s' % (link, colored(status, 'yellow'))
    else:
        print '%s => %s' % (link, colored(status, 'red'))


def get_broken_links(address, max_depth=2, depth=1):
    global broken_link_list
    global visited_links
    base_address_no_scheme = urlparse.urlparse(address).netloc
    base_address = urlparse.urlparse(address).scheme + '://' + base_address_no_scheme
    user_agent = 'Link Validator https://github.com/at1as/link-validator'
    r = requests.get(address, verify=False, headers={'User-Agent': user_agent}, allow_redirects=True)
    html_object = BeautifulSoup(r.text)
    for link in html_object.find_all('a'):
        try:
            inner_link = link.get('href')
            print 'Origin: %s' % address
            print 'Link: %s' % inner_link
        except:
            pass

        if inner_link is not None:
            if inner_link and not inner_link.startswith('www') and not inner_link.startswith('http'):
                inner_link = urlparse.urljoin(address, inner_link)
            inner_link = inner_link.split('#')[0]
            if visited_links.has_key(inner_link):
                print 'Result: %s was already searched.' % inner_link, colored('Skipping.', 'yellow')
            elif inner_link and ('mailto:' or 'tel:') in inner_link:
                print 'Result: multimedia address. %s' % colored('Skipping.', 'yellow')
            else:
                try:
                    link_follow = requests.get(inner_link, verify=False, headers={'User-Agent': user_agent}, allow_redirects=True)
                    if link_follow.status_code >= 400:
                        broken_link_list.append([address, inner_link, link_follow.status_code])
                        print 'BLL: %s' % broken_link_list
                        visited_links[inner_link] = link_follow.status_code
                        print 'Result: ', inner_link, colored(': broken link', 'red'), link_follow.status_code
                    else:
                        print 'Result: ', inner_link, colored(': valid link', 'green')
                        visited_links[inner_link] = link_follow.status_code
                        if depth < max_depth:
                            domain = urlparse.urlparse(inner_link).netloc
                            print 'Depth: Transcended %d / %d levels' % (depth, max_depth)
                            if base_address_no_scheme in domain:
                                print '\n---\n'
                                get_broken_links(inner_link, max_depth, depth + 1)
                            else:
                                print 'External Link %s' % colored('stopping recursion', 'yellow')
                        else:
                            print 'Depth: Transcended %d / %d levels. %s' % (depth, max_depth, colored('Stopping recusion', 'yellow'))
                except Exception as e:
                    print '%s: not searchable %s Exception: %s' % (inner_link, colored('uncontrolled failure.', 'red'), e)

        else:
            print 'Link does not contain an "href" tag %s' % colored('skipping', 'yellow')
        print '\n---\n'

    return


def main():
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    requests.packages.urllib3.disable_warnings(InsecurePlatformWarning)
    parser = argparse.ArgumentParser(description='Recursive Link validator')
    parser.add_argument('--url', required=True, help='the url of the website to test against (ex. "http://www.w3.org/TR/html401/struct/links.html)')
    parser.add_argument('--depth', required=False, default=2, type=int, help='depth of recursion to search child links. Value > 2 will slow script down a lot (ex. 2)')
    args = parser.parse_args()
    user_args = vars(args)
    if not user_args['url'].lower().startswith('http'):
        user_args['url'] = 'http://%s' % user_args['url']
    print '\n'
    get_broken_links(user_args['url'], user_args['depth'])
    print '----\nResults:'
    print '\n>> Starting Link:\n%s' % user_args['url']
    print '\n>> Visited Links:'
    for link, status in sorted(visited_links.items(), key=lambda x: x[1]):
        print_colored_status(link, status)

    print '\n>> Broken Links:'
    for broken_link in broken_link_list:
        print 'Origin : %s Link : %s => %s' % (broken_link[0], broken_link[1], colored(broken_link[2], 'red'))

    if len(broken_link_list) == 0:
        print 'None!'
    print '\n'


if __name__ == '__main__':
    main()