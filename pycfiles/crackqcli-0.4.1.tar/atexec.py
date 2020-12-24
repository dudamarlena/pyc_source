# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/byt3bl33d3r/.virtualenvs/CME_old/lib/python2.7/site-packages/cme/execmethods/atexec.py
# Compiled at: 2016-12-29 01:51:56
from impacket.dcerpc.v5 import tsch, transport
from impacket.dcerpc.v5.dtypes import NULL
from cme.helpers import gen_random_string
from gevent import sleep

class TSCH_EXEC:

    def __init__(self, target, username, password, domain, hashes=None):
        self.__target = target
        self.__username = username
        self.__password = password
        self.__domain = domain
        self.__lmhash = ''
        self.__nthash = ''
        self.__outputBuffer = ''
        self.__retOutput = False
        if hashes is not None:
            if hashes.find(':') != -1:
                self.__lmhash, self.__nthash = hashes.split(':')
            else:
                self.__nthash = hashes
        if self.__password is None:
            self.__password = ''
        stringbinding = 'ncacn_np:%s[\\pipe\\atsvc]' % self.__target
        self.__rpctransport = transport.DCERPCTransportFactory(stringbinding)
        if hasattr(self.__rpctransport, 'set_credentials'):
            self.__rpctransport.set_credentials(self.__username, self.__password, self.__domain, self.__lmhash, self.__nthash)
        return

    def execute(self, command, output=False):
        self.__retOutput = output
        self.doStuff(command)
        return self.__outputBuffer

    def doStuff(self, command):

        def output_callback(data):
            self.__outputBuffer = data

        dce = self.__rpctransport.get_dce_rpc()
        dce.set_credentials(*self.__rpctransport.get_credentials())
        dce.connect()
        dce.bind(tsch.MSRPC_UUID_TSCHS)
        tmpName = gen_random_string(8)
        xml = '<?xml version="1.0" encoding="UTF-16"?>\n<Task version="1.2" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">\n  <Triggers>\n    <CalendarTrigger>\n      <StartBoundary>2015-07-15T20:35:13.2757294</StartBoundary>\n      <Enabled>true</Enabled>\n      <ScheduleByDay>\n        <DaysInterval>1</DaysInterval>\n      </ScheduleByDay>\n    </CalendarTrigger>\n  </Triggers>\n  <Principals>\n    <Principal id="LocalSystem">\n      <UserId>S-1-5-18</UserId>\n      <RunLevel>HighestAvailable</RunLevel>\n    </Principal>\n  </Principals>\n  <Settings>\n    <MultipleInstancesPolicy>IgnoreNew</MultipleInstancesPolicy>\n    <DisallowStartIfOnBatteries>false</DisallowStartIfOnBatteries>\n    <StopIfGoingOnBatteries>false</StopIfGoingOnBatteries>\n    <AllowHardTerminate>true</AllowHardTerminate>\n    <RunOnlyIfNetworkAvailable>false</RunOnlyIfNetworkAvailable>\n    <IdleSettings>\n      <StopOnIdleEnd>true</StopOnIdleEnd>\n      <RestartOnIdle>false</RestartOnIdle>\n    </IdleSettings>\n    <AllowStartOnDemand>true</AllowStartOnDemand>\n    <Enabled>true</Enabled>\n    <Hidden>true</Hidden>\n    <RunOnlyIfIdle>false</RunOnlyIfIdle>\n    <WakeToRun>false</WakeToRun>\n    <ExecutionTimeLimit>P3D</ExecutionTimeLimit>\n    <Priority>7</Priority>\n  </Settings>\n  <Actions Context="LocalSystem">\n    <Exec>\n      <Command>cmd.exe</Command>\n'
        if self.__retOutput:
            tmpFileName = tmpName + '.tmp'
            xml += ('      <Arguments>/C {} &gt; %windir%\\Temp\\{} 2&gt;&amp;1</Arguments>\n    </Exec>\n  </Actions>\n</Task>\n        ').format(command, tmpFileName)
        else:
            if self.__retOutput is False:
                xml += ('      <Arguments>/C {}</Arguments>\n    </Exec>\n  </Actions>\n</Task>\n        ').format(command)
            taskCreated = False
            tsch.hSchRpcRegisterTask(dce, '\\%s' % tmpName, xml, tsch.TASK_CREATE, NULL, tsch.TASK_LOGON_NONE)
            taskCreated = True
            tsch.hSchRpcRun(dce, '\\%s' % tmpName)
            done = False
            while not done:
                resp = tsch.hSchRpcGetLastRunInfo(dce, '\\%s' % tmpName)
                if resp['pLastRuntime']['wYear'] != 0:
                    done = True
                else:
                    sleep(2)

        tsch.hSchRpcDelete(dce, '\\%s' % tmpName)
        taskCreated = False
        if taskCreated is True:
            tsch.hSchRpcDelete(dce, '\\%s' % tmpName)
        peer = (':').join(map(str, self.__rpctransport.get_socket().getpeername()))
        if self.__retOutput:
            smbConnection = self.__rpctransport.get_smb_connection()
            while True:
                try:
                    smbConnection.getFile('ADMIN$', 'Temp\\%s' % tmpFileName, output_callback)
                    break
                except Exception as e:
                    if str(e).find('SHARING') > 0:
                        sleep(3)
                    elif str(e).find('STATUS_OBJECT_NAME_NOT_FOUND') >= 0:
                        sleep(3)
                    else:
                        raise

            smbConnection.deleteFile('ADMIN$', 'Temp\\%s' % tmpFileName)
        dce.disconnect()