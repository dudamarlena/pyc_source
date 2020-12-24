# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/krikava/.python-virtenvs/omnigraffle-export/lib/python2.7/site-packages/omnigraffle_export/omnigraffle.py
# Compiled at: 2015-03-16 08:34:38
import logging, os
from appscript import *

class OmniGraffleSchema(object):
    """ A class that encapsulates an OmniGraffle schema file"""
    EXPORT_FORMATS = {'eps': 'EPS', 
       'pdf': 'PDF', 
       'png': 'PNG'}
    PDF_CHECKSUM_ATTRIBUTE = 'OmnigraffleExportChecksum: '

    def __init__(self, og, doc):
        self.og = og
        self.doc = doc
        self.path = doc.path()

    def sandboxed(self):
        return self.og.version()[0] == '6' and os.path.exists(os.path.expanduser(OmniGraffle.SANDBOXED_DIR_6))

    def get_canvas_list(self):
        """
        Returns a list of names of all the canvases in the document
        """
        return [ c.name() for c in self.doc.canvases() ]

    def export(self, canvasname, fname, format='pdf'):
        """
        Exports one canvas named `canvasname into `fname` using `format` format.
        """
        assert canvasname and len(canvasname) > 0, 'canvasname is missing'
        self.og.current_export_settings.area_type.set(k.all_graphics)
        if format not in OmniGraffleSchema.EXPORT_FORMATS:
            raise RuntimeError('Unknown format: %s' % format)
        canvas = [ c for c in self.doc.canvases() if c.name() == canvasname ]
        if len(canvas) == 1:
            canvas = canvas[0]
        else:
            raise RuntimeError('Canvas %s does not exist in %s' % (
             canvasname, self.doc.path()))
        self.og.windows.first().canvas.set(canvas)
        export_format = OmniGraffleSchema.EXPORT_FORMATS[format]
        export_path = fname
        if self.sandboxed():
            export_path = os.path.expanduser(OmniGraffle.SANDBOXED_DIR_6) + os.path.basename(fname)
            logging.debug('OmniGraffle is sandboxed - exporting to: %s' % export_path)
        if export_format == None:
            self.doc.save(in_=export_path)
        else:
            self.doc.save(as_=export_format, in_=export_path)
        if self.sandboxed():
            os.rename(export_path, fname)
            logging.debug('OmniGraffle is sandboxed - moving %s to: %s' % (export_path, fname))
        logging.debug("Exported `%s' into `%s' as %s" % (canvasname, fname, format))
        return

    def active_canvas_name(self):
        """
        Returns an active canvas name. The canvas that is currently selected in the the active OmniGraffle window.
        """
        window = self.og.windows.first()
        canvas = window.canvas()
        return canvas.name()


class OmniGraffle(object):
    SANDBOXED_DIR_6 = '~/Library/Containers/com.omnigroup.OmniGraffle6/Data/'

    def __init__(self):
        names = [
         'OmniGraffle 5.app', 'OmniGraffle Professional 5.app', 'OmniGraffle']
        self.og = None
        for name in names:
            try:
                self.og = app(name)
                break
            except ApplicationNotFoundError:
                continue

        if self.og == None:
            raise RuntimeError('Unable to connect to OmniGraffle (%s)' % (', ').join(names))
        return

    def active_document(self):
        self.og.activate()
        window = self.og.windows.first()
        doc = window.document()
        if doc == None:
            return
        else:
            fname = doc.path()
            if fname == None:
                fname = 'Untitled'
            logging.debug('Active OmniGraffle file: ' + fname)
            return OmniGraffleSchema(self.og, doc)

    def open(self, fname):
        fname = os.path.abspath(fname)
        if not os.path.isfile(fname) and not os.path.isfile(os.path.join(fname, 'data.plist')):
            raise ValueError('File: %s does not exists' % fname)
        fname = os.path.abspath(fname)
        self.og.activate()
        import subprocess
        subprocess.call(['open', fname])
        window = self.og.windows.first()
        doc = self.og.open(fname)
        logging.debug('Opened OmniGraffle file: ' + fname)
        return OmniGraffleSchema(self.og, doc)