# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/springheel/parsemeta.py
# Compiled at: 2019-12-16 05:38:51
# Size of source mod 2**32: 3957 bytes
from slugify import slugify, slugify_url
import springheel.parseconf, html

def readMeta--- This code section failed: ---

 L.  37         0  SETUP_FINALLY        44  'to 44'

 L.  38         2  LOAD_GLOBAL              open
                4  LOAD_FAST                'file_name'
                6  LOAD_STR                 'r'
                8  LOAD_STR                 'utf-8'
               10  LOAD_CONST               ('encoding',)
               12  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               14  SETUP_WITH           34  'to 34'
               16  STORE_FAST               'f'

 L.  39        18  LOAD_FAST                'f'
               20  LOAD_METHOD              read
               22  CALL_METHOD_0         0  ''
               24  LOAD_METHOD              splitlines
               26  CALL_METHOD_0         0  ''
               28  STORE_FAST               'text_to_read'
               30  POP_BLOCK        
               32  BEGIN_FINALLY    
             34_0  COME_FROM_WITH       14  '14'
               34  WITH_CLEANUP_START
               36  WITH_CLEANUP_FINISH
               38  END_FINALLY      
               40  POP_BLOCK        
               42  JUMP_FORWARD        102  'to 102'
             44_0  COME_FROM_FINALLY     0  '0'

 L.  40        44  DUP_TOP          
               46  LOAD_GLOBAL              IOError
               48  COMPARE_OP               exception-match
               50  POP_JUMP_IF_FALSE    72  'to 72'
               52  POP_TOP          
               54  POP_TOP          
               56  POP_TOP          

 L.  41        58  LOAD_GLOBAL              print
               60  LOAD_STR                 'An I/O error has occurred.'
               62  CALL_FUNCTION_1       1  ''
               64  POP_TOP          

 L.  42        66  POP_EXCEPT       
               68  LOAD_CONST               False
               70  RETURN_VALUE     
             72_0  COME_FROM            50  '50'

 L.  43        72  DUP_TOP          
               74  LOAD_GLOBAL              UnboundLocalError
               76  COMPARE_OP               exception-match
               78  POP_JUMP_IF_FALSE   100  'to 100'
               80  POP_TOP          
               82  POP_TOP          
               84  POP_TOP          

 L.  44        86  LOAD_GLOBAL              print
               88  LOAD_STR                 "An Unbound Local Error has occurred. I'm probably looking for a page that doesn't exist."
               90  CALL_FUNCTION_1       1  ''
               92  POP_TOP          

 L.  45        94  POP_EXCEPT       
               96  LOAD_CONST               False
               98  RETURN_VALUE     
            100_0  COME_FROM            78  '78'
              100  END_FINALLY      
            102_0  COME_FROM            42  '42'

 L.  46       102  LOAD_FAST                'text_to_read'
              104  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_CONST' instruction at offset 68


def getMetaCom(meta_raw, translated_strings):
    """
    Separate the metadata from formatting info and commentary.

    Parameters
    ----------
    meta_raw : list
        Lines from the metadata file.
    translated_strings : dict
        The translation file contents for this site.
    Returns
    -------
    meta_nl : list
        Metadata lines with key: value pairs.
    comments : list
        HTML-escaped creator commentary lines.
    """
    meta_nl = []
    comments = []
    for i in meta_raw:
        if not i == '---\n':
            if i == '---':
                pass
            elif i[0:2] == '  ':
                meta_nl.append(i.strip)
            else:
                comments.append(html.escape(i))
        else:
            if comments == []:
                comments = [
                 translated_strings['no_comment']]
            return (
             meta_nl, comments)


def dictizeMeta(m):
    """
    Convert the plain metadata into a dictionary.

    Parameters
    ----------
    m : list
        A list of lines with colon-separated metadata.
    Returns
    -------
    meta : dict
        The dictionary-fied metadata.
    """
    meta = []
    for i in m:
        s = i.split(': ', 1)
        d = {s[0]: s[1]}
        meta.append(d)
    else:
        result = {}
        for d in meta:
            result.update(d)
        else:
            meta = result
            return meta


def parseMetadata(file_name, translated_strings):
    """
    Short description.

    Parameters
    ----------
    file_name : str
        The path to the metadata file.
    translated_strings : dict
        The translation file contents for this site.
    Returns
    -------
    meta : dict
        A dictionary of strip metadata.
    commentary : str
        Creator commentary formatted as HTML paragraphs.
    slugs : list
        URL-safe slugs for the strip title and category.
    """
    meta_raw = readMeta(file_name)
    m, c = getMetaCom(meta_raw, translated_strings)
    meta = dictizeMeta(m)
    series_slug = slugify_url(meta['category'])
    title_slug = slugify_url(meta['title'])
    slugs = [title_slug, series_slug]
    commentary = []
    for line in c:
        comm = [
         '<p>', line, '</p>']
        comm = ''.join(comm)
        commentary.append(comm)
    else:
        commentary = ''.join(commentary)
        return (meta, commentary, slugs)