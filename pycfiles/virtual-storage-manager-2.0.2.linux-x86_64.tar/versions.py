# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vsm/api/views/versions.py
# Compiled at: 2016-06-13 14:11:03
import copy, os

def get_view_builder(req):
    base_url = req.application_url
    return ViewBuilder(base_url)


class ViewBuilder(object):

    def __init__(self, base_url):
        """
        :param base_url: url of the root wsgi application
        """
        self.base_url = base_url

    def build_choices(self, VERSIONS, req):
        version_objs = []
        for version in VERSIONS:
            version = VERSIONS[version]
            version_objs.append({'id': version['id'], 
               'status': version['status'], 
               'links': [
                       {'rel': 'self', 'href': self.generate_href(req.path)}], 
               'media-types': version['media-types']})

        return dict(choices=version_objs)

    def build_versions(self, versions):
        version_objs = []
        for version in sorted(versions.keys()):
            version = versions[version]
            version_objs.append({'id': version['id'], 
               'status': version['status'], 
               'updated': version['updated'], 
               'links': self._build_links(version)})

        return dict(versions=version_objs)

    def build_version(self, version):
        reval = copy.deepcopy(version)
        reval['links'].insert(0, {'rel': 'self', 
           'href': self.base_url.rstrip('/') + '/'})
        return dict(version=reval)

    def _build_links(self, version_data):
        """Generate a container of links that refer to the provided version."""
        href = self.generate_href()
        links = [
         {'rel': 'self', 'href': href}]
        return links

    def generate_href(self, path=None):
        """Create an url that refers to a specific version_number."""
        version_number = 'v1'
        if path:
            path = path.strip('/')
            return os.path.join(self.base_url, version_number, path)
        else:
            return os.path.join(self.base_url, version_number) + '/'