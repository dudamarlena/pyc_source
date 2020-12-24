# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-intel/egg/scxml/compiler.py
# Compiled at: 2012-01-08 09:05:20
__doc__ = '\nThis file is part of pyscxml.\n\n    PySCXML is free software: you can redistribute it and/or modify\n    it under the terms of the GNU Lesser General Public License as published by\n    the Free Software Foundation, either version 3 of the License, or\n    (at your option) any later version.\n\n    PySCXML is distributed in the hope that it will be useful,\n    but WITHOUT ANY WARRANTY; without even the implied warranty of\n    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\n    GNU Lesser General Public License for more details.\n\n    You should have received a copy of the GNU Lesser General Public License\n    along with PySCXML.  If not, see <http://www.gnu.org/licenses/>.\n    \n    @author Johan Roxendal\n    @contact: johan@roxendal.com\n    \n'
from node import *
import re, sys
from functools import partial
from messaging import UrlGetter, get_path
from louie import dispatcher
from urllib2 import URLError
from eventlet.green.urllib2 import urlopen
from eventprocessor import Event, SCXMLEventProcessor as Processor
from invoke import *
from xml.parsers.expat import ExpatError
from threading import Timer
from StringIO import StringIO
from xml.etree import ElementTree
import textwrap, time
from datamodel import *
from errors import *
from eventlet import Queue
import scxml.pyscxml

def prepend_ns(tag):
    return '{%s}' % ns + tag


def split_ns(node):
    return node.tag[1:].split('}')


ns = 'http://www.w3.org/2005/07/scxml'
pyscxml_ns = 'http://code.google.com/p/pyscxml'
tagsForTraversal = ['scxml', 'state', 'parallel', 'history', 'final', 'transition', 'invoke', 'onentry', 'onexit', 'datamodel']
tagsForTraversal = map(prepend_ns, tagsForTraversal)
custom_exec_mapping = {}
preprocess_mapping = {}
datamodel_mapping = {'python': DataModel, 
   'ecmascript': ECMAScriptDataModel}

class Compiler(object):
    """The class responsible for compiling the statemachine"""

    def __init__(self):
        self.doc = SCXMLDocument()
        self.initData = {}
        self.script_src = {}
        self.log_function = None
        self.strict_parse = False
        self.timer_mapping = {}
        self.instantiate_datamodel = None
        self.default_datamodel = None
        return

    def setupDatamodel(self, datamodel):
        self.datamodel = datamodel
        self.doc.datamodel = datamodel_mapping[datamodel]()
        self.dm = self.doc.datamodel
        self.dm['_response'] = Queue()
        self.dm['_websocket'] = Queue()
        self.dm['__event'] = None
        return

    def parseAttr(self, elem, attr, default=None, is_list=False):
        if not elem.get(attr, elem.get(attr + 'expr')):
            return default
        else:
            try:
                output = elem.get(attr) or self.getExprValue(elem.get(attr + 'expr'), True)
            except ExprEvalError as e:
                raise AttributeEvalError(e, elem, attr + 'expr')

            if not is_list:
                return output
            return output.split(' ')

    def init_scripts(self, tree):
        scripts = tree.getiterator(prepend_ns('script'))
        scripts = filter(lambda x: x.get('src'), scripts)
        self.script_src = self.parallelize_download(scripts)
        failedList = filter(lambda x: isinstance(x[1], Exception), self.script_src.items())
        if not failedList:
            return
        linenums = map(lambda x: str(x[0].lineno), failedList)
        if len(linenums) > 2:
            linenums[:(-2)] = map(lambda x: x + ',', linenums[:-2])
        plur = ''
        if len(failedList) > 1:
            plur = 's'
            linenums[(-1):] = ['and', linenums[(-1)]]
        raise ScriptFetchError('Fetching remote script file%s failed on line%s %s.' % (plur, plur, (' ').join(linenums)))

    def try_execute_content(self, parent):
        try:
            self.do_execute_content(parent)
        except SendError as e:
            self.logger.error('Parsing of send node failed on line %s.' % e.elem.lineno)
            self.logger.error(str(e))
            self.raiseError('error.' + e.error_type, e, sendid=e.sendid)
        except (CompositeError, AtomicError) as e:
            getFirst = lambda x: x.exception if isinstance(x, AtomicError) else getFirst(x.exception)
            self.logger.error(e)
            self.raiseError('error.execution.' + type(getFirst(e)).__name__.lower(), e)
        except Exception as e:
            self.logger.exception('An unknown error occurred when executing content in block on line %s.' % parent.lineno)
            self.raiseError('error.execution', e)

    def do_execute_content(self, parent):
        """
        @param parent: usually an xml Element containing executable children
        elements, but can also be any iterator of executable elements. 
        """
        for node in parent:
            node_ns, node_name = split_ns(node)
            if node_ns == ns:
                if node_name == 'log':
                    try:
                        self.log_function(node.get('label'), self.getExprValue(node.get('expr'), True))
                    except ExprEvalError as e:
                        raise AttributeEvalError(e, node, 'expr')

                elif node_name == 'raise':
                    eventName = node.get('event').split('.')
                    self.interpreter.raiseFunction(eventName, {})
                elif node_name == 'send':
                    if not hasattr(node, 'id_n'):
                        node.id_n = 0
                    else:
                        node.id_n += 1
                    sendid = node.get('id', 'send_id_%s_%s' % (id(node), node.id_n))
                    try:
                        self.parseSend(node, sendid)
                    except AttributeEvalError:
                        raise
                    except (SendExecutionError, SendCommunicationError) as e:
                        raise SendError(e, node, e.type, sendid=sendid)
                    except Exception as e:
                        raise SendError(e, node, 'execution', sendid=sendid)

                elif node_name == 'cancel':
                    sendid = self.parseAttr(node, 'sendid')
                    if sendid in self.timer_mapping:
                        eventlet.greenthread.cancel(self.timer_mapping[sendid])
                        del self.timer_mapping[sendid]
                elif node_name == 'assign':
                    if not self.dm.hasLocation(node.get('location')):
                        msg = "The location expression '%s' was not instantiated in the datamodel." % node.get('location')
                        raise ExecutableError(IllegalLocationError(msg), node)
                    expression = node.get('expr') or node.text.strip()
                    try:
                        self.execExpr(node.get('location') + ' = ' + expression)
                    except ExprEvalError as e:
                        raise ExecutableError(e, node)

                elif node_name == 'script':
                    try:
                        src = node.text or self.script_src.get(node) or ''
                        self.execExpr(src)
                    except ExprEvalError as e:
                        raise ExecutableError(e, node)

                elif node_name == 'if':
                    self.parseIf(node)
                elif node_name == 'foreach':
                    try:
                        itr = enumerate(self.getExprValue(node.get('array'), True))
                    except ExprEvalError as e:
                        raise AttributeEvalError(e, node, 'array')
                    except TypeError as e:
                        err = DataModelError(e)
                        raise AttributeEvalError(err, node, 'array')

                    for index, item in itr:
                        try:
                            self.dm[node.get('item')] = item
                        except DataModelError as e:
                            raise AttributeEvalError(e, node, 'item')

                        try:
                            if node.get('index'):
                                self.dm[node.get('index')] = index
                        except DataModelError as e:
                            raise AttributeEvalError(e, node, 'index')

                        try:
                            self.do_execute_content(node)
                        except Exception as e:
                            raise ExecutableContainerError(e, node)

            elif node_ns == pyscxml_ns:
                if node_name == 'start_session':
                    xml = None
                    data = self.parseData(node, getContent=False)
                    contentNode = node.find(prepend_ns('content'))
                    if contentNode != None:
                        xml = self.parseContent(contentNode)
                    else:
                        if node.get('expr'):
                            xml = self.getExprValue('(%s)' % node.get('expr'))
                        elif self.parseAttr(node, 'src'):
                            xml = urlopen(self.parseAttr(node, 'src')).read()
                        try:
                            multisession = self.dm['_x']['sessions']
                            sm = multisession.make_session(self.parseAttr(node, 'sessionid'), xml)
                            sm.compiler.initData = data
                            sm.start_threaded()
                            timeout = self.parseCSSTime(node.get('timeout', '0s'))
                            if timeout:

                                def cancel():
                                    if not sm.isFinished():
                                        sm.cancel()

                                eventlet.spawn_after(timeout, cancel)
                        except AssertionError:
                            raise ExecutableError(node, 'You supplied no xml for <pyscxml:start_session /> and no default has been declared.')
                        except KeyError:
                            raise ExecutableError(node, 'You can only use the pyscxml:start_session element for documents in a MultiSession enviroment')

            elif node_ns in custom_exec_mapping:
                custom_exec_mapping[node_ns](node, self.dm)
            elif self.strict_parse:
                raise ExecutableError(node, "PySCXML doesn't recognize the executabel content '%s'" % node.tag)

        return

    def parseIf(self, node):

        def gen_prefixExec(itr):
            for elem in itr:
                if elem.tag not in map(prepend_ns, ['elseif', 'else']):
                    yield elem
                else:
                    break

        def gen_ifblock(ifnode):
            yield (
             ifnode, gen_prefixExec(ifnode))
            for elem in (x for x in ifnode if x.tag == prepend_ns('elseif') or x.tag == prepend_ns('else')):
                elemIndex = list(ifnode).index(elem)
                yield (elem, gen_prefixExec(ifnode[elemIndex + 1:]))

        for ifNode, execList in gen_ifblock(node):
            isElse = ifNode.tag == prepend_ns('else')
            if not isElse:
                try:
                    cond = self.getExprValue(ifNode.get('cond'), True)
                except ExprEvalError as e:
                    raise AttributeEvalError(e, ifNode, 'cond')

            try:
                if isElse:
                    self.do_execute_content(execList)
                    break
                elif cond:
                    self.do_execute_content(execList)
                    break
            except Exception as e:
                raise ExecutableContainerError(e, node)

    def parseData(self, child, getContent=True):
        """
        Given a parent node, returns a data object corresponding to 
        its param child nodes, namelist attribute or content child element.
        """
        contentNode = child.find(prepend_ns('content'))
        if getContent and contentNode != None:
            return self.parseContent(contentNode)
        else:
            output = {}
            for p in child.findall(prepend_ns('param')):
                expr = p.get('expr', p.get('location'))
                output[p.get('name')] = self.getExprValue(expr, True)

            if child.get('namelist'):
                for name in child.get('namelist').split(' '):
                    output[name] = self.getExprValue(name, True)

            return output

    def parseContent(self, contentNode):
        output = None
        if contentNode != None:
            if contentNode.get('expr'):
                output = self.getExprValue('(%s)' % contentNode.get('expr'), True)
            elif len(contentNode) == 0:
                output = contentNode.text
            elif len(contentNode) > 0:
                output = ElementTree.tostring(contentNode[0])
            else:
                self.logger.error('Line %s: error when parsing content node.' % contentNode.lineno)
                return
        return output

    def parseCSSTime(self, timestr):
        n, unit = re.search('(\\d+)(\\w+)', timestr).groups()
        assert unit in ('s', 'ms')
        if unit == 's':
            return float(n)
        return float(n) / 1000

    def parseSend(self, sendNode, sendid):
        if sendNode.get('idlocation'):
            if not self.dm.hasLocation(sendNode.get('idlocation')):
                msg = "The location expression '%s' was not instantiated in the datamodel." % sendNode.get('location')
                raise ExecutableError(IllegalLocationError(msg), sendNode)
            self.dm[sendNode.get('idlocation')] = sendid
        type = self.parseAttr(sendNode, 'type', 'scxml')
        event = self.parseAttr(sendNode, 'event').split('.') if self.parseAttr(sendNode, 'event') else None
        eventstr = ('.').join(event) if event else ''
        if not eventstr:
            raise SendExecutionError("Illegal send value: '%s'" % eventstr)
        target = self.parseAttr(sendNode, 'target')
        if target == '#_response':
            type = 'x-pyscxml-response'
        sender = None
        defaultSend = partial(self.interpreter.send, sendid=sendid if sendNode.get('id', sendNode.get('idlocation')) else None)
        try:
            data = self.parseData(sendNode)
        except ExprEvalError as e:
            self.logger.exception('Line %s: send not executed: parsing of data failed' % getattr(sendNode, 'lineno', 'unknown'))
            raise e

        scxmlSendType = ('http://www.w3.org/TR/scxml/#SCXMLEventProcessor', 'scxml')
        httpSendType = ('http://www.w3.org/TR/scxml/#BasicHTTPEventProcessor', 'basichttp')
        if (type in scxmlSendType or type in httpSendType) and not target:
            sender = partial(defaultSend, event, data)
        else:
            if isinstance(target, scxml.pyscxml.StateMachine):
                sendid = sendid if sendNode.get('id', sendNode.get('idlocation')) else None
                sender = partial(target.interpreter.send, event, data, sendid=sendid)
            elif type in scxmlSendType:
                if target == '#_parent':
                    sender = partial(defaultSend, event, data, self.interpreter.invokeId, toQueue=self.dm['_parent'])
                elif target == '#_internal':
                    self.interpreter.raiseFunction(event, data, sendid=sendid)
                elif target.startswith('#_scxml_'):
                    sessionid = target.split('#_scxml_')[(-1)]
                    try:
                        toQueue = self.dm['_x']['sessions'][sessionid].interpreter.externalQueue
                    except KeyError:
                        raise SendCommunicationError("The session '%s' is inaccessible." % sessionid)

                    sender = partial(defaultSend, event, data, toQueue=toQueue)
                elif target == '#_websocket':
                    self.logger.debug('sending to _websocket')
                    eventXML = Processor.toxml(eventstr, target, data, '', sendNode.get('id', ''), language='json')
                    sender = partial(self.dm['_websocket'].put, eventXML)
                elif target.startswith('#_') and not target == '#_response':
                    try:
                        sessionid = self.dm['_sessionid'] + '.' + target[2:]
                        sm = self.dm['_x']['sessions'][sessionid]
                    except KeyError:
                        e = SendCommunicationError("Line %s: No valid invoke target at '%s'." % (sendNode.lineno, sessionid))

                    sender = partial(sm.interpreter.send, event, data, sendid=sendid)
                elif target.startswith('http://'):
                    origin = 'unreachable'
                    if self.dm['_ioprocessors']['scxml']['location'].startswith('http://'):
                        origin = self.dm['_ioprocessors']['scxml']['location']
                    eventXML = Processor.toxml(eventstr, target, data, origin, sendNode.get('id', ''))
                    getter = self.getUrlGetter(target)
                    sender = partial(getter.get_async, target, eventXML, content_type='text/xml')
                else:
                    raise SendExecutionError("The send target '%s' is malformed or unsupported by the platform for the send type '%s'." % (
                     target, type))
            elif type in httpSendType:
                getter = self.getUrlGetter(target)
                sender = partial(getter.get_async, target, data)
            elif type == 'x-pyscxml-soap':
                sender = partial(self.dm[target[1:]].send, event, data)
            elif type == 'x-pyscxml-statemachine':
                try:
                    evt_obj = Event(event, data)
                    sender = partial(self.dm[target].send, evt_obj)
                except Exception:
                    raise SendExecutionError("No StateMachine instance at datamodel location '%s'" % target)

            elif type == 'x-pyscxml-response':
                self.logger.debug('sending to _response')
                headers = data.pop('headers') if 'headers' in data else {}
                data = Processor.toxml(eventstr, target, data, self.dm['_ioprocessors']['scxml']['location'], sendNode.get('id', ''), language='json')
                headers['Content-Type'] = 'text/xml'
                sender = partial(self.dm['_response'].put, (data, headers))
            else:
                raise SendExecutionError('The send type %s is invalid or unsupported by the platform' % type)
            delay = self.parseAttr(sendNode, 'delay', '0s')
            try:
                delay = self.parseCSSTime(delay)
            except (AttributeError, AssertionError):
                raise SendExecutionError('delay format error: the delay attribute should be specified using the CSS time format, you supplied the faulty value: %s' % delay)

        if delay:
            self.timer_mapping[sendid] = eventlet.spawn_after(delay, sender)
        else:
            sender()
        return

    def getUrlGetter(self, target):
        getter = UrlGetter()
        dispatcher.connect(self.onHttpResult, UrlGetter.HTTP_RESULT, getter)
        dispatcher.connect(self.onHttpError, UrlGetter.HTTP_ERROR, getter)
        dispatcher.connect(self.onURLError, UrlGetter.URL_ERROR, getter)
        return getter

    def onHttpError(self, signal, error_code, source, exception, **named):
        self.logger.error('A code %s HTTP error has ocurred when trying to send to target %s' % (error_code, source))
        self.interpreter.send('error.communication', data=exception)

    def onURLError(self, signal, sender, exception, url):
        print 'sender', url
        self.logger.error('The address %s is currently unavailable' % url)
        self.interpreter.send('error.communication', data=exception)

    def onHttpResult(self, signal, **named):
        self.logger.debug('onHttpResult ' + str(named))

    def raiseError(self, err, exception=None, sendid=None):
        self.interpreter.raiseFunction(err.split('.'), exception, sendid=sendid, type='platform')

    def parseXML(self, xmlStr, interpreterRef):
        self.interpreter = interpreterRef
        xmlStr = self.addDefaultNamespace(xmlStr)
        try:
            tree = xml_from_string(xmlStr)
        except ExpatError:
            xmlStr = ('\n').join('%s %s' % (n, line) for n, line in enumerate(xmlStr.split('\n')))
            self.logger.error(xmlStr)
            raise

        self.strict_parse = tree.get('exmode', 'lax') == 'strict'
        self.doc.binding = tree.get('binding', 'early')
        preprocess(tree)
        self.is_response = tree.get('{%s}%s' % (pyscxml_ns, 'response')) in ('true',
                                                                             'True')
        self.setupDatamodel(tree.get('datamodel', self.default_datamodel))
        self.instantiate_datamodel = partial(self.setDatamodel, tree)
        self.init_scripts(tree)
        for n, parent, node in iter_elems(tree):
            if parent != None and parent.get('id'):
                parentState = self.doc.getState(parent.get('id'))
            node_ns, node_tag = split_ns(node)
            if node_tag == 'scxml':
                s = State(node.get('id'), None, n)
                s.initial = self.parseInitial(node)
                self.doc.name = node.get('name', '')
                if 'name' in node.attrib:
                    self.dm['_name'] = node.get('name')
                for scriptChild in node.findall(prepend_ns('script')):
                    src = scriptChild.text or self.script_src.get(scriptChild, '') or ''
                    try:
                        self.execExpr(src)
                    except ExprEvalError as e:
                        self.logger.exception('An exception was raised in a top-level script element.')

                self.doc.rootState = s
            elif node_tag == 'state':
                s = State(node.get('id'), parentState, n)
                s.initial = self.parseInitial(node)
                self.doc.addNode(s)
                parentState.addChild(s)
            elif node_tag == 'parallel':
                s = Parallel(node.get('id'), parentState, n)
                self.doc.addNode(s)
                parentState.addChild(s)
            elif node_tag == 'final':
                s = Final(node.get('id'), parentState, n)
                self.doc.addNode(s)
                if node.find(prepend_ns('donedata')) != None:
                    doneNode = node.find(prepend_ns('donedata'))

                    def donedata():
                        try:
                            return self.parseData(doneNode)
                        except Exception as e:
                            self.logger.exception('Line %s: Donedata crashed.' % doneNode.lineno)
                            self.raiseError('error.execution', exception=e)

                        return {}

                    s.donedata = donedata
                else:
                    s.donedata = lambda : {}
                parentState.addFinal(s)
            elif node_tag == 'history':
                h = History(node.get('id'), parentState, node.get('type'), n)
                self.doc.addNode(h)
                parentState.addHistory(h)
            elif node_tag == 'transition':
                t = Transition(parentState)
                if node.get('target'):
                    t.target = node.get('target').split(' ')
                if node.get('event'):
                    t.event = map(lambda x: re.sub('(.*)\\.\\*$', '\\1', x).split('.'), node.get('event').split(' '))
                if node.get('cond'):
                    t.cond = partial(self.getExprValue, node.get('cond'))
                t.type = node.get('type', 'external')
                t.exe = partial(self.try_execute_content, node)
                parentState.addTransition(t)
            elif node_tag == 'invoke':
                parentState.addInvoke(self.make_invoke_wrapper(node, parentState.id, n))
            elif node_tag == 'onentry':
                s = Onentry()
                s.exe = partial(self.try_execute_content, node)
                parentState.addOnentry(s)
            elif node_tag == 'onexit':
                s = Onexit()
                s.exe = partial(self.try_execute_content, node)
                parentState.addOnexit(s)
            elif node_tag == 'datamodel':

                def initDatamodel(datalist):
                    try:
                        self.setDataList(datalist)
                    except Exception as e:
                        self.logger.exception('Evaluation of a data element failed.')

                parentState.initDatamodel = partial(initDatamodel, node.findall(prepend_ns('data')))
            else:
                self.logger.error("Parsing of element '%s' failed at line %s" % (node_tag, node.lineno or 'unknown'))

        return self.doc

    def execExpr(self, expr):
        if not expr or not expr.strip():
            return
        expr = normalizeExpr(expr)
        self.dm.execExpr(expr)

    def getExprValue(self, expr, throwErrors=False):
        """These expression are always one-line, so their value is evaluated and returned."""
        if not expr:
            return
        else:
            try:
                return self.dm.evalExpr(expr)
            except Exception as e:
                if throwErrors:
                    raise
                else:
                    self.logger.exception("Exception while evaluating expression: '%s'" % expr)
                    self.raiseError('error.execution.' + type(e).__name__.lower(), e)
                return

            return

    def make_invoke_wrapper(self, node, parentId, n):

        def start_invoke(wrapper):
            try:
                inv = self.parseInvoke(node, parentId, n)
            except Exception as e:
                self.logger.exception('Line %s: Exception while parsing invoke.' % node.lineno)
                self.raiseError('error.execution.invoke.' + type(e).__name__.lower(), e)
                return

            wrapper.set_invoke(inv)
            dispatcher.connect(self.onInvokeSignal, 'init.invoke.' + inv.invokeid, inv)
            dispatcher.connect(self.onInvokeSignal, 'result.invoke.' + inv.invokeid, inv)
            dispatcher.connect(self.onInvokeSignal, 'error.communication.invoke.' + inv.invokeid, inv)
            try:
                if isinstance(inv, InvokeSCXML):

                    def onCreated(sender, sm):
                        sessionid = sm.sessionid
                        self.dm['_x']['sessions'].make_session(sessionid, sm)

                    dispatcher.connect(onCreated, 'created', inv, weak=False)
                inv.start(self.interpreter.externalQueue)
            except Exception as e:
                self.logger.exception('Line %s: Exception while parsing invoke xml.' % node.lineno)
                self.raiseError('error.execution.invoke.' + type(e).__name__.lower(), e)

        wrapper = InvokeWrapper()
        wrapper.invoke = start_invoke
        wrapper.autoforward = node.get('autoforward', 'false').lower() == 'true'
        return wrapper

    def onInvokeSignal(self, signal, sender, **kwargs):
        self.logger.debug('onInvokeSignal ' + signal)
        if signal.startswith('error'):
            self.raiseError(signal, kwargs['data']['exception'])
            return
        self.interpreter.send(signal, data=kwargs.get('data', {}), invokeid=sender.invokeid)

    def parseInvoke(self, node, parentId, n):
        invokeid = node.get('id')
        if not invokeid:
            if not hasattr(node, 'id_n'):
                node.id_n = 0
            else:
                node.id_n += 1
            invokeid = '%s.%s.%s' % (parentId, n, node.id_n)
            if node.get('idlocation'):
                self.dm[node.get('idlocation')] = invokeid
        type = self.parseAttr(node, 'type', 'scxml')
        src = self.parseAttr(node, 'src')
        if src and src.startswith('file:'):
            newsrc, search_path = get_path(src.replace('file:', ''))
            if not newsrc:
                raise Exception('file not found when searching the PYTHONPATH: %s' % src)
            src = 'file:' + newsrc
        data = self.parseData(node, getContent=False)
        scxmlType = ['http://www.w3.org/TR/scxml', 'scxml']
        if type.strip('/') in scxmlType:
            inv = InvokeSCXML(data)
            contentNode = node.find(prepend_ns('content'))
            if contentNode != None:
                inv.content = self.parseContent(contentNode)
        elif type == 'x-pyscxml-soap':
            inv = InvokeSOAP()
        elif type == 'x-pyscxml-httpserver':
            inv = InvokeHTTP()
        else:
            raise NotImplementedError("The invoke type '%s' is not supported by the platform." % type)
        inv.invokeid = invokeid
        inv.parentSessionid = self.dm['_sessionid']
        inv.src = src
        inv.type = type
        inv.default_datamodel = self.default_datamodel
        finalizeNode = node.find(prepend_ns('finalize'))
        if finalizeNode != None and not len(finalizeNode):
            paramList = node.findall(prepend_ns('param'))
            namelist = filter(bool, map(lambda x: (x, x), node.get('namelist', '').split(' ')))
            paramMapping = [ (param.get('name'), param.get('location')) for param in (p for p in paramList if p.get('location')) ]

            def f():
                for name, location in namelist + paramMapping:
                    if name in self.dm['_event'].data:
                        self.dm[location] = self.dm['_event'].data[name]

            inv.finalize = f
        elif finalizeNode != None:
            inv.finalize = partial(self.try_execute_content, finalizeNode)
        return inv

    def parseInitial(self, node):
        if node.get('initial'):
            return Initial(node.get('initial').split(' '))
        else:
            if node.find(prepend_ns('initial')) is not None:
                transitionNode = node.find(prepend_ns('initial'))[0]
                assert transitionNode.get('target')
                initial = Initial(transitionNode.get('target').split(' '))
                initial.exe = partial(self.try_execute_content, transitionNode)
                return initial
            else:
                childNodes = filter(lambda x: x.tag in map(prepend_ns, ['state', 'parallel', 'final']), list(node))
                if childNodes:
                    return Initial([childNodes[0].get('id')])
                return

            return

    def setDatamodel(self, tree):
        for data in tree.getiterator(prepend_ns('data')):
            self.dm[data.get('id')] = None

        if tree.find(prepend_ns('datamodel')) is not None:
            try:
                self.setDataList(tree.find(prepend_ns('datamodel')))
            except Exception as e:
                raise ParseError('Parsing of data tag caused document startup to fail. \n%s' % e)

        if self.doc.binding == 'early':
            try:
                self.setDataList(tree.getiterator(prepend_ns('data')))
            except Exception as e:
                self.logger.exception('Evaluation of a data element failed.')

        for key, value in self.initData.items():
            if key in self.dm:
                self.dm[key] = value

        return

    def setDataList(self, datalist):
        dl_mapping = self.parallelize_download(filter(lambda x: x.get('src'), datalist))
        for node in datalist:
            key = node.get('id')
            value = None
            if node.get('expr'):
                try:
                    value = self.getExprValue('(%s)' % node.get('expr'), True)
                except Exception as e:
                    self.raiseError('error.execution', AttributeEvalError(e, node, 'expr'))

            elif node.get('src'):
                value = dl_mapping[node]
                if isinstance(value, Exception):
                    self.logger.error("Data src not found : '%s'. \n\t%s" % (node.get('src'), value))
                    value = None
            elif len(list(node)) == 1:
                value = ElementTree.tostring(list(node)[0])
            elif node.text and node.text.strip(' '):
                try:
                    value = self.dm.evalExpr(node.text)
                except:
                    raise ParseError('Parsing of inline data failed for data tag on line %s.' % node.lineno)

            self.dm[key] = value

        return

    def parallelize_download(self, nodelist):

        def download(node):
            src = node.get('src')
            if src.startswith('file:'):
                src, search_path = get_path(node.get('src').replace('file:', ''))
                if not src:
                    return (node, URLError('File not found: %s' % node.get('src')))
                src = 'file:' + src
            try:
                return (
                 node, urlopen(src).read())
            except Exception as e:
                return (node, e)

        pool = eventlet.greenpool.GreenPool()
        output = {}
        for node, result in pool.imap(download, nodelist):
            output[node] = result

        return output

    def addDefaultNamespace(self, xmlStr):
        if not ElementTree.fromstring(xmlStr).tag == '{http://www.w3.org/2005/07/scxml}scxml':
            self.logger.warn('Your document lacks the correct default namespace declaration. It has been added for you, for parsing purposes.')
            return xmlStr.replace('<scxml', "<scxml xmlns='http://www.w3.org/2005/07/scxml'", 1)
        return xmlStr


def preprocess(tree):
    tree.set('id', '__main__')
    toAppend = []
    for parent in tree.getiterator():
        for child in parent:
            node_ns, node_tag = split_ns(child)
            if node_ns in preprocess_mapping:
                xmlstr = preprocess_mapping[node_ns](child)
                i = list(parent).index(child)
                newNode = ElementTree.fromstring('<wrapper>%s</wrapper>' % xmlstr)
                for node in newNode:
                    if '{' not in node.tag:
                        node.set('xmlns', ns)

                newNode = ElementTree.fromstring(ElementTree.tostring(newNode))
                toAppend.append((parent, (i, len(newNode) - 1), newNode))

    for parent, (i, j), newNode in toAppend:
        parent[i:j] = newNode[:]

    for n, parent, node in iter_elems(tree):
        node_ns, node_tag = split_ns(node)
        if node_tag in ('state', 'parallel', 'final', 'history') and not node.get('id'):
            id = parent.get('id') + '_%s_child_%s' % (node_tag, n)
            node.set('id', id)


def normalizeExpr(expr):
    return textwrap.dedent(expr)


def iter_elems(tree):
    stack = [
     (
      None, tree)]
    n = 0
    while len(stack) > 0:
        parent, child = stack.pop()
        yield (n, parent, child)
        n += 1
        for elem in reversed(child):
            if elem.tag in tagsForTraversal:
                stack.append((child, elem))

    return


class FileWrapper(object):

    def __init__(self, source):
        self.source = source
        self.lineno = 0

    def read(self, bytes):
        s = self.source.readline()
        self.lineno += 1
        return s


def xml_from_string(xmlstr):
    f = FileWrapper(StringIO(xmlstr))
    root = None
    for event, elem in ElementTree.iterparse(f, events=('start', )):
        if root is None:
            root = elem
        elem.lineno = f.lineno

    return root