# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/compress-project/compress/compressor.py
# Compiled at: 2017-11-15 03:09:04
# Size of source mod 2**32: 9843 bytes
import warnings, inspect, zlib, bz2
flag_lzma = True
try:
    import lzma
except ImportError:
    try:
        from backports import lzma
    except:
        flag_lzma = False

except:
    flag_lzma = False

flag_pylzma = True
try:
    import pylzma
except:
    flag_pylzma = False

flag_snappy = True
try:
    import snappy
except:
    flag_snappy = False

flag_lz4 = True
try:
    import lz4.block
except:
    flag_lz4 = False

try:
    from . import sixmini
except:
    from compress import sixmini

_example_data = ('Hello World' * 1000).encode('utf-8')
_warning_msg = '{pkg_name} is not properly installed! please try `pip install {pkg_name}`. if you have problem to compile the .c file, download pre-built binary installation file (.whl) from https://www.lfd.uci.edu/~gohlke/pythonlibs/#{pkg_name}'

class CompressAlgorithm(object):
    name = None
    all_params = None

    @classmethod
    def validate_implement(cls):
        for com_params, decom_params in cls.all_params:
            compressed_data = cls.compress(_example_data, **com_params)
            decompressed_data = cls.decompress(compressed_data, **decom_params)
            if not _example_data == decompressed_data:
                raise AssertionError


class CompressAlgorithmsMeta(type):

    def __new__(cls, name, bases, attrs):
        klass = super(CompressAlgorithmsMeta, cls).__new__(cls, name, bases, attrs)
        _mapper = dict()
        _algorithm_list = list()
        _algorithm_class_list = list()
        for key, value in attrs.items():
            if inspect.isclass(value):
                if issubclass(value, CompressAlgorithm):
                    algo_name = key
                    algo_class = value
                    try:
                        algo_class.validate_implement()
                    except:
                        continue

                    algo_class.name = algo_class.__name__
                    _mapper[key] = {'_compress': algo_class.compress, 
                     '_decompress': algo_class.decompress}
                    _algorithm_list.append(algo_name)
                    _algorithm_class_list.append(algo_class)
                _algorithm_list.sort()

        klass._mapper = _mapper
        klass._algorithm_list = _algorithm_list
        klass._algorithm_set = set(_algorithm_list)
        klass._algorithm_class_list = _algorithm_class_list
        return klass


@sixmini.add_metaclass(CompressAlgorithmsMeta)
class CompressAlgorithms(object):
    __doc__ = "\n    Collection of string encoding algorithms. API in different API are\n    normalized.\n\n    Each algorithm's python implementation is tested, and their performance are\n    listed in class doc string. There are five level for speed and compress\n    ratio.\n\n    Speed:\n\n    5. very fast\n    4. fast\n    3. normal\n    2. slow\n    1. very slow\n\n    Compress Ratio:\n\n    5. very high\n    4. high\n    3. normal\n    2. low\n    1. very low\n\n    Reference: `Benchmark for all algorithm <https://quixdb.github.io/squash-benchmark/>`_\n    "
    _algorithm_list = list()
    _algorithm_set = set()
    _algorithm_class_list = list()

    class Zlib(CompressAlgorithm):
        __doc__ = '\n        Speed: 3\n\n        Ratio: 3\n\n        API:\n\n        - https://docs.python.org/2/library/zlib.html\n\n        or\n\n        - https://docs.python.org/3/library/zlib.html\n        '
        all_params = [({'zlib_level': zlib_level}, {}) for zlib_level in range(0, 10)]

        @staticmethod
        def compress(data, zlib_level, **kwargs):
            return zlib.compress(data, zlib_level)

        @staticmethod
        def decompress(data, **kwargs):
            return zlib.decompress(data)

    class Bz2(CompressAlgorithm):
        __doc__ = '\n        Compress Speed: 2\n\n        Decompress Speed: 1\n\n        Compress Ratio: 5\n\n        API:\n\n        - https://docs.python.org/2/library/bz2.html\n\n        or\n\n        - https://docs.python.org/3/library/bz2.html\n        '
        all_params = [({'bz2_level': bz2_level}, {}) for bz2_level in range(1, 10)]

        @staticmethod
        def compress(data, bz2_level, **kwargs):
            return bz2.compress(data, compresslevel=bz2_level)

        @staticmethod
        def decompress(data, **kwargs):
            return bz2.decompress(data)

    class LZMA(CompressAlgorithm):
        __doc__ = '\n        Speed: 1\n\n        Compress Ratio: 5\n\n        API:\n\n        - https://docs.python.org/3/library/lzma.html\n\n        or\n\n        - https://pypi.python.org/pypi/backports.lzma\n        '
        all_params = [({}, {})]

        @staticmethod
        def compress(data, **kwargs):
            return lzma.compress(data)

        @staticmethod
        def decompress(data, **kwargs):
            return lzma.decompress(data)

    class PyLZMA(CompressAlgorithm):
        all_params = [({}, {})]

        @staticmethod
        def compress(data, **kwargs):
            return pylzma.compress(data)

        @staticmethod
        def decompress(data, **kwargs):
            return pylzma.decompress(data)

    class Snappy(CompressAlgorithm):
        __doc__ = '\n        Speed: 5\n\n        Compress Ratio: 2\n\n        API:\n\n        - https://pypi.python.org/pypi/python-snappy\n        '
        all_params = [({}, {})]

        @staticmethod
        def compress(data, **kwargs):
            return snappy.compress(data)

        @staticmethod
        def decompress(data, **kwargs):
            return snappy.uncompress(data)

    class Lz4(CompressAlgorithm):
        __doc__ = '\n        Speed: 5\n\n        Compress Ratio: 2\n\n        API:\n\n        - https://pypi.python.org/pypi/lz4\n\n        '
        all_params = [
         (
          {'lz4_mode': 'default'}, {}),
         (
          {'lz4_mode': 'fast'}, {}),
         (
          {'lz4_mode': 'high_compression'}, {})]

        @staticmethod
        def compress(data, lz4_mode, **kwargs):
            return lz4.block.compress(data, mode=lz4_mode)

        @staticmethod
        def decompress(data, **kwargs):
            return lz4.block.decompress(data)


class Compressor(object):
    __doc__ = '\n    String encoder utility class.\n\n    Example::\n\n        >>> compressor = Compressor().use_zlib()\n        >>> compressor.compress(binary_data)\n        ...\n        >>> compressor.decompress(binary_data)\n        ...\n    '

    def __init__(self, algorithm=None, **kwargs):
        self.use(algorithm)

    def use(self, algo=None):
        """
        Use specified compression algorithm.

        :param algo: str or :class:`CompressAlgorithm`
        """
        if algo is None:
            return self
            try:
                algo_name = algo.__name__
            except:
                algo_name = algo

            if algo_name in CompressAlgorithms._algorithm_set:
                self._compress = CompressAlgorithms._mapper[algo_name]['_compress']
                self._decompress = CompressAlgorithms._mapper[algo_name]['_decompress']
                return self
            raise ValueError('algorithm has to be one of %r' % CompressAlgorithms._algorithm_list)

    def use_zlib(self):
        """
        Use zlib algorithm.
        """
        return self.use(CompressAlgorithms.Zlib)

    def use_bz2(self):
        """
        Use bz2 algorithm.
        """
        return self.use(CompressAlgorithms.Bz2)

    def use_lzma(self):
        """
        Use lzma algorithm.
        """
        if flag_lzma:
            return self.use(CompressAlgorithms.LZMA)
        warnings.warn(_warning_msg.format(pkg_name='backports.lzma'))

    def use_pylzma(self):
        """
        Use pylzma algorithm.
        """
        if flag_pylzma:
            return self.use(CompressAlgorithms.PyLZMA)
        warnings.warn(_warning_msg.format(pkg_name='pylzma'))

    def use_snappy(self):
        """
        Use snappy algorithm.
        """
        if flag_snappy:
            return self.use(CompressAlgorithms.Snappy)
        warnings.warn(_warning_msg.format(pkg_name='python-snappy'))

    def use_lz4(self):
        """
        Use lz4 algorithm.
        """
        if flag_lz4:
            return self.use(CompressAlgorithms.Lz4)
        warnings.warn(_warning_msg.format(pkg_name='lz4'))

    def _compress(self, data, **kwargs):
        raise NotImplementedError

    def _decompress(self, data, **kwargs):
        raise NotImplementedError

    def compress(self, data, zlib_level=6, bz2_level=9, lz4_mode='default', **kwargs):
        """
        Compress binary data.

        :return: binary data.
        """
        kwargs['zlib_level'] = zlib_level
        kwargs['bz2_level'] = bz2_level
        kwargs['lz4_mode'] = lz4_mode
        return self._compress(data, **kwargs)

    def decompress(self, data, **kwargs):
        """
        Decompress binary data.

        :return: binary data.
        """
        return self._decompress(data, **kwargs)