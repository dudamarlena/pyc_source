# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vsmclient/v1/contrib/list_extensions.py
# Compiled at: 2016-06-13 14:11:03
from vsmclient import base
from vsmclient import utils

class ListExtResource(base.Resource):

    @property
    def summary(self):
        descr = self.description.strip()
        if not descr:
            return '??'
        else:
            lines = descr.split('\n')
            if len(lines) == 1:
                return lines[0]
            return lines[0] + '...'


class ListExtManager(base.Manager):
    resource_class = ListExtResource

    def show_all(self):
        return self._list('/extensions', 'extensions')


@utils.service_type('vsm')
def do_list_extensions(client, _args):
    """
    List all the os-api extensions that are available.
    """
    extensions = client.list_extensions.show_all()
    fields = ['Name', 'Summary', 'Alias', 'Updated']
    utils.print_list(extensions, fields)