# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/springheel/parsetranscript.py
# Compiled at: 2019-12-16 05:45:03
# Size of source mod 2**32: 3302 bytes
import os, html

def readTranscript--- This code section failed: ---

 L.  35         0  SETUP_FINALLY        60  'to 60'

 L.  36         2  LOAD_GLOBAL              open
                4  LOAD_FAST                'file_name'
                6  LOAD_STR                 'r'
                8  LOAD_STR                 'utf-8'
               10  LOAD_CONST               ('encoding',)
               12  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               14  SETUP_WITH           30  'to 30'
               16  STORE_FAST               'f'

 L.  37        18  LOAD_FAST                'f'
               20  LOAD_METHOD              read
               22  CALL_METHOD_0         0  ''
               24  STORE_FAST               'text_to_read'
               26  POP_BLOCK        
               28  BEGIN_FINALLY    
             30_0  COME_FROM_WITH       14  '14'
               30  WITH_CLEANUP_START
               32  WITH_CLEANUP_FINISH
               34  END_FINALLY      

 L.  38        36  LOAD_FAST                'text_to_read'
               38  LOAD_STR                 ''
               40  COMPARE_OP               !=
               42  POP_JUMP_IF_FALSE    50  'to 50'

 L.  39        44  LOAD_FAST                'text_to_read'
               46  POP_BLOCK        
               48  RETURN_VALUE     
             50_0  COME_FROM            42  '42'

 L.  41        50  POP_BLOCK        
               52  LOAD_STR                 'No transcript file found.'
               54  RETURN_VALUE     
               56  POP_BLOCK        
               58  JUMP_FORWARD         82  'to 82'
             60_0  COME_FROM_FINALLY     0  '0'

 L.  42        60  DUP_TOP          
               62  LOAD_GLOBAL              IOError
               64  COMPARE_OP               exception-match
               66  POP_JUMP_IF_FALSE    80  'to 80'
               68  POP_TOP          
               70  POP_TOP          
               72  POP_TOP          

 L.  43        74  POP_EXCEPT       
               76  LOAD_STR                 'No transcript file found.'
               78  RETURN_VALUE     
             80_0  COME_FROM            66  '66'
               80  END_FINALLY      
             82_0  COME_FROM            58  '58'

Parse error at or near `LOAD_STR' instruction at offset 52


def makeTranscript(file_name):
    """
    Create a format transcript from a transcript file.

    Parameters
    ----------
    file_name : str
        The path to the transcript file.
    Returns
    -------
    second_pass : str
        The HTML-formatted transcript.
    """
    raw_transcript = readTranscript(file_name)
    if raw_transcript == 'No transcript file found.':
        return raw_transcript
    sep = '\n'
    sep_transcript = raw_transcript.split(sep)
    curr_loc = 0
    first_pass = []
    for i in sep_transcript:
        if i[0:1] == '(':
            escaped = html.escape(i)
            action_list = ['<p class="action">', escaped, '</p>']
            action_string = ''.join(action_list)
            first_pass.append(action_string)
        else:
            if i[0:2] == '  ':
                line_stripped = html.escape(i[2:])
                line_list = [
                 '<span class="linedia">', line_stripped, '</span></p>']
                line_string = ''.join(line_list)
                first_pass.append(line_string)
            else:
                if i == '':
                    break
                else:
                    charname_list = [
                     '<p class="line"><span class="charname">', html.escape(i), '</span>: ']
                    charname_string = ''.join(charname_list)
                    first_pass.append(charname_string)
        curr_loc += 1
    else:
        sep = '\n'
        second_pass = sep.join(first_pass)
        return second_pass