# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/bullseye/process.py
# Compiled at: 2012-03-03 20:29:01
from traits.api import HasTraits, Float, Int, Unicode, Range, Bool, Instance, on_trait_change, Dict, Event
import numpy as np, logging, bisect
from threading import Thread
from .special_sums import angle_sum, polar_sum
from .capture import BaseCapture

class Process(HasTraits):
    capture = Instance(BaseCapture)
    thread = Instance(Thread)
    active = Bool(False)
    track = Bool(False)
    crops = Int(3)
    rad = Float(3 / 2.0)
    background = Range(0.0, 1.0, 0.0)
    ignore = Range(0.0, 0.5, 0.01)
    include_radius = Float
    x = Float
    y = Float
    t = Float
    e = Float
    a = Float
    b = Float
    d = Float
    black = Float
    peak = Float
    text = Unicode
    data = Dict()
    new_data = Event()

    def initialize(self):
        self.capture.start()
        im = self.capture.capture()
        self.process(im.copy())
        self.capture.stop()

    def moments(self, im):
        y, x = np.ogrid[:im.shape[0], :im.shape[1]]
        imx, imy = im.sum(axis=0)[None, :], im.sum(axis=1)[:, None]
        m00 = float(imx.sum()) or 1.0
        m10, m01 = (imx * x).sum() / m00, (imy * y).sum() / m00
        x, y = x - m10, y - m01
        m20, m02 = (imx * x ** 2).sum() / m00, (imy * y ** 2).sum() / m00
        m11 = (im * x * y).sum() / m00
        return (
         m00, m10, m01, m20, m02, m11)

    def gauss(self, m00, m20, m02, m11):
        p = m00 / (2 * np.pi * (m02 * m20 - m11 ** 2) ** 0.5)
        q = ((m20 - m02) ** 2 + 4 * m11 ** 2) ** 0.5
        a = 2 * 1.4142135623730951 * (m20 + m02 + q) ** 0.5
        b = 2 * 1.4142135623730951 * (m20 + m02 - q) ** 0.5
        t = 0.5 * np.arctan2(2 * m11, m20 - m02)
        return (
         p, a, b, t)

    def do_crop(self, imc, m00, m10, m01, m20, m02, m11):
        if self.ignore > 0:
            re = polar_sum(imc, center=(m01, m10), direction='azimuthal', aspect=1.0, binsize=1.0)
            np.cumsum(re, out=re)
            rinc = bisect.bisect(re, (1.0 - self.ignore) * m00)
            w20 = w02 = rinc
        else:
            w20 = self.rad * 4 * m20 ** 0.5
            w02 = self.rad * 4 * m02 ** 0.5
            rinc = ((w20 ** 2 + w02 ** 2) / 2) ** 0.5
        w02 = max(w02, 4)
        w20 = max(w20, 4)
        lc = int(max(0, m10 - w20))
        bc = int(max(0, m01 - w02))
        tc = int(min(imc.shape[0], m01 + w02))
        rc = int(min(imc.shape[1], m10 + w20))
        imc = imc[bc:tc, lc:rc]
        return (
         rinc, lc, bc, rc, tc, imc)

    def process(self, im):
        im = np.array(im)
        imc = im
        lc, bc = (0, 0)
        black = 0
        for i in range(self.crops):
            if self.background > 0:
                blackc = np.percentile(imc, self.background * 100)
                imc = imc - blackc
                np.clip(imc, 0, self.capture.maxval, out=imc)
                black += blackc
            m00, m10, m01, m20, m02, m11 = self.moments(imc)
            if i < self.crops - 1:
                rinc, dlc, dbc, drc, dtc, imc = self.do_crop(imc, m00, m10, m01, m20, m02, m11)
                lc += dlc
                bc += dbc

        m10 += lc
        m01 += bc
        wp, wa, wb, wt = self.gauss(m00, m20, m02, m11)
        px = self.capture.pixelsize
        l, b, w, h = self.capture.bounds
        self.m00 = m00
        self.m20 = m20
        self.m02 = m02
        self.black = black / self.capture.maxval
        self.peak = (wp + black) / self.capture.maxval
        self.x = (m10 + l - self.capture.width / 2) * px
        self.y = (m01 + b - self.capture.height / 2) * px
        self.t = np.rad2deg(wt)
        self.a = wa * px
        self.b = wb * px
        self.d = ((self.a ** 2 + self.b ** 2) / 2) ** 0.5
        self.e = wb / wa
        self.include_radius = rinc * px
        self.update_text()
        x = np.arange(l, l + w) - self.capture.width / 2
        y = np.arange(b, b + h) - self.capture.height / 2
        xbounds = (np.r_[(x, x[(-1)] + 1)] - 0.5) * px
        ybounds = (np.r_[(y, y[(-1)] + 1)] - 0.5) * px
        imx = im.sum(axis=0)
        imy = im.sum(axis=1)
        gx = m00 / (2 * np.pi * m20) ** 0.5 * np.exp(-(x - self.x / px) ** 2 / (m20 * 2))
        gy = m00 / (2 * np.pi * m02) ** 0.5 * np.exp(-(y - self.y / px) ** 2 / (m02 * 2))
        xc, yc = m10 - im.shape[1] / 2.0, m01 - im.shape[0] / 2.0
        dab = max(abs(np.cos(wt)), abs(np.sin(wt)))
        ima = angle_sum(im, wt, binsize=dab)
        imb = angle_sum(im, wt + np.pi / 2, binsize=dab)
        xcr = (np.cos(wt) * xc + np.sin(wt) * yc) / dab + ima.shape[0] / 2.0
        ycr = (-np.sin(wt) * xc + np.cos(wt) * yc) / dab + imb.shape[0] / 2.0
        ima = ima[int(max(0, xcr - self.rad * wa / dab)):int(min(ima.shape[0], xcr + self.rad * wa / dab))]
        imb = imb[int(max(0, ycr - self.rad * wb / dab)):int(min(imb.shape[0], ycr + self.rad * wb / dab))]
        a = np.arange(ima.shape[0]) * dab - min(xcr * dab, self.rad * wa)
        b = np.arange(imb.shape[0]) * dab - min(ycr * dab, self.rad * wb)
        ga = m00 / ((2 * np.pi) ** 0.5 * wa / 4) * np.exp(-a ** 2 / ((wa / 4) ** 2 * 2))
        gb = m00 / ((2 * np.pi) ** 0.5 * wb / 4) * np.exp(-b ** 2 / ((wb / 4) ** 2 * 2))
        upd = dict((
         (
          'img', im),
         (
          'xbounds', xbounds), ('ybounds', ybounds),
         (
          'x', x * px), ('y', y * px),
         (
          'imx', imx), ('imy', imy),
         (
          'gx', gx), ('gy', gy),
         (
          'a', a * px), ('b', b * px),
         (
          'ima', ima), ('imb', imb),
         (
          'ga', ga), ('gb', gb)))
        upd.update(self.markers())
        self.data = upd
        self.new_data = True

    def markers(self):
        px = self.capture.pixelsize
        ts = np.linspace(0, 2 * np.pi, 41)
        ex, ey = self.a / 2 * np.cos(ts), self.b / 2 * np.sin(ts)
        t = np.deg2rad(self.t)
        ex, ey = ex * np.cos(t) - ey * np.sin(t), ex * np.sin(t) + ey * np.cos(t)
        k = np.array([-self.rad, self.rad])
        upd = dict((
         (
          'ell1_x', self.x + ex),
         (
          'ell1_y', self.y + ey),
         (
          'ell3_x', self.x + 3 * ex),
         (
          'ell3_y', self.y + 3 * ey),
         (
          'a_x', self.a * k * np.cos(t) + self.x),
         (
          'a_y', self.a * k * np.sin(t) + self.y),
         (
          'b_x', -self.b * k * np.sin(t) + self.x),
         (
          'b_y', self.b * k * np.cos(t) + self.y),
         (
          'x0_mark', 2 * [self.x]),
         (
          'xp_mark', 2 * [self.x + 2 * px * self.m20 ** 0.5]),
         (
          'xm_mark', 2 * [self.x - 2 * px * self.m20 ** 0.5]),
         (
          'x_bar', [0, self.m00 / (2 * np.pi * self.m20) ** 0.5]),
         (
          'y0_mark', 2 * [self.y]),
         (
          'yp_mark', 2 * [self.y + 2 * px * self.m02 ** 0.5]),
         (
          'ym_mark', 2 * [self.y - 2 * px * self.m02 ** 0.5]),
         (
          'y_bar', [0, self.m00 / (2 * np.pi * self.m02) ** 0.5]),
         (
          'a0_mark', 2 * [0]),
         (
          'ap_mark', 2 * [self.a / 2]),
         (
          'am_mark', 2 * [-self.a / 2]),
         (
          'a_bar', [0, self.m00 / (np.pi ** 0.5 * self.a / px / 2 / 1.4142135623730951)]),
         (
          'b0_mark', 2 * [0]),
         (
          'bp_mark', 2 * [self.b / 2]),
         (
          'bm_mark', 2 * [-self.b / 2]),
         (
          'b_bar', [0, self.m00 / (np.pi ** 0.5 * self.b / px / 2 / 1.4142135623730951)])))
        return upd

    def update_text(self):
        fields = (
         self.x, self.y,
         self.a, self.b,
         self.t, self.e,
         self.black, self.peak, self.include_radius)
        logging.info(('beam: ' + '% 6.4g,' * len(fields)), *fields)
        self.text = 'centroid x: %.4g µm\ncentroid y: %.4g µm\nmajor 4sig: %.4g µm\nminor 4sig: %.4g µm\nrotation: %.4g°\nellipticity: %.4g\nblack-peak: %.4g-%.4g\ninclude radius: %.4g µm\n' % fields

    def do_track(self):
        r = self.rad
        w, h = self.capture.roi[2:]
        x, y = float(self.x - w / 2), float(self.y - h / 2)
        self.capture.roi = [
         x, y, w, h]

    @on_trait_change('active')
    def _start_me(self, active):
        if active:
            if self.thread is not None:
                if self.thread.is_alive():
                    logging.warning('already have a capture thread running')
                    return
                self.thread.join()
            self.thread = Thread(target=self.run)
            self.thread.start()
        elif self.thread is not None:
            self.thread.join(timeout=5)
            if self.thread is not None:
                if self.thread.is_alive():
                    logging.warning('capture thread did not terminate')
                    return
                logging.warning('capture thread crashed')
                self.thread = None
        else:
            logging.debug('capture thread terminated')
        return

    def run(self):
        logging.debug('start')
        self.capture.start()
        while self.active:
            im = self.capture.capture()
            if im is None:
                continue
            try:
                self.process(im.copy())
                if self.track:
                    self.do_track()
            except ValueError:
                pass

        logging.debug('stop')
        self.capture.stop()
        self.thread = None
        return