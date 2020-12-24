# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\dragonfly\actions\_generate_typeables.py
# Compiled at: 2008-11-19 12:15:10
"""
    This file automates the creation of the typeables.py file.
"""
from ctypes import windll, c_char
import win32con

def parse(input):
    output = []
    for item in input.split(';'):
        parts = item.split('=')
        left_string = parts[0].strip()
        if not left_string:
            continue
        for right_string in parts[1].split(','):
            right_string = right_string.strip()
            if not right_string:
                continue
            output.append((left_string, right_string))

    return output


constant_keys = '\n    shift = shift; control = control, ctrl; menu = alt;\n    up = up; down = down; left = left; right = right;\n    prior = pgup;\n    next = pgdown;\n    home = home;\n    end = end;\n    return = enter;\n    tab = tab;\n    space = space;\n    back = backspace;\n    delete = delete, del;\n    apps = apps, popup;\n    escape = escape;\n\n    multiply = npmul;\n    add = npadd;\n    separator = npsep;\n    subtract = npsub;\n    decimal = npdec;\n    divide = npdiv;\n' + (' ').join([ 'numpad%(n)d = np%(n)d, numpad%(n)d;' % {'n': n} for n in range(10) ]) + (' ').join([ 'f%(n)d = f%(n)d;' % {'n': n} for n in range(1, 25) ])
for (virtual_name, name) in parse(constant_keys):
    virtual_name = 'VK_%s' % virtual_name.upper()
    keycode = getattr(win32con, virtual_name)
    print '    "%s": %sTypeable(code=win32con.%s, %sname="%s"),' % (name, ' ' * (12 - len(name)), virtual_name, ' ' * (12 - len(virtual_name)), name)

lookup_keys = '\n    a = alpha, a; b = bravo, b; c = charlie, c; d = delta, d;\n    e = echo, e; f = foxtrot, f; g = golf, g; h = hotel, h;\n    i = india, i; j = juliet, j; k = kilo, k; l = lima, l;\n    m = mike, m; n = november, n; o = oscar, o; p = papa, p;\n    q = quebec, q; r = romeo, r; s = sierra, s; t = tango, t;\n    u = uniform, u; v = victor, v; w = whisky, w; x = xray, x;\n\n    y = yankee, y; z = zulu, z;\n    A = Alpha, A; B = Bravo, B; C = Charlie, C; D = Delta, D;\n    E = Echo, E; F = Foxtrot, F; G = Golf, G; H = Hotel, H;\n    I = India, I; J = Juliet, J; K = Kilo, K; L = Lima, L;\n    M = Mike, M; N = November, N; O = Oscar, O; P = Papa, P;\n    Q = Quebec, Q; R = Romeo, R; S = Sierra, S; T = Tango, T;\n    U = Uniform, U; V = Victor, V; W = Whisky, W; X = Xray, X;\n    Y = Yankee, Y; Z = Zulu, Z;\n\n    0 = 0, zero; 1 = 1, one; 2 = 2, two; 3 = 3, three; 4 = 4, four;\n    5 = 5, five; 6 = 6, six; 7 = 7, seven; 8 = 8, eight; 9 = 9, nine;\n\n    ! = bang, exclamation;  @ = at;  # = hash;  $ = dollar;\n    % = percent;  ^ = caret;  & = and, ampersand;  * = star, asterisk; \n    ( = leftparen, lparen; ) = rightparen, rparen;\n\n    - = minus, hyphen;\n    _ = underscore; + = plus; ` = backtick; ~ = tilde;\n    [ = leftbracket, lbracket; ] = rightbracket, rbracket;\n    { = leftbrace, lbrace; } = rightbrace, rbrace;\n    \\ = backslash; | = bar;\n    : = colon;\n    \' = apostrophe, singlequote, squote; " = quote, doublequote, dquote;\n    , = comma; . = dot; / = slash;\n    < = lessthan, leftangle, langle; > = greaterthan, rightangle, rangle;\n    ? = question;\n'
for (character, name) in parse(lookup_keys):
    print '    "%s": %skeyboard.get_typeable(char=%r),' % (
     name, ' ' * (12 - len(name)), character)

character = '='
for name in ('equal', 'equals'):
    print '    "%s": %skeyboard.get_typeable(char=%r),' % (
     name, ' ' * (12 - len(name)), character)