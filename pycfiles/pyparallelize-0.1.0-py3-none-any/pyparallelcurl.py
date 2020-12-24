# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/pyparallelcurl/pyparallelcurl.py
# Compiled at: 2010-10-13 13:53:38
import sys, pycurl, cStringIO, time
try:
    import signal
    from signal import SIGPIPE, SIG_IGN
    signal.signal(signal.SIGPIPE, signal.SIG_IGN)
except ImportError:
    pass

class ParallelCurl:
    max_requests = 10
    options = {}
    outstanding_requests = {}
    multi_handle = None

    def __init__(self, in_max_requests=10, in_options={}):
        self.max_requests = in_max_requests
        self.options = in_options
        self.outstanding_requests = {}
        self.multi_handle = pycurl.CurlMulti()

    def __del__(self):
        print 'self.max_requests=' + str(self.max_requests)
        self.finishallrequests()

    def setmaxrequests(self, in_max_requests):
        self.max_requests = in_max_requests

    def setoptions(self, in_options):
        self.options = in_options

    def startrequest(self, url, callback, user_data={}, post_fields=None):
        if self.max_requests > 0:
            self.waitforoutstandingrequeststodropbelow(self.max_requests)
        ch = pycurl.Curl()
        for (option, value) in self.options.items():
            ch.setopt(option, value)

        ch.setopt(pycurl.URL, url)
        result_buffer = cStringIO.StringIO()
        ch.setopt(pycurl.WRITEFUNCTION, result_buffer.write)
        if post_fields is not None:
            ch.setopt(pycurl.POST, True)
            ch.setopt(pycurl.POSTFIELDS, post_fields)
        self.multi_handle.add_handle(ch)
        self.outstanding_requests[ch] = {'handle': ch, 
           'result_buffer': result_buffer, 
           'url': url, 
           'callback': callback, 
           'user_data': user_data}
        self.checkforcompletedrequests()
        return

    def finishallrequests(self):
        self.waitforoutstandingrequeststodropbelow(1)

    def checkforcompletedrequests(self):
        if self.multi_handle.select(1.0) == -1:
            return
        else:
            while True:
                (ret, num_handles) = self.multi_handle.perform()
                if ret != pycurl.E_CALL_MULTI_PERFORM:
                    break

            while True:
                (num_q, ok_list, err_list) = self.multi_handle.info_read()
                for ch in ok_list:
                    if ch not in self.outstanding_requests:
                        raise RuntimeError("Error - handle wasn't found in requests: '" + str(ch) + "' in " + str(self.outstanding_requests))
                    request = self.outstanding_requests[ch]
                    url = request['url']
                    content = request['result_buffer'].getvalue()
                    callback = request['callback']
                    user_data = request['user_data']
                    callback(content, url, ch, user_data)
                    self.multi_handle.remove_handle(ch)
                    del self.outstanding_requests[ch]

                for (ch, errno, errmsg) in err_list:
                    if ch not in self.outstanding_requests:
                        raise RuntimeError("Error - handle wasn't found in requests: '" + str(ch) + "' in " + str(self.outstanding_requests))
                    request = self.outstanding_requests[ch]
                    url = request['url']
                    content = None
                    callback = request['callback']
                    user_data = request['user_data']
                    callback(content, url, ch, user_data)
                    self.multi_handle.remove_handle(ch)
                    del self.outstanding_requests[ch]

                if num_q < 1:
                    break

            return

    def waitforoutstandingrequeststodropbelow(self, max):
        while True:
            self.checkforcompletedrequests()
            if len(self.outstanding_requests) < max:
                break
            time.sleep(0.01)