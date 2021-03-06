# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\sboon\AppData\Local\Temp\pip-install-ptdbtr91\quarchpy\quarchpy\fio\FIO_interface.py
# Compiled at: 2020-03-25 05:10:07
# Size of source mod 2**32: 12669 bytes
import os, time, json
from datetime import datetime
import subprocess
all_outputs = {'terse_version_3':'0', 
 'fio_version':'1', 
 'jobname':'2', 
 'groupid':'3', 
 'error':'4', 
 'read_kb':'5', 
 'read_bandwidth':'6', 
 'read_iops':'7', 
 'read_runtime_ms':'8', 
 'read_slat_min':'9', 
 'read_slat_max':'10', 
 'read_slat_mean':'11', 
 'read_slat_dev':'12', 
 'read_clat_min':'13', 
 'read_clat_max':'14', 
 'read_clat_mean':'15', 
 'read_clat_dev':'16', 
 'read_clat_pct01':'17', 
 'read_clat_pct02':'18', 
 'read_clat_pct03':'19', 
 'read_clat_pct04':'20', 
 'read_clat_pct05':'21', 
 'read_clat_pct06':'22', 
 'read_clat_pct07':'23', 
 'read_clat_pct08':'24', 
 'read_clat_pct09':'25', 
 'read_clat_pct10':'26', 
 'read_clat_pct11':'27', 
 'read_clat_pct12':'28', 
 'read_clat_pct13':'29', 
 'read_clat_pct14':'30', 
 'read_clat_pct15':'31', 
 'read_clat_pct16':'32', 
 'read_clat_pct17':'33', 
 'read_clat_pct18':'34', 
 'read_clat_pct19':'35', 
 'read_clat_pct20':'36', 
 'read_tlat_min':'37', 
 'read_lat_max':'38', 
 'read_lat_mean':'39', 
 'read_lat_dev':'40', 
 'read_bw_min':'41', 
 'read_bw_max':'42', 
 'read_bw_agg_pct':'43', 
 'read_bw_mean':'44', 
 'read_bw_dev':'45', 
 'write_kb':'46', 
 'write_bandwidth':'47', 
 'write_iops':'48', 
 'write_runtime_ms':'49', 
 'write_slat_min':'50', 
 'write_slat_max':'51', 
 'write_slat_mean':'52', 
 'write_slat_dev':'53', 
 'write_clat_min':'54', 
 'write_clat_max':'55', 
 'write_clat_mean':'56', 
 'write_clat_dev':'57', 
 'write_clat_pct01':'58', 
 'write_clat_pct02':'59', 
 'write_clat_pct03':'60', 
 'write_clat_pct04':'61', 
 'write_clat_pct05':'62', 
 'write_clat_pct06':'63', 
 'write_clat_pct07':'64', 
 'write_clat_pct08':'65', 
 'write_clat_pct09':'66', 
 'write_clat_pct10':'67', 
 'write_clat_pct11':'68', 
 'write_clat_pct12':'69', 
 'write_clat_pct13':'70', 
 'write_clat_pct14':'71', 
 'write_clat_pct15':'72', 
 'write_clat_pct16':'73', 
 'write_clat_pct17':'74', 
 'write_clat_pct18':'75', 
 'write_clat_pct19':'76', 
 'write_clat_pct20':'77', 
 'write_tlat_min':'78', 
 'write_lat_max':'79', 
 'write_lat_mean':'80', 
 'write_lat_dev':'81', 
 'write_bw_min':'82', 
 'write_bw_max':'83', 
 'write_bw_agg_pct':'84', 
 'write_bw_mean':'85', 
 'write_bw_dev':'86', 
 'cpu_user':'87', 
 'cpu_sys':'88', 
 'cpu_csw':'89', 
 'cpu_mjf':'90', 
 'cpu_minf':'91', 
 'iodepth_1':'92', 
 'iodepth_2':'93', 
 'iodepth_4':'94', 
 'iodepth_8':'95', 
 'iodepth_16':'96', 
 'iodepth_32':'97', 
 'iodepth_64':'98', 
 'lat_2us':'99', 
 'lat_4us':'100', 
 'lat_10us':'101', 
 'lat_20us':'102', 
 'lat_50us':'103', 
 'lat_100us':'104', 
 'lat_250us':'105', 
 'lat_500us':'106', 
 'lat_750us':'107', 
 'lat_1000us':'108', 
 'lat_2ms':'109', 
 'lat_4ms':'110', 
 'lat_10ms':'111', 
 'lat_20ms':'112', 
 'lat_50ms':'113', 
 'lat_100ms':'114', 
 'lat_250ms':'115', 
 'lat_500ms':'116', 
 'lat_750ms':'117', 
 'lat_1000ms':'118', 
 'lat_2000ms':'119', 
 'lat_over_2000ms':'120', 
 'disk_name':'121', 
 'disk_read_iops':'122', 
 'disk_write_iops':'123', 
 'disk_read_merges':'124', 
 'disk_write_merges':'125', 
 'disk_read_ticks':'126', 
 'write_ticks':'127', 
 'disk_queue_time':'128', 
 'disk_util':'129'}
out_data = {}

def timeNow():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')


def adjustTime(timestamp):
    return time.mktime(datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S:%f').timetuple())


def follow(thefile, p):
    thefile.seek(0, 2)
    processCompleted = False
    while processCompleted == False:
        line = thefile.readline()
        if p.poll() is not None:
            if not line:
                yield 'quarch_end_Process'
                processCompleted = True
        if not line:
            time.sleep(0.1)
            continue
        yield line


def return_data(output_file, p, fioCallbacks, myStream, user_data, arguments):
    isThreaded = True
    if os.name == 'nt':
        isThreaded = False
        for i in arguments:
            if str(i.lower()) == 'thread':
                isThreaded = True

    info_out = {}
    logfile = open(output_file, 'r')
    loglines = follow(logfile, p)
    iterator = 0
    jobCount = 0
    jsonLines = ''
    openBracketCount = 0
    closeBracketCount = 0
    jobEndTime = int(round(time.time() * 1000))
    for line in loglines:
        if isThreaded == False:
            if iterator == 0:
                iterator = iterator + 1
                isThreaded = True
                continue
            else:
                iterator = iterator + 1
                jsonLines += line
                if '{' in line:
                    openBracketCount = openBracketCount + 1
                if '}' in line:
                    closeBracketCount = closeBracketCount + 1
                if openBracketCount == closeBracketCount and openBracketCount != 0:
                    try:
                        TempJsonObject = jsonLines[0:jsonLines.rindex('}') + 1]
                        jsonobject = json.loads(TempJsonObject)
                        if jobCount == 0:
                            startTime = jsonobject['timestamp_ms'] - jsonobject['jobs'][0]['read']['runtime']
                            comment = str(arguments).replace(',', '\n').replace('}', '').replace('{', '')
                            jobName = str(jsonobject['jobs'][0]['jobname'])
                            fioCallbacks['TEST_START'](myStream, str(startTime), jobName, comment)
                        readDataValue = jsonobject['jobs'][0]['read']['iops']
                        writeDataValue = jsonobject['jobs'][0]['write']['iops']
                        dataValues = {'read_iops':readDataValue, 
                         'write_iops':writeDataValue}
                        jobEndTime = str(jsonobject['timestamp_ms'])
                        fioCallbacks['TEST_RESULT'](myStream, jobEndTime, dataValues)
                        jsonLines = jsonLines[jsonLines.rindex('}') + 1:]
                        jobCount += 1
                    except:
                        pass

            if p.poll() is not None and line == 'quarch_end_Process':
                time.sleep(0.1)
                fioCallbacks['TEST_END'](myStream, str(int(jobEndTime) + 1))
                logfile.close()
                return


def rem_return_data(output_file, p, fioCallbacks, myStream, user_data, arguments):
    info_out = {}
    logfile = open(output_file, 'r')
    loglines = follow(logfile, p)
    iterator = 0
    for line in loglines:
        try:
            list = line.split(';')
            if len(list) == 1:
                continue
            if iterator == 0:
                timeStamp = adjustTime(timeNow())
                comment = str(arguments).replace(',', '\n').replace('}', '').replace('{', '')
                timeStamp = timeStamp - float(list[8]) / 1000
                fioCallbacks['TEST_START'](myStream, float(timeStamp), comment)
            for i in user_data:
                out_data[i] = list[int(all_outputs[i])]

            iterator += 1
            timeStamp = adjustTime(timeNow())
            fioCallbacks['TEST_RESULT'](myStream, timeStamp, out_data)
            if p.poll() is not None:
                return
        except:
            return


def start_fio(output_file, mode, options, fileName=''):
    if mode == 'cli':
        command = command + ' > pipe'
    if mode == 'file':
        command = 'fio ' + fileName + ' --log_unix_epoch=1 --output-format=json --output=' + output_file + ' --status-interval=1 --eta=never'
    if mode == 'arg':
        command = 'fio --log_unix_epoch=1 --output-format=json'
        for i in options:
            if options[i] == '':
                command = command + ' --' + i
            else:
                command = command + ' --' + i + '=' + options[i]

        command = command + ' > pipe'
    if os.path.exists(output_file):
        os.remove(output_file)
    if os.path.exists('pipe'):
        os.remove('pipe')
    p = subprocess.Popen(command, shell=True)
    while not os.path.exists(output_file):
        time.sleep(0.1)

    return p


def runFIO(myStream, mode, fioCallbacks, user_data, arguments='', file_name=''):
    try:
        xrange
    except NameError:
        xrange = range

    for i in xrange(0, len(arguments)):
        try:
            arguments_ori = arguments[i]
        except:
            arguments_ori = arguments

        output_file = arguments_ori['output']
        if file_name != '':
            file_name = '"' + file_name + '"'
        p = start_fio(output_file, mode, arguments_ori, file_name)
        return_data(output_file, p, fioCallbacks, myStream, user_data, arguments_ori)
        if os.path.exists('pipe'):
            os.remove('pipe')
        if isinstance(arguments, dict):
            break