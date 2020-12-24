# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./tests/test_event_hooks.py
# Compiled at: 2014-04-22 14:05:10
import os, time, testing, testify as T, catbox

class EventHooksTestCase(testing.BaseTestCase):

    def test_non_dictionary_event_hooks(self):
        self.run_child_function_in_catbox(event_hooks=None)
        return

    def test_invalid_event_hooks(self):
        event_hooks = {'child_initialized_hook': 'invalid_event_hook'}
        with T.assert_raises(TypeError):
            self.run_child_function_in_catbox(event_hooks=event_hooks)

    def test_successful_child_initialized_hook(self):
        expected_message_from_init_function = 'Init function is successful!'

        def child_initialized_hook(child_pid):
            os.write(self.write_pipe, expected_message_from_init_function)

        event_hooks = {'child_initialized': child_initialized_hook}
        self.run_child_function_in_catbox(event_hooks=event_hooks)
        self.verify_message_from_child(expected_message_from_init_function)

    def test_failing_child_initialized_hook(self):

        def child_initialized_hook(child_pid):
            raise Exception, 'child_initialized hook raises exception'

        pid = os.fork()
        if not pid:
            event_hooks = {'child_initialized': child_initialized_hook}
            with testing.no_stderr():
                self.run_child_function_in_catbox(event_hooks=event_hooks)
        else:
            status = 0
            wait_pid = 0
        try:
            for _ in range(5):
                (wait_pid, status, _) = os.wait4(pid, os.WNOHANG)
                if wait_pid == pid:
                    break
                time.sleep(0.1)

        except OSError, e:
            T.assert_in('No child processes', e)
        else:
            T.assert_not_equal(status, 0, 'Failing child_initialized hook did not make parent exit')

    def test_catbox_run_with_no_event_hooks(self):
        catbox.run(self.default_child_function)