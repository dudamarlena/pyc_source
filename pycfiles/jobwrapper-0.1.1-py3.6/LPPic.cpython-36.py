# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/jobwrapper/LPPic.py
# Compiled at: 2018-09-07 05:20:19
# Size of source mod 2**32: 14380 bytes
from sys import exit
import numpy as np, glob, h5py as hp, os, subprocess
from inputclass import inputparams

class LPPic:
    __doc__ = 'docstring for LPPic.'
    eps0 = 8.854187817e-12
    qe = 1.6021766e-19
    _Z_theta = False

    def __init__(self, path, oldmemo=True):
        inputobject = inputparams(path)
        inputobject.autodump()
        try:
            self._Z_theta = inputobject.parameters['Z_theta']
        except KeyError:
            self._Z_theta = False

        self.getpath(path=path)
        if not oldmemo:
            self.get_memo()
        else:
            self.oldgetmemo(self._path)
        self.inputobject = inputparams(path)

    def getpath(self, path):
        if path is '':
            print('you need to give a path')
            path = '.'
        self._path = path
        self._data_path = self._path + 'data/'
        self.image_path = self._path + 'images/'
        self.films_path = self._path + 'films/'

    def get_memo(self):
        """this function get the memo from the attributes of a file"""
        fichiers = glob.glob(self._data_path + 'particles*')
        fichier = fichiers[0]
        fichier = hp.File(fichier, 'r')
        self._imax = fichier.attrs['imax']
        self._xmax = fichier.attrs['xmax']
        self._ymax = fichier.attrs['ymax']
        self._zmax = fichier.attrs['zmax']
        self._Lx = fichier.attrs['Lx']
        self._Ly = fichier.attrs['Ly']
        self._Lz = fichier.attrs['Lz']
        self._n = fichier.attrs['n']
        self._ng = fichier.attrs['ng']
        self._qf = fichier.attrs['qf']
        self._M = fichier.attrs['M']
        self._dT = fichier.attrs['dT']
        self._dX = fichier.attrs['dX']
        self._B = fichier.attrs['B']
        self._Ez = fichier.attrs['Ez']
        self._procs = fichier.attrs['nprocs']
        self._Na = fichier.attrs['N_average']
        self._No = fichier.attrs['No_average']
        if fichier.attrs['isdiel'] == 1:
            self._ndiel = fichier.attrs['ndiel']
        else:
            self._ndiel = 0
        fichier.close()

    def oldgetmemo(self, path):
        """read the memo file present in the given path (usualy path/data)"""
        a = open(path + 'memo').read()
        exec('global imax,ymax,xmax,zmax,Lx,Ly,Lz,n,ng,qf,M,dT,dX,B,Ez,procs,Na,No,N_average,No_average,isdiel,ndiel,ionization_process ;' + a)
        self._imax = imax
        self._xmax = xmax
        self._ymax = ymax
        self._zmax = zmax
        self._Lx = Lx
        self._Ly = Ly
        self._Lz = Lz
        self._n = n
        self._ng = ng
        self._qf = qf
        self._M = M
        self._dT = dT
        self._dX = dX
        self._B = B
        self._Ez = Ez
        self._procs = procs
        try:
            N_average
        except NameError:
            self._Na = Na
        else:
            self._Na = N_average
        try:
            No_average
        except NameError:
            self._No = No
        else:
            self._No = No_average
        try:
            isdiel
        except NameError:
            self._ndiel = 0
        else:
            if isdiel:
                self._ndiel = ndiel
            else:
                self._ndiel = 0
            self.delta_T = self._dT * self._Na * 1000000.0

    def getallfiles(self, filetype):
        """select all of the file of the given type
            filetype should correspond to the begining of the file wanted
             (as tabgrid, particle, ...)"""
        files = glob.glob(self._data_path + filetype + '*')
        files.sort()
        self._nT = len(files)
        print('found ' + str(self._nT) + ' files')
        if files[0][-2:] == 'h5':
            fichier = hp.File(files[0], 'r')
        if files[0][-3:] == 'dat':
            print('loading dat file')
        self._files = files

    def lastfile(self):
        """ return the last file """
        return self._files[(-1)]

    def select_files(self, rangee):
        """"return file list for given range """
        if len(rangee) is not 2:
            print('wrong rangee shape')
            return 0
        if rangee[0] < 1:
            if rangee[1] < 1:
                rangee *= self._nT
                rangee = [int(r) for r in rangee]
        self._files = self._files[(rangee[0], rangee[1])]

    def plot1d(self, axe, vector, legend='', aspect=None):
        """plot the vector with the good labels"""
        self.definecoords()
        end = len(self.tab_time)
        start = int(end)
        if axe == 'x' or axe == 'X':
            abciss = self.tab_x
            xlabel = '$x$ $[cm]$'
        else:
            if axe == 't':
                abciss = self.tab_time
                xlabel = 'Time $[\\mu s]$'
            else:
                if axe == 'y' or axe == 'Y':
                    abciss = self.tab_y
                    xlabel = '$y$ $[cm]$'
                else:
                    if axe == 'z' or axe == 'Z':
                        abciss = self.tab_z
                        xlabel = '$z$ $[cm]$'
                    else:
                        print('axe not understood')
        if axe == 'y' or axe == 'Y':
            if not np.shape(vector)[0] == np.shape(abciss)[0]:
                abciss = abciss[self._ndiel:self._ymax + 1 + self._ndiel]
                abciss -= abciss[0]
        else:
            if not np.shape(abciss)[0] == np.shape(vector)[0]:
                print('abciss : ', np.shape(abciss))
                print('Ordonnee : ', np.shape(vector))
                print('ERROR in the PLOT1D value size')
            if aspect != None:
                plt.plot(abciss, vector, aspect, label=legend)
            else:
                plt.plot(abciss, vector, label=legend)
        plt.xlim(abciss[0], abciss[(-1)])
        if legend is not None:
            plt.legend(loc='best')
        plt.grid()
        plt.xlabel(xlabel)
        try:
            plt.ylabel(self.extended_label + ' $[$' + self.unit + '$]$')
        except AttributeError:
            print('no extended label possible')

    def saveimage(self, name, show=False):
        plt.savefig(self.image_path + name + '.png')
        if show:
            plt.show()
        plt.close()

    def savefilm(self, name):
        plt.savefig(self.films_path + name + '.png')

    def makefilm(self, snapname, moviename):
        try:
            os.remove(self.films_path + moviename + '.mp4')
        except:
            pass

        import ffmpy
        ff = ffmpy.FFmpeg(inputs={self.films_path + snapname + '%d.png': '-r 24'}, outputs={self.films_path + moviename + '.mp4': '-r 24'})
        ff.run()
        try:
            os.remove(self.films_path + snapname + '%d.png')
        except:
            pass

    def definecoords(self):
        self.tab_time = [(t * self._Na * self._dT + self._No) * 1000000.0 for t in np.arange(self._nT)]
        taby = np.loadtxt(self._data_path + 'tab_dy.txt')
        self.tab_y = [0 for i in taby]
        for x in range(1, np.shape(taby)[0]):
            self.tab_y[x] = self.tab_y[(x - 1)] + (taby[x] + taby[(x - 1)]) / 2 * self._dX * 100

        self.tab_x = [x * self._dX * 100 for x in np.arange(self._xmax + 1)]
        self.tab_z = [z * self._dX * 100 for z in np.arange(self._zmax + 1)]

    def definenames(self):
        if self.label == 'Phi':
            self.extended_label = 'Plasma potential'
            self.unit = '$V$'
        else:
            if self.label == 'Nume':
                self.extended_label = 'Electron density'
                self.unit = '$m^{-3}$'
            else:
                if self.label == 'Numi':
                    self.extended_label = 'Ion density'
                    self.unit = '$m^{-3}$'
                else:
                    if self.label == 'Ej(1)':
                        self.extended_label = 'Azimuthal electric field'
                        self.unit = '$V.m^{-1}$'
                    else:
                        if self.label == 'Ej(2)':
                            if self._Z_theta:
                                self.extended_label = 'Axial electric field'
                            else:
                                self.extended_label = 'Radial electric field'
                            self.unit = '$V.m^{-1}$'
                        else:
                            if self.label == 'Rho':
                                self.extended_label = 'Density of charge'
                                self.unit = '$C.m^{-3}$'
                            else:
                                if self.label == 'Ejnj':
                                    self.extended_label = 'Correlation term'
                                    self.unit = '$(Vs)^{-1}$'
                                else:
                                    if self.label == 'Mob':
                                        self.extended_label = 'Electron mobility'
                                        self.unit = '$V^{-1}s^{-1}$'
                                    else:
                                        if self.label == 'Ri':
                                            self.extended_label = 'Ionization source term'
                                            self.unit = '$collisions.m^{-3}.s^{-1}$'
                                        else:
                                            if self.label == 'nu_total':
                                                self.extended_label = 'Collisions term'
                                                self.unit = '$collisions.m^{-2}$'
                                            else:
                                                if self.label == 'X':
                                                    self.extended_label = 'Azimutal position'
                                                    self.unit = '$cm$'
                                                else:
                                                    if self.label == 'Y':
                                                        if self._Z_theta:
                                                            self.extended_label = 'Axial position'
                                                        else:
                                                            self.extended_label = 'Radial position'
                                                        self.unit = '$cm$'
                                                    else:
                                                        if self.label == 'Z':
                                                            if self._Z_theta:
                                                                self.extended_label = 'Radial position'
                                                            else:
                                                                self.extended_label = 'Axial position'
                                                            self.unit = '$cm$'
                                                        else:
                                                            if self.label == 'Vx':
                                                                self.extended_label = 'Azimutal Velocity'
                                                                self.unit = '$m.s^{-1}$'
                                                            else:
                                                                if self.label == 'Vy':
                                                                    if self._Z_theta:
                                                                        self.extended_label = 'Axial velocity'
                                                                    else:
                                                                        self.extended_label = 'Radial velocity'
                                                                    self.unit = '$m.s^{-1}$'
                                                                else:
                                                                    if self.label == 'Vz':
                                                                        if self._Z_theta:
                                                                            self.extended_label = 'Radial velocity'
                                                                        else:
                                                                            self.extended_label = 'Axial velocity'
                                                                        self.unit = '$m.s^{-1}$'
                                                                    else:
                                                                        if self.label == 'EEDF':
                                                                            self.extended_label = 'Energy'
                                                                            self.unit = '$eV$'
                                                                        else:
                                                                            if self.label == 'EEPF':
                                                                                self.extended_label = 'Energy'
                                                                                self.unit = '$eV$'
                                                                            else:
                                                                                if self.label == 'Mob_average_ratio':
                                                                                    self.extended_label = 'Electron mobility'
                                                                                    self.unit = '$m^{2}.V^{-1}.s^{-1}$'
                                                                                else:
                                                                                    if self.label == 'Mob_ratio_average':
                                                                                        self.extended_label = 'Electron mobility'
                                                                                        self.unit = '$m^{2}.V^{-1}.s^{-1}$'
                                                                                    else:
                                                                                        if self.label == 'Je(1)':
                                                                                            self.extended_label = 'Electron azimutal current'
                                                                                            self.unit = '$A.m^{-2}$'
                                                                                        else:
                                                                                            if self.label == 'Je(2)':
                                                                                                if self._Z_theta:
                                                                                                    self.extended_label = 'Electron axial current'
                                                                                                else:
                                                                                                    self.extended_label = 'Electron radial current'
                                                                                                self.unit = '$A.m^{-2}$'
                                                                                            else:
                                                                                                if self.label == 'Je(3)':
                                                                                                    if self._Z_theta:
                                                                                                        self.extended_label = 'Electron radial current'
                                                                                                    else:
                                                                                                        self.extended_label = 'Electron axial current'
                                                                                                    self.unit = '$A.m^{-2}$'
                                                                                                else:
                                                                                                    if self.label == 'Ji(1)':
                                                                                                        self.extended_label = 'Ion azimutal current'
                                                                                                        self.unit = '$A.m^{-2}$'
                                                                                                    else:
                                                                                                        if self.label == 'Ji(2)':
                                                                                                            if self._Z_theta:
                                                                                                                self.extended_label = 'Ion axial current'
                                                                                                            else:
                                                                                                                self.extended_label = 'Ion radial current'
                                                                                                            self.unit = '$A.m^{-2}$'
                                                                                                        else:
                                                                                                            if self.label == 'Ji(3)':
                                                                                                                if self._Z_theta:
                                                                                                                    self.extended_label = 'Ion radial current'
                                                                                                                else:
                                                                                                                    self.extended_label = 'Ion axial current'
                                                                                                                self.unit = '$A.m^{-2}$'
                                                                                                            else:
                                                                                                                if self.label == 'Eke(1)':
                                                                                                                    self.extended_label = 'Electron azimutal energy'
                                                                                                                    self.unit = '$eV$'
                                                                                                                else:
                                                                                                                    if self.label == 'Eke(2)':
                                                                                                                        if self._Z_theta:
                                                                                                                            self.extended_label = 'Electron axial energy'
                                                                                                                        else:
                                                                                                                            self.extended_label = 'Electron radial energy'
                                                                                                                        self.unit = '$eV$'
                                                                                                                    else:
                                                                                                                        if self.label == 'Eke(3)':
                                                                                                                            if self._Z_theta:
                                                                                                                                self.extended_label = 'Electron radial energy'
                                                                                                                            else:
                                                                                                                                self.extended_label = 'Electron axial energy'
                                                                                                                            self.unit = '$eV$'
                                                                                                                        else:
                                                                                                                            if self.label == 'Eki(1)':
                                                                                                                                self.extended_label = 'Ion azimutal energy'
                                                                                                                                self.unit = '$eV$'
                                                                                                                            else:
                                                                                                                                if self.label == 'Eki(2)':
                                                                                                                                    if self._Z_theta:
                                                                                                                                        self.extended_label = 'Ion axial energy'
                                                                                                                                    else:
                                                                                                                                        self.extended_label = 'Ion radial energy'
                                                                                                                                    self.unit = '$eV$'
                                                                                                                                else:
                                                                                                                                    if self.label == 'Eki(3)':
                                                                                                                                        if self._Z_theta:
                                                                                                                                            self.extended_label = 'Ion radial energy'
                                                                                                                                        else:
                                                                                                                                            self.extended_label = 'Ion axial energy'
                                                                                                                                        self.unit = '$eV$'
                                                                                                                                    else:
                                                                                                                                        print('you need to define the label')
                                                                                                                                        self.extended_label = 'Error label '
                                                                                                                                        self.unit = 'Error label'

    def getmeanTe(self):
        """return the mean Te at the end of a run"""
        try:
            Te = self.outputobject.parameters['meanTe']
        except KeyError:
            self.getallfiles('tempor')
            data = np.loadtxt(self.lastfile())
            SUMe_x = data[:, 3]
            SUMe_y = data[:, 4]
            SUMe_z = data[:, 5]
            SUMe = SUMe_x + SUMe_y + SUMe_z
            icut = int(0.2 * dat._nT)
            Te = np.mean(SUMe[icut:])
            self.outputobject.addattribute('meanTe', Te)

        return Te