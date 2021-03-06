# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/upfluence/error_logger/opbeat.py
# Compiled at: 2016-08-03 15:23:39
import socket, opbeat

class Client(object):

    def __init__(self, organization_id, app_id, secret_token, hname=None, extra={}):
        self.extra = extra
        self.base_service = None
        machine = hname or socket.gethostname()
        self._client = opbeat.Client(organization_id=organization_id, app_id=app_id, secret_token=secret_token, hostname=machine)

        def _build_base_extra(self):
            extras = {}
            versions = self.base_service.getInterfaceVersion()
            versions.update({self.base_service.getName(): self.base_service.getVersion()})
            for name, version in versions.iteritems():
                if version.git_version:
                    gitver = version.git_version
                    extras.update({('{}_git_version').format(name): ('{}/commit/{}').format(gitver.remote, gitver.commit)})
                if version.semantic_version:
                    semver = version.semantic_version
                    extras.update({('{}_semantic_version').format(name): ('{}.{}.{}').format(semver.major, semver.minor, semver.patch)})

            return extras

        def capture_exception(*args, **kwargs):
            kwargs['extra'] = dict(kwargs.get('extra', {}), **self._extra)
            self._client.capture_exception(*args, **kwargs)

        return