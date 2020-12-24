# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/alpha1p/robot/robot.py
# Compiled at: 2020-04-14 08:04:08
# Size of source mod 2**32: 35339 bytes
from .control import *
from .bthandler import *
import serial, time, usb, serial.tools.list_ports, threading, sys
__all__ = [
 'Alpha1S']
INIT_STAND = {'runTime':1200, 
 'totalTime':1200, 
 'jointAngle':[
  90, 90, 90, 90, 90, 90, 90, 60, 76, 110, 90, 90, 120, 104, 70, 90]}
LAST_SLAUTE = [
 [
  [
   90, 90, 90, 90, 90, 90, 90, 60, 76, 110, 90, 90, 120, 104, 70, 90, 90, 90, 90, 90], 1500, 1500],
 [
  [
   120, 40, 59, 133, 133, 107, 90, 57, 140, 70, 90, 90, 125, 46, 108, 90, 90, 90, 90, 90], 1500, 1500],
 [
  [
   120, 35, 39, 133, 163, 157, 90, 57, 140, 70, 90, 90, 125, 46, 108, 90, 90, 90, 90, 90], 800, 1500],
 [
  [
   120, 40, 59, 133, 133, 107, 90, 57, 140, 70, 90, 90, 125, 48, 107, 90, 90, 90, 90, 90], 800, 800],
 [
  [
   90, 35, 48, 90, 154, 130, 90, 60, 76, 110, 90, 90, 120, 104, 70, 90, 90, 90, 90, 90], 800, 800]]

def lock(func):

    def wrapper(self, *args, **kwargs):
        self.lock.acquire()
        resut = func(self, *args, **kwargs)
        self.lock.release()
        return resut

    return wrapper


def get_input(options=[
 'y', 'n']):
    value = ''
    while value not in options:
        value = input()

    return value


class DaemonThread(threading.Thread):

    def __init__(self, robot, time):
        threading.Thread.__init__(self)
        self.robot = robot
        self.heat_time = time

    def run--- This code section failed: ---

 L.  54         0  LOAD_GLOBAL              print
                2  LOAD_STR                 '守护线程已经启动！'
                4  CALL_FUNCTION_1       1  ''
                6  POP_TOP          

 L.  56      8_10  SETUP_LOOP          676  'to 676'
             12_0  COME_FROM           536  '536'
               12  LOAD_FAST                'self'
               14  LOAD_ATTR                robot
               16  LOAD_ATTR                is_alive
            18_20  POP_JUMP_IF_FALSE   674  'to 674'

 L.  57        22  LOAD_GLOBAL              time
               24  LOAD_METHOD              sleep
               26  LOAD_FAST                'self'
               28  LOAD_ATTR                heat_time
               30  CALL_METHOD_1         1  ''
               32  POP_TOP          

 L.  58        34  LOAD_FAST                'self'
               36  LOAD_ATTR                robot
               38  LOAD_METHOD              get_response
               40  CALL_METHOD_0         0  ''
               42  STORE_FAST               'response'

 L.  59        44  LOAD_FAST                'response'
               46  LOAD_STR                 ''
               48  COMPARE_OP               !=
            50_52  POP_JUMP_IF_FALSE   524  'to 524'

 L.  60        54  LOAD_CONST               1
               56  LOAD_CONST               3
               58  LOAD_CONST               5
               60  LOAD_CONST               6
               62  LOAD_CONST               7
               64  LOAD_CONST               8
               66  LOAD_CONST               11
               68  LOAD_CONST               12
               70  LOAD_CONST               13
               72  LOAD_CONST               14
               74  LOAD_CONST               15
               76  LOAD_CONST               16
               78  LOAD_CONST               17
               80  LOAD_CONST               24
               82  LOAD_CONST               25
               84  LOAD_CONST               32
               86  LOAD_CONST               34

 L.  61        88  LOAD_CONST               35
               90  LOAD_CONST               36
               92  LOAD_CONST               37
               94  LOAD_CONST               38
               96  LOAD_CONST               39
               98  LOAD_CONST               40
              100  LOAD_CONST               41
              102  LOAD_CONST               42
              104  LOAD_CONST               43
              106  LOAD_CONST               49
              108  LOAD_CONST               50
              110  LOAD_CONST               51
              112  LOAD_CONST               52
              114  BUILD_LIST_30        30 
              116  STORE_FAST               'single_type'

 L.  62   118_120  SETUP_LOOP          672  'to 672'
              122  LOAD_GLOBAL              len
              124  LOAD_FAST                'response'
              126  CALL_FUNCTION_1       1  ''
              128  LOAD_CONST               0
              130  COMPARE_OP               !=
          132_134  POP_JUMP_IF_FALSE   520  'to 520'

 L.  63       136  LOAD_CONST               True
              138  STORE_FAST               'success'

 L.  64   140_142  SETUP_EXCEPT        472  'to 472'

 L.  65       144  LOAD_FAST                'response'
              146  LOAD_METHOD              index
              148  LOAD_CONST               b'\xfb\xbf'
              150  LOAD_CONST               0
              152  CALL_METHOD_2         2  ''
              154  STORE_FAST               'p_start'

 L.  66       156  LOAD_FAST                'response'
              158  LOAD_FAST                'p_start'
              160  LOAD_CONST               2
              162  BINARY_ADD       
              164  BINARY_SUBSCR    
              166  STORE_FAST               'cmd_len'

 L.  67       168  LOAD_FAST                'response'
              170  LOAD_FAST                'p_start'
              172  LOAD_CONST               3
              174  BINARY_ADD       
              176  BINARY_SUBSCR    
              178  STORE_FAST               'cmd_type'

 L.  68       180  LOAD_FAST                'p_start'
              182  LOAD_FAST                'cmd_len'
              184  BINARY_ADD       
              186  STORE_FAST               'end'

 L.  70       188  LOAD_FAST                'cmd_type'
              190  LOAD_FAST                'single_type'
              192  COMPARE_OP               in
              194  POP_JUMP_IF_FALSE   198  'to 198'

 L.  71       196  JUMP_FORWARD        426  'to 426'
            198_0  COME_FROM           194  '194'

 L.  72       198  LOAD_FAST                'cmd_type'
              200  LOAD_CONST               2
              202  COMPARE_OP               ==
          204_206  POP_JUMP_IF_FALSE   282  'to 282'

 L.  73       208  SETUP_LOOP          426  'to 426'

 L.  74       210  SETUP_EXCEPT        238  'to 238'

 L.  75       212  LOAD_FAST                'response'
              214  LOAD_METHOD              index
              216  LOAD_CONST               b'\xfb\xbf\x06\x81'
              218  LOAD_FAST                'end'
              220  CALL_METHOD_2         2  ''
              222  STORE_FAST               'tmp_start'

 L.  76       224  LOAD_FAST                'tmp_start'
              226  LOAD_CONST               6
              228  BINARY_ADD       
              230  STORE_FAST               'end'

 L.  77       232  BREAK_LOOP       
              234  POP_BLOCK        
              236  JUMP_BACK           210  'to 210'
            238_0  COME_FROM_EXCEPT    210  '210'

 L.  78       238  DUP_TOP          
              240  LOAD_GLOBAL              ValueError
              242  COMPARE_OP               exception-match
          244_246  POP_JUMP_IF_FALSE   274  'to 274'
              248  POP_TOP          
              250  POP_TOP          
              252  POP_TOP          

 L.  79       254  LOAD_FAST                'response'
              256  LOAD_FAST                'self'
              258  LOAD_ATTR                robot
              260  LOAD_METHOD              get_response
              262  CALL_METHOD_0         0  ''
              264  INPLACE_ADD      
              266  STORE_FAST               'response'

 L.  80       268  CONTINUE_LOOP       210  'to 210'
              270  POP_EXCEPT       
              272  JUMP_BACK           210  'to 210'
            274_0  COME_FROM           244  '244'
              274  END_FINALLY      
              276  JUMP_BACK           210  'to 210'
              278  POP_BLOCK        
              280  JUMP_FORWARD        426  'to 426'
            282_0  COME_FROM           204  '204'

 L.  81       282  LOAD_FAST                'cmd_type'
              284  LOAD_CONST               10
              286  COMPARE_OP               ==
          288_290  POP_JUMP_IF_FALSE   400  'to 400'

 L.  82       292  SETUP_LOOP          426  'to 426'
              294  LOAD_FAST                'cmd_type'
              296  LOAD_CONST               10
              298  COMPARE_OP               ==
          300_302  POP_JUMP_IF_FALSE   396  'to 396'

 L.  83       304  SETUP_EXCEPT        368  'to 368'

 L.  84       306  LOAD_FAST                'response'
              308  LOAD_METHOD              index
              310  LOAD_CONST               b'\xfb\xbf'
              312  LOAD_FAST                'end'
              314  CALL_METHOD_2         2  ''
              316  STORE_FAST               'tmp_start'

 L.  85       318  LOAD_FAST                'response'
              320  LOAD_FAST                'tmp_start'
              322  LOAD_CONST               2
              324  BINARY_ADD       
              326  BINARY_SUBSCR    
              328  STORE_FAST               'cmd_len'

 L.  86       330  LOAD_FAST                'response'
              332  LOAD_FAST                'tmp_start'
              334  LOAD_CONST               3
              336  BINARY_ADD       
              338  BINARY_SUBSCR    
              340  STORE_FAST               'cmd_type'

 L.  87       342  LOAD_FAST                'cmd_type'
              344  LOAD_CONST               10
              346  COMPARE_OP               ==
          348_350  POP_JUMP_IF_FALSE   362  'to 362'

 L.  88       352  LOAD_FAST                'tmp_start'
              354  LOAD_GLOBAL              ßcmd_len
              356  BINARY_ADD       
              358  STORE_FAST               'end'
              360  JUMP_FORWARD        364  'to 364'
            362_0  COME_FROM           348  '348'

 L.  90       362  BREAK_LOOP       
            364_0  COME_FROM           360  '360'
              364  POP_BLOCK        
              366  JUMP_BACK           294  'to 294'
            368_0  COME_FROM_EXCEPT    304  '304'

 L.  91       368  DUP_TOP          
              370  LOAD_GLOBAL              ValueError
              372  COMPARE_OP               exception-match
          374_376  POP_JUMP_IF_FALSE   390  'to 390'
              378  POP_TOP          
              380  POP_TOP          
              382  POP_TOP          

 L.  92       384  BREAK_LOOP       
              386  POP_EXCEPT       
              388  JUMP_BACK           294  'to 294'
            390_0  COME_FROM           374  '374'
              390  END_FINALLY      
          392_394  JUMP_BACK           294  'to 294'
            396_0  COME_FROM           300  '300'
              396  POP_BLOCK        
              398  JUMP_FORWARD        426  'to 426'
            400_0  COME_FROM           288  '288'

 L.  94       400  LOAD_GLOBAL              print
              402  LOAD_STR                 '发现未知命令，命令内容为：%s'
              404  LOAD_FAST                'response'
              406  LOAD_FAST                'p_start'
              408  LOAD_FAST                'end'
              410  LOAD_CONST               1
              412  BINARY_ADD       
              414  BUILD_SLICE_2         2 
              416  BINARY_SUBSCR    
              418  CALL_FUNCTION_2       2  ''
              420  POP_TOP          

 L.  95       422  LOAD_CONST               False
              424  STORE_FAST               'success'
            426_0  COME_FROM           398  '398'
            426_1  COME_FROM_LOOP      292  '292'
            426_2  COME_FROM           280  '280'
            426_3  COME_FROM_LOOP      208  '208'
            426_4  COME_FROM           196  '196'

 L.  96       426  LOAD_FAST                'success'
          428_430  POP_JUMP_IF_FALSE   452  'to 452'

 L.  97       432  LOAD_GLOBAL              parsing_all_response
              434  LOAD_FAST                'response'
              436  LOAD_FAST                'p_start'
              438  LOAD_FAST                'end'
              440  LOAD_CONST               1
              442  BINARY_ADD       
              444  BUILD_SLICE_2         2 
              446  BINARY_SUBSCR    
              448  CALL_FUNCTION_1       1  ''
              450  POP_TOP          
            452_0  COME_FROM           428  '428'

 L.  98       452  LOAD_FAST                'response'
              454  LOAD_FAST                'end'
              456  LOAD_CONST               1
              458  BINARY_ADD       
              460  LOAD_CONST               None
              462  BUILD_SLICE_2         2 
              464  BINARY_SUBSCR    
              466  STORE_FAST               'response'
              468  POP_BLOCK        
              470  JUMP_BACK           122  'to 122'
            472_0  COME_FROM_EXCEPT    140  '140'

 L.  99       472  DUP_TOP          
              474  LOAD_GLOBAL              ValueError
              476  COMPARE_OP               exception-match
          478_480  POP_JUMP_IF_FALSE   516  'to 516'
              482  POP_TOP          
              484  POP_TOP          
              486  POP_TOP          

 L. 100       488  LOAD_GLOBAL              len
              490  LOAD_FAST                'response'
              492  CALL_FUNCTION_1       1  ''
              494  STORE_FAST               'end'

 L. 101       496  LOAD_FAST                'response'
              498  LOAD_FAST                'end'
              500  LOAD_CONST               1
              502  BINARY_ADD       
              504  LOAD_CONST               None
              506  BUILD_SLICE_2         2 
              508  BINARY_SUBSCR    
              510  STORE_FAST               'response'
              512  POP_EXCEPT       
              514  JUMP_BACK           122  'to 122'
            516_0  COME_FROM           478  '478'
              516  END_FINALLY      
              518  JUMP_BACK           122  'to 122'
            520_0  COME_FROM           132  '132'
              520  POP_BLOCK        
              522  JUMP_BACK            12  'to 12'
            524_0  COME_FROM            50  '50'

 L. 103       524  LOAD_FAST                'self'
              526  LOAD_ATTR                robot
              528  LOAD_METHOD              heart_beat
              530  CALL_METHOD_0         0  ''
              532  STORE_FAST               'flag'

 L. 104       534  LOAD_FAST                'flag'
              536  POP_JUMP_IF_TRUE     12  'to 12'

 L. 105       538  LOAD_FAST                'self'
              540  LOAD_ATTR                robot
              542  LOAD_ATTR                lock
              544  LOAD_METHOD              acquire
              546  CALL_METHOD_0         0  ''
              548  POP_TOP          

 L. 106       550  LOAD_CONST               False
              552  LOAD_FAST                'self'
              554  LOAD_ATTR                robot
              556  STORE_ATTR               is_alive

 L. 107       558  LOAD_GLOBAL              print
              560  LOAD_STR                 '机器人连接已断开，正在尝试重新连接。。。'
              562  CALL_FUNCTION_1       1  ''
              564  POP_TOP          

 L. 109       566  LOAD_FAST                'self'
              568  LOAD_METHOD              reconnect_robot_automatic
              570  CALL_METHOD_0         0  ''
              572  POP_TOP          

 L. 111       574  LOAD_FAST                'self'
              576  LOAD_ATTR                robot
              578  LOAD_ATTR                is_alive
          580_582  POP_JUMP_IF_TRUE    660  'to 660'

 L. 112       584  LOAD_GLOBAL              print
              586  LOAD_STR                 '机器人自动重连失败，请手动关闭机器人再次尝试连接!'
              588  CALL_FUNCTION_1       1  ''
              590  POP_TOP          

 L. 113       592  LOAD_GLOBAL              print
              594  LOAD_STR                 '请选择是否手动重启？y/n'
              596  CALL_FUNCTION_1       1  ''
              598  POP_TOP          

 L. 114       600  LOAD_GLOBAL              get_input
              602  CALL_FUNCTION_0       0  ''
              604  STORE_FAST               'confirm'

 L. 115       606  SETUP_LOOP          660  'to 660'
            608_0  COME_FROM           636  '636'
              608  LOAD_FAST                'confirm'
              610  LOAD_STR                 'y'
              612  COMPARE_OP               ==
          614_616  POP_JUMP_IF_FALSE   658  'to 658'

 L. 116       618  LOAD_FAST                'self'
              620  LOAD_METHOD              reconnect_robot_manually
              622  CALL_METHOD_0         0  ''
              624  POP_TOP          

 L. 117       626  LOAD_STR                 'end'
              628  STORE_FAST               'confirm'

 L. 118       630  LOAD_FAST                'self'
              632  LOAD_ATTR                robot
              634  LOAD_ATTR                is_alive
          636_638  POP_JUMP_IF_TRUE    608  'to 608'

 L. 119       640  LOAD_GLOBAL              print
              642  LOAD_STR                 '手动连接失败，是否再次尝试手动连接？y/n'
              644  CALL_FUNCTION_1       1  ''
              646  POP_TOP          

 L. 120       648  LOAD_GLOBAL              get_input
              650  CALL_FUNCTION_0       0  ''
              652  STORE_FAST               'confirm'
          654_656  JUMP_BACK           608  'to 608'
            658_0  COME_FROM           614  '614'
              658  POP_BLOCK        
            660_0  COME_FROM_LOOP      606  '606'
            660_1  COME_FROM           580  '580'

 L. 121       660  LOAD_FAST                'self'
              662  LOAD_ATTR                robot
              664  LOAD_ATTR                lock
              666  LOAD_METHOD              release
              668  CALL_METHOD_0         0  ''
              670  POP_TOP          
            672_0  COME_FROM_LOOP      118  '118'
              672  JUMP_BACK            12  'to 12'
            674_0  COME_FROM            18  '18'
              674  POP_BLOCK        
            676_0  COME_FROM_LOOP        8  '8'

Parse error at or near `COME_FROM' instruction at offset 674_0

    def reconnect_robot_automatic(self, times=3):
        con_num = 1
        while con_num <= times:
            print('正在进行第%d次尝试连接。。。' % con_num)
            time.sleep(2)
            self.robot.connect_to_PC(tips=False)
            if self.robot.dev != 0:
                self.robot.is_alive = True
                print('机器人已重新连接！')
                break
            else:
                con_num += 1

    def reconnect_robot_manually(self, times=3):
        print('机器人是否已完成手动重启？y/n')
        confirm_2 = get_input()
        if confirm_2 == 'y':
            self.reconnect_robot_automatic()


class Alpha1S:

    def __init__(self, con_type, vendor=1155, product=22352, port='/dev/cu.Alpha1_E983-SerialPort', baud_rate=9600, timeout=0.5):
        self.con_type = con_type
        self.vendor = vendor
        self.product = product
        self.port = port
        self.baud_rate = baud_rate
        self.timeout = timeout
        self.execute_action = self.multi_control
        self.lock = threading.RLock()
        self.sound_status = self.play_status = self.sound_size = self.light_status = self.tf_card = None
        if self.con_type == 'usb':
            self.get_response = self._Alpha1S__usb_get_response
        elif self.con_type == 'bt':
            self.get_response = self._Alpha1S__bt_get_response
        else:
            print("请选则正确的连接类型：'usb'或者'bt\\’，目前连接类型为：%s", self.con_type)
        self.connect_to_PC()
        if self.dev == 0:
            sys.exit(0)
        self.handshake()
        self.get_robot_status()
        self.version = 'Soft Version:{}    Hard Version:{}'.formatself._Alpha1S__soft_version()self._Alpha1S__hard_version()
        self.get_udid(tips=False)
        self.get_sn(tips=False)
        self.open_daemon_thread(20)

    def connect_to_PC(self, tips=True):
        if self.con_type == 'usb':
            try:
                self.dev, self.ep, self.r_ep, self.r_ps = establish_usb_connection(self.vendor, self.product)
                self._Alpha1S__clear_usb_output(tips=False)
                self.change_usb_type(usb_write=True)
                time.sleep(1)
            except TypeError as e:
                try:
                    pass
                finally:
                    e = None
                    del e

            port_list = list(serial.tools.list_ports.comports())
            self.port = port_list[(-1)][0]
        self.dev = establish_bt_connection((self.port), (self.baud_rate), (self.timeout), tips=tips)

    def reset(self):
        self.__init__(self.con_type)
        if self.dev != 0:
            rec_con = True
            print('机器人已重新连接！')
        else:
            rec_con = False
        return rec_con

    def __usb_output(self):
        """
        读取机器人的输出
        """
        response = self.dev.readself.r_epself.r_ps
        return response

    def read(self):
        """
        读取机器人的输出
        """
        response = self.dev.read_all()
        return response

    def write(self, cmd):
        """
        功能：以Bluetooth形式执行单个命令。
        输入：单个执行命令。
        """
        self.dev.write(cmd)

    def __usb_write(self, cmd):
        """
        功能：以Bluetooth形式执行单个命令。
        输入：单个执行命令。
        """
        self.dev.writeself.epcmd

    @lock
    def __usb_get_response(self, duration=0, timeout=1000):
        response = ''
        i = 0
        if duration != 0:
            timeout = duration / 100
        else:
            timeout = timeout / 100
        while True:
            tmp = self.dev.read(64)
            if tmp != '':
                response += usb_reformat_response(tmp)
            else:
                break

        while response == '' or duration != 0:
            while True:
                tmp = self.dev.read(64)
                if tmp != '':
                    response += usb_reformat_response(tmp)
                else:
                    break

            if i >= timeout:
                break
            time.sleep(0.1)
            i += 1

        return response

    @lock
    def __bt_get_response(self, duration=0, timeout=1000):
        response = ''
        i = 0
        if duration != 0:
            timeout = duration / 100
        else:
            timeout = timeout / 100
        response = self.read()
        while response == '' or duration != 0:
            while True:
                tmp = self.read()
                if tmp != '':
                    response += tmp
                else:
                    break

            if i >= timeout:
                break
            time.sleep(0.1)
            i += 1

        return response

    def clear_output(self, tips=False, duration=0, timeout=100):
        self._Alpha1S__bt_get_responsedurationtimeout
        if tips:
            print('机器人输出管道已初始化！')

    @lock
    def change_usb_type(self, c_type=2, usb_write=False):
        """
        功能：更改机器人与pc的USB连接类型。
        输入：
        c_type：USB连接类型，数据格式为int。取值范围1~3，1：U盘模式；2：VCP模式：3：HID模式。
                pyusb默认连接为HID模式，因此本函数默认更改为VCP模式。
        返回：空
        """
        cmd_list = [
         249, 159]
        parameters = [c_type, 0, 0, 0, 0, 0]
        for x in parameters:
            cmd_list.append(x)

        checkSum = 0
        for x in cmd_list[2:]:
            checkSum += x

        cmd_list.append(checkSum % 256)
        cmd_list.append(237)
        cmd = serial.to_bytes(cmd_list)
        if usb_write:
            self._Alpha1S__usb_write(cmd)
        else:
            self.write(cmd)

    def open_daemon_thread(self, heart_time=20):
        """
        功能：开启守护线程，防止机器人断线
        输入：
        heart_time:心跳包发送间隔时间，单位s。
        返回：空
        """
        self.heart_time = heart_time
        self.is_alive = True
        self.Daemon = DaemonThread(robot=self, time=heart_time)
        self.Daemon.start()

    def close_daemon_thread(self):
        """
        功能：关闭守护线程。
        输入：空
        返回：空
        """
        self.is_alive = False
        time.sleep(self.heart_time)

    @lock
    def execute_actions(self, list_actions):
        """
        list_actions:\u3000必须是列表形式的动作序列，如以上的last_slaute
        """
        for item in list_actions:
            cmd = {'jointAngle':item[0], 
             'runTime':item[1],  'totalTime':item[2]}
            self.multi_control(cmd)
            time.sleep((item[2] - 40) / 1000.0)

    def stand(self):
        self.execute_action(INIT_STAND)

    def salute(self):
        self.execute_actions(LAST_SLAUTE)

    def power_on_single(self, joint_id):
        """
        功能：为单个舵机恢复加电状态。
        输入：
        joint_id：舵机ID
        返回：空
        """
        angle = self.read_back_single(joint_id)
        cmd = {'joint_id':joint_id,  'jointAngle':angle,  'runTime':400,  'totalTime':400}
        self.single_control(cmd)

    def power_on_all(self):
        """
        功能：为所有舵机恢复加电状态。
        输入：空
        返回：空
        """
        angles = self.read_back_all()
        cmd = {'jointAngle':angles,  'runTime':400,  'totalTime':400}
        self.multi_control(cmd)

    @lock
    def handshake(self):
        """
        功能：连接机器人之后与机器人进行握手操作，获取机器人的名字。
        输入：空
        返回：机器人的名字。
        """
        action_name = ''
        cmd = packageCommand([0], 'handShake')
        self.clear_output()
        self.write(cmd)
        if self.con_type == 'bt':
            timeout = 1500
        else:
            response = self.get_response(duration=timeout)
            if len(response) == 17:
                self.name = parsing_handshake(response)
            elif len(response) > 17:
                self.name = parsing_handshake(response[:17])
                action_name = parsing_play_end(response[17:])
            else:
                print(response)
                print('与机器人握手失败，请重试！')
            print('Action name:%s\n' % action_name)
            if self.con_type == 'bt':
                print('当前通信方式为蓝牙串口通信！')
            else:
                print('当前通信方式为USB串口通信！')

    @lock
    def get_action_list(self, recept_time=4):
        """
        功能：获取机器人本机的动作表。
        输入：空
        返回：动作表，数据格式：list。
        """
        cmd = packageCommand([0], 'get_action_list')
        self.clear_output()
        self.write(cmd)
        response = ''
        while True:
            response += self.get_response()
            try:
                action_list = parsing_get_action_list(response)
                break
            except ValueError:
                continue

        action_list = parsing_get_action_list(response)
        return action_list

    @lock
    def execute_action_table(self, action_name):
        """
        功能：执行机器人上面的一个动作表。
        输入：
        action_name:动作表名称，数据类型为str
        返回：是否执行成功。
        """
        self.is_runing = True
        cmd = packageCommand(action_name.encode(encoding='gbk'), 'execute_action_table')
        self.clear_output()
        self.write(cmd)
        response = self.get_response()
        parsing_execute_action_table(response)

    @lock
    def stop(self, tips=True):
        """
        功能：停止机器人正在执行的动作表。
        输入：空
        返回：空。
        """
        cmd = packageCommand([0], 'stop_play')
        self.clear_output()
        self.write(cmd)
        if tips:
            response = self.get_response()
            if len(response) == 7:
                response += self.get_response()
            action_name = parsing_play_end(response[7:])
            if response[3] == 5:
                if response[4] == 1:
                    if action_name != '':
                        print('机器人已停止运动，动作表“%s”已结束执行！' % action_name)
                else:
                    print('停止指令执行成功，机器人已停止行动！')
            else:
                print('机器人停止指令执行失败！')
                return
        else:
            self.clear_output(timeout=1000)

    def turn_on_sound(self, tips=False):
        self._Alpha1S__sound_switch1tips

    def turn_off_sound(self, tips=False):
        self._Alpha1S__sound_switch0tips

    @lock
    def __sound_switch(self, switch, tips=False):
        """
        功能：机器人声音开关。
        输入：
        switch:根据switch内容控制机器人声音开关。switch数据类型为int，取值范围0或1，为0时关闭声音，当为1时打开声音。
        返回：空。
        """
        cmd = packageCommand([switch], 'sound_switch')
        self.write(cmd)
        self.clear_output(timeout=1000)

    def play(self):
        self._Alpha1S__play_switch(1)

    def pause(self):
        self._Alpha1S__play_switch(0)

    @lock
    def __play_switch(self, switch):
        """
        功能：机器人播放开关。
        输入：
        switch:根据switch内容控制机器人运动或者暂停。switch数据类型为int，取值范围0或1，当为0时暂停播放，为1时继续播放。
        返回：空。
        """
        cmd = packageCommand([switch], 'play_switch')
        self.write(cmd)
        self.clear_output(timeout=1000)

    @lock
    def heart_beat(self):
        """
        功能：向机器人发送心跳包命令。
        输入：空
        返回：确定机器人在线。
        """
        response = ''
        i = 0
        cmd = packageCommand([0], 'heart_beat')
        self.clear_output()
        try:
            self.write(cmd)
        except OSError:
            return False
        else:
            response = self.get_response()
            flag = parsing_heart_beat(response)
            return flag

    @lock
    def get_robot_status(self, tips=True):
        """
        功能：获取机器人当前状态信息。
        输入：空
        返回：空
        """
        response = ''
        i = 0
        cmd = packageCommand([0], 'robot_status')
        self.clear_output()
        self.write(cmd)
        response = self.get_response()
        self.is_mute, self.play_status, self.sound_size, self.light_status, self.tf_card = parsing_get_robot_status(response)
        if tips:
            mute_s = '是' if self.is_mute else '否'
            play_s = '播放中' if self.play_status else '暂停中'
            light_s = '开' if self.light_status else '关'
            tf_s = '已插入' if self.tf_card else '已拔出'
            print('======机器人当前状态======\n静音: %s\n状态: %s\n音量: %d\n灯光: %s\n内存卡: %s' % (
             mute_s, play_s, self.sound_size, light_s, tf_s))

    @lock
    def set_sound(self, size):
        """
        功能：设置机器人音量。
        输入：
        size：音量大小，取值范围为0~100。
        返回：空。
        """
        response = ''
        if size > 100:
            size = 100
        elif size < 0:
            size = 0
        self.sound_size = size
        size = int(255 * size / 100)
        cmd = packageCommand([size], 'set_sound')
        self.write(cmd)
        self.clear_output(timeout=1000)

    @lock
    def power_down(self):
        """
        功能：所有舵机进行掉电操作。
        输入：空
        返回：空。
        """
        cmd = packageCommand([0], 'power_down')
        self.write(cmd)
        self.clear_output(timeout=1000)

    def turn_on_light(self, tips=False):
        self._Alpha1S__light_switch1tips

    def turn_off_light(self, tips=False):
        self._Alpha1S__light_switch0tips

    @lock
    def __light_switch(self, switch, tips=False):
        """
        功能：机器人灯光开关。
        输入：
        switch:根据switch内容控制机器人的灯光。switch数据类型为int，取值范围0或1，当为0时打开灯光，为1时关闭灯光。
        返回：空。
        """
        cmd = packageCommand([switch], 'light_switch')
        self.clear_output()
        self.write(cmd)
        response = self.get_response()
        if len(response) == 15:
            if response[3] == 13:
                response = response[7:]
            elif len(response) == 7:
                if response[3] == 13:
                    response = self.get_response()
            self.light_status = bool(response[5])
            if tips:
                if self.light_status:
                    print('舵机灯已打开！')
        else:
            print('舵机灯已关闭！')

    @lock
    def sync_time(self):
        """
        功能：同步机器人的时钟。
        输入：空
        返回：空。
        """
        cmd = get_set_time_cmd(time.localtime())
        self.clear_output()
        self.write(cmd)
        response = self.get_response()
        if response == '':
            print('机器人没有应答，时钟可能设置失败，请重试！')
        elif response[4] == 1:
            print('时钟设置失败，请重试！')

    @lock
    def read_alarm(self, is_call=False, tips=True):
        """
        功能：读取机器人的闹钟。
        输入：空
        返回：空。
        """
        cmd = packageCommand([0], 'read_alarm')
        self.clear_output()
        self.write(cmd)
        response = self.get_response()
        alarm = parsing_read_alarm(response)
        if is_call:
            return alarm
        if tips:
            switch = '开' if alarm['switch'] else '关'
            every_day = '开' if alarm['every_day'] else '关'
            times = '{}:{}:{}'.format(str(alarm['hour']).rjust2'0', str(alarm['min']).rjust2'0', str(alarm['sec']).rjust2'0')
            print('======机器人闹钟======\n闹钟开关: %s\n每日重复: %s\n响铃时间: %s\n闹钟舞蹈: %s\n' % (
             switch, every_day, times, alarm['action_name']))

    @lock
    def set_alarm(self, switch=None, every_day=None, hour=None, minute=None, sec=None, action_name=None, tips=False):
        """
        功能：设置机器人的闹钟。
        输入：
        switch:闹钟开关，数据格式bool。
        every_day:是否每天开启闹钟，数据格式bool。
        hour:时，数据格式int，取值范围0~23。
        minute:分，数据格式int，取值范围0~59。
        sec:秒，数据格式int，取值范围0~59。
        action_name:舞蹈名称，数据格式string。
        tips:是否验证设置成功，数据格式bool。
        返回：空。
        """
        alarm = self.read_alarm(is_call=True)
        if switch is not None:
            alarm['switch'] = switch
        else:
            if every_day is not None:
                alarm['every_day'] = every_day
            if hour is not None:
                if hour < 0:
                    hour = 0
                elif hour > 23:
                    hour = 23
                alarm['hour'] = hour
            if minute is not None:
                if minute < 0:
                    minute = 0
                elif minute > 59:
                    minute = 59
                alarm['min'] = minute
            if sec is not None:
                if minute < 0:
                    minute = 0
                elif minute > 59:
                    minute = 59
                alarm['sec'] = sec
            if action_name is not None:
                alarm['action_name'] = action_name
            cmd = get_set_alarm_cmd(alarm)
            self.write(cmd)
            if tips:
                alarm_new = self.read_alarm(is_call=True)
                if alarm == alarm_new:
                    print('闹钟设置成功！')
                else:
                    print(alarm, alarm_new)
                    print('闹钟设置失败，请重试！')
            else:
                self.clear_output(timeout=1000)

    def __soft_version(self):
        """
        功能：获取机器人的软件版本。
        输入：空
        返回：
        version:机器人的软件版本，格式为string
        """
        cmd = packageCommand([0], 'soft_version')
        self.clear_output()
        self.write(cmd)
        response = self.get_response()
        version = response[4:14].decode('gbk')
        return version

    def __hard_version(self):
        """
        功能：获取机器人的硬件版本。
        输入：空
        返回：
        version:机器人的硬件版本，格式为string
        """
        cmd = packageCommand([0], 'hard_version')
        self.clear_output()
        self.write(cmd)
        response = self.get_response()
        cmd_len = response[2]
        version = response[4:cmd_len - 1].decode('gbk')
        return version

    @lock
    def power_info(self):
        """
        功能：获取机器人的电量信息。
        输入：空
        返回：空
        """
        cmd = packageCommand([0], 'power_info')
        self.clear_output()
        self.write(cmd)
        response = self.get_response()
        voltage, charging, power = parsing_power_info(response)
        if charging == 0:
            charge_info = '当前未充电！'
        elif charging == 1:
            charge_info = '正在充电中....'
        elif charging == 3:
            charge_info = '机器人没有电池，当前电源供电！'
        else:
            charge_info = '获取电量信息失败！'
        print('电压：{}v\n电量：{}%\n{}'.format(voltage, power, charge_info))

    @lock
    def single_control(self, cmd):
        """
        功能：控制机器人的单个舵机运动。
        输入：
        cmd：单个舵机运动的命令参数，包括：舵机ID，舵机角度，运行时间，和允许下帧数据时间。
        注意：舵机ID从1开始计算
        返回：空
        """
        response = ''
        cmd = get_single_control_cmd(cmd)
        self.clear_output()
        self.write(cmd)
        while response == '':
            response = self.get_response()

        flag = parsing_single_control(response)
        if flag is False:
            print('命令执行失败，请重试！')
            return 0

    @lock
    def multi_control(self, cmd):
        """
        功能：控制机器人的所有舵机运动。
        输入：
        cmd：多舵机运动的命令参数，包括：所有舵机的角度值，运行时间，和允许下帧数据时间。
        注意：舵机ID从1开始计算
        返回：空
        """
        response = ''
        cmd = get_multi_control_cmd(cmd)
        self.clear_output()
        self.write(cmd)
        while response == '':
            response = self.get_response()

        flag = parsing_multi_control(response)
        if flag is False:
            print('命令执行失败，请重试！')
            return 0
        return flag

    @lock
    def read_back_single(self, joint_id):
        """
        功能：回读单个舵机的角度。
        输入：
        joint_id：舵机ID。
        返回：舵机当前的角度。
        """
        if joint_id not in range(1, 17):
            print('舵机ID错误，舵机ID从1开始计数，必须为1~16中的一个。当前输入ID为：%d' % joint_id)
            return
        cmd = packageCommand([joint_id], 'read_back_single')
        self.clear_output()
        self.write(cmd)
        response = self.get_response()
        angle = parsing_rb_single(response)
        return angle

    @lock
    def read_back_all(self):
        """
        功能：回读所有舵机的角度。
        输入：空
        返回：所有舵机的当前角度。
        """
        cmd = packageCommand([0], 'read_back_all')
        self.clear_output()
        self.write(cmd)
        response = self.get_response()
        angles = parsing_rb_all(response)
        return angles

    @lock
    def set_single_offset(self, geer_id, value):
        """
        功能：设置单个舵机偏移值的命令。
        输入：
        geer_id:舵机ID， 数据格式：int
        注意：舵机ID从1开始计算
        value:舵机的偏移值， 数据格式：int
        返回：空
        """
        response = ''
        cmd = get_set_single_offset_cmd(geer_id, value)
        self.clear_output()
        self.write(cmd)
        while response == '':
            response = self.get_response()

        flag = parsing_set_single_offsset(response)
        if flag is False:
            print('命令执行失败，请重试！')
            return 0

    @lock
    def set_all_offset(self, offset_values):
        """
        功能：设置所有舵机偏移值的命令。
        输入：
        offset_values:所有舵机的偏移值，数据格式：list
        返回：空
        """
        response = ''
        cmd = get_set_all_offset_cmd(offset_values)
        self.clear_output()
        self.write(cmd)
        while response == '':
            response = self.get_response()

        flag = parsing_set_all_offsset(response)
        if flag is False:
            print('命令执行失败，请重试！')
            return 0

    @lock
    def read_single_geer_offset(self, geer_id, tips=False):
        """
        功能：读取单个舵机的偏移值
        输入：
        geer_id:舵机ID
        返回：
        value:舵机的偏移值。
        """
        cmd = packageCommand([geer_id], 'read_single_offset')
        self.clear_output()
        self.write(cmd)
        response = self.get_response()
        geer_id, value = parsing_read_single_offsset(response)
        if tips:
            print('%d号舵机的版本号为：%s' % (geer_id, value))
        return value

    @lock
    def read_all_geer_offset(self, tips=False):
        """
        功能：读取所有舵机的偏移值
        输入：空
        返回：
        geer_nums:舵机数量
        versions:所有舵机的偏移值
        """
        cmd = packageCommand([0], 'read_all_offset')
        self.clear_output()
        self.write(cmd)
        response = self.get_response()
        geer_nums, values = parsing_read_all_offsset(response)
        if tips:
            print('===========机器人共有%d个舵机，各舵机的偏移值如下：===========' % geer_nums)
            for i in range(geer_nums // 2):
                print('{}号舵机：{}                  {}号舵机：{}'.format(str(i * 2 + 1).rjust2'0', values[(i * 2)], str(i * 2 + 2).rjust2'0', values[(i * 2 + 1)]))

        return (
         geer_nums, values)

    @lock
    def single_geer_version(self, geer_id, tips=False):
        """
        功能：读取单个舵机的版本号
        输入：
        geer_id:舵机ID
        返回：
        version:舵机的版本号。
        """
        cmd = packageCommand([geer_id], 'single_geer_version')
        self.clear_output()
        self.write(cmd)
        response = self.get_response()
        geer_id, version = parsing_single_geer_version(response)
        if tips:
            print('%d号舵机的版本号为：%s' % (geer_id, version))
        return version

    @lock
    def all_geer_version(self, tips=False):
        """
        功能：读取所有舵机的版本号
        输入：空
        返回：
        geer_nums:舵机数量
        versions:所有舵机的版本号
        """
        cmd = packageCommand([0], 'all_geer_version')
        self.clear_output()
        self.write(cmd)
        response = self.get_response()
        geer_nums, versions = parsing_all_geer_version(response)
        if tips:
            print('===========机器人共有%d个舵机，各舵机的版本号如下：===========' % geer_nums)
            for i in range(geer_nums // 2):
                print('%s号舵机：%s                  %s号舵机：%s' % (
                 str(i * 2 + 1).rjust2'0', versions[(i * 2)], str(i * 2 + 2).rjust2'0', versions[(i * 2 + 1)]))

        return (
         geer_nums, versions)

    @lock
    def play_and_charge(self, switch, tips=True):
        """
        功能：控制机器人是否允许边玩边充。
        输入：
        switch:根据switch内容控制机器人边玩边充开关。switch数据类型为int，取值范围0或1，0表示不允许，1表示允许。
        返回：空。
        """
        cmd = packageCommand([switch], 'play_and_charge')
        self.write(cmd)
        self.clear_output(timeout=1000)
        if tips:
            p_s = '已开启' if switch else '已关闭'
            print('边玩边充功能%s！' % p_s)

    @lock
    def get_sn(self, tips=True):
        """
        功能：获取机器人的sn号。
        输入：空
        返回：空
        """
        cmd = packageCommand([0], 'get_sn')
        self.write(cmd)
        response = self.get_response()
        self.SN = parsing_sn(response)
        if tips:
            print('机器人的SN号为：%s' % self.SN)

    @lock
    def get_udid(self, tips=True):
        """
        功能：获取机器人的udid号。
        输入：空
        返回：空
        """
        cmd = packageCommand([0], 'get_udid')
        self.write(cmd)
        response = self.get_response()
        self.UDID = parsing_udid(response)
        if tips:
            print('机器人的UDID号为：%s' % self.UDID)