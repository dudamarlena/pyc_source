# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\bip_utils\bip39.py
# Compiled at: 2020-04-28 06:18:09
# Size of source mod 2**32: 13801 bytes
import os
from enum import IntEnum, unique
from .bip39_ex import Bip39InvalidFileError, Bip39ChecksumError
from . import utils

@unique
class Bip39WordsNum(IntEnum):
    __doc__ = ' Enumerative for BIP-0039 words number. '
    WORDS_NUM_12 = (12, )
    WORDS_NUM_15 = (15, )
    WORDS_NUM_18 = (18, )
    WORDS_NUM_21 = (21, )
    WORDS_NUM_24 = (24, )


@unique
class Bip39EntropyBitLen(IntEnum):
    __doc__ = ' Enumerative for BIP-0039 entropy bit lengths. '
    BIT_LEN_128 = (128, )
    BIT_LEN_160 = (160, )
    BIT_LEN_192 = (192, )
    BIT_LEN_224 = (224, )
    BIT_LEN_256 = (256, )


class Bip39Const:
    __doc__ = ' Class container for BIP39 constants. '
    ENTROPY_BIT_LEN = [
     Bip39EntropyBitLen.BIT_LEN_128,
     Bip39EntropyBitLen.BIT_LEN_160,
     Bip39EntropyBitLen.BIT_LEN_192,
     Bip39EntropyBitLen.BIT_LEN_224,
     Bip39EntropyBitLen.BIT_LEN_256]
    MNEMONIC_WORD_LEN = [
     Bip39WordsNum.WORDS_NUM_12,
     Bip39WordsNum.WORDS_NUM_15,
     Bip39WordsNum.WORDS_NUM_18,
     Bip39WordsNum.WORDS_NUM_21,
     Bip39WordsNum.WORDS_NUM_24]
    WORDS_LIST_NUM = 2048
    WORD_BITS = 11
    SEED_SALT_MOD = 'mnemonic'
    SEED_PBKDF2_ROUNDS = 2048
    SEED_LEN = 64


class EntropyGenerator:
    __doc__ = ' Entropy generator class. It generates random entropy bytes with the specified length. '

    def __init__(self, bits_len):
        """ Construct class by specifying the bits length.

        Args:
            bits_len (int or Bip39EntropyBitLen): Entropy length in bits

        Raises:
            ValueError: If the bit length is not valid
        """
        if bits_len % 8 != 0:
            raise ValueError('Bit length not multiple of 8')
        self.m_bits_len = bits_len

    def Generate(self):
        """ Generate random entropy bytes with the length specified during construction.

        Returns:
            bytes: Generated entropy bytes
        """
        return os.urandom(self.m_bits_len // 8)


class MnemonicFileReader:
    __doc__ = ' Mnemonic file reader class. It reads the English BIP39 words list from a file '
    FILE_NAME = 'bip39_wordslist_en.txt'

    def __init__(self):
        """ Construct class by reading the words list from file.

        Raises:
            Bip39InvalidFileError: If loaded words list length is not 2048
        """
        file_path = os.path.join(os.path.dirname(__file__), self.FILE_NAME)
        with open(file_path, 'r', encoding='utf-8') as (fin):
            self.m_words_list = [word.strip() for word in fin.readlines() if word.strip() != '']
        if len(self.m_words_list) != Bip39Const.WORDS_LIST_NUM:
            raise Bip39InvalidFileError('Number of loaded words list (%d) is not valid' % len(self.m_words_list))

    def GetWordIdx(self, word):
        """ Get the index of the specified word, by searching it in the list.

        Args:
            word (str): Word to be searched

        Returns:
            int: Word index

        Raises:
            ValueError: If the word is not found
        """
        idx = utils.BinarySearch(self.m_words_list, word)
        if idx == -1:
            raise ValueError('Word %s is not existent in word list' % word)
        return idx

    def GetWordAtIdx(self, word_idx):
        """ Get the word at the specified index.

        Args:
            word_idx (int): Word index

        Returns:
            str: Word at the specified index
        """
        return self.m_words_list[word_idx]


class Bip39MnemonicGenerator:
    __doc__ = ' BIP39 mnemonic generator class. It generates the mnemonic in according to BIP39.\n    Mnemonic can be generated randomly or from a specified entropy.\n    BIP-0039 specifications: https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki\n     '

    @staticmethod
    def FromWordsNumber(words_num):
        """ Generate mnemonic with the specified words number from random entropy.

        Args:
            words_num (int or Bip39WordsNum): Number of words (12, 15, 18, 21, 24)

        Returns:
            str: Generated mnemonic from random entropy

        Raises:
            ValueError: If words number is not valid
        """
        if words_num not in Bip39Const.MNEMONIC_WORD_LEN:
            raise ValueError('Words number for mnemonic (%d) is not valid' % words_num)
        entropy_bit_len = Bip39MnemonicGenerator._Bip39MnemonicGenerator__EntropyBitLenFromWordsNum(words_num)
        entropy_bytes = EntropyGenerator(entropy_bit_len).Generate()
        return Bip39MnemonicGenerator.FromEntropy(entropy_bytes)

    @staticmethod
    def FromEntropy(entropy_bytes):
        """ Generate mnemonic from the specified entropy bytes.

        Args:
            entropy_bytes (bytes): Entropy bytes (accepted lengths in bits: 128, 160, 192, 224, 256)

        Returns:
            str: Generated mnemonic from specified entropy

        Raises:
            ValueError: If entropy length is not valid
        """
        entropy_bit_len = len(entropy_bytes) * 8
        if entropy_bit_len not in Bip39Const.ENTROPY_BIT_LEN:
            raise ValueError('Entropy length in bits (%d) is not valid' % entropy_bit_len)
        entropy_hash_bytes = utils.Sha256(entropy_bytes)
        entropy_bin = utils.BytesToBinaryStr(entropy_bytes, len(entropy_bytes) * 8)
        entropy_hash_bin = utils.BytesToBinaryStr(entropy_hash_bytes, utils.Sha256DigestSize() * 8)
        checksum_bin = entropy_hash_bin[:len(entropy_bytes) // 4]
        mnemonic_entropy_bin = entropy_bin + checksum_bin
        mnemonic_reader = MnemonicFileReader()
        mnemonic = []
        for i in range(len(mnemonic_entropy_bin) // Bip39Const.WORD_BITS):
            word_idx = int(mnemonic_entropy_bin[i * Bip39Const.WORD_BITS:(i + 1) * Bip39Const.WORD_BITS], 2)
            mnemonic.append(mnemonic_reader.GetWordAtIdx(word_idx))
        else:
            return ' '.join(mnemonic)

    @staticmethod
    def __EntropyBitLenFromWordsNum(words_num):
        """ Get entropy length from words number.

        Args:
            words_num (int): Words numer

        Returns:
            int: Correspondent entropy length
        """
        return words_num * Bip39Const.WORD_BITS - words_num // 3


class Bip39MnemonicValidator:
    __doc__ = ' BIP39 mnemonic validator class. It validates a mnemonic string or list. '

    def __init__(self, mnemonic):
        """ Construct the class from mnemonic.

        Args:
            mnemonic (str or list): Mnemonic
        """
        self.m_mnemonic = mnemonic

    def Validate(self):
        """ Validate the mnemonic specified at construction.

        Returns:
            bool: True if valid, False otherwise
        """
        try:
            mnemonic_bin = self._Bip39MnemonicValidator__GetMnemonicBinaryStr()
        except ValueError:
            return False
        else:
            return self._Bip39MnemonicValidator__ComputeChecksum(mnemonic_bin) == self._Bip39MnemonicValidator__GetChecksum(mnemonic_bin)

    def GetEntropy(self):
        """Get entropy bytes from mnemonic.

        Returns:
            bytes: Entropy bytes corresponding to the mnemonic

        Raises:
            ValueError: If mnemonic is not valid
            Bip39ChecksumError: If checksum is not valid
        """
        mnemonic_bin = self._Bip39MnemonicValidator__GetMnemonicBinaryStr()
        checksum = self._Bip39MnemonicValidator__GetChecksum(mnemonic_bin)
        comp_checksum = self._Bip39MnemonicValidator__ComputeChecksum(mnemonic_bin)
        if checksum != comp_checksum:
            raise Bip39ChecksumError('Invalid checksum when getting entropy (expected %s, got %s' % (comp_checksum, checksum))
        return self._Bip39MnemonicValidator__GetEntropyBytes(mnemonic_bin)

    def __GetMnemonicBinaryStr(self):
        """ Get mnemonic binary string from mnemonic string or list.

        Returns:
           str: Mnemonic binary string

        Raises:
            ValueError: If mnemonic is not valid
        """
        mnemonic = self.m_mnemonic.split(' ') if not isinstance(self.m_mnemonic, list) else self.m_mnemonic
        if len(mnemonic) not in Bip39Const.MNEMONIC_WORD_LEN:
            raise ValueError('Mnemonic length (%d) is not valid' % len(mnemonic))
        mnemonic_reader = MnemonicFileReader()
        mnemonic_bin = map(lambda word: utils.IntToBinaryStr(mnemonic_reader.GetWordIdx(word), Bip39Const.WORD_BITS), mnemonic)
        return ''.join(mnemonic_bin)

    def __GetEntropyBytes(self, mnemonic_bin_str):
        """ Get entropy from mnemonic binary string.

        Args:
            mnemonic_bin_str (str): Mnemonic binary string

        Returns:
           bytes: Entropy bytes
        """
        checksum_len = self._Bip39MnemonicValidator__GetChecksumLen(mnemonic_bin_str)
        entropy_bin = mnemonic_bin_str[:-checksum_len]
        return utils.BytesFromBinaryStr(entropy_bin, checksum_len * 8)

    def __GetChecksum(self, mnemonic_bin_str):
        """ Get checksum from mnemonic binary string.

        Args:
            mnemonic_bin_str (str): Mnemonic binary string

        Returns:
           str: Checksum binary string
        """
        return mnemonic_bin_str[-self._Bip39MnemonicValidator__GetChecksumLen(mnemonic_bin_str):]

    def __ComputeChecksum(self, mnemonic_bin_str):
        """ Compute checksum from mnemonic binary string.

        Args:
            mnemonic_bin_str (str): Mnemonic binary string

        Returns:
           bytes: Computed checksum binary string
        """
        entropy_bytes = self._Bip39MnemonicValidator__GetEntropyBytes(mnemonic_bin_str)
        entropy_hash_bin = utils.BytesToBinaryStr(utils.Sha256(entropy_bytes), utils.Sha256DigestSize() * 8)
        checksum_bin = entropy_hash_bin[:self._Bip39MnemonicValidator__GetChecksumLen(mnemonic_bin_str)]
        return checksum_bin

    @staticmethod
    def __GetChecksumLen(mnemonic_bin_str):
        """ Get checksum length from mnemonic binary string.

        Args:
            mnemonic_bin_str (str): Mnemonic binary string

        Returns:
           int: Checksum length
        """
        return len(mnemonic_bin_str) // 33


class Bip39SeedGenerator:
    __doc__ = ' BIP39 seed generator class. It generates the seed from a mnemonic in according to BIP39. '

    def __init__(self, mnemonic):
        """ Construct the class from a specified mnemonic.

        Args:
            mnemonic (str or list): Mnemonic

        Raises:
            ValueError: If the mnemonic is not valid
        """
        if not Bip39MnemonicValidator(mnemonic).Validate():
            raise ValueError('Invalid mnemonic (%s)' % mnemonic)
        self.m_mnemonic = mnemonic

    def Generate(self, passphrase=''):
        """ Generate the seed using the specified passphrase.

        Args:
            passphrase (str, optional): Passphrase, empty if not specified

        Returns:
            bytes: Generated seed
        """
        salt = Bip39Const.SEED_SALT_MOD + passphrase
        key = utils.Pbkdf2HmacSha512(utils.StringEncode(self.m_mnemonic), utils.StringEncode(salt), Bip39Const.SEED_PBKDF2_ROUNDS)
        return key[:Bip39Const.SEED_LEN]