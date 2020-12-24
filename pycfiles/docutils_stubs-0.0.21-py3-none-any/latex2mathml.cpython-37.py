# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/tkomiya/work/sphinx/.tox/py37/lib/python3.7/site-packages/docutils/utils/math/latex2mathml.py
# Compiled at: 2018-11-25 06:19:18
# Size of source mod 2**32: 17407 bytes
"""Convert LaTex math code into presentational MathML"""
import docutils.utils.math.tex2unichar as tex2unichar
over = {'acute':'´', 
 'bar':'¯', 
 'breve':'˘', 
 'check':'ˇ', 
 'dot':'˙', 
 'ddot':'¨', 
 'dddot':'⃛', 
 'grave':'`', 
 'hat':'^', 
 'mathring':'˚', 
 'overleftrightarrow':'⃡', 
 'tilde':'˜', 
 'vec':'⃗'}
Greek = {'Phi':'Φ', 
 'Xi':'Ξ',  'Sigma':'Σ',  'Psi':'Ψ', 
 'Delta':'Δ',  'Theta':'Θ',  'Upsilon':'ϒ', 
 'Pi':'Π',  'Omega':'Ω',  'Gamma':'Γ', 
 'Lambda':'Λ'}
letters = tex2unichar.mathalpha
special = tex2unichar.mathbin
special.update(tex2unichar.mathrel)
special.update(tex2unichar.mathord)
special.update(tex2unichar.mathop)
special.update(tex2unichar.mathopen)
special.update(tex2unichar.mathclose)
special.update(tex2unichar.mathfence)
sumintprod = ''.join([special[symbol] for symbol in ('sum', 'int', 'oint', 'prod')])
functions = [
 'arccos', 'arcsin', 'arctan', 'arg', 'cos', 'cosh',
 'cot', 'coth', 'csc', 'deg', 'det', 'dim',
 'exp', 'gcd', 'hom', 'inf', 'ker', 'lg',
 'lim', 'liminf', 'limsup', 'ln', 'log', 'max',
 'min', 'Pr', 'sec', 'sin', 'sinh', 'sup',
 'tan', 'tanh',
 'injlim', 'varinjlim', 'varlimsup',
 'projlim', 'varliminf', 'varprojlim']
mathbb = {'A':'𝔸', 
 'B':'𝔹', 
 'C':'ℂ', 
 'D':'𝔻', 
 'E':'𝔼', 
 'F':'𝔽', 
 'G':'𝔾', 
 'H':'ℍ', 
 'I':'𝕀', 
 'J':'𝕁', 
 'K':'𝕂', 
 'L':'𝕃', 
 'M':'𝕄', 
 'N':'ℕ', 
 'O':'𝕆', 
 'P':'ℙ', 
 'Q':'ℚ', 
 'R':'ℝ', 
 'S':'𝕊', 
 'T':'𝕋', 
 'U':'𝕌', 
 'V':'𝕍', 
 'W':'𝕎', 
 'X':'𝕏', 
 'Y':'𝕐', 
 'Z':'ℤ'}
mathscr = {'A':'𝒜', 
 'B':'ℬ', 
 'C':'𝒞', 
 'D':'𝒟', 
 'E':'ℰ', 
 'F':'ℱ', 
 'G':'𝒢', 
 'H':'ℋ', 
 'I':'ℐ', 
 'J':'𝒥', 
 'K':'𝒦', 
 'L':'ℒ', 
 'M':'ℳ', 
 'N':'𝒩', 
 'O':'𝒪', 
 'P':'𝒫', 
 'Q':'𝒬', 
 'R':'ℛ', 
 'S':'𝒮', 
 'T':'𝒯', 
 'U':'𝒰', 
 'V':'𝒱', 
 'W':'𝒲', 
 'X':'𝒳', 
 'Y':'𝒴', 
 'Z':'𝒵', 
 'a':'𝒶', 
 'b':'𝒷', 
 'c':'𝒸', 
 'd':'𝒹', 
 'e':'ℯ', 
 'f':'𝒻', 
 'g':'ℊ', 
 'h':'𝒽', 
 'i':'𝒾', 
 'j':'𝒿', 
 'k':'𝓀', 
 'l':'𝓁', 
 'm':'𝓂', 
 'n':'𝓃', 
 'o':'ℴ', 
 'p':'𝓅', 
 'q':'𝓆', 
 'r':'𝓇', 
 's':'𝓈', 
 't':'𝓉', 
 'u':'𝓊', 
 'v':'𝓋', 
 'w':'𝓌', 
 'x':'𝓍', 
 'y':'𝓎', 
 'z':'𝓏'}
negatables = {'=':'≠', 
 '\\in':'∉', 
 '\\equiv':'≢'}

class math:
    __doc__ = 'Base class for MathML elements.'
    nchildren = 1000000

    def __init__(self, children=None, inline=None):
        """math([children]) -> MathML element

        children can be one child or a list of children."""
        self.children = []
        if children is not None:
            if type(children) is list:
                for child in children:
                    self.append(child)

            else:
                self.append(children)
        if inline is not None:
            self.inline = inline

    def __repr__(self):
        if hasattr(self, 'children'):
            return self.__class__.__name__ + '(%s)' % ','.join([repr(child) for child in self.children])
        return self.__class__.__name__

    def full(self):
        """Room for more children?"""
        return len(self.children) >= self.nchildren

    def append(self, child):
        """append(child) -> element

        Appends child and returns self if self is not full or first
        non-full parent."""
        assert not self.full()
        self.children.append(child)
        child.parent = self
        node = self
        while node.full():
            node = node.parent

        return node

    def delete_child(self):
        """delete_child() -> child

        Delete last child and return it."""
        child = self.children[(-1)]
        del self.children[-1]
        return child

    def close(self):
        """close() -> parent

        Close element and return first non-full element."""
        parent = self.parent
        while parent.full():
            parent = parent.parent

        return parent

    def xml(self):
        """xml() -> xml-string"""
        return self.xml_start() + self.xml_body() + self.xml_end()

    def xml_start(self):
        if not hasattr(self, 'inline'):
            return [
             '<%s>' % self.__class__.__name__]
        xmlns = 'http://www.w3.org/1998/Math/MathML'
        if self.inline:
            return [
             '<math xmlns="%s">' % xmlns]
        return ['<math xmlns="%s" mode="display">' % xmlns]

    def xml_end(self):
        return [
         '</%s>' % self.__class__.__name__]

    def xml_body(self):
        xml = []
        for child in self.children:
            xml.extend(child.xml())

        return xml


class mrow(math):

    def xml_start(self):
        return [
         '\n<%s>' % self.__class__.__name__]


class mtable(math):

    def xml_start(self):
        return [
         '\n<%s>' % self.__class__.__name__]


class mtr(mrow):
    pass


class mtd(mrow):
    pass


class mx(math):
    __doc__ = 'Base class for mo, mi, and mn'
    nchildren = 0

    def __init__(self, data):
        self.data = data

    def xml_body(self):
        return [
         self.data]


class mo(mx):
    translation = {'<':'&lt;', 
     '>':'&gt;'}

    def xml_body(self):
        return [self.translation.get(self.data, self.data)]


class mi(mx):
    pass


class mn(mx):
    pass


class msub(math):
    nchildren = 2


class msup(math):
    nchildren = 2


class msqrt(math):
    nchildren = 1


class mroot(math):
    nchildren = 2


class mfrac(math):
    nchildren = 2


class msubsup(math):
    nchildren = 3

    def __init__(self, children=None, reversed=False):
        self.reversed = reversed
        math.__init__(self, children)

    def xml(self):
        if self.reversed:
            self.children[1:3] = [self.children[2], self.children[1]]
            self.reversed = False
        return math.xml(self)


class mfenced(math):
    translation = {'\\{':'{', 
     '\\langle':'〈',  '\\}':'}', 
     '\\rangle':'〉',  '.':''}

    def __init__(self, par):
        self.openpar = par
        math.__init__(self)

    def xml_start(self):
        open = self.translation.get(self.openpar, self.openpar)
        close = self.translation.get(self.closepar, self.closepar)
        return ['<mfenced open="%s" close="%s">' % (open, close)]


class mspace(math):
    nchildren = 0


class mstyle(math):

    def __init__(self, children=None, nchildren=None, **kwargs):
        if nchildren is not None:
            self.nchildren = nchildren
        math.__init__(self, children)
        self.attrs = kwargs

    def xml_start(self):
        return [
         '<mstyle '] + ['%s="%s"' % item for item in list(self.attrs.items())] + ['>']


class mover(math):
    nchildren = 2

    def __init__(self, children=None, reversed=False):
        self.reversed = reversed
        math.__init__(self, children)

    def xml(self):
        if self.reversed:
            self.children.reverse()
            self.reversed = False
        return math.xml(self)


class munder(math):
    nchildren = 2


class munderover(math):
    nchildren = 3

    def __init__(self, children=None):
        math.__init__(self, children)


class mtext(math):
    nchildren = 0

    def __init__(self, text):
        self.text = text

    def xml_body(self):
        return [
         self.text]


def parse_latex_math--- This code section failed: ---

 L. 370         0  LOAD_STR                 ' '
                2  LOAD_METHOD              join
                4  LOAD_FAST                'string'
                6  LOAD_METHOD              split
                8  CALL_METHOD_0         0  '0 positional arguments'
               10  CALL_METHOD_1         1  '1 positional argument'
               12  STORE_FAST               'string'

 L. 372        14  LOAD_FAST                'inline'
               16  POP_JUMP_IF_FALSE    38  'to 38'

 L. 373        18  LOAD_GLOBAL              mrow
               20  CALL_FUNCTION_0       0  '0 positional arguments'
               22  STORE_FAST               'node'

 L. 374        24  LOAD_GLOBAL              math
               26  LOAD_FAST                'node'
               28  LOAD_CONST               True
               30  LOAD_CONST               ('inline',)
               32  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               34  STORE_FAST               'tree'
               36  JUMP_FORWARD         64  'to 64'
             38_0  COME_FROM            16  '16'

 L. 376        38  LOAD_GLOBAL              mtd
               40  CALL_FUNCTION_0       0  '0 positional arguments'
               42  STORE_FAST               'node'

 L. 377        44  LOAD_GLOBAL              math
               46  LOAD_GLOBAL              mtable
               48  LOAD_GLOBAL              mtr
               50  LOAD_FAST                'node'
               52  CALL_FUNCTION_1       1  '1 positional argument'
               54  CALL_FUNCTION_1       1  '1 positional argument'
               56  LOAD_CONST               False
               58  LOAD_CONST               ('inline',)
               60  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               62  STORE_FAST               'tree'
             64_0  COME_FROM            36  '36'

 L. 379     64_66  SETUP_LOOP          842  'to 842'
               68  LOAD_GLOBAL              len
               70  LOAD_FAST                'string'
               72  CALL_FUNCTION_1       1  '1 positional argument'
               74  LOAD_CONST               0
               76  COMPARE_OP               >
            78_80  POP_JUMP_IF_FALSE   840  'to 840'

 L. 380        82  LOAD_GLOBAL              len
               84  LOAD_FAST                'string'
               86  CALL_FUNCTION_1       1  '1 positional argument'
               88  STORE_FAST               'n'

 L. 381        90  LOAD_FAST                'string'
               92  LOAD_CONST               0
               94  BINARY_SUBSCR    
               96  STORE_FAST               'c'

 L. 382        98  LOAD_CONST               1
              100  STORE_FAST               'skip'

 L. 383       102  LOAD_FAST                'n'
              104  LOAD_CONST               1
              106  COMPARE_OP               >
              108  POP_JUMP_IF_FALSE   120  'to 120'

 L. 384       110  LOAD_FAST                'string'
              112  LOAD_CONST               1
              114  BINARY_SUBSCR    
              116  STORE_FAST               'c2'
              118  JUMP_FORWARD        124  'to 124'
            120_0  COME_FROM           108  '108'

 L. 386       120  LOAD_STR                 ''
              122  STORE_FAST               'c2'
            124_0  COME_FROM           118  '118'

 L. 388       124  LOAD_FAST                'c'
              126  LOAD_STR                 ' '
              128  COMPARE_OP               ==
              130  POP_JUMP_IF_FALSE   136  'to 136'

 L. 389   132_134  JUMP_FORWARD        826  'to 826'
            136_0  COME_FROM           130  '130'

 L. 390       136  LOAD_FAST                'c'
              138  LOAD_STR                 '\\'
              140  COMPARE_OP               ==
          142_144  POP_JUMP_IF_FALSE   396  'to 396'

 L. 391       146  LOAD_FAST                'c2'
              148  LOAD_STR                 '{}'
              150  COMPARE_OP               in
              152  POP_JUMP_IF_FALSE   174  'to 174'

 L. 392       154  LOAD_FAST                'node'
              156  LOAD_METHOD              append
              158  LOAD_GLOBAL              mo
              160  LOAD_FAST                'c2'
              162  CALL_FUNCTION_1       1  '1 positional argument'
              164  CALL_METHOD_1         1  '1 positional argument'
              166  STORE_FAST               'node'

 L. 393       168  LOAD_CONST               2
              170  STORE_FAST               'skip'
              172  JUMP_FORWARD        826  'to 826'
            174_0  COME_FROM           152  '152'

 L. 394       174  LOAD_FAST                'c2'
              176  LOAD_STR                 ' '
              178  COMPARE_OP               ==
              180  POP_JUMP_IF_FALSE   200  'to 200'

 L. 395       182  LOAD_FAST                'node'
              184  LOAD_METHOD              append
              186  LOAD_GLOBAL              mspace
              188  CALL_FUNCTION_0       0  '0 positional arguments'
              190  CALL_METHOD_1         1  '1 positional argument'
              192  STORE_FAST               'node'

 L. 396       194  LOAD_CONST               2
              196  STORE_FAST               'skip'
              198  JUMP_FORWARD        826  'to 826'
            200_0  COME_FROM           180  '180'

 L. 397       200  LOAD_FAST                'c2'
              202  LOAD_STR                 ','
              204  COMPARE_OP               ==
              206  POP_JUMP_IF_FALSE   226  'to 226'

 L. 398       208  LOAD_FAST                'node'
              210  LOAD_METHOD              append
              212  LOAD_GLOBAL              mspace
              214  CALL_FUNCTION_0       0  '0 positional arguments'
              216  CALL_METHOD_1         1  '1 positional argument'
              218  STORE_FAST               'node'

 L. 399       220  LOAD_CONST               2
              222  STORE_FAST               'skip'
              224  JUMP_FORWARD        826  'to 826'
            226_0  COME_FROM           206  '206'

 L. 400       226  LOAD_FAST                'c2'
              228  LOAD_METHOD              isalpha
              230  CALL_METHOD_0         0  '0 positional arguments'
          232_234  POP_JUMP_IF_FALSE   324  'to 324'

 L. 402       236  LOAD_CONST               2
              238  STORE_FAST               'i'

 L. 403       240  SETUP_LOOP          278  'to 278'
              242  LOAD_FAST                'i'
              244  LOAD_FAST                'n'
              246  COMPARE_OP               <
          248_250  POP_JUMP_IF_FALSE   276  'to 276'
              252  LOAD_FAST                'string'
              254  LOAD_FAST                'i'
              256  BINARY_SUBSCR    
              258  LOAD_METHOD              isalpha
              260  CALL_METHOD_0         0  '0 positional arguments'
          262_264  POP_JUMP_IF_FALSE   276  'to 276'

 L. 404       266  LOAD_FAST                'i'
              268  LOAD_CONST               1
              270  INPLACE_ADD      
              272  STORE_FAST               'i'
              274  JUMP_BACK           242  'to 242'
            276_0  COME_FROM           262  '262'
            276_1  COME_FROM           248  '248'
              276  POP_BLOCK        
            278_0  COME_FROM_LOOP      240  '240'

 L. 405       278  LOAD_FAST                'string'
              280  LOAD_CONST               1
              282  LOAD_FAST                'i'
              284  BUILD_SLICE_2         2 
              286  BINARY_SUBSCR    
              288  STORE_FAST               'name'

 L. 406       290  LOAD_GLOBAL              handle_keyword
              292  LOAD_FAST                'name'
              294  LOAD_FAST                'node'
              296  LOAD_FAST                'string'
              298  LOAD_FAST                'i'
              300  LOAD_CONST               None
              302  BUILD_SLICE_2         2 
              304  BINARY_SUBSCR    
              306  CALL_FUNCTION_3       3  '3 positional arguments'
              308  UNPACK_SEQUENCE_2     2 
              310  STORE_FAST               'node'
              312  STORE_FAST               'skip'

 L. 407       314  LOAD_FAST                'skip'
              316  LOAD_FAST                'i'
              318  INPLACE_ADD      
              320  STORE_FAST               'skip'
              322  JUMP_FORWARD        826  'to 826'
            324_0  COME_FROM           232  '232'

 L. 408       324  LOAD_FAST                'c2'
              326  LOAD_STR                 '\\'
              328  COMPARE_OP               ==
          330_332  POP_JUMP_IF_FALSE   376  'to 376'

 L. 410       334  LOAD_GLOBAL              mtd
              336  CALL_FUNCTION_0       0  '0 positional arguments'
              338  STORE_FAST               'entry'

 L. 411       340  LOAD_GLOBAL              mtr
              342  LOAD_FAST                'entry'
              344  CALL_FUNCTION_1       1  '1 positional argument'
              346  STORE_FAST               'row'

 L. 412       348  LOAD_FAST                'node'
              350  LOAD_METHOD              close
              352  CALL_METHOD_0         0  '0 positional arguments'
              354  LOAD_METHOD              close
              356  CALL_METHOD_0         0  '0 positional arguments'
              358  LOAD_METHOD              append
              360  LOAD_FAST                'row'
              362  CALL_METHOD_1         1  '1 positional argument'
              364  POP_TOP          

 L. 413       366  LOAD_FAST                'entry'
              368  STORE_FAST               'node'

 L. 414       370  LOAD_CONST               2
              372  STORE_FAST               'skip'
              374  JUMP_FORWARD        826  'to 826'
            376_0  COME_FROM           330  '330'

 L. 416       376  LOAD_GLOBAL              SyntaxError
              378  LOAD_STR                 'Syntax error: "%s%s"'
              380  LOAD_FAST                'c'
              382  LOAD_FAST                'c2'
              384  BUILD_TUPLE_2         2 
              386  BINARY_MODULO    
              388  CALL_FUNCTION_1       1  '1 positional argument'
              390  RAISE_VARARGS_1       1  'exception instance'
          392_394  JUMP_FORWARD        826  'to 826'
            396_0  COME_FROM           142  '142'

 L. 417       396  LOAD_FAST                'c'
              398  LOAD_METHOD              isalpha
              400  CALL_METHOD_0         0  '0 positional arguments'
          402_404  POP_JUMP_IF_FALSE   424  'to 424'

 L. 418       406  LOAD_FAST                'node'
              408  LOAD_METHOD              append
              410  LOAD_GLOBAL              mi
              412  LOAD_FAST                'c'
              414  CALL_FUNCTION_1       1  '1 positional argument'
              416  CALL_METHOD_1         1  '1 positional argument'
              418  STORE_FAST               'node'
          420_422  JUMP_FORWARD        826  'to 826'
            424_0  COME_FROM           402  '402'

 L. 419       424  LOAD_FAST                'c'
              426  LOAD_METHOD              isdigit
              428  CALL_METHOD_0         0  '0 positional arguments'
          430_432  POP_JUMP_IF_FALSE   452  'to 452'

 L. 420       434  LOAD_FAST                'node'
              436  LOAD_METHOD              append
              438  LOAD_GLOBAL              mn
              440  LOAD_FAST                'c'
              442  CALL_FUNCTION_1       1  '1 positional argument'
              444  CALL_METHOD_1         1  '1 positional argument'
              446  STORE_FAST               'node'
          448_450  JUMP_FORWARD        826  'to 826'
            452_0  COME_FROM           430  '430'

 L. 421       452  LOAD_FAST                'c'
              454  LOAD_STR                 "+-*/=()[]|<>,.!?':;@"
              456  COMPARE_OP               in
          458_460  POP_JUMP_IF_FALSE   480  'to 480'

 L. 422       462  LOAD_FAST                'node'
              464  LOAD_METHOD              append
              466  LOAD_GLOBAL              mo
              468  LOAD_FAST                'c'
              470  CALL_FUNCTION_1       1  '1 positional argument'
              472  CALL_METHOD_1         1  '1 positional argument'
              474  STORE_FAST               'node'
          476_478  JUMP_FORWARD        826  'to 826'
            480_0  COME_FROM           458  '458'

 L. 423       480  LOAD_FAST                'c'
              482  LOAD_STR                 '_'
              484  COMPARE_OP               ==
          486_488  POP_JUMP_IF_FALSE   584  'to 584'

 L. 424       490  LOAD_FAST                'node'
              492  LOAD_METHOD              delete_child
              494  CALL_METHOD_0         0  '0 positional arguments'
              496  STORE_FAST               'child'

 L. 425       498  LOAD_GLOBAL              isinstance
              500  LOAD_FAST                'child'
              502  LOAD_GLOBAL              msup
              504  CALL_FUNCTION_2       2  '2 positional arguments'
          506_508  POP_JUMP_IF_FALSE   526  'to 526'

 L. 426       510  LOAD_GLOBAL              msubsup
              512  LOAD_FAST                'child'
              514  LOAD_ATTR                children
              516  LOAD_CONST               True
              518  LOAD_CONST               ('reversed',)
              520  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              522  STORE_FAST               'sub'
              524  JUMP_FORWARD        568  'to 568'
            526_0  COME_FROM           506  '506'

 L. 427       526  LOAD_GLOBAL              isinstance
              528  LOAD_FAST                'child'
              530  LOAD_GLOBAL              mo
              532  CALL_FUNCTION_2       2  '2 positional arguments'
          534_536  POP_JUMP_IF_FALSE   560  'to 560'
              538  LOAD_FAST                'child'
              540  LOAD_ATTR                data
              542  LOAD_GLOBAL              sumintprod
              544  COMPARE_OP               in
          546_548  POP_JUMP_IF_FALSE   560  'to 560'

 L. 428       550  LOAD_GLOBAL              munder
              552  LOAD_FAST                'child'
              554  CALL_FUNCTION_1       1  '1 positional argument'
              556  STORE_FAST               'sub'
              558  JUMP_FORWARD        568  'to 568'
            560_0  COME_FROM           546  '546'
            560_1  COME_FROM           534  '534'

 L. 430       560  LOAD_GLOBAL              msub
              562  LOAD_FAST                'child'
              564  CALL_FUNCTION_1       1  '1 positional argument'
              566  STORE_FAST               'sub'
            568_0  COME_FROM           558  '558'
            568_1  COME_FROM           524  '524'

 L. 431       568  LOAD_FAST                'node'
              570  LOAD_METHOD              append
              572  LOAD_FAST                'sub'
              574  CALL_METHOD_1         1  '1 positional argument'
              576  POP_TOP          

 L. 432       578  LOAD_FAST                'sub'
              580  STORE_FAST               'node'
              582  JUMP_FORWARD        826  'to 826'
            584_0  COME_FROM           486  '486'

 L. 433       584  LOAD_FAST                'c'
              586  LOAD_STR                 '^'
              588  COMPARE_OP               ==
          590_592  POP_JUMP_IF_FALSE   726  'to 726'

 L. 434       594  LOAD_FAST                'node'
              596  LOAD_METHOD              delete_child
              598  CALL_METHOD_0         0  '0 positional arguments'
              600  STORE_FAST               'child'

 L. 435       602  LOAD_GLOBAL              isinstance
            604_0  COME_FROM           172  '172'
              604  LOAD_FAST                'child'
              606  LOAD_GLOBAL              msub
              608  CALL_FUNCTION_2       2  '2 positional arguments'
          610_612  POP_JUMP_IF_FALSE   626  'to 626'

 L. 436       614  LOAD_GLOBAL              msubsup
              616  LOAD_FAST                'child'
              618  LOAD_ATTR                children
              620  CALL_FUNCTION_1       1  '1 positional argument'
              622  STORE_FAST               'sup'
              624  JUMP_FORWARD        710  'to 710'
            626_0  COME_FROM           610  '610'

 L. 437       626  LOAD_GLOBAL              isinstance
              628  LOAD_FAST                'child'
            630_0  COME_FROM           198  '198'
              630  LOAD_GLOBAL              mo
              632  CALL_FUNCTION_2       2  '2 positional arguments'
          634_636  POP_JUMP_IF_FALSE   660  'to 660'
              638  LOAD_FAST                'child'
              640  LOAD_ATTR                data
              642  LOAD_GLOBAL              sumintprod
              644  COMPARE_OP               in
          646_648  POP_JUMP_IF_FALSE   660  'to 660'

 L. 438       650  LOAD_GLOBAL              mover
              652  LOAD_FAST                'child'
              654  CALL_FUNCTION_1       1  '1 positional argument'
            656_0  COME_FROM           224  '224'
              656  STORE_FAST               'sup'
              658  JUMP_FORWARD        710  'to 710'
            660_0  COME_FROM           646  '646'
            660_1  COME_FROM           634  '634'

 L. 439       660  LOAD_GLOBAL              isinstance
              662  LOAD_FAST                'child'
              664  LOAD_GLOBAL              munder
              666  CALL_FUNCTION_2       2  '2 positional arguments'
          668_670  POP_JUMP_IF_FALSE   702  'to 702'

 L. 440       672  LOAD_FAST                'child'
              674  LOAD_ATTR                children
              676  LOAD_CONST               0
              678  BINARY_SUBSCR    
              680  LOAD_ATTR                data
              682  LOAD_GLOBAL              sumintprod
              684  COMPARE_OP               in
          686_688  POP_JUMP_IF_FALSE   702  'to 702'

 L. 441       690  LOAD_GLOBAL              munderover
              692  LOAD_FAST                'child'
              694  LOAD_ATTR                children
              696  CALL_FUNCTION_1       1  '1 positional argument'
              698  STORE_FAST               'sup'
              700  JUMP_FORWARD        710  'to 710'
            702_0  COME_FROM           686  '686'
            702_1  COME_FROM           668  '668'

 L. 443       702  LOAD_GLOBAL              msup
              704  LOAD_FAST                'child'
              706  CALL_FUNCTION_1       1  '1 positional argument'
              708  STORE_FAST               'sup'
            710_0  COME_FROM           700  '700'
            710_1  COME_FROM           658  '658'
            710_2  COME_FROM           624  '624'

 L. 444       710  LOAD_FAST                'node'
              712  LOAD_METHOD              append
              714  LOAD_FAST                'sup'
              716  CALL_METHOD_1         1  '1 positional argument'
              718  POP_TOP          

 L. 445       720  LOAD_FAST                'sup'
              722  STORE_FAST               'node'
              724  JUMP_FORWARD        826  'to 826'
            726_0  COME_FROM           590  '590'

 L. 446       726  LOAD_FAST                'c'
              728  LOAD_STR                 '{'
              730  COMPARE_OP               ==
          732_734  POP_JUMP_IF_FALSE   758  'to 758'

 L. 447       736  LOAD_GLOBAL              mrow
              738  CALL_FUNCTION_0       0  '0 positional arguments'
              740  STORE_FAST               'row'

 L. 448       742  LOAD_FAST                'node'
              744  LOAD_METHOD              append
              746  LOAD_FAST                'row'
              748  CALL_METHOD_1         1  '1 positional argument'
              750  POP_TOP          

 L. 449       752  LOAD_FAST                'row'
            754_0  COME_FROM           322  '322'
              754  STORE_FAST               'node'
              756  JUMP_FORWARD        826  'to 826'
            758_0  COME_FROM           732  '732'

 L. 450       758  LOAD_FAST                'c'
              760  LOAD_STR                 '}'
              762  COMPARE_OP               ==
          764_766  POP_JUMP_IF_FALSE   778  'to 778'

 L. 451       768  LOAD_FAST                'node'
              770  LOAD_METHOD              close
              772  CALL_METHOD_0         0  '0 positional arguments'
              774  STORE_FAST               'node'
              776  JUMP_FORWARD        826  'to 826'
            778_0  COME_FROM           764  '764'

 L. 452       778  LOAD_FAST                'c'
              780  LOAD_STR                 '&'
              782  COMPARE_OP               ==
          784_786  POP_JUMP_IF_FALSE   814  'to 814'

 L. 453       788  LOAD_GLOBAL              mtd
              790  CALL_FUNCTION_0       0  '0 positional arguments'
              792  STORE_FAST               'entry'

 L. 454       794  LOAD_FAST                'node'
              796  LOAD_METHOD              close
              798  CALL_METHOD_0         0  '0 positional arguments'
              800  LOAD_METHOD              append
              802  LOAD_FAST                'entry'
              804  CALL_METHOD_1         1  '1 positional argument'
            806_0  COME_FROM           374  '374'
              806  POP_TOP          

 L. 455       808  LOAD_FAST                'entry'
              810  STORE_FAST               'node'
              812  JUMP_FORWARD        826  'to 826'
            814_0  COME_FROM           784  '784'

 L. 457       814  LOAD_GLOBAL              SyntaxError
              816  LOAD_STR                 'Illegal character: "%s"'
              818  LOAD_FAST                'c'
              820  BINARY_MODULO    
              822  CALL_FUNCTION_1       1  '1 positional argument'
              824  RAISE_VARARGS_1       1  'exception instance'
            826_0  COME_FROM           812  '812'
            826_1  COME_FROM           776  '776'
            826_2  COME_FROM           756  '756'
            826_3  COME_FROM           724  '724'
            826_4  COME_FROM           582  '582'
            826_5  COME_FROM           476  '476'
            826_6  COME_FROM           448  '448'
            826_7  COME_FROM           420  '420'
            826_8  COME_FROM           392  '392'
            826_9  COME_FROM           132  '132'

 L. 458       826  LOAD_FAST                'string'
              828  LOAD_FAST                'skip'
              830  LOAD_CONST               None
              832  BUILD_SLICE_2         2 
              834  BINARY_SUBSCR    
              836  STORE_FAST               'string'
              838  JUMP_BACK            68  'to 68'
            840_0  COME_FROM            78  '78'
              840  POP_BLOCK        
            842_0  COME_FROM_LOOP       64  '64'

 L. 459       842  LOAD_FAST                'tree'
              844  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM' instruction at offset 604_0


def handle_keyword(name, node, string):
    skip = 0
    if len(string) > 0:
        if string[0] == ' ':
            string = string[1:]
            skip = 1
    if name == 'begin':
        if not string.startswith('{matrix}'):
            raise SyntaxError('Environment not supported! Supported environment: "matrix".')
        skip += 8
        entry = mtd
        table = mtable(mtr(entry))
        node.append(table)
        node = entry
    else:
        if name == 'end':
            if not string.startswith('{matrix}'):
                raise SyntaxError('Expected "\\end{matrix}"!')
            skip += 8
            node = node.close().close().close()
        else:
            if name in ('text', 'mathrm'):
                if string[0] != '{':
                    raise SyntaxError('Expected "\\text{...}"!')
                i = string.find('}')
                if i == -1:
                    raise SyntaxError('Expected "\\text{...}"!')
                node = node.append(mtext(string[1:i]))
                skip += i + 1
            else:
                if name == 'sqrt':
                    sqrt = msqrt
                    node.append(sqrt)
                    node = sqrt
                else:
                    if name == 'frac':
                        frac = mfrac
                        node.append(frac)
                        node = frac
                    else:
                        if name == 'left':
                            for par in ('(', '[', '|', '\\{', '\\langle', '.'):
                                if string.startswith(par):
                                    break
                            else:
                                raise SyntaxError('Missing left-brace!')

                            fenced = mfenced(par)
                            node.append(fenced)
                            row = mrow
                            fenced.append(row)
                            node = row
                            skip += len(par)
                        else:
                            if name == 'right':
                                for par in (')', ']', '|', '\\}', '\\rangle', '.'):
                                    if string.startswith(par):
                                        break
                                else:
                                    raise SyntaxError('Missing right-brace!')

                                node = node.close()
                                node.closepar = par
                                node = node.close()
                                skip += len(par)
                            else:
                                if name == 'not':
                                    for operator in negatables:
                                        if string.startswith(operator):
                                            break
                                    else:
                                        raise SyntaxError('Expected something to negate: "\\not ..."!')

                                    node = node.append(mo(negatables[operator]))
                                    skip += len(operator)
                                else:
                                    if name == 'mathbf':
                                        style = mstyle(nchildren=1, fontweight='bold')
                                        node.append(style)
                                        node = style
                                    else:
                                        if name == 'mathbb':
                                            if not (string[0] != '{' or string[1].isupper)() or string[2] != '}':
                                                raise SyntaxError('Expected something like "\\mathbb{A}"!')
                                            node = node.append(mi(mathbb[string[1]]))
                                            skip += 3
                                        else:
                                            if name in ('mathscr', 'mathcal') and not string[0] != '{':
                                                if string[2] != '}':
                                                    raise SyntaxError('Expected something like "\\mathscr{A}"!')
                                                node = node.append(mi(mathscr[string[1]]))
                                                skip += 3
                                            else:
                                                if name == 'colon':
                                                    node = node.append(mo(':'))
                                                else:
                                                    if name in Greek:
                                                        node = node.append(mo(Greek[name]))
                                                    else:
                                                        if name in letters:
                                                            node = node.append(mi(letters[name]))
                                                        else:
                                                            if name in special:
                                                                node = node.append(mo(special[name]))
                                                            else:
                                                                if name in functions:
                                                                    node = node.append(mo(name))
                                                                else:
                                                                    if name in over:
                                                                        ovr = mover((mo(over[name])), reversed=True)
                                                                        node.append(ovr)
                                                                        node = ovr
                                                                    else:
                                                                        raise SyntaxError('Unknown LaTeX command: ' + name)
    return (
     node, skip)


def tex2mathml(tex_math, inline=True):
    """Return string with MathML code corresponding to `tex_math`. 
    
    `inline`=True is for inline math and `inline`=False for displayed math.
    """
    mathml_tree = parse_latex_math(tex_math, inline=inline)
    return ''.join(mathml_tree.xml())