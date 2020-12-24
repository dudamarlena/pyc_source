# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/advancedcaching/fieldnotesuploader.py
# Compiled at: 2011-04-23 08:43:29
VERSION = 3
VERSION_DATE = '2010-07-03'
import geocaching, re, gobject, logging
logger = logging.getLogger('fieldnotesuploader')

class FieldnotesUploader(gobject.GObject):
    __gsignals__ = {'finished-uploading': (gobject.SIGNAL_RUN_FIRST,
                            gobject.TYPE_NONE,
                            ()), 
       'upload-error': (
                      gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,))}
    URL = 'http://www.geocaching.com/my/uploadfieldnotes.aspx'

    def __init__(self, downloader):
        gobject.GObject.__init__(self)
        self.downloader = downloader
        self.notes = []

    def add_fieldnote(self, geocache):
        if geocache.logdate == '':
            raise Exception('Illegal Date.')
        if geocache.logas == geocaching.GeocacheCoordinate.LOG_AS_FOUND:
            log = 'Found it'
        elif geocache.logas == geocaching.GeocacheCoordinate.LOG_AS_NOTFOUND:
            log = "Didn't find it"
        elif geocache.logas == geocaching.GeocacheCoordinate.LOG_AS_NOTE:
            log = 'Write note'
        else:
            raise Exception('Illegal status: %s' % geocache.logas)
        text = geocache.fieldnotes.replace('"', "'")
        self.notes.append('%s,%sT10:00Z,%s,"%s"' % (geocache.name, geocache.logdate, log, text))

    def upload(self):
        try:
            logger.info('Uploading fieldnotes...')
            page = self.downloader.get_reader(self.URL).read()
            m = re.search('<input type="hidden" name="__VIEWSTATE" id="__VIEWSTATE" value="([^"]+)" />', page)
            if m == None:
                raise Exception('Could not download fieldnotes page.')
            viewstate = m.group(1)
            text = ('\r\n').join(self.notes).encode('UTF-16')
            response = self.downloader.get_reader(self.URL, data=self.downloader.encode_multipart_formdata([
             ('ctl00$ContentBody$btnUpload', 'Upload Field Note'), ('ctl00$ContentBody$chkSuppressDate', ''), ('__VIEWSTATE', viewstate)], [
             (
              'ctl00$ContentBody$FieldNoteLoader', 'geocache_visits.txt', text)]))
            res = response.read()
            if 'successfully uploaded' not in res:
                raise Exception('Something went wrong while uploading the field notes.')
            else:
                self.emit('finished-uploading')
                logger.info('Finished upload')
        except Exception, e:
            self.emit('upload-error', e)

        return