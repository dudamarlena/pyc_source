# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dropboxmonitor.py
# Compiled at: 2014-04-03 03:33:52
# Size of source mod 2**32: 6729 bytes
"""
Created on Nov 29, 2013

@author: "Colin Manning"
"""
import traceback, os, sys, getopt, requests, logging.handlers, signal, json, utils
__dropbox_monitor_version__ = '0.1.3'
logger = None
config_data = None
os_userid = None
os_groupid = None

def main():
    global config_data
    global logger
    global os_groupid
    global os_userid
    help_text = 'usage:\n rintflow2-dropboxmonitor -c <configfile> -l <logfile>\n dropboxmonitor -v'
    configFile = None
    logFile = None
    logger = None
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'vhc:w:l:', ['version', 'configfile=', 'workgroup=', 'logfile='])
    except getopt.GetoptError:
        print(help_text)
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print(help_text)
            sys.exit()
        elif opt in ('-v', '--version'):
            print(('printflow2-dropboxmonitor version:', __printflow2_version__))
            sys.exit()
        elif opt in ('-c', '--configfile'):
            configFile = arg
        elif opt in ('-l', '--logfile'):
            logFile = arg
            continue

    if configFile is not None:
        with open(configFile) as (f):
            config_data = json.load(f)
            f.close()
        os_userid = config_data['os_userid']
        os_groupid = config_data['os_groupid']
        requests_log = logging.getLogger('requests')
        requests_log.setLevel(logging.WARNING)
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger('dropboxmonitor')
        handler = logging.handlers.TimedRotatingFileHandler(logFile, when='midnight')
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        if config_data['rootdir_done'] is not None:
            utils.ensureDirectoryExistsForUser(config_data['rootdir_done'], os_userid, os_groupid, 511)
            scanDir = os.path.join(config_data['rootdir'], config_data['scandir'])
        if config_data['rootdir'] is not None and os.path.exists(scanDir):
            process_scandir(scanDir)
        else:
            print('No root directory or root directory does not exist - bye.')
    return


def process_scandir(scanDir):
    file_index = 1
    rootDir = config_data['rootdir']
    rootDirDone = config_data['rootdir_done']
    rootCategory = config_data['rootcategory']
    logger.info('Scanning directory: ' + scanDir + ' for files to upload')
    logger.info('--- moving processed files to : ' + rootDirDone)
    for dirname, dirnames, filenames in os.walk(scanDir):
        rel_dirname = strip_prefix(rootDir, dirname)
        category_path = rootCategory + rel_dirname.replace('/', ':')
        category_info = createDamCategory(category_path)
        category_id = category_info['id']
        for filename in filenames:
            parent_dir = dirname.split('/')[(-1)]
            filename_bits = filename.split('.')
            pathname = os.path.join(dirname, filename)
            path_bits = dirname.split('/')
            try:
                if config_data['rename_files'] and config_data['rename_prefix'] is not None:
                    ext = None
                    if len(filename_bits) > 1:
                        ext = filename_bits[(-1)]
                    new_filename = config_data['rename_prefix'] + '_' + str(file_index)
                    if ext is not None:
                        new_filename = new_filename + '.' + ext
                    file_index = file_index + 1
                else:
                    new_filename = filename
                done_folder = os.path.join(rootDirDone, rel_dirname[1:])
                utils.ensureDirectoryExistsForUser(done_folder, os_userid, os_groupid, 511)
                process_file(filename, pathname, new_filename, category_id, done_folder)
            except:
                logger.error('problem processing file')
                logger.error(traceback.format_exc())

    logger.info('Scanning directory: ' + scanDir + ' done')
    return


def strip_prefix(prefix, s):
    if s.startswith(prefix):
        if len(prefix) == len(s):
            return ''
        else:
            return s[len(prefix):]
    else:
        return s


def process_file(filename, pathname, new_filename, category_id, done_folder):
    try:
        files = {'filename': (new_filename, open(pathname, 'rb'))}
        data = {'name': new_filename,  'profile': 'Images (Fast)',  'fulcrum_Country': config_data['metadata_template']['Country'], 
         'fulcrum_Original Name': filename}
        upload_url = config_data['cumulusapi'] + '/file/' + config_data['damsite'] + '/upload'
        response = requests.post(upload_url, data=data, files=files)
        if response.status_code == 200:
            r = response.json()
            asset_id = int(r['id'])
            if asset_id > 0:
                category_set_url = config_data['cumulusapi'] + '/data/' + config_data['damsite'] + '/addrecordtocategory?recordid=' + str(asset_id) + '&categoryid=' + str(category_id)
                response = requests.get(category_set_url)
                if response.status_code == 200:
                    logger.info('file: ' + filename + ' uploaded as: ' + new_filename)
                else:
                    logger.error('failed to link uploaded file: ' + filename + ' uploaded as: ' + new_filename + ' to category')
                utils.safe_file_move(pathname, done_folder)
            else:
                logger.error('failed to upload file: ' + pathname)
    except:
        logger.error(traceback.format_exc())
        traceback.print_exc()


def createDamCategory(category_path):
    requestUrl = config_data['cumulusapi'] + '/data/' + config_data['damsite'] + '/create?item=category&path=' + category_path.replace('&', '%26')
    disResponse = requests.get(requestUrl)
    return disResponse.json()


def close_down(signal, frame):
    print('dropboxmonitor is shutting down')
    sys.exit(0)


signal.signal(signal.SIGINT, close_down)
signal.signal(signal.SIGTERM, close_down)
if __name__ == '__main__':
    main()