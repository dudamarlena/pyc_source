# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/site-packages/gmssl/sm2_helper.py
# Compiled at: 2020-03-10 11:26:45
# Size of source mod 2**32: 31650 bytes
import math
from .sm2_parameter import *

class Point(object):

    def __init__(self, x=0, y=0):
        self._x = x
        self._y = y

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value

    def __str__(self):
        return '(' + str(self.x) + ', ' + str(self.y) + ')'


def remove_0b_at_beginning(a):
    if a[0:2] == '0b':
        a = a[2:len(a)]
    return a


def padding_0_to_length(S, length):
    temp = S
    S = ''
    if temp[0:2] == '0b':
        S = S + '0b'
        temp = temp[2:len(temp)]
    for i in range(0, length - len(temp)):
        S = S + '0'

    for i in range(0, len(temp)):
        S = S + temp[i]

    return S


def int_to_bytes(x, k):
    M = []
    for i in range(0, k):
        M.append(x >> i * 8 & 255)

    M.reverse()
    return M


def bytes_to_int(M):
    x = 0
    for b in M:
        x = x * 256 + int(b)

    return x


def bits_to_bytes(s):
    if s[0:2] == '0b':
        s = s.replace('0b', '')
        m = len(s)
        k = math.ceil(m / 8)
        M = []
        for i in range(0, k):
            temp = ''
            j = 0
            while j < 8:
                if 8 * i + j >= m:
                    temp = temp + '0'
                else:
                    temp = temp + s[m - (8 * i + j) - 1:m - (8 * i + j)]
                j = j + 1

            temp = temp[::-1]
            temp = int(temp, 2)
            M.append(temp)

        M.reverse()
    else:
        print('*** ERROR: 输入必须为比特串 *** function：bits_to_bytes(s) ***')
        return -1
    return M


def bytes_to_bits(M):
    k = len(M)
    m = 8 * k
    temp = ''
    s = 0
    M.reverse()
    j = 0
    for i in M:
        s = s + i * 256 ** j
        j = j + 1

    s = bin(s)
    s = padding_0_to_length(s, m)
    M.reverse()
    return s


def ele_to_bytes(a):
    S = []
    q = get_q()
    if is_q_prime():
        if q % 2 == 1:
            if a >= 0:
                if a <= q - 1:
                    t = math.ceil(math.log(q, 2))
                    l = math.ceil(t / 8)
                    S = int_to_bytes(a, l)
            print('*** ERROR: 域元素须在区间[0, q-1]上 *** function：ele_to_bytes(a) ***')
            return -1
    else:
        if is_q_power_of_two():
            if type(a) == str:
                if a[0:2] == '0b':
                    m = math.ceil(math.log(q, 2))
                    a = padding_0_to_length(a, m)
                    if len(a) - 2 == m:
                        S = bits_to_bytes(a)
                    else:
                        print('*** ERROR: 域元素必须为长度为m的比特串 *** function：ele_to_bytes(a)')
                        return -1
            print('*** ERROR: 输入必须为比特串 *** function：ele_to_bytes(a) ***')
            return -1
        else:
            print('*** ERROR: q不满足奇素数或2的幂 *** function：ele_to_bytes(a) ***')
            return -1
    return S


def bytes_to_ele(q, S):
    a = ''
    if is_q_prime() and q % 2 == 1:
        a = 0
        t = math.ceil(math.log(q, 2))
        l = math.ceil(t / 8)
        a = bytes_to_int(S)
        if not (a >= 0 and a <= q - 1):
            print('*** ERROR: 域元素须在区间[0, q-1]上 *** function：bytes_to_ele(q, S) ***')
            return -1
    else:
        if is_q_power_of_two():
            m = math.ceil(math.log(q, 2))
            a = padding_0_to_length(a, m)
            if not len(a) - 2 == m:
                print('*** ERROR: 域元素必须为长度为m的比特串 *** function：bytes_to_ele(q, S)')
                return -1
        else:
            print('*** ERROR: q不满足奇素数或2的幂 *** function：bytes_to_ele(q, S) ***')
            return -1
    return a


def ele_to_int(a):
    x = 0
    q = get_q()
    if is_q_prime():
        if q % 2 == 1:
            x = a
    else:
        if is_q_power_of_two():
            if type(a) == str:
                if a[0:2] == '0b':
                    m = math.log(q, 2)
                    if len(a) - 2 == m:
                        a = remove_0b_at_beginning(a)
                        for i in a:
                            x = x * 2 + int(i)

                    else:
                        print('*** ERROR: 域元素必须为长度为m的比特串 *** function：ele_to_int(a, q)')
                        return -1
            print('*** ERROR: 输入必须为比特串 *** function：ele_to_int(a, q) ***')
            return -1
        else:
            print('*** ERROR: q不满足奇素数或2的幂 *** function：ele_to_int(a, q) ***')
            return -1
    return x


def point_to_bytes(point):
    q = get_q()
    l = math.ceil(math.log(q, 2) / 8)
    x = point.x
    y = point.y
    S = []
    PC = ''
    X = ele_to_bytes(x)
    temp = X
    X = []
    for i in range(0, l - len(temp)):
        X.append(0)

    for i in range(0, len(temp)):
        X.append(temp[i])

    Y = ele_to_bytes(y)
    temp = Y
    Y = []
    for i in range(0, l - len(temp)):
        Y.append(0)

    for i in range(0, len(temp)):
        Y.append(temp[i])

    y1_temp = bytes_to_bits(Y)
    y1 = y1_temp[len(y1_temp) - 1:len(y1_temp)]
    if y1 == '0':
        PC = 6
    else:
        if y1 == '1':
            PC = 7
        else:
            print('*** ERROR: PC值不对 function: point_to_bytes ***')
    S.append(PC)
    for m in X:
        S.append(m)

    for n in Y:
        S.append(n)

    return S


def bytes_to_point(a, b, S):
    q = get_q()
    l = math.ceil(math.log(q, 2) / 8)
    PC = ''
    X = []
    Y = []
    if len(S) == 2 * l + 1:
        PC = S[0]
        for i in range(1, l + 1):
            X.append(S[i])

        for i in range(l + 1, 2 * l + 1):
            Y.append(S[i])

    else:
        if len(S) == l + 1:
            PC = S[0]
            for i in range(1, l):
                X.append(S[i])

        else:
            print('*** ERROR: wrong size  function: bytes_to_point ***')
        x = bytes_to_ele(q, X)
        y1 = ''
        if PC == 2:
            y1 = '0'
        else:
            if PC == 3:
                y1 = '1'
            else:
                if PC == 4:
                    y = bytes_to_ele(q, Y)
                else:
                    if PC == 6 or 7:
                        y = bytes_to_ele(q, Y)
                    else:
                        print('ERROR in bytes_to_point')
    result = 0
    if type(x) != type(1):
        x = int(x, 2)
    if type(y) != type(1):
        y = int(y, 2)
    if is_q_prime() and q % 2 == 1:
        if y ** 2 % q != (x ** 3 + a * x + b) % q:
            return -1
    else:
        if is_q_power_of_two():
            if y ** 2 + x * y != x ** 3 + a * x + b:
                return -1
    point = Point(x, y)
    return point


def bytes_to_str(S):
    temp = ''
    string = ''
    temp = remove_0b_at_beginning(bytes_to_bits(S))
    temp = padding_0_to_length(temp, 8 * math.ceil(len(temp) / 8))
    for i in range(0, math.ceil(len(temp) / 8)):
        string = string + chr(int(temp[i * 8:(i + 1) * 8], 2))

    return string


def str_to_bytes(x):
    S = []
    for i in x:
        S.append(ord(i))

    return S


def polynomial_zero():
    return '0b0'


def polynomial_one():
    return '0b1'


def polynomial_times(a, b):
    a_bytes = bits_to_bytes(a)
    a_int = bytes_to_int(a_bytes)
    b_bytes = bits_to_bytes(b)
    b_int = bytes_to_int(b_bytes)
    m = len(a) - 2 + len(b) - 2
    m_bytes = math.ceil(float(m) / 8.0)
    i = 0
    c = 0
    while a_int != 0:
        if a_int % 2 == 1:
            c = c ^ b_int << i
        a_int = a_int // 2
        i += 1

    return bytes_to_bits(int_to_bytes(c, m_bytes))


def polynomial_a_devide_b(a, b):
    a_bytes = bits_to_bytes(a)
    a_int = bytes_to_int(a_bytes)
    a_len = len(a_bytes)
    b_bytes = bits_to_bytes(b)
    b_int = bytes_to_int(b_bytes)
    b_len = len(b_bytes)
    m = len(a) - 2
    m_bytes = math.ceil(float(m) / 8.0)
    c = 0
    i = len(a) - len(b)
    while i >= 0:
        a_int = a_int ^ b_int << i
        c += 1 << i
        i = len(bytes_to_bits(int_to_bytes(a_int, a_len))) - len(bytes_to_bits(int_to_bytes(b_int, b_len)))

    return bytes_to_bits(int_to_bytes(c, m_bytes))


def polynomial_a_mod_b(a, b):
    a_bytes = bits_to_bytes(a)
    a_int = bytes_to_int(a_bytes)
    a_len = len(a_bytes)
    b_bytes = bits_to_bytes(b)
    b_int = bytes_to_int(b_bytes)
    b_len = len(b_bytes)
    m = len(b) - 1
    m_bytes = math.ceil(float(m) / 8.0)
    i = len(a) - len(b)
    while i >= 0:
        a_int = a_int ^ b_int << i
        i = len(bytes_to_bits(int_to_bytes(a_int, a_len))) - len(bytes_to_bits(int_to_bytes(b_int, b_len)))

    return bytes_to_bits(int_to_bytes(a_int, m_bytes))


def in_field(a):
    q = get_q()
    if is_q_prime():
        if q > 2:
            if not (a >= 0 and a <= q - 1):
                print('*** ERROR: a不是有限域中元素 *** function: in_field ***')
                return False
            else:
                return True
    else:
        if is_q_power_of_two():
            m = math.log2(q)
            if len(a) - 2 > m:
                print('*** ERROR: a 不是有限域元素 *** function: in_field ***')
                return False
            else:
                for i in range(2, len(a)):
                    if a[i] != '0':
                        if a[i] != '1':
                            print('*** ERROR: a 不是有限域元素 *** function: in_field ***')
                            return False

                return True
        else:
            print('*** ERROR: 模数q不是奇素数或者2的幂 *** function: field_ele_add ***')
            return -1


def field_ele_zero():
    q = get_q()
    if is_q_prime():
        if q > 2:
            return 0
    if is_q_power_of_two():
        m = int(math.log2(q))
        zero = '0b'
        for i in range(0, m):
            zero += '0'

        return zero
    else:
        print('*** ERROR: 模数q不是奇素数或者2的幂 *** function: field_ele_zero ***')
        return -1


def field_ele_one():
    q = get_q()
    if is_q_prime():
        if q > 2:
            return 1
    if is_q_power_of_two():
        m = int(math.log2(q))
        one = '0b'
        for i in range(0, m - 1):
            one += '0'

        one += '1'
        return one
    else:
        print('*** ERROR: 模数q不是奇素数或者2的幂 *** function: field_ele_one ***')
        return -1


def field_ele_add(a, b):
    q = get_q()
    if is_q_prime():
        if q > 2:
            if not in_field(a):
                print('*** ERROR: a不是素域中元素 *** function: field_ele_add ***')
                return -1
            else:
                if not in_field(b):
                    print('*** ERROR: b不是素域中元素 *** function: field_ele_add ***')
                    return -1
                return (a + b) % q
        else:
            if is_q_power_of_two():
                in_field(a) and in_field(b) or print('*** ERROR: 参数不是二元扩域元素 *** function: field_ele_add ***')
                return -1
            else:
                c_int = ele_to_int(a) ^ ele_to_int(b)
                c_bytes = int_to_bytes(c_int, 2)
                c_ele = bytes_to_ele(q, c_bytes)
                return c_ele
    else:
        print('*** ERROR: 模数q不是奇素数或者2的幂 *** function: field_ele_add ***')
        return -1


def field_ele_inverse_add(a):
    q = get_q()
    if is_q_prime():
        if q > 2:
            if not in_field(a):
                print('*** ERROR: a不是域中元素 *** function: field_ele_inverse_add ***')
                return -1
            else:
                return (q - a) % q
        else:
            if is_q_power_of_two():
                in_field(a) or print('*** ERROR: 参数不是二元扩域元素 *** function: field_ele_inverse_add ***')
                return -1
            else:
                return a
    else:
        print('*** ERROR: 模数q不是奇素数或2的幂 *** function: field_ele_inverse_add ***')
        return -1


def field_ele_sub(a, b):
    return field_ele_add(a, field_ele_inverse_add(b))


def field_ele_times(a, b):
    q = get_q()
    if is_q_prime():
        if q > 2:
            if not in_field(a):
                print('*** ERROR: a不是域中元素 *** function: field_ele_times ***')
                return -1
            else:
                if not in_field(b):
                    print('*** ERROR: b不是域中元素 *** function: field_ele_times ***')
                    return -1
                return a * b % q
        else:
            if is_q_power_of_two():
                in_field(a) and in_field(b) or print('*** ERROR: 参数不是二元扩域元素 *** function: field_ele_times ***')
                return -1
            else:
                result_bits = polynomial_a_mod_b(polynomial_times(a, b), config.get_fx())
                return bytes_to_ele(q, bits_to_bytes(result_bits))
    else:
        print('*** ERROR: 模数q不是奇素数或2的幂 *** function: field_ele_times ***')
        return -1


def field_ele_g_pow_a(g, a):
    q = get_q()
    if is_q_prime():
        if q > 2:
            if not in_field(g):
                print('*** ERROR: a不是域中元素 *** function: field_ele_g_pow_a ***')
                return -1
            else:
                e = a % (q - 1)
                if e == 0:
                    return 1
                r = int(math.log2(e))
                x = g
                for i in range(0, r):
                    x = field_ele_times(x, x)
                    if e & 1 << r - 1 - i == 1 << r - 1 - i:
                        x = field_ele_times(x, g)

                return x
        else:
            if is_q_power_of_two():
                in_field(g) or print('*** ERROR: 参数不是二元扩域元素 *** function: field_ele_g_pow_a ***')
                return -1
            else:
                e = a % (q - 1)
                if e == 0:
                    return polynomial_one()
                r = int(math.log2(e))
                x = g
                for i in range(0, r):
                    x = field_ele_times(x, x)
                    if e & 1 << r - 1 - i == 1 << r - 1 - i:
                        x = field_ele_times(x, g)

                return x
    else:
        print('*** ERROR: 模数q不是奇素数或2的幂 *** function: field_ele_g_pow_a ***')
        return -1


def field_ele_inverse_times(a):
    q = get_q()
    if is_q_prime():
        if q > 2:
            if not in_field(a):
                print('*** ERROR: a不是域中元素 *** function: field_ele_inverse_times ***')
                return -1
            else:
                return field_ele_g_pow_a(a, get_q() - 2)
        else:
            if is_q_power_of_two():
                in_field(a) or print('*** ERROR: 参数不是二元扩域元素 *** function: field_ele_inverse_times ***')
                return -1
            else:
                return field_ele_g_pow_a(a, get_q() - 2)
    else:
        print('*** ERROR: 模数q不是奇素数或2的幂 *** function: field_ele_inverse_times ***')
        return -1


def field_ele_a_devide_b(a, b):
    return field_ele_times(a, field_ele_inverse_times(b))


def ECG_ele_zero():
    return Point(field_ele_zero(), field_ele_zero())


def ECG_ele_is_zero(p):
    if p.x == field_ele_zero():
        if p.y == field_ele_zero():
            return True
    return False


def ECG_is_inverse_ele(p1, p2):
    q = get_q()
    if is_q_prime():
        if p1.x == p2.x:
            if p1.y == field_ele_inverse_add(p2.y):
                return True
        return False
    else:
        if is_q_power_of_two():
            if p1.x == p2.x:
                if p2.y == field_ele_add(p1.x, p1.y):
                    return True
            return False
        else:
            print('*** ERROR: q 不是素数或者 2 的幂 *** function: ECG_is_inverse_ele ***')
            return False


def ECG_ele_equal(p1, p2):
    if p1.x == p2.x:
        if p1.y == p2.y:
            return True
    return False


def ECG_ele_add(p1, p2):
    if is_q_prime():
        if ECG_ele_is_zero(p1):
            return p2
        else:
            if ECG_ele_is_zero(p2):
                return p1
            else:
                if ECG_is_inverse_ele(p1, p2):
                    return ECG_ele_zero()
                if ECG_ele_equal(p1, p2):
                    t1 = field_ele_add(field_ele_times(3, field_ele_g_pow_a(p1.x, 2)), get_a())
                    t2 = field_ele_times(2, p1.y)
                    lam = field_ele_a_devide_b(t1, t2)
                    x = field_ele_sub(field_ele_g_pow_a(lam, 2), field_ele_times(2, p1.x))
                    y = field_ele_sub(field_ele_times(lam, field_ele_sub(p1.x, x)), p1.y)
                    return Point(x, y)
            lam = field_ele_a_devide_b(field_ele_sub(p2.y, p1.y), field_ele_sub(p2.x, p1.x))
            x = field_ele_sub(field_ele_sub(field_ele_g_pow_a(lam, 2), p1.x), p2.x)
            y = field_ele_sub(field_ele_times(lam, field_ele_sub(p1.x, x)), p1.y)
            return Point(x, y)
    if is_q_power_of_two():
        if ECG_ele_is_zero(p1):
            return p2
        else:
            if ECG_ele_is_zero(p2):
                return p1
            else:
                if ECG_is_inverse_ele(p1, p2):
                    return ECG_ele_zero()
                if ECG_ele_equal(p1, p2):
                    lam = field_ele_add(p1.x, field_ele_a_devide_b(p1.y, p1.x))
                    x = field_ele_add(field_ele_add(field_ele_g_pow_a(lam, 2), lam), get_a())
                    y = field_ele_add(field_ele_g_pow_a(p1.x, 2), field_ele_times(field_ele_add(lam, field_ele_one()), x))
                    return Point(x, y)
            lam = field_ele_a_devide_b(field_ele_add(p1.y, p2.y), field_ele_add(p1.x, p2.x))
            t1 = field_ele_add(field_ele_g_pow_a(lam, 2), lam)
            t2 = field_ele_add(field_ele_add(p1.x, p2.x), get_a())
            x = field_ele_add(t1, t2)
            t1 = field_ele_times(lam, field_ele_add(p1.x, x))
            t2 = field_ele_add(x, p1.y)
            y = field_ele_add(t1, t2)
            return Point(x, y)


def ECG_double_point(p):
    if is_q_prime():
        if ECG_ele_is_zero(p):
            return p
        else:
            t1 = field_ele_add(field_ele_times(3, field_ele_g_pow_a(p.x, 2)), get_a())
            t2 = field_ele_times(2, p.y)
            lam = field_ele_a_devide_b(t1, t2)
            x = field_ele_sub(field_ele_g_pow_a(lam, 2), field_ele_times(2, p.x))
            y = field_ele_sub(field_ele_times(lam, field_ele_sub(p.x, x)), p.y)
            return Point(x, y)
    if is_q_power_of_two():
        if ECG_ele_is_zero(p):
            return p
        else:
            lam = field_ele_add(p.x, field_ele_a_devide_b(p.y, p.x))
            x = field_ele_add(field_ele_add(field_ele_g_pow_a(lam, 2), lam), get_a())
            y = field_ele_add(field_ele_g_pow_a(p.x, 2), field_ele_times(field_ele_add(lam, field_ele_one()), x))
            return Point(x, y)


def ECG_k_point(k, p):
    l = int(math.log2(k)) + 1
    point_q = ECG_ele_zero()
    for i in range(0, l):
        j = l - 1 - i
        point_q = ECG_double_point(point_q)
        if k & 1 << j == 1 << j:
            point_q = ECG_ele_add(point_q, p)

    return point_q


def key_pair_generation():
    """
    config.set_q(parameters['q'])
    config.set_a(parameters['a'])
    config.set_b(parameters['b'])
    n = parameters['n']
    point_g = Point(parameters['Gx'], parameters['Gy'])
    # q 为 2 的幂
    if config.is_q_power_of_two():
        config.set_fx(parameters['f(x)'])
    """
    point_g = Point(get_Gx(), get_Gy())
    n = get_n()
    d = random.randint(1, n - 2)
    p = ECG_k_point(d, point_g)
    keypair = []
    keypair.append(d)
    keypair.append(p)
    return keypair


def fix_integer(num):
    int_hex = hex(num)[2:]
    return '0' * (64 - len(int_hex)) + int_hex


def sm2_key_pair_gen():
    key_pair = key_pair_generation()
    prive_key = key_pair[0]
    pub_key = bytes_to_str(point_to_bytes(key_pair[1]))
    a = get_a()
    b = get_b()
    point = bytes_to_point(a, b, str_to_bytes(pub_key))
    return (
     fix_integer(prive_key), fix_integer(point.x) + fix_integer(point.y))