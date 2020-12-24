# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/lib.macosx-10.13-x86_64-2.7/Cheetah/Version.py
# Compiled at: 2019-09-22 10:12:27
Version = '3.2.4'
VersionTuple = (3, 2, 4, 'final', 0)
MinCompatibleVersion = '3.0.0a1'
MinCompatibleVersionTuple = (3, 0, 0, 'alpha', 1)

def convertVersionStringToTuple(s):
    versionNum = [
     0, 0, 0]
    releaseType = 'final'
    releaseTypeSubNum = 0
    if s.find('a') != -1:
        num, releaseTypeSubNum = s.split('a')
        releaseType = 'alpha'
    else:
        if s.find('b') != -1:
            num, releaseTypeSubNum = s.split('b')
            releaseType = 'beta'
        elif s.find('rc') != -1:
            num, releaseTypeSubNum = s.split('rc')
            releaseType = 'candidate'
        else:
            num = s
        num = num.split('.')
        for i in range(len(num)):
            versionNum[i] = int(num[i])

    if len(versionNum) < 3:
        versionNum += [0]
    releaseTypeSubNum = int(releaseTypeSubNum)
    return tuple(versionNum + [releaseType, releaseTypeSubNum])


if __name__ == '__main__':
    c = convertVersionStringToTuple
    print c('2.0a1')
    print c('2.0b1')
    print c('2.0rc1')
    print c('2.0')
    print c('2.0.2')
    assert c('0.9.19b1') < c('0.9.19')
    assert c('0.9b1') < c('0.9.19')
    assert c('2.0a2') > c('2.0a1')
    assert c('2.0b1') > c('2.0a2')
    assert c('2.0b2') > c('2.0b1')
    assert c('2.0b2') == c('2.0b2')
    assert c('2.0rc1') > c('2.0b1')
    assert c('2.0rc2') > c('2.0rc1')
    assert c('2.0rc2') > c('2.0b1')
    assert c('2.0') > c('2.0a1')
    assert c('2.0') > c('2.0b1')
    assert c('2.0') > c('2.0rc1')
    assert c('2.0.1') > c('2.0')
    assert c('2.0rc1') > c('2.0b1')