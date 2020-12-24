# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/aes.py
# Compiled at: 2010-05-23 12:38:17
import os, sys, math

def append_PKCS7_padding(s):
    """return s padded to a multiple of 16-bytes by PKCS7 padding"""
    numpads = 16 - len(s) % 16
    return s + numpads * chr(numpads)


def strip_PKCS7_padding(s):
    """return s stripped of PKCS7 padding"""
    if len(s) % 16 or not s:
        raise ValueError("String of len %d can't be PCKS7-padded" % len(s))
    numpads = ord(s[(-1)])
    if numpads > 16:
        raise ValueError("String ending with %r can't be PCKS7-padded" % s[(-1)])
    return s[:-numpads]


class AES(object):
    __module__ = __name__
    keySize = dict(SIZE_128=16, SIZE_192=24, SIZE_256=32)
    sbox = [
     99, 124, 119, 123, 242, 107, 111, 197, 48, 1, 103, 43, 254, 215, 171, 118, 202, 130, 201, 125, 250, 89, 71, 240, 173, 212, 162, 175, 156, 164, 114, 192, 183, 253, 147, 38, 54, 63, 247, 204, 52, 165, 229, 241, 113, 216, 49, 21, 4, 199, 35, 195, 24, 150, 5, 154, 7, 18, 128, 226, 235, 39, 178, 117, 9, 131, 44, 26, 27, 110, 90, 160, 82, 59, 214, 179, 41, 227, 47, 132, 83, 209, 0, 237, 32, 252, 177, 91, 106, 203, 190, 57, 74, 76, 88, 207, 208, 239, 170, 251, 67, 77, 51, 133, 69, 249, 2, 127, 80, 60, 159, 168, 81, 163, 64, 143, 146, 157, 56, 245, 188, 182, 218, 33, 16, 255, 243, 210, 205, 12, 19, 236, 95, 151, 68, 23, 196, 167, 126, 61, 100, 93, 25, 115, 96, 129, 79, 220, 34, 42, 144, 136, 70, 238, 184, 20, 222, 94, 11, 219, 224, 50, 58, 10, 73, 6, 36, 92, 194, 211, 172, 98, 145, 149, 228, 121, 231, 200, 55, 109, 141, 213, 78, 169, 108, 86, 244, 234, 101, 122, 174, 8, 186, 120, 37, 46, 28, 166, 180, 198, 232, 221, 116, 31, 75, 189, 139, 138, 112, 62, 181, 102, 72, 3, 246, 14, 97, 53, 87, 185, 134, 193, 29, 158, 225, 248, 152, 17, 105, 217, 142, 148, 155, 30, 135, 233, 206, 85, 40, 223, 140, 161, 137, 13, 191, 230, 66, 104, 65, 153, 45, 15, 176, 84, 187, 22]
    rsbox = [
     82, 9, 106, 213, 48, 54, 165, 56, 191, 64, 163, 158, 129, 243, 215, 251, 124, 227, 57, 130, 155, 47, 255, 135, 52, 142, 67, 68, 196, 222, 233, 203, 84, 123, 148, 50, 166, 194, 35, 61, 238, 76, 149, 11, 66, 250, 195, 78, 8, 46, 161, 102, 40, 217, 36, 178, 118, 91, 162, 73, 109, 139, 209, 37, 114, 248, 246, 100, 134, 104, 152, 22, 212, 164, 92, 204, 93, 101, 182, 146, 108, 112, 72, 80, 253, 237, 185, 218, 94, 21, 70, 87, 167, 141, 157, 132, 144, 216, 171, 0, 140, 188, 211, 10, 247, 228, 88, 5, 184, 179, 69, 6, 208, 44, 30, 143, 202, 63, 15, 2, 193, 175, 189, 3, 1, 19, 138, 107, 58, 145, 17, 65, 79, 103, 220, 234, 151, 242, 207, 206, 240, 180, 230, 115, 150, 172, 116, 34, 231, 173, 53, 133, 226, 249, 55, 232, 28, 117, 223, 110, 71, 241, 26, 113, 29, 41, 197, 137, 111, 183, 98, 14, 170, 24, 190, 27, 252, 86, 62, 75, 198, 210, 121, 32, 154, 219, 192, 254, 120, 205, 90, 244, 31, 221, 168, 51, 136, 7, 199, 49, 177, 18, 16, 89, 39, 128, 236, 95, 96, 81, 127, 169, 25, 181, 74, 13, 45, 229, 122, 159, 147, 201, 156, 239, 160, 224, 59, 77, 174, 42, 245, 176, 200, 235, 187, 60, 131, 83, 153, 97, 23, 43, 4, 126, 186, 119, 214, 38, 225, 105, 20, 99, 85, 33, 12, 125]

    def getSBoxValue(self, num):
        """Retrieves a given S-Box Value"""
        return self.sbox[num]

    def getSBoxInvert(self, num):
        """Retrieves a given Inverted S-Box Value"""
        return self.rsbox[num]

    def rotate(self, word):
        """ Rijndael's key schedule rotate operation.

        Rotate a word eight bits to the left: eg, rotate(1d2c3a4f) == 2c3a4f1d
        Word is an char list of size 4 (32 bits overall).
        """
        return word[1:] + word[:1]

    Rcon = [
     141, 1, 2, 4, 8, 16, 32, 64, 128, 27, 54, 108, 216, 171, 77, 154, 47, 94, 188, 99, 198, 151, 53, 106, 212, 179, 125, 250, 239, 197, 145, 57, 114, 228, 211, 189, 97, 194, 159, 37, 74, 148, 51, 102, 204, 131, 29, 58, 116, 232, 203, 141, 1, 2, 4, 8, 16, 32, 64, 128, 27, 54, 108, 216, 171, 77, 154, 47, 94, 188, 99, 198, 151, 53, 106, 212, 179, 125, 250, 239, 197, 145, 57, 114, 228, 211, 189, 97, 194, 159, 37, 74, 148, 51, 102, 204, 131, 29, 58, 116, 232, 203, 141, 1, 2, 4, 8, 16, 32, 64, 128, 27, 54, 108, 216, 171, 77, 154, 47, 94, 188, 99, 198, 151, 53, 106, 212, 179, 125, 250, 239, 197, 145, 57, 114, 228, 211, 189, 97, 194, 159, 37, 74, 148, 51, 102, 204, 131, 29, 58, 116, 232, 203, 141, 1, 2, 4, 8, 16, 32, 64, 128, 27, 54, 108, 216, 171, 77, 154, 47, 94, 188, 99, 198, 151, 53, 106, 212, 179, 125, 250, 239, 197, 145, 57, 114, 228, 211, 189, 97, 194, 159, 37, 74, 148, 51, 102, 204, 131, 29, 58, 116, 232, 203, 141, 1, 2, 4, 8, 16, 32, 64, 128, 27, 54, 108, 216, 171, 77, 154, 47, 94, 188, 99, 198, 151, 53, 106, 212, 179, 125, 250, 239, 197, 145, 57, 114, 228, 211, 189, 97, 194, 159, 37, 74, 148, 51, 102, 204, 131, 29, 58, 116, 232, 203]

    def getRconValue(self, num):
        """Retrieves a given Rcon Value"""
        return self.Rcon[num]

    def core(self, word, iteration):
        """Key schedule core."""
        word = self.rotate(word)
        for i in range(4):
            word[i] = self.getSBoxValue(word[i])

        word[0] = word[0] ^ self.getRconValue(iteration)
        return word

    def expandKey(self, key, size, expandedKeySize):
        """Rijndael's key expansion.

        Expands an 128,192,256 key into an 176,208,240 bytes key

        expandedKey is a char list of large enough size,
        key is the non-expanded key.
        """
        currentSize = 0
        rconIteration = 1
        expandedKey = [0] * expandedKeySize
        for j in range(size):
            expandedKey[j] = key[j]

        currentSize += size
        while currentSize < expandedKeySize:
            t = expandedKey[currentSize - 4:currentSize]
            if currentSize % size == 0:
                t = self.core(t, rconIteration)
                rconIteration += 1
            if size == self.keySize['SIZE_256'] and currentSize % size == 16:
                for l in range(4):
                    t[l] = self.getSBoxValue(t[l])

            for m in range(4):
                expandedKey[currentSize] = expandedKey[(currentSize - size)] ^ t[m]
                currentSize += 1

        return expandedKey

    def addRoundKey(self, state, roundKey):
        """Adds (XORs) the round key to the state."""
        for i in range(16):
            state[i] ^= roundKey[i]

        return state

    def createRoundKey(self, expandedKey, roundKeyPointer):
        """Create a round key.
        Creates a round key from the given expanded key and the
        position within the expanded key.
        """
        roundKey = [
         0] * 16
        for i in range(4):
            for j in range(4):
                roundKey[j * 4 + i] = expandedKey[(roundKeyPointer + i * 4 + j)]

        return roundKey

    def galois_multiplication(self, a, b):
        """Galois multiplication of 8 bit characters a and b."""
        p = 0
        for counter in range(8):
            if b & 1:
                p ^= a
            hi_bit_set = a & 128
            a <<= 1
            a &= 255
            if hi_bit_set:
                a ^= 27
            b >>= 1

        return p

    def subBytes(self, state, isInv):
        if isInv:
            getter = self.getSBoxInvert
        else:
            getter = self.getSBoxValue
        for i in range(16):
            state[i] = getter(state[i])

        return state

    def shiftRows(self, state, isInv):
        for i in range(4):
            state = self.shiftRow(state, i * 4, i, isInv)

        return state

    def shiftRow(self, state, statePointer, nbr, isInv):
        for i in range(nbr):
            if isInv:
                state[statePointer:(statePointer + 4)] = state[statePointer + 3:statePointer + 4] + state[statePointer:statePointer + 3]
            else:
                state[statePointer:(statePointer + 4)] = state[statePointer + 1:statePointer + 4] + state[statePointer:statePointer + 1]

        return state

    def mixColumns(self, state, isInv):
        for i in range(4):
            column = state[i:i + 16:4]
            column = self.mixColumn(column, isInv)
            state[i:i + 16:4] = column

        return state

    def mixColumn(self, column, isInv):
        if isInv:
            mult = [14, 9, 13, 11]
        else:
            mult = [
             2, 1, 1, 3]
        cpy = list(column)
        g = self.galois_multiplication
        column[0] = g(cpy[0], mult[0]) ^ g(cpy[3], mult[1]) ^ g(cpy[2], mult[2]) ^ g(cpy[1], mult[3])
        column[1] = g(cpy[1], mult[0]) ^ g(cpy[0], mult[1]) ^ g(cpy[3], mult[2]) ^ g(cpy[2], mult[3])
        column[2] = g(cpy[2], mult[0]) ^ g(cpy[1], mult[1]) ^ g(cpy[0], mult[2]) ^ g(cpy[3], mult[3])
        column[3] = g(cpy[3], mult[0]) ^ g(cpy[2], mult[1]) ^ g(cpy[1], mult[2]) ^ g(cpy[0], mult[3])
        return column

    def aes_round(self, state, roundKey):
        state = self.subBytes(state, False)
        state = self.shiftRows(state, False)
        state = self.mixColumns(state, False)
        state = self.addRoundKey(state, roundKey)
        return state

    def aes_invRound(self, state, roundKey):
        state = self.shiftRows(state, True)
        state = self.subBytes(state, True)
        state = self.addRoundKey(state, roundKey)
        state = self.mixColumns(state, True)
        return state

    def aes_main(self, state, expandedKey, nbrRounds):
        state = self.addRoundKey(state, self.createRoundKey(expandedKey, 0))
        i = 1
        while i < nbrRounds:
            state = self.aes_round(state, self.createRoundKey(expandedKey, 16 * i))
            i += 1

        state = self.subBytes(state, False)
        state = self.shiftRows(state, False)
        state = self.addRoundKey(state, self.createRoundKey(expandedKey, 16 * nbrRounds))
        return state

    def aes_invMain(self, state, expandedKey, nbrRounds):
        state = self.addRoundKey(state, self.createRoundKey(expandedKey, 16 * nbrRounds))
        i = nbrRounds - 1
        while i > 0:
            state = self.aes_invRound(state, self.createRoundKey(expandedKey, 16 * i))
            i -= 1

        state = self.shiftRows(state, True)
        state = self.subBytes(state, True)
        state = self.addRoundKey(state, self.createRoundKey(expandedKey, 0))
        return state

    def encrypt(self, iput, key, size):
        output = [
         0] * 16
        nbrRounds = 0
        block = [
         0] * 16
        if size == self.keySize['SIZE_128']:
            nbrRounds = 10
        elif size == self.keySize['SIZE_192']:
            nbrRounds = 12
        elif size == self.keySize['SIZE_256']:
            nbrRounds = 14
        else:
            return
        expandedKeySize = 16 * (nbrRounds + 1)
        for i in range(4):
            for j in range(4):
                block[i + j * 4] = iput[(i * 4 + j)]

        expandedKey = self.expandKey(key, size, expandedKeySize)
        block = self.aes_main(block, expandedKey, nbrRounds)
        for k in range(4):
            for l in range(4):
                output[k * 4 + l] = block[(k + l * 4)]

        return output

    def decrypt(self, iput, key, size):
        output = [
         0] * 16
        nbrRounds = 0
        block = [
         0] * 16
        if size == self.keySize['SIZE_128']:
            nbrRounds = 10
        elif size == self.keySize['SIZE_192']:
            nbrRounds = 12
        elif size == self.keySize['SIZE_256']:
            nbrRounds = 14
        else:
            return
        expandedKeySize = 16 * (nbrRounds + 1)
        for i in range(4):
            for j in range(4):
                block[i + j * 4] = iput[(i * 4 + j)]

        expandedKey = self.expandKey(key, size, expandedKeySize)
        block = self.aes_invMain(block, expandedKey, nbrRounds)
        for k in range(4):
            for l in range(4):
                output[k * 4 + l] = block[(k + l * 4)]

        return output


class AESModeOfOperation(object):
    __module__ = __name__
    aes = AES()
    modeOfOperation = dict(OFB=0, CFB=1, CBC=2)

    def convertString(self, string, start, end, mode):
        if end - start > 16:
            end = start + 16
        if mode == self.modeOfOperation['CBC']:
            ar = [0] * 16
        else:
            ar = []
        i = start
        j = 0
        while len(ar) < end - start:
            ar.append(0)

        while i < end:
            ar[j] = ord(string[i])
            j += 1
            i += 1

        return ar

    def encrypt(self, stringIn, mode, key, size, IV):
        if len(key) % size:
            return
        if len(IV) % 16:
            return
        plaintext = []
        iput = [
         0] * 16
        output = []
        ciphertext = [0] * 16
        cipherOut = []
        firstRound = True
        if stringIn != None:
            for j in range(int(math.ceil(float(len(stringIn)) / 16))):
                start = j * 16
                end = j * 16 + 16
                if end > len(stringIn):
                    end = len(stringIn)
                plaintext = self.convertString(stringIn, start, end, mode)
                if mode == self.modeOfOperation['CFB']:
                    if firstRound:
                        output = self.aes.encrypt(IV, key, size)
                        firstRound = False
                    else:
                        output = self.aes.encrypt(iput, key, size)
                    for i in range(16):
                        if len(plaintext) - 1 < i:
                            ciphertext[i] = 0 ^ output[i]
                        elif len(output) - 1 < i:
                            ciphertext[i] = plaintext[i] ^ 0
                        elif len(plaintext) - 1 < i and len(output) < i:
                            ciphertext[i] = 0 ^ 0
                        else:
                            ciphertext[i] = plaintext[i] ^ output[i]

                    for k in range(end - start):
                        cipherOut.append(ciphertext[k])

                    iput = ciphertext
                elif mode == self.modeOfOperation['OFB']:
                    if firstRound:
                        output = self.aes.encrypt(IV, key, size)
                        firstRound = False
                    else:
                        output = self.aes.encrypt(iput, key, size)
                    for i in range(16):
                        if len(plaintext) - 1 < i:
                            ciphertext[i] = 0 ^ output[i]
                        elif len(output) - 1 < i:
                            ciphertext[i] = plaintext[i] ^ 0
                        elif len(plaintext) - 1 < i and len(output) < i:
                            ciphertext[i] = 0 ^ 0
                        else:
                            ciphertext[i] = plaintext[i] ^ output[i]

                    for k in range(end - start):
                        cipherOut.append(ciphertext[k])

                    iput = output
                elif mode == self.modeOfOperation['CBC']:
                    for i in range(16):
                        if firstRound:
                            iput[i] = plaintext[i] ^ IV[i]
                        else:
                            iput[i] = plaintext[i] ^ ciphertext[i]

                    firstRound = False
                    ciphertext = self.aes.encrypt(iput, key, size)
                    for k in range(16):
                        cipherOut.append(ciphertext[k])

        return (
         mode, len(stringIn), cipherOut)

    def decrypt(self, cipherIn, originalsize, mode, key, size, IV):
        if len(key) % size:
            return
        if len(IV) % 16:
            return
        ciphertext = []
        iput = []
        output = []
        plaintext = [
         0] * 16
        stringOut = ''
        firstRound = True
        if cipherIn != None:
            for j in range(int(math.ceil(float(len(cipherIn)) / 16))):
                start = j * 16
                end = j * 16 + 16
                if j * 16 + 16 > len(cipherIn):
                    end = len(cipherIn)
                ciphertext = cipherIn[start:end]
                if mode == self.modeOfOperation['CFB']:
                    if firstRound:
                        output = self.aes.encrypt(IV, key, size)
                        firstRound = False
                    else:
                        output = self.aes.encrypt(iput, key, size)
                    for i in range(16):
                        if len(output) - 1 < i:
                            plaintext[i] = 0 ^ ciphertext[i]
                        elif len(ciphertext) - 1 < i:
                            plaintext[i] = output[i] ^ 0
                        elif len(output) - 1 < i and len(ciphertext) < i:
                            plaintext[i] = 0 ^ 0
                        else:
                            plaintext[i] = output[i] ^ ciphertext[i]

                    for k in range(end - start):
                        stringOut += chr(plaintext[k])

                    iput = ciphertext
                elif mode == self.modeOfOperation['OFB']:
                    if firstRound:
                        output = self.aes.encrypt(IV, key, size)
                        firstRound = False
                    else:
                        output = self.aes.encrypt(iput, key, size)
                    for i in range(16):
                        if len(output) - 1 < i:
                            plaintext[i] = 0 ^ ciphertext[i]
                        elif len(ciphertext) - 1 < i:
                            plaintext[i] = output[i] ^ 0
                        elif len(output) - 1 < i and len(ciphertext) < i:
                            plaintext[i] = 0 ^ 0
                        else:
                            plaintext[i] = output[i] ^ ciphertext[i]

                    for k in range(end - start):
                        stringOut += chr(plaintext[k])

                    iput = output
                elif mode == self.modeOfOperation['CBC']:
                    output = self.aes.decrypt(ciphertext, key, size)
                    for i in range(16):
                        if firstRound:
                            plaintext[i] = IV[i] ^ output[i]
                        else:
                            plaintext[i] = iput[i] ^ output[i]

                    firstRound = False
                    if originalsize is not None and originalsize < end:
                        for k in range(originalsize - start):
                            stringOut += chr(plaintext[k])

                    else:
                        for k in range(end - start):
                            stringOut += chr(plaintext[k])

                    iput = ciphertext

        return stringOut


def encryptData(key, data, mode=AESModeOfOperation.modeOfOperation['CBC']):
    """encrypt `data` using `key`

    `key` should be a string of bytes.

    returned cipher is a string of bytes prepended with the initialization
    vector.

    """
    key = map(ord, key)
    if mode == AESModeOfOperation.modeOfOperation['CBC']:
        data = append_PKCS7_padding(data)
    keysize = len(key)
    assert keysize in AES.keySize.values(), 'invalid key size: %s' % keysize
    iv = [ ord(i) for i in os.urandom(16) ]
    moo = AESModeOfOperation()
    (mode, length, ciph) = moo.encrypt(data, mode, key, keysize, iv)
    return ('').join(map(chr, iv)) + ('').join(map(chr, ciph))


def decryptData(key, data, mode=AESModeOfOperation.modeOfOperation['CBC']):
    """decrypt `data` using `key`

    `key` should be a string of bytes.

    `data` should have the initialization vector prepended as a string of
    ordinal values.

    """
    key = map(ord, key)
    keysize = len(key)
    assert keysize in AES.keySize.values(), 'invalid key size: %s' % keysize
    iv = map(ord, data[:16])
    data = map(ord, data[16:])
    moo = AESModeOfOperation()
    decr = moo.decrypt(data, None, mode, key, keysize, iv)
    if mode == AESModeOfOperation.modeOfOperation['CBC']:
        decr = strip_PKCS7_padding(decr)
    return decr


def generateRandomKey(keysize):
    """Generates a key from random data of length `keysize`.
    
    The returned key is a string of bytes.
    
    """
    if keysize not in (16, 24, 32):
        emsg = 'Invalid keysize, %s. Should be one of (16, 24, 32).'
        raise ValueError, emsg % keysize
    return os.urandom(keysize)


if __name__ == '__main__':
    moo = AESModeOfOperation()
    cleartext = 'This is a test!'
    cypherkey = [143, 194, 34, 208, 145, 203, 230, 143, 177, 246, 97, 206, 145, 92, 255, 84]
    iv = [103, 35, 148, 239, 76, 213, 47, 118, 255, 222, 123, 176, 106, 134, 98, 92]
    (mode, orig_len, ciph) = moo.encrypt(cleartext, moo.modeOfOperation['CBC'], cypherkey, moo.aes.keySize['SIZE_128'], iv)
    print 'm=%s, ol=%s (%s), ciph=%s' % (mode, orig_len, len(cleartext), ciph)
    decr = moo.decrypt(ciph, orig_len, mode, cypherkey, moo.aes.keySize['SIZE_128'], iv)
    print decr