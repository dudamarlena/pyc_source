# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/minwebhelpers/jsmin.py
# Compiled at: 2009-12-21 08:27:35
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
        else:
            if c == '':
                return '\x00'
            if c == '\r':
                return '\n'
            return ' '

    def _peek(self):
        self.theLookahead = self._get()
        return self.theLookahead

    def _next--- This code section failed: ---

 L.  92         0  LOAD_FAST             0  'self'
                3  LOAD_ATTR             0  '_get'
                6  CALL_FUNCTION_0       0  None
                9  STORE_FAST            1  'c'

 L.  93        12  LOAD_FAST             1  'c'
               15  LOAD_CONST               '/'
               18  COMPARE_OP            2  ==
               21  JUMP_IF_FALSE       203  'to 227'
             24_0  THEN                     228
               24  POP_TOP          

 L.  94        25  LOAD_FAST             0  'self'
               28  LOAD_ATTR             1  '_peek'
               31  CALL_FUNCTION_0       0  None
               34  STORE_FAST            2  'p'

 L.  95        37  LOAD_FAST             2  'p'
               40  LOAD_CONST               '/'
               43  COMPARE_OP            2  ==
               46  JUMP_IF_FALSE        50  'to 99'
             49_0  THEN                     99
               49  POP_TOP          

 L.  96        50  LOAD_FAST             0  'self'
               53  LOAD_ATTR             0  '_get'
               56  CALL_FUNCTION_0       0  None
               59  STORE_FAST            1  'c'

 L.  97        62  SETUP_LOOP           30  'to 95'
               65  LOAD_FAST             1  'c'
               68  LOAD_CONST               '\n'
               71  COMPARE_OP            4  >
               74  JUMP_IF_FALSE        16  'to 93'
               77  POP_TOP          

 L.  98        78  LOAD_FAST             0  'self'
               81  LOAD_ATTR             0  '_get'
               84  CALL_FUNCTION_0       0  None
               87  STORE_FAST            1  'c'
               90  JUMP_BACK            65  'to 65'
               93  POP_TOP          
               94  POP_BLOCK        
             95_0  COME_FROM            62  '62'

 L.  99        95  LOAD_FAST             1  'c'
               98  RETURN_END_IF    
               99  POP_TOP          

 L. 100       100  LOAD_FAST             2  'p'
              103  LOAD_CONST               '*'
              106  COMPARE_OP            2  ==
              109  JUMP_IF_FALSE       111  'to 223'
            112_0  THEN                     224
              112  POP_TOP          

 L. 101       113  LOAD_FAST             0  'self'
              116  LOAD_ATTR             0  '_get'
              119  CALL_FUNCTION_0       0  None
              122  STORE_FAST            1  'c'

 L. 102       125  SETUP_LOOP           96  'to 224'

 L. 103       128  LOAD_FAST             0  'self'
              131  LOAD_ATTR             0  '_get'
              134  CALL_FUNCTION_0       0  None
              137  STORE_FAST            1  'c'

 L. 104       140  LOAD_FAST             1  'c'
              143  LOAD_CONST               '*'
              146  COMPARE_OP            2  ==
              149  JUMP_IF_FALSE        38  'to 190'
            152_0  THEN                     186
              152  POP_TOP          

 L. 105       153  LOAD_FAST             0  'self'
              156  LOAD_ATTR             1  '_peek'
              159  CALL_FUNCTION_0       0  None
              162  LOAD_CONST               '/'
              165  COMPARE_OP            2  ==
              168  JUMP_IF_FALSE        15  'to 186'
            171_0  THEN                     186
              171  POP_TOP          

 L. 106       172  LOAD_FAST             0  'self'
              175  LOAD_ATTR             0  '_get'
              178  CALL_FUNCTION_0       0  None
              181  POP_TOP          

 L. 107       182  LOAD_CONST               ' '
              185  RETURN_END_IF    
              186  POP_TOP          
              187  JUMP_FORWARD          1  'to 191'
              190  POP_TOP          
            191_0  COME_FROM           187  '187'

 L. 108       191  LOAD_FAST             1  'c'
              194  LOAD_CONST               '\x00'
              197  COMPARE_OP            2  ==
              200  JUMP_IF_FALSE        13  'to 216'
              203  POP_TOP          

 L. 109       204  LOAD_GLOBAL           2  'UnterminatedComment'
              207  CALL_FUNCTION_0       0  None
              210  RAISE_VARARGS_1       1  None
              213  JUMP_BACK           128  'to 128'
            216_0  COME_FROM           200  '200'
              216  POP_TOP          
              217  JUMP_BACK           128  'to 128'
            220_0  COME_FROM           125  '125'
              220  JUMP_ABSOLUTE       228  'to 228'
            223_0  COME_FROM           109  '109'
              223  POP_TOP          
              224  JUMP_FORWARD          1  'to 228'
            227_0  COME_FROM            21  '21'
              227  POP_TOP          
            228_0  COME_FROM           224  '224'

 L. 111       228  LOAD_FAST             1  'c'
              231  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_TOP' instruction at offset 190

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