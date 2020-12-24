# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.4-x86_64/egg/yapocis/demo_mandelbrot.py
# Compiled at: 2011-08-30 23:33:15
import numpy as np, time
w = 1024
h = 1024
from rpc import kernels, interfaces
calc_fractal_opencl = kernels.loadProgram(interfaces.mandelbrot, engine=kernels.CPU_ENGINE).mandelbrot

def calc_fractal_serial(q, maxiter):
    z = np.zeros(q.shape, np.complex64)
    output = np.resize(np.array(0), q.shape)
    for i in range(len(q)):
        for iter in range(maxiter):
            z[i] = z[i] * z[i] + q[i]
            if abs(z[i]) > 2.0:
                q[i] = complex(0.0, 0.0)
                z[i] = complex(0.0, 0.0)
                output[i] = iter

    return output


def calc_fractal_numpy(q, maxiter):
    output = np.resize(np.array(0), q.shape)
    z = np.zeros(q.shape, np.complex64)
    for iter in range(maxiter):
        z = z * z + q
        done = np.greater(abs(z), 2.0)
        q = np.where(done, complex(0.0, 0.0), q)
        z = np.where(done, complex(0.0, 0.0), z)
        output = np.where(done, iter, output)

    return output


calc_fractal = calc_fractal_opencl
if __name__ == '__main__':
    import Tkinter as tk
    try:
        import Image, ImageTk
    except:
        from PIL import Image
        from PIL import ImageTk

    class Mandelbrot(object):

        def __init__(self):
            self.root = tk.Tk()
            self.root.title('Mandelbrot Set')
            self.create_image()
            self.create_label()
            self.root.mainloop()

        def draw(self, x1, x2, y1, y2, maxiter=256):
            xx = np.arange(x1, x2, (x2 - x1) / w)
            yy = np.arange(y2, y1, (y1 - y2) / h) * complex(0.0, 1.0)
            q = np.ravel(xx + yy[:, np.newaxis]).astype(np.complex64)
            start_main = time.time()
            output = calc_fractal(q, maxiter)
            end_main = time.time()
            secs = end_main - start_main
            print ('Main took', secs)
            self.mandel = (output.reshape((h, w)) / float(output.max()) * 255.0).astype(np.uint8)

        def create_image(self):
            """"
            create the image from the draw() string
            """
            self.draw(-2.13, 0.77, -1.3, 1.3)
            self.im = Image.fromarray(self.mandel)
            self.im.putpalette(reduce(lambda a, b: a + b, ((i, 0, 0) for i in range(255))))

        def create_label(self):
            self.image = ImageTk.PhotoImage(self.im)
            self.label = tk.Label(self.root, image=self.image)
            self.label.pack()


    test = Mandelbrot()