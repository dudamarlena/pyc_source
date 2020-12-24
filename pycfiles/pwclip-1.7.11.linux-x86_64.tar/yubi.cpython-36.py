# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pwclip/lib/secrecy/yubi.py
# Compiled at: 2020-03-20 08:07:42
# Size of source mod 2**32: 1674 bytes
"""
yubikey challenge-response lib
"""
from binascii import hexlify
from yubico import find_yubikey, yubikey, yubico_exception

def yubikeys(ykser=None, dbg=False):
    """
        return a list of yubikeys objects
        """
    keys = {}
    for i in range(0, 255):
        try:
            key = find_yubikey(debug=dbg, skip=i)
        except yubikey.YubiKeyError:
            break

        if ykser:
            if int(ykser) != int(key.serial()):
                continue
        keys[key.serial()] = key

    return keys


def ykslotchalres(yk, chal, slot):
    """
        challenge-response function using with given
        challenge (chal) for slot on yubikey found by yubikeys()
        """
    try:
        return hexlify(yk.challenge_response((str(chal).ljust(64, '\x00').encode()),
          slot=slot)).decode()
    except (AttributeError, yubico_exception.YubicoError):
        pass

    return False


def ykchalres(chal, slot=None, ykser=None):
    """
        challenge-response function using specified slot
        or default (2) as wrapping function for yubikeys() and slotchalres()
        """
    keys = yubikeys(None)
    res = None
    for ser, key in keys.items():
        slots = [2, 1] if not slot else [slot]
        for i in slots:
            res = ykslotchalres(key, chal, i)
            if res:
                return res

    return False