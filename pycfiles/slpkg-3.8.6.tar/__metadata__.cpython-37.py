# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/dslackw/Downloads/slpkg-3.8.6/slpkg/__metadata__.py
# Compiled at: 2020-03-26 09:43:46
# Size of source mod 2**32: 7865 bytes
import os

def remove_repositories(repositories, default_repositories):
    """
    Remove no default repositories
    """
    for repo in repositories:
        if repo in default_repositories:
            yield repo


def update_repositories(repositories, conf_path):
    """
    Upadate with user custom repositories
    """
    repo_file = f"{conf_path}custom-repositories"
    if os.path.isfile(repo_file):
        f = open(repo_file, 'r')
        repositories_list = f.read()
        f.close()
        for line in repositories_list.splitlines():
            line = line.lstrip()
            if line:
                line.startswith('#') or repositories.append(line.split()[0])

    return repositories


def grab_sub_repo(repositories, repos):
    """
    Grab SUB_REPOSITORY
    """
    for i, repo in enumerate(repositories):
        if repos in repo:
            sub = repositories[i].replace(repos, '')
            repositories[i] = repos
            return sub

    return ''


def select_slack_release(slack_rel):
    """
    Warning message if Slackware release not defined or
    defined wrong
    """
    if slack_rel not in ('stable', 'current'):
        return 'FAULT'
    return slack_rel


class MetaData:
    __all__ = 'slpkg'
    __author__ = 'dslackw'
    __version_info__ = (3, 8, 6)
    __version__ = ('{0}.{1}.{2}'.format)(*__version_info__)
    __license__ = 'GNU General Public License v3 (GPLv3)'
    __email__ = 'd.zlatanidis@gmail.com'
    __maintainer__ = 'Dimitris Zlatanidis (dslackw)'
    __homepage__ = 'https://dslackw.gitlab.io/slpkg/'
    slack_rel = 'stable'
    conf_path = f"/etc/{__all__}/"
    tmp = '/tmp/'
    tmp_path = f"{tmp}{__all__}/"
    _conf_slpkg = {'RELEASE':'stable', 
     'SLACKWARE_VERSION':'off', 
     'COMP_ARCH':'off', 
     'REPOSITORIES':[
      'slack', 'sbo', 'rlw', 'alien',
      'slacky', 'conrad', 'slonly',
      'ktown{latest}', 'multi', 'slacke{18}',
      'salix', 'slackl', 'rested', 'msb{1.18}',
      'csb', 'connos', 'mles{desktop}'], 
     'BUILD_PATH':'/tmp/slpkg/build/', 
     'SBOSRCARCH':'off', 
     'SBOSRCARCH_LINK':'http://slackware.uk/sbosrcarch/by-name/', 
     'PACKAGES':'/tmp/slpkg/packages/', 
     'PATCHES':'/tmp/slpkg/patches/', 
     'CHECKMD5':'on', 
     'DEL_ALL':'on', 
     'DEL_BUILD':'off', 
     'SBO_BUILD_LOG':'on', 
     'MAKEFLAGS':'off', 
     'DEFAULT_ANSWER':'n', 
     'REMOVE_DEPS_ANSWER':'n', 
     'SKIP_UNST':'n', 
     'RSL_DEPS':'on', 
     'DEL_DEPS':'off', 
     'USE_COLORS':'on', 
     'DOWNDER':'wget', 
     'DOWNDER_OPTIONS':'-c -N', 
     'SLACKPKG_LOG':'on', 
     'ONLY_INSTALLED':'off', 
     'EDITOR':'nano', 
     'NOT_DOWNGRADE':'off', 
     'HTTP_PROXY':''}
    default_repositories = [
     'slack', 'sbo', 'rlw', 'alien', 'slacky', 'conrad',
     'slonly', 'ktown', 'multi', 'slacke', 'salix',
     'slackl', 'rested', 'msb', 'csb', 'connos', 'mles']
    repositories = []
    for files in ('slpkg.conf', 'repositories.conf'):
        if os.path.isfile(f"{conf_path}{files}"):
            f = open(f"{conf_path}{files}", 'r')
            conf = f.read()
            f.close()
            for line in conf.splitlines():
                line = line.lstrip()
                if line:
                    if line.startswith('#') or files == 'slpkg.conf':
                        _conf_slpkg[line.split('=')[0]] = line.split('=')[1]
                    elif files == 'repositories.conf':
                        repositories.append(line)

    slack_rel = _conf_slpkg['RELEASE']
    slackware_version = _conf_slpkg['SLACKWARE_VERSION']
    comp_arch = _conf_slpkg['COMP_ARCH']
    build_path = _conf_slpkg['BUILD_PATH']
    sbosrcarch = _conf_slpkg['SBOSRCARCH']
    sbosrcarch_link = _conf_slpkg['SBOSRCARCH_LINK']
    slpkg_tmp_packages = _conf_slpkg['PACKAGES']
    slpkg_tmp_patches = _conf_slpkg['PATCHES']
    checkmd5 = _conf_slpkg['CHECKMD5']
    del_all = _conf_slpkg['DEL_ALL']
    del_folder = _conf_slpkg['DEL_BUILD']
    sbo_build_log = _conf_slpkg['SBO_BUILD_LOG']
    makeflags = _conf_slpkg['MAKEFLAGS']
    default_answer = _conf_slpkg['DEFAULT_ANSWER']
    remove_deps_answer = _conf_slpkg['REMOVE_DEPS_ANSWER']
    skip_unst = _conf_slpkg['SKIP_UNST']
    rsl_deps = _conf_slpkg['RSL_DEPS']
    del_deps = _conf_slpkg['DEL_DEPS']
    use_colors = _conf_slpkg['USE_COLORS']
    downder = _conf_slpkg['DOWNDER']
    downder_options = _conf_slpkg['DOWNDER_OPTIONS']
    slackpkg_log = _conf_slpkg['SLACKPKG_LOG']
    only_installed = _conf_slpkg['ONLY_INSTALLED']
    editor = _conf_slpkg['EDITOR']
    not_downgrade = _conf_slpkg['NOT_DOWNGRADE']
    http_proxy = _conf_slpkg['HTTP_PROXY']
    SBo_SOURCES = build_path + '_SOURCES/'
    repositories = [repo.strip() for repo in repositories]
    slack_rel = select_slack_release(slack_rel)
    ktown_kde_repo = grab_sub_repo(repositories, 'ktown')
    slacke_sub_repo = grab_sub_repo(repositories, 'slacke')
    msb_sub_repo = grab_sub_repo(repositories, 'msb')
    mles_sub_repo = grab_sub_repo(repositories, 'mles')
    repositories = list(remove_repositories(repositories, default_repositories))
    update_repositories(repositories, conf_path)
    color = {'RED':'\x1b[31m', 
     'GREEN':'\x1b[32m', 
     'YELLOW':'\x1b[33m', 
     'CYAN':'\x1b[36m', 
     'GREY':'\x1b[38;5;247m', 
     'ENDC':'\x1b[0m'}
    if use_colors in ('off', 'OFF'):
        color = {'RED':'',  'GREEN':'', 
         'YELLOW':'', 
         'CYAN':'', 
         'GREY':'', 
         'ENDC':''}
    else:
        CHECKSUMS_link = f"https://gitlab.com/{__author__}/{__all__}/raw/master/CHECKSUMS.md5"
        sp = '-'
        try:
            path = os.getcwd() + '/'
        except OSError:
            path = tmp_path

        lib_path = '/var/lib/slpkg/'
        log_path = '/var/log/slpkg/'
        pkg_path = '/var/log/packages/'
        slackpkg_lib_path = '/var/lib/slackpkg/'
        if comp_arch in ('off', 'OFF'):
            arch = os.uname()[4]
        else:
            arch = comp_arch
    try:
        output = os.environ['OUTPUT']
    except KeyError:
        output = tmp

    if not output.endswith('/'):
        output += '/'