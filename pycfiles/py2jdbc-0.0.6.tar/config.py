# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/scott/git/py2jdbc/tests/config.py
# Compiled at: 2019-08-05 19:09:34
import os, six
from py2jdbc.jni import JNI_FALSE, JNI_TRUE, jfloat, jdouble
from py2jdbc.jvm import CP_SEP
BOOLEANS = (
 JNI_FALSE, JNI_TRUE)
MIN_BYTE = -128
MAX_BYTE = 127
MIN_CHAR = 0
MAX_CHAR = 65535
MIN_SHORT = -32768
MAX_SHORT = 32767
MIN_INT = -2147483648
MAX_INT = 2147483647
MIN_LONG = -9223372036854775808
MAX_LONG = 9223372036854775807
MIN_FLOAT = -3.4028234663852886e+38
MAX_FLOAT = 3.4028234663852886e+38
ERR_FLOAT = 1e-06
MIN_DOUBLE = -1.7976931348623157e+308
MAX_DOUBLE = 1.7976931348623157e+308
ERR_DOUBLE = 1e-30
FIELDS = (
 (
  'Z', 'boolean', JNI_TRUE, JNI_FALSE),
 ('B', 'byte', 1, 35),
 (
  'C', 'char', six.unichr(2), six.unichr(353)),
 ('S', 'short', 291, 1383),
 ('I', 'int', 1193046, 180275966),
 ('J', 'long', 4886718345, 3203386110),
 (
  'F', 'float', jfloat(123.456).value, jfloat(3.14).value),
 (
  'D', 'double', jdouble(123456.789789).value, jdouble(3.14159265).value),
 ('Ljava/lang/String;', 'string', 'abcdef', 'one two three'))
STATIC_FIELDS = (
 (
  'Z', 'Boolean', JNI_FALSE, JNI_TRUE),
 ('B', 'Byte', 4, 38),
 (
  'C', 'Char', six.unichr(8), six.unichr(33)),
 ('S', 'Short', 1110, 25920),
 ('I', 'Int', 126419235, 286401075),
 ('J', 'Long', 1450744508, 1229801703532086340),
 (
  'F', 'Float', jfloat(987.453).value, jfloat(0.000123).value),
 (
  'D', 'Double', jdouble(789.1234567).value, jdouble(-14560000000000.0).value),
 ('Ljava/lang/String;', 'String', 'Sell your cleverness and buy bewilderment.', 'Let silence take you to the core of life.'))
CWD = os.path.dirname(os.path.realpath(__file__))
LIB = os.path.join(CWD, 'lib')
SRC = os.path.join(CWD, 'src')
CLASSPATH = [
 os.path.join(SRC),
 os.path.join(LIB, 'sqlite-jdbc-3.23.1.jar')]
path = os.path.join(LIB, 'mysql-connector-java-8.0.12.jar')
HAS_MYSQL = os.path.exists(path)
if os.path.exists(path):
    CLASSPATH.append(path)
path = os.path.join(LIB, 'derby.jar')
HAS_DERBY = os.path.exists(path)
if HAS_DERBY:
    CLASSPATH.append(path)
CLASSPATH = CP_SEP.join(CLASSPATH)
DRIVER = 'org.sqlite.JDBC'
JAVA_OPTS = dict(classpath=CLASSPATH, verbose=('memory', 'gc'))