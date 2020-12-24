# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/alessio/Envs/remote-wps/lib/python2.7/site-packages/wpsremote/xmpp_data/configs/myservice/code/test.py
# Compiled at: 2018-11-09 04:01:19
import subprocess, logging.config, logging, argparse, sys, thread, traceback, logging, sys, os, uuid, zipfile, time
id = str(uuid.uuid4())
gdalContour = '/usr/bin/gdal_contour'
dst = 'contour_' + id[:13]
src = '%s/../../../resource_dir/srtm_39_04/srtm_39_04_c.tif' % os.path.dirname(os.path.abspath(__file__))
cmd = '-a elev'
interval = '-i'

class GDALTest(object):

    def __init__(self, args):
        self.args = args
        self.create_logger('logger_test.properties')
        self.logger.info('ProgressInfo:0.0%')

    def run(self):
        trg = '%s/../../../output/%s/%s.shp' % (os.path.dirname(os.path.abspath(__file__)), self.args.execution_id, dst)
        fullCmd = (' ').join([gdalContour, cmd, src, trg, interval, self.args.interval])
        self.logger.debug('Running command > ' + fullCmd)
        self.logger.info('going to sleep again...')
        time.sleep(30)
        proc = subprocess.Popen(fullCmd.split(), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=False)
        for line in proc.stdout:
            self.logger.info(line)

        proc.communicate()
        ret = proc.returncode
        self.logger.info('...waking up and going to sleep again...')
        time.sleep(30)
        if ret == 0:
            output_dir = '%s/../../../output/%s' % (os.path.dirname(os.path.abspath(__file__)), self.args.execution_id)
            zipf = zipfile.ZipFile(output_dir + '/contour.zip', 'w')
            self.zipdir(output_dir + '/', zipf)
            zipf.close()
            self.logger.info('ProgressInfo:100%')
        else:
            self.logger.critical('Error occurred during processing.')
        return ret

    def youCanQuoteMe(self, item):
        return '"' + item + '"'

    def zipdir(self, path, zip):
        for root, dirs, files in os.walk(path):
            files = [ fi for fi in files if fi.startswith(dst) ]
            for file in files:
                zip.write(os.path.join(root, file))

    def create_logger(self, logger_config_file):
        defaults = {}
        logging.config.fileConfig(str(logger_config_file), defaults=defaults)
        self.logger = logging.getLogger('main.create_logger')
        self.logger.debug('Logger initialized with file ' + str(logger_config_file))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--interval', nargs='?', default='10', help='Elevation interval between contours.')
    parser.add_argument('-w', '--workdir', nargs='?', default='', help='Remote process sandbox working directory.')
    parser.add_argument('-e', '--execution_id', nargs='?', default='', help='Remote process Unique Execution Id.')
    cmdargs = parser.parse_args()
    gdalTest = GDALTest(cmdargs)
    return_code = gdalTest.run()
    sys.exit(return_code)