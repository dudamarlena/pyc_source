# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/dslackw/Downloads/alarm-3.0/alarm/main.py
# Compiled at: 2019-12-11 17:39:32
# Size of source mod 2**32: 11052 bytes
import os, sys, time, datetime, calendar
__all__ = 'alarm'
__author__ = 'dslackw'
__version_info__ = (3, 0)
__version__ = ('{0}.{1}'.format)(*__version_info__)
__license__ = 'GNU General Public License v3 (GPLv3)'
__email__ = 'd.zlatanidis@gmail.com'
_found_mplayer = None
for dr in os.environ['PATH'].split(os.pathsep):
    if os.path.exists(os.path.join(dr, 'mplayer')):
        _found_mplayer = dr

if not _found_mplayer:
    print('Error: Mplayer required !')
    sys.exit()
configuration = [
 '# configuration file for alarm\n\n',
 '[Day]\n',
 "# Choose 'today' if you do not want to regulate daily day.\n",
 'DAY=today\n\n',
 '[Alarm Time]\n',
 '# Constant alarm time.\n',
 'ALARM_TIME=HH:MM\n\n',
 '[Alarm Attempts]\n',
 '# Select number for attempts.\n',
 'ATTEMPTS=5\n\n',
 '[Path]\n',
 '# Path statements sound files.\n',
 'SONG=/path/to/song.mp3']
HOME = os.getenv('HOME') + '/'
alarm_config_dir = '.alarm'
config_file = 'config'
alarm_config = '%s%s/%s' % (HOME, alarm_config_dir, config_file)
if not os.path.exists(HOME + alarm_config_dir):
    os.mkdir(HOME + alarm_config_dir)
if not os.path.isfile(alarm_config):
    with open(alarm_config, 'w') as (conf):
        for line in configuration:
            conf.write(line)

        conf.close()

def config():
    """
        Reading the config file in $HOME directory
        /home/user/.alarm/config
    """
    alarm_day = alarm_time = alarm_attempts = song = []
    for line in open(alarm_config, 'r'):
        line = line.lstrip()
        if line.startswith('DAY'):
            alarm_day = line[4:].split()
        if line.startswith('ALARM_TIME'):
            alarm_time = line[11:].split()
        if line.startswith('ATTEMPTS'):
            alarm_attempts = line[9:].split()
        if line.startswith('SONG'):
            song = line[5:].split()

    if alarm_day == ['today']:
        alarm_day = time.strftime('%d').split()
    alarm_args = alarm_day + alarm_time + alarm_attempts + song
    if alarm_args:
        if len(alarm_args) == 4:
            return alarm_args
        print('Error: config file: missing argument')
        sys.exit()
    else:
        print('Error: config file: missing argument')
        sys.exit()


class MplayerNotInstalledException(Exception):

    def __init__(self):
        print('Error: Mplayer required for playing alarm sounds\n')


class ALARM(object):
    """ALARM"""

    def __init__(self, alarm_day, alarm_time, alarm_attempts, song):
        self.wakeup = [
         '__        __    _          _   _         _ ',
         '\\ \\      / /_ _| | _____  | | | |_ __   | |',
         " \\ \\ /\\ / / _` | |/ / _ \\ | | | | '_ \\  | |",
         '  \\ V  V / (_| |   <  __/ | |_| | |_) | |_|',
         '   \\_/\\_/ \\__,_|_|\\_\\___|  \\___/| .__/  (_)',
         '                                |_|\n']
        self.RUN_ALARM = True
        self.alarm_day = alarm_day
        self.alarm_time = alarm_time.replace(':', ' ').split()
        self.alarm_pattern = ['HH', 'MM']
        self.alarm_attempts = alarm_attempts
        self.song = song
        self.mplayer_options = '-really-quiet'
        try:
            self.alarm_hour = self.alarm_time[0]
            self.alarm_minutes = self.alarm_time[1]
        except IndexError:
            print("error: time: usage 'HH:MM'")
            self.alarm_hour = '00'
            self.alarm_minutes = '00'
            self.alarm_time = [self.alarm_hour, self.alarm_minutes]
            self.RUN_ALARM = False

    def errors--- This code section failed: ---

 L. 150       0_2  SETUP_EXCEPT        326  'to 326'

 L. 151         4  LOAD_GLOBAL              datetime
                6  LOAD_ATTR                datetime
                8  LOAD_METHOD              now
               10  CALL_METHOD_0         0  ''
               12  LOAD_FAST                'self'
               14  STORE_ATTR               now

 L. 152        16  LOAD_GLOBAL              len
               18  LOAD_FAST                'self'
               20  LOAD_ATTR                alarm_day
               22  CALL_FUNCTION_1       1  ''
               24  LOAD_CONST               2
               26  COMPARE_OP               <
               28  POP_JUMP_IF_TRUE     44  'to 44'
               30  LOAD_GLOBAL              len
               32  LOAD_FAST                'self'
               34  LOAD_ATTR                alarm_day
               36  CALL_FUNCTION_1       1  ''
               38  LOAD_CONST               2
               40  COMPARE_OP               >
               42  POP_JUMP_IF_FALSE    70  'to 70'
             44_0  COME_FROM            28  '28'

 L. 153        44  LOAD_GLOBAL              print
               46  LOAD_STR                 "error: day: usage 'DD' such us '0%s' not '%s'"

 L. 154        48  LOAD_FAST                'self'
               50  LOAD_ATTR                alarm_day
               52  LOAD_FAST                'self'
               54  LOAD_ATTR                alarm_day
               56  BUILD_TUPLE_2         2 
               58  BINARY_MODULO    
               60  CALL_FUNCTION_1       1  ''
               62  POP_TOP          

 L. 155        64  LOAD_CONST               False
               66  LOAD_FAST                'self'
               68  STORE_ATTR               RUN_ALARM
             70_0  COME_FROM            42  '42'

 L. 156        70  LOAD_GLOBAL              int
               72  LOAD_FAST                'self'
               74  LOAD_ATTR                alarm_day
               76  CALL_FUNCTION_1       1  ''
               78  LOAD_GLOBAL              calendar
               80  LOAD_METHOD              monthrange

 L. 157        82  LOAD_FAST                'self'
               84  LOAD_ATTR                now
               86  LOAD_ATTR                year
               88  LOAD_FAST                'self'
               90  LOAD_ATTR                now
               92  LOAD_ATTR                month
               94  CALL_METHOD_2         2  ''
               96  LOAD_CONST               1
               98  BINARY_SUBSCR    
              100  COMPARE_OP               >
              102  POP_JUMP_IF_TRUE    118  'to 118'
              104  LOAD_GLOBAL              int

 L. 158       106  LOAD_FAST                'self'
              108  LOAD_ATTR                alarm_day
              110  CALL_FUNCTION_1       1  ''
              112  LOAD_CONST               1
              114  COMPARE_OP               <
              116  POP_JUMP_IF_FALSE   132  'to 132'
            118_0  COME_FROM           102  '102'

 L. 159       118  LOAD_GLOBAL              print
              120  LOAD_STR                 'error: day: out of range'
              122  CALL_FUNCTION_1       1  ''
              124  POP_TOP          

 L. 160       126  LOAD_CONST               False
              128  LOAD_FAST                'self'
              130  STORE_ATTR               RUN_ALARM
            132_0  COME_FROM           116  '116'

 L. 162       132  LOAD_GLOBAL              len
              134  LOAD_FAST                'self'
              136  LOAD_ATTR                alarm_time
              138  CALL_FUNCTION_1       1  ''
              140  LOAD_GLOBAL              len
              142  LOAD_FAST                'self'
              144  LOAD_ATTR                alarm_pattern
              146  CALL_FUNCTION_1       1  ''
              148  COMPARE_OP               !=
              150  POP_JUMP_IF_TRUE    224  'to 224'

 L. 163       152  LOAD_GLOBAL              len
              154  LOAD_FAST                'self'
              156  LOAD_ATTR                alarm_time
              158  LOAD_CONST               0
              160  BINARY_SUBSCR    
              162  CALL_FUNCTION_1       1  ''
              164  LOAD_CONST               2
              166  COMPARE_OP               <
              168  POP_JUMP_IF_TRUE    224  'to 224'

 L. 164       170  LOAD_GLOBAL              len
              172  LOAD_FAST                'self'
              174  LOAD_ATTR                alarm_time
              176  LOAD_CONST               0
              178  BINARY_SUBSCR    
              180  CALL_FUNCTION_1       1  ''
              182  LOAD_CONST               2
              184  COMPARE_OP               >
              186  POP_JUMP_IF_TRUE    224  'to 224'

 L. 165       188  LOAD_GLOBAL              len
              190  LOAD_FAST                'self'
              192  LOAD_ATTR                alarm_time
              194  LOAD_CONST               1
              196  BINARY_SUBSCR    
              198  CALL_FUNCTION_1       1  ''
              200  LOAD_CONST               2
              202  COMPARE_OP               <
              204  POP_JUMP_IF_TRUE    224  'to 224'
              206  LOAD_GLOBAL              len
              208  LOAD_FAST                'self'
              210  LOAD_ATTR                alarm_time
              212  LOAD_CONST               1
              214  BINARY_SUBSCR    
              216  CALL_FUNCTION_1       1  ''
              218  LOAD_CONST               2
              220  COMPARE_OP               >
              222  POP_JUMP_IF_FALSE   250  'to 250'
            224_0  COME_FROM           204  '204'
            224_1  COME_FROM           186  '186'
            224_2  COME_FROM           168  '168'
            224_3  COME_FROM           150  '150'

 L. 166       224  LOAD_GLOBAL              print
              226  LOAD_STR                 "error: time: usage '%s'"
              228  LOAD_STR                 ':'
              230  LOAD_METHOD              join
              232  LOAD_FAST                'self'
              234  LOAD_ATTR                alarm_pattern
              236  CALL_METHOD_1         1  ''
              238  BINARY_MODULO    
              240  CALL_FUNCTION_1       1  ''
              242  POP_TOP          

 L. 167       244  LOAD_CONST               False
              246  LOAD_FAST                'self'
              248  STORE_ATTR               RUN_ALARM
            250_0  COME_FROM           222  '222'

 L. 170       250  LOAD_GLOBAL              int
              252  LOAD_FAST                'self'
              254  LOAD_ATTR                alarm_hour
              256  CALL_FUNCTION_1       1  ''
              258  LOAD_GLOBAL              range
              260  LOAD_CONST               0
              262  LOAD_CONST               24
              264  CALL_FUNCTION_2       2  ''
              266  COMPARE_OP               not-in
          268_270  POP_JUMP_IF_FALSE   286  'to 286'

 L. 171       272  LOAD_GLOBAL              print
              274  LOAD_STR                 'error: hour: out of range'
              276  CALL_FUNCTION_1       1  ''
              278  POP_TOP          

 L. 172       280  LOAD_CONST               False
              282  LOAD_FAST                'self'
              284  STORE_ATTR               RUN_ALARM
            286_0  COME_FROM           268  '268'

 L. 173       286  LOAD_GLOBAL              int
              288  LOAD_FAST                'self'
              290  LOAD_ATTR                alarm_minutes
              292  CALL_FUNCTION_1       1  ''
              294  LOAD_GLOBAL              range
              296  LOAD_CONST               0
              298  LOAD_CONST               60
              300  CALL_FUNCTION_2       2  ''
              302  COMPARE_OP               not-in
          304_306  POP_JUMP_IF_FALSE   322  'to 322'

 L. 174       308  LOAD_GLOBAL              print
              310  LOAD_STR                 'error: minutes: out of range'
              312  CALL_FUNCTION_1       1  ''
              314  POP_TOP          

 L. 175       316  LOAD_CONST               False
              318  LOAD_FAST                'self'
              320  STORE_ATTR               RUN_ALARM
            322_0  COME_FROM           304  '304'
              322  POP_BLOCK        
              324  JUMP_FORWARD        374  'to 374'
            326_0  COME_FROM_EXCEPT      0  '0'

 L. 176       326  DUP_TOP          
              328  LOAD_GLOBAL              ValueError
              330  COMPARE_OP               exception-match
          332_334  POP_JUMP_IF_FALSE   372  'to 372'
              336  POP_TOP          
              338  POP_TOP          
              340  POP_TOP          

 L. 177       342  LOAD_GLOBAL              print
              344  LOAD_STR                 "Usage '%s'"
              346  LOAD_STR                 ':'
              348  LOAD_METHOD              join
              350  LOAD_FAST                'self'
              352  LOAD_ATTR                alarm_pattern
              354  CALL_METHOD_1         1  ''
              356  BINARY_MODULO    
              358  CALL_FUNCTION_1       1  ''
              360  POP_TOP          

 L. 178       362  LOAD_CONST               False
              364  LOAD_FAST                'self'
              366  STORE_ATTR               RUN_ALARM
              368  POP_EXCEPT       
              370  JUMP_FORWARD        374  'to 374'
            372_0  COME_FROM           332  '332'
              372  END_FINALLY      
            374_0  COME_FROM           370  '370'
            374_1  COME_FROM           324  '324'

 L. 179       374  LOAD_GLOBAL              os
              376  LOAD_ATTR                path
              378  LOAD_METHOD              isfile
              380  LOAD_FAST                'self'
              382  LOAD_ATTR                song
              384  CALL_METHOD_1         1  ''
          386_388  POP_JUMP_IF_TRUE    404  'to 404'

 L. 180       390  LOAD_GLOBAL              print
              392  LOAD_STR                 'error: song: file does not exist'
              394  CALL_FUNCTION_1       1  ''
              396  POP_TOP          

 L. 181       398  LOAD_CONST               False
              400  LOAD_FAST                'self'
              402  STORE_ATTR               RUN_ALARM
            404_0  COME_FROM           386  '386'

Parse error at or near `COME_FROM' instruction at offset 250_0

    def start(self):
        """
        All the work going on here. To the Authority the right day and time
        format and finding the correct path of the file. The Application
        requires Mplayer to play the alarm sound. Please read which sounds
        are supported in page:
        http://web.njit.edu/all_topics/Prog_Lang_Docs/html/mplayer/formats.html
        """
        self.errors()
        try:
            alarm_day_name = calendar.day_name[calendar.weekday(self.now.year, self.now.month, int(self.alarm_day))]
        except ValueError:
            pass

        self.alarm_time.insert(0, self.alarm_day)
        self.alarm_time = ':'.join(self.alarm_time)
        if self.RUN_ALARM:
            os.system('clear')
            print('+==============================================================================+')
            print('|                              CLI Alarm Clock                                 |')
            print('+==============================================================================+')
            print('| Alarm set at : %s %s' % (alarm_day_name, self.alarm_time[3:]) + ' ' * (62 - len(alarm_day_name + self.alarm_time[2:])) + '|')
            print('| Sound file : %s' % self.song + ' ' * (64 - len(self.song)) + '|')
            print('| Time :                                                                       |')
            print('+==============================================================================+')
            print("Press 'Ctrl + c' to cancel alarm ...")
            try:
                while self.RUN_ALARM:
                    start_time = time.strftime('%d:%H:%M:%S')
                    self.position(6, 10, self.color('green') + start_time[3:] + self.color('endc'))
                    time.sleep(1)
                    begin = start_time[:-3]
                    if begin == self.alarm_time:
                        self.position(6, 10, self.color('red') + start_time[3:-3] + self.color('endc') + ' Wake Up !')
                        for wake in self.wakeup:
                            print(wake)

                        print("\nPress 'SPACE' to pause alarm ...\n")
                        if not self.alarm_attempts:
                            self.alarm_attempts = 5
                        else:
                            self.alarm_attempts = int(self.alarm_attempts)
                        for att in range(0, self.alarm_attempts):
                            print('Attempt %d\n' % (att + 1))
                            play = os.system("mplayer %s '%s'" % (
                             self.mplayer_options, self.song))
                            if play != 0 and play != 256:
                                MplayerNotInstalledException()
                                break

                        self.RUN_ALARM = False

            except KeyboardInterrupt:
                print('\nAlarm canceled!')
                self.RUN_ALARM = False

    def position(self, x, y, text):
        """
            ANSI Escape sequences
            http://ascii-table.com/ansi-escape-sequences.php
        """
        print(('\x1b7\x1b[%d;%df%s\x1b8' % (x, y, text)), end='', flush=True)

    def color(self, color):
        """
            Print foreground colors
        """
        paint = {'red':'\x1b[31m', 
         'green':'\x1b[32m', 
         'endc':'\x1b[0m'}
        return paint[color]


class Args(object):

    def __init__(self):
        pass

    def view(self):
        """Usage: alarm [OPTIONS] <day> <alarm_time> <song>

Optional arguments
  -h, --help       show this help message and exit
  -v, --version    print version and exit
  -s, --set        set alarm day, time and sound

  --config         use config file

  Example: alarm -s 21 06:00 /path/to/song.mp3
  """
        print(self.view.__doc__)


def main():
    args = sys.argv
    args.pop(0)
    if len(args) == 0:
        print('try alarm --help')
    elif len(args) == 1:
        if args[0] == '-h' or :
            Args().view()
    elif len(args) == 1:
        if args[0] == '-v' or :
            print('Version : %s' % __version__)
    elif not (len(args) == 4 and args[0] == '-s'):
        if len(args) == 4:
            if args[0] == '--set':
                ALARM(alarm_day=(args[1]), alarm_time=(args[2]), alarm_attempts='', song=(args[3])).start()
        if len(args) == 1 and args[0] == '--config':
            alarm_set_args = config()
            ALARM(alarm_set_args[0], alarm_set_args[1], alarm_set_args[2], alarm_set_args[3]).start()
        else:
            print('try alarm --help')


if __name__ == '__main__':
    main()