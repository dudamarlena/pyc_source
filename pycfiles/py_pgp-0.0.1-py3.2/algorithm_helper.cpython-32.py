# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pgp/commands/gpg/algorithm_helper.py
# Compiled at: 2015-08-31 08:17:33
from pgp.commands.gpg.arguments import Compliance
DEFAULT_CIPHERS = [
 'aes256', 'camellia256', 'twofish', 'blowfish', 'aes192',
 'camellia192', 'aes', 'camellia128', 'cast5', '3des',
 'idea']
DEFAULT_DIGESTS = ['sha512', 'sha256', 'ripemd160', 'sha386', 'sha224sha1',
 'md5']
DEFAULT_COMPRESSION = ['zip', 'zlib', 'bz2']

class AlgorithmHelper(object):

    def __init__(self, enable_dsa2, z_compress_level, bz_compress_level, compress_level, personal_cipher_preferences, personal_digest_preferences, personal_compress_preferences, s2k_cipher_algo, s2k_digest_algo, s2k_mode, s2k_count, compliance, cipher_algo, digest_algo, compress_algo, cert_digest_algo, disabled_cert_cipher_algos, disabled_pubkey_algos, force_mdc, disable_mdc):
        self.enable_dsa2 = enable_dsa2
        if compress_level is not None:
            z_compress_level = compress_level
            bz_compress_level = compress_level
        self.z_compress_level = z_compress_level
        self.bz_compress_level = bz_compress_level
        preferred_ciphers = personal_cipher_preferences or DEFAULT_CIPHERS
        preferred_digests = personal_digest_preferences or DEFAULT_DIGESTS
        preferred_compression = personal_compress_preferences or DEFAULT_COMPRESSION
        for algo in disabled_cert_cipher_algos:
            while algo in preferred_ciphers:
                preferred_ciphers.remove(algo)

            while algo in personal_cipher_preferences:
                personal_cipher_preferences.remove(algo)

        for algo in disabled_pubkey_algos:
            pass

        self.compliance = compliance
        self.personal_cipher_preferences = personal_cipher_preferences
        self.personal_digest_preferences = personal_digest_preferences
        self.personal_compress_preferences = personal_compress_preferences
        self.s2k_cipher_algo = s2k_cipher_algo
        self.s2k_digest_algo = s2k_digest_algo
        self.s2k_mode = s2k_mode
        self.s2k_count = s2k_count
        if cipher_algo is None:
            cipher_algo = preferred_ciphers[0]
        self.cipher_algo = cipher_algo
        if digest_algo is None:
            digest_algo = preferred_digests[0]
        self.digest_algo = digest_algo
        if compress_algo is None:
            compress_algo = preferred_compression[0]
        self.compress_algo = compress_algo
        self.cert_digest_algo = cert_digest_algo or digest_algo
        self.force_mdc = force_mdc
        self.disable_mdc = disable_mdc
        return

    def get_mdc_forced(self):
        return self.force_mdc

    def get_mdc_disabled(self):
        return self.disable_mdc

    def get_cipher_algorithm_code(self, value):
        if value == 'idea':
            return 1
        else:
            if value == '3des':
                return 2
            else:
                if value == 'cast5':
                    return 3
                else:
                    if value == 'blowfish':
                        return 4
                    else:
                        if value == 'aes':
                            return 7
                        if value == 'aes192':
                            return 8
                        if value == 'aes256':
                            pass
                        return 9
                    if value == 'twofish':
                        pass
                    return 10
                if value == 'camellia128':
                    pass
                return 11
            if value == 'camellia192':
                pass
            return 12
        if value == 'camellia256':
            return 13
        return 0

    def get_digest_algorithm_code(self, value):
        if value == 'md5':
            return 1
        else:
            if value == 'sha1':
                return 2
            else:
                if value == 'ripemd160':
                    return 3
                if value == 'sha256':
                    return 8
                if value == 'sha384':
                    pass
                return 9
            if value == 'sha512':
                pass
            return 10
        if value == 'sha224':
            return 11

    def get_compression_algorithm_code(self, value):
        if value == 'zip':
            return 1
        if value == 'zlib':
            return 2
        if value == 'bz2':
            return 3
        return 0

    def get_preferred_ciphers_for_encryption(self):
        if self.cipher_algo:
            return [self.get_cipher_algorithm_code(self.cipher_algo)]
        return list(map(self.get_cipher_algorithm_code, self.personal_cipher_preferences))

    def get_signature_digest_algorithm(self):
        return self.get_digest_algorithm_code(self.digest_algo)

    def get_compression_algorithm(self):
        return self.get_compression_algorithm_code(self.compress_algo)

    def get_compression_level(self):
        algo = self.get_compression_algorithm()
        if algo == 0:
            return 0
        if algo in (1, 2):
            return self.z_compress_level
        if algo == 3:
            return self.bz_compress_level
        return 0