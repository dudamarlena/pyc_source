# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/graphgit/core.py
# Compiled at: 2013-02-12 14:41:59
import sys, os, logging, git, networkx as nx, constants

def safe_str(obj):
    """ return the byte string representation of obj """
    try:
        return str(obj)
    except UnicodeEncodeError:
        return unicode(obj).encode('unicode_escape')


def graph_repo(repo_url, output_loc, format='graphml'):
    """ generates a graph for a git repository """
    log = logging.getLogger('graphgit')
    local_repo = os.path.isabs(repo_url)
    repo_name = (local_repo or repo_url)[repo_url.rfind('/') + 1:repo_url.rfind('.git')] if 1 else repo_url[repo_url.rfind(os.sep) + 1:]
    log.info('Processing git repository: %s' % repo_name)
    repo_loc = (local_repo or os.path.join)(constants.REPO_DOWNLOAD_LOCATION, repo_name) if 1 else repo_url
    repo = None
    gitt = git.Git()
    try:
        repo = git.Repo(repo_loc, odbt=git.GitCmdObjectDB)
        log.info('Repository already cloned... Going ahead and using it...')
    except git.exc.NoSuchPathError:
        try:
            if local_repo:
                raise Exception
            log.info('Cloning repository... this might take some time, please wait !')
            gitt.clone(repo_url, repo_loc)
            log.info('Git clone completed...')
            repo = git.Repo(repo_loc, odbt=git.GitCmdObjectDB)
        except:
            log.error('Could not obtain repository: %s !' % repo_url)
            sys.exit(1)

    if repo is None:
        log.error('Could not obtain repository: %s !' % repo_url)
        sys.exit(1)
    G = nx.DiGraph()
    G.add_node(repo_name, type=constants.NODE_TYPE_VALS['REPOSITORY'])
    for branch in repo.branches:
        log.debug('Processing branch %s' % branch)
        G.add_node(branch, type=constants.NODE_TYPE_VALS['BRANCH'])
        G.add_edge(repo_name, branch, label=constants.EDGE_LABEL_VALS['REPOSITORY_BRANCH'])
        for commit in repo.iter_commits(branch):
            try:
                author = safe_str(commit.author)
                ts = commit.committed_date
                sha = safe_str(commit)
                log.debug('%s> %s --[commit]--> %s' % (branch, author, sha))
                G.add_node(author, type=constants.NODE_TYPE_VALS['PERSON'])
                G.add_node(sha, ts=ts, type=constants.NODE_TYPE_VALS['COMMIT'])
                G.add_edge(author, sha, label=constants.EDGE_LABEL_VALS['PERSON_COMMIT'])
                G.add_edge(branch, sha, label=constants.EDGE_LABEL_VALS['BRANCH_COMMIT'])
            except LookupError:
                log.warning('Could not process %s !' % commit)
                continue

    log.info('Graph built ! saving...')
    output_file_name = '%s.%s' % (repo_name, format)
    output_file_loc = os.path.join(output_loc, output_file_name)
    if format == 'graphml':
        nx.write_graphml(G, output_file_loc, encoding='utf-8')
    elif format == 'gexf':
        nx.write_gexf(G, output_file_loc, encoding='utf-8')
    else:
        log.error('Invalid output format: %s !' % format)
        sys.exit(1)
    log.info('Saved to %s !' % output_file_loc)
    return