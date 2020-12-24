# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-m_4qh6p6/docutils/docutils/utils/math/latex2mathml.py
# Compiled at: 2019-07-30 18:47:12
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
        else:
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
            return ['<%s>' % self.__class__.__name__]
        else:
            xmlns = 'http://www.w3.org/1998/Math/MathML'
            if self.inline:
                return [
                 '<math xmlns="%s">' % xmlns]
            return ['<math xmlns="%s" mode="display">' % xmlns]

    def xml_end(self):
        return ['</%s>' % self.__class__.__name__]

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


def parse_latex_math(string, inline=True):
    """parse_latex_math(string [,inline]) -> MathML-tree

    Returns a MathML-tree parsed from string.  inline=True is for
    inline math and inline=False is for displayed math.

    tree is the whole tree and node is the current element."""
    string = ' '.join(string.split())
    if inline:
        node = mrow()
        tree = math(node, inline=True)
    else:
        node = mtd()
        tree = math((mtable(mtr(node))), inline=False)
    while len(string) > 0:
        n = len(string)
        c = string[0]
        skip = 1
        if n > 1:
            c2 = string[1]
        else:
            c2 = ''
        if c == ' ':
            pass
        else:
            if c == '\\':
                if c2 in '{}':
                    node = node.append(mo(c2))
                    skip = 2
                else:
                    if c2 == ' ':
                        node = node.append(mspace())
                        skip = 2
                    else:
                        if c2 == ',':
                            node = node.append(mspace())
                            skip = 2
                        else:
                            if c2.isalpha():
                                i = 2
                                while i < n and string[i].isalpha():
                                    i += 1

                                name = string[1:i]
                                node, skip = handle_keyword(name, node, string[i:])
                                skip += i
                            else:
                                if c2 == '\\':
                                    entry = mtd()
                                    row = mtr(entry)
                                    node.close().close().append(row)
                                    node = entry
                                    skip = 2
                                else:
                                    raise SyntaxError('Syntax error: "%s%s"' % (c, c2))
            else:
                if c.isalpha():
                    node = node.append(mi(c))
                else:
                    if c.isdigit():
                        node = node.append(mn(c))
                    else:
                        if c in "+-*/=()[]|<>,.!?':;@":
                            node = node.append(mo(c))
                        else:
                            if c == '_':
                                child = node.delete_child()
                                if isinstance(child, msup):
                                    sub = msubsup((child.children), reversed=True)
                                elif isinstance(child, mo):
                                    if child.data in sumintprod:
                                        sub = munder(child)
                                else:
                                    sub = msub(child)
                                node.append(sub)
                                node = sub
                            else:
                                if c == '^':
                                    child = node.delete_child()
                                    if isinstance(child, msub):
                                        sup = msubsup(child.children)
                                    elif isinstance(child, mo):
                                        if child.data in sumintprod:
                                            sup = mover(child)
                                    elif isinstance(child, munder):
                                        if child.children[0].data in sumintprod:
                                            sup = munderover(child.children)
                                    else:
                                        sup = msup(child)
                                    node.append(sup)
                                    node = sup
                                else:
                                    if c == '{':
                                        row = mrow()
                                        node.append(row)
                                        node = row
                                    else:
                                        if c == '}':
                                            node = node.close()
                                        else:
                                            if c == '&':
                                                entry = mtd()
                                                node.close().append(entry)
                                                node = entry
                                            else:
                                                raise SyntaxError('Illegal character: "%s"' % c)
        string = string[skip:]

    return tree


def handle_keyword(name, node, string):
    skip = 0
    if len(string) > 0:
        if string[0] == ' ':
            string = string[1:]
            skip = 1
    else:
        if name == 'begin':
            if not string.startswith('{matrix}'):
                raise SyntaxError('Environment not supported! Supported environment: "matrix".')
            skip += 8
            entry = mtd()
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
                        sqrt = msqrt()
                        node.append(sqrt)
                        node = sqrt
                    else:
                        if name == 'frac':
                            frac = mfrac()
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
                                row = mrow()
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
                                                if string[0] != '{' or not string[1].isupper() or string[2] != '}':
                                                    raise SyntaxError('Expected something like "\\mathbb{A}"!')
                                                node = node.append(mi(mathbb[string[1]]))
                                                skip += 3
                                            else:
                                                if name in ('mathscr', 'mathcal'):
                                                    if string[0] != '{' or string[2] != '}':
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