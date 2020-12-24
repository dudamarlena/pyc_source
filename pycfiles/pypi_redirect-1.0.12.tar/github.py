# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.8-x86_64/egg/pypi_rankings/crawlers/github.py
# Compiled at: 2015-02-17 04:35:44
import requests, time, re
from progress import Progress
MAX_REPOS = 100
AUTH = None

def cleanup_url(url):
    url = url.lower()
    url = url.replace('github.com:', 'github.com/')
    url = url.replace('github.io', 'github.com')
    url = url.replace('github.org', 'github.com')
    url = url.split('://')[(-1)]
    url = url.split('www.')[(-1)]
    if not url.startswith('github.com'):
        matchobj = re.search('([^/.]+)\\.github\\.com/(.+)', url)
        if matchobj:
            url = ('/').join(matchobj.groups())
    url = url.split('github.com/')[(-1)]
    url = url.split('#')[0]
    url = url.rstrip('/')
    if url.endswith('.git'):
        url = url[:-4]
    url = ('/').join(url.split('/')[:2])
    if len(url) == 0 or not url[(-1)].isalnum():
        return None
    else:
        return url


def get_github_list(conn):
    repo_cursor = conn.execute("SELECT name, homepage FROM packages WHERE LOWER(homepage) LIKE '%github.%'")
    res = [ (repo, cleanup_url(url)) for repo, url in repo_cursor ]
    return [ (repo, url) for repo, url in res if url is not None ]


def build_url(current_list):
    url = 'https://api.github.com/search/repositories?per_page=100&q='
    for name, repo in current_list:
        url += ('repo:{}\n').format(repo)

    return url


def save_data(conn, github_json, current_list):
    for github_repo_info in github_json['items']:
        repo_part = github_repo_info['html_url'].split('github.com/')[(-1)]
        package_name = [ name for name, repo in current_list if repo.lower() == repo_part.lower()
                       ]
        if len(package_name) == 0:
            continue
        conn.execute('REPLACE INTO scm(name, type, url, open_issues, last_change, crawl_time) VALUES (?, ?, ?, ?, ?, ?)', (
         package_name[0],
         'github',
         github_repo_info['html_url'],
         github_repo_info['open_issues'],
         github_repo_info['pushed_at'],
         time.time()))

    conn.commit()


def get_rate_limit():
    url = 'https://api.github.com/rate_limit'
    return requests.get(url, auth=AUTH).json()['resources']['search']['remaining']


def crawl(conn, crawl_count=1):
    github_list = get_github_list(conn)
    start = 0
    rate_limit = get_rate_limit()
    total_count = len(github_list)
    progress = Progress('github', crawl_count, total_count)
    progress.start()
    while start < total_count:
        current_list = github_list[start:start + MAX_REPOS]
        repo_count = len(current_list)
        url = build_url(current_list)
        github_json = requests.get(url, auth=AUTH).json()
        if 'items' in github_json:
            save_data(conn, github_json, current_list)
        progress.parse_count += repo_count
        rate_limit -= 1
        while rate_limit <= 0:
            time.sleep(5)
            rate_limit = get_rate_limit()

        start += repo_count

    progress.stop()


if __name__ == '__main__':
    from . import get_conn
    conn = get_conn()
    crawl(conn)