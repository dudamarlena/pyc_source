# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/socek/projects/impaf/core/build/lib/impaf/requestable.py
# Compiled at: 2015-11-11 07:29:09
# Size of source mod 2**32: 618 bytes


class Requestable(object):

    def feed_request(self, request):
        self.request = request

    @property
    def registry(self):
        return self.request.registry

    @property
    def POST(self):
        return self.request.POST

    @property
    def GET(self):
        return self.request.GET

    @property
    def matchdict(self):
        return self.request.matchdict

    @property
    def route_path(self):
        return self.request.route_path

    @property
    def settings(self):
        return self.registry['settings']

    @property
    def paths(self):
        return self.registry['paths']