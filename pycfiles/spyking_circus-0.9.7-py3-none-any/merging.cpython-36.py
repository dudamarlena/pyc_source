# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pierre/github/spyking-circus/build/lib/circus/merging.py
# Compiled at: 2019-11-21 11:07:31
# Size of source mod 2**32: 2539 bytes
from .shared.utils import *
from .shared import gui
from .shared.messages import init_logging, print_and_log
from circus.shared.utils import query_yes_no
import pylab
try:
    from PyQt5.QtWidgets import QApplication
except ImportError:
    from matplotlib.backends import qt_compat
    use_pyside = qt_compat.QT_API == qt_compat.QT_API_PYSIDE
    if use_pyside:
        from PySide.QtGui import QApplication
    else:
        from PyQt4.QtGui import QApplication

def main(params, nb_cpu, nb_gpu, use_gpu, extension):
    logger = init_logging(params.logfile)
    logger = logging.getLogger('circus.merging')
    file_out_suff = params.get('data', 'file_out_suff')
    erase_all = params.getboolean('merging', 'erase_all')
    extension_in = extension
    extension_out = '-merged'
    if comm.rank == 0:
        existing_file_paths = [file_path for file_path in [file_out_suff + '.%s%s.hdf5' % (file_id, extension_out) for file_id in ('templates',
                                                                                                                                   'clusters',
                                                                                                                                   'result')] if os.path.isfile(file_path)]
        existing_directory_path = [directory_path for directory_path in [
         file_out_suff + '%s.GUI' % extension_out] if os.path.isdir(directory_path)]
        if len(existing_file_paths) > 0 or len(existing_directory_path) > 0:
            if not erase_all:
                erase = query_yes_no('Merging already done! Do you want to erase previous merging results?', default=None)
            else:
                erase = True
            if erase:
                for path in existing_file_paths:
                    os.remove(path)
                    if comm.rank == 0:
                        print_and_log(['Removed file %s' % path], 'debug', logger)

                for path in existing_directory_path:
                    shutil.rmtree(path)
                    if comm.rank == 0:
                        print_and_log(['Removed directory %s' % path], 'debug', logger)

    else:
        comm.Barrier()
        if comm.rank == 0:
            if params.getfloat('merging', 'auto_mode') == 0:
                app = QApplication([])
                try:
                    pylab.style.use('ggplot')
                except Exception:
                    pass

        app = None
    if comm.rank == 0:
        print_and_log(['Launching the merging GUI...'], 'debug', logger)
    _ = gui.MergeWindow(params, app, extension_in, extension_out)
    sys.exit(app.exec_())