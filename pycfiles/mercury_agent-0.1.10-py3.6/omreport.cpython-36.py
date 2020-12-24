# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mercury_agent/hardware/oem/dell/omreport.py
# Compiled at: 2019-02-11 13:08:11
# Size of source mod 2**32: 2292 bytes
import os
from mercury.common.helpers.cli import run
from mercury_agent.hardware.oem.dell.om_xml_deserializer import XLoader, XMLController, XMLAbout, XMLPDisk, XMLVDisk, XMLChassisStatus

class OMReportInitException(Exception):
    pass


class OMReportRunException(Exception):

    def __init__(self, message, stdout, stderr):
        self.message = message
        self.stdout = stdout
        self.stderr = stderr

    def __str__(self):
        return repr(self.message)


class OMReport(object):

    def __init__(self, path='/opt/dell/srvadmin/bin/omreport'):
        self.omreport_path = path
        if not os.getuid() == 0:
            raise OMReportInitException('Script must be run as root.')
        if not self._check_service:
            raise OMReportInitException('dataeng services are not running.')
        if not os.path.exists(self.omreport_path):
            raise OMReportInitException('{0} does not exist.'.format(self.omreport_path))

    @property
    def _check_service(self):
        """
        Tested only on redhat/cent
        """
        res = run('service dataeng status')
        if res.returncode:
            return False
        else:
            return True

    def run_omreport(self, command, fmt='xml'):
        full_command = '{0} {1} -fmt {2}'.format(self.omreport_path, command, fmt)
        res = run(full_command)
        if res.returncode:
            raise OMReportRunException('Had trouble running {0}'.format(full_command), res, res.stderr)
        return res.encode()

    @property
    def about(self):
        xml_data = self.run_omreport('about')
        return XMLAbout(XLoader(xml_data).root)

    @property
    def chassis(self):
        xml_data = self.run_omreport('chassis')
        return XMLChassisStatus(XLoader(xml_data).root)

    @property
    def controller(self):
        xml_data = self.run_omreport('controller')
        return XMLController(XLoader(xml_data).root)

    @property
    def vdisk(self):
        xml_data = self.run_omreport('storage vdisk controller=0')
        return XMLVDisk(XLoader(xml_data).root)

    @property
    def pdisk(self):
        xml_data = self.run_omreport('storage pdisk controller=0')
        return XMLPDisk(XLoader(xml_data).root)