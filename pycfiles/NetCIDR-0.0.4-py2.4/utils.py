# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/netcidr/utils.py
# Compiled at: 2007-12-30 21:07:23
import itertools, ipmath

def validateMask(mask):
    """
    Validate the variable length subnet masking value.

    >>> validateMask(50)
    Traceback (most recent call last):
    ValueError: The subnet mask (prefix length) must be between 0 and 32, inclusive.
    >>> validateMask('45')
    Traceback (most recent call last):
    ValueError: The subnet mask (prefix length) must be between 0 and 32, inclusive.
    >>> validateMask(32)
    >>> validateMask('27')
    >>> validateMask(17)
    >>> validateMask('0')
    >>> validateMask(-1)
    Traceback (most recent call last):
    ValueError: The subnet mask (prefix length) must be between 0 and 32, inclusive.
    >>> validateMask('-10')
    Traceback (most recent call last):
    ValueError: The subnet mask (prefix length) must be between 0 and 32, inclusive.
    """
    if 0 > int(mask) or int(mask) > 32:
        msg = 'The subnet mask (prefix length) must be between 0 and ' + '32, inclusive.'
        raise ValueError, msg


def iterIPs(startIP, endIP):
    """
    >>> ips = iterIPs('172.16.0.0', '172.16.0.8')
    >>> ips.next()
    '172.16.0.0'
    >>> ips.next()
    '172.16.0.1'
    >>> list(ips)
    ['172.16.0.2', '172.16.0.3', '172.16.0.4', '172.16.0.5', '172.16.0.6', '172.16.0.7', '172.16.0.8']
    """
    end = ipmath.octets2int(endIP) + 1
    current = ipmath.octets2int(startIP)
    while current < end:
        result = current
        current += 1
        yield ipmath.int2octets(result)


def getIPs(startIP, endIP):
    """
    A list version of the iterator iterIPs.

    >>> ips = getIPs('172.16.0.0', '172.16.0.8')
    >>> len(ips)
    9
    >>> ips
    ['172.16.0.0', '172.16.0.1', '172.16.0.2', '172.16.0.3', '172.16.0.4', '172.16.0.5', '172.16.0.6', '172.16.0.7', '172.16.0.8']
    """
    return list(iterIPs(startIP, endIP))


def _test():
    import sys, doctest
    if len(sys.argv) > 1:
        possibleObject = sys.argv[(-1)]
        if possibleObject.split('.')[0] in globals().keys():
            return doctest.run_docstring_examples(eval(possibleObject), globals(), name=possibleObject)
    return doctest.testmod()


if __name__ == '__main__':
    _test()