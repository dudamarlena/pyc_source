# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/bullseye/app.py
# Compiled at: 2012-03-03 20:44:32
from traits.trait_base import ETSConfig
if ETSConfig.toolkit == 'wx':
    from traitsui.wx import constants
    constants.WindowColor = constants.wx.NullColor
import optparse, logging, urlparse
from .process import Process
from .bullseye import Bullseye

def main():
    p = optparse.OptionParser(usage='%prog [options]')
    p.add_option('-c', '--camera', default='any:', help='camera uri (none:, any:, dc1394://guid/b09d01009981f9, fc2://index/1, replay://glob/beam*.npz) [%default]')
    p.add_option('-s', '--save', default=None, help="save images accordint to strftime() format string (e.g. 'beam_%Y%m%d%H%M%S.npz'), compressed npz format [%default]")
    p.add_option('-l', '--log', help='log output file [stderr]')
    p.add_option('-d', '--debug', default='info', help='log level (debug, info, warn, error, critical, fatal) [%default]')
    opts, args = p.parse_args()
    logging.basicConfig(filename=opts.log, level=getattr(logging, opts.debug.upper()), format='%(asctime)s %(levelname)s %(message)s')
    scheme, loc, path, query, frag = urlparse.urlsplit(opts.camera)
    if scheme == 'dc1394':
        from .dc1394_capture import DC1394Capture
        if loc == 'guid':
            cam = DC1394Capture(long(path[1:], base=16))
    elif scheme == 'fc2':
        from .flycapture2_capture import Fc2Capture
        if loc == 'index':
            cam = Fc2Capture(int(path[1:]))
    elif scheme == 'replay':
        from .replay_capture import ReplayCapture
        if loc == 'glob':
            cam = ReplayCapture(path[1:])
    elif scheme == 'none':
        from .capture import DummyCapture
        cam = DummyCapture()
    elif scheme == 'any':
        try:
            from .dc1394_capture import DC1394Capture
            cam = DC1394Capture()
        except Exception as e:
            logging.debug('dc1394 error: %s', e)
            try:
                from .flycapture2_capture import Fc2Capture
                cam = Fc2Capture()
            except Exception as e:
                logging.debug('flycapture2 error: %s', e)
                from .capture import DummyCapture
                cam = DummyCapture()

    logging.debug('running with capture device: %s', cam)
    if opts.save:
        cam.save_format = opts.save
    proc = Process(capture=cam)
    bull = Bullseye(process=proc)
    bull.configure_traits()
    bull.close()
    return


if __name__ == '__main__':
    main()