# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/qgispluginci/release.py
# Compiled at: 2020-05-01 10:08:01
# Size of source mod 2**32: 13932 bytes
import os, sys, git, tarfile, zipfile
from tempfile import mkstemp
from glob import glob
from github import Github, GithubException
import xmlrpc.client, re, warnings
try:
    import importlib.resources as importlib_resources
except ImportError:
    import importlib_resources

import datetime, pyqt5ac
from qgispluginci.parameters import Parameters
from qgispluginci.translation import Translation
from qgispluginci.utils import replace_in_file, configure_file
from qgispluginci.exceptions import GithubReleaseNotFound, GithubReleaseCouldNotUploadAsset, UncommitedChanges

def release(parameters: Parameters, release_version: str, release_tag: str=None, github_token: str=None, upload_plugin_repo_github: str=False, transifex_token: str=None, osgeo_username: str=None, osgeo_password: str=None, allow_uncommitted_changes: bool=False):
    """
    
    Parameters
    ----------
    parameters
        The configuration parameters 
    release_version: 
        The release version (x.y.z)
    release_tag:
        The release tag (vx.y.z).
        If not given, the release version will be used
    github_token
        The Github token
    upload_plugin_repo_github
        If true, a custom repo will be created as a release asset on Github and could later be used in QGIS as a custom plugin repository.
    transifex_token
        The Transifex token
    osgeo_username
        osgeo username to upload the plugin to official QGIS repository
    osgeo_password
        osgeo password to upload the plugin to official QGIS repository
    allow_uncommitted_changes
        If False, uncommitted changes are not allowed before packaging/releasing.
        If True and some changes are detected, a hard reset on a stash create will be used to revert changes made by qgis-plugin-ci.
    """
    if transifex_token is not None:
        tr = Translation(parameters, create_project=False, transifex_token=transifex_token)
        tr.pull()
        tr.compile_strings()
    else:
        archive_name = parameters.archive_name(release_version)
        is_prerelease = False
        if github_token is not None:
            is_prerelease = release_is_prerelease(parameters, release_tag=release_version, github_token=github_token)
        print('*** is pre-release: {}'.format('YES' if is_prerelease else 'NO'))
        create_archive(parameters,
          release_version, archive_name, add_translations=(transifex_token is not None),
          allow_uncommitted_changes=allow_uncommitted_changes,
          is_prerelease=is_prerelease)
        experimental_archive_name = None
        if osgeo_username is not None:
            if is_prerelease:
                experimental_archive_name = parameters.archive_name(release_version, True)
                create_archive(parameters,
                  release_version, experimental_archive_name, add_translations=(transifex_token is not None),
                  allow_uncommitted_changes=allow_uncommitted_changes,
                  is_prerelease=True,
                  raise_min_version='3.14')
        if github_token is not None:
            upload_asset_to_github_release(parameters,
              asset_path=archive_name, release_tag=release_version, github_token=github_token)
            if upload_plugin_repo_github:
                xml_repo = create_plugin_repo(parameters=parameters,
                  release_version=release_version,
                  release_tag=release_tag,
                  archive=archive_name,
                  osgeo_username=osgeo_username)
                upload_asset_to_github_release(parameters,
                  asset_path=xml_repo,
                  release_tag=release_version,
                  github_token=github_token,
                  asset_name='plugins.xml')
        if osgeo_username is not None:
            assert osgeo_password is not None
            if is_prerelease:
                assert experimental_archive_name is not None
                upload_plugin_to_osgeo(username=osgeo_username, password=osgeo_password, archive=experimental_archive_name)
            else:
                upload_plugin_to_osgeo(username=osgeo_username, password=osgeo_password, archive=archive_name)


def create_archive(parameters: Parameters, release_version: str, archive_name: str, add_translations: bool=False, allow_uncommitted_changes: bool=False, is_prerelease: bool=False, raise_min_version: str=None):
    repo = git.Repo()
    top_tar_handle, top_tar_file = mkstemp(suffix='.tar')
    initial_stash = None
    diff = repo.index.diff(None)
    if diff:
        print('Uncommitted changes:')
        for diff in diff:
            print(diff)

        if not allow_uncommitted_changes:
            raise UncommitedChanges('You have uncommitted changes. Stash or commit them or use --allow-uncommitted-changes.')
        else:
            initial_stash = repo.git.stash('create')
    replace_in_file('{}/metadata.txt'.format(parameters.plugin_path), '^version=.*$', 'version={}'.format(release_version))
    if is_prerelease:
        replace_in_file('{}/metadata.txt'.format(parameters.plugin_path), '^experimental=.*$', 'experimental={}'.format(True if is_prerelease else False))
    if raise_min_version:
        replace_in_file('{}/metadata.txt'.format(parameters.plugin_path), '^qgisMinimumVersion=.*$', 'qgisMinimumVersion={}'.format(raise_min_version))
    if not is_prerelease:
        for file in glob(('{}/**/*.py'.format(parameters.plugin_path)), recursive=True):
            replace_in_file(file, '^DEBUG\\s*=\\s*True', 'DEBUG = False')

    else:
        try:
            stash = repo.git.stash('create')
        except git.exc.GitCommandError:
            stash = 'HEAD'

        if not stash == '':
            if stash is None:
                stash = 'HEAD'
            print('archive plugin with stash: {}'.format(stash))
            repo.git.archive(stash, '-o', top_tar_file, parameters.plugin_path)
            for submodule in repo.submodules:
                _, sub_tar_file = mkstemp(suffix='.tar')
                if submodule.path.split('/')[0] != parameters.plugin_path:
                    print('skipping submodule not in plugin source directory ({})'.format(submodule.name))
                    continue
                submodule.update(init=True)
                sub_repo = submodule.module()
                print('archive submodule:', sub_repo)
                sub_repo.git.archive('HEAD', '--prefix', '{}/'.format(submodule.path), '-o', sub_tar_file)
                with tarfile.open(top_tar_file, mode='a') as (tt):
                    with tarfile.open(sub_tar_file, mode='r:') as (st):
                        for m in st.getmembers():
                            if not m.isfile():
                                continue
                            tt.add(m.name)

            if add_translations:
                with tarfile.open(top_tar_file, mode='a') as (tt):
                    print('adding translations')
                    for file in glob('{}/i18n/*.qm'.format(parameters.plugin_path)):
                        print('  adding translation: {}'.format(os.path.basename(file)))
                        tt.add(file)

            pyqt5ac.main(ioPaths=[
             [
              '{}/*.qrc'.format(parameters.plugin_path), '{}/%%FILENAME%%_rc.py'.format(parameters.plugin_path)]])
            for file in glob('{}/*_rc.py'.format(parameters.plugin_path)):
                with tarfile.open(top_tar_file, mode='a') as (tt):
                    print('  adding resource: {}'.format(file))
                    tt.add(file)

            with zipfile.ZipFile(file=archive_name, mode='w', compression=(zipfile.ZIP_DEFLATED)) as (zf):
                with tarfile.open(top_tar_file, mode='r:') as (tt):
                    for m in tt.getmembers():
                        if m.isdir():
                            continue
                        f = tt.extractfile(m)
                        fl = f.read()
                        fn = m.name
                        zf.writestr(fn, fl)

            print('-------')
            print('files in ZIP archive ({}):'.format(archive_name))
            with zipfile.ZipFile(file=archive_name, mode='r') as (zf):
                for f in zf.namelist():
                    print(f)

            print('-------')
            if initial_stash:
                repo.git.reset('--hard', initial_stash)
                repo.git.reset('HEAD^')
        else:
            repo.git.checkout('--', '.')


def upload_asset_to_github_release(parameters: Parameters, asset_path: str, release_tag: str, github_token: str, asset_name: str=None):
    slug = '{}/{}'.format(parameters.github_organization_slug, parameters.project_slug)
    repo = Github(github_token).get_repo(slug)
    try:
        print('Getting release on {}/{}'.format(parameters.github_organization_slug, parameters.project_slug))
        gh_release = repo.get_release(id=release_tag)
        print(gh_release, gh_release.tag_name, gh_release.upload_url)
    except GithubException as e:
        try:
            raise GithubReleaseNotFound('Release {} not found'.format(release_tag))
        finally:
            e = None
            del e

    try:
        if not os.path.exists(asset_path):
            raise AssertionError
        elif asset_name:
            print('Uploading asset: {} as {}'.format(asset_path, asset_name))
            gh_release.upload_asset(path=asset_path, label=asset_name, name=asset_name)
        else:
            print('Uploading asset: {}'.format(asset_path))
            gh_release.upload_asset(asset_path)
        print('OK')
    except GithubException as e:
        try:
            print(e)
            raise GithubReleaseCouldNotUploadAsset('Could not upload asset for release {}. Are you sure the user for the given token can upload asset to this repo?'.format(release_tag))
        finally:
            e = None
            del e


def release_is_prerelease(parameters: Parameters, release_tag: str, github_token: str) -> bool:
    slug = '{}/{}'.format(parameters.github_organization_slug, parameters.project_slug)
    repo = Github(github_token).get_repo(slug)
    try:
        print('Getting release on {}/{}'.format(parameters.github_organization_slug, parameters.project_slug))
        gh_release = repo.get_release(id=release_tag)
        print(gh_release, gh_release.tag_name, gh_release.upload_url)
    except GithubException as e:
        try:
            raise GithubReleaseNotFound('Release {} not found'.format(release_tag))
        finally:
            e = None
            del e

    return gh_release.prerelease


def create_plugin_repo(parameters: Parameters, release_version: str, release_tag: str, archive: str, osgeo_username) -> str:
    """
    Creates the plugin repo as an XML file
    """
    _, xml_repo = mkstemp(suffix='.xml')
    replace_dict = {'__RELEASE_VERSION__':release_version, 
     '__RELEASE_TAG__':release_tag or release_version, 
     '__PLUGIN_NAME__':parameters.plugin_name, 
     '__RELEASE_DATE__':datetime.date.today().strftime('%Y-%m-%d'), 
     '__CREATE_DATE__':parameters.create_date.strftime('%Y-%m-%d'), 
     '__ORG__':parameters.github_organization_slug, 
     '__REPO__':parameters.project_slug, 
     '__PLUGINZIP__':archive, 
     '__OSGEO_USERNAME__':osgeo_username or parameters.author, 
     '__DEPRECATED__':str(parameters.deprecated), 
     '__EXPERIMENTAL__':str(parameters.experimental), 
     '__TAGS__':parameters.tags, 
     '__ICON__':parameters.icon, 
     '__AUTHOR__':parameters.author, 
     '__QGIS_MIN_VERSION__':parameters.qgis_minimum_version, 
     '__DESCRIPTION__':parameters.description, 
     '__ISSUE_TRACKER__':parameters.issue_tracker, 
     '__HOMEPAGE__':parameters.homepage, 
     '__REPO_URL__':parameters.repository_url}
    with importlib_resources.path('qgispluginci', 'plugins.xml.template') as (xml_template):
        configure_file(xml_template, xml_repo, replace_dict)
    return xml_repo


def upload_plugin_to_osgeo(username: str, password: str, archive: str):
    """
    Upload the plugin to QGIS repository

    Parameters
    ----------
    username
        The username
    password
        The password
    archive
        The plugin archive file path to be uploaded
    """
    address = 'https://{username}:{password}@plugins.qgis.org:443/plugins/RPC2/'.format(username=username,
      password=password)
    server = xmlrpc.client.ServerProxy(address, verbose=False)
    try:
        with open(archive, 'rb') as (handle):
            plugin_id, version_id = server.plugin.upload(xmlrpc.client.Binary(handle.read()))
        print('Plugin ID: %s' % plugin_id)
        print('Version ID: %s' % version_id)
    except xmlrpc.client.ProtocolError as err:
        try:
            print('A protocol error occurred')
            print('URL: %s' % re.sub(':[^/].*@', ':******@', err.url))
            print('HTTP/HTTPS headers: %s' % err.headers)
            print('Error code: %d' % err.errcode)
            print('Error message: %s' % err.errmsg)
            sys.exit(1)
        finally:
            err = None
            del err

    except xmlrpc.client.Fault as err:
        try:
            print('A fault occurred')
            print('Fault code: %d' % err.faultCode)
            print('Fault string: %s' % err.faultString)
            sys.exit(1)
        finally:
            err = None
            del err