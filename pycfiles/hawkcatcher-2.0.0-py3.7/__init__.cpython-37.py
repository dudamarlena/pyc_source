# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/hawkcatcher/__init__.py
# Compiled at: 2020-03-16 07:58:41
# Size of source mod 2**32: 5229 bytes
import traceback, sys, time, requests, os

class Hawk:
    params = {}

    def __init__(self, settings):
        """
        Init Hawk Catcher class with params.
        Set exceptions hook.

        :param settings String|Dict: init params

        {String} settings = '1234567-abcd-8901-efgh-123456789012'
            Pass your project JWT token

        {Dictionary} settings = {
            'token': 'eyJhbGciOiJIUz<...>WyQPiqc',
                Project JWT token from Hawk
            'host': 'hawk.so',
                (optional) Hostname for your Hawk server
            'secure': True
                (optional) https or http
        }
        """
        if type(settings).__name__ == 'str':
            settings = {'token': settings}
        else:
            self.params = {'token':settings.get('token', ''),  'host':settings.get('host', 'hawk.so'), 
             'secure':settings.get('secure', True)}
            self.params['token'] or print('Token is missed. Check init params.')
            return
        self.params['url'] = 'http{}://{}/'.format('s' if self.params['secure'] else '', self.params['host'])
        sys.excepthook = self.handler

    def handler(self, exc_cls, exc, tb):
        """
        Catch, prepare and send error

        :param exc_cls: error class
        :param exc: exception
        :param tb: exception traceback
        """
        ex_message = traceback.format_exception_only(exc_cls, exc)[(-1)]
        ex_message = ex_message.strip()
        error_frame = tb
        while error_frame.tb_next is not None:
            error_frame = error_frame.tb_next

        file = error_frame.tb_frame.f_code.co_filename
        line = error_frame.tb_lineno
        stack = traceback.extract_tb(tb)
        backtrace = []
        for summary in stack:
            callee = {'file':os.path.abspath(summary[0]), 
             'line':summary[1], 
             'function':summary[2]}
            callee['sourceCode'] = self.get_near_filelines(callee['file'], callee['line'])
            backtrace.append(callee)

        backtrace = tuple(reversed(backtrace))
        event = {'token':self.params['token'], 
         'catcherType':'errors/python', 
         'payload':{'title':ex_message, 
          'backtrace':backtrace, 
          'headers':{},  'addons':{}}}
        try:
            r = requests.post((self.params['url']), json=event)
            response = r.content.decode('utf-8')
            print('[Hawk] Response: %s' % response)
        except Exception as e:
            try:
                print("[Hawk] Can't send error cause of %s" % e)
            finally:
                e = None
                del e

    def catch(self):
        """
        Exception processor
        """
        (self.handler)(*sys.exc_info())

    def get_near_filelines(self, filepath, line, margin=5):
        """
        Return part of file near the string with error

        :param filepath: path to file
        :param line: error line
        :param margin: get that number of strings above and below error
        :return trace: tuple
        """
        with open(filepath, 'r') as (file):
            content = file.readlines()
            content = [x.rstrip() for x in content]
        error_line_in_array = line - 1
        start = max(0, error_line_in_array - margin)
        end = min(len(content), error_line_in_array + margin + 1)
        trace = []
        index = 1
        lines = content[start:end]
        for array_line in range(start, end):
            trace.append({'line':array_line + 1, 
             'content':lines[array_line - start]})

        return trace