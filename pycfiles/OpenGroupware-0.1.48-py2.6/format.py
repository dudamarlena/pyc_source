# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/workflow/formats/format.py
# Compiled at: 2012-10-12 07:02:39
import logging, inspect, pickle, yaml
from datetime import datetime
from time import sleep
from lxml import etree
from xml.sax.saxutils import escape, unescape
from coils.foundation import *
from coils.core import *
from exception import RecordFormatException
COILS_FORMAT_DESCRIPTION_OK = 0
COILS_FORMAT_DESCRIPTION_INCOMPLETE = -1

class Format(object):
    FORMATTERS = None

    def __init__(self):
        self.log = logging.getLogger('workflow')

    def set_description(self, fd):
        self._reject_file = None
        self._discard_on_error = False
        if 'name' in fd and 'class' in fd and 'data' in fd:
            self._chunk_size = int(fd.get('chunkSize', 1000))
            self._chunk_delay = float(fd.get('chunkDelay', 0.5))
            return (
             COILS_FORMAT_DESCRIPTION_OK, 'OK')
        else:
            return (
             COILS_FORMAT_DESCRIPTION_INCOMPLETE, 'Incomplete Description')
            return

    def pause(self, counter):
        if self._chunk_size == 0:
            return
        if counter % self._chunk_size == 0:
            sleep(self._chunk_delay)

    def load_description(self, name):
        filename = ('wf/f/{0}.pf').format(name)
        handle = BLOBManager.Open(filename, 'rb', encoding='binary')
        data = pickle.load(handle)
        BLOBManager.Close(handle)
        return self.set_description(data)

    def save(self):
        filename = ('wf/f/{0}.pf').format(self.description.get('name'))
        handle = BLOBManager.Create(filename, encoding='binary')
        pickle.dump(self.description, handle)
        BLOBManager.Close(handle)
        return True

    @property
    def mimetype(self):
        return 'application/xml'

    def get_name(self):
        return self.description.get('name')

    def encode_text(self, text):
        return escape(text)

    def decode_text(self, text):
        return unescape(text)

    def next_record(self):
        raise NotImplementedException()

    def process_record(self, record):
        raise NotImplementedException()

    @property
    def reject_buffer(self):
        if self._reject_file is None:
            self._reject_file = BLOBManager.ScratchFile()
        return self._reject_file

    def reject(self, data, message=None):
        self.reject_buffer.write(data)

    def process_in(self, rfile, wfile):
        self._input = rfile
        self._result = []
        wfile.write('<?xml version="1.0" encoding="UTF-8"?>')
        wfile.write(('<ResultSet formatName="{0}" className="{1}" tableName="{2}">').format(self.description.get('name'), self.__class__.__name__, self.description.get('tableName', '_undefined_')))
        counter = 0
        while True:
            record = self.next_record_in()
            counter += 1
            self.pause(counter)
            if record is None:
                break
            try:
                data = self.process_record_in(record)
            except RecordFormatException, e:
                self.reject(record)
                self.log.warn(('Record format exception on record {0}: {1}').format(self.in_counter, record))
                if self._discard_on_error:
                    self.log.info(('Record {0} of input message dropped due to format error').format(self.in_counter))
                else:
                    raise e
            else:
                if data is not None:
                    wfile.write(data)

        wfile.write('</ResultSet>')
        return

    def begin_output(self):
        pass

    def end_output(self):
        pass

    def as_yaml(self):
        return yaml.dump(self.description)

    def process_out(self, rfile, wfile):
        doc = etree.parse(rfile)
        self.begin_output()
        for record in doc.xpath('/ResultSet/row'):
            data = self.process_record_out(record)
            if data is not None:
                wfile.write(data)

        self.end_output()
        return

    @staticmethod
    def Create_Date_Value(date_string, in_format):
        return StandardXML.Create_Date_Value(date_string, in_format)

    @staticmethod
    def Reformat_Date_String(date_string, in_format, out_format):
        return StandardXML.Reformat_Date_String(date_string, in_format, out_format)

    @staticmethod
    def Load_Formatters():
        Format.FORMATTERS = {}
        bundle = __import__('coils.logic.workflow.formats', fromlist=['*'])
        for (name, data) in inspect.getmembers(bundle, inspect.isclass):
            if data.__module__[:len(bundle.__name__)] == bundle.__name__:
                if issubclass(data, Format):
                    logging.getLogger('workflow').info(('Format class {0} loaded').format(name))
                    Format.FORMATTERS[name] = data

    @staticmethod
    def Marshall(name):
        if Format.FORMATTERS is None:
            Format.Load_Formatters()
        if name in Format.FORMATTERS:
            return Format.FORMATTERS.get(name)()
        else:
            return

    @staticmethod
    def Load(name):
        filename = ('wf/f/{0}.pf').format(name)
        handle = BLOBManager.Open(filename, 'rb', encoding='binary')
        description = pickle.load(handle)
        BLOBManager.Close(handle)
        format = Format.Marshall(description.get('class'))
        code = format.set_description(description)
        if code[0] == COILS_FORMAT_DESCRIPTION_OK:
            return format
        raise CoilsException(code[1])

    @staticmethod
    def LoadYAML(name):
        format = Format.Load(name)
        return format.as_yaml()

    @staticmethod
    def Delete(name):
        return BLOBManager.Delete(('wf/f/{0}.pf').format(name))

    @staticmethod
    def ListFormats():
        result = []
        for name in BLOBManager.List('wf/f/'):
            result.append(name[:-3])

        return result