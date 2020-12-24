# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: C:\Users\shu\PycharmProjects\py34\constant-project\constant\pkg\name_convention.py
# Compiled at: 2017-04-06 15:23:44
# Size of source mod 2**32: 4406 bytes
import sys, string
PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3
if PY3:
    string_types = (
     str,)
    integer_types = (int,)
else:
    string_types = (
     basestring,)
    integer_types = (int, long)
SEP = '____'
KLS_NAME_CHARSET = set(string.ascii_letters + string.digits)
VAR_NAME_CHARSET = set(string.ascii_lowercase + string.digits + '_')
VAR_FORBIDDEN_CHARSET = set('~`!@#$%^&*()-+={}[]|\\:;"\'<,>.?/' + string.ascii_uppercase)
INDEX_KEY_FORBIDDEN_CHARSET = set('~`!@#$%^&*()-+={}[]|\\:;"\'<,>.?/')
WHITE_SPACE = set(string.whitespace)

def is_valid_class_name(name):
    """Check if it is a valid variable name.
    
    A valid variable name has to:
    
    - start wither upper case
    - only alpha digits
    """
    try:
        assert name[0].isupper()
        assert len(set(name).difference(KLS_NAME_CHARSET)) == 0
        return True
    except:
        return False


def is_valid_variable_name(name):
    """Check if it is a valid variable name.
    
    A valid variable name has to:
    
    - start wither lower case
    - reserved SEPTERATOR is not in it.
    """
    try:
        assert name[0].islower()
        assert SEP not in name
        assert len(set(name).difference(VAR_NAME_CHARSET)) == 0
        return True
    except:
        return False


def is_valid_surfix(name):
    """Surfix is the attribute name used for index.
    
    **中文文档**
    
    此方法暂时没用。
    """
    try:
        assert SEP not in name
        assert len(VAR_FORBIDDEN_CHARSET.intersection(name)) == 0
        return True
    except:
        return False


def to_variable_name(cls_name):
    """Convert class name to variable name format. usually use "_" to connect
    each word.
    
    **中文文档**
    
    将类名转化为其实例的变量名。
    """
    assert is_valid_class_name(cls_name)
    words = list()
    chunks = list()
    for char in cls_name:
        if char.isupper():
            words.append(''.join(chunks))
            chunks = ['_', char.lower()]
        else:
            chunks.append(char)

    words.append(''.join(chunks))
    return ''.join(words)[1:]


def to_index_key(value):
    """Convert a value to it's index key in string.
    Only alpha and digits and underscore is allowed. Whitespace delimiter will
    replaced with underscore.
    
    ``  *David#   #John* `` -> ``David_John``
    """
    if isinstance(value, integer_types):
        key = str(value)
    else:
        if isinstance(value, string_types):
            l = list()
            for c in value:
                if c not in INDEX_KEY_FORBIDDEN_CHARSET:
                    if c in WHITE_SPACE:
                        l.append(' ')
                    else:
                        l.append(c)
                        continue

            words = [word for word in ''.join(l).strip().split(' ') if word.strip()]
            key = '_'.join(words)
        else:
            if isinstance(value, float):
                key = str(value).replace('.', 'd')
            else:
                raise TypeError('%r is not an indexable value.')
    return key


def test_is_valid_class_name():
    for name in ['User', 'MyClass', 'TestCase']:
        if not is_valid_class_name(name) is True:
            raise AssertionError

    for name in ['user', 'My_Class', 'testCase']:
        if not is_valid_class_name(name) is False:
            raise AssertionError


def test_is_valid_variable_name():
    for name in ['name', 'my_class', 'num1']:
        if not is_valid_variable_name(name) is True:
            raise AssertionError

    for name in ['Name', 'myClass', '1a']:
        if not is_valid_variable_name(name) is False:
            raise AssertionError


def test_is_valid_surfix():
    assert is_valid_surfix('大卫') is True


def test_to_variable_name():
    assert to_variable_name('User') == 'user'
    assert to_variable_name('MyClass') == 'my_class'


def test_to_index_key():
    assert to_index_key(1) == '1'
    assert to_index_key('David John') == 'David_John'
    assert to_index_key('  *David+  +John*  ') == 'David_John'
    assert to_index_key('中文') == '中文'
    assert to_index_key(' 英 文 ') == '英_文'
    assert to_index_key(3.14) == '3d14'


if __name__ == '__main__':
    test_is_valid_class_name()
    test_is_valid_variable_name()
    test_is_valid_surfix()
    test_to_variable_name()
    test_to_index_key()