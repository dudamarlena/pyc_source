# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/sanhehu/Documents/GitHub/pygitrepo-project/pygitrepo/cli.py
# Compiled at: 2018-08-05 14:29:05
# Size of source mod 2**32: 12659 bytes
__doc__ = '\nThis script can generate automate scripts for open source python project.\n'
from __future__ import print_function
import sys, datetime
from os import walk, mkdir, getcwd
import click
from jinja2 import Template
from pathlib_mate.pathlib import Path
try:
    from . import integrate
    from .util import read, write
    from .version import __version__
except:
    from pygitrepo import integrate
    from pygitrepo.util import read, write
    from pygitrepo.version import __version__

py_ver_major = sys.version_info.major
py_ver_minor = sys.version_info.minor
py_ver_micro = sys.version_info.micro
py_ver_long = '%s.%s.%s' % (py_ver_major, py_ver_minor, py_ver_micro)
py_ver_short = '%s.%s' % (py_ver_major, py_ver_minor)

def simple_render(template_content, kwargs):
    """
    Rend a jinja2 styled template.

    :param template_content: str
    :param kwargs: dict
    """
    temp_prefix = '{{ PyGitRepo_Temp_Prefix____%s }}'
    mapper1 = dict()
    mapper2 = dict()
    for i, (key, value) in enumerate(kwargs.items()):
        temp_key = temp_prefix % i
        mapper1['{{ %s }}' % key] = temp_key
        mapper2[temp_key] = str(value)

    for old, new in mapper1.items():
        template_content = template_content.replace(old, new)

    for old, new in mapper2.items():
        template_content = template_content.replace(old, new)

    return template_content


def jinja2_render(template_content, kwargs):
    template = Template(template_content)
    return template.render(**kwargs)


def is_none_or_empty(value):
    """
    Test if a value is None or 'False' things.
    """
    if value is None or bool(value) is False:
        return True
    else:
        return False


SUPPORT_DOC_HOST_SERVICE = ['none', 'rtd', 's3']

def initiate_project(package_name=None, repo_name=None, github_username=None, supported_py_ver=None, author_name=None, author_email=None, maintainer_name=None, maintainer_email=None, license='MIT', rtd_name=None, s3_bucket=None, doc_service='none', verbose=True, **kwargs):
    """
    Generate skeleton of project files.

    :param package_name: your python package name, it should be able to install
        via ``pip install <package_name>``, and will be published on
        https://pypi.python.org/pypi/<package_name>

    :param repo_name: github repository name, the github link will be:
        https://github.com//<github_username>/<repo_name>

    :param github_username: github username, the github link will be:
        https://github.com//<github_username>/<repo_name>

    :param supported_py_ver: list of Python version you want to support,
        it has to be a valid pyenv version.
        available Python Version names can be found at:
        https://github.com/pyenv/pyenv/blob/master/plugins/python-build/share/python-build.

    :param author_name: author name
    :param author_email: author email
    :param maintainer_name: maintainer name
    :param maintainer_email: maintainer email

    :param license: currently only support MIT license, you can manually replace
        the license file yourself.

    :param rtd_name: Read the doc project name, doc will be host at:
        http://<rtd_name>.readthedocs.io/

    :param s3_bucket: AWS S3 bucket name, doc will be host at
        http://<s3_bucket>.s3.amazonaws.com/<package_name>/index.html. You need to
        config your bucket to allow all public get traffic. Tutorial is here:
        http://docs.aws.amazon.com/AmazonS3/latest/dev/WebsiteHosting.html

    :param doc_service: str, doc service you want to use, one of
        "none", "rtd", "s3".

    :param verbose: bool, toggle on / off the log info.
    """
    if is_none_or_empty(package_name):
        raise ValueError("`package_name` can't be None!")
    if is_none_or_empty(repo_name):
        repo_name = '%s-project' % package_name
    if is_none_or_empty(github_username):
        raise ValueError("`github_username` can't be None!")
    else:
        repo_url = 'https://github.com/{github_username}/{repo_name}'.format(github_username=github_username, repo_name=repo_name)
    if is_none_or_empty(supported_py_ver):
        supported_py_ver = [
         py_ver_long]
    supported_py_ver_for_tox = set()
    for py_ver in supported_py_ver:
        try:
            supported_py_ver_for_tox.add(integrate.pyenv_ver_to_tox_ver(py_ver))
        except Exception as e:
            print(e)

    supported_py_ver_for_tox = list(supported_py_ver_for_tox)
    supported_py_ver_for_tox.sort()
    supported_py_ver_for_tarvis = set()
    for py_ver in supported_py_ver:
        try:
            supported_py_ver_for_tarvis.add(integrate.pyenv_ver_to_travis_ver(py_ver))
        except Exception as e:
            print(e)

    supported_py_ver_for_tarvis = list(supported_py_ver_for_tarvis)
    supported_py_ver_for_tarvis.sort()
    if license != 'MIT':
        license = 'MIT'
    click.secho('Initiate with a MIT license, you can manually change the file yourself!', fg='red')
    if is_none_or_empty(rtd_name) is False:
        doc_domain_rtd = 'https://{rtd_name}.readthedocs.io'.format(rtd_name=rtd_name)
    else:
        rtd_name = 'Unknown_ReadTheDocs_Project_Name'
    if is_none_or_empty(s3_bucket) is False:
        doc_domain_s3 = 'http://{s3_bucket}.s3.amazonaws.com/{package_name}'.format(s3_bucket=s3_bucket, package_name=package_name)
    else:
        s3_bucket = 'Unknwon_S3_Bucket_Name'
    doc_domain = None
    if doc_service == 'none':
        click.secho("You don't have a website to host your documents! You could use either https://readthedocs.org or AWS S3.", fg='green')
    else:
        if doc_service == 'rtd':
            doc_domain = doc_domain_rtd
        else:
            if doc_service == 's3':
                doc_domain = doc_domain_s3
            else:
                raise ValueError("doesn't recognize doc host service '%s'!" % doc_service)
    click.secho("There's author introduction file at {repo_name}/docs/source/author.rst, you should change it to your own introduction.".format(repo_name=repo_name), fg='red')
    if not maintainer_name:
        maintainer_name = author_name
    if not maintainer_email:
        maintainer_email = author_email
    kwargs_ = dict(pygitrepo_version=__version__, package_name=package_name, repo_name=repo_name, github_username=github_username, repo_url=repo_url, supported_py_ver=supported_py_ver, supported_py_ver_for_tox=supported_py_ver_for_tox, supported_py_ver_for_travis=supported_py_ver_for_tarvis, py_ver_major=py_ver_major, py_ver_minor=py_ver_minor, py_ver_micro=py_ver_micro, year=datetime.datetime.utcnow().year, today=datetime.date.today(), license=license, author_name=author_name, author_email=author_email, maintainer_name=maintainer_name, maintainer_email=maintainer_email, rtd_name=rtd_name, s3_bucket=s3_bucket, doc_domain=doc_domain)
    kwargs_.update(kwargs)
    print("Initate '%s' from template ..." % repo_name)
    template_dir = Path(__file__).absolute().change(new_basename='{{ repo_name }}')
    output_dir = Path(getcwd(), repo_name).absolute()
    file_count = 0
    for src_dir, dir_list, file_list in walk(template_dir.abspath):
        if src_dir.endswith('__pycache__'):
            pass
        else:
            dst_dir = Path(jinja2_render(src_dir.replace(template_dir.abspath, output_dir.abspath, 1), kwargs_))
            try:
                if verbose:
                    print("    Create '%s' ..." % dst_dir)
                mkdir(dst_dir.abspath)
            except:
                pass

            for filename in file_list:
                if not filename.endswith('.pyc'):
                    if filename.endswith('.DS_Store'):
                        pass
                    else:
                        src = Path(src_dir, filename)
                        dst = Path(jinja2_render(Path(dst_dir.abspath, filename).abspath, kwargs_))
                        try:
                            content = jinja2_render(read(src.abspath), kwargs_)
                            if verbose:
                                print("    Create '%s' ..." % dst)
                            write(content, dst.abspath)
                        except:
                            src.copyto(new_abspath=dst.abspath, overwrite=True)

                        file_count += 1

    print('    COMPLETE! %s files created.' % file_count)


@click.command()
@click.option('--package_name', prompt='(REQUIRED) Your Package Name (e.g. pip)')
@click.option('--repo_name', prompt='(optional) Your Repository Name (e.g. pip-project)', default='')
@click.option('--github_username', prompt='(REQUIRED) Your Github Username')
@click.option('--supported_py_ver', prompt="(optional) Enter python version list your package will support, seperate by comma. For example: '2.7.13, 3.4.6'. All available version are listed here: https://github.com/pyenv/pyenv/tree/master/plugins/python-build/share/python-build", default='')
@click.option('--author_name', prompt='(optional) Author Name', default='')
@click.option('--author_email', prompt='(optional) Author Email', default='')
@click.option('--maintainer_name', prompt='(optional) Maintainer Name', default='')
@click.option('--maintainer_email', prompt='(optional) Maintainer Email', default='')
@click.option('--rtd_name', prompt='(optional) If use ReadTheDocs to host your document, please specify the project name (will be your domain prefix).', default='')
@click.option('--s3_bucket', prompt='(optional) If use AWS S3 to host your document, please specify the bucket name.', default='')
@click.option('--doc_service', prompt='(REQUIRED) Choose your doc host serivce from %s.' % (
 ' | '.join(SUPPORT_DOC_HOST_SERVICE),), type=click.Choice(SUPPORT_DOC_HOST_SERVICE))
def _initiate_project(package_name, repo_name, github_username, supported_py_ver, author_name, author_email, maintainer_name, maintainer_email, rtd_name, s3_bucket, doc_service):
    if supported_py_ver is None:
        pass
    else:
        if supported_py_ver.strip():
            supported_py_ver = [ver.strip().lower() for ver in supported_py_ver.split(',') if ver.strip()]
        else:
            supported_py_ver = None
        initiate_project(package_name=package_name, repo_name=repo_name, github_username=github_username, supported_py_ver=supported_py_ver, author_name=author_name, author_email=author_email, maintainer_name=maintainer_name, maintainer_email=maintainer_email, rtd_name=rtd_name, s3_bucket=s3_bucket, doc_service=doc_service)


if __name__ == '__main__':
    initiate_project()