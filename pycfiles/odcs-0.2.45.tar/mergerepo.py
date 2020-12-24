# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hanzz/releases/odcs/server/odcs/server/mergerepo.py
# Compiled at: 2019-03-11 05:08:52
import os, requests
from xml.etree import ElementTree
from concurrent.futures import ThreadPoolExecutor
from datetime import timedelta
from six.moves.urllib.parse import urlparse
from distutils.spawn import find_executable
from flufl.lock import Lock
from odcs.server import log, conf
from odcs.server.utils import makedirs, execute_cmd

class MergeRepo(object):

    def __init__(self, compose):
        self.compose = compose

    def _download_file(self, path, url):
        """
        Downloads repodata file, stores it into `path`/repodata and returns
        its content.

        :param str path: Path to store the file to.
        :param str url: URL of file to download.
        :rtype: str
        :return: content of downloaded file.
        """
        log.info('%r: Downloading %s', self.compose, url)
        r = requests.get(url)
        r.raise_for_status()
        filename = os.path.basename(url)
        makedirs(os.path.join(path, 'repodata'))
        with open(os.path.join(path, 'repodata', filename), 'wb') as (f):
            f.write(r.content)
        return r.content

    def _download_repodata(self, path, baseurl):
        """
        Downloads the repodata from `baseurl` to `path`.

        :param str path: Path to store the file to.
        :param str baseurl: Base URL of repository to download.
        """
        last_repomd = None
        repodata_path = os.path.join(path, 'repodata')
        repomd_path = os.path.join(repodata_path, 'repomd.xml')
        if os.path.exists(repomd_path):
            with open(repomd_path, 'r') as (f):
                last_repomd = f.read()
        repomd_url = os.path.join(baseurl, 'repodata', 'repomd.xml')
        repomd = self._download_file(path, repomd_url)
        tree = ElementTree.fromstring(repomd)
        if repomd == last_repomd:
            log.info('%r: Reusing cached repodata for %s', self.compose, baseurl)
            return
        else:
            for f in os.listdir(repodata_path):
                if f == 'repomd.xml':
                    continue
                os.unlink(os.path.join(repodata_path, f))

            ns = '{http://linux.duke.edu/metadata/repo}'
            with ThreadPoolExecutor(5) as (downloader):
                for data in tree.findall('%sdata' % ns):
                    if data.get('type').endswith('_db'):
                        continue
                    data_location = data.find('%slocation' % ns).get('href')
                    data_url = os.path.join(baseurl, data_location)
                    downloader.submit(self._download_file, path, data_url)

            return

    def run(self, arch, repos, repo_name):
        """
        Merges multiple RPM repositories and stores the output to
        `os.path.join(compose.result_repo_dir, repo_name, arch)`.

        Raises an RuntimeError in case of error.

        :param str arch: Architecture of RPMs in repositories.
        :param list repos: List of URLs pointing to repos to merge.
        :param str repo_name: Name of the repository defining the subdirectory
            in `compose.result_repo_dir`.
        """
        locks = []
        repo_paths = []
        parsed_url = urlparse(repos[0])
        repo_prefix = '%s://%s' % (parsed_url.scheme, parsed_url.hostname)
        repo_prefix = repo_prefix.strip('/') + '/'
        for repo in repos:
            repo_path = os.path.join(conf.target_dir, 'pulp_repo_cache', repo.replace(repo_prefix, ''))
            repo_paths.append(repo_path)
            makedirs(repo_path)
            lock = Lock(os.path.join(repo_path, 'lock'))
            lock.lifetime = timedelta(minutes=30)
            locks.append(lock)

        try:
            for lock in locks:
                lock.lock()

            for repo, repo_path in zip(repos, repo_paths):
                self._download_repodata(repo_path, repo)

            log.info('%r: Starting mergerepo_c: %r', self.compose, repo_paths)
            mergerepo_exe = find_executable('mergerepo_c')
            if not mergerepo_exe:
                raise RuntimeError('mergerepo_c is not available on system')
            result_repo_dir = os.path.join(self.compose.result_repo_dir, repo_name, arch)
            makedirs(result_repo_dir)
            args = [
             mergerepo_exe, '--method', 'nvr', '-o',
             result_repo_dir]
            args += ['--repo-prefix-search', os.path.join(conf.target_dir, 'pulp_repo_cache')]
            args += ['--repo-prefix-replace', repo_prefix]
            for repo in repo_paths:
                args.append('-r')
                args.append(repo)

            execute_cmd(args)
        finally:
            for lock in locks:
                if lock.is_locked:
                    lock.unlock()