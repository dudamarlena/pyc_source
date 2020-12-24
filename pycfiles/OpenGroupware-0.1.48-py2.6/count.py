# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/workflow/actions/json/count.py
# Compiled at: 2012-10-12 07:02:39
try:
    import ijson
except:

    class CountJSONPathAction(object):
        pass


else:
    from coils.core.logic import ActionCommand

    class CountJSONPathAction(ActionCommand):
        __domain__ = 'action'
        __operation__ = 'count-json-path'
        __aliases__ = ['countJSONPathAction']

        def __init__(self):
            ActionCommand.__init__(self)

        def do_action(self):
            counter = 0
            for item in ijson.items(self.rfile, self._path):
                counter += 1

            self.wfile.write(str(counter))

        def parse_action_parameters(self):
            self._path = self.action_parameters.get('path')
            self._path = self.process_label_substitutions(self._path)

        def do_epilogue(self):
            pass