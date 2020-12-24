# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/gmisclib/parse_tree_number.py
# Compiled at: 2008-03-29 07:04:43
import sets, math, operator as OP

class Array(object):

    def __init__(self, name):
        """This creates an array.   Arrays are basic
                elements of expressions."""
        self.name = name

    def __getitem__(self, key):
        return elementof(self, key)

    def __str__(self, env={}):
        if self.name in env:
            return env[self.name].__str__(env)
        return self.name

    __repr__ = __str__

    def indices(self, env={}):
        raise RuntimeError, 'It is an array'

    def eval(self, env={}):
        raise RuntimeError, 'It is an array'

    def variables(self, env={}):
        if self.name in env:
            return env[self.name].variables(env)
        return sets.Set((self.name,))

    def debug(self):
        return '<Array %s>' % self.name

    def _complexity(self):
        return 2


class output_mixin(object):

    def __init__(self):
        pass

    def eval(self, env={}):
        """This returns an Expression.
                """
        raise RuntimeError, 'Virtual!'

    def variables(self, env={}):
        """Any definitions in env are used to resolve otherwise
                undefined names.    This returns a Set containing
                all undefined variable names.
                """
        raise RuntimeError, 'Virtual!'

    def indices(self, variable, env={}):
        raise RuntimeError, 'Virtual!'

    def debug(self):
        return '<Output_mixin: virtual!>'

    def __str__(self, env={}):
        """Env is optional. Anything defined in env is used
                to resolve references, but the outcome may still contain
                undefined variables, which are printed as names.
                """
        raise RuntimeError, 'Virtual!'

    def _complexity(self):
        raise RuntimeError, 'Virtual!'


def _is_opNg1(x, op):
    assert op in _operator.Priority
    return isinstance(x, operatorNg1) and x.op == op


def _is_op1(x, op):
    assert op in _operator.Priority
    return isinstance(x, operator1) and x.op == op


def _IMO_float(a, b, indent):
    if a is b:
        return Float(1.0)
    else:
        try:
            fb = float(b)
        except TypeError:
            pass
        else:
            if fb == 0.0:
                return
            else:
                try:
                    fa = float(a)
                except TypeError:
                    return

                return Float(fa / fb)

        return


def _IMO_Name(a, b, indent):
    if isinstance(a, Name) and isinstance(b, Name) and a.name == b.name:
        return Float(1.0)
    else:
        return


def _IMO_elementof(a, b, indent):
    if isinstance(a, elementof) and isinstance(b, elementof):
        if str(a.array) == str(b.array) and str(a.index) == str(b.index):
            return Float(1.0)
    return


def _IMO_products(a, b, indent):
    if _is_opNg1(a, '*'):
        atmp = list(a.operands)
    else:
        atmp = [
         a]
    if _is_opNg1(b, '*'):
        btmp = list(b.operands)
    else:
        btmp = [
         b]
    if len(atmp) + len(btmp) > 2:
        rtmp = []
        while atmp:
            ai = atmp.pop()
            t = None
            for j in range(len(btmp)):
                t = is_mul_of(ai, btmp[j], indent + '#')
                if t is not None:
                    tmp = coerce_into(t)
                    if tmp._complexity() < ai._complexity() + btmp[j]._complexity():
                        break

            if t is not None:
                atmp.append(t)
                btmp.pop(j)
            else:
                rtmp.append(ai)

        if len(btmp) == 0:
            rv = rtmp[0]
            for rt in rtmp[1:]:
                rv *= rt

            return rv
    return


def _IMO_neg(a, b, indent):
    if _is_op1(a, 'U-') and _is_op1(b, 'U-'):
        return is_mul_of(a.operand, b.operand, indent + '#')
    else:
        if _is_op1(a, 'U-'):
            t = is_mul_of(a.operand, b, indent + '#')
            if t is not None:
                return -t
        if _is_op1(b, 'U-'):
            t = is_mul_of(a, b.operand, indent + '#')
            if t is not None:
                return -t
        return


def _IMO_exp(a, b, indent):
    if _is_op1(a, 'exp') and _is_op1(b, 'exp'):
        return operator1('exp', a.operand - b.operand)
    else:
        return


def _IMO_pow(a, b, indent):
    if _is_opNg1(a, '**') and len(a.operands) == 2:
        if a.operands[1] >= 1.0:
            t = is_mul_of(a.operands[0], b, indent + '#')
            if t is not None:
                return operatorN('*', operatorN('**', [t, a.operands[1]]), operatorN('**', [b, operatorN('-', a.operands[1], 1)]))
    if _is_opNg1(a, '**') and len(a.operands) == 2 and _is_opNg1(b, '**') and len(b.operands) == 2:
        if a.operands[1] >= b.operands[1]:
            t = is_mul_of(a.operands[0], b.operands[0], indent + '#')
            if t is not None:
                return operatorN('*', operatorN('**', t, a.operands[1]), operatorN('**', b, operatorN('-', [a.operands[1],
                 b.operands[1]])))
    return


def is_mul_of(a, b, indent=''):
    """Returns the ratio a/b if a contains b as a factor,
        returns None otherwise.
        The routine does not promise to find all possible factors.
        """
    for test in [
     _IMO_Name, _IMO_elementof,
     _IMO_neg,
     _IMO_products,
     _IMO_exp, _IMO_pow]:
        tmp = test(a, b, indent)
        if tmp is not None:
            if tmp._complexity() < a._complexity() + b._complexity():
                return tmp

    return


class abstract_number(object):

    def __init__(self):
        pass

    def __add__(self, other):
        try:
            fs = float(self)
        except TypeError:
            fs = None

        try:
            fo = float(other)
        except TypeError:
            fo = None

        if fo is not None and fs is not None:
            return Float(fo + fs)
        else:
            if fs == 0.0:
                return other
            if fo == 0.0:
                return self
            other = coerce_into(other)
            if _is_opNg1(self, '+'):
                a = list(self.operands)
            else:
                a = [
                 self]
            if _is_opNg1(other, '+'):
                b = list(other.operands)
            else:
                b = [
                 other]
            ao = []
            while a:
                ai = a.pop()
                for j in range(len(b)):
                    t1 = is_mul_of(ai, b[j])
                    if t1 is not None:
                        tmp = coerce_into(t1 + 1.0) * b[j]
                        if tmp._complexity() < ai._complexity() + b[j]._complexity() + 1:
                            a.append(tmp)
                            b.pop(j)
                            ai = None
                            break
                    t2 = is_mul_of(b[j], ai)
                    if t2 is not None:
                        tmp = coerce_into(t2 + 1.0) * ai
                        if tmp._complexity() < ai._complexity() + b[j]._complexity() + 1:
                            a.append(tmp)
                            ai = None
                            b.pop(j)
                            break
                        else:
                            continue

                if ai:
                    ao.append(ai)

            return operatorN('+', tuple(ao) + tuple(b))

    __radd__ = __add__

    def __sub__(self, other):
        try:
            fs = float(self)
        except TypeError:
            fs = None

        try:
            fo = float(other)
        except TypeError:
            fo = None

        if fo is not None and fs is not None:
            return Float(fs - fo)
        else:
            if fs == 0.0:
                return operator1('U-', other)
            if fo == 0.0:
                return self
            other = coerce_into(other)
            if _is_op1(other, 'U-'):
                return operatorN('+', (self, other))
            if _is_op1(self, 'U-'):
                return operator1('U-', operatorN('+', (self, other)))
            return operatorN('-', (self, other))

    def __rsub__(self, other):
        return other.__sub__(self)

    def __pow__(self, other):
        try:
            fs = float(self)
        except TypeError:
            fs = None

        try:
            fo = float(other)
        except TypeError:
            fo = None

        if fo is not None and fs is not None:
            return Float(fs ** fo)
        else:
            other = coerce_into(other)
            if _is_float(self, 1.0):
                return Float(1.0)
            if _is_float(other, 1.0):
                return self
            if _is_float(other, 0.5):
                return operator1('sqrt', self)
            return operatorN('**', (self, other))

    def __rpow__(self, other):
        return other.__pow__(self)

    def __mul__(self, other):
        try:
            fs = float(self)
        except TypeError:
            fs = None

        try:
            fo = float(other)
        except TypeError:
            fo = None

        if fo is not None and fs is not None:
            return Float(fo * fs)
        else:
            if fs == 1.0:
                return other
            if fo == 1.0:
                return self
            if fs == -1.0:
                return operator1('U-', other)
            if fo == -1.0:
                return operator1('U-', self)
            other = coerce_into(other)
            if _is_op1(self, 'U-') and _is_op1(other, 'U-'):
                self = self.operand
                other = other.operand
            if _is_opNg1(self, '*'):
                if _is_opNg1(other, '*'):
                    return self.more(other.operands)
                else:
                    return self.more((other,))

            return operatorN('*', (self, other))

    __rmul__ = __mul__

    def __div__(self, other):
        try:
            fs = float(self)
        except TypeError:
            fs = None

        try:
            fo = float(other)
        except TypeError:
            fo = None

        if fo is not None and fs is not None:
            return Float(fs / fo)
        else:
            if fo == 1.0:
                return self
            if fo == -1.0:
                return operator1('U-', self)
            if fo is not None and _is_opNg1(self, '*'):
                modified = False
                atmp = list(self.operands)
                for i, op in enumerate(atmp):
                    try:
                        f = float(op)
                    except TypeError:
                        pass
                    else:
                        atmp[i] = Float(f / fo)
                        modified = True

                if modified:
                    rv = atmp[0]
                    for rt in atmp[1:]:
                        rv *= rt

                    return rv
            other = coerce_into(other)
            t = is_mul_of(self, other)
            if t is not None:
                tmp = coerce_into(t)
                if tmp._complexity() < self._complexity + other._complexity():
                    return tmp
            if _is_op1(self, 'U-') and _is_op1(other, 'U-'):
                self = self.operand
            return operatorN('/', (self, other))

    def __rdiv__(self, other):
        return other.__div__(self)

    __truediv__ = __div__
    __rtruediv__ = __rdiv__

    def __neg__(self):
        try:
            fs = float(self)
        except TypeError:
            pass
        else:
            return Float(-fs)

        if _is_op1(self, 'U-'):
            return self.operand
        if _is_opNg1(self, '-') and len(self.operands) == 2:
            return operatorN('-', (self.operands[1], self.operands[0]))
        return operator1('U-', self)

    def __pos__(self):
        return self

    def __abs__(self):
        if _is_op1(self, 'U-'):
            return operator1('abs', self.operand)
        if _is_op1(self, 'exp') or _is_op1(self, 'abs'):
            return self
        return operator1('abs', self)


_Opfcn = {'-': OP.neg, 'abs': abs, 'sin': math.sin, 
   'cos': math.cos, 'exp': math.exp, 'log': math.log}

def _do_math(x, name):
    try:
        f = float(x)
    except TypeError:
        return operator1(name, x)

    return _Opfcn[name](f)


def abs(x):
    if _is_op1(x, 'abs'):
        return x
    _do_math(x, 'abs')


def cos(x):
    if _is_op1(x, 'abs'):
        return _do_math(x.operand, 'cos')
    return _do_math(x, 'cos')


def sin(x):
    return _do_math(x, 'sin')


def exp(x):
    return _do_math(x, 'exp')


def log(x):
    if _is_op1(x, 'exp'):
        return x
    return _do_math(x, 'log')


def sqrt(x):
    if _is_opNg1(x, '**') and len(x.operands) == 2 and _is_float(x.operands[1], 2.0):
        return operator1('abs', x.operands[0])
    return _do_math(x, 'sqrt')


class Expression(abstract_number, output_mixin):

    def __init__(self, value):
        abstract_number.__init__(self)
        output_mixin.__init__(self)
        self.x = coerce_into(value)
        self._check()

    def _check--- This code section failed: ---

 L. 528         0  LOAD_GLOBAL           0  'isinstance'
                3  LOAD_FAST             0  'self'
                6  LOAD_ATTR             1  'x'
                9  LOAD_GLOBAL           2  'Float'
               12  CALL_FUNCTION_2       2  None
               15  POP_JUMP_IF_TRUE     64  'to 64'
               18  LOAD_GLOBAL           0  'isinstance'
               21  LOAD_FAST             0  'self'
               24  LOAD_ATTR             1  'x'
               27  LOAD_GLOBAL           3  'abstract_number'
               30  CALL_FUNCTION_2       2  None
               33  POP_JUMP_IF_TRUE     64  'to 64'
               36  LOAD_ASSERT              AssertionError
               39  LOAD_CONST               'Bad type=%s'
               42  LOAD_GLOBAL           5  'str'
               45  LOAD_GLOBAL           6  'type'
               48  LOAD_FAST             0  'self'
               51  LOAD_ATTR             1  'x'
               54  CALL_FUNCTION_1       1  None
               57  CALL_FUNCTION_1       1  None
               60  BINARY_MODULO    
               61  RAISE_VARARGS_2       2  None

Parse error at or near `None' instruction at offset -1

    def __iadd__(self, other):
        self._check()
        ci = coerce_into(other)
        self.x = self.x + ci
        self._check()
        return self

    def __isub__(self, other):
        self._check()
        self.x = self.x - coerce_into(other)
        self._check()
        return self

    def __imul__(self, other):
        self._check()
        self.x = self.x * coerce_into(other)
        self._check()
        return self

    def __idiv__(self, other):
        self._check()
        self.x = self.x / coerce_into(other)
        self._check()
        return self

    def eval(self, env={}):
        return self.x.eval(env)

    def variables(self, env={}):
        return self.x.variables(env)

    def indices(self, variable, env={}):
        return self.x.indices(variable, env)

    def __str__(self, env={}):
        return self.x.__str__(env)

    __repr__ = __str__

    def debug(self):
        return 'E%s' % self.x.debug()

    def __float__(self):
        return float(self.x)

    def priority(self):
        return self.x.priority()

    def _complexity(self):
        return self.x.complexity()


class Name(abstract_number, output_mixin):

    def __init__(self, name):
        """This creates a named variable.   Names are
                basic parts of expressions."""
        abstract_number.__init__(self)
        output_mixin.__init__(self)
        self.name = name

    def __str__(self, env={}):
        if self.name in env:
            return str(env[self.name])
        return self.name

    __repr__ = __str__

    def eval(self, env):
        return env.get(self.name, self.name)

    def variables(self, env={}):
        if self.name in env:
            return env[self.name].variables(env)
        else:
            return sets.Set((self.name,))

    def indices(self, variable, env={}):
        if self.name in env:
            return env[self.name].indices(variable, env)
        else:
            return sets.Set()

    def debug(self):
        return '<Name %s>' % self.name

    def _complexity(self):
        return 2


class Float(abstract_number, output_mixin):

    def __init__(self, v):
        self.v = float(v)

    def eval(self, env={}):
        return self.v

    def variables(self, env={}):
        return sets.Set()

    def indices(self, variable, env={}):
        return sets.Set()

    def debug(self, env={}):
        return '<Float %g>' % self.v

    def __str__(self, env={}):
        return str(self.v)

    def __float__(self):
        return self.v

    def _complexity(self):
        return 1


def _is_float(x, v):
    try:
        f = float(x)
    except TypeError:
        return

    return f == v


class _operator(abstract_number, output_mixin):
    Priority = {'U-': 5, 'abs': 5, 'sin': 5, 'cos': 5, 'exp': 5, 'sqrt': 5, 
       'log': 5, '+': 2, 
       '-': 2, '*': 3, '/': 3, '**': 4, 
       '[]': 6}

    def __init__(self, operator):
        abstract_number.__init__(self)
        output_mixin.__init__(self)
        self.op = operator

    def priority(self):
        return self.Priority[self.op]


def coerce_into(x):
    if isinstance(x, Expression):
        x = x.x
    try:
        f = float(x)
    except TypeError:
        assert isinstance(x, abstract_number)
        assert isinstance(x, output_mixin)
        return x

    return Float(x)


class operator1(_operator):
    Printable = {'U-': '-', 'abs': 'abs', 'sin': 'math.sin', 
       'cos': 'math.cos', 'exp': 'math.exp', 
       'log': 'math.log', 'sqrt': 'math.sqrt'}

    def __init__(self, operator, operand):
        _operator.__init__(self, operator)
        self.operand = operand
        assert self.op

    def __str__(self, env={}):
        return '%s(%s)' % (self.Printable[self.op], str(self.operand))

    __repr__ = __str__

    def eval(self, env={}):
        _do_math(self.op, self.operand.eval(env))

    def variables(self, env={}):
        return self.operand.variables(env)

    def indices(self, variable, env={}):
        return self.operand.indices(variable, env)

    def debug(self):
        return '<op1:%s %s>' % (self.op, self.operand.debug())

    def _complexity(self):
        return 1 + len(self.operand)


class elementof(_operator):

    def __init__(self, array, index):
        _operator.__init__(self, '[]')
        self.array = array
        self.index = index

    def __str__(self, env={}):
        index = repr(env.get(self.index, self.index))
        array = str(env.get(self.array, self.array))
        return '%s[%s]' % (array, index)

    __repr__ = __str__

    def variables(self, env={}):
        tmp = sets.Set()
        tmp.update(self.array.variables(env))
        try:
            v = self.index.variables(env)
            tmp.update(v)
        except AttributeError:
            pass

        return tmp

    def indices(self, variable, env={}):
        tmp = sets.Set()
        if isinstance(self.array, Array) and self.array.name == variable:
            if isinstance(self.index, abstract_number):
                tmp.add(self.index.eval(env))
            else:
                tmp.add(self.index)
        return tmp

    def debug(self):
        if isinstance(self.array, Array):
            a = self.array.debug()
        else:
            a = str(self.array)
        if isinstance(self.index, abstract_number):
            i = self.index.debug()
        else:
            i = str(self.index)
        return '%s[%s]' % (a, i)

    def _complexity(self):
        if isinstance(self.array, Array):
            a = self.array._complexity()
        else:
            a = 0
        if isinstance(self.index, abstract_number):
            a += self.index._complexity()
        return a


def operatorN--- This code section failed: ---

 L. 782         0  LOAD_GLOBAL           0  'len'
                3  LOAD_FAST             1  'operands'
                6  CALL_FUNCTION_1       1  None
                9  LOAD_CONST               1
               12  COMPARE_OP            2  ==
               15  POP_JUMP_IF_FALSE    26  'to 26'

 L. 783        18  LOAD_FAST             1  'operands'
               21  LOAD_CONST               0
               24  BINARY_SUBSCR    
               25  RETURN_END_IF    
             26_0  COME_FROM            15  '15'

 L. 784        26  LOAD_CONST               0
               29  STORE_FAST            2  'nf'

 L. 785        32  SETUP_LOOP           58  'to 93'
               35  LOAD_FAST             1  'operands'
               38  GET_ITER         
               39  FOR_ITER             50  'to 92'
               42  STORE_FAST            3  'o'

 L. 786        45  SETUP_EXCEPT         24  'to 72'

 L. 787        48  LOAD_GLOBAL           1  'float'
               51  LOAD_FAST             3  'o'
               54  CALL_FUNCTION_1       1  None
               57  POP_TOP          

 L. 788        58  LOAD_FAST             2  'nf'
               61  LOAD_CONST               1
               64  INPLACE_ADD      
               65  STORE_FAST            2  'nf'
               68  POP_BLOCK        
               69  JUMP_BACK            39  'to 39'
             72_0  COME_FROM            45  '45'

 L. 789        72  DUP_TOP          
               73  LOAD_GLOBAL           2  'TypeError'
               76  COMPARE_OP           10  exception-match
               79  POP_JUMP_IF_FALSE    88  'to 88'
               82  POP_TOP          
               83  POP_TOP          
               84  POP_TOP          

 L. 790        85  JUMP_BACK            39  'to 39'
               88  END_FINALLY      
             89_0  COME_FROM            88  '88'
               89  JUMP_BACK            39  'to 39'
               92  POP_BLOCK        
             93_0  COME_FROM            32  '32'

 L. 791        93  LOAD_FAST             2  'nf'
               96  LOAD_GLOBAL           0  'len'
               99  LOAD_FAST             1  'operands'
              102  CALL_FUNCTION_1       1  None
              105  COMPARE_OP            0  <
              108  POP_JUMP_IF_TRUE    120  'to 120'
              111  LOAD_ASSERT              AssertionError
              114  LOAD_CONST               'All floats!'
              117  RAISE_VARARGS_2       2  None

 L. 792       120  LOAD_GLOBAL           4  'operatorNg1'
              123  LOAD_FAST             0  'operator'
              126  LOAD_FAST             1  'operands'
              129  CALL_FUNCTION_2       2  None
              132  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 132


class operatorNg1(_operator):

    def __init__(self, operator, operands):
        _operator.__init__(self, operator)
        assert type(operands) == type(())
        assert len(operands) > 1
        self.operands = operands

    def more(self, items):
        assert type(items) == type(())
        return operatorNg1(self.op, self.operands + items)

    def __str__(self, env={}):
        tmp = []
        p = self.priority()
        for o in self.operands:
            try:
                if o.priority() <= p:
                    tmp.append('(%s)' % o.__str__(env))
                else:
                    tmp.append(o.__str__(env))
            except AttributeError as x:
                so = str(o)
                if so.startswith('-'):
                    tmp.append('(%s)' % so)
                else:
                    tmp.append(so)

        return self.op.join(tmp)

    __repr__ = __str__

    def variables(self, env={}):
        tmp = sets.Set()
        for o in self.operands:
            tmp.update(o.variables(env))

        return tmp

    def indices(self, variable, env={}):
        tmp = sets.Set()
        for o in self.operands:
            tmp.update(o.indices(variable, env))

        return tmp

    def debug(self):
        dl = [ x.debug() for x in self.operands ]
        if len(dl) > 5:
            dl = dl[:4] + ['...']
        return '<opNg1:%s %s>' % (self.op, (' ').join(dl))

    def _complexity(self):
        c = 1
        for op in self.operands:
            c += op._complexity()

        return c


if __name__ == '__main__':
    x = 3.0
    z = 3.0
    y = Name('q')
    w = x + y + y
    print 'w=', w
    print 'wz*wz*wz=', (w + z) * (w + z) * (w + z)
    print 'w.variables()=', w.variables()
    print 'w*w.variables()=', (w * w).variables()
    print '---------- arrays --'
    a = Array('p')
    print "a['x']=", a['x']
    print 336.0 * a[5] / 336.0 - a[5] * 336.0 / 336.0
    print a[1] + a[3] + a[1]
    print a[1]
    print a[1] + a[1]
    print (a[1] + a[1] + a[1] + a[1]) / 4
    print a[1] + y + x
    print (a[1] + y + x) / 336
    print (a[1] + a[2] + a[3]) / 336
    print a[1].variables()
    print a[1].indices('p')
    print (a[1] + a[3] + a[Name('q')]).indices('p')
    print a[1].indices('b')
    print '--------Expressions-----'
    q = Expression(0.0)
    print 'Float(Expression)=', float(q)
    q += w
    print q
    print q.variables()