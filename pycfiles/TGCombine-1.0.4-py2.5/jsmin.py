# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tgcombine/jsmin.py
# Compiled at: 2008-04-27 18:48:07
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

def jsmin(js):
    ins = StringIO(js)
    outs = StringIO()
    JavascriptMinify().minify(ins, outs)
    str = outs.getvalue()
    if len(str) > 0 and str[0] == '\n':
        str = str[1:]
    return str


def isAlphanum(c):
    """return true if the character is a letter, digit, underscore,
           dollar sign, or non-ASCII character.
    """
    return c >= 'a' and c <= 'z' or c >= '0' and c <= '9' or c >= 'A' and c <= 'Z' or c == '_' or c == '$' or c == '\\' or c is not None and ord(c) > 126


class UnterminatedComment(Exception):
    pass


class UnterminatedStringLiteral(Exception):
    pass


class UnterminatedRegularExpression(Exception):
    pass


class JavascriptMinify(object):

    def _outA(self):
        self.outstream.write(self.theA)

    def _outB(self):
        self.outstream.write(self.theB)

    def _get(self):
        """return the next character from stdin. Watch out for lookahead. If
           the character is a control character, translate it to a space or
           linefeed.
        """
        c = self.theLookahead
        self.theLookahead = None
        if c == None:
            c = self.instream.read(1)
        if c >= ' ' or c == '\n':
            return c
        if c == '':
            return '\x00'
        if c == '\r':
            return '\n'
        return ' '

    def _peek(self):
        self.theLookahead = self._get()
        return self.theLookahead

    def _next--- This code section failed: ---

 L.  95         0  LOAD_FAST             0  'self'
                3  LOAD_ATTR             0  '_get'
                6  CALL_FUNCTION_0       0  None
                9  STORE_FAST            1  'c'

 L.  96        12  LOAD_FAST             1  'c'
               15  LOAD_CONST               '/'
               18  COMPARE_OP            2  ==
               21  JUMP_IF_FALSE       209  'to 233'
             24_0  THEN                     234
               24  POP_TOP          

 L.  97        25  LOAD_FAST             0  'self'
               28  LOAD_ATTR             1  '_peek'
               31  CALL_FUNCTION_0       0  None
               34  STORE_FAST            2  'p'

 L.  98        37  LOAD_FAST             2  'p'
               40  LOAD_CONST               '/'
               43  COMPARE_OP            2  ==
               46  JUMP_IF_FALSE        53  'to 102'
             49_0  THEN                     103
               49  POP_TOP          

 L.  99        50  LOAD_FAST             0  'self'
               53  LOAD_ATTR             0  '_get'
               56  CALL_FUNCTION_0       0  None
               59  STORE_FAST            1  'c'

 L. 100        62  SETUP_LOOP           30  'to 95'
               65  LOAD_FAST             1  'c'
               68  LOAD_CONST               '\n'
               71  COMPARE_OP            4  >
               74  JUMP_IF_FALSE        16  'to 93'
               77  POP_TOP          

 L. 101        78  LOAD_FAST             0  'self'
               81  LOAD_ATTR             0  '_get'
               84  CALL_FUNCTION_0       0  None
               87  STORE_FAST            1  'c'
               90  JUMP_BACK            65  'to 65'
               93  POP_TOP          
               94  POP_BLOCK        
             95_0  COME_FROM            62  '62'

 L. 102        95  LOAD_FAST             1  'c'
               98  RETURN_VALUE     
               99  JUMP_FORWARD          1  'to 103'
            102_0  COME_FROM            46  '46'
              102  POP_TOP          
            103_0  COME_FROM            99  '99'

 L. 103       103  LOAD_FAST             2  'p'
              106  LOAD_CONST               '*'
              109  COMPARE_OP            2  ==
              112  JUMP_IF_FALSE       114  'to 229'
            115_0  THEN                     230
              115  POP_TOP          

 L. 104       116  LOAD_FAST             0  'self'
              119  LOAD_ATTR             0  '_get'
              122  CALL_FUNCTION_0       0  None
              125  STORE_FAST            1  'c'

 L. 105       128  SETUP_LOOP           99  'to 230'

 L. 106       131  LOAD_FAST             0  'self'
              134  LOAD_ATTR             0  '_get'
              137  CALL_FUNCTION_0       0  None
              140  STORE_FAST            1  'c'

 L. 107       143  LOAD_FAST             1  'c'
              146  LOAD_CONST               '*'
              149  COMPARE_OP            2  ==
              152  JUMP_IF_FALSE        41  'to 196'
            155_0  THEN                     189
              155  POP_TOP          

 L. 108       156  LOAD_FAST             0  'self'
              159  LOAD_ATTR             1  '_peek'
              162  CALL_FUNCTION_0       0  None
              165  LOAD_CONST               '/'
              168  COMPARE_OP            2  ==
              171  JUMP_IF_FALSE        18  'to 192'
            174_0  THEN                     189
              174  POP_TOP          

 L. 109       175  LOAD_FAST             0  'self'
              178  LOAD_ATTR             0  '_get'
              181  CALL_FUNCTION_0       0  None
              184  POP_TOP          

 L. 110       185  LOAD_CONST               ' '
              188  RETURN_END_IF    
            189_0  COME_FROM           171  '171'
            189_1  COME_FROM           152  '152'
              189  JUMP_ABSOLUTE       197  'to 197'
              192  POP_TOP          
              193  JUMP_FORWARD          1  'to 197'
              196  POP_TOP          
            197_0  COME_FROM           193  '193'

 L. 111       197  LOAD_FAST             1  'c'
              200  LOAD_CONST               '\x00'
              203  COMPARE_OP            2  ==
              206  JUMP_IF_FALSE        13  'to 222'
              209  POP_TOP          

 L. 112       210  LOAD_GLOBAL           2  'UnterminatedComment'
              213  CALL_FUNCTION_0       0  None
              216  RAISE_VARARGS_1       1  None
              219  JUMP_BACK           131  'to 131'
            222_0  COME_FROM           206  '206'
              222  POP_TOP          
              223  JUMP_BACK           131  'to 131'
            226_0  COME_FROM           128  '128'
              226  JUMP_ABSOLUTE       234  'to 234'
            229_0  COME_FROM           112  '112'
              229  POP_TOP          
              230  JUMP_FORWARD          1  'to 234'
            233_0  COME_FROM            21  '21'
              233  POP_TOP          
            234_0  COME_FROM           230  '230'

 L. 114       234  LOAD_FAST             1  'c'
              237  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_ABSOLUTE' instruction at offset 189

    def _action(self, action):
        """do something! What you do is determined by the argument:
           1   Output A. Copy B to A. Get the next B.
           2   Copy B to A. Get the next B. (Delete A).
           3   Get the next B. (Delete B).
           action treats a string as a single character. Wow!
           action recognizes a regular expression if it is preceded by ( or , or =.
        """
        if action <= 1:
            self._outA()
        if action <= 2:
            self.theA = self.theB
            if self.theA == "'" or self.theA == '"':
                while 1:
                    self._outA()
                    self.theA = self._get()
                    if self.theA == self.theB:
                        break
                    if self.theA <= '\n':
                        raise UnterminatedStringLiteral()
                    if self.theA == '\\':
                        self._outA()
                        self.theA = self._get()

        if action <= 3:
            self.theB = self._next()
            if self.theB == '/' and (self.theA == '(' or self.theA == ',' or self.theA == '=' or self.theA == ':' or self.theA == '[' or self.theA == '?' or self.theA == '!' or self.theA == '&' or self.theA == '|' or self.theA == ';' or self.theA == '{' or self.theA == '}' or self.theA == '\n'):
                self._outA()
                self._outB()
                while 1:
                    self.theA = self._get()
                    if self.theA == '/':
                        break
                    elif self.theA == '\\':
                        self._outA()
                        self.theA = self._get()
                    elif self.theA <= '\n':
                        raise UnterminatedRegularExpression()
                    self._outA()

                self.theB = self._next()

    def _jsmin(self):
        """Copy the input to the output, deleting the characters which are
           insignificant to JavaScript. Comments will be removed. Tabs will be
           replaced with spaces. Carriage returns will be replaced with linefeeds.
           Most spaces and linefeeds will be removed.
        """
        self.theA = '\n'
        self._action(3)
        while self.theA != '\x00':
            if self.theA == ' ':
                if isAlphanum(self.theB):
                    self._action(1)
                else:
                    self._action(2)
            elif self.theA == '\n':
                if self.theB in ('{', '[', '(', '+', '-'):
                    self._action(1)
                elif self.theB == ' ':
                    self._action(3)
                elif isAlphanum(self.theB):
                    self._action(1)
                else:
                    self._action(2)
            elif self.theB == ' ':
                if isAlphanum(self.theA):
                    self._action(1)
                else:
                    self._action(3)
            elif self.theB == '\n':
                if self.theA in ('}', ']', ')', '+', '-', '"', "'"):
                    self._action(1)
                elif isAlphanum(self.theA):
                    self._action(1)
                else:
                    self._action(3)
            else:
                self._action(1)

    def minify(self, instream, outstream):
        self.instream = instream
        self.outstream = outstream
        self.theA = '\n'
        self.theB = None
        self.theLookahead = None
        self._jsmin()
        self.instream.close()
        return


if __name__ == '__main__':
    import sys
    jsm = JavascriptMinify()
    jsm.minify(sys.stdin, sys.stdout)