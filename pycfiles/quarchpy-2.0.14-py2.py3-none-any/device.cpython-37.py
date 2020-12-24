# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\sboon\AppData\Local\Temp\pip-install-ptdbtr91\quarchpy\quarchpy\device\device.py
# Compiled at: 2020-03-25 05:10:07
# Size of source mod 2**32: 16958 bytes
import time, sys, os, logging
from quarchpy.connection import QISConnection, PYConnection, QPSConnection
from quarchpy import user_interface

class quarchDevice:
    __doc__ = '\n    Allows control over a Quarch device, over a wide range of underlying connection methods.  This is the core class\n    used for control of all Quarch products.\n    \n    '

    def __init__(self, ConString, ConType='PY', timeout='5', forceFind=0):
        """
        Constructor for quarchDevice, allowing the connection method of the device to be specified.
        
        Parameters
        ----------
        ConString : str
            
            Connection string, specifying the underlying connection type and module identifier. The underlying
            connection must be supported both by the connection type and the target module.
            
            Example:
            USB:QTL1743             - USB connection with given part number
            USB:QTL1743-03-015      - USB connection with fully qualified serial number
            SERIAL:COM4             - Serial connection with COM port (ttyS0 for linux)
            TCP:192.168.1.55        - LAN(TCP) connection to IP address
            TELNET:QTL1079-03-004   - LAN(TELNET) connection to netBIOS name (must resolve to IP address)
            REST:192.168.1.60       - LAN(REST) connection to IP address
            
        ConType : {'PY', 'QIS', 'QPS'}
            
            Specifies the software type which runs the connection:
            PY  -   (Default) Connection is run via pure Python code
            
            QIS -   Power modules only, connection run via QIS (Quarch Instrument Server) for easy power capture in raw formats. 
                    Serial is not supported. IP and port can be specified to connect to a QIS instance running at another location "QIS:192.168.1.100:9722"
                    
            QPS -   Power modules only, connection run via QPS (Quarch Power Studio) for automated power capture and analysis within thr QPS graphical environment. 
                    Serial is not supported. IP and port can be specified to connect to a QPS instance running at another location "QPS:192.168.1.100:9822"
        
        timeout : str, optional
            
            Timeout in seconds for the device to respond. 
        
        forceFind : str, optional
            
            When using QIS, if a LAN device you wish to connect to is outside the local subnet, enter it's IP address here
            to force a scan and enumeration, otherwise the broadcast scan will probably not find it                    
            
        """
        self.ConString = ConString
        if 'serial' not in ConString.lower():
            self.ConString = ConString.lower()
        else:
            self.ConType = ConType
            try:
                self.timeout = int(timeout)
            except:
                raise Exception('Invalid value for timeout, must be a numeric value')

            self.forceFind = forceFind
            if checkModuleFormat(self.ConString) == False:
                raise Exception('Module format is invalid!')
            elif self.ConType.upper() == 'PY':
                numb_colons = self.ConString.count(':')
                if numb_colons == 2:
                    self.ConString = self.ConString.replace('::', ':')
                self.connectionObj = PYConnection(self.ConString)
                self.ConCommsType = self.connectionObj.ConnTypeStr
                self.connectionName = self.connectionObj.ConnTarget
                self.connectionTypeName = self.connectionObj.ConnTypeStr
                time.sleep(0.1)
                item = None
                item = self.connectionObj.connection.sendCommand('*tst?')
                if 'OK' in item:
                    pass
                elif 'FAIL' in item:
                    pass
                else:
                    if item is not None:
                        pass
                    else:
                        raise Exception('No module responded to *tst? command!')
                    time.sleep(0.1)
            else:
                if self.ConType[:3].upper() == 'QIS':
                    try:
                        QIS, host, port = self.ConType.split(':')
                        port = int(port)
                    except:
                        host = '127.0.0.1'
                        port = 9722

                    numb_colons = self.ConString.count(':')
                    if numb_colons == 1:
                        self.ConString = self.ConString.replace(':', '::')
                    self.connectionObj = QISConnection(self.ConString, host, port)
                    if self.forceFind != 0:
                        self.connectionObj.qis.sendAndReceiveCmd(cmd=('$scan ' + self.forceFind))
                        time.sleep(0.1)
                    list = self.connectionObj.qis.getDeviceList()
                    list_str = ''.join(list).lower()
                    while True:
                        if self.timeout == 0:
                            raise ValueError('Search timeout - no Quarch module found.')
                        elif self.ConString in list_str:
                            break
                        else:
                            time.sleep(1)
                            self.timeout -= 1
                            list = self.connectionObj.qis.getDeviceList()
                            list_str = ''.join(list).lower()

                    self.connectionObj.qis.sendAndReceiveCmd(cmd=('$default ' + self.ConString))
                else:
                    if self.ConType[:3].upper() == 'QPS':
                        try:
                            QIS, host, port = self.ConType.split(':')
                            port = int(port)
                        except:
                            host = '127.0.0.1'
                            port = 9822

                        numb_colons = self.ConString.count(':')
                        if numb_colons == 1:
                            self.ConString = self.ConString.replace(':', '::')
                        self.connectionObj = QPSConnection(host, port)
                    else:
                        raise ValueError('Invalid connection type. Acceptable values [PY,QIS,QPS]')
        logging.debug(os.path.basename(__file__) + ' ConString : ' + str(self.ConString) + ' ConType : ' + str(self.ConType))

    def sendCommand(self, CommandString, expectedResponse=True):
        """
        Executes a text based command on the device.  This is the primary way of controlling a device.  The full command set available to use
        is found in the technical manual for the device.
        
        Parameters
        ----------
        CommandString : str

            The text based command string to send to the device
        
        Returns
        -------
        command_response : str or None

            The response text from the module.  Multiline responses will be seperated with LF. Some commands
            do not return a response and None will be returned

        """
        logging.debug(os.path.basename(__file__) + ': ' + self.ConType[:3] + ' sending command: ' + CommandString)
        if self.ConType[:3] == 'QIS':
            numb_colons = self.ConString.count(':')
            if numb_colons == 1:
                self.ConString = self.ConString.replace(':', '::')
            response = self.connectionObj.qis.sendCmd(self.ConString, CommandString)
            logging.debug(os.path.basename(__file__) + ': ' + self.ConType[:3] + ' received: ' + response)
            return response
        if self.ConType == 'PY':
            response = self.connectionObj.connection.sendCommand(CommandString)
            logging.debug(os.path.basename(__file__) + ': ' + self.ConType[:3] + ' received: ' + response)
            return response
        if self.ConType[:3] == 'QPS':
            if CommandString[0] != '$':
                CommandString = self.ConString + ' ' + CommandString
            response = self.connectionObj.qps.sendCmdVerbose(CommandString)
            logging.debug(os.path.basename(__file__) + ': ' + self.ConType[:3] + ' received: ' + response)
            return response

    def sendBinaryCommand(self, cmd):
        self.connectionObj.connection.Connection.SendCommand(cmd)
        return self.connectionObj.connection.Connection.BulkRead()

    def openConnection(self):
        """
        Opens the connection to the module.  This will be open by default on creation of quarchDevice but this
        allows re-opening if required.
        
        """
        if self.ConType[:3] == 'QIS':
            self.connectionObj.qis.connect()
        else:
            if self.ConType == 'PY':
                del self.connectionObj
                self.connectionObj = PYConnection(self.ConString)
                return self.connectionObj
            if self.ConType[:3] == 'QPS':
                self.connectionObj.qps.connect(self.ConString)

    def closeConnection(self):
        """
        Closes the connection to the module, freeing the module for other uses.  This should always be called whern you are finished with a device.
        
        """
        if self.ConType[:3] == 'QIS':
            self.connectionObj.qis.disconnect()
        else:
            if self.ConType == 'PY':
                self.connectionObj.connection.close()
            else:
                if self.ConType[:3] == 'QPS':
                    self.connectionObj.qps.disconnect(self.ConString)

    def resetDevice(self, timeout=10):
        """
        Issues a power-on-reset command to the device.  Attempts to recover the connection to the module after reset.
        Function halts until the timeout is complete or the module is found
        
        Parameters
        ----------
        timeout : int
            
            Number of seconds to wait for the module to re-enumerate and become available
            
        Returns
        -------
        result : bool
        
            True if the device was found and reconnected, false if it was not and we timed out
        
        """
        logging.debug(os.path.basename(__file__) + ': sending command: *rst')
        if self.ConType[:3] == 'QIS':
            numb_colons = self.ConString.count(':')
            if numb_colons == 1:
                self.ConString = self.ConString.replace(':', '::')
            retval = self.ConString
            self.connectionObj.qis.sendCmd((self.ConString), '*rst', expectedResponse=False)
            logging.debug(os.path.basename(__file__) + ': connecting back to ' + retval)
        else:
            if self.ConType == 'PY':
                retval = self.ConString
                self.connectionObj.connection.sendCommand('*rst', expectedResponse=False)
                self.connectionObj.connection.close()
                logging.debug(os.path.basename(__file__) + ': connecting back to ' + retval)
            else:
                if self.ConType[:3] == 'QPS':
                    retval = self.ConString
                    CommandString = self.ConString + ' ' + '*rst'
                    self.connectionObj.qps.sendCmdVerbose(CommandString, expectedResponse=False)
                    logging.debug(os.path.basename(__file__) + ': connecting back to ' + retval)
                temp = None
                startTime = time.time()
                time.sleep(0.6)
                while temp == None:
                    try:
                        temp = quarchDevice(retval)
                    except:
                        time.sleep(0.2)
                        if time.time() - startTime > timeout:
                            logging.critical(os.path.basename(__file__) + ': connection failed to ' + retval)
                            return False

                self.connectionObj = temp.connectionObj
                time.sleep(1)
                return True

    def sendAndVerifyCommand(self, commandString, responseExpected='OK', exception=True):
        """
        Sends a command to the device and verifies the response is as expected.  This is a simple
        wrapper of sendCommand and helps write cleaner code in test scripts.
        
        Parameters
        ----------
        commandString : str
            
            The text command to send to the device
            
        commandString : str, optional
            
            The expected text response from the module.
            
        exception : bool, optional
        
            If True, an exception is raised on mismatch.  If False, we just return False
            
        Returns
        -------
        result : bool
        
            True if we matched the response, False if we did not
            
        Raises
        ------
        ValueError
            If the response does not match AND the exception parameter is set to True
        
        """
        responseStr = self.sendCommand(commandString)
        if responseStr != responseExpected:
            if exception:
                raise ValueError('Command response error: ' + responseStr)
            else:
                return False
        else:
            return True


def checkModuleFormat(ConString):
    ConnectionTypes = [
     'USB', 'SERIAL', 'TELNET', 'REST', 'TCP']
    conTypeSpecified = ConString[:ConString.find(':')]
    correctConType = False
    for value in ConnectionTypes:
        if value.lower() == conTypeSpecified.lower():
            correctConType = True

    if not correctConType:
        raise Exception('Invalid connection type specified in Module string, use one of [USB|SERIAL|TELNET|REST|TCP]')
        return False
    numb_colons = ConString.count(':')
    if numb_colons > 2 or numb_colons <= 0:
        raise Exception('Invalid number of colons in module string')
        return False
    return True