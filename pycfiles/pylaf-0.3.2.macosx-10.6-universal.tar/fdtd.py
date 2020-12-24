# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Python/2.6/site-packages/PyLAF/recipes/fdtd.py
# Compiled at: 2011-05-31 05:25:03
import scipy, numpy, threading
from scipy import weave
import Tkinter, ttk, pylaf
from pylaf import Component, Port, Panel, Entry, TableBuilder
from pylaf.vtkext import numpy_to_vtk, UIntScalarStructuredPoints, StructuredPoints

def calchx(yee, dt):
    code = '\n    #define mu 1.256637061\n    #define Vhx(i,j,k) (hx+(i)*Nhx[1]*Nhx[2]+(j)*Nhx[2]+k)\n    #define Vey(i,j,k) (ey+(i)*Ney[1]*Ney[2]+(j)*Ney[2]+k)\n    #define Vez(i,j,k) (ez+(i)*Nez[1]*Nez[2]+(j)*Nez[2]+k)\n    for (int k = 0; k < Nhx[2]; k++)\n        for (int j = 0; j < Nhx[1]; j++)\n            for (int i = 0; i < Nhx[0]; i++) {\n                *Vhx(i,j,k) +=\n                    - dt/mu/dy*(*Vez(i,j+1,k  )-*Vez(i,j,k))\n                    + dt/mu/dz*(*Vey(i,j  ,k+1)-*Vey(i,j,k));\n            }\n    '
    (ex, ey, ez) = yee.efield
    (hx, hy, hz) = yee.hfield
    (dx, dy, dz) = yee.delta
    weave.inline(code, ['hx', 'ey', 'ez', 'dy', 'dz', 'dt'])


def calchy(yee, dt):
    code = '\n    #define mu 1.256637061\n    #define Vex(i,j,k) (ex+(i)*Nex[1]*Nex[2]+(j)*Nex[2]+k)\n    #define Vhy(i,j,k) (hy+(i)*Nhy[1]*Nhy[2]+(j)*Nhy[2]+k)\n    #define Vez(i,j,k) (ez+(i)*Nez[1]*Nez[2]+(j)*Nez[2]+k)\n    for (int k = 0; k < Nhy[2]; k++)\n        for (int j = 0; j < Nhy[1]; j++)\n            for (int i = 0; i < Nhy[0]; i++) {\n                *Vhy(i,j,k) +=\n                    - dt/mu/dz*(*Vex(i  ,j,k+1)-*Vex(i,j,k))\n                    + dt/mu/dx*(*Vez(i+1,j,k  )-*Vez(i,j,k));\n            }\n    '
    (ex, ey, ez) = yee.efield
    (hx, hy, hz) = yee.hfield
    (dx, dy, dz) = yee.delta
    weave.inline(code, ['ex', 'hy', 'ez', 'dz', 'dx', 'dt'])


def calchz(yee, dt):
    code = '\n    #define mu 1.256637061\n    #define Vex(i,j,k) (ex+(i)*Nex[1]*Nex[2]+(j)*Nex[2]+k)\n    #define Vey(i,j,k) (ey+(i)*Ney[1]*Ney[2]+(j)*Ney[2]+k)\n    #define Vhz(i,j,k) (hz+(i)*Nhz[1]*Nhz[2]+(j)*Nhz[2]+k)\n    for (int k = 0; k < Nhz[2]; k++)\n        for (int j = 0; j < Nhz[1]; j++)\n            for (int i = 0; i < Nhz[0]; i++) {\n                *Vhz(i,j,k) +=\n                    - dt/mu/dx*(*Vey(i+1,j  ,k)-*Vey(i,j,k))\n                    + dt/mu/dy*(*Vex(i  ,j+1,k)-*Vex(i,j,k));\n            }\n    '
    (ex, ey, ez) = yee.efield
    (hx, hy, hz) = yee.hfield
    (dx, dy, dz) = yee.delta
    weave.inline(code, ['ex', 'ey', 'hz', 'dx', 'dy', 'dt'])


def calcex(yee, dt):
    code = '\n    #define ep 0.000008854187817\n    #define Vex(i,j,k) (ex+(i)*Nex[1]*Nex[2]+(j)*Nex[2]+k)\n    #define Vhy(i,j,k) (hy+(i)*Nhy[1]*Nhy[2]+(j)*Nhy[2]+k)\n    #define Vhz(i,j,k) (hz+(i)*Nhz[1]*Nhz[2]+(j)*Nhz[2]+k)\n    #define Vepr(i,j,k) (epr+(i)*Nepr[1]*Nepr[2]+(j)*Nepr[2]+k)\n    for (int k = 1; k < Nex[2]-1; k++)\n        for (int j = 1; j < Nex[1]-1; j++)\n            for (int i = 0; i < Nex[0]; i++) {\n                double er = (*Vepr(i,j,k)+*Vepr(i,j,k-1)+*Vepr(i,j-1,k-1)+*Vepr(i,j-1,k))/4;\n                *Vex(i,j,k) +=\n                    + dt/ep/er/dy*(*Vhz(i,j,k)-*Vhz(i,j-1,k  ))\n                    - dt/ep/er/dz*(*Vhy(i,j,k)-*Vhy(i,j  ,k-1));\n            }\n    '
    (ex, ey, ez) = yee.efield
    (hx, hy, hz) = yee.hfield
    (dx, dy, dz) = yee.delta
    epr = yee.epr
    weave.inline(code, ['ex', 'hy', 'hz', 'dy', 'dz', 'dt', 'epr'])


def pcalcex(yee, dt):
    ep = 8.854187817e-06
    (ex, ey, ez) = yee.efield
    (hx, hy, hz) = yee.hfield
    (dx, dy, dz) = yee.delta
    epr = yee.epr
    er = (epr[:, 1:, 1:] + epr[:, 1:, :-1] + epr[:, :-1, :-1] + epr[:, :-1, 1:]) / 4.0
    ex[:, 1:-1, 1:-1] += dt / ep / er / dy * (hz[:, 1:, 1:-1] - hz[:, :-1, 1:-1]) - dt / ep / er / dz * (hy[:, 1:-1, 1:] - hy[:, 1:-1, :-1])


def calcey(yee, dt):
    code = '\n    #define ep 0.000008854187817\n    #define Vhx(i,j,k) (hx+(i)*Nhx[1]*Nhx[2]+(j)*Nhx[2]+k)\n    #define Vey(i,j,k) (ey+(i)*Ney[1]*Ney[2]+(j)*Ney[2]+k)\n    #define Vhz(i,j,k) (hz+(i)*Nhz[1]*Nhz[2]+(j)*Nhz[2]+k)\n    #define Vepr(i,j,k) (epr+(i)*Nepr[1]*Nepr[2]+(j)*Nepr[2]+k)\n    for (int k = 1; k < Ney[2]-1; k++)\n        for (int j = 0; j < Ney[1]; j++)\n            for (int i = 1; i < Ney[0]-1; i++) {\n                double er = (*Vepr(i,j,k)+*Vepr(i,j,k-1)+*Vepr(i-1,j,k-1)+*Vepr(i-1,j,k))/4;\n                *Vey(i,j,k) +=\n                    + dt/ep/er/dz*(*Vhx(i,j,k)-*Vhx(i  ,j,k-1))\n                    - dt/ep/er/dx*(*Vhz(i,j,k)-*Vhz(i-1,j,k  ));\n            }\n    '
    (ex, ey, ez) = yee.efield
    (hx, hy, hz) = yee.hfield
    (dx, dy, dz) = yee.delta
    epr = yee.epr
    weave.inline(code, ['hx', 'ey', 'hz', 'dz', 'dx', 'dt', 'epr'])


def calcez(yee, dt):
    code = '\n    #define ep 0.000008854187817\n    #define Vhx(i,j,k) (hx+(i)*Nhx[1]*Nhx[2]+(j)*Nhx[2]+k)\n    #define Vhy(i,j,k) (hy+(i)*Nhy[1]*Nhy[2]+(j)*Nhy[2]+k)\n    #define Vez(i,j,k) (ez+(i)*Nez[1]*Nez[2]+(j)*Nez[2]+k)\n    #define Vepr(i,j,k) (epr+(i)*Nepr[1]*Nepr[2]+(j)*Nepr[2]+k)\n    for (int k = 0; k < Nez[2]; k++)\n        for (int j = 1; j < Nez[1]-1; j++)\n            for (int i = 1; i < Nez[0]-1; i++) {\n                double er = (*Vepr(i,j,k)+*Vepr(i,j-1,k)+*Vepr(i-1,j-1,k)+*Vepr(i-1,j,k))/4;\n                *Vez(i,j,k) +=\n                    + dt/ep/er/dx*(*Vhy(i,j,k)-*Vhy(i-1,j  ,k))\n                    - dt/ep/er/dy*(*Vhx(i,j,k)-*Vhx(i  ,j-1,k));\n            }\n    '
    (ex, ey, ez) = yee.efield
    (hx, hy, hz) = yee.hfield
    (dx, dy, dz) = yee.delta
    epr = yee.epr
    weave.inline(code, ['hx', 'hy', 'ez', 'dx', 'dy', 'dt', 'epr'])


class StructuredYee:

    def __init__(self, size=(30, 30, 30), delta=(10.0, 10.0, 10.0), dt=1.0):
        self.size = size
        self.shape = size
        self.delta = delta
        self.dt = dt
        self.current_time = 0.0
        self.clear_fields()
        self.epr = scipy.ones(size, dtype=scipy.double)

    def clear_fields(self):
        size, opts = self.size, {'dtype': scipy.double}
        hx = scipy.zeros([size[0] + 1, size[1], size[2]], **opts)
        hy = scipy.zeros([size[0], size[1] + 1, size[2]], **opts)
        hz = scipy.zeros([size[0], size[1], size[2] + 1], **opts)
        ex = scipy.zeros([size[0], size[1] + 1, size[2] + 1], **opts)
        ey = scipy.zeros([size[0] + 1, size[1], size[2] + 1], **opts)
        ez = scipy.zeros([size[0] + 1, size[1] + 1, size[2]], **opts)
        self.hfield = [hx, hy, hz]
        self.efield = [ex, ey, ez]

    def courant(self):
        max_epr = self.epr.max()
        vc = 299.792458 / scipy.sqrt(max_epr)
        (dx, dy, dz) = self.delta
        tc = 1.0 / (vc * scipy.sqrt(1.0 / dx ** 2 + 1.0 / dy ** 2 + 1.0 / dz ** 2))
        return tc


class YeeUIntScalarStructuredPoints(UIntScalarStructuredPoints):

    def __init__(self, **kw):
        UIntScalarStructuredPoints.__init__(self, **kw)

    def reset(self):
        UIntScalarStructuredPoints.reset(self)
        yee = self.sigin.get()
        try:
            yee.delta
        except AttributeError:
            return
        else:
            (dz, dy, dx) = yee.delta
            if not self.GetSpacing() == (dx, dy, dz):
                self.config(Spacing=(dx, dy, dz))

    def update(self, yee):
        (ex, ey, ez) = yee.efield
        ex = (ex[:, :-1, :-1] + ex[:, :-1, 1:] + ex[:, 1:, 1:] + ex[:, 1:, :-1]) / 4.0
        ey = (ey[:-1, :, :-1] + ey[:-1, :, 1:] + ey[1:, :, 1:] + ey[1:, :, :-1]) / 4.0
        ez = (ez[:-1, :-1, :] + ez[:-1, 1:, :] + ez[1:, 1:, :] + ez[1:, :-1, :]) / 4.0
        return scipy.sqrt(ex * ex + ey * ey + ez * ez)


class YeeStructuredPoints(StructuredPoints):

    def __init__(self, **kw):
        StructuredPoints.__init__(self, **kw)

    def reset(self):
        StructuredPoints.reset(self)
        yee = self.sigin.get()
        try:
            yee.delta
        except AttributeError:
            pass
        else:
            (dz, dy, dx) = yee.delta
            self.config(Spacing=(dx, dy, dz))

    def shape(self, yee):
        if not len(yee.shape) == 3:
            return StructuredPoints.shape(self, yee)
        (i, j, k) = yee.shape
        return (i, j, k, 3)

    def update_scalars(self):
        (k, j, i, c) = self.vectorData.shape
        self.scalarData[:, :, :] = self.vectorData[:, :, :, 0] ** 2
        for l in range(1, c):
            self.scalarData[:, :, :] += self.vectorData[:, :, :, l] ** 2

        self.scalarData[:, :, :] = numpy.sqrt(self.scalarData)


class YeeEStructuredPoints(YeeStructuredPoints):

    def __init__(self, **kw):
        YeeStructuredPoints.__init__(self, **kw)

    def update_vectors(self, vector, yee):
        (ex, ey, ez) = yee.efield
        vector[:, :, :, 0] = (ex[:, :-1, :-1] + ex[:, :-1, 1:] + ex[:, 1:, 1:] + ex[:, 1:, :-1]) / 4.0
        vector[:, :, :, 1] = (ey[:-1, :, :-1] + ey[:-1, :, 1:] + ey[1:, :, 1:] + ey[1:, :, :-1]) / 4.0
        vector[:, :, :, 2] = (ez[:-1, :-1, :] + ez[:-1, 1:, :] + ez[1:, 1:, :] + ez[1:, :-1, :]) / 4.0


class YeeHStructuredPoints(YeeStructuredPoints):

    def __init__(self, **kw):
        YeeStructuredPoints.__init__(self, **kw)

    def update_vectors(self, vector, yee):
        (hx, hy, hz) = yee.hfield
        vector[:, :, :, 0] = (hx[:-1, :, :] + hx[1:, :, :]) / 2.0
        vector[:, :, :, 1] = (hy[:, :-1, :] + hy[:, 1:, :]) / 2.0
        vector[:, :, :, 2] = (hz[:, :, :-1] + hz[:, :, 1:]) / 2.0
        (z, y, x, c) = vector.shape
        self.GetPointData().SetVectors(numpy_to_vtk(vector.reshape(z * y * x, c)))


class Plugin:

    def __init__(self, **kw):
        self.dataset = Port(None)
        self.config(**kw)
        return

    def config(self, **kw):
        if kw == None:
            return
        else:
            if kw.has_key('dataset'):
                kw['dataset'].link(self.dataset)
            return

    def __call__(self):
        pass


class UpdatingTime(Plugin):

    def __init__(self, **kw):
        self.counter = Port(None)
        self.offset = Port(0.0)
        Plugin.__init__(self, **kw)
        return

    def config(self, **kw):
        Plugin.config(self, **kw)
        if kw.has_key('counter'):
            kw['counter'].link(self.counter)
        if kw.has_key('offset'):
            self.offset.set(kw['offset'])

    def __call__(self):
        dataset = self.dataset.get()
        dt = dataset.dt
        dataset.current_time = dt * (self.counter.get() + self.offset.get())


class UpdatingEField(Plugin):

    def __call__(self):
        dataset = self.dataset.get()
        dt = dataset.dt
        pcalcex(dataset, dt)
        calcey(dataset, dt)
        calcez(dataset, dt)


class UpdatingHField(Plugin):

    def __call__(self):
        dataset = self.dataset.get()
        dt = dataset.dt
        calchx(dataset, dt)
        calchy(dataset, dt)
        calchz(dataset, dt)


class AlgorithmView(ttk.Treeview):

    def __init__(self, master=None, name=None, **kw):
        ttk.Treeview.__init__(self, master, name=name)
        self.config(**kw)
        self.loop()

    def loop(self):
        self.populate()
        self.after(500, self.loop)

    def populate(self, parent=''):
        pass


class Fdtd(Component):

    def __init__(self, master=None, name=None, **kw):
        Component.__init__(self, master, name)
        self.yee = self.sigout = Port(None)
        self.maxiter = Port(1000)
        self.counter = Port(0)
        self.finish = Port(None)
        self.initialize = []
        self.sequence = []
        self.config(**kw)
        return

    def config(self, **kw):
        if kw == None:
            return
        else:
            if kw.has_key('dataset'):
                self.yee.set(kw['dataset'])
            return

    def start(self):
        for o in self.initialize:
            o()

        thread = threading.Thread(target=self.run)
        thread.setDaemon(True)
        thread.start()

    def cancel(self):
        self.canceled = None
        return

    def run(self):
        counter = self.counter.get()
        while counter < self.maxiter.get():
            try:
                self.canceled
            except AttributeError:
                pass
            else:
                del self.canceled
                break

            self.step()
            counter = self.counter.get()

        self.finish.set(None)
        return

    def step(self):
        for o in self.sequence:
            o()

        self.yee.subject.notify(pylaf.EVENT_SET)
        self.counter.set(self.counter.get() + 1)

    class Control(Panel):

        def __init__(self, master=None, cnf={}, **kw):
            Panel.__init__(self, master, cnf, **kw)
            Tkinter.Label(self, text='カウンタ(最大反復数)').grid(row=0, column=0)
            f = Tkinter.Frame(self)
            f.grid(row=0, column=1)
            self.grid_rowconfigure(0, weight=0)
            pylaf.Label(f, name='counter', width=8).pack(side=Tkinter.LEFT, expand=True, fill=Tkinter.X)
            Tkinter.Label(f, text='(').pack(side=Tkinter.LEFT, expand=True, fill=Tkinter.X)
            Entry(f, name='maxiter', width=8).pack(side=Tkinter.LEFT, expand=True, fill=Tkinter.X)
            Tkinter.Label(f, text=')').pack(side=Tkinter.LEFT, expand=True, fill=Tkinter.X)
            b, l, e = TableBuilder(self), Tkinter.Label, Entry
            b.add(Tkinter.Button, name='calculate', text='Calculate', command=self.calculate).grid(columnspan=2, sticky=Tkinter.W + Tkinter.E)
            b.add(Tkinter.Button, name='clear', text='Clear Fields', command=self._clear).grid(columnspan=2, sticky=Tkinter.W + Tkinter.E)
            b.add(AlgorithmView, name='sequence').grid(columnspan=2)
            self.finish = Port(None).bind(self._finished)
            self.grid_rowconfigure(1, weight=0)
            self.grid_rowconfigure(2, weight=0)
            return

        def assign(self, component):
            Panel.assign(self, component)

        def calculate(self):
            calculate = self.children['calculate']
            text = calculate.config('text')[(-1)]
            if text == 'Calculate':
                self.component().start()
                calculate.config(text='Cancel')
            elif text == 'Cancel':
                self.component().cancel()

        def _finished(self):
            calculate = self.children['calculate']
            text = calculate.config('text')[(-1)]
            if text == 'Cancel':
                calculate.config(text='Calculate')

        def _clear(self):
            c = self.component()
            c.counter.set(0)
            c.yee.get().clear_fields()
            c.yee.subject.notify(pylaf.EVENT_SET)


dummy_yee = StructuredYee(size=(1, 1, 1))
calchx(dummy_yee, dummy_yee.dt)
calchy(dummy_yee, dummy_yee.dt)
calchz(dummy_yee, dummy_yee.dt)
calcex(dummy_yee, dummy_yee.dt)
calcey(dummy_yee, dummy_yee.dt)
calcez(dummy_yee, dummy_yee.dt)
dummy_yee = None