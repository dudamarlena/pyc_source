# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /marrow/interface/schema.py
# Compiled at: 2019-01-22 10:33:23
# Size of source mod 2**32: 3968 bytes
import inspect
from marrow.schema import Container, Attribute as Setting
undefined = object()

class Attribute(Container):
    value = Setting(default=undefined)
    exact = Setting(default=undefined)
    validator = Setting(default=None)

    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__, self.__name__)

    def __call__--- This code section failed: ---

 L.  18         0  LOAD_GLOBAL              getattr
                2  LOAD_FAST                'instance'
                4  LOAD_FAST                'self'
                6  LOAD_ATTR                __name__
                8  LOAD_GLOBAL              undefined
               10  CALL_FUNCTION_3       3  '3 positional arguments'
               12  STORE_FAST               'value'

 L.  20        14  LOAD_FAST                'value'
               16  LOAD_GLOBAL              undefined
               18  COMPARE_OP               is
               20  POP_JUMP_IF_TRUE     90  'to 90'

 L.  21        22  LOAD_FAST                'self'
               24  LOAD_ATTR                value
               26  LOAD_GLOBAL              undefined
               28  COMPARE_OP               is-not
               30  POP_JUMP_IF_FALSE    42  'to 42'
               32  LOAD_FAST                'value'
               34  LOAD_FAST                'self'
               36  LOAD_ATTR                value
               38  COMPARE_OP               !=
               40  POP_JUMP_IF_TRUE     90  'to 90'
             42_0  COME_FROM            30  '30'

 L.  22        42  LOAD_FAST                'self'
               44  LOAD_ATTR                exact
               46  LOAD_GLOBAL              undefined
               48  COMPARE_OP               is-not
               50  POP_JUMP_IF_FALSE    62  'to 62'
               52  LOAD_FAST                'value'
               54  LOAD_FAST                'self'
               56  LOAD_ATTR                exact
               58  COMPARE_OP               is-not
               60  POP_JUMP_IF_TRUE     90  'to 90'
             62_0  COME_FROM            50  '50'

 L.  23        62  LOAD_FAST                'self'
               64  LOAD_ATTR                validator
               66  POP_JUMP_IF_FALSE    78  'to 78'
               68  LOAD_FAST                'self'
               70  LOAD_METHOD              validator
               72  LOAD_FAST                'value'
               74  CALL_METHOD_1         1  '1 positional argument'
               76  POP_JUMP_IF_FALSE    90  'to 90'
             78_0  COME_FROM            66  '66'

 L.  24        78  LOAD_FAST                'self'
               80  LOAD_METHOD              check
               82  LOAD_FAST                'instance'
               84  LOAD_FAST                'value'
               86  CALL_METHOD_2         2  '2 positional arguments'
               88  POP_JUMP_IF_TRUE     94  'to 94'
             90_0  COME_FROM            76  '76'
             90_1  COME_FROM            60  '60'
             90_2  COME_FROM            40  '40'
             90_3  COME_FROM            20  '20'

 L.  25        90  LOAD_CONST               False
               92  RETURN_VALUE     
             94_0  COME_FROM            88  '88'

 L.  27        94  LOAD_CONST               True
               96  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 96

    def check(self, instance, value):
        """Basic "attribute exists" check; if we get this far, it exists."""
        return True


class Property(Attribute):
    type = Setting(default=None)

    def check--- This code section failed: ---

 L.  38         0  LOAD_GLOBAL              super
                2  LOAD_GLOBAL              Property
                4  LOAD_FAST                'self'
                6  CALL_FUNCTION_2       2  '2 positional arguments'
                8  LOAD_METHOD              check
               10  LOAD_FAST                'instance'
               12  LOAD_FAST                'value'
               14  CALL_METHOD_2         2  '2 positional arguments'
               16  POP_JUMP_IF_FALSE    36  'to 36'

 L.  39        18  LOAD_FAST                'self'
               20  LOAD_ATTR                type
               22  POP_JUMP_IF_FALSE    40  'to 40'
               24  LOAD_GLOBAL              isinstance
               26  LOAD_FAST                'value'
               28  LOAD_FAST                'self'
               30  LOAD_ATTR                type
               32  CALL_FUNCTION_2       2  '2 positional arguments'
               34  POP_JUMP_IF_TRUE     40  'to 40'
             36_0  COME_FROM            16  '16'

 L.  40        36  LOAD_CONST               None
               38  RETURN_VALUE     
             40_0  COME_FROM            34  '34'
             40_1  COME_FROM            22  '22'

 L.  42        40  LOAD_CONST               True
               42  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 42


class ClassProperty(Property):

    def check(self, instance, value):
        if not superClassPropertyself.checkinstancevalue or self.__name__ in instance.__dict__ or self.__name__ not in (attr for cls in type(instance).mro() for attr in cls.__dict__):
            return
        return True


class InstanceProperty(Property):

    def check(self, instance, value):
        if not superInstancePropertyself.checkinstancevalue or self.__name__ not in instance.__dict__:
            return
        return True


class Callable(Attribute):
    skip = 0
    args = Setting(default=None)
    optional = Setting(default=None)
    names = Setting(default=None)
    vargs = Setting(default=None)
    kwargs = Setting(default=None)

    def __init__(self, *args, **kw):
        if 'like' in kw:
            like = kw.pop'like'
        else:
            if args:
                args = list(args)
                like = args.pop0
            else:
                like = None
        (superCallableself.__init__)(*args, **kw)
        if like:
            names_, vargs, kwargs, defaults, *remainder = inspect.getfullargspeclike
            if not self.optional:
                self.optional = len(defaults) if defaults else None
            if not self.args:
                if self.names is not None:
                    self.args = len(names_) - self.skip - (self.optional or 0)
            if not self.names:
                self.names = names_[self.skip:]
        self.names = set(self.names) if self.names else None

    def check--- This code section failed: ---

 L.  99         0  LOAD_GLOBAL              super
                2  LOAD_GLOBAL              Callable
                4  LOAD_FAST                'self'
                6  CALL_FUNCTION_2       2  '2 positional arguments'
                8  LOAD_METHOD              check
               10  LOAD_FAST                'instance'
               12  LOAD_FAST                'value'
               14  CALL_METHOD_2         2  '2 positional arguments'
               16  POP_JUMP_IF_FALSE    28  'to 28'

 L. 100        18  LOAD_GLOBAL              hasattr
               20  LOAD_FAST                'value'
               22  LOAD_STR                 '__call__'
               24  CALL_FUNCTION_2       2  '2 positional arguments'
               26  POP_JUMP_IF_TRUE     32  'to 32'
             28_0  COME_FROM            16  '16'

 L. 101        28  LOAD_CONST               None
               30  RETURN_VALUE     
             32_0  COME_FROM            26  '26'

 L. 103        32  SETUP_EXCEPT         58  'to 58'

 L. 104        34  LOAD_GLOBAL              inspect
               36  LOAD_METHOD              getfullargspec
               38  LOAD_FAST                'value'
               40  CALL_METHOD_1         1  '1 positional argument'
               42  UNPACK_EX_4+0           
               44  STORE_FAST               'names'
               46  STORE_FAST               'vargs'
               48  STORE_FAST               'kwargs'
               50  STORE_FAST               'defaults'
               52  STORE_FAST               'remainder'
               54  POP_BLOCK        
               56  JUMP_FORWARD         68  'to 68'
             58_0  COME_FROM_EXCEPT     32  '32'

 L. 105        58  POP_TOP          
               60  POP_TOP          
               62  POP_TOP          

 L. 106        64  LOAD_CONST               None
               66  RETURN_VALUE     
             68_0  COME_FROM            56  '56'

 L. 108        68  LOAD_FAST                'names'
               70  POP_JUMP_IF_TRUE     76  'to 76'

 L. 109        72  BUILD_LIST_0          0 
               74  STORE_FAST               'names'
             76_0  COME_FROM            70  '70'

 L. 111        76  LOAD_FAST                'defaults'
               78  POP_JUMP_IF_FALSE    88  'to 88'
               80  LOAD_GLOBAL              len
               82  LOAD_FAST                'defaults'
               84  CALL_FUNCTION_1       1  '1 positional argument'
               86  JUMP_FORWARD         90  'to 90'
             88_0  COME_FROM            78  '78'
               88  LOAD_CONST               0
             90_0  COME_FROM            86  '86'
               90  STORE_FAST               'optional'

 L. 113        92  LOAD_FAST                'names'
               94  LOAD_CONST               None
               96  LOAD_FAST                'self'
               98  LOAD_ATTR                skip
              100  BUILD_SLICE_2         2 
              102  DELETE_SUBSCR    

 L. 115       104  LOAD_FAST                'self'
              106  LOAD_ATTR                args
              108  LOAD_CONST               None
              110  COMPARE_OP               is-not
              112  POP_JUMP_IF_FALSE   132  'to 132'
              114  LOAD_GLOBAL              len
              116  LOAD_FAST                'names'
              118  CALL_FUNCTION_1       1  '1 positional argument'
              120  LOAD_FAST                'optional'
              122  BINARY_SUBTRACT  
              124  LOAD_FAST                'self'
              126  LOAD_ATTR                args
              128  COMPARE_OP               !=
              130  POP_JUMP_IF_TRUE    198  'to 198'
            132_0  COME_FROM           112  '112'

 L. 116       132  LOAD_FAST                'self'
              134  LOAD_ATTR                names
              136  POP_JUMP_IF_FALSE   158  'to 158'
              138  LOAD_GLOBAL              set
              140  LOAD_FAST                'names'
              142  CALL_FUNCTION_1       1  '1 positional argument'
              144  LOAD_FAST                'self'
              146  LOAD_ATTR                names
              148  BINARY_AND       
              150  LOAD_FAST                'self'
              152  LOAD_ATTR                names
              154  COMPARE_OP               ==
              156  POP_JUMP_IF_FALSE   198  'to 198'
            158_0  COME_FROM           136  '136'

 L. 117       158  LOAD_FAST                'self'
              160  LOAD_ATTR                vargs
              162  POP_JUMP_IF_FALSE   168  'to 168'
              164  LOAD_FAST                'vargs'
              166  POP_JUMP_IF_FALSE   198  'to 198'
            168_0  COME_FROM           162  '162'

 L. 118       168  LOAD_FAST                'self'
              170  LOAD_ATTR                kwargs
              172  POP_JUMP_IF_FALSE   178  'to 178'
              174  LOAD_FAST                'kwargs'
              176  POP_JUMP_IF_FALSE   198  'to 198'
            178_0  COME_FROM           172  '172'

 L. 119       178  LOAD_FAST                'self'
              180  LOAD_ATTR                optional
              182  LOAD_CONST               None
              184  COMPARE_OP               is-not
              186  POP_JUMP_IF_FALSE   202  'to 202'
              188  LOAD_FAST                'optional'
              190  LOAD_FAST                'self'
              192  LOAD_ATTR                optional
              194  COMPARE_OP               !=
              196  POP_JUMP_IF_FALSE   202  'to 202'
            198_0  COME_FROM           176  '176'
            198_1  COME_FROM           166  '166'
            198_2  COME_FROM           156  '156'
            198_3  COME_FROM           130  '130'

 L. 120       198  LOAD_CONST               None
              200  RETURN_VALUE     
            202_0  COME_FROM           196  '196'
            202_1  COME_FROM           186  '186'

 L. 122       202  LOAD_CONST               True
              204  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM' instruction at offset 202_1


class Method(Callable):
    skip = 1

    def check--- This code section failed: ---

 L. 129         0  LOAD_GLOBAL              super
                2  LOAD_GLOBAL              Method
                4  LOAD_FAST                'self'
                6  CALL_FUNCTION_2       2  '2 positional arguments'
                8  LOAD_METHOD              check
               10  LOAD_FAST                'instance'
               12  LOAD_FAST                'value'
               14  CALL_METHOD_2         2  '2 positional arguments'
               16  POP_JUMP_IF_FALSE    38  'to 38'

 L. 130        18  LOAD_GLOBAL              inspect
               20  LOAD_METHOD              isclass
               22  LOAD_FAST                'instance'
               24  CALL_METHOD_1         1  '1 positional argument'
               26  POP_JUMP_IF_TRUE     42  'to 42'
               28  LOAD_GLOBAL              inspect
               30  LOAD_METHOD              ismethod
               32  LOAD_FAST                'value'
               34  CALL_METHOD_1         1  '1 positional argument'
               36  POP_JUMP_IF_TRUE     42  'to 42'
             38_0  COME_FROM            16  '16'

 L. 131        38  LOAD_CONST               None
               40  RETURN_VALUE     
             42_0  COME_FROM            36  '36'
             42_1  COME_FROM            26  '26'

 L. 133        42  LOAD_CONST               True
               44  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 44


class ClassMethod(Method):

    def check(self, instance, value):
        if not superClassMethodself.checkinstancevalue:
            return
        mro = (instance if inspect.isclassinstance else type(instance)).mro()
        for cls in mro:
            if self.__name__ in cls.__dict__ and type(cls.__dict__[self.__name__]) is classmethod:
                return True


class StaticMethod(Callable):

    def check(self, instance, value):
        if not superStaticMethodself.checkinstancevalue:
            return
        for cls in (instance if inspect.isclassinstance else type(instance)).mro():
            if self.__name__ in cls.__dict__:
                if type(cls.__dict__[self.__name__]) is staticmethod:
                    return True
                break