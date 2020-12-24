# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/daviswx/getobs.py
# Compiled at: 2019-12-07 20:35:15
# Size of source mod 2**32: 3346 bytes
import argparse, os, re, shutil, subprocess, sys, time, tempfile
params = {'port':9100, 
 'host':'localhost'}
if 'DAVIS_HOSTNAME' in os.environ.keys():
    params['host'] = os.environ['DAVIS_HOSTNAME']
if 'DAVIS_PORT' in os.environ.keys():
    params['port'] = os.environ['DAVIS_PORT']

def validate_externals(path=None):
    tools = []
    tools.append(shutil.which('remserial'))
    tools.append(shutil.which('vproweather'))
    if None in tools:
        raise OSError('External tools not in PATH. Check.')


def append_externals_to_path():
    env = os.environ
    current_script = os.path.abspath(__file__)
    current_directory = os.path.dirname(current_script)
    external_dir = current_directory + '/../external'
    env['PATH'] = external_dir + ':' + env['PATH']
    return env


def establish_connection(params):
    tempname = next(tempfile._get_candidate_names())
    device_link = '/tmp/' + tempname
    connection = subprocess.Popen(['remserial', '-d', '-r', str(params['host']),
     '-p', str(params['port']), '-l', device_link, '/dev/ptmx'],
      stdout=(subprocess.PIPE),
      stderr=(subprocess.STDOUT))
    time.sleep(2)
    return (connection, device_link)


class realTimeOutput:
    __doc__ = '\n    rtBaroCurr\n    rtBaroTrend\n    rtBaroTrendImg\n    rtBattVoltage\n    rtDayET\n    rtDayRain\n    rtForeIcon\n    rtForeRule\n    rtForecast\n    rtInsideHum\n    rtInsideTemp\n    rtIsRaining\n    rtMonthET\n    rtMonthRain\n    rtOutsideHum\n    rtOutsideTemp\n    rtRainRate\n    rtRainStorm\n    rtSolarRad\n    rtStormStartDate\n    rtSunrise\n    rtSunset\n    rtUVLevel\n    rtWindAvgSpeed\n    rtWindDir\n    rtWindDirRose\n    rtWindSpeed\n    rtXmitBattt\n    rtYearRain\n    '

    def __init__(self, stdout):
        stdout = stdout.decode('utf-8')
        stdout = stdout.split('\n')
        stdout = [x for x in stdout if x != '']
        result = {}
        regex = re.compile('^[0-9][0-9]-[A-Z]')
        for x in stdout:
            k, v = x.split(' = ')
            if 'n/a' in v:
                v = None
            else:
                if 'AM' in v or 'PM' in v:
                    v = str(v)
                else:
                    if re.match(regex, v):
                        v = str(v)
                    else:
                        if v == 'no':
                            v = False
                        else:
                            if v == 'yes':
                                v = True
                            else:
                                if v[0].isdigit():
                                    v = float(v)
            result[k] = v

        self.__dict__ = result


def call_vproweather(device, opt='-x'):
    cmd = 'vproweather -x ' + device
    proc = subprocess.Popen((cmd.split(' ')), stdout=(subprocess.PIPE), stderr=(subprocess.STDOUT))
    stdout, stderr = proc.communicate()
    proc.terminate()
    time.sleep(1)
    return (stdout, proc.returncode)


def current():
    env = append_externals_to_path()
    validate_externals(path=(env['PATH']))
    connection, device = establish_connection(params)
    stdout, rc = call_vproweather(device)
    connection.terminate()
    return realTimeOutput(stdout)


if __name__ == '__main__':
    C = current()
    print('Current Temperature: ' + str(C.rtOutsideTemp))
    exit(0)