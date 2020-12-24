# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/site-packages/gmssl/sm4.py
# Compiled at: 2020-03-10 11:26:45
# Size of source mod 2**32: 6696 bytes
import copy
from .func import xor, rotl, get_uint32_be, put_uint32_be, bytes_to_list, list_to_bytes, padding, unpadding
SM4_BOXES_TABLE = [
 214, 144, 233, 254, 204, 225, 61, 183, 22, 182, 20, 194, 40, 251, 44,
 5, 43, 103, 154, 118, 42, 190, 4, 195, 170, 68, 19, 38, 73, 134,
 6, 153, 156, 66, 80, 244, 145, 239, 152, 122, 51, 84, 11, 67, 237,
 207, 172, 98, 228, 179, 28, 169, 201, 8, 232, 149, 128, 223, 148, 250,
 117, 143, 63, 166, 71, 7, 167, 252, 243, 115, 23, 186, 131, 89, 60,
 25, 230, 133, 79, 168, 104, 107, 129, 178, 113, 100, 218, 139, 248, 235,
 15, 75, 112, 86, 157, 53, 30, 36, 14, 94, 99, 88, 209, 162, 37,
 34, 124, 59, 1, 33, 120, 135, 212, 0, 70, 87, 159, 211, 39, 82,
 76, 54, 2, 231, 160, 196, 200, 158, 234, 191, 138, 210, 64, 199, 56,
 181, 163, 247, 242, 206, 249, 97, 21, 161, 224, 174, 93, 164, 155, 52,
 26, 85, 173, 147, 50, 48, 245, 140, 177, 227, 29, 246, 226, 46, 130,
 102, 202, 96, 192, 41, 35, 171, 13, 83, 78, 111, 213, 219, 55, 69,
 222, 253, 142, 47, 3, 255, 106, 114, 109, 108, 91, 81, 141, 27, 175,
 146, 187, 221, 188, 127, 17, 217, 92, 65, 31, 16, 90, 216, 10, 193,
 49, 136, 165, 205, 123, 189, 45, 116, 208, 18, 184, 229, 180, 176, 137,
 105, 151, 74, 12, 150, 119, 126, 101, 185, 241, 9, 197, 110, 198, 132,
 24, 240, 125, 236, 58, 220, 77, 32, 121, 238, 95, 62, 215, 203, 57,
 72]
SM4_FK = [
 2746333894, 1453994832, 1736282519, 2993693404]
SM4_CK = [
 462357, 472066609, 943670861, 1415275113,
 1886879365, 2358483617, 2830087869, 3301692121,
 3773296373, 4228057617, 404694573, 876298825,
 1347903077, 1819507329, 2291111581, 2762715833,
 3234320085, 3705924337, 4177462797, 337322537,
 808926789, 1280531041, 1752135293, 2223739545,
 2695343797, 3166948049, 3638552301, 4110090761,
 269950501, 741554753, 1213159005, 1684763257]
SM4_ENCRYPT = 0
SM4_DECRYPT = 1

class CryptSM4(object):

    def __init__(self, mode=SM4_ENCRYPT):
        self.sk = [0] * 32
        self.mode = mode

    @classmethod
    def _round_key(cls, ka):
        b = [0, 0, 0, 0]
        a = put_uint32_be(ka)
        b[0] = SM4_BOXES_TABLE[a[0]]
        b[1] = SM4_BOXES_TABLE[a[1]]
        b[2] = SM4_BOXES_TABLE[a[2]]
        b[3] = SM4_BOXES_TABLE[a[3]]
        bb = get_uint32_be(b[0:4])
        rk = bb ^ rotl(bb, 13) ^ rotl(bb, 23)
        return rk

    @classmethod
    def _f(cls, x0, x1, x2, x3, rk):

        def _sm4_l_t(ka):
            b = [
             0, 0, 0, 0]
            a = put_uint32_be(ka)
            b[0] = SM4_BOXES_TABLE[a[0]]
            b[1] = SM4_BOXES_TABLE[a[1]]
            b[2] = SM4_BOXES_TABLE[a[2]]
            b[3] = SM4_BOXES_TABLE[a[3]]
            bb = get_uint32_be(b[0:4])
            c = bb ^ rotl(bb, 2) ^ rotl(bb, 10) ^ rotl(bb, 18) ^ rotl(bb, 24)
            return c

        return x0 ^ _sm4_l_t(x1 ^ x2 ^ x3 ^ rk)

    def set_key(self, key, mode):
        key = bytes_to_list(key)
        MK = [0, 0, 0, 0]
        k = [0] * 36
        MK[0] = get_uint32_be(key[0:4])
        MK[1] = get_uint32_be(key[4:8])
        MK[2] = get_uint32_be(key[8:12])
        MK[3] = get_uint32_be(key[12:16])
        k[0:4] = xor(MK[0:4], SM4_FK[0:4])
        for i in range(32):
            k[i + 4] = k[i] ^ self._round_key(k[(i + 1)] ^ k[(i + 2)] ^ k[(i + 3)] ^ SM4_CK[i])
            self.sk[i] = k[(i + 4)]

        self.mode = mode
        if mode == SM4_DECRYPT:
            for idx in range(16):
                t = self.sk[idx]
                self.sk[idx] = self.sk[(31 - idx)]
                self.sk[31 - idx] = t

    def one_round(self, sk, in_put):
        out_put = []
        ulbuf = [
         0] * 36
        ulbuf[0] = get_uint32_be(in_put[0:4])
        ulbuf[1] = get_uint32_be(in_put[4:8])
        ulbuf[2] = get_uint32_be(in_put[8:12])
        ulbuf[3] = get_uint32_be(in_put[12:16])
        for idx in range(32):
            ulbuf[idx + 4] = self._f(ulbuf[idx], ulbuf[(idx + 1)], ulbuf[(idx + 2)], ulbuf[(idx + 3)], sk[idx])

        out_put += put_uint32_be(ulbuf[35])
        out_put += put_uint32_be(ulbuf[34])
        out_put += put_uint32_be(ulbuf[33])
        out_put += put_uint32_be(ulbuf[32])
        return out_put

    def crypt_ecb(self, input_data):
        input_data = bytes_to_list(input_data)
        if self.mode == SM4_ENCRYPT:
            input_data = padding(input_data)
        length = len(input_data)
        i = 0
        output_data = []
        while length > 0:
            output_data += self.one_round(self.sk, input_data[i:i + 16])
            i += 16
            length -= 16

        if self.mode == SM4_DECRYPT:
            return list_to_bytes(unpadding(output_data))
        else:
            return list_to_bytes(output_data)

    def crypt_cbc(self, iv, input_data):
        input_data = bytes_to_list(input_data)
        i = 0
        output_data = []
        tmp_input = [0] * 16
        iv = bytes_to_list(iv)
        if self.mode == SM4_ENCRYPT:
            input_data = padding(input_data)
            length = len(input_data)
            while length > 0:
                tmp_input[0:16] = xor(input_data[i:i + 16], iv[0:16])
                output_data += self.one_round(self.sk, tmp_input[0:16])
                iv = copy.deepcopy(output_data[i:i + 16])
                i += 16
                length -= 16

            return list_to_bytes(output_data)
        else:
            length = len(input_data)
            while length > 0:
                output_data += self.one_round(self.sk, input_data[i:i + 16])
                output_data[i:i + 16] = xor(output_data[i:i + 16], iv[0:16])
                iv = copy.deepcopy(input_data[i:i + 16])
                i += 16
                length -= 16

            return list_to_bytes(unpadding(output_data))