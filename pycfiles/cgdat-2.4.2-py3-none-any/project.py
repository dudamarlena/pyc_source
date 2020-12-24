# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/cgcloud/core/project.py
# Compiled at: 2016-11-22 15:21:45
import glob, os, pkg_resources
from bd2k.util.collections import rindex

def project_artifacts(project_name):
    """
    Similar to project_artifact but including dependent project artifacts
    """
    if project_name == 'lib':
        return [project_artifact(project_name)]
    else:
        return [
         project_artifact('lib'), project_artifact(project_name)]


def project_artifact(project_name):
    """
    Resolve the name of a sibling project to something that can be passed to pip in order to get
    that project installed. The version of the sibling project is assumed to be identical to the
    currently installed version of this project (cgcloud-core). If the version can't be
    determined, a source distribution is looked up in the 'dist' subdirectory of the sibling
    project. This is likely to be the case in development mode, i.e. if this project was
    installed via 'setup.py develop'. If neither version nor source distribution can be
    determined, an exception will be raised.

    :param project_name: the name of a sibling project such as 'agent' or 'spark-tools'

    :return: Either an absolute path to a source distribution or a requirement specifier to be
    looked up in the Python package index (PyPI).
    """
    dir_path = os.path.abspath(__file__).split(os.path.sep)
    try:
        i = rindex(dir_path, 'src')
    except ValueError:
        version = pkg_resources.get_distribution('cgcloud-core').version
        return 'cgcloud-%s==%s' % (project_name, version)

    dir_path = os.path.sep.join(dir_path[:i])
    project_path = os.path.join(os.path.dirname(dir_path), project_name)
    sdist_glob = os.path.join(project_path, 'dist', 'cgcloud-%s*.tar.gz' % project_name)
    sdist = glob.glob(sdist_glob)
    if len(sdist) == 1:
        sdist = sdist[0]
    elif sdist:
        raise RuntimeError("Can't decide which of these is the '%s' source distribution: %s" % (
         project_name, sdist))
    else:
        raise RuntimeError("Can't find '%s' source distribution. Looking for '%s'. You may just need to run 'make sdist' to fix this" % (
         project_name, sdist_glob))
    return sdist