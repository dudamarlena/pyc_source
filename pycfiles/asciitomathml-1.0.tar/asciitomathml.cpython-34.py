# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./asciitomathml/asciitomathml.py
# Compiled at: 2016-07-16 13:54:09
# Size of source mod 2**32: 37324 bytes
import re, sys, copy
from copy import deepcopy
from xml.etree.ElementTree import Element, tostring
import xml.etree.ElementTree as etree

class InvalidAsciiMath(Exception):
    __doc__ = '\n    handle invalid Ascii Math\n\n    '


class AsciiMathML:
    greek_dict = {'alpha': 'α', 
     'beta': 'β', 
     'chi': 'χ', 
     'delta': 'δ', 
     'epsi': 'ε', 
     'epsilon': 'ε', 
     'varepsilon': 'ɛ', 
     'eta': 'η', 
     'gamma': 'γ', 
     'iota': 'ι', 
     'kappa': 'κ', 
     'lambda': 'λ', 
     'mu': 'μ', 
     'nu': 'ν', 
     'omega': 'ω', 
     'phi': 'φ', 
     'varphi': 'ϕ', 
     'pi': 'π', 
     'psi': 'ψ', 
     'Psi': 'Ψ', 
     'rho': 'ρ', 
     'sigma': 'σ', 
     'tau': 'τ', 
     'theta': 'θ', 
     'vartheta': 'ϑ', 
     'Theta': 'Θ', 
     'upsilon': 'υ', 
     'xi': 'ξ', 
     'zeta': 'ζ'}
    symbol_dict = {}
    text_dict = {'and': 'and', 
     'or': 'or', 
     'if': 'if'}
    symbol_dict.update(greek_dict)
    operator_dict = {'min': 'min', 
     'max': 'max', 
     'lim': 'lim', 
     'Lim': 'Lim', 
     'sin': 'sin', 
     'cos': 'cos', 
     'tan': 'tan', 
     'sinh': 'sinh', 
     'cosh': 'cosh', 
     'tanh': 'tanh', 
     'cot': 'cot', 
     'sec': 'sec', 
     'csc': 'csc', 
     'log': 'log', 
     'ln': 'ln', 
     'det': 'det', 
     'gcd': 'gcd', 
     'lcm': 'lcm', 
     'Delta': 'Δ', 
     'Gamma': 'Γ', 
     'Lambda': 'Λ', 
     'Omega': 'Ω', 
     'Phi': 'Φ', 
     'Pi': 'Π', 
     'Sigma': '∑', 
     'sum': '∑', 
     'Xi': 'Ξ', 
     'prod': '∏', 
     '^^^': '⋀', 
     'vvv': '⋁', 
     'nnn': '⋂', 
     'uuu': '⋃', 
     '*': '⋅', 
     '**': '⋆', 
     '//': '/', 
     '\\\\': '\\', 
     'setminus': '\\', 
     'xx': '×', 
     '-:': '÷', 
     '@': '∘', 
     'o+': '⊕', 
     'ox': '⊗', 
     'o.': '⊙', 
     '^^': '∧', 
     'vv': '∨', 
     'nn': '∩', 
     'uu': '∪', 
     '!=': '≠', 
     ':=': ':=', 
     'lt': '<', 
     '<=': '≤', 
     'lt=': '≤', 
     '>=': '≥', 
     'geq': '≥', 
     'ge': '≥', 
     '-<': '≺', 
     '-lt': '≺', 
     '>-': '≻', 
     '-<=': '⪯', 
     '>-=': '⪰', 
     'in': '∈', 
     '!in': '∉', 
     'sub': '⊂', 
     'sup': '⊃', 
     'sube': '⊆', 
     'supe': '⊇', 
     '-=': '≡', 
     '~=': '≅', 
     '~~': '≈', 
     'prop': '∝', 
     'not': '¬', 
     '=>': '⇒', 
     '<=>': '⇔', 
     'AA': '∀', 
     'EE': '∃', 
     '_|_': '⊥', 
     'TT': '⊤', 
     '|--': '⊢', 
     '|==': '⊨', 
     'int': '∫', 
     'oint': '∮', 
     'del': '∂', 
     'grad': '∇', 
     '+-': '±', 
     'O/': '∅', 
     'oo': '∞', 
     'aleph': 'ℵ', 
     '...': '...', 
     ':.': '∴', 
     '/_': '∠', 
     '\\ ': '\xa0', 
     'quad': '\xa0\xa0', 
     'qquad': '\xa0\xa0\xa0\xa0', 
     'cdots': '⋯', 
     'vdots': '⋮', 
     'ddots': '⋱', 
     'ldots': '…', 
     'diamond': '⋄', 
     'square': '□', 
     '|__': '⌊', 
     '__|': '⌋', 
     '|~': '⌈', 
     '~|': '⌉', 
     'CC': 'ℂ', 
     'NN': 'ℕ', 
     'QQ': 'ℚ', 
     'RR': 'ℝ', 
     'ZZ': 'ℤ', 
     'dim': 'dim', 
     'mod': 'mod', 
     'lub': 'lub', 
     'glb': 'glb', 
     '->': '→'}
    special_dict = {'(': {'type': 'special'},  '{': {'type': 'special'},  '}': {'type': 'special'},  ')': {'type': 'special'},  '[': {'type': 'special'},  ']': {'type': 'special'},  '/': {'type': 'special'},  '^': {'type': 'special'},  '_': {'type': 'special'},  '|': {'type': 'special'},  '||': {'type': 'special'},  '(:': {'type': 'special'},  ':)': {'type': 'special'},  '<<': {'type': 'special'},  '>>': {'type': 'special'},  '{:': {'type': 'special'},  ':}': {'type': 'special'},  'hat': {'type': 'special'},  'bar': {'type': 'special'},  'vec': {'type': 'special'},  'dot': {'type': 'special'},  'ddot': {'type': 'special'},  'ul': {'type': 'special'},  'root': {'type': 'special'},  'stackrel': {'type': 'special'},  'frac': {'type': 'special'},  'sqrt': {'type': 'special'},  'text': {'type': 'special'}}
    under_over_list = [
     '∑', '∏', '⋀', '⋁', '⋂', '⋃', 'min', 'max', 'Lim', 'lim']
    under_over_base_last = ['hat', 'bar', 'vec', 'dot', 'ddot', 'ul']
    over_list = ['hat', 'bar', 'vec', 'dot', 'ddot']
    under_list = ['ul']
    fence_list = ['(', ')', '{', '}', '[', ']', '∹', '〉', '(:', ':)', '<<', '>>', '{:', ':}']
    open_fence_list = ['(', '{', '[', '〈', '<<', '{:']
    close_fence_list = [')', '}', ']', '〉', '>>', ':}']
    function_list = ['root', 'stackrel', 'frac', 'sqrt']
    group_func_list = ['min', 'max', 'sin', 'cos', 'tan', 'sinh', 'cosh', 'tanh', 'cot', 'sec', 'csc', 'log', 'ln', 'det', 'gcd', 'lcm']
    fence_pair = {')': '(',  '}': '{',  ']': '[',  '〉': '〈',  ':}': '{:'}
    over_dict = {'hat': '^',  'bar': '¯',  'vec': '→',  'dot': '.',  'ddot': '..'}
    under_dict = {'ul': '̲'}
    sym_list = list(symbol_dict.keys())
    spec_name_list = list(special_dict.keys())
    op_name_list = list(operator_dict.keys())
    text_list = list(text_dict.keys())
    names = sorted(sym_list + op_name_list + spec_name_list + text_list, key=lambda key_string: len(key_string), reverse=True)

    def __init__(self, output_encoding='us-ascii', mstyle={}):
        self._number_re = re.compile('-?(\\d+\\.(\\d+)?|\\.?\\d+)')
        self._tree = Element('math')
        mstyle = Element('mstyle', **mstyle)
        self._tree.append(mstyle)
        self.VERSION = 0.86
        self._mathml_ns = 'http://www.w3.org/1998/Math/MathML'
        self._append_el = mstyle
        self._output_encoding = output_encoding
        self._fenced_for_right = False
        self._fenced_for_left = False
        self._use_fence = True

    def _add_namespace(self):
        attributes = self._tree.attrib
        value = attributes.get('xmlns')
        if not value:
            self._tree.set('xmlns', self._mathml_ns)

    def _get_rid_of_version_tag(self, string):
        encode_exp = re.compile('^\\<\\?xml .*?\\?\\>')
        string = re.sub(encode_exp, '', string)
        return string.lstrip()

    def to_xml_string(self, encoding=None, no_encoding_string=False, as_string=False):
        if not encoding:
            encoding = self._output_encoding
        self._add_namespace()
        if as_string:
            encoding = 'unicode'
        elif no_encoding_string:
            xml_string = self._get_rid_of_version_tag(xml_string)
        xml_string = tostring(self._tree, encoding=encoding)
        return xml_string

    def get_tree(self):
        self._add_namespace()
        return self._tree

    def _make_element(self, tag, text=None, *children, **attrib):
        """
        Create an element

        """
        element = Element(tag, **attrib)
        if text is not None:
            if isinstance(text, str):
                element.text = text
            else:
                children = (
                 text,) + children
        for child in children:
            element.append(child)

        return element

    def _change_el_name(self, element, new_name):
        element.tag = new_name

    def _get_previous_sibling(self, element, the_tree=0):
        """
        either the previous sibling passed to the function, or if none is passed, 
        the previous sibling of the last element written

        """
        if the_tree == 0:
            the_tree = self._tree
        parent = self._get_parent(child=element, the_tree=the_tree)
        if parent == None:
            return
        counter = -1
        for child in parent:
            counter += 1
            if child == element:
                if counter - 1 < 0:
                    return
                return parent[(counter - 1)]

    def _get_last_element(self):
        if len(self._append_el) > 0:
            return self._append_el[(-1)]
        return self._append_el

    def _get_following_sibling(self, element, the_tree=0):
        if the_tree == 0:
            the_tree = self._tree
        parent = self._get_parent(the_tree=the_tree, child=element)
        if parent == None:
            return
        counter = -1
        for child in parent:
            counter += 1
            if child == element:
                if len(parent) == counter + 1:
                    return
                return parent[(counter + 1)]

    def _get_parent(self, child, the_tree=0):
        """

        the_tree: an xml.etree of the whole tree

        child: an xml.etree of the child element

        There is no direct way to get the parent of an element in etree. This
        method makes a child-parent dictionary of the whold tree, than accesses
        the dictionary

        """
        if the_tree == 0:
            the_tree = self._tree
        child_parent_map = dict((c, p) for p in the_tree.iter() for c in p)
        parent = child_parent_map.get(child)
        return parent

    def _get_grandparent(self, child, the_tree=0):
        parent = self._get_parent(child=child, the_tree=the_tree)
        grandparent = self._get_parent(child=parent, the_tree=the_tree)

    def _change_element(self, element, name, **attributes):
        """
        Changes just the top element to the name "element' with the **attributes passed to it.

        """
        element.tag = name
        the_keys = list(element.attrib.keys())
        for the_key in list(the_keys):
            del element.attrib[the_key]

        for att in attributes:
            element.set(att, attributes[att])

    def _look_at_next_token(self, the_string):
        the_string, token, the_type = self._parse_tokens(the_string)
        return (the_string, token, the_type)

    def _fix_open_fence(self, element):
        """
        changes <mfence open="(" close=""
         ...
         </mfenced>

         <mo>(</mo>
         ...

        """
        parent = self._get_parent(element)
        the_open = element.get('open')
        position = 0
        found = False
        for e in parent:
            if e == element:
                found = 1
                break
            position += 1

        paren = self._make_element('mo', text=the_open)
        parent.insert(position, paren)
        c = 1 + position
        for e in element:
            parent.insert(c, e)
            c += 1

        parent.remove(element)

    def _insert_mrow(self, element, class_name):
        """
        Inserts an mrow element around element

        """
        if len(element) == 1:
            return
        last_element = self._get_last_element()
        atts = deepcopy(last_element.attrib)
        self._change_element(element, 'mrow', **{'class': class_name})
        new_element = deepcopy(element)
        self._append_el.remove(element)
        parenthesis = self._make_element('mfenced', **atts)
        parenthesis.append(new_element)
        self._append_el.append(parenthesis)

    def _count_commas(self, element):
        """
        counts commas for matrix
        """
        if element == None:
            return 0
        count = 0
        for child in element:
            if child.tag == 'mo' and child.text == ',':
                count += 1
                continue

        return count

    def _is_matrix(self, element):
        """
        Tests if element is in fact a matrix

        """
        if len(element) < 3:
            return
        if not self._is_full_fenced(element):
            return
        counter = 0
        row_len = None
        for child in element:
            if counter % 2 == 0:
                if not self._is_full_fenced(child):
                    return
                num_commas = self._count_commas(child)
                if row_len == None:
                    row_len = num_commas
                elif num_commas != row_len:
                    return
                inner_counter = 0
            elif child.tag != 'mo' or child.text != ',':
                return
            counter += 1

        return True

    def _is_full_fenced(self, element):
        """
        Returns True if element is a fence with matching open and close; or if open is {: or closse is :}

        """
        if element == None:
            return
        close_fence = element.get('close')
        the_class = element.get('class')
        open_fence = element.get('open')
        if close_fence == '〉':
            return
        pair = self.fence_pair.get(close_fence)
        if the_class == 'invisible':
            pass
        elif not pair:
            return
        if element.tag == 'mfenced':
            return True

    def _add_num_to_tree(self, token, the_type):
        element = self._make_element('mn', text=token)
        self._append_el.append(element)

    def _add_text_to_tree(self, text):
        present_text = self._append_el.text
        if present_text == None:
            present_text = ''
        self._append_el.text = present_text + text

    def _add_text_el_to_tree(self):
        element = self._make_element('mtext')
        self._append_el.append(element)
        self._append_el = element

    def _end_text_el_to_tree(self):
        self._append_el.attrib.pop('open')
        self._append_el = self._get_parent(self._append_el)

    def _add_special_text_to_tree(self, text):
        """
        adds if , and , or

        """
        element = self._make_element('mspace', **{'width': '1ex'})
        self._append_el.append(element)
        element = self._make_element('mo', text=text)
        self._append_el.append(element)
        element = self._make_element('mspace', **{'width': '1ex'})
        self._append_el.append(element)

    def _add_neg_num_to_tree(self, token, the_type):
        groups = [
         'msup', 'msub', 'munderover', 'munder', 'mover', 'mroot', 'msqrt', 'mfrac']
        if self._append_el.tag in groups:
            element = self._make_element('mrow', **{'class': 'neg-num'})
            self._append_el.append(element)
            append_el = element
        else:
            append_el = self._append_el
        num = token[1:]
        element = self._make_element('mo', text='-')
        append_el.append(element)
        element = self._make_element('mn', text=num)
        append_el.append(element)

    def _add_alpha_to_tree(self, token, the_type):
        element = self._make_element('mi', text=token)
        self._append_el.append(element)

    def _add_symbol_to_tree(self, token, token_dict):
        token = token_dict['symbol']
        element = self._make_element('mi', text=token)
        self._append_el.append(element)

    def _add_operator_to_tree(self, token, token_info):
        if isinstance(token_info, dict):
            text = token_info.get('symbol')
        else:
            text = token
        element = self._make_element('mo', text=text)
        self._append_el.append(element)

    def _do_matrix(self):
        """
        Converts fenced elements to matrices, when elements fit asciimath patterns
        for matrices

        """
        last_element = self._get_last_element()
        is_matrix = self._is_matrix(last_element)
        if not is_matrix:
            return
        the_open = last_element.get('open')
        close = last_element.get('close')
        the_class = last_element.get('class')
        the_dict = {'open': the_open,  'close': close,  'separators': ''}
        if the_class:
            the_dict['class'] = the_class
        fenced = self._make_element('mfenced', **the_dict)
        table = self._make_element('mtable')
        fenced.append(table)
        for child in last_element:
            if self._is_full_fenced(child):
                row = self._make_element('mtr')
                table.append(row)
                cell = self._make_element('mtd')
                row.append(cell)
                for gc in child:
                    if gc.tag != 'mo' or gc.text != ',':
                        cell.append(gc)
                    else:
                        cell = self._make_element('mtd')
                        row.append(cell)

                continue

        self._append_el.remove(last_element)
        self._append_el.append(fenced)

    def _handle_frac(self, token, info):
        last_element = self._get_last_element()
        if last_element == self._append_el:
            self._add_operator_to_tree(token, info)
            return
        num_frac = 0
        if last_element.tag == 'mfrac':
            for child in last_element:
                if child.tag == 'mfrac':
                    num_frac += 1
                    continue

        if num_frac % 2 != 0:
            self._append_el = last_element
            last_element = self._get_last_element()
        if self._is_full_fenced(last_element):
            self._change_element(last_element, 'mrow', **{'class': 'nominator'})
        nominator = deepcopy(last_element)
        self._append_el.remove(last_element)
        mfrac = self._make_element('mfrac', nominator)
        self._append_el.append(mfrac)
        self._append_el = mfrac

    def _handle_lower_upper(self, token, info):
        last_element = self._get_last_element()
        if last_element.tag == 'msub' or last_element.tag == 'munder':
            if last_element.tag == 'msub':
                new_element = self._make_element('msubsup')
            else:
                new_element = self._make_element('munderover')
            for child in last_element:
                element = deepcopy(child)
                new_element.append(element)

            self._append_el.remove(last_element)
            self._append_el.append(new_element)
            self._append_el = new_element
        else:
            if last_element.text in self.under_over_list and token == '^':
                el_name = 'mover'
            else:
                if last_element.text in self.under_over_list and token == '_':
                    el_name = 'munder'
                else:
                    if token == '^':
                        el_name = 'msup'
                    elif token == '_':
                        el_name = 'msub'
                base = deepcopy(last_element)
                self._append_el.remove(last_element)
                base = self._make_element(el_name, base)
                self._append_el.append(base)
                self._append_el = base

    def _handle_open_fence(self, token):
        if self._use_fence:
            element = self._make_element('mfenced', open=token, separators='', close='')
        else:
            element = self._make_element('mo', text=token)
        self._append_el.append(element)
        self._append_el = element

    def _handle_close_fence(self, token):
        first_match = self.fence_pair.get(token)
        element = self._append_el
        match_found = False
        while element != None:
            if element.tag == 'mfenced' and element.get('open') == first_match:
                element.set('close', token)
                parent = self._get_parent(element)
                self._append_el = parent
                match_found = True
                break
            elif element.tag == 'mfenced':
                if element.get('open') == '{:' or token == ':}':
                    element.set('class', 'invisible')
                    parent = self._get_parent(element)
                    self._append_el = parent
                    match_found = True
                    break
            element = self._get_parent(element)

        if match_found:
            return
        if self._fenced_for_right:
            element = self._make_element('mfenced', open='', separators='', close=token)
            self._append_el.append(element)
        else:
            element = self._make_element('mo', text=token)
            self._append_el.append(element)

    def _handle_double_single_bar(self, token, the_type):
        if token == '||':
            the_chr = '‖'
        else:
            if token == '|':
                the_chr = '|'
            if self._append_el.tag == 'mfenced' and self._append_el.get('open') == the_chr:
                self._append_el.set('close', the_chr)
                parent = self._get_parent(self._append_el)
                self._append_el = parent
            else:
                element = self._make_element('mfenced', open=the_chr, separators='', close='')
                self._append_el.append(element)
                self._append_el = element

    def _handle_over(self, token):
        element = self._make_element('mover', **{'class': token})
        self._append_el.append(element)
        self._append_el = element

    def _handle_under(self, token):
        element = self._make_element('munder', **{'class': token})
        self._append_el.append(element)
        self._append_el = element

    def _handle_function(self, token):
        if token == 'root':
            element = self._make_element('mroot')
            self._append_el.append(element)
            self._append_el = element
        else:
            if token == 'stackrel':
                element = self._make_element('mover', **{'class': 'stackrel'})
                self._append_el.append(element)
                self._append_el = element
            else:
                if token == 'frac':
                    element = self._make_element('mfrac')
                    self._append_el.append(element)
                    self._append_el = element
                elif token == 'sqrt':
                    element = self._make_element('msqrt')
                    self._append_el.append(element)
                    self._append_el = element

    def _add_special_to_tree(self, token, the_type):
        if token in self.open_fence_list:
            self._handle_open_fence(token)
        else:
            if token in self.close_fence_list:
                self._handle_close_fence(token)
            else:
                if token == '/':
                    self._handle_frac(token, the_type)
                else:
                    if token == '^' or token == '_':
                        self._handle_lower_upper(token, the_type)
                    else:
                        if token == '||' or token == '|':
                            self._handle_double_single_bar(token, the_type)
                        else:
                            if token == '|':
                                self._handle_single_bar(token, the_type)
                            else:
                                if token in self.over_list:
                                    self._handle_over(token)
                                else:
                                    if token in self.under_list:
                                        self._handle_under(token)
                                    elif token in self.function_list:
                                        self._handle_function(token)

    def _add_fence_to_tree(self, token, the_type):
        if token == '(:' or token == '<<':
            token = '〈'
        if token == ':)' or token == '>>':
            token = '〉'
        if token in self.open_fence_list:
            self._handle_open_fence(token)
        elif token in self.close_fence_list:
            self._handle_close_fence(token)

    def _fix_tree(self):
        """
        Inserts matrix when necessary, and inserts elements where user has 
        erronously non completed them.

        """
        for e in self._tree.iter('mfenced'):
            if e.get('close') == '' and e.get('class') != 'invisible' and not self._fenced_for_left:
                self._fix_open_fence(e)
                continue

        for e in self._tree.iter():
            if e.tag == 'mfrac' and len(e) != 2 and len(e) < 3:
                element = self._make_element('mo')
                while len(e) != 2:
                    element = self._make_element('mo')
                    e.insert(len(e), element)

            elif e.tag == 'mroot' and len(e) != 2:
                if len(e) == 1:
                    element = self._make_element('mo')
                    e.insert(0, element)
                else:
                    while len(e) != 2:
                        element = self._make_element('mo')
                        e.insert(len(e), element)

            elif (e.tag == 'mover' or e.tag == 'munder') and len(e) != 2:
                char = self.over_dict.get(e.get('class'))
                if not char:
                    char = self.under_dict.get(e.get('class'))
                if len(e) == 0:
                    element = self._make_element('mo')
                    e.insert(0, element)
                    element = self._make_element('mo', text=char)
                    e.insert(1, element)
                elif len(e) == 1:
                    element = self._make_element('mo')
                    e.insert(1, element)
            elif (e.tag == 'munderover' or e.tag == 'msubsup') and len(e) != 3:
                element = self._make_element('mo')
                while len(e) != 3:
                    element = self._make_element('mo')
                    e.insert(len(e), element)

            elif (e.tag == 'msup' or e.tag == 'msub') and len(e) != 2:
                element = self._make_element('mo')
                while len(e) != 2:
                    element = self._make_element('mo')
                    e.insert(len(e), element)

                continue

    def _end_stackrel(self):
        """
        ends the stackrel element. The children have to be switched.

        """
        if self._is_full_fenced(self._append_el[0]):
            self._change_element(self._append_el[0], 'mrow', **{'class': 'top'})
        if self._is_full_fenced(self._append_el[1]):
            self._change_element(self._append_el[1], 'mrow', **{'class': 'bottom'})
        top = deepcopy(self._append_el[0])
        self._append_el[0] = self._append_el[1]
        self._append_el[1] = top
        self._append_el = self._get_parent(self._append_el)

    def _end_under_over_char(self):
        """
        Remove parethesis when needed. 
        Add a second element to the parent. The second element depends on the class
        of the parent. For example, class="hat" takes <mo>^</mo> 
        """
        last_element = self._get_last_element()
        if self._is_full_fenced(last_element):
            if self._append_el.tag == 'mover':
                the_dict = {'class': 'mover'}
            if self._append_el.tag == 'munder':
                the_dict = {'class': 'munder'}
            self._change_element(last_element, 'mrow', **the_dict)
        text = self._append_el.get('class')
        if self._append_el.tag == 'mover':
            text = self.over_dict.get(text)
        elif self._append_el.tag == 'munder':
            text = self.under_dict.get(text)
        element = self._make_element('mo', text=text)
        self._append_el.append(element)
        self._append_el = self._get_parent(self._append_el)

    def _end_sqrt(self):
        """
        Remove parenthesis and set the append element to the parent
        """
        if self._is_full_fenced(self._append_el[0]):
            self._change_element(self._append_el[0], 'mrow', **{'class': 'radical'})
        self._append_el = self._get_parent(self._append_el)

    def _end_root(self):
        """
        End parenthesis when needed. 

        The two childrend of mroot have to be switched. In ASCII, the index 
        comes first, followed by the base. In mathml, the base comes first,
        followed by the index.

        Set the appending element to the parent.

        """
        if self._is_full_fenced(self._append_el[0]):
            self._change_element(self._append_el[0], 'mrow', **{'class': 'index'})
        if self._is_full_fenced(self._append_el[1]):
            self._change_element(self._append_el[1], 'mrow', **{'class': 'base'})
        the_index = deepcopy(self._append_el[0])
        self._append_el[0] = self._append_el[1]
        self._append_el[1] = the_index
        self._append_el = self._get_parent(self._append_el)

    def _end_2_child(self):
        """
        These elements have two children. 

        Remove parenthesis if needed.

        Set the appending element to the parent.

        """
        if self._is_full_fenced(self._append_el[1]):
            if self._append_el.tag == 'mfrac':
                the_dict = {'class': 'denominator'}
            else:
                if self._append_el.tag == 'msup':
                    the_dict = {'class': 'superscript'}
                else:
                    if self._append_el.tag == 'msub':
                        the_dict = {'class': 'subcript'}
                    else:
                        if self._append_el.tag == 'munder':
                            the_dict = {'class': 'munder'}
                        elif self._append_el.tag == 'mover':
                            the_dict = {'class': 'mover'}
            self._change_element(self._append_el[1], 'mrow', **the_dict)
        self._append_el = self._get_parent(self._append_el)

    def _end_subsup_underover(self):
        """
        These elements have three childen.

        Remove parenthesis, when needed. 

        Set appending element to parent.

        """
        last_element = self._get_last_element()
        if self._is_full_fenced(last_element):
            if self._append_el.tag == 'msubsup':
                the_dict = {'class': 'subsuper'}
            else:
                the_dict = {'class': 'munderover'}
            self._change_element(last_element, 'mrow', **the_dict)
        self._append_el = self._get_parent(self._append_el)

    def _delete_invisibles(self):
        """
        Remove any  :}

        Single {: are removed in the fix_tree method
        
        """
        last_element = self._get_last_element()
        if last_element.tag == 'mfenced':
            if last_element.get('close') == ':}':
                self._change_element(last_element, 'mrow', **{'class': 'invisible'})

    def _group_functions(self):
        """
        Functions like sin shoud be grouped with mrow
        sin (x + y) => <mo>sin<mrow class="function"> ...</mrow>

        """
        last_element = self._get_last_element()
        if self._is_full_fenced(last_element):
            if len(self._append_el) > 1:
                prev_sib = self._get_previous_sibling(last_element)
                is_function = False
                if prev_sib.text in self.group_func_list:
                    is_function = True
                if prev_sib.tag == 'munderover':
                    if prev_sib[0].tag == 'mo':
                        if prev_sib[0].text in self.group_func_list:
                            is_function = True
                    if is_function:
                        self._insert_mrow(last_element, 'function')

    def _end_elements(self):
        """
        1. mover for stackrel and len is 2: switch elements, move one up
        2. mover or munder and hat etc  and have written element: 
            a. remove parenthesis
            b. write text, such as '^'
            c. append element
            d. move up to parent
        3. sqrt and has one element: remove parenthesis, move up
        4. mroot and len is 2: 
            a. remove parenthesis
            b. switch elements
            c. move one up
        5. mface, msup, msub, munder, mover and len = 2:
            a. get rid of parenthesis
            b. move one up

        6. munderover subsup and len is 3. remove parenthesis, move up 1

        delete invisibles gets rid of {: :}
        group functions groups funcions like sin in mrow
        do_matrix forms matrices

        """
        if self._append_el.tag == 'mover' and self._append_el.get('class') == 'stackrel' and len(self._append_el) == 2:
            self._end_stackrel()
        else:
            if (self._append_el.tag == 'mover' or self._append_el.tag == 'munder') and self._append_el.get('class') in self.under_over_base_last and len(self._append_el) > 0:
                self._end_under_over_char()
            else:
                if self._append_el.tag == 'msqrt' and len(self._append_el) == 1:
                    self._end_sqrt()
                else:
                    if self._append_el.tag == 'mroot' and len(self._append_el) == 2:
                        self._end_root()
                    else:
                        if (self._append_el.tag == 'mfrac' or self._append_el.tag == 'msup' or self._append_el.tag == 'msub' or self._append_el.tag == 'munder' or self._append_el.tag == 'mover') and len(self._append_el) == 2:
                            self._end_2_child()
                        elif self._append_el.tag == 'msubsup' or self._append_el.tag == 'munderover':
                            if len(self._append_el) == 3:
                                self._end_subsup_underover()
        self._delete_invisibles()
        self._group_functions()
        self._do_matrix()

    def parse_string(self, the_string):
        """
        Add element to the tree; fix tree after elements are added.

        """
        while the_string != '':
            the_string, token, token_info = self._parse_tokens(the_string)
            if isinstance(token_info, str):
                the_type = token_info
            else:
                the_type = token_info.get('type')
            if the_type == 'text':
                text = token
                self._add_text_to_tree(text)
            else:
                if the_type == 'start_text':
                    self._add_text_el_to_tree()
                else:
                    if the_type == 'end_text':
                        self._end_text_el_to_tree()
                    else:
                        if the_type == 'special_text':
                            self._add_special_text_to_tree(token)
                        else:
                            if the_type == 'number':
                                self._add_num_to_tree(token, the_type)
                            else:
                                if the_type == 'neg_number':
                                    self._add_neg_num_to_tree(token, the_type)
                                else:
                                    if the_type == 'alpha':
                                        self._add_alpha_to_tree(token, the_type)
                                    else:
                                        if the_type == 'symbol':
                                            self._add_symbol_to_tree(token, token_info)
                                        else:
                                            if the_type == 'operator':
                                                self._add_operator_to_tree(token, token_info)
                                            else:
                                                if token in self.fence_list:
                                                    self._add_fence_to_tree(token, the_type)
                                                elif the_type == 'special':
                                                    self._add_special_to_tree(token, the_type)
            self._end_elements()

        self._fix_tree()

    def _parse_tokens(self, the_string):
        """

        processes the string one token at a time. If a number is found, process
        and return the number with the rest of the stirng.

        Else, see if the string starts with a special symbol, and process and
        return that with the rest of the string.

        Else, get the next character, and process that with the rest of the string.

        """
        if self._append_el.tag == 'mtext':
            next_char = the_string[0]
            if not self._append_el.get('open'):
                if next_char == ' ':
                    return (the_string[1:], ' ', {'type': 'empty_text'})
                if next_char == '(' or next_char == '{' or next_char == '[':
                    self._append_el.set('open', next_char)
                    return (
                     the_string[1:], ' ', {'type': 'empty_text'})
                self._append_el = self._get_parent(self._append_el)
            else:
                first_match = self.fence_pair.get(next_char)
                if first_match:
                    return (the_string[1:], next_char, {'type': 'end_text'})
                else:
                    return (
                     the_string[1:], next_char, {'type': 'text'})
        the_string = the_string.strip()
        if the_string == '':
            return (None, None, None)
        else:
            match = self._number_re.match(the_string)
            if match:
                number = match.group(0)
                if number[0] == '-':
                    return (the_string[match.end():], number, 'neg_number')
                else:
                    return (
                     the_string[match.end():], number, 'number')
            for name in self.names:
                if the_string.startswith(name):
                    the_found = the_string[:len(name)]
                    symbol = self.symbol_dict.get(the_found)
                    operator = self.operator_dict.get(the_found)
                    special = self.special_dict.get(the_found)
                    text = self.text_dict.get(the_found)
                    if the_found == 'text':
                        return (the_string[len(name):], name, {'type': 'start_text'})
                    if symbol != None:
                        return (the_string[len(name):], name, {'type': 'symbol',  'symbol': symbol})
                    if special != None:
                        return (the_string[len(name):], name, special)
                    if operator != None:
                        return (the_string[len(name):], name, {'type': 'operator',  'symbol': operator})
                    if text != None:
                        return (the_string[len(name):], name, {'type': 'special_text'})
                    continue

            if the_string[0].isalpha():
                return (the_string[1:], the_string[0], 'alpha')
            return (the_string[1:], the_string[0], 'operator')