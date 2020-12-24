# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/modelmachine/asm.py
# Compiled at: 2016-03-05 13:44:31
# Size of source mod 2**32: 10346 bytes
"""Model machine assembler."""
import re, warnings
from ply import lex, yacc
from modelmachine.memory import RandomAccessMemory
from modelmachine.io import InputOutputUnit

class g:
    lexer = None
    parser = None
    error_list = None
    mapper = None
    output = None
    pos = None
    max_pos = None
    label_table = None
    ram = None

    @classmethod
    def put(cls, value, size):
        """Write test memory."""
        cls.ram.put(cls.pos, value, size)
        for i in range(size // 16):
            i = i
            cls.pos = (cls.pos + 1) % 65536
            cls.max_pos = max(cls.max_pos, cls.pos)

    @classmethod
    def clear(cls):
        """Set up."""
        cls.lexer = None
        cls.parser = None
        cls.error_list = []
        cls.mapper = []
        cls.output = []
        cls.pos = 0
        cls.max_pos = 0
        cls.label_table = dict()
        cls.ram = RandomAccessMemory(word_size=16, memory_size=65536, endianess='big', is_protected=False)


TEMPLATE = 'mmm\n\n[config]\noutput = {output}\n\n[code]\n{code}\n\n[input]\n\n'
literals = '()-:,\n'
opcodes = {'load': 0, 
 'add': 1, 
 'sub': 2, 
 'smul': 3, 
 'sdiv': 4, 
 'comp': 5, 
 'addr': 17, 
 'umul': 19, 
 'udiv': 20, 
 'store': 16, 
 'rmove': 32, 
 'radd': 33, 
 'rsub': 34, 
 'rsmul': 35, 
 'rsdiv': 36, 
 'rcomp': 37, 
 'rumul': 51, 
 'rudiv': 52, 
 'jump': 128, 
 'jeq': 129, 
 'jneq': 130, 
 'sjl': 131, 
 'sjgeq': 132, 
 'sjleq': 133, 
 'sjg': 134, 
 'ujl': 147, 
 'ujgeq': 148, 
 'ujleq': 149, 
 'ujg': 150, 
 'halt': 153}
preproc_instructions = {'.config': 'CONFIG', 
 '.word': 'WORD', 
 '.code': 'CODE', 
 '.dump': 'DUMP'}
tokens = [
 'LABEL', 'NUMBER', 'REGISTER'] + [op.upper() for op in opcodes.keys()] + list(preproc_instructions.values())

def find_column(lexpos):
    """Get symbol position."""
    last_cr = g.lexer.lexdata.rfind('\n', 0, lexpos)
    if last_cr == -1:
        return lexpos + 1
    else:
        return lexpos - last_cr


def position(t):
    """Get term position."""
    return '{line}:{col}'.format(line=t.lineno, col=find_column(t.lexpos))


def lexer():
    t_ignore = ' \t'
    t_ignore_COMMENT = ';.*'

    def t_LABEL(t):
        r"""[\.\w]+"""
        if re.compile('^(?:0x[\\da-f]+)|(?:0b[01]+)|(?:0o[0-7]+)|(?:\\d+)$').match(t.value):
            t.value = int(t.value, 0)
            t.type = 'NUMBER'
        else:
            if t.value in preproc_instructions:
                t.type = preproc_instructions[t.value]
            else:
                if t.value in opcodes:
                    t.type = t.value.upper()
                else:
                    if re.compile('^r[0-9a-f]$').match(t.value):
                        t.type = 'REGISTER'
                        t.value = int(t.value[1], 16)
                    else:
                        if re.compile('^[a-z_]\\w*$').match(t.value):
                            t.type = 'LABEL'
                        else:
                            g.error_list.append("Illegal token '{value}' at {line}:{col}".format(value=t.value, line=t.lineno, col=find_column(t.lexpos)))
                            t = None
        return t

    def t_newline(t):
        r"""\n+"""
        t.lexer.lineno += len(t.value)
        t.type = '\n'
        return t

    def t_error(t):
        g.error_list.append("Illegal character '{char}' at {position}".format(char=t.value[0], position=position(t)))
        g.lexer.skip(1)

    g.lexer = lex.lex()
    return g.lexer


def get_lexems(code):
    """Get array of lexems and errors."""
    g.clear()
    lexer()
    g.lexer.input(code.lower())
    result = list(g.lexer)
    return (g.error_list, result)


def parser():
    """Get the parser."""
    start = 'program'

    def p_empty(p):
        """empty :"""
        pass

    def p_negative_minus(p):
        """negative : '-' NUMBER"""
        p[0] = -p[2]

    def p_negative_plus(p):
        """negative : NUMBER"""
        p[0] = p[1]

    def p_position_label(p):
        """position : LABEL"""
        p[0] = (
         p[1], 1)

    def p_position_array(p):
        """position : LABEL '(' NUMBER ')'"""
        p[0] = (
         p[1], p[3])

    def p_listtail(p):
        """numberlist : negative
           poslist : position
        """
        p[0] = [
         p[1]]

    def p_list(p):
        """numberlist : numberlist ',' negative
           poslist : poslist ',' position
        """
        p[0] = p[1].copy()
        p[0].append(p[3])

    def p_address_label(p):
        """address : LABEL"""
        p[0] = (
         0, p[1])

    def p_address_register(p):
        """address : LABEL '(' REGISTER ')'"""
        if p[3] == 0:
            g.error_list.append('Cannot use R0 for indexing at {line}:{col}'.format(line=p.lineno(3), col=find_column(p.lexpos(1))))
            raise SyntaxError
        else:
            p[0] = (
             p[3], p[1])

    def p_line_empty(p):
        """line : empty"""
        pass

    def p_line_deflabel(p):
        """line : deflabel line"""
        pass

    def p_deflabel_label(p):
        """deflabel : LABEL ':'"""
        if p[1] in g.label_table:
            prev = g.label_table[p[1]]
            g.error_list.append("Double definition of label '{label}' at {line}:{col}".format(label=p[1], line=p.lineno(1), col=find_column(p.lexpos(1))) + ' previously defined at {line}:{col}'.format(line=prev[1], col=prev[2]))
            raise SyntaxError
        else:
            g.label_table[p[1]] = (
             g.pos, p.lineno(1), find_column(p.lexpos(1)))

    def p_line_config(p):
        """line : CONFIG NUMBER"""
        g.pos = p[2]

    def p_line_code(p):
        """line : CODE"""
        g.pos = 0

    def p_line_word(p):
        """line : WORD numberlist"""
        for number in p[2]:
            g.put(number % 4294967296, 32)

    def p_line_dump(p):
        """line : DUMP poslist"""
        g.output.extend(p[2])

    def p_error(p):
        if not p:
            g.error_list.append('Unexpected EOF')
            return
        g.error_list.append("Unexpected '{token}' at {position}".format(token=p.type, position=position(p)))

    def p_line_memops(p):
        """line : LOAD  REGISTER ',' address
                | ADD   REGISTER ',' address
                | SUB   REGISTER ',' address
                | SMUL  REGISTER ',' address
                | SDIV  REGISTER ',' address
                | COMP  REGISTER ',' address
                | UMUL  REGISTER ',' address
                | UDIV  REGISTER ',' address
                | ADDR  REGISTER ',' address
                | STORE REGISTER ',' address
        """
        data = opcodes[p[1]] << 8 | p[2] << 4 | p[4][0]
        g.put(data, 16)
        g.mapper.append((g.pos, p[4][1], p.lineno(3), find_column(p.lexpos(3))))
        g.put(0, 16)

    def p_line_regops(p):
        """line : RADD  REGISTER ',' REGISTER
                | RSUB  REGISTER ',' REGISTER
                | RSMUL REGISTER ',' REGISTER
                | RSDIV REGISTER ',' REGISTER
                | RCOMP REGISTER ',' REGISTER
                | RUMUL REGISTER ',' REGISTER
                | RUDIV REGISTER ',' REGISTER
                | RMOVE REGISTER ',' REGISTER
        """
        data = opcodes[p[1]] << 8 | p[2] << 4 | p[4]
        g.put(data, 16)

    def p_line_jumps(p):
        """line : JUMP  address
                | JEQ   address
                | JNEQ  address
                | SJL   address
                | SJGEQ address
                | SJLEQ address
                | SJG   address
                | UJL   address
                | UJGEQ address
                | UJLEQ address
                | UJG   address
        """
        data = opcodes[p[1]] << 8 | p[2][0]
        g.put(data, 16)
        g.mapper.append((g.pos, p[2][1], p.lineno(1), find_column(p.lexpos(1))))
        g.put(0, 16)

    def p_line_halt(p):
        """line : HALT"""
        g.put(39168, 16)

    def p_program(p):
        r"""program : line
                    | program '\n' line"""
        pass

    lexer()
    g.parser = yacc.yacc()
    return g.parser


def parse(code):
    """Parse asm code and return model machine code."""
    error_list, lexems = get_lexems(code)
    if error_list != []:
        return (error_list, None)
    else:
        g.clear()
        lexer()
        parser()
        g.parser.parse(code.lower())
        if g.error_list != []:
            return (g.error_list, None)
        for insert in g.mapper:
            pos, label = insert[:2]
            if label in g.label_table:
                g.ram.put(pos, g.label_table[label][0], 16)
            else:
                g.error_list.append("Undefined label '{label}' at {line}:{col}".format(label=label, line=insert[2], col=insert[3]))

        for label, count in g.output:
            if label not in g.label_table:
                g.error_list.append("Undefined label '{label}' at output".format(label=label))

        if g.error_list == []:
            output = g.output
            g.output = []
            for label, count in output:
                for i in range(count):
                    g.output.append(str(g.label_table[label][0] + 2 * i))

        if g.error_list != []:
            return (g.error_list, None)
        io_unit = InputOutputUnit(g.ram, 0, 16)
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            code = io_unit.store_hex(0, g.max_pos * 16)
        output = ', '.join(g.output)
        return ([], TEMPLATE.format(output=output, code=code))