# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/cloud_admin/services/dns_service.py
# Compiled at: 2018-01-31 14:44:08
import sys, time
from cloud_admin.services.services import EucaComponentService
try:
    from dns import resolver
except ImportError as IE:
    sys.stderr.write(('Failed to import dns.resolver:"{0}"').format(IE))

class EucaDnsService(EucaComponentService):

    def __init__(self, *args, **kwargs):
        self._resolver = None
        self.host = None
        super(EucaDnsService, self).__init__(*args, **kwargs)
        return

    @property
    def resolver(self):
        if not self._resolver:
            if self.host:
                self._resolver = resolver.Resolver(configure=False)
                self._resolver.nameservers = [self.host]
        return self._resolver

    @resolver.setter
    def resolver(self, value):
        self._resolver = value

    def update(self, new_service=None, get_instances=True, silent=True):
        return self._update(get_method=self.connection.get_services, get_method_kwargs={'service_type': 'dns'}, new_service=new_service, silent=silent)

    def resolve(self, name, timeout=360, poll_count=20):
        """
        Resolve hostnames against the Eucalyptus DNS service
        """
        poll_sleep = timeout / poll_count
        for _ in range(poll_count):
            try:
                try:
                    self.debug_method(("DNSQUERY: Resolving `{0}' against nameserver(s) {1}").format(name, self.resolver.nameservers))
                    ans = self.resolver.query(name)
                    return str(ans[0])
                except resolver.NXDOMAIN:
                    raise RuntimeError(("Unable to resolve hostname `{0}'").format(name))
                except resolver.NoNameservers:
                    pass

            finally:
                time.sleep(poll_sleep)

        raise RuntimeError(("Unable to resolve hostname `{0}'").format(name))