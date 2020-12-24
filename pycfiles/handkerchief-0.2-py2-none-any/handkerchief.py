# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jreinhardt/sources/handkerchief/handkerchief/handkerchief.py
# Compiled at: 2016-03-10 14:05:34
import argparse, requests, json, subprocess, re, base64, getpass, glob, os
from sys import exit
from string import Template
from codecs import open
from jinja2 import Environment, FileSystemLoader, BaseLoader, PackageLoader
from os.path import join, realpath, dirname
from pkg_resources import resource_string
re_mote = re.compile('([a-zA-Z0-9_]*)\\s*((git@github.com\\:)|(https://github.com/))([a-zA-Z0-9_/]*)\\.git\\s*\\(([a-z]*)\\)')
issue_url = 'https://api.github.com/repos/%s/issues?state=%s&filter=all&direction=asc'
issue_last_re = '<https://api.github.com/repositories/([0-9]*)/issues\\?state=%s&filter=all&direction=asc&page=([0-9]*)>; rel="last"'
comment_url = 'https://api.github.com/repos/%s/issues/comments?'
comment_last_re = '<https://api.github.com/repositories/([0-9]*)/issues/comments\\?page=([0-9]*)>; rel="last"'
comment_issue_re = 'https://github.com/%s/issues/([0-9]*)#issuecomment-[0-9]*'
label_url = 'https://api.github.com/repos/%s/labels?'
label_last_re = '<https://api.github.com/repositories/([0-9]*)/labels\\?page=([0-9]*)>; rel="last"'
milestone_url = 'https://api.github.com/repos/%s/milestones?'
milestone_last_re = '<https://api.github.com/repositories/([0-9]*)/milestones\\?page=([0-9]*)>; rel="last"'
assignee_url = 'https://api.github.com/repos/%s/assignees?'
assignee_last_re = '<https://api.github.com/repositories/([0-9]*)/assignees\\?page=([0-9]*)>; rel="last"'
repo_url = 'https://api.github.com/repos/%s?'
file_url = 'https://api.github.com/repos/%s/contents/%s'
avatar_style = 'div.%s {background-image: url(data:image/png;base64,%s); background-size: 100%% 100%%;}\n'
repo_marker_re = '<!--\\s*([^\\s]*)\\s-->'

def get_github_content(repo, path, auth=None):
    """
        Retrieve text files from a github repo
        """
    request = requests.get(file_url % (repo, path), auth=auth)
    if not request.ok:
        print 'There is a problem with the request'
        print file_url % (repo, path)
        print request.json()
        exit(1)
    if not request.json()['encoding'] == 'base64':
        raise RuntimeError('Unknown Encoding encountered when fetching %s from repo %s: %s' % (path, repo, request.json()['encoding']))
    return request.json()['content'].decode('base64').decode('utf8')


class GitHubLoader(BaseLoader):
    """
        A loader for Jinja templates that fetches them from a GitHub repository
        """

    def __init__(self, repo, layout, auth=None):
        self.repo = repo
        self.layout = layout
        self.auth = auth

    def get_source(self, environment, template):
        source = get_github_content(self.repo, 'layouts/%s/%s' % (self.layout, template), self.auth)
        return (source, None, lambda : False)


class Layout:

    def __init__(self, layout):
        self.layout = layout
        self.js = []
        self.css = []
        self.template = None
        return

    def init_local(self, layout_dir):
        layout_root = join(layout_dir, self.layout)
        with open(join(layout_root, '%s.json' % self.layout), 'r', 'utf8') as (fid):
            params = json.load(fid)
        env = Environment(loader=FileSystemLoader(layout_root))
        self.template = env.get_template(params['html'])
        for n in params['js']:
            self.js.append({'name': n, 
               'content': open(join(layout_root, n), 'r', 'utf8').read()})

        for n in params['css']:
            self.css.append(open(join(layout_root, n), 'r', 'utf8').read())

    def init_remote(self, auth):
        repo = 'jreinhardt/handkerchief'
        layout_root = join('layouts', self.layout)
        params = get_github_content(repo, join(layout_root, '%s.json' % self.layout), auth)
        params = json.loads(params)
        env = Environment(loader=GitHubLoader(repo, self.layout, auth))
        self.template = env.get_template(params['html'])
        for n in params['js']:
            self.js.append({'name': n, 
               'content': get_github_content(repo, join(layout_root, n), auth)})

        for n in params['css']:
            self.css.append(get_github_content(repo, join(layout_root, n), auth))

    def init_package(self):
        layout_root = join('layouts', self.layout)
        package = 'handkerchief'
        p = resource_string(__name__, join(layout_root, '%s.json' % self.layout))
        params = json.loads(p.decode('utf8'))
        env = Environment(loader=PackageLoader(package, layout_root))
        self.template = env.get_template(params['html'])
        for n in params['js']:
            self.js.append({'name': n, 
               'content': resource_string(__name__, join(layout_root, n)).decode('utf8')})

        for n in params['css']:
            self.css.append(resource_string(__name__, join(layout_root, n)).decode('utf8'))


def get_all_pages(url, re_last_page, auth=None):
    url_temp = url + '&page=%d'
    data = []
    i = 1
    request = requests.get(url_temp % i, auth=auth)
    if not request.ok:
        print 'There is a problem with the request'
        print url_temp % i
        print request
        exit(1)
    data += request.json()
    if 'link' not in request.headers:
        return data
    else:
        result = re.match(re_last_page, request.headers['link'].split(',')[(-1)].strip())
        if result is None:
            print request.headers['link']
        last_page = int(result.group(2))
        for i in range(2, last_page + 1):
            request = requests.get(url_temp % i, auth=auth)
            data += request.json()

        return data
        return


def fetch_issue_data(reponame, auth, local_avatars, states):
    data = {}
    data['reponame'] = reponame
    try:
        data['issues'] = []
        for state in states:
            data['issues'] += get_all_pages(issue_url % (reponame, state), issue_last_re % state, auth)

        repo_request = requests.get(repo_url % reponame, auth=auth)
        if not repo_request.ok:
            print 'There is a problem with the request'
            print repo_url % reponame
            print repo_request
            exit(1)
        data['repo'] = repo_request.json()
        comments = get_all_pages(comment_url % reponame, comment_last_re, auth)
        data['labels'] = get_all_pages(label_url % reponame, label_last_re, auth)
        data['milestones'] = get_all_pages(milestone_url % reponame, milestone_last_re, auth)
        data['assignees'] = get_all_pages(assignee_url % reponame, assignee_last_re, auth)
    except requests.exceptions.ConnectionError:
        print 'Could not connect to GitHub. Please check your internet connection'
        exit(1)

    data['javascript'] = []
    data['stylesheets'] = []
    if local_avatars:
        av_style = ''
        avatars = []
        for item in comments + data['issues']:
            url = item['user']['avatar_url']
            avclass = 'avatar_' + item['user']['login']
            if avclass not in avatars:
                r = requests.get(url, auth=auth)
                if r.status_code == 200:
                    av_style += avatar_style % (avclass, base64.b64encode(r.content))
                    avatars.append(avclass)
            item['user']['avatar_class'] = avclass

        data['stylesheets'].append(av_style)
    for issue in data['issues']:
        issue['comments_list'] = []

    for comment in comments:
        match = re.match(comment_issue_re % reponame, comment['html_url'])
        if match is not None:
            for issue in data['issues']:
                if int(issue['number']) == int(match.group(1)):
                    issue['comments_list'].append(comment)
                    break

    for issue in data['issues']:
        issue['labelnames'] = [ l['name'] for l in issue['labels'] ]

    return data


def collect_reponames():
    """
        Try to figure out a list of repos to consider by default from the contents of the working directory.
        """
    reponames = []
    try:
        with open(os.devnull) as (devnull):
            remote_data = subprocess.check_output(['git', 'remote', '-v', 'show'], stderr=devnull)
        branches = {}
        for line in remote_data.split('\n'):
            if line.strip() == '':
                continue
            remote_match = re_mote.match(line)
            if remote_match is not None:
                branches[remote_match.group(1)] = remote_match.group(5)

        if len(branches) > 0:
            if 'origin' in branches:
                reponames.append(branches['origin'])
            else:
                reponames.append(branches.values()[0])
    except OSError:
        pass
    except subprocess.CalledProcessError:
        pass

    for fname in glob.iglob('*.html'):
        fid = open(fname, 'r', 'utf8')
        fid.readline()
        line = fid.readline()
        match = re.match(repo_marker_re, line)
        if match is not None:
            reponames.append(match.group(1))
        reponames = list(set(reponames))

    return reponames


def main():
    reponames = collect_reponames()
    parser = argparse.ArgumentParser('Download GitHub Issues into self-contained HTML file')
    parser.add_argument('-o', dest='outname', default=None, help='filename of output HTML file')
    parser.add_argument('-l', dest='layout', default='default', help='name of a layout to use')
    parser.add_argument('-q', dest='verbose', default='store_false', help='suppress output to stdout')
    parser.add_argument('--state', dest='state', default='all', choices=['all', 'open', 'closed'], help='download issues of this state only')
    parser.add_argument('--layout-dir', dest='layout_dir', default=None, help='use layouts from the given directory, useful during development')
    parser.add_argument('--remote-layouts', dest='remote_layouts', action='store_true', help='get layouts from GitHub, useful standalone script standalone mode')
    parser.add_argument('-a', dest='auth', action='store_true', help='authenticate, is sometimes necessary to avoid rate limiting')
    parser.add_argument('--user', help='Username for authentication', default=os.environ.get('GITHUB_USERNAME'))
    parser.add_argument('--token', help='Use Github token for authentication instead of password', default=os.environ.get('GITHUB_ACCESS_TOKEN'))
    parser.add_argument('--no-local-avatars', dest='local_avatars', action='store_false', help='do not embed avatars, leads to smaller results')
    parser.add_argument('reponame', default=reponames, nargs='*', help='GitHub repo in the form username/reponame. If not given, handkerchief guesses')
    args = parser.parse_args()
    if len(args.reponame) == 0:
        print 'No repository was given and handkerchief failed to guess one'
        exit(1)
    if len(args.reponame) > 1 and args.outname is not None:
        print 'Output filename is impossible if multiple repos are given'
        exit(1)
    if args.token or args.auth:
        username = args.user or raw_input('Username: ')
        if args.token:
            auth = (
             username, args.token)
        else:
            auth = (
             username, getpass.getpass())
    else:
        auth = None
    layout = Layout(args.layout)
    if args.layout_dir:
        layout.init_local(args.layout_dir)
    else:
        if args.remote_layouts:
            layout.init_remote(auth)
        else:
            try:
                layout.init_package()
            except Exception as e:
                print e
                layout.init_remote(auth)

        for repo in args.reponame:
            if args.verbose:
                print 'Fetching data for %s ...' % repo
            if args.state == 'all':
                states = [
                 'open', 'closed']
            else:
                states = [
                 args.state]
            data = fetch_issue_data(repo, auth, args.local_avatars, states)
            data['javascript'] += layout.js
            data['stylesheets'] += layout.css
            outname = args.outname or 'issues-%s.html' % repo.split('/')[1]
            with open(outname, 'w', 'utf8') as (fid):
                fid.write(layout.template.render(data))

    return


if __name__ == '__main__':
    main()