# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/bill/py3/.virtualenvs/pytest/lib/python2.7/site-packages/Csys/ReportPrint.py
# Compiled at: 2009-11-25 02:34:45
import Csys, sys

class ReportPrint(Csys.CSClass):
    _attributes = dict(company='Celestial Software LLC', title='', title1='', progname=Csys.Config.progname, version='0.00', header1='', width=132, lefttitle='', period='', subtitle='', lasttitle='', pagelgth=66, printlgth=60, filehandle=sys.__stdout__, pageno=0, _curline=0, _uscore='')

    def __init__(self, **kwargs):
        Csys.CSClass.__init__(self, True, **kwargs)
        self._uscore = ' ' + '-' * self.width
        self._progver = '[%s,v %s]' % (self.progname, self.version)

    def fmtline(self, left, middle, right=''):
        """Formats line with left, centered, and right justified titles."""
        centerPosition = (self.width - len(middle)) / 2
        rightPosition = self.width - len(right)
        middleLength = rightPosition - centerPosition
        fmt = '%%-%ds%%-%ds%%s' % (centerPosition, middleLength)
        return fmt % (left, middle, right)

    def write(self, msg, need=1, numberlines=False):
        """Check for page overflow then write line"""
        if self._curline + need > self.printlgth:
            self.writeHeader()
        msg = str(msg).rstrip()
        lines = msg.split('\n')
        if len(lines) > 1:
            for line in lines:
                self.write(line, numberlines=numberlines)

        else:
            self._curline += 1
            msg = str(msg).rstrip()[:self.width]
            if numberlines:
                self.filehandle.write('%3d %s\n' % (self._curline, msg))
            else:
                self.filehandle.write('%s\n' % msg)

    def skip(self):
        """Skip to next page and print header"""
        if self._curline:
            linesrem = self.pagelgth - self._curline
            if linesrem > 0:
                self.filehandle.write('\n' * linesrem)
            self._curline = 0

    def writeHeader(self):
        """Print header"""
        self.skip()
        import time
        t = time.localtime(time.time())
        left = 'Date: ' + time.strftime('%m/%d/%Y', t)
        self.pageno += 1
        right = 'Page: %d' % self.pageno
        self.write(self.fmtline(left, self.company, right))
        left = 'Time: ' + time.strftime('%H:%M:%S', t)
        self.write(self.fmtline(left, self.title, self._progver))
        if self.title1 or self.lefttitle:
            self.write(self.fmtline(self.lefttitle, self.title1, ''))
            self.write('\n')
        if self.subtitle:
            self.write(self.fmtline('', self.subtitle, ''))
            self.write('\n')
        if self.lasttitle:
            self.write('')
            self.write(self.lasttitle)
        self.write(self._uscore)


from cStringIO import StringIO
_filehandle = StringIO()
_docPrint = ReportPrint(filehandle=_filehandle, company='Company Header', title='title', title1='title1', lefttitle='lefttitle', header1='header1', progname='progname', version='version', width=74, period='Period: xxx through yyy', subtitle='subtitle', lasttitle='lasttitle (left justified)')
_docPrint.writeHeader()
_doctxt = "\nReportPrint is a module to automatically generate printed\nheaders with sufficient information.\n\nUsage:\n    The ReportPrint class may be called with a variety of\n    keyword arguments.  The example below shows all options and\n    their default values.  Empty titles and subtitles will not\n    result in blank lines.\n\n    from Csys.ReportPrint import ReportPrint\n\n    printer = ReportPrint(\n        company     = 'Celestial Software LLC',\n        title       = '',\n        title1      = '',\n        progname    = Csys.Config.progname,\n        version     = '0.00',\n        header1     = '',\n        width       = 132,\n        lefttitle   = '',\n        period      = '',\n        subtitle    = '',\n        lasttitle   = '',\n        pagelgth    = 66,\n        printlgth   = 60,\n        filehandle  = sys.__stdout__,\n        pageno      = 0,\n    )\n\n    printer.writeHeader()\n    for someloop:\n        # ...\n        printer.write(msg, [need=lines], [numberlines=True])\n\nMethods:\n    write(msg, need=1, numberlines=False)\n\n        This writes the string msg, splitting on newlines to\n        properly keep track of line count.\n\n        The ``need'' paramter is the number of lines needed on\n        the page before printing the first line in msg.  This is\n        useful when writing reports where one wants to avoid\n        widow lines at the end of the page.\n\n        The ``numberlines'' paramter prints line numbers on ever\n        line of the page.  This may be useful for debugging or\n        forms generation.\n"
_docPrint.write(_doctxt)
_filehandle.seek(0)
__doc__ = ('\n').join([ line.rstrip() for line in _filehandle ])
if __name__ == '__main__':
    t = ReportPrint()
    print 'OK'
    print __doc__