# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/grey/.pyenv/versions/cm/lib/python2.7/site-packages/cloudmesh_client/cloud/usage.py
# Compiled at: 2017-04-23 10:30:41
from cloudmesh_client.cloud.iaas.provider.openstack.CloudProviderOpenstackAPI import set_os_environ
from cloudmesh_client.common.Printer import Printer
from cloudmesh_client.common.Shell import Shell
from cloudmesh_client.cloud.ListResource import ListResource
from cloudmesh_client.common.TableParser import TableParser
from cloudmesh_client.cloud.nova import Nova

class Usage(ListResource):

    @classmethod
    def list(cls, cloud, start=None, end=None, tenant=None, format='table'):
        set_os_environ(cloud)
        try:
            args = [
             'usage']
            if start is not None:
                args.extend(['--start', start])
            if end is not None:
                args.extend(['--end', end])
            if tenant is not None:
                args.extend(['--tenant', tenant])
            result = Shell.execute('nova', args)
            result = Nova.remove_subjectAltName_warning(result)
            lines = result.splitlines()
            dates = lines[0]
            for l in lines[1:]:
                if l.__contains__('SecurityWarning'):
                    lines.remove(l)

            table = ('\n').join(lines[1:])
            dates = dates.replace('Usage from ', '').replace('to', '').replace(' +', ' ')[:-1].split()
            d = TableParser.convert(table, comment_chars='+#')
            d['0']['start'] = dates[0]
            d['0']['end'] = dates[1]
            return Printer.write(d, order=[
             'start',
             'end',
             'servers',
             'cpu hours',
             'ram mb-hours',
             'disk gb-hours'], output=format)
        except Exception as e:
            return e

        return