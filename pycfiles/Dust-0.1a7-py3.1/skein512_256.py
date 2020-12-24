# uncompyle6 version 3.7.4
# Python bytecode 3.1 (3151)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/dust/crypto/skein512_256.py
# Compiled at: 2010-05-24 14:36:08


def print_state(g, T=None, msg=None):
    if msg:
        print(msg)
    for i in range(len(g) // 8):
        print('X[{0}] ='.format(i), end='')
        for j in range(8):
            print(' {0}'.format(g[(8 * i + j)]), end='')

        print()

    if T is not None:
        for i in (0, 1):
            print('T[{0}] ='.format(i), end='')
            for j in range(8):
                print(' {0}'.format(T[(8 * i + j)]), end='')

            print()

    return


def BytesToWords(b, n):
    """Return n words for 8*n bytes."""
    return [sum(b[(8 * i + j)] << 8 * j for j in range(8)) for i in range(n)]


def WordsToBytes(w):
    """Return 8*n bytes for n words."""
    return bytearray(v >> 8 * j & 255 for v in w for j in range(8))


R = [
 [
  46, 36, 19, 37],
 [
  33, 27, 14, 42],
 [
  17, 49, 36, 39],
 [
  44, 9, 54, 56],
 [
  39, 30, 34, 24],
 [
  13, 50, 10, 17],
 [
  25, 29, 39, 43],
 [
  8, 35, 56, 22]]

def mix(d, j, x0, x1):
    r = R[(d % 8)][j]
    y0 = x0 + x1 & 18446744073709551615
    y1 = (x1 << r | x1 >> 64 - r) & 18446744073709551615
    y1 ^= y0
    return (y0, y1)


def mix_inv(d, j, y0, y1):
    r = R[(d % 8)][j]
    y1 ^= y0
    x1 = y1 >> r | y1 << 64 - r & 18446744073709551615
    x0 = y0 - x1 & 18446744073709551615
    return (x0, x1)


def subkeys(k, t):
    ek = 6148914691236517205
    for kw in k:
        ek ^= kw

    k.append(ek)
    t.append(t[0] ^ t[1])
    for s in range(19):
        sk = [k[((s + i) % 9)] for i in range(5)]
        sk.append(k[((s + 5) % 9)] + t[(s % 3)] & 18446744073709551615)
        sk.append(k[((s + 6) % 9)] + t[((s + 1) % 3)] & 18446744073709551615)
        sk.append(k[((s + 7) % 9)] + s & 18446744073709551615)
        yield sk


PI = [2, 1, 4, 7, 6, 5, 0, 3]

def threefish(key, tweak, plain):
    """'key' and 'plain' contain 64 bytes, 'tweak' contains 16 bytes."""
    k = BytesToWords(key, 8)
    t = BytesToWords(tweak, 2)
    v = BytesToWords(plain, 8)
    f = [0] * 8
    d = 0
    for sk in subkeys(k, t):
        for i in range(8):
            v[i] = v[i] + sk[i] & 18446744073709551615

        if d == 72:
            break
        for _ in range(4):
            for j in range(4):
                f[2 * j], f[2 * j + 1] = mix(d, j, v[(2 * j)], v[(2 * j + 1)])

            for i in range(8):
                v[i] = f[PI[i]]

            d += 1

    return WordsToBytes(v)


def threefish_decrypt(key, tweak, encrypted):
    """'key' and 'plain' contain 64 bytes, 'tweak' contains 16 bytes."""
    k = BytesToWords(key, 8)
    t = BytesToWords(tweak, 2)
    v = BytesToWords(encrypted, 8)
    f = [0] * 8
    d = 72
    for sk in reversed(list(subkeys(k, t))):
        for i in range(8):
            v[i] = v[i] - sk[i] & 18446744073709551615

        if d == 0:
            break
        for _ in range(4):
            d -= 1
            for i in range(8):
                f[PI[i]] = v[i]

            for j in range(4):
                v[2 * j], v[2 * j + 1] = mix_inv(d, j, f[(2 * j)], f[(2 * j + 1)])

    return WordsToBytes(v)


def ubi(g, m, ts):
    m = bytearray(m)
    l = len(m)
    if l == 0 or l % 64 != 0:
        m.extend([0] * (64 - l % 64))
    h = bytearray(g)
    ts_pos = ts
    for i in range(0, len(m), 64):
        block = m[i:i + 64]
        ts_pos += 64
        tweak = ts_pos
        if i == 0:
            tweak |= 85070591730234615865843651857942052864
        if i == len(m) - 64:
            tweak |= 170141183460469231731687303715884105728
            tweak -= len(m) - l
        tweak_bytes = WordsToBytes([tweak & 18446744073709551615, tweak >> 64])
        cipher = threefish(h, tweak_bytes, block)
        h = bytearray(x ^ y for x, y in zip(cipher, block))

    return h


CONFIG = b'SHA3\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00'

def skein512_256(msg, mac=b'', pers=b'', nonce=b'', tree=None):
    tree_leaf, tree_fan, tree_max = tree if tree is not None else (0, 0, 0)
    g = bytes(64)
    if mac:
        g = ubi(g, mac, 0)
    config = CONFIG + bytes((tree_leaf, tree_fan, tree_max)) + bytes(13)
    g = ubi(g, config, 5316911983139663491615228241121378304)
    if pers:
        g = ubi(g, pers, 10633823966279326983230456482242756608)
    if nonce:
        g = ubi(g, nonce, 26584559915698317458076141205606891520)
    if tree_leaf == tree_fan == tree_max == 0:
        g = ubi(g, msg, 63802943797675961899382738893456539648)
    else:
        if tree_leaf < 1:
            raise ValueError('tree leaf parameter has to be >= 1')
        if tree_fan < 1:
            raise ValueError('tree fan-out parameter has to be >= 1')
        if tree_max < 2:
            raise ValueError('maximum tree depth parameter has to be >= 2')
        g = tree_hash(g, msg, 64 * 2 ** tree_leaf, 2 ** tree_fan, tree_max)
    g = ubi(g, bytes(8), 83741363734449699992939844797661708288)[:32]
    return g


def tree_hash(g, msg, leaf_size, children, max_level):
    if msg:
        blocks = [msg[i * leaf_size:(i + 1) * leaf_size] for i in range((len(msg) - 1) // leaf_size + 1)]
    else:
        blocks = [
         b'']
    blocks = [ubi(g, block, i * leaf_size | 5192296858534827628530496329220096 | 63802943797675961899382738893456539648) for i, block in enumerate(blocks)]
    level = 2
    while level < max_level and len(blocks) > 1:
        blocks = [(b'').join(blocks[i * children:(i + 1) * children]) for i in range((len(blocks) - 1) // children + 1)]
        blocks = [ubi(g, block, 64 * i * children | level << 112 | 63802943797675961899382738893456539648) for i, block in enumerate(blocks)]
        level += 1

    if len(blocks) == 1:
        return blocks[0]
    else:
        return ubi(g, (b'').join(blocks), max_level << 112 | 63802943797675961899382738893456539648)


if __name__ == '__main__':
    MSG = b'Nobody inspects the spammish repetition'
    hash = skein512_256(MSG)
    print(':Skein-512:   256-bit hash, msgLen = {0:5} bits'.format(len(MSG) * 8))
    print('\nMessage:', MSG)
    print('Result:')
    for i in range(0, len(hash), 16):
        print('     ', end='')
        for j in range(i, i + 16, 4):
            print(' '.join(format(b, '02X') for b in hash[j:j + 4]), end='  ')

        print()