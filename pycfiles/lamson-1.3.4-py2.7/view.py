# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-intel/egg/lamson/view.py
# Compiled at: 2011-05-21 19:39:14
"""
These are helper functions that make it easier to work with either
Jinja2 or Mako templates.  You MUST configure it by setting
lamson.view.LOADER to one of the template loaders in your config.boot
or config.testing.

After that these functions should just work.
"""
from lamson import mail
import email, warnings
LOADER = None

def load--- This code section failed: ---

 L.  22         0  LOAD_GLOBAL           0  'LOADER'
                3  POP_JUMP_IF_TRUE     15  'to 15'
                6  LOAD_ASSERT              AssertionError
                9  LOAD_CONST               "You haven't set lamson.view.LOADER to a loader yet."
               12  RAISE_VARARGS_2       2  None

 L.  23        15  LOAD_GLOBAL           0  'LOADER'
               18  LOAD_ATTR             2  'get_template'
               21  LOAD_FAST             0  'template'
               24  CALL_FUNCTION_1       1  None
               27  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 27


def render(variables, template):
    """
    Takes the variables given and renders the template for you.
    Assumes the template returned by load() will have a .render()
    method that takes the variables as a dict.

    Use this if you just want to render a single template and don't
    want it to be a message.  Use render_message if the contents
    of the template are to be interpreted as a message with headers
    and a body.
    """
    return load(template).render(variables)


def respond--- This code section failed: ---

 L.  66         0  LOAD_FAST             1  'Body'
                3  POP_JUMP_IF_TRUE     21  'to 21'
                6  LOAD_FAST             2  'Html'
                9  POP_JUMP_IF_TRUE     21  'to 21'
               12  LOAD_ASSERT              AssertionError
               15  LOAD_CONST               'You need to give either the Body or Html template of the mail.'
               18  RAISE_VARARGS_2       2  None

 L.  68        21  SETUP_LOOP           32  'to 56'
               24  LOAD_FAST             3  'kwd'
               27  GET_ITER         
               28  FOR_ITER             24  'to 55'
               31  STORE_FAST            4  'key'

 L.  69        34  LOAD_FAST             3  'kwd'
               37  LOAD_FAST             4  'key'
               40  BINARY_SUBSCR    
               41  LOAD_FAST             0  'variables'
               44  BINARY_MODULO    
               45  LOAD_FAST             3  'kwd'
               48  LOAD_FAST             4  'key'
               51  STORE_SUBSCR     
               52  JUMP_BACK            28  'to 28'
               55  POP_BLOCK        
             56_0  COME_FROM            21  '21'

 L.  71        56  LOAD_GLOBAL           1  'mail'
               59  LOAD_ATTR             2  'MailResponse'
               62  LOAD_FAST             3  'kwd'
               65  CALL_FUNCTION_KW_0     0  None
               68  STORE_FAST            5  'msg'

 L.  73        71  LOAD_FAST             1  'Body'
               74  POP_JUMP_IF_FALSE    98  'to 98'

 L.  74        77  LOAD_GLOBAL           3  'render'
               80  LOAD_FAST             0  'variables'
               83  LOAD_FAST             1  'Body'
               86  CALL_FUNCTION_2       2  None
               89  LOAD_FAST             5  'msg'
               92  STORE_ATTR            4  'Body'
               95  JUMP_FORWARD          0  'to 98'
             98_0  COME_FROM            95  '95'

 L.  76        98  LOAD_FAST             2  'Html'
              101  POP_JUMP_IF_FALSE   125  'to 125'

 L.  77       104  LOAD_GLOBAL           3  'render'
              107  LOAD_FAST             0  'variables'
              110  LOAD_FAST             2  'Html'
              113  CALL_FUNCTION_2       2  None
              116  LOAD_FAST             5  'msg'
              119  STORE_ATTR            5  'Html'
              122  JUMP_FORWARD          0  'to 125'
            125_0  COME_FROM           122  '122'

 L.  79       125  LOAD_FAST             5  'msg'
              128  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 128


def attach(msg, variables, template, filename=None, content_type=None, disposition=None):
    """
    Useful for rendering an attachment and then attaching it to the message
    given.  All the parameters that are in lamson.mail.MailResponse.attach
    are there as usual.
    """
    data = render(variables, template)
    msg.attach(filename=filename, data=data, content_type=content_type, disposition=disposition)