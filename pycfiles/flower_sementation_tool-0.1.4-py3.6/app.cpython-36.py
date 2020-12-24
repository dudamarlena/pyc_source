# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/gui/app.py
# Compiled at: 2019-06-19 03:47:57
# Size of source mod 2**32: 15852 bytes
import os, cv2, glob, numpy as np
from matplotlib.patches import Circle
from PyQt5 import QtWidgets
from gui.pyqt5backend.guidesign import Ui_MainWindow
from filter.data import Data

class DesignerMainWindow(QtWidgets.QMainWindow, Ui_MainWindow, Data):
    __doc__ = '\n    This is the Application class.\n    It inherits Ui_MainWindow created in the Qt5Designer.\n    It inherits the Data class to ensure access of image objects faster.\n    App class DesignerMainWindow is called by main.py\n\n    Flower Segmentation Tool\n    * RGB image plot\n    * crops images centers by percentage to original\n    * to segment and visualize yellow flowers\n    * adjust the minimum size of segmented areas\n    * another visualization with red circles available\n    * can be used on individual images or on images of a file directory\n\n    Author: Anna Tenberg\n    github: github.com/AnnaTe/arnica\n    '

    def __init__(self, parent=None):
        super(DesignerMainWindow, self).__init__(parent)
        self.setupUi(self)
        self.i = None
        self.perc = 100
        self.mins = None
        self.statusbar.showMessage('Ready')
        self.actionSingle.triggered.connect(self.select_file)
        self.actionDirectory.triggered.connect(self.select_dir)
        self.pbImageOpen.clicked.connect(self.select_file)
        self.pbUpdate.clicked.connect(self.update_graph)
        self.pbExport.clicked.connect(self.export_image)
        self.pbDirectoryOpen.clicked.connect(self.select_dir)
        self.pbDirectoryExport.clicked.connect(self.select_dir)
        self.pbRun.clicked.connect(self.run_export)

    def select_file(self):
        """opens a file select dialog and plots file"""
        self.statusbar.showMessage('Loading Image')
        if self.lineEditImage.text() == '' or self.sender().text() == 'Open Image':
            file = QtWidgets.QFileDialog.getOpenFileName(self, 'Select Image')
            self.lineEditImage.setText(file[0])
            self.tabWidget.setCurrentIndex(0)
        try:
            self.initial_plot()
            self.perc = 100
            self.mins = None
        except:
            self.statusbar.showMessage('ERROR: File has to be an image. Try JPG or PNG Type.')

    def select_dir(self):
        """opens directory selection dialog"""
        directory = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select directory')
        if self.sender().text() == 'Export':
            self.lineEditDirOut.setText(directory)
        else:
            self.lineEditDirIn.setText(directory)
            self.tabWidget.setCurrentIndex(1)

    def parse_file(self):
        """ initiates image as an object of data class."""
        self.i = Data(self.lineEditImage.text())
        return self.i

    def plot(self, image):
        """ plots filtered image in Matplotlib canvas widget."""
        self.mpl.canvas.ax.clear()
        self.mpl.canvas.ax.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        self.mpl.canvas.ax.axis('off')
        self.mpl.canvas.draw()
        self.statusbar.clearMessage()

    def initial_plot(self):
        """ plots first input image in Matplotlib canvas widget."""
        a = self.parse_file()
        self.plot(a.img)

    def update_graph(self):
        """ updates the plot in Matplotlib canvas widget. """
        self.statusbar.showMessage('update is running...')
        percent = self.sbCrop.value()
        lowsize = self.sbBlob.value()
        if self.cbCircle.isChecked() == True:
            if percent != self.perc:
                self.i.filter(percent, lowsize)
                self.mins = lowsize
                self.perc = percent
            else:
                if lowsize != self.mins:
                    self.i.yellow(self.i.cropped, lowsize)
                    self.mins = lowsize
            self.mpl.canvas.ax.clear()
            number, output, stats, centroids = cv2.connectedComponentsWithStats((self.i.blob[:, :, 2]), connectivity=8)
            nb_components = number - 1
            left = stats[1:, 0]
            top = stats[1:, 1]
            width = stats[1:, 2]
            height = stats[1:, 3]
            sizes = stats[1:, 4]
            center = np.array((centroids[1:, 0].astype(int), centroids[1:, 1].astype(int))).transpose()
            groupsize = np.mean(sizes) * 2
            centers = []
            radius = []
            for i in range(0, nb_components):
                if sizes[i] >= groupsize:
                    if width[i] / height[i] >= 0.75:
                        if width[i] / height[i] < 1.5:
                            continue
                    if width[i] / height[i] < 0.75:
                        if width[i] / height[i] >= 0.415:
                            center[i] = np.array([width[i] / 2 + left[i], height[i] / 4 + top[i]])
                            centers.append([width[i] / 2 + left[i], height[i] / 4 * 3 + top[i]])
                            radius.append(np.min((width[i], height[i])))
                    if width[i] / height[i] < 2.5:
                        if width[i] / height[i] >= 1.5:
                            center[i] = np.array([width[i] / 4 + left[i], height[i] / 2 + top[i]])
                            centers.append([width[i] / 4 * 3 + left[i], height[i] / 2 + top[i]])
                            radius.append(np.min((width[i], height[i])))
                    if width[i] / height[i] >= 2.5:
                        if width[i] / height[i] < 3.5:
                            centers.append([width[i] / 4 + left[i], height[i] / 2 + top[i]])
                            radius.append(np.min((width[i], height[i])))
                            centers.append([width[i] / 4 * 3 + left[i], height[i] / 2 + top[i]])
                            radius.append(np.min((width[i], height[i])))
                    if width[i] / height[i] < 0.415:
                        if width[i] / height[i] >= 0.29:
                            centers.append([width[i] / 2 + left[i], height[i] / 4 + top[i]])
                            radius.append(np.min((width[i], height[i])))
                            centers.append([width[i] / 2 + left[i], height[i] / 4 * 3 + top[i]])
                            radius.append(np.min((width[i], height[i])))
                if width[i] / height[i] < 0.29 and width[i] / height[i] >= 0.225:
                    center[i] = np.array([width[i] / 2 + left[i], height[i] / 5 + top[i]])
                    centers.append([width[i] / 2 + left[i], height[i] / 5 * 2 + top[i]])
                    radius.append(np.min((width[i], height[i])))
                    centers.append([width[i] / 2 + left[i], height[i] / 5 * 3 + top[i]])
                    radius.append(np.min((width[i], height[i])))
                    centers.append([width[i] / 2 + left[i], height[i] / 5 * 4 + top[i]])
                    radius.append(np.min((width[i], height[i])))
                elif width[i] / height[i] >= 3.5 and width[i] / height[i] < 4.5:
                    center[i] = np.array([width[i] / 5 + left[i], height[i] / 2 + top[i]])
                    centers.append([width[i] / 5 * 2 + left[i], height[i] / 2 + top[i]])
                    radius.append(np.min((width[i], height[i])))
                    centers.append([width[i] / 5 * 3 + left[i], height[i] / 2 + top[i]])
                    radius.append(np.min((width[i], height[i])))
                    centers.append([width[i] / 5 * 4 + left[i], height[i] / 2 + top[i]])
                    radius.append(np.min((width[i], height[i])))
                else:
                    if width[i] / height[i] < 0.225:
                        centers.append([width[i] / 2 + left[i], height[i] / 6 + top[i]])
                        radius.append(np.min((width[i], height[i])))
                        centers.append([width[i] / 2 + left[i], height[i] / 6 * 2 + top[i]])
                        radius.append(np.min((width[i], height[i])))
                        centers.append([width[i] / 2 + left[i], height[i] / 6 * 4 + top[i]])
                        radius.append(np.min((width[i], height[i])))
                        centers.append([width[i] / 2 + left[i], height[i] / 6 * 5 + top[i]])
                        radius.append(np.min((width[i], height[i])))
                    else:
                        if width[i] / height[i] >= 4.5:
                            centers.append([width[i] / 6 + left[i], height[i] / 2 + top[i]])
                            radius.append(np.min((width[i], height[i])))
                            centers.append([width[i] / 6 * 2 + left[i], height[i] / 2 + top[i]])
                            radius.append(np.min((width[i], height[i])))
                            centers.append([width[i] / 6 * 5 + left[i], height[i] / 2 + top[i]])
                            radius.append(np.min((width[i], height[i])))
                            centers.append([width[i] / 6 * 4 + left[i], height[i] / 2 + top[i]])
                            radius.append(np.min((width[i], height[i])))

            self.mpl.canvas.ax.imshow(cv2.cvtColor(self.i.cropped, cv2.COLOR_BGR2RGB))
            self.mpl.canvas.ax.axis('off')
            self.i.count = 0
            for i in range(centroids[1:, 1].shape[0]):
                circ = Circle((tuple(center[i])), (np.min(stats[i + 1, 2:4])), color='r', linewidth=0.5, fill=False)
                self.mpl.canvas.ax.add_patch(circ)
                self.i.count += 1

            for a in range(len(centers)):
                circ2 = Circle((tuple(centers[a])), (int(radius[a])), color='b', linewidth=0.5, fill=False)
                self.mpl.canvas.ax.add_patch(circ2)
                self.i.count += 1

            self.mpl.canvas.draw()
            self.statusbar.showMessage('{} Flowers counted.'.format(self.i.count))
        else:
            if self.cbYellow.isChecked() == True:
                if percent != self.perc:
                    self.i.filter(percent, lowsize)
                    self.mins = lowsize
                    self.perc = percent
                else:
                    if lowsize != self.mins:
                        self.i.yellow(self.i.cropped, lowsize)
                        self.mins = lowsize
                self.plot(self.i.blob)
                self.statusbar.showMessage('{} Flowers counted.'.format(self.i.count))
            else:
                if percent == self.perc:
                    self.plot(self.i.cropped)
                else:
                    self.perc = percent
                    self.i.crop(self.perc)
                    self.plot(self.i.cropped)

    def export_image(self):
        """Exports the plotted image with filedialog."""
        self.statusbar.showMessage('Export is running...')
        percent = self.sbCrop.value()
        lowsize = self.sbBlob.value()
        if self.cbCircle.isChecked() == True:
            if percent == self.perc:
                if lowsize == self.mins:
                    try:
                        self.mpl.ntb.save_figure()
                    except:
                        self.statusbar.showMessage('Figsave not working.')

            else:
                if percent != self.perc:
                    self.i.filter(percent, lowsize)
                    self.mins = lowsize
                    self.perc = percent
                else:
                    self.i.yellow(self.i.cropped, lowsize)
                    self.mins = lowsize
            number, output, stats, centroids = cv2.connectedComponentsWithStats((self.i.blob[:, :, 0]), connectivity=8)
            center = list(zip(centroids[1:, 0].astype(int), centroids[1:, 1].astype(int)))
            radius = stats[1:, 3]
            image = np.copy(self.i.cropped)
            self.i.count = 0
            for i in range(centroids[1:, 1].shape[0]):
                cv2.circle(image, (center[i]), (radius[i]), color=(0, 0, 255), thickness=3)
                self.i.count += 1

            self.plot(image)
            self.mpl.ntb.save_figure()
            self.statusbar.showMessage('{} Flowers counted.'.format(self.i.count))
        else:
            if self.cbYellow.isChecked() == True:
                try:
                    saveas = QtWidgets.QFileDialog.getSaveFileName(self, 'Save as')[0]
                except:
                    self.statusbar.showMessage('Export failed, try again.')

                if percent != self.perc:
                    self.i.filter(percent, lowsize)
                    self.mins = lowsize
                    self.perc = percent
                else:
                    if lowsize != self.mins:
                        self.i.yellow(self.i.cropped, lowsize)
                        self.mins = lowsize
                    try:
                        cv2.imwrite(saveas, self.i.blob)
                    except:
                        self.statusbar.showMessage('ERROR: Not a valid file name. File type has to be JPG or PNG.')
                    else:
                        self.statusbar.clearMessage()
            else:
                try:
                    saveas = QtWidgets.QFileDialog.getSaveFileName(self, 'Save as')[0]
                except:
                    self.statusbar.showMessage('Export failed, try again.')

                if percent == self.perc:
                    pass
                else:
                    self.perc = percent
                    self.i.crop(self.perc)
        try:
            cv2.imwrite(saveas, self.i.cropped)
        except:
            self.statusbar.showMessage('ERROR: Not a valid file name. File type has to be JPG or PNG.')
        else:
            self.statusbar.clearMessage()

    def run_export(self):
        """runs process for all images of directory and exports into output directory"""
        self.statusbar.showMessage('Export is running...')
        path = self.lineEditDirIn.text() + '/*.*'
        paths = glob.glob(path)
        outputdir = self.lineEditDirOut.text() + '/'
        os.makedirs(outputdir, exist_ok=True)
        self.completed = 0
        self.total = len(paths)
        percent = self.sbCropDir.value()
        lowsize = self.sbBlobDir.value()
        for imagepath in paths:
            self.i = Data(imagepath)
            if self.cbYellowDir.isChecked() == True:
                try:
                    self.i.filter(percent, lowsize)
                except:
                    self.statusbar.showMessage('ERROR: Images in import directory not found. Try again.')

                outpath = outputdir + self.i.name + 'seg' + str(lowsize) + '.png'
                cv2.imwrite(outpath, self.i.blob)
                self.completed += 1
                self.statusbar.showMessage('Running: {} of {} images exported.'.format(self.completed, self.total))
            else:
                try:
                    self.i.crop(percent)
                except:
                    self.statusbar.showMessage('ERROR: Images in import directory not found. Try again.')

                outpath = outputdir + self.i.name + 'crop' + str(percent) + '.png'
                cv2.imwrite(outpath, self.i.cropped)
                self.completed += 1
                self.statusbar.showMessage('Running: {} of {} images exported.'.format(self.completed, self.total))

        self.statusbar.showMessage('Process finished.', 500)