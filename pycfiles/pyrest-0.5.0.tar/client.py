# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\iress\client.py
# Compiled at: 2012-04-24 02:47:38
__doc__ = "\nPythonic interface to Iress data objects.\n\nThe following example extracts financial data for BHP:\n\n    from client import IressDataClient, DfsSec\n\n    iress = IressDataClient()\n    iress.connect()\n\n    print iress.execute(DfsSec.constants.dfsDataFinancial, dict(\n        Security='BHP',\n        Exchange='ASX',\n        StartDate='2000-01-01',\n        EndDate='2008-01-01',\n        ItemList=-1,\n        AnnualReport=True,\n        QuarterlyReport=True,\n        InterimReport=True,\n        PreliminaryReport=True,\n    ))   \n\n"
import time, logging
from win32com import client
from typelibhelper import EnsureLatestVersion
log = logging.getLogger(__name__)
DfsCmd = EnsureLatestVersion('{96EB07E1-03D0-11CF-B214-00AA002F2ED9}')
DfsPrice = EnsureLatestVersion('{DF120F00-A275-11D1-A122-0000F82508F6}')
DfsSec = EnsureLatestVersion('{AF802C80-B975-11D1-A138-0000F82508F6}')
DfsIndicate = EnsureLatestVersion('{9339DB61-1602-11D2-8FC4-0000F824C8AA}')
DfsTimeSeries = EnsureLatestVersion('{4832E620-C2AA-11D1-A143-0000F82508F6}')
DEFAULT_DATA_TIMEOUT = 15
REQUEST_POLL_INTERVAL = 0.2

class IressError(StandardError):
    pass


class IressDataClient(object):
    """
    Pythonic interface to the Iress data objects automation
    interface.

    """

    def __init__(self):
        self._iress = None
        return

    def connect(self):
        """
        Connects to the running Iress instance.

        """
        self._iress = client.Dispatch('Iress.Application')

    def execute--- This code section failed: ---

 L.  75         0  LOAD_FAST             0  'self'
                3  LOAD_ATTR             0  '_iress'
                6  LOAD_CONST               None
                9  COMPARE_OP            9  is-not
               12  POP_JUMP_IF_TRUE     24  'to 24'
               15  LOAD_ASSERT              AssertionError
               18  LOAD_CONST               'Not connected to Iress instance.'
               21  RAISE_VARARGS_2       2  None

 L.  77        24  LOAD_GLOBAL           3  'log'
               27  LOAD_ATTR             4  'debug'
               30  LOAD_CONST               'Executing query %s with parameters %r.'
               33  LOAD_FAST             1  'name'
               36  LOAD_FAST             2  'params'
               39  CALL_FUNCTION_3       3  None
               42  POP_TOP          

 L.  80        43  LOAD_FAST             0  'self'
               46  LOAD_ATTR             0  '_iress'
               49  LOAD_ATTR             5  'DataManager'
               52  LOAD_ATTR             6  'CreateOb'
               55  LOAD_FAST             1  'name'
               58  CALL_FUNCTION_1       1  None
               61  STORE_FAST            3  'request'

 L.  81        64  LOAD_FAST             3  'request'
               67  LOAD_ATTR             7  'Clear'
               70  CALL_FUNCTION_0       0  None
               73  POP_TOP          

 L.  82        74  SETUP_LOOP           42  'to 119'
               77  LOAD_FAST             2  'params'
               80  LOAD_ATTR             8  'iteritems'
               83  CALL_FUNCTION_0       0  None
               86  GET_ITER         
               87  FOR_ITER             28  'to 118'
               90  UNPACK_SEQUENCE_2     2 
               93  STORE_FAST            4  'k'
               96  STORE_FAST            5  'v'

 L.  83        99  LOAD_GLOBAL           9  'setattr'
              102  LOAD_FAST             3  'request'
              105  LOAD_FAST             4  'k'
              108  LOAD_FAST             5  'v'
              111  CALL_FUNCTION_3       3  None
              114  POP_TOP          
              115  JUMP_BACK            87  'to 87'
              118  POP_BLOCK        
            119_0  COME_FROM            74  '74'

 L.  85       119  LOAD_FAST             0  'self'
              122  LOAD_ATTR            10  '_do_request'
              125  LOAD_FAST             3  'request'
              128  CALL_FUNCTION_1       1  None
              131  POP_TOP          

 L.  86       132  LOAD_GLOBAL           3  'log'
              135  LOAD_ATTR             4  'debug'
              138  LOAD_CONST               '%i rows returned.'
              141  LOAD_FAST             3  'request'
              144  LOAD_ATTR            11  'RowCount'
              147  CALL_FUNCTION_2       2  None
              150  POP_TOP          

 L.  89       151  BUILD_LIST_0          0 
              154  STORE_FAST            6  'results'

 L.  90       157  LOAD_FAST             3  'request'
              160  LOAD_ATTR            11  'RowCount'
              163  LOAD_CONST               0
              166  COMPARE_OP            4  >
              169  POP_JUMP_IF_FALSE   238  'to 238'

 L.  91       172  LOAD_FAST             3  'request'
              175  LOAD_ATTR            12  'AvailableFields'
              178  LOAD_GLOBAL          13  'False'
              181  CALL_FUNCTION_1       1  None
              184  STORE_FAST            7  'fields'

 L.  92       187  SETUP_LOOP           48  'to 238'
              190  LOAD_FAST             3  'request'
              193  LOAD_ATTR            14  'GetRows'
              196  GET_ITER         
              197  FOR_ITER             34  'to 234'
              200  STORE_FAST            8  'row'

 L.  93       203  LOAD_FAST             6  'results'
              206  LOAD_ATTR            15  'append'
              209  LOAD_GLOBAL          16  'dict'
              212  LOAD_GLOBAL          17  'zip'
              215  LOAD_FAST             7  'fields'
              218  LOAD_FAST             8  'row'
              221  CALL_FUNCTION_2       2  None
              224  CALL_FUNCTION_1       1  None
              227  CALL_FUNCTION_1       1  None
              230  POP_TOP          
              231  JUMP_BACK           197  'to 197'
              234  POP_BLOCK        
            235_0  COME_FROM           187  '187'
              235  JUMP_FORWARD          0  'to 238'
            238_0  COME_FROM           187  '187'

 L.  94       238  LOAD_FAST             6  'results'
              241  RETURN_VALUE     

Parse error at or near `LOAD_FAST' instruction at offset 238

    def _do_request(self, request):
        request.Request()
        while self._wait_for_data(request):
            request.RequestNext()

    def _wait_for_data(self, request, timeout=DEFAULT_DATA_TIMEOUT):
        """
        Waits for data to be received from Iress. Returns True if
        another request is required.

        """
        running_time = 0
        while request.state == DfsCmd.constants.DataPending:
            time.sleep(REQUEST_POLL_INTERVAL)
            running_time += REQUEST_POLL_INTERVAL
            if running_time > timeout:
                raise IressError('Timed out waiting for data.')

        if request.state == DfsCmd.constants.DataReady:
            return False
        if request.state == DfsCmd.constants.Error:
            raise IressError(request.Error)
        elif request.state == DfsCmd.constants.DataIncomplete:
            raise IressError('Data was incomplete at the time of request.')
        else:
            if request.state == DfsCmd.constants.DataMorePending:
                log.debug('More data required.')
                return True
            raise IressError('Unkown Error.')


if __name__ == '__main__':
    iress = IressDataClient()
    iress.connect()
    logging.basicConfig(level=logging.DEBUG)
    r = iress.execute(DfsIndicate.constants.dfsDataHistoricalMarketCapitalisation, dict(StartDate='01/05/2009', EndDate='01/05/2009', IndexFilter='XJO', Exchange='ASX'))
    print len(r)