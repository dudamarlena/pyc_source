# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/will/projects/moya/moya/tags/system.py
# Compiled at: 2016-12-08 16:29:22
from __future__ import unicode_literals
from __future__ import print_function
from threading import Thread
import logging
try:
    import subprocess32 as subprocess
except ImportError:
    import subprocess

log = logging.getLogger(b'moya.runtime')
from ..context import Context
from ..context.missing import is_missing
from ..compat import iteritems, text_type
from ..elements.elementbase import Attribute
from ..tags.context import DataSetter, LogicElement
from .. import db
from ..__init__ import pilot

class MoyaThread(Thread):

    def __init__(self, element, app, name, context, data, join_timeout=None):
        super(MoyaThread, self).__init__(name=name)
        self.element = element
        self.app = app
        self.context = context
        self.data = data
        self.join_timeout = join_timeout
        self.libid = element.libid
        self._result = None
        self._error = None
        return

    def __repr__(self):
        return (b"<thread {} '{}'>").format(self.libid, self.name)

    def run(self):
        archive = self.element.archive
        with pilot.manage(self.context):
            try:
                self._result = archive.call_params(self.element.libid, self.context, self.app, self.data)
            except Exception as e:
                self.context[b'.console'].obj(self.context, e)
                self._error = e
                dbsessions = self.context[b'._dbsessions']
                if dbsessions:
                    db.rollback_sessions(self.context)

            dbsessions = self.context[b'._dbsessions']
            if dbsessions:
                db.commit_sessions(self.context)

    def wait(self):
        self.join(self.join_timeout)

    def __moyacontext__(self, context):
        self.join(self.join_timeout)
        if self.join_timeout:
            if self.is_alive():
                self.element.throw(b'thread.timeout', b'the thread failed to complete within timeout', thread=self)
        if self._error:
            self.element.throw(b'thread.fail', b'exception occurred in thread', diagnosis=(b"{!r} raised exception '{}'").format(self, self._error), original=self._error, thread=self)
        return self._result


class ThreadElement(DataSetter):
    """
    Run enclosed block in a thread.

    When Moya encounters this tag it executes the enclosed code in a new [url "https://en.wikipedia.org/wiki/Thread_(computing)"]thread[/url]. The calling thread will jump to the end of the [tag]thread[/tag] tag.

    The enclosed code may return a value (with [tag]return[/tag]), which can be retrieved by the calling thread via it's [c]dst[/c] parameter. If the calling thread references the return value before the thread has returned, it will block until the thread returns.

    This tag is useful in a request when you have some long running action to do, and you don't want to delay returning a response. Here's an example:

    [code xml]
    <view libname="view.process" template="slowprocess.html">
        <thread>
            <call macro="slow"/>
        </thread>
    </view>
    [/code]

    This view will render a template and return immediately, while the macro is processing in the background. Note, that the slow macro will have no way of returning anything in the response, but could still send an email or store something in the database to communicate the result to the user.

    """

    class Help:
        synopsis = b'run a thread'

    class Meta:
        tag_name = b'thread'

    name = Attribute(b'Name of thread', required=False, default=None)
    scope = Attribute(b'Use the current scope?', type=b'boolean', default=False)
    timeout = Attribute(b'Maximum time to wait for thread to complete', type=b'timespan', default=None)
    join = Attribute(b'Join threads before end of request?', type=b'boolean', default=False)

    def logic(self, context):
        params = self.get_parameters(context)
        thread_context = Context({k:v for k, v in iteritems(context.root) if not k.startswith(b'_') if not k.startswith(b'_')})
        if b'._dbsessions' in context:
            thread_context[b'._dbsessions'] = db.get_session_map(self.archive)
        data = {}
        if params.scope:
            data.update(context.capture_scope())
        data.update(self.get_let_map(context))
        for k, v in iteritems(data):
            if hasattr(v, b'_moyadb'):
                self.throw(b'thread.not-thread-safe', (b"thread parameter {} ('{}') may not be passed to a thread").format(context.to_expr(v), k), diagnosis=b'Database objects are not [i]thread safe[/i], try retrieving the object again inside the thread.')

        moya_thread = MoyaThread(self, context.get(b'.app', None), params.name or self.docname, thread_context, data=data, join_timeout=params.timeout)
        if params.join:
            context.set_new_call(b'._threads', list).append(moya_thread)
        moya_thread.start()
        self.set_context(context, params.dst, moya_thread)
        return


class WaitOnThreads(LogicElement):
    """
    Wait for threads to complete.

    This tag will will for all [tag]tread[/tag] tags with [c]join[/c] set to [c]yes[/c] to complete.

    """

    class Help:
        synopsis = b'wait threads to complete'

    def logic(self, context):
        for thread in context.get(b'._threads', []):
            thread.wait()

        context.safe_delete(b'._threads')


class SystemCall(DataSetter):
    """
    Call a system command and get output.

    Commands may be invoked in one of two ways; either with the [c]args[/c] attribute, which should be a list, or with the [c]shell[/c] attribute which should be a string to be passed to the shell. For example, the following two calls are equivalent:

    [code xml]
    <system-call shell="ls -al"/>
    [/code]
    [code xml]
    <system-call args="['ls', '-al']"/>
    [/code]

    The [c]args[/c] form is preferred because [c]shell[/c] is a potential security risk; if you don't escape parameters retrieved from a request it may be possible for a malicious use to execute code on your server.

    If the process returns a non-zero error code, then a [c]system-call.process-error[/c] exception is thrown. The [c]info[/c] value of the exception will contain [c]code[/c] and [c]output[/c].

    """

    class Help:
        synopsis = b'run a system command'
        example = b'\n        <system-call shell="ls -al" console="yes"/>\n        '

    class Meta:
        one_of = [
         ('shell', 'args')]

    args = Attribute(b'call arguments', type=b'expression', required=False)
    shell = Attribute(b'shell command', required=False)
    console = Attribute(b'write output to the console?', type=b'boolean', default=False, required=False)
    log = Attribute(b'write output to this log', default=None, required=False)
    output = Attribute(b'Destination for output', type=b'reference', default=None, required=False)

    def logic(self, context):
        params = self.get_parameters(context)
        console = context[b'.console']
        shell = False
        if self.has_parameter(b'args'):
            for arg in params.args:
                if is_missing(arg):
                    self.throw(b'bad-value.args', (b'args parameter must not contain missing values (args contains {})').format(context.to_expr(arg)))

            try:
                command = [ text_type(arg) for arg in params.args ]
            except:
                self.throw(b'bad-value.args', b'args parameter should be a list')

        else:
            command = params.shell
            shell = True

        def write_log(output, write):
            for line in output.splitlines():
                write(line)

        try:
            output = subprocess.check_output(command, shell=shell, stderr=subprocess.STDOUT, universal_newlines=True)
        except subprocess.CalledProcessError as e:
            return_code = e.returncode
            output = e.output
            if params.console and console:
                console(output)
            if params.log:
                write_log(output, logging.getLogger(params.log).error)
            self.throw(b'system-call.process-error', (b'system call returned non-zero code ({})').format(return_code), code=return_code, output=output)
        except OSError as e:
            self.throw(b'system-call.os-error', (b'system call failed ({})').format(e), errono=e.errno)

        if params.console and console:
            console(output)
        if params.log:
            write_log(output, logging.getLogger(params.log).info)
        if params.output:
            context[params.output] = output
        self.set_context(context, params.dst, output)