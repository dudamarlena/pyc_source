# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\Yihui\lab\m2-dock\power_profiler\power_profiler.py
# Compiled at: 2020-05-08 03:47:10
# Size of source mod 2**32: 16478 bytes
"""
Power Profiler

Requirement:

    ```
    pip install pyserial
    pip install PyQt5
    # or `pip install PySide2`. PySide 2 does't work with Python 3.8.0
    pip install https://github.com/pyqtgraph/pyqtgraph/archive/develop.zip
    ```
"""
import time, traceback, sys, serial
from serial.tools import list_ports
import numpy as np, pyqtgraph as pg, pyqtgraph.exporters
GAIN = 0
DIV = 48
baudrate = 1073741824 | DIV << 16 | GAIN << 8
sample_rate = 48000000 / DIV / 2 / 11
BETA = (1.449, 119.52)
MAX_HISTORY = 1048576

class Probe(pg.QtCore.QThread):
    error = pg.QtCore.Signal(int)

    def __init__(self):
        super().__init__()
        self.done = False
        self.data = np.empty((4, 4096))
        self.index = 0
        self.n = 0
        self._gain = GAIN
        self.queue = []

    def run(self):
        for p in list_ports.comports():
            print(p)
            if p[2].upper().startswith('USB VID:PID=0D28:0204'):
                port = p[0]
                break
        else:
            print('No device found')
            self.error.emit(1)
            return

        print('Open {}'.format(port))
        device = serial.Serial(port=port, baudrate=baudrate,
          bytesize=8,
          parity='N',
          stopbits=1,
          timeout=1)
        device.write(b's')
        time.sleep(1)
        device.reset_input_buffer()
        device.write(str(self.gain).encode())
        device.write(b'g')
        bytes_count = 0
        samples_count = 0
        t1 = time.monotonic_ns()
        output = 'data.csv'
        with open(output, 'w') as (f):
            f.write('t,I,U\n')
            while not self.done:
                try:
                    if self.queue:
                        command = self.queue.pop(0)
                        device.write(command)
                        print('tx:{}'.format(command))
                    current_gain = self.gain
                    raw = device.read(4)
                    current = raw[3] << 2 | raw[2] >> 6
                    current = current * 1.3524 / BETA[current_gain]
                    voltage = (raw[2] & 63) << 4 | raw[1] >> 4
                    n = (raw[1] & 15) << 8 | raw[0]
                except IOError:
                    traceback.print_exc()
                    self.error.emit(2)
                    break
                except ValueError:
                    print(raw)
                    traceback.print_exc()

                bytes_count += 4
                samples_count += n
                t2 = time.monotonic_ns()
                dt = t2 - t1
                if dt >= 1000000000:
                    t1 = t2
                    print((bytes_count, samples_count, dt / 1000000))
                    bytes_count = 0
                    samples_count = 0
                if self.index & 4095 == 0:
                    print([n, current, voltage])

                def index_inc():
                    self.index += 1
                    if self.index < self.data.shape[1]:
                        return
                    else:
                        if self.index < MAX_HISTORY:
                            buffer = np.concatenate((
                             self.data, np.empty(self.data.shape)),
                              axis=1)
                            self.data = buffer
                        else:
                            half = MAX_HISTORY >> 1
                            np.savetxt(f, self.data[1:, :half].T, ['%d', '%f', '%d'], ',')
                            self.data[:, :half] = self.data[:, half:]
                            self.index -= half

                if n > 1:
                    self.data[0][self.index] = (self.n + 1) / sample_rate
                    self.data[1][self.index] = self.n + 1
                    self.data[2][self.index] = current
                    self.data[3][self.index] = voltage
                    index_inc()
                self.n += n
                self.data[0][self.index] = self.n / sample_rate
                self.data[1][self.index] = self.n
                self.data[2][self.index] = current
                self.data[3][self.index] = voltage
                index_inc()

            device.write(b's')
            device.close()
            np.savetxt(f, self.data[1:, :self.index].T, ['%d', '%f', '%d'], ',')

    def get(self):
        return (self.data, self.index)

    @property
    def gain(self):
        return self._gain

    @gain.setter
    def gain(self, g):
        self._gain = g
        self.queue.append(str(g).encode())

    def start(self):
        self.done = False
        super().start()

    def stop(self):
        self.done = True
        self.wait(2)


class MainWindow(pg.QtGui.QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowIcon(self.style().standardIcon(pg.QtGui.QStyle.SP_MediaPlay))
        self.setWindowTitle('Power Profiler')
        self.resize(1200, 720)
        self.widget = pg.PlotWidget()
        self.setCentralWidget(self.widget)
        self.widget.setLabel('left', 'I')
        self.widget.setLabel('bottom', 't/s')
        self.widget.showButtons()
        self.widget.setXRange(0, 10.0)
        self.widget.setYRange(0, 4)
        self.widget.setMouseEnabled(True, False)
        line = pg.InfiniteLine(pos=512,
          angle=0,
          movable=True,
          bounds=[0, 1024])
        self.widget.addItem(line)
        self.widget.showGrid(x=True, y=True, alpha=0.5)
        self.plot = self.widget.plot()
        self.plot.setPen((0, 255, 0))
        self.toolbar = self.addToolBar('toolbar')
        self.toolbar.setMovable(False)
        startAction = pg.QtGui.QAction('▶️', self)
        startAction.setToolTip('Run')
        startAction.setCheckable(True)
        startAction.setChecked(True)
        startAction.toggled.connect(self.start)
        self.toolbar.addAction(startAction)
        freezeAction = pg.QtGui.QAction('❄️', self)
        freezeAction.setToolTip('Freeze (Space)')
        freezeAction.setShortcut(' ')
        freezeAction.setCheckable(True)
        freezeAction.setChecked(False)
        freezeAction.toggled.connect(self.freeze)
        self.toolbar.addAction(freezeAction)
        saveAction = pg.QtGui.QAction('💾', self)
        saveAction.setToolTip('Save (Ctrl+S)')
        saveAction.setShortcut('Ctrl+S')
        saveAction.triggered.connect(self.save)
        self.toolbar.addAction(saveAction)
        gainAction = pg.QtGui.QAction('\U0001f9d0', self)
        gainAction.setToolTip('Increase Gain (.)')
        gainAction.setShortcut('.')
        gainAction.setCheckable(True)
        gainAction.setChecked(False)
        gainAction.toggled.connect(self.increaseGain)
        self.toolbar.addAction(gainAction)
        xZoomInShortcut = pg.QtGui.QShortcut('[', self)
        xZoomInShortcut.activated.connect(self.zoomInX)
        xZoomOutShortcut = pg.QtGui.QShortcut(']', self)
        xZoomOutShortcut.activated.connect(self.zoomOutX)
        yZoomInAction = pg.QtGui.QAction('🔍-', self)
        yZoomInAction.setToolTip('Y Zoom In (-)')
        yZoomInAction.setShortcut('-')
        yZoomInAction.triggered.connect(self.zoomInY)
        self.toolbar.addAction(yZoomInAction)
        yZoomOutAction = pg.QtGui.QAction('🔍+', self)
        yZoomOutAction.setToolTip('Y Zoom Out (+)')
        yZoomOutAction.setShortcut('=')
        yZoomOutAction.triggered.connect(self.zoomOutY)
        self.toolbar.addAction(yZoomOutAction)
        leftAction = pg.QtGui.QAction('←', self)
        leftAction.triggered.connect(self.moveLeft)
        self.toolbar.addAction(leftAction)
        leftAction.setVisible(False)
        leftShortcut = pg.QtGui.QShortcut(pg.QtGui.QKeySequence(pg.QtCore.Qt.Key_Left), self)
        leftShortcut.activated.connect(self.moveLeft)
        rightAction = pg.QtGui.QAction('→', self)
        rightAction.setShortcut(pg.QtGui.QKeySequence(pg.QtCore.Qt.Key_Right))
        rightAction.triggered.connect(self.moveRight)
        self.toolbar.addAction(rightAction)
        rightAction.setVisible(False)
        rightShortcut = pg.QtGui.QShortcut(pg.QtGui.QKeySequence(pg.QtCore.Qt.Key_Right), self)
        rightShortcut.activated.connect(self.moveRight)
        upAction = pg.QtGui.QAction('↑', self)
        upAction.setToolTip('Move Up (↑)')
        upAction.setShortcut(pg.QtGui.QKeySequence(pg.QtCore.Qt.Key_Up))
        upAction.triggered.connect(self.moveUp)
        self.toolbar.addAction(upAction)
        downAction = pg.QtGui.QAction('↓', self)
        downAction.setToolTip('Move Down (↓)')
        downAction.setShortcut(pg.QtGui.QKeySequence(pg.QtCore.Qt.Key_Down))
        downAction.triggered.connect(self.moveDown)
        self.toolbar.addAction(downAction)
        pinAction = pg.QtGui.QAction('📌', self)
        pinAction.setToolTip('Always On Top (Ctrl+t)')
        pinAction.setShortcut('Ctrl+t')
        pinAction.setCheckable(True)
        pinAction.setChecked(False)
        pinAction.toggled.connect(self.pin)
        self.toolbar.addAction(pinAction)
        infoAction = pg.QtGui.QAction('💡', self)
        infoAction.setToolTip('How it work (?)')
        infoAction.setShortcut('Shift+/')
        infoAction.triggered.connect(self.showInfo)
        self.toolbar.addAction(infoAction)
        self.toolbar.setStyleSheet('QToolButton {color: rgb(0,255,0)}QToolBar {background: rgb(30,30,30); border: none}')
        self.freezed = False
        self.probe = Probe()
        self.probe.error.connect(self.handle_error)
        self.probe.start()
        self.timer = pg.QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(50)
        gainAction.setChecked(True)

    def update(self):
        if not (self.freezed or self.probe.done):
            r = self.widget.viewRange()
            data, size = self.probe.get()
            n = data[0][(size - 1)]
            if n >= r[0][1]:
                self.widget.setXRange(n, (n + r[0][1] - r[0][0]), padding=0)
            self.plot.setData(data[0][:size], data[2][:size])

    def closeEvent(self, event):
        self.probe.stop()
        event.accept()

    def start(self, checked):
        if checked:
            self.probe.start()
            self.setWindowIcon(self.style().standardIcon(pg.QtGui.QStyle.SP_MediaPlay))
        else:
            self.probe.stop()
            self.setWindowIcon(self.style().standardIcon(pg.QtGui.QStyle.SP_MediaStop))

    def freeze(self, checked):
        self.freezed = checked

    def increaseGain(self, checked):
        self.probe.gain = 1 if checked else 0

    def save(self):
        dialog = pg.widgets.FileDialog.FileDialog(self)
        dialog.setAcceptMode(pg.QtGui.QFileDialog.AcceptSave)
        dialog.setFileMode(pg.QtGui.QFileDialog.AnyFile)
        dialog.setDefaultSuffix('csv')
        dialog.setNameFilter('*.csv')
        dialog.fileSelected.connect(self.export)
        dialog.show()

    def export(self, fileName):
        exporter = pg.exporters.CSVExporter(self.widget.getPlotItem())
        exporter.export(fileName)

    def zoomOutX(self):
        r = self.widget.viewRange()
        delta = (r[0][1] - r[0][0]) / 8
        self.widget.setXRange((r[0][0] + delta), (r[0][1] - delta), padding=0)

    def zoomInX(self):
        r = self.widget.viewRange()
        delta = (r[0][1] - r[0][0]) / 6
        self.widget.setXRange((r[0][0] - delta), (r[0][1] + delta), padding=0)

    def zoomOutY(self):
        r = self.widget.viewRange()
        delta = (r[1][1] - r[1][0]) / 8
        self.widget.setYRange((r[1][0]), (r[1][1] - delta), padding=0)

    def zoomInY(self):
        r = self.widget.viewRange()
        delta = (r[1][1] - r[1][0]) / 6
        self.widget.setYRange((r[1][0]), (r[1][1] + delta), padding=0)

    def moveLeft(self):
        r = self.widget.viewRange()
        delta = (r[0][1] - r[0][0]) / 16
        self.widget.setXRange((r[0][0] + delta), (r[0][1] + delta), padding=0)

    def moveRight(self):
        r = self.widget.viewRange()
        delta = (r[0][1] - r[0][0]) / 16
        self.widget.setXRange((r[0][0] - delta), (r[0][1] - delta), padding=0)

    def moveUp(self):
        r = self.widget.viewRange()
        delta = (r[1][1] - r[1][0]) / 16
        self.widget.setYRange((r[1][0] - delta), (r[1][1] - delta), padding=0)

    def moveDown(self):
        r = self.widget.viewRange()
        delta = (r[1][1] - r[1][0]) / 16
        self.widget.setYRange((r[1][0] + delta), (r[1][1] + delta), padding=0)

    def showInfo(self):
        pg.QtGui.QDesktopServices.openUrl(pg.QtCore.QUrl('https://github.com'))

    def pin(self, checked):
        if checked:
            self.setWindowFlags(self.windowFlags() | pg.QtCore.Qt.WindowStaysOnTopHint)
        else:
            self.setWindowFlags(self.windowFlags() & ~pg.QtCore.Qt.WindowStaysOnTopHint)
        self.show()

    def handle_error(self, error):
        message = 'No device found' if error == 1 else 'Read failed'
        flags = pg.QtGui.QMessageBox.Abort | pg.QtGui.QMessageBox.Retry
        result = pg.QtGui.QMessageBox.critical(self, 'ERROR', message, flags)
        if result == pg.QtGui.QMessageBox.Retry:
            self.probe.start()
        else:
            self.close()


def main():
    app = pg.QtGui.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()