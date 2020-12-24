# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/libel/cipher.py
# Compiled at: 2010-08-24 22:22:10
import base64, hashlib

def encrypt(String, Password):
    password = ''
    for character in Password:
        password += hashlib.sha1(character).hexdigest()

    password = hashlib.sha1(password).hexdigest()
    encrypted = ''
    for character in String:
        encrypted_character = ord(character)
        for c in password:
            encrypted_character = encrypted_character + ord(c)

        encrypted += str(encrypted_character)

    return base64.b64encode(str(encrypted))


def decrypt(String, Password):
    password = ''
    for character in Password:
        password += hashlib.sha1(character).hexdigest()

    password = hashlib.sha1(password).hexdigest()
    decrypted = ''
    elements = []
    s = base64.b64decode(String)
    for i in xrange(len(s) / 4):
        elements.append(s[i * 4:i * 4 + 4])

    for element in elements:
        try:
            decrypted_character = int(element)
        except:
            return ''
        else:
            for c in password:
                decrypted_character -= ord(c)

            try:
                decrypted += chr(decrypted_character)
            except:
                pass

    return decrypted