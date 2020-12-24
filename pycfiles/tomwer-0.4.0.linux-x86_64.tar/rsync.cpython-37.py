# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/tomwer_venc/lib/python3.7/site-packages/tomwer/app/rsync.py
# Compiled at: 2020-01-23 10:07:36
# Size of source mod 2**32: 4163 bytes
import logging, sys, argparse, glob, os, shutil
from tomwer.core.scan.scanfactory import ScanFactory
from tomwer.synctools.utils.scanstages import ScanStages
logging.basicConfig(level=(logging.INFO))
logger = logging.getLogger(__name__)

def getinputinfo():
    return 'tomwer rsync [source_dir] [dest_dir] [options]'


def main(argv):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source_dir',
      help='folder containing the acquisition to copy.To copy /dir_path/scan_dir into /dir_path2/scan_dir source-dir should be /dir_path/scan_dir')
    parser.add_argument('dest_dir',
      help="destination folder. If doesn't exists will create it.Will synchronizeIf exists and contains some files, those won't be removeexcept if the --fresh option is activatedTo copy /dir_path/scan_dir into /dir_path2/scan_dir dest-dir should be /dir_path2")
    parser.add_argument('--advancement',
      help=("An acquisition contains several steps (initialization, acquisition, complete...). You can ask to synchronize file until a specific stage. \nFor edf for example if you specify the stage `on_going` no .info while be created and the targeted directory won't contain any 'slice' files. \nDefault value is `complete`Valid advancement values are: %s" % str(ScanStages.AcquisitionStage.get_command_names())))
    parser.add_argument('--fresh',
      help='first file to be used for computing axis',
      action='store_true',
      default=False)
    parser.add_argument('--force',
      '-f', help='force folder removal',
      action='store_true',
      default=False)
    parser.add_argument('--rm-final-xml',
      help='util option: remove the .xml created at the end of some .edfacquisition (which notify the end of the acquisition). \nWarning: this is an exclusive option. So it cannot be associatedwith any other option.',
      action='store_true',
      default=False)
    options = parser.parse_args(argv[1:])
    if options.rm_final_xml is True:
        if options.advancement is not None or options.fresh is True:
            logger.error('--rm-final-xml is an `exclusive`option. It cannot beassociated with an other option')
            return
    if options.advancement is None:
        if options.rm_final_xml is False:
            options.advancement = 'complete'
    for scan_path in glob.glob(options.source_dir):
        try:
            scan = ScanFactory.create_scan_object(scan_path=scan_path)
        except ValueError:
            logger.error(scan_path + ' is not containing a scan')
            continue

        dest_dir = os.path.join(options.dest_dir, os.path.basename(options.source_dir))

        def refresh_dir(dir_):
            logger.info('recreate', dir_)
            shutil.rmtree(dir_)
            os.mkdir(dir_)

        if options.rm_final_xml is True:
            final_xml = os.path.join(dest_dir, os.path.basename(dest_dir) + '.xml')
            if os.path.exists(final_xml):
                os.remove(final_xml)
                continue
            if options.fresh:
                if os.path.exists(dest_dir):
                    if options.force is False:
                        conf = input('do you want to remove %s (yes/y) ?' % dest_dir)
                        if conf.lower() in ('yes', 'y'):
                            refresh_dir(dir_=dest_dir)
                    else:
                        refresh_dir(dir_=dest_dir)
            scan_stages = ScanStages(scan=scan)
            stage = ScanStages.AcquisitionStage.from_command_name(options.advancement)
            scan_stages.rsync_until(stage=stage, dest_dir=dest_dir)


if __name__ == '__main__':
    main(sys.argv)