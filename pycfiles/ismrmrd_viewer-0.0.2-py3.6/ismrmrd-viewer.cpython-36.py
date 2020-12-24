# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\ismrmrd-viewer\ismrmrd-viewer.py
# Compiled at: 2019-05-10 16:25:06
# Size of source mod 2**32: 701 bytes
import ui, sys, logging, argparse
from PySide2 import QtWidgets
if __name__ == '__main__':
    logging.basicConfig(format='[%(levelname)s] %(message)s',
      level='INFO')
    parser = argparse.ArgumentParser(description='Simple ISMRMRD data file viewer.')
    parser.add_argument('file', type=str, nargs='?', help='ISMRMRD data file.')
    args = parser.parse_args()
    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName('ismrmrd-viewer.py')
    main = ui.MainWindow()
    main.resize(800, 600)
    main.show()
    if args.file:
        main.open_file(args.file)
    sys.exit(app.exec_())