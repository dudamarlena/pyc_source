# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/indra/ipc/webdav.py
# Compiled at: 2008-07-28 17:15:44
"""
@file webdav.py
@brief Classes to make manipulation of a webdav store easier.

$LicenseInfo:firstyear=2007&license=mit$

Copyright (c) 2007-2008, Linden Research, Inc.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
$/LicenseInfo$
"""
import sys, os, httplib, urlparse, socket, time, xml.dom.minidom, syslog
__revision__ = '0'
dav_debug = False

class DAVError(Exception):
    """ Base class for exceptions in this module. """
    __module__ = __name__

    def __init__(self, status=0, message='', body='', details=''):
        self.status = status
        self.message = message
        self.body = body
        self.details = details
        Exception.__init__(self, '%d:%s:%s%s' % (self.status, self.message, self.body, self.details))

    def print_to_stderr(self):
        """ print_to_stderr docstring """
        print >> sys.stderr, str(self.status) + ' ' + self.message
        print >> sys.stderr, str(self.details)


class Timeout(Exception):
    """ Timeout docstring """
    __module__ = __name__

    def __init__(self, arg=''):
        Exception.__init__(self, arg)


def alarm_handler(signum, frame):
    """ alarm_handler docstring """
    raise Timeout('caught alarm')


class WebDAV:
    """ WebDAV docstring """
    __module__ = __name__

    def __init__(self, url, proxy=None, retries_before_fail=6):
        self.init_url = url
        self.init_proxy = proxy
        self.retries_before_fail = retries_before_fail
        url_parsed = urlparse.urlsplit(url)
        self.top_path = url_parsed[2]
        if self.top_path == None or self.top_path == '':
            self.top_path = '/'
        elif len(self.top_path) > 1 and self.top_path[-1:] != '/':
            self.top_path += '/'
        if dav_debug:
            syslog.syslog('new WebDAV %s : %s' % (str(url), str(proxy)))
        if proxy:
            proxy_parsed = urlparse.urlsplit(proxy)
            self.host_header = url_parsed[1]
            host_and_port = proxy_parsed[1].split(':')
            self.host = host_and_port[0]
            if len(host_and_port) > 1:
                self.port = int(host_and_port[1])
            else:
                self.port = 80
        else:
            host_and_port = url_parsed[1].split(':')
            self.host_header = None
            self.host = host_and_port[0]
            if len(host_and_port) > 1:
                self.port = int(host_and_port[1])
            else:
                self.port = 80
        self.connection = False
        self.connect()
        return

    def log(self, msg, depth=0):
        """ log docstring """
        if dav_debug and depth == 0:
            host = str(self.init_url)
            if host == 'http://int.tuco.lindenlab.com:80/asset/':
                host = 'tuco'
            if host == 'http://harriet.lindenlab.com/asset-keep/':
                host = 'harriet/asset-keep'
            if host == 'http://harriet.lindenlab.com/asset-flag/':
                host = 'harriet/asset-flag'
            if host == 'http://harriet.lindenlab.com/asset/':
                host = 'harriet/asset'
            if host == 'http://ozzy.lindenlab.com/asset/':
                host = 'ozzy/asset'
            if host == 'http://station11.lindenlab.com:12041/:':
                host = 'station11:12041'
            proxy = str(self.init_proxy)
            if proxy == 'None':
                proxy = ''
            if proxy == 'http://int.tuco.lindenlab.com:3128/':
                proxy = 'tuco'
            syslog.syslog('WebDAV (%s:%s) %s' % (host, proxy, str(msg)))

    def connect(self):
        """ connect docstring """
        self.log('connect')
        self.connection = httplib.HTTPConnection(self.host, self.port)

    def __err(self, response, details):
        """ __err docstring """
        raise DAVError(response.status, response.reason, response.read(), str(self.init_url) + ':' + str(self.init_proxy) + ':' + str(details))

    def request(self, method, path, body=None, headers=None, read_all=True, body_hook=None, recurse=0, allow_cache=True):
        """ request docstring """
        if headers == None:
            headers = {}
        if not allow_cache:
            headers['Pragma'] = 'no-cache'
            headers['cache-control'] = 'no-cache'
        try:
            if method.lower() != 'purge':
                if path.startswith('/'):
                    path = path[1:]
                if self.host_header:
                    headers['host'] = self.host_header
                    fullpath = 'http://%s%s%s' % (self.host_header, self.top_path, path)
                else:
                    fullpath = self.top_path + path
            else:
                fullpath = path
            self.connection.request(method, fullpath, body, headers)
            if body_hook:
                body_hook()
            response = self.connection.getresponse()
            if read_all:
                while len(response.read(1024)) > 0:
                    pass

            if (response.status == 500 or response.status == 503 or response.status == 403) and recurse < self.retries_before_fail:
                return self.retry_request(method, path, body, headers, read_all, body_hook, recurse)
            return response
        except (httplib.ResponseNotReady, httplib.BadStatusLine, socket.error):
            if recurse < self.retries_before_fail:
                return self.retry_request(method, path, body, headers, read_all, body_hook, recurse)
            raise DAVError(0, 'reconnect failed', self.host, (
             method, path, body, headers, recurse))

        return

    def retry_request(self, method, path, body, headers, read_all, body_hook, recurse):
        """ retry_request docstring """
        time.sleep(10.0 * recurse)
        self.connect()
        return self.request(method, path, body, headers, read_all, body_hook, recurse + 1)

    def propfind(self, path, body=None, depth=1):
        """ propfind docstring """
        headers = {'Content-Type': 'text/xml; charset="utf-8"', 'Depth': str(depth)}
        response = self.request('PROPFIND', path, body, headers, False)
        if response.status == 207:
            return response
        self.__err(response, ('PROPFIND', path, body, headers, 0))

    def purge(self, path):
        """ issue a squid purge command """
        headers = {'Accept': '*/*'}
        response = self.request('PURGE', path, None, headers)
        if response.status == 200 or response.status == 404:
            return response
        self.__err(response, ('PURGE', path, None, headers))
        return

    def get_file_size(self, path):
        """
        Use propfind to ask a webdav server what the size of
        a file is.  If used on a directory (collection) return 0
        """
        self.log('get_file_size %s' % path)
        nsurl = 'http://apache.org/dav/props/'
        doc = xml.dom.minidom.Document()
        propfind_element = doc.createElementNS(nsurl, 'D:propfind')
        propfind_element.setAttributeNS(nsurl, 'xmlns:D', 'DAV:')
        doc.appendChild(propfind_element)
        prop_element = doc.createElementNS(nsurl, 'D:prop')
        propfind_element.appendChild(prop_element)
        con_len_element = doc.createElementNS(nsurl, 'D:getcontentlength')
        prop_element.appendChild(con_len_element)
        response = self.propfind(path, doc.toxml())
        doc.unlink()
        resp_doc = xml.dom.minidom.parseString(response.read())
        cln = resp_doc.getElementsByTagNameNS('DAV:', 'getcontentlength')[0]
        try:
            content_length = int(cln.childNodes[0].nodeValue)
        except IndexError:
            return 0

        resp_doc.unlink()
        return content_length

    def file_exists(self, path):
        """
        do an http head on the given file.  return True if it succeeds
        """
        self.log('file_exists %s' % path)
        expect_gzip = path.endswith('.gz')
        response = self.request('HEAD', path)
        got_gzip = response.getheader('Content-Encoding', '').strip()
        if got_gzip.lower() == 'x-gzip' and expect_gzip == False:
            return False
        return response.status == 200

    def mkdir(self, path):
        """ mkdir docstring """
        self.log('mkdir %s' % path)
        headers = {}
        response = self.request('MKCOL', path, None, headers)
        if response.status == 201:
            return
        if response.status == 405:
            return
        self.__err(response, ('MKCOL', path, None, headers, 0))
        return

    def delete(self, path):
        """ delete docstring """
        self.log('delete %s' % path)
        headers = {'Depth': 'infinity'}
        response = self.request('DELETE', path, None, headers)
        if response.status == 204:
            return
        if response.status == 404:
            return
        self.__err(response, ('DELETE', path, None, headers, 0))
        return

    def list_directory(self, path, dir_filter=None, allow_cache=True, minimum_cache_time=False):
        """
        Request an http directory listing and parse the filenames out of lines
        like: '<LI><A HREF="X"> X</A>'. If a filter function is provided,
        only return filenames that the filter returns True for.

        This is sort of grody, but it seems faster than other ways of getting
        this information from an isilon.
        """
        self.log('list_directory %s' % path)

        def try_match(lline, before, after):
            """ try_match docstring """
            try:
                blen = len(before)
                asset_start_index = lline.index(before)
                asset_end_index = lline.index(after, asset_start_index + blen)
                asset = line[asset_start_index + blen:asset_end_index]
                if not dir_filter or dir_filter(asset):
                    return [
                     asset]
                return []
            except ValueError:
                return []

        if len(path) > 0 and path[-1:] != '/':
            path += '/'
        response = self.request('GET', path, None, {}, False, allow_cache=allow_cache)
        if allow_cache and minimum_cache_time:
            print response.getheader('Date')
        if response.status != 200:
            self.__err(response, ('GET', path, None, {}, 0))
        assets = []
        for line in response.read().split('\n'):
            lline = line.lower()
            if lline.find('parent directory') == -1:
                assets += try_match(lline, '<li><a href="', '"> ')
                assets += try_match(lline, 'alt="[dir]"> <a href="', '/">')
                assets += try_match(lline, 'alt="[   ]"> <a href="', '">')

        return assets

    def __tmp_filename(self, path_and_file):
        """ __tmp_filename docstring """
        (head, tail) = os.path.split(path_and_file)
        if head != '':
            return head + '/.' + tail + '.' + str(os.getpid())
        else:
            return head + '.' + tail + '.' + str(os.getpid())

    def __put__(self, filesize, body_hook, remotefile):
        """ __put__ docstring """
        headers = {'Content-Length': str(filesize)}
        remotefile_tmp = self.__tmp_filename(remotefile)
        response = self.request('PUT', remotefile_tmp, None, headers, True, body_hook)
        if response.status not in (201, 204):
            self.__err(response, ('PUT', remotefile, None, headers, 0))
        if filesize != self.get_file_size(remotefile_tmp):
            try:
                self.delete(remotefile_tmp)
            except:
                pass
            else:
                raise DAVError(0, 'tmp upload error', remotefile_tmp)
        try:
            self.rename(remotefile_tmp, remotefile)
        except DAVError, exc:
            if exc.status == 403:
                try:
                    self.delete(remotefile_tmp)
                except:
                    pass

            raise

        if filesize != self.get_file_size(remotefile):
            raise DAVError(0, 'file upload error', str(remotefile_tmp))
        return

    def put_string(self, strng, remotefile):
        """ put_string docstring """
        self.log('put_string %d -> %s' % (len(strng), remotefile))
        filesize = len(strng)

        def body_hook():
            """ body_hook docstring """
            self.connection.send(strng)

        self.__put__(filesize, body_hook, remotefile)

    def put_file(self, localfile, remotefile):
        """
        Send a local file to a remote webdav store.  First, upload to
        a temporary filename.  Next make sure the file is the size we
        expected.  Next, move the file to its final location.  Next,
        check the file size at the final location.
        """
        self.log('put_file %s -> %s' % (localfile, remotefile))
        filesize = os.path.getsize(localfile)

        def body_hook():
            """ body_hook docstring """
            handle = open(localfile)
            while True:
                data = handle.read(1300)
                if len(data) == 0:
                    break
                self.connection.send(data)

            handle.close()

        self.__put__(filesize, body_hook, remotefile)

    def create_empty_file(self, remotefile):
        """ create an empty file """
        self.log('touch_file %s' % remotefile)
        headers = {'Content-Length': '0'}
        response = self.request('PUT', remotefile, None, headers)
        if response.status not in (201, 204):
            self.__err(response, ('PUT', remotefile, None, headers, 0))
        if self.get_file_size(remotefile) != 0:
            raise DAVError(0, 'file upload error', str(remotefile))
        return

    def __get_file_setup(self, remotefile, check_size=True):
        """ __get_file_setup docstring """
        if check_size:
            remotesize = self.get_file_size(remotefile)
        response = self.request('GET', remotefile, None, {}, False)
        if response.status != 200:
            self.__err(response, ('GET', remotefile, None, {}, 0))
        try:
            content_length = int(response.getheader('Content-Length'))
        except TypeError:
            content_length = None

        if check_size:
            if content_length != remotesize:
                raise DAVError(0, 'file DL size error', remotefile)
        return (
         response, content_length)

    def __get_file_read--- This code section failed: ---

 L. 466         0  LOAD_FAST             3  'content_length'
                3  LOAD_CONST               None
                6  COMPARE_OP            3  !=
                9  JUMP_IF_FALSE       150  'to 162'
               12  POP_TOP          

 L. 467        13  LOAD_CONST               0
               16  STORE_FAST            4  'so_far_length'

 L. 468        19  SETUP_LOOP          104  'to 126'
               22  LOAD_FAST             4  'so_far_length'
               25  LOAD_FAST             3  'content_length'
               28  COMPARE_OP            0  <
               31  JUMP_IF_FALSE        90  'to 124'
               34  POP_TOP          

 L. 469        35  LOAD_FAST             2  'response'
               38  LOAD_ATTR             4  'read'
               41  LOAD_FAST             3  'content_length'
               44  LOAD_FAST             4  'so_far_length'
               47  BINARY_SUBTRACT  
               48  CALL_FUNCTION_1       1  None
               51  STORE_FAST            5  'data'

 L. 470        54  LOAD_GLOBAL           6  'len'
               57  LOAD_FAST             5  'data'
               60  CALL_FUNCTION_1       1  None
               63  LOAD_CONST               0
               66  COMPARE_OP            2  ==
               69  JUMP_IF_FALSE        19  'to 91'
             72_0  THEN                     92
               72  POP_TOP          

 L. 471        73  LOAD_GLOBAL           7  'DAVError'
               76  LOAD_CONST               0
               79  LOAD_CONST               'short file download'
               82  CALL_FUNCTION_2       2  None
               85  RAISE_VARARGS_1       1  None
               88  JUMP_FORWARD          1  'to 92'
             91_0  COME_FROM            69  '69'
               91  POP_TOP          
             92_0  COME_FROM            88  '88'

 L. 472        92  LOAD_FAST             4  'so_far_length'
               95  LOAD_GLOBAL           6  'len'
               98  LOAD_FAST             5  'data'
              101  CALL_FUNCTION_1       1  None
              104  INPLACE_ADD      
              105  STORE_FAST            4  'so_far_length'

 L. 473       108  LOAD_FAST             1  'writehandle'
              111  LOAD_ATTR             9  'write'
              114  LOAD_FAST             5  'data'
              117  CALL_FUNCTION_1       1  None
              120  POP_TOP          
              121  JUMP_BACK            22  'to 22'
              124  POP_TOP          
              125  POP_BLOCK        
            126_0  COME_FROM            19  '19'

 L. 474       126  SETUP_LOOP           98  'to 227'
              129  LOAD_GLOBAL           6  'len'
              132  LOAD_FAST             2  'response'
              135  LOAD_ATTR             4  'read'
              138  CALL_FUNCTION_0       0  None
              141  CALL_FUNCTION_1       1  None
              144  LOAD_CONST               0
              147  COMPARE_OP            4  >
              150  JUMP_IF_FALSE         4  'to 157'
              153  POP_TOP          

 L. 475       154  CONTINUE            129  'to 129'
              157  POP_TOP          
              158  POP_BLOCK        
              159  JUMP_FORWARD         65  'to 227'
            162_0  COME_FROM             9  '9'
              162  POP_TOP          

 L. 477       163  SETUP_LOOP           61  'to 227'
              166  LOAD_GLOBAL          10  'True'
              169  JUMP_IF_FALSE        53  'to 225'
              172  POP_TOP          

 L. 478       173  LOAD_FAST             2  'response'
              176  LOAD_ATTR             4  'read'
              179  CALL_FUNCTION_0       0  None
              182  STORE_FAST            5  'data'

 L. 479       185  LOAD_GLOBAL           6  'len'
              188  LOAD_FAST             5  'data'
              191  CALL_FUNCTION_1       1  None
              194  LOAD_CONST               1
              197  COMPARE_OP            0  <
              200  JUMP_IF_FALSE         5  'to 208'
            203_0  THEN                     209
              203  POP_TOP          

 L. 480       204  BREAK_LOOP       
              205  JUMP_FORWARD          1  'to 209'
            208_0  COME_FROM           200  '200'
              208  POP_TOP          
            209_0  COME_FROM           205  '205'

 L. 481       209  LOAD_FAST             1  'writehandle'
              212  LOAD_ATTR             9  'write'
              215  LOAD_FAST             5  'data'
              218  CALL_FUNCTION_1       1  None
              221  POP_TOP          
              222  JUMP_BACK           166  'to 166'
              225  POP_TOP          
              226  POP_BLOCK        
            227_0  COME_FROM           163  '163'
            227_1  COME_FROM           126  '126'
              227  LOAD_CONST               None
              230  RETURN_VALUE     

Parse error at or near `POP_TOP' instruction at offset 157

    def get_file(self, remotefile, localfile, check_size=True):
        """
        Get a remote file from a webdav server.  Download to a local
        tmp file, then move into place.  Sanity check file sizes as
        we go.
        """
        self.log('get_file %s -> %s' % (remotefile, localfile))
        (response, content_length) = self.__get_file_setup(remotefile, check_size)
        localfile_tmp = self.__tmp_filename(localfile)
        handle = open(localfile_tmp, 'w')
        self.__get_file_read(handle, response, content_length)
        handle.close()
        if check_size:
            if content_length != os.path.getsize(localfile_tmp):
                raise DAVError(0, 'file DL size error', remotefile + ',' + localfile)
        os.rename(localfile_tmp, localfile)

    def get_file_as_string(self, remotefile, check_size=True):
        """
        download a file from a webdav server and return it as a string.
        """
        self.log('get_file_as_string %s' % remotefile)
        (response, content_length) = self.__get_file_setup(remotefile, check_size)
        tmp_handle = os.tmpfile()
        self.__get_file_read(tmp_handle, response, content_length)
        tmp_handle.seek(0)
        ret = tmp_handle.read()
        tmp_handle.close()
        return ret

    def get_post_as_string(self, remotefile, body):
        """
        Do an http POST, send body, get response and return it.
        """
        self.log('get_post_as_string %s' % remotefile)
        headers = {'Content-Type': 'text/xml; charset="utf-8"'}
        response = self.request('POST', remotefile, body, headers, False)
        if response.status != 200:
            self.__err(response, ('POST', remotefile, body, headers, 0))
        try:
            content_length = int(response.getheader('Content-Length'))
        except TypeError:
            content_length = None

        tmp_handle = os.tmpfile()
        self.__get_file_read(tmp_handle, response, content_length)
        tmp_handle.seek(0)
        ret = tmp_handle.read()
        tmp_handle.close()
        return ret

    def __destination_command(self, verb, remotesrc, dstdav, remotedst):
        """
        self and dstdav should point to the same http server.
        """
        if len(remotedst) > 0 and remotedst[0] == '/':
            remotedst = remotedst[1:]
        headers = {'Destination': 'http://%s:%d%s%s' % (dstdav.host, dstdav.port, dstdav.top_path, remotedst)}
        response = self.request(verb, remotesrc, None, headers)
        if response.status == 201:
            return
        if response.status == 204:
            return
        self.__err(response, (verb, remotesrc, None, headers, 0))
        return

    def rename(self, remotesrc, remotedst):
        """ rename a file on a webdav server """
        self.log('rename %s -> %s' % (remotesrc, remotedst))
        self.__destination_command('MOVE', remotesrc, self, remotedst)

    def xrename(self, remotesrc, dstdav, remotedst):
        """ rename a file on a webdav server """
        self.log('xrename %s -> %s' % (remotesrc, remotedst))
        self.__destination_command('MOVE', remotesrc, dstdav, remotedst)

    def copy(self, remotesrc, remotedst):
        """ copy a file on a webdav server """
        self.log('copy %s -> %s' % (remotesrc, remotedst))
        self.__destination_command('COPY', remotesrc, self, remotedst)

    def xcopy(self, remotesrc, dstdav, remotedst):
        """ copy a file on a webdav server """
        self.log('xcopy %s -> %s' % (remotesrc, remotedst))
        self.__destination_command('COPY', remotesrc, dstdav, remotedst)


def put_string(data, url):
    """
    upload string s to a url
    """
    url_parsed = urlparse.urlsplit(url)
    dav = WebDAV('%s://%s/' % (url_parsed[0], url_parsed[1]))
    dav.put_string(data, url_parsed[2])


def get_string(url, check_size=True):
    """
    return the contents of a url as a string
    """
    url_parsed = urlparse.urlsplit(url)
    dav = WebDAV('%s://%s/' % (url_parsed[0], url_parsed[1]))
    return dav.get_file_as_string(url_parsed[2], check_size)