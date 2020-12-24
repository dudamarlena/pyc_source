# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pgpdump/utils.py
# Compiled at: 2015-08-18 08:22:24
import binascii, sys
PY26 = sys.version_info[0] == 2 and sys.version_info[1] <= 6
if PY26:
    import struct

class PgpdumpException(Exception):
    """Base exception class raised by any parsing errors, etc."""
    pass


CRC24_TABLE = (0, 8801531, 9098509, 825846, 9692897, 1419802, 1651692, 10452759, 10584377,
               2608578, 2839604, 11344079, 3303384, 11807523, 12104405, 4128302,
               12930697, 4391538, 5217156, 13227903, 5679208, 13690003, 14450021,
               5910942, 6606768, 14844747, 15604413, 6837830, 16197969, 7431594,
               8256604, 16494759, 840169, 9084178, 8783076, 18463, 10434312, 1670131,
               1434117, 9678590, 11358416, 2825259, 2590173, 10602790, 4109873, 12122826,
               11821884, 3289031, 13213536, 5231515, 4409965, 12912278, 5929345,
               14431610, 13675660, 5693559, 6823513, 15618722, 14863188, 6588335,
               16513208, 8238147, 7417269, 16212302, 1680338, 10481449, 9664223,
               1391140, 9061683, 788936, 36926, 8838341, 12067563, 4091408, 3340262,
               11844381, 2868234, 11372785, 10555655, 2579964, 14478683, 5939616,
               5650518, 13661357, 5180346, 13190977, 12967607, 4428364, 8219746,
               16457881, 16234863, 7468436, 15633027, 6866552, 6578062, 14816117,
               1405499, 9649856, 10463030, 1698765, 8819930, 55329, 803287, 9047340,
               11858690, 3325945, 4072975, 12086004, 2561507, 10574104, 11387118,
               2853909, 13647026, 5664841, 5958079, 14460228, 4446803, 12949160,
               13176670, 5194661, 7454091, 16249200, 16476294, 8201341, 14834538,
               6559633, 6852199, 15647388, 3360676, 11864927, 12161705, 4185682,
               10527045, 2551230, 2782280, 11286707, 9619101, 1346150, 1577872, 10379115,
               73852, 8875143, 9172337, 899466, 16124205, 7357910, 8182816, 16421083,
               6680524, 14918455, 15678145, 6911546, 5736468, 13747439, 14507289,
               5968354, 12873461, 4334094, 5159928, 13170435, 4167245, 12180150,
               11879232, 3346363, 11301036, 2767959, 2532769, 10545498, 10360692,
               1596303, 1360505, 9604738, 913813, 9157998, 8856728, 92259, 16439492,
               8164415, 7343561, 16138546, 6897189, 15692510, 14936872, 6662099,
               5986813, 14488838, 13733104, 5750795, 13156124, 5174247, 4352529,
               12855018, 2810998, 11315341, 10498427, 2522496, 12124823, 4148844,
               3397530, 11901793, 9135439, 862644, 110658, 8912057, 1606574, 10407765,
               9590435, 1317464, 15706879, 6940164, 6651890, 14889737, 8145950, 16384229,
               16161043, 7394792, 5123014, 13133629, 12910283, 4370992, 14535975,
               5997020, 5707818, 13718737, 2504095, 10516836, 11329682, 2796649,
               11916158, 3383173, 4130419, 12143240, 8893606, 129117, 876971, 9121104,
               1331783, 9576124, 10389322, 1625009, 14908182, 6633453, 6925851, 15721184,
               7380471, 16175372, 16402682, 8127489, 4389423, 12891860, 13119266,
               5137369, 13704398, 5722165, 6015427, 14517560)

def crc24(data):
    """Implementation of the CRC-24 algorithm used by OpenPGP."""
    crc = 11994318
    crc_table = CRC24_TABLE
    for byte in data:
        tbl_idx = (crc >> 16 ^ byte) & 255
        crc = (crc_table[tbl_idx] ^ crc << 8) & 16777215

    return crc


def get_int2(data, offset):
    """Pull two bytes from data at offset and return as an integer."""
    return (data[offset] << 8) + data[(offset + 1)]


def get_int4(data, offset):
    """Pull four bytes from data at offset and return as an integer."""
    return (data[offset] << 24) + (data[(offset + 1)] << 16) + (data[(offset + 2)] << 8) + data[(offset + 3)]


def get_int8(data, offset):
    """Pull eight bytes from data at offset and return as an integer."""
    return (get_int4(data, offset) << 32) + get_int4(data, offset + 4)


def get_mpi(data, offset):
    """Gets a multi-precision integer as per RFC-4880.
    Returns the MPI and the new offset.
    See: http://tools.ietf.org/html/rfc4880#section-3.2"""
    mpi_len = get_int2(data, offset)
    offset += 2
    to_process = (mpi_len + 7) // 8
    mpi = 0
    i = -4
    for i in range(0, to_process - 3, 4):
        mpi <<= 32
        mpi += get_int4(data, offset + i)

    for j in range(i + 4, to_process):
        mpi <<= 8
        mpi += data[(offset + j)]

    offset += to_process
    return (mpi, offset)


def get_hex_data(data, offset, byte_count):
    """Pull the given number of bytes from data at offset and return as a
    hex-encoded string."""
    key_data = data[offset:offset + byte_count]
    if PY26:
        key_data = buffer(key_data)
    key_id = binascii.hexlify(key_data)
    return key_id.upper()


def get_key_id(data, offset):
    """Pull eight bytes from data at offset and return as a 16-byte hex-encoded
    string."""
    return get_hex_data(data, offset, 8)


def get_int_bytes(data):
    """Get the big-endian byte form of an integer or MPI."""
    hexval = '%X' % data
    new_len = (len(hexval) + 1) // 2 * 2
    hexval = hexval.zfill(new_len)
    return binascii.unhexlify(hexval.encode('ascii'))


def pack_data(data):
    """Pack iterable of binary data into a bytestring if necessary."""
    if PY26:
        return struct.pack(('%dB' % len(data)), *data)
    return data


def same_key(key_a, key_b):
    """Comparison function for key ID or fingerprint strings, taking into
    account varying length."""
    if len(key_a) == len(key_b):
        return key_a == key_b
    else:
        if len(key_a) < len(key_b):
            return key_b.endswith(key_a)
        return key_a.endswith(key_b)