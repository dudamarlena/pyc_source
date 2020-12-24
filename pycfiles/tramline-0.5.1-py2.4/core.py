# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/tramline/core.py
# Compiled at: 2006-12-22 08:09:16
import os, tempfile, random, sys, errno

def tramline_path(req):
    return req.get_options()['tramline_path']


def tramline_upload_path(req):
    return os.path.join(tramline_path(req), 'upload')


def tramline_repository_path(req):
    return os.path.join(tramline_path(req), 'repository')


def create_paths(req):
    for p in [tramline_path(req), tramline_upload_path(req), tramline_repository_path(req)]:
        if not os.path.isdir(p):
            os.mkdir(p)


FILE_CHUNKSIZE = 8 * 1024

def inputfilter(filter):
    if filter.req.main is not None:
        filter.pass_on()
        return
    if filter.req.method != 'POST':
        filter.pass_on()
        return
    enctype = filter.req.headers_in.get('Content-Type')
    if enctype[:19] != 'multipart/form-data':
        filter.pass_on()
        return
    id = filter.req.headers_in.get('tramline_id')
    if id is None:
        processor = theProcessorRegistry.createProcessor()
        filter.req.headers_in['tramline_id'] = str(processor.id)
    else:
        processor = theProcessorRegistry.getProcessor(int(id))
    s = filter.read()
    while s:
        processor.pushInput(s, filter)
        s = filter.read()

    if s is not None:
        return
    processor.finalizeInput(filter)
    filter.close()
    return


def outputfilter(filter):
    if filter.req.main is not None:
        filter.pass_on()
        filter.flush()
        return
    if filter.req.method == 'POST':
        outputfilter_post(filter)
        return
    elif filter.req.method == 'GET':
        outputfilter_get(filter)
        return
    filter.pass_on()
    filter.flush()
    return


def outputfilter_post(filter):
    id = filter.req.headers_in.get('tramline_id')
    if id is None:
        filter.pass_on()
        filter.flush()
        return
    processor = theProcessorRegistry.getProcessor(int(id))
    is_ok = filter.req.headers_out.has_key('tramline_ok')
    if is_ok:
        processor.commit(filter.req)
    else:
        processor.abort()
    theProcessorRegistry.removeProcessor(processor)
    del filter.req.headers_in['tramline_id']
    filter.pass_on()
    filter.flush()
    return


def outputfilter_get(filter):
    if not filter.req.headers_out.has_key('tramline_file'):
        filter.pass_on()
        filter.flush()
        return
    data = []
    s = filter.read()
    while s:
        data.append(s)
        s = filter.read()

    file_id = ('').join(data)
    p = os.path.join(tramline_repository_path(filter.req), file_id)
    size = os.stat(p).st_size
    filter.req.headers_out['content-length'] = str(size)
    f = open(p, 'rb')
    while True:
        data = f.read(FILE_CHUNKSIZE)
        if not data:
            break
        filter.write(data)
        filter.flush()

    f.close()
    if s is None:
        filter.close()
    return


class ProcessorRegistry:
    __module__ = __name__

    def __init__(self):
        self._processors = {}

    def getProcessor(self, id):
        return self._processors[id]

    def createProcessor(self):
        while True:
            id = random.randrange(sys.maxint)
            if id not in self._processors:
                break

        result = self._processors[id] = Processor(id)
        return result

    def removeProcessor(self, processor):
        del self._processors[processor.id]


theProcessorRegistry = ProcessorRegistry()

class Processor:
    __module__ = __name__

    def __init__(self, id):
        self.id = id
        self._upload_files = []
        self._incoming = []
        self.handle = self.handle_first_boundary

    def pushInput(self, data, out):
        lines = data.splitlines(True)
        for line in lines:
            self.pushInputLine(line, out)

    def pushInputLine(self, data, out):
        self._incoming.append(data)
        if data[(-1)] != '\n':
            return
        if len(self._incoming) == 1:
            line = data
        else:
            line = ('').join(self._incoming)
        self._incoming = []
        self.handle(line, out)

    def finalizeInput(self, out):
        if self._upload_files:
            out.req.headers_in['tramline'] = ''

    def commit(self, req):
        for upload_file in self._upload_files:
            (dummy, filename) = os.path.split(upload_file)
            os.rename(upload_file, os.path.join(tramline_repository_path(req), filename))

    def abort(self):
        for upload_file in self._upload_files:
            os.remove(upload_file)

    def handle_first_boundary(self, line, out):
        self._boundary = line
        self._last_boundary = self._boundary.rstrip() + '--\r\n'
        self.init_headers()
        self.handle = self.handle_headers
        out.write(line)

    def init_headers(self):
        self._disposition = None
        self._disposition_options = {}
        self._content_type = 'text/plain'
        self._content_type_options = {}
        return

    def handle_headers(self, line, out):
        out.write(line)
        if line in ['\n', '\r\n']:
            self.init_data(out)
            return
        (key, value) = line.split(':', 1)
        key = key.lower()
        if key == 'content-disposition':
            (self._disposition, self._disposition_options) = parse_header(value)
        elif key == 'content-type':
            (self._content_type, self._content_type_options) = parse_header(value)

    def init_data(self, out):
        filename = self._disposition_options.get('filename')
        if filename is None or not filename:
            self.handle = self.handle_data
            return
        (fd, pathname, file_id) = createUniqueFile(out.req)
        self._f = os.fdopen(fd, 'wb')
        self._upload_files.append(pathname)
        out.write(file_id)
        out.write('\r\n')
        self._previous_line = None
        self.handle = self.handle_file_data
        return

    def handle_data(self, line, out):
        out.write(line)
        if line == self._boundary:
            self.init_headers()
            self.handle = self.handle_headers
        elif line == self._last_boundary:
            self.handle = None
        return

    def handle_file_data(self, line, out):
        if line == self._boundary:
            self._f.write(self._previous_line[:-2])
            out.write(line)
            self._f.close()
            self._f = None
            self.handle = self.handle_headers
        elif line == self._last_boundary:
            self._f.write(self._previous_line[:-2])
            out.write(line)
            self._f.close()
            self._f = None
            self.handle = None
        else:
            if self._previous_line is not None:
                self._f.write(self._previous_line)
            self._previous_line = line
        return


def parse_header(s):
    l = [ e.strip() for e in s.split(';') ]
    result_value = l.pop(0).lower()
    result_d = {}
    for e in l:
        try:
            (key, value) = e.split('=', 1)
        except ValueError:
            continue

        key = key.strip().lower()
        value = value.strip()
        if len(value) >= 2 and value.startswith('"') and value.endswith('"'):
            value = value[1:-1]
        result_d[key] = value

    return (
     result_value, result_d)


def createUniqueFile(req):
    """Create a file with unique file id in upload directory.

    Returns file descriptor, path, like tempfile.mkstemp, but in
    addition returns unique file id.
    """
    create_paths(req)
    while True:
        file_id = str(random.randrange(sys.maxint))
        if os.path.exists(os.path.join(tramline_repository_path(req), file_id)):
            continue
        path = os.path.join(tramline_upload_path(req), file_id)
        try:
            fd = os.open(path, tempfile._bin_openflags)
            tempfile._set_cloexec(fd)
            return (fd, path, file_id)
        except OSError, e:
            if e.errno == errno.EEXIST:
                continue
            raise


def log(data):
    f = open(os.path.join(tramline_path(), 'tramline.log'), 'ab')
    f.write(data)
    f.write('\n')
    f.close()