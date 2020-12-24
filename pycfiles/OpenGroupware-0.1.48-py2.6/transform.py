# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/workflow/actions/xml/transform.py
# Compiled at: 2012-10-12 07:02:39
import os, base64
from lxml import etree
from coils.core import *
from coils.core.logic import ActionCommand
from extentions import OIEXSLTExtensionPoints
from coils.logic.workflow import XSLTDocument

class TransformAction(ActionCommand):
    __domain__ = 'action'
    __operation__ = 'transform'
    __aliases__ = ['transformAction']

    def __init__(self):
        ActionCommand.__init__(self)

    @property
    def result_mimetype(self):
        return self._output_mimetype

    def do_action(self):
        oie_extentions = OIEXSLTExtensionPoints(context=self._ctx, process=self.process, scope=self.scope_stack, ctxids=self._ctx_ids)
        extensions = etree.Extension(oie_extentions, ('sequencereset', 'sequencevalue',
                                                      'sequenceincrement', 'messagetext',
                                                      'searchforobjectid', 'tablelookup',
                                                      'reformatdate', 'datetimetodate',
                                                      'stringtodate', 'stringtodate',
                                                      'xattrvalue', 'countobjects',
                                                      'getpid', 'month', 'year',
                                                      'monthstart', 'monthend', 'today',
                                                      'yesterday', 'tomorrow', 'dateplusdays',
                                                      'days', 'weekdays', 'replace'), ns='http://www.opengroupware.us/oie')
        source = etree.parse(self.rfile)
        self.log.debug(('Template is {0}b').format(len(self._xslt)))
        xslt = etree.XSLT(etree.XML(self._xslt), extensions=extensions)
        self.wfile.write(unicode(xslt(source)))
        oie_extentions.shutdown()

    def parse_action_parameters(self):
        self._b64 = self.action_parameters.get('isBase64', 'NO').upper()
        xslt_string = self.action_parameters.get('xslt', None)
        xslt_name = self.action_parameters.get('template', None)
        if xslt_string:
            if self._b64 == 'YES':
                self.log_message('Base64 encoded inline template', category='debug')
                self._xslt = base64.decodestring(xslt_string.strip())
            else:
                self.log_message('Native inline template', category='debug')
                self._xslt = self.decode_text(xslt_string)
        elif xslt_name:
            self.log_message(('Loading XSLT template named "{0}"').format(xslt_name), category='debug')
            stylesheet = XSLTDocument(xslt_name)
            if stylesheet:
                handle = stylesheet.read_handle
                if handle:
                    self._xslt = handle.read()
                    BLOBManager.Close(handle)
                else:
                    raise CoilsException(('Unable to open XSLT stylesheet "{0}" for reading').format(xslt_name))
                stylesheet.close()
            else:
                raise CoilsException(('XSLT Stylesheet "{0}" not found.').format(xslt_name))
        else:
            raise CoilsException('No XSLT provided for transform')
        self.log_message(('Template size is {0}b').format(len(self._xslt)), category='debug')
        ctx_param = self.action_parameters.get('contextIds', None)
        if ctx_param:
            ctx_param = self.process_label_substitutions(ctx_param)
            self._ctx_ids = [ int(x) for x in ctx_param.split(',') if x in self._ctx.context_ids ]
        else:
            self._ctx_ids = self._ctx.context_ids
        self._output_mimetype = self.action_parameters.get('mimetype', 'application/xml')
        return

    def do_epilogue(self):
        pass