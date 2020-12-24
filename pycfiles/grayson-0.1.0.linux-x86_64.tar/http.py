# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/scox/dev/grayson/venv/lib/python2.7/site-packages/net/http.py
# Compiled at: 2012-03-02 14:59:52
""" system """
import httplib, json, logging, socket, ssl, urllib2, pycurl, traceback

class GraysonHTTP:

    def __init__(self, uri):
        self.uri = uri

    def post_binary_file(self, field_name='data', file_name='data.zip', write_function=None, verbose=False):
        curl = pycurl.Curl()
        curl.setopt(curl.POST, 1)
        logging.info('URI: %s', self.uri)
        curl.setopt(curl.URL, self.uri)
        curl.setopt(curl.HTTPPOST, [
         (
          field_name,
          (
           curl.FORM_FILE, file_name))])
        if verbose:
            curl.setopt(curl.VERBOSE, 1)
        if write_function:

            def process_response(data):
                try:
                    try:
                        object = json.loads(data)
                        write_function(object)
                    except:
                        logging.error('========= HTTP ERROR ========== \n%s', data)
                        traceback.print_exc()

                finally:
                    pass

                return len(data)

            curl.setopt(curl.WRITEFUNCTION, process_response)
        curl.perform()
        curl.close()


__version__ = '0.1'
__all__ = ['GraysonHTTP']
__author__ = 'Steve Cox <scox@renci.org>'