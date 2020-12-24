# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/datapkggui/lib.py
# Compiled at: 2011-10-27 15:23:46
__author__ = 'dgraziotin'
import datapkg, datapkg.spec, datapkg.index, datapkg.download, datapkg.config, ckanclient, os, shutil

def index_from_spec(spec_str, all_index=False):
    spec = datapkg.spec.Spec.parse_spec(spec_str, all_index=all_index)
    return spec.index_from_spec()


def create():
    pass


def get_config():
    """
    Returns datapkg configuration

    Return values:
    None if the configuration does not exist.
    a datapkg.config.Config object on success
    """
    return datapkg.CONFIG


def download(package_spec, destination_path):
    """Download a Package and the connected Resources

    Keyword arguments:
    package_spec -- a string Spec in the form of <scheme>://<package name>, where:
                    <scheme> identifies the type of index to be used
                    <package name> identifies the name of the package
                    Ex: ckan://iso-codes
    destination_path -- a string specifying the directory in which to save the package

    Return values:
    True if the operation succeeds
    The actual datapkg design does not let us to specify other values. Must fix this
    """
    pkg_downloader = datapkg.download.PackageDownloader(verbose=True)
    filterfunc = None
    index, path = index_from_spec(package_spec)
    package = index.get(path)
    os_destination_path = os.path.join(destination_path, package.name)
    pkg_downloader.download(package, os_destination_path, filterfunc)
    return True


def info(package_spec, request_for='metadata'):
    """Retrieve info on Package

    Keyword arguments:
    package_spec -- either:
                    * a string Spec in the form of <scheme>://<package name>, where:
                    <scheme> identifies the type of index to be used
                    <package name> identifies the name of the package
                    Ex: ckan://iso-codes.
                    * an object of type Package
    request_for -- a string specifying what to retrieve. Up to know we let choose either for 'metadata'
                   or for 'manifest'. Default is 'manifest'

    Return values:
    The package Metadata (or the Manifest)
    None elsewhere
    """
    if type(package_spec) == str:
        index, path = index_from_spec(package_spec)
        package = index.get(path)
    else:
        package = package_spec
    if not type(package) == datapkg.package.Package:
        return
    else:
        if request_for == 'metadata':
            return package.metadata
        else:
            if request_for == 'manifest':
                return package.manifest
            return package.metadata

        return


def list(index_spec=''):
    """Returns the Packages (not the resources) pointed by an index

    Keyword arguments:
    index_spec -- a string in the form of <scheme>://, where <scheme> identifies the type of index to be used.
                  Ex: ckan://

    Return values:
    A list of Packages pointed by the Index
    Actually, datapkg lacks the case in which an exception occurs (see datapkg.index.ckan.py.list())
    """
    index, path = index_from_spec(index_spec, all_index=True)
    packages = index.list()
    return packages


def register():
    pass


def search(index_spec, query):
    """Search a Package

    Keyword arguments:
    index_spec -- a string in the form of <scheme>://, where <scheme> identifies the type of index to be used.
                  Ex: ckan://
    query -- a string specifying the query to be executed.
             Ex: iso

    Return values:
    A list of Package object if there are results
    An empty list elsewhere
    """
    spec_from = index_spec
    index, path = index_from_spec(spec_from)
    packages = []
    try:
        for package in index.search(query):
            packages.append(package)

    except ckanclient.CkanApiNotAuthorizedError:
        pass

    return packages


def update():
    pass