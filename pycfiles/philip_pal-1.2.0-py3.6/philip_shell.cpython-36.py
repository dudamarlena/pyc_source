# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/philip_pal/philip_shell.py
# Compiled at: 2020-03-26 05:07:50
# Size of source mod 2**32: 19812 bytes
"""
This script handles interfacing to the PHiLIP device.  It parses data and
exposes from the PhilipExtIf class to be run in a shell.

The purpose of this script is allow easy setup and manual usage of PHiLIP.

Usage
-----

```
usage: philip_shell.py  [-h]
                        [--loglevel {debug,info,warning,error,fatal,critical}]
                        [--port PORT]
                        [--filter-data]

optional arguments:
  -h, --help            show this help message and exit
  --loglevel {debug,info,warning,error,fatal,critical}
                        Python logger log level (default: warning)
  --port, -p
                        Specify the serial port
  --data_only, -do
                        Filters data from philip responses to only display
                        what is needed (default: False)
```
"""
import os, glob, cmd
from json import dumps
import logging, argparse
try:
    import readline
except ImportError:
    readline = None

from tabulate import tabulate
import statistics as sta, serial.tools.list_ports
try:
    from .philip_if import PhilipExtIf
except ImportError:
    from philip_pal.philip_if import PhilipExtIf

_HISTFILE = os.path.join(os.path.expanduser('~'), '.philip_history')

class PhilipShell(cmd.Cmd):
    __doc__ = 'Command loop for the PHiLIP interface\n\n    Args:\n        port - Serial port for the PHiLIP, if None connection wizard tries to\n               connent\n    '
    prompt = 'PHiLIP: '

    def __init__(self, port=None, use_dev_map=False):
        if port is None:
            self.phil = self._connect_wizard(use_dev_map=use_dev_map)
        else:
            if port == 'ignore':
                cmd.Cmd.__init__(self)
                return
            self.phil = PhilipExtIf(port, use_dev_map=use_dev_map)
        print('Interface Version: {}'.format(self.phil.if_version))
        self.data_only = True
        cmd.Cmd.__init__(self)

    @staticmethod
    def _connect_wizard(use_dev_map=False):
        print('Starting PHiLIP shell')
        serial_devices = sorted(serial.tools.list_ports.comports())
        if len(serial_devices) == 0:
            raise ConnectionError('Could not find any available devices')
        else:
            if len(serial_devices) == 1:
                print('Connected to {}'.format(serial_devices[0]))
                return PhilipExtIf(port=(serial_devices[0][0]), use_dev_map=use_dev_map)
            else:
                print('Select a serial port:')
                for i, s_dev in enumerate(serial_devices):
                    print('{}: {}'.format(i, s_dev))

                s_num = input('Selection(number): ')
                return PhilipExtIf(port=(serial_devices[int(s_num)][0]), use_dev_map=use_dev_map)

    def preloop(self):
        if readline:
            try:
                readline.read_history_file(_HISTFILE)
            except IOError:
                pass

    def do_read_reg(self, arg):
        """Read a register defined by the memory map

        Usage:
            read_reg <cmd_name> [offset] [size] [to_byte_array] [timeout]

        Args:
            cmd_name: The name of the register to read
            offset: The number of elements to offset in an array
            size: The number of elements to read in an array
            to_byte_array: If True and data is bytes leave it as an array
            timeout: Optional timeout value for command specific timeouts

        """
        self._print_func_result(self.phil.read_reg, arg)

    def complete_read_reg(self, text, line, begidx, endidx):
        """Completes arg with memory map record names"""
        begidx = begidx
        endidx = endidx
        return self._complete_map(text, line)

    def do_write_reg(self, arg):
        """Writes a register defined by the memory map

        If writing to change a periph configuration the .mode.init bit should
        be set to 0 for reinitialization to occur.

        Usage:
            write_reg <cmd_name> <data> [offset] [timeout]

        Args:
            cmd_name: The name of the register to write
            data: The data to write to the register
            offset: The number of elements to offset in an array
            timeout: Optional timeout value for command specific timeouts

        Example:
            To write to user register 0 the data 42 we can do this
            write_reg user_reg 42 0

            To write many bytes the data must not be separated by spaces
            write_reg user_reg [1,2,3,4,5,6] 0
        """
        self._print_func_result(self.phil.write_reg, arg)

    def complete_write_reg(self, text, line, begidx, endidx):
        """Completes arg with memory map record names"""
        begidx = begidx
        endidx = endidx
        return self._complete_map(text, line)

    def do_read_struct(self, arg):
        """Reads a set of registers defined by the memory map

        Usage:
            read_struct <cmd_name> [timeout]

        Args:
            cmd_name: The name if the structure to read
            timeout: Optional timeout value for command specific timeouts
        """
        self._print_func_result(self.phil.read_struct, arg)

    def complete_read_struct(self, text, line, begidx, endidx):
        """Completes arg with memory map record structs"""
        begidx = begidx
        endidx = endidx
        mline = line.partition(' ')[2]
        offs = len(mline) - len(text)
        map_records = [*self.phil.mem_map]
        map_structs = []
        for record in map_records:
            first_name = record.split('.')[0]
            if first_name not in map_structs:
                map_structs.append(first_name)

        return [s[offs:] for s in map_structs if s.startswith(mline)]

    def do_execute_changes(self, arg):
        """Executes or commits device configuration changes

        This will cause any changes in configuration to be applied. For many
        periphs the .mode.init must be set to 0 for the periph to reinitialize.

        Usage:
            execute_changes [timeout]

        Args:
            timeout: Optional timeout value for command specific timeouts
        """
        self._print_func_result(self.phil.execute_changes, arg)

    def do_philip_reset(self, arg):
        """Resets the device

        Usage:
            philip_reset [timeout]

        Args:
            timeout: Optional timeout value for command specific timeouts
        """
        self._print_func_result(self.phil.reset_mcu, arg)

    def do_get_version(self, arg):
        """Get the version of the interface/memory map that is being used

        Usage:
            get_version
        """
        arg = arg
        print(self.phil.if_version)

    def do_write_and_execute(self, arg):
        """Writes the register and the init for the struct and executes changes

        Usage:
            write_and_execute <cmd_name> <data> [timeout]

        Args:
            cmd_name: The name of the register to write
            data: The data to write to the register
            timeout: Optional timeout value for command specific timeouts
        """
        self._print_func_result(self.phil.write_and_execute, arg)

    def complete_write_and_execute(self, text, line, begidx, endidx):
        """Completes arg with memory map record names"""
        begidx = begidx
        endidx = endidx
        return self._complete_map(text, line)

    def do_dut_reset(self, arg):
        """Provides a reset to the dut

        Toggles the dut reset pin for the reset time.

        Usage:
            dut_reset [reset_time] [timeout]

        Args:
            reset_time: Optional duration the dut is put in reset
            timeout: Optional timeout value for command specific timeouts
        """
        self._print_func_result(self.phil.dut_reset, arg)

    def do_read_trace(self, arg):
        """Reads event trace from the dut

        Usage:
            read_trace
        """
        try:
            results = self.phil.read_trace()
        except KeyError as exc:
            print('Could not parse argument {}'.format(exc))
        except (TypeError, ValueError, SyntaxError) as exc:
            print(exc)
        else:
            if len(results) == 0:
                return
            headers = [
             'time', 'diff', 'source_diff', 'source', 'event']
            table_data = []
            diffs = []
            for event in results['data']:
                row_data = []
                for key_name in headers:
                    if key_name == 'diff':
                        diffs.append(event[key_name])
                    row_data.append(event[key_name])

                table_data.append(row_data)

            print(tabulate(table_data, headers=headers, floatfmt='.9f'))
            try:
                if len(diffs) > 1:
                    diffs = diffs[1:]
                    print('\nDifference Stats')
                    print('     min: {:.9f}'.format(min(diffs)))
                    print('     max: {:.9f}'.format(max(diffs)))
                    print('    mean: {:.9f}'.format(sta.mean(diffs)))
                    print('  median: {:.9f}'.format(sta.median(diffs)))
                    print('   stdev: {:.9f}'.format(sta.stdev(diffs)))
                    print('variance: {:.9f}'.format(sta.variance(diffs)))
            except ValueError:
                pass

    def do_data_filter(self, arg):
        """Select or toggle filtering for data

        Usage:
            data_filter [{ON, OFF}]

        Args:
            {ON, OFF}: Turn filtering on or off, if no arg it toggles
        """
        if arg:
            if arg.upper() == 'ON':
                self.data_only = True
                print('Filtering for data')
            else:
                if arg.upper() == 'OFF':
                    self.data_only = False
                    print('Raw data, no filtering')
                else:
                    print('Incorrect arg')
        else:
            if self.data_only:
                self.data_only = False
                print('Raw data, no filtering')
            else:
                self.data_only = True
                print('Filtering for data')

    def do_print_map(self, arg):
        """Prints the device map

        Usage:
            print_map [cmd_name]

        Args:
            cmd_name: The name of the register in the map to print
        """
        arg = arg
        if arg:
            try:
                print(dumps((self.phil.mem_map[arg]), sort_keys=True, indent=4))
            except KeyError as exc:
                print('Cannot parse {}'.format(exc))

        else:
            print(dumps((self.phil.mem_map), sort_keys=True, indent=4))

    def complete_print_map(self, text, line, begidx, endidx):
        """Completes arg with memory map record names"""
        begidx = begidx
        endidx = endidx
        return self._complete_map(text, line)

    def _complete_map(self, text, line):
        mline = line.partition(' ')[2]
        offs = len(mline) - len(text)
        map_records = filter(lambda x: not x.endswith('.res'), [
         *self.phil.mem_map])
        return [s[offs:] for s in map_records if s.startswith(mline)]

    def do_info_record_type(self, arg):
        """Prints the device map

        Usage:
            info_record_type <record_type>

        Args:
            record_type: The record type in a map, such as description
        """
        try:
            record_types = {}
            for key, val in self.phil.mem_map.items():
                if arg in val and val[arg]:
                    record_types[key] = val[arg]

            print(dumps(record_types, sort_keys=True, indent=4))
        except KeyError as exc:
            print('Cannot parse {}'.format(exc))

    def complete_info_record_type(self, text, line, begidx, endidx):
        """Completes arg with common record types"""
        begidx = begidx
        endidx = endidx
        mline = line.partition(' ')[2]
        offs = len(mline) - len(text)
        info_record_types = ['description', 'access', 'default', 'bit',
         'flag', 'max', 'min']
        return [s[offs:] for s in info_record_types if s.startswith(mline)]

    def do_show_pinout(self, arg):
        """Prints the pinout for the connected board

        Usage:
            show_pinout
        """
        try:
            if arg:
                showboard = int(arg)
            else:
                showboard = self.phil.read_reg('sys.status.board')['data']
            if showboard == 1:
                print('\nPHILIP-B -> BLUEPILL\n\n                    ____\n                 ___|__|___\n DUT_RST = B12 - |        | - GND\n DUT_CTS = B13 - |        | - GND\n DUT_RTS = B14 - |        | - 3V3\nUSER_BTN = B15 - |        | - NRST\n   DUT_IC = A8 - |        | - B11 = DUT_RX\n    IF_TX = A9 - |        | - B10 = DUT_TX\n   IF_RX = A10 - |        | - B1 = PM_V_ADC\n  USB_DM = A11 - |        | - B0 = PM_HI_ADC\n  USB_DP = A12 - |        | - A7 = PM_LO_ADC\n DUT_NSS = A15 - |        | - A6 = DUT_ADC\n  DUT_SCK = B3 - |        | - A5 = TEST_FAIL\n DUT_MISO = B4 - |        | - A4 = TEST_WARN\n DUT_MOSI = B5 - |        | - A3 = TEST_PASS\n  DUT_SCL = B6 - |        | - A2 = DEBUG2\n  DUT_SDA = B7 - |        | - A1 = DEBUG1\n  DUT_PWM = B8 - |        | - A0 = DEBUG0\n  DUT_DAC = B9 - |        | - C15\n            5V - |        | - C14\n           GND - |        | - C13 = LED0\n           3V3 - |        | - VBAT\n                 __________\n                    ||||\n')
            else:
                print('\nPHILIP-N -> NUCLEO-F103RB\nCN6\n\n                            DUT_SCL = PB8 = SCL/D15 -\n                            DUT_SDA = PB9 = SDA/D14 -\n                                               AVDD -\n                                                GND -\n-                              LED0 = PA5 = SCK/D13 -\n- IOREF                                    MISO/D12 -\n- NRST                                 PWM/MOSI/D11 -\n- 3V3                                    PWM/CS/D10 -\n- 5V                                         PWM/D9 -\n- GND                             DUT_TX = PA9 = D8 -\n- GND                                           |CN5|\n- VIN                             DUT_IC = PA8 = D7 -\n|CN6|                                        PWM/D6 -\n- A0 = PA0 = TEST_WARN        DEBUG1 = PB4 = PWM/D5 -\n- A1 = PA1 = TEST_FAIL            DEBUG2 = PB5 = D4 -\n- A2 = PA4 = TEST_PASS        DEBUG0 = PB3 = PWM/D3 -\n- A3 = PB0 = DUT_ADC             DUT_RX = PA10 = D2 -\n- A4 = PC1 = PM_HI_ADC          IF_TX = PA2 = TX/D1 -\n- A5 = PC0 = PM_V_ADC           IF_RX = PA3 = RX/D0 -\n|CN8|                                          |CN9|\n\n          -1 -                  DUT_DAC -1 - DUT_PWM\n          -2 - DEBUG2           DUT_SCL -2 -\n          -3 -                  DUT_SDA -3 -\n          -4 -                          -4 -\n          -5 -                          -5 -\n          -6 -                     LED0 -6 - DUT_RTS\n          -7 -                          -7 - DUT_CTS\n          -8 -                          -8 - DUT_NSS\n          -9 -                          -9 -\n          -10-                          -10-\n          -11-                   DUT_TX -11- DUT_RST\n USER_BTN -12-                   DUT_IC -12-\n          -13-                          -13- DUT_MOSI\n          -14- TEST_WARN         DEBUG1 -14- DUT_MISO\n          -15- TEST_FAIL                -15- DUT_SCK\n          -16- TEST_PASS         DEBUG0 -16-\n          -17- DUT_ADC           DUT_RX -17-\nPM_LO_ADC -18- PM_HI_ADC          IF_TX -18-\n          -19- PM_V_ADC           IF_RX -19-\n          |CN7|                         |CN10|\n')
        except ValueError as exc:
            print(exc)

    def do_run_script(self, arg):
        """Runs a number of commands from a file.
        Example:
            example.txt
            write_and_execute i2c.slave_addr_1 99
            read_reg i2c.slave_addr_1
            (in the shell)
            PHiLIP: run_script example.txt
        Usage:
            run_script <filename>
        Args:
            filename: This is the name of the file that contains the commands
        """
        try:
            with open(os.path.join(os.getcwd(), arg), 'r') as (fin):
                script = fin.readlines()
                for line in script:
                    self.onecmd(line)

        except FileNotFoundError as exc:
            print(exc)

    def complete_run_script(self, text, line, start_idx, end_idx):
        """Autocomplete file search"""
        text = text
        before_arg = line.rfind(' ', 0, start_idx)
        if before_arg == -1:
            return
        else:
            fixed = line[before_arg + 1:start_idx]
            arg = line[before_arg + 1:end_idx]
            pattern = arg + '*'
            completions = []
            for path in glob.glob(pattern):
                if path:
                    if os.path.isdir(path):
                        if path[(-1)] != os.sep:
                            path = path + os.sep
                else:
                    path = path
                completions.append(path.replace(fixed, '', 1))

            return completions

    def do_exit(self, arg):
        """I mean it should be obvious

        Usage:
            exit
        """
        arg = arg
        return True

    def _print_func_result_success--- This code section failed: ---

 L. 515         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'results'
                4  LOAD_GLOBAL              list
                6  CALL_FUNCTION_2       2  '2 positional arguments'
                8  POP_JUMP_IF_TRUE     16  'to 16'

 L. 516        10  LOAD_FAST                'results'
               12  BUILD_LIST_1          1 
               14  STORE_FAST               'results'
             16_0  COME_FROM             8  '8'

 L. 517        16  LOAD_FAST                'self'
               18  LOAD_ATTR                phil
               20  LOAD_ATTR                RESULT_SUCCESS
               22  STORE_FAST               'result'

 L. 518        24  LOAD_CONST               False
               26  STORE_FAST               'printed_something'

 L. 519        28  SETUP_LOOP          146  'to 146'
               30  LOAD_FAST                'results'
               32  GET_ITER         
               34  FOR_ITER            144  'to 144'
               36  STORE_FAST               'res'

 L. 520        38  LOAD_FAST                'self'
               40  LOAD_ATTR                data_only
               42  POP_JUMP_IF_FALSE   126  'to 126'

 L. 521        44  LOAD_STR                 'result'
               46  LOAD_FAST                'res'
               48  COMPARE_OP               in
               50  POP_JUMP_IF_FALSE   108  'to 108'

 L. 522        52  LOAD_FAST                'res'
               54  LOAD_STR                 'result'
               56  BINARY_SUBSCR    
               58  LOAD_FAST                'self'
               60  LOAD_ATTR                phil
               62  LOAD_ATTR                RESULT_SUCCESS
               64  COMPARE_OP               is
               66  POP_JUMP_IF_FALSE    98  'to 98'

 L. 523        68  LOAD_STR                 'data'
               70  LOAD_FAST                'res'
               72  COMPARE_OP               in
               74  POP_JUMP_IF_FALSE   106  'to 106'

 L. 524        76  LOAD_GLOBAL              print
               78  LOAD_GLOBAL              dumps
               80  LOAD_FAST                'res'
               82  LOAD_STR                 'data'
               84  BINARY_SUBSCR    
               86  CALL_FUNCTION_1       1  '1 positional argument'
               88  CALL_FUNCTION_1       1  '1 positional argument'
               90  POP_TOP          

 L. 525        92  LOAD_CONST               True
               94  STORE_FAST               'printed_something'
               96  JUMP_ABSOLUTE       124  'to 124'
               98  ELSE                     '106'

 L. 527        98  LOAD_FAST                'res'
              100  LOAD_STR                 'result'
              102  BINARY_SUBSCR    
              104  STORE_FAST               'result'
            106_0  COME_FROM            74  '74'
              106  JUMP_ABSOLUTE       142  'to 142'
              108  ELSE                     '124'

 L. 529       108  LOAD_GLOBAL              print
              110  LOAD_GLOBAL              dumps
              112  LOAD_FAST                'res'
              114  CALL_FUNCTION_1       1  '1 positional argument'
              116  CALL_FUNCTION_1       1  '1 positional argument'
              118  POP_TOP          

 L. 530       120  LOAD_CONST               True
              122  STORE_FAST               'printed_something'
              124  JUMP_BACK            34  'to 34'
              126  ELSE                     '142'

 L. 532       126  LOAD_GLOBAL              print
              128  LOAD_GLOBAL              dumps
              130  LOAD_FAST                'res'
              132  CALL_FUNCTION_1       1  '1 positional argument'
              134  CALL_FUNCTION_1       1  '1 positional argument'
              136  POP_TOP          

 L. 533       138  LOAD_CONST               True
              140  STORE_FAST               'printed_something'
              142  JUMP_BACK            34  'to 34'
              144  POP_BLOCK        
            146_0  COME_FROM_LOOP       28  '28'

 L. 534       146  LOAD_FAST                'printed_something'
              148  POP_JUMP_IF_TRUE    158  'to 158'

 L. 535       150  LOAD_GLOBAL              print
              152  LOAD_FAST                'result'
              154  CALL_FUNCTION_1       1  '1 positional argument'
              156  POP_TOP          
            158_0  COME_FROM           148  '148'

Parse error at or near `JUMP_ABSOLUTE' instruction at offset 106

    def _print_func_result(self, func, arg):
        value = (arg or '').split(' ')
        func_args = [v for v in value if v]
        try:
            results = func(*func_args)
        except KeyError as exc:
            print('Could not parse argument {}'.format(exc))
        except (TypeError, ValueError, SyntaxError) as exc:
            print(exc)
        else:
            self._print_func_result_success(results)


PARSER = argparse.ArgumentParser()
LOG_LEVELS = ('debug', 'info', 'warning', 'error', 'fatal', 'critical')
PARSER.add_argument('--loglevel', choices=LOG_LEVELS, default='info', help='Python logger log level')
PARSER.add_argument('--port', '-p', help='Specifies the serial port', default=None)
PARSER.add_argument('--use_dev_map', '-dm', default=False, action='store_true',
  help='Uses the memory map from device')

def _exit_cmd_loop():
    if readline:
        try:
            readline.write_history_file(_HISTFILE)
        except IOError:
            pass


def main():
    """Main program"""
    pargs = PARSER.parse_args()
    if pargs.loglevel:
        loglevel = logging.getLevelName(pargs.loglevel.upper())
        logging.basicConfig(level=loglevel)
    try:
        PhilipShell(port=(pargs.port), use_dev_map=(pargs.use_dev_map)).cmdloop()
        _exit_cmd_loop()
    except KeyboardInterrupt:
        _exit_cmd_loop()
        print('')


if __name__ == '__main__':
    main()