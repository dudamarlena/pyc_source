# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ale/progr/github/wasp-general/wasp_general/io.py
# Compiled at: 2017-12-22 01:09:04
# Size of source mod 2**32: 11739 bytes
from wasp_general.version import __author__, __version__, __credits__, __license__, __copyright__, __email__
from wasp_general.version import __status__
import io, time, gzip, bz2
from wasp_general.verify import verify_type, verify_subclass, verify_value
from wasp_general.crypto.aes import WAES
from wasp_general.crypto.hash import WHash

class WHashIO:

    def __init__(self, hash_name):
        self._WHashIO__hash_name = hash_name
        self._WHashIO__hash_obj = WHash.generator(hash_name).new(b'')

    @verify_type(b=bytes)
    def update_hash(self, b):
        self._WHashIO__hash_obj.update(b)

    def hash_name(self):
        return self._WHashIO__hash_name

    def hexdigest(self):
        return self._WHashIO__hash_obj.hexdigest()


class WResponsiveIO:

    class IOTerminated(Exception):
        pass

    def __init__(self, stop_event):
        self._WResponsiveIO__stop_event = stop_event

    def stop_event(self):
        return self._WResponsiveIO__stop_event


class WIOCounter:

    def __init__(self):
        self._WIOCounter__bytes_processed = 0
        self._WIOCounter__start_at = None
        self._WIOCounter__finished_at = None

    def bytes_processed(self):
        return self._WIOCounter__bytes_processed

    def start_counter(self):
        if self._WIOCounter__start_at is None:
            self._WIOCounter__start_at = time.time()
        else:
            raise RuntimeError('Unable to start counter two times in a row')

    def stop_counter(self):
        if self._WIOCounter__finished_at is None:
            self._WIOCounter__finished_at = time.time()

    def rate(self):
        start_at = self._WIOCounter__start_at
        if start_at is None:
            raise RuntimeError('Unable to calculate rate without start method called')
        finished_at = self._WIOCounter__finished_at
        if finished_at is None:
            finished_at = time.time()
        return self.bytes_processed() / (finished_at - start_at)

    @verify_type('paranoid', processed_bytes=int)
    def __iadd__(self, processed_bytes):
        self.increase_counter(processed_bytes)
        return self

    @verify_type(processed_bytes=int)
    def increase_counter(self, processed_bytes):
        self._WIOCounter__bytes_processed += processed_bytes

    def reset(self):
        self._WIOCounter__bytes_processed = 0
        self._WIOCounter__start_at = None
        self._WIOCounter__finished_at = None


class WThrottlingIO(WIOCounter):
    __default_maximum_timeout__ = 1.5

    @verify_type(throttling_to=(int, float, None), maximum_timeout=(int, float, None))
    @verify_value(maximum_timeout=lambda x: x is None or x > 0)
    def __init__(self, throttling_to=None, maximum_timeout=None):
        WIOCounter.__init__(self)
        self._WThrottlingIO__throttling_to = throttling_to
        self._WThrottlingIO__maximum_timeout = maximum_timeout if maximum_timeout is not None else self.__default_maximum_timeout__

    def throttling_to(self):
        return self._WThrottlingIO__throttling_to

    def maximum_timeout(self):
        return self._WThrottlingIO__maximum_timeout

    def check_rate(self):
        current_rate = self.rate()
        max_rate = self.throttling_to()
        if max_rate is not None and current_rate > max_rate:
            rate_delta = current_rate - max_rate
            sleep_time = self.bytes_processed() / rate_delta
            time.sleep(min(sleep_time, self.maximum_timeout()))


class WIOChainLink:

    def __init__(self, io_cls, *args, **kwargs):
        self._WIOChainLink__io_cls = io_cls
        self._WIOChainLink__args = args
        self._WIOChainLink__kwargs = kwargs

    def io_cls(self):
        return self._WIOChainLink__io_cls

    def io_obj(self, raw):
        return self.io_cls()(raw, *self._WIOChainLink__args, **self._WIOChainLink__kwargs)


class WIOChain:

    @verify_type(links=WIOChainLink)
    def __init__(self, last_io_obj, *links):
        self._WIOChain__chain = [last_io_obj]
        for link in links:
            next_io_obj = link.io_obj(last_io_obj)
            self._WIOChain__chain.append(next_io_obj)
            last_io_obj = next_io_obj

    def first_io(self):
        return self._WIOChain__chain[(-1)]

    def instance(self, io_cls):
        for io_obj in self:
            if isinstance(io_obj, io_cls) is True:
                return io_obj

    def __iter__(self):
        chain = self._WIOChain__chain.copy()
        chain.reverse()
        for io_obj in chain:
            yield io_obj


class WAESWriter(io.BufferedWriter):
    __doc__ = ' File-like writer with transparent encryption\n\t'

    @verify_type(cipher=WAES)
    def __init__(self, raw, cipher):
        """ Create new encryption writer

                :param cipher: cipher to use. As written data size may differ - cipher must be constructed with
                padding object
                :param raw: target file-like object to write to
                """
        io.BufferedWriter.__init__(self, raw)
        self._WAESWriter__cipher_padding = cipher.mode().padding()
        if self._WAESWriter__cipher_padding is None:
            raise ValueError('AES cipher must be created with "padding" option')
        self._WAESWriter__cipher = cipher.cipher()
        self._WAESWriter__cipher_block_size = cipher.mode().key_size()
        self._WAESWriter__buffer = b''

    @verify_type(b=(bytes, memoryview))
    def write(self, b):
        """ Encrypt and write data

                :param b: data to encrypt and write

                :return: None
                """
        self._WAESWriter__buffer += bytes(b)
        bytes_written = 0
        while len(self._WAESWriter__buffer) >= self._WAESWriter__cipher_block_size:
            io.BufferedWriter.write(self, self._WAESWriter__cipher.encrypt(self._WAESWriter__buffer[:self._WAESWriter__cipher_block_size]))
            self._WAESWriter__buffer = self._WAESWriter__buffer[self._WAESWriter__cipher_block_size:]
            bytes_written += self._WAESWriter__cipher_block_size

        return len(b)

    def flush(self):
        if len(self._WAESWriter__buffer) > 0:
            data = self._WAESWriter__cipher_padding.pad(self._WAESWriter__buffer, self._WAESWriter__cipher_block_size)
            encrypted_data = self._WAESWriter__cipher.encrypt(data)
            io.BufferedWriter.write(self, encrypted_data)
        self._WAESWriter__buffer = b''
        io.BufferedWriter.flush(self)


class WHashCalculationWriter(io.BufferedWriter, WHashIO):

    @verify_type(hash_name=str)
    def __init__(self, raw, hash_name):
        io.BufferedWriter.__init__(self, raw)
        WHashIO.__init__(self, hash_name)

    @verify_type('paranoid', b=(bytes, memoryview))
    def write(self, b):
        self.update_hash(bytes(b))
        io.BufferedWriter.write(self, b)
        return len(b)


class WThrottlingWriter(io.BufferedWriter, WThrottlingIO):

    @verify_type('paranoid', throttling_to=(int, float, None), maximum_timeout=(int, float, None))
    @verify_value('paranoid', maximum_timeout=lambda x: x is None or x > 0)
    def __init__(self, raw, throttling_to=None, maximum_timeout=None):
        io.BufferedWriter.__init__(self, raw)
        WThrottlingIO.__init__(self, throttling_to=throttling_to, maximum_timeout=maximum_timeout)
        self.start_counter()

    def close(self, *args, **kwargs):
        self.stop_counter()
        io.BufferedWriter.close(self, *args, **kwargs)

    @verify_type(b=(bytes, memoryview))
    def write(self, b):
        self.check_rate()
        io.BufferedWriter.write(self, b)
        data_length = len(b)
        self.increase_counter(data_length)
        return data_length


class WResponsiveWriter(io.BufferedWriter, WResponsiveIO):

    def __init__(self, raw, stop_event):
        io.BufferedWriter.__init__(self, raw)
        WResponsiveIO.__init__(self, stop_event)

    @verify_type(b=(bytes, memoryview))
    def write(self, b):
        if self.stop_event().is_set():
            raise WResponsiveIO.IOTerminated('Stop event was set')
        io.BufferedWriter.write(self, b)
        return len(b)


class WDiscardWriterResult(io.BufferedWriter):

    @verify_type(b=(bytes, memoryview))
    def write(self, b):
        return len(b)


class WWriterChainLink(WIOChainLink):

    @verify_subclass(writer_cls=io.BufferedWriter)
    def __init__(self, writer_cls, *args, **kwargs):
        WIOChainLink.__init__(self, writer_cls, *args, **kwargs)


class WWriterChain(WIOChain, io.BufferedWriter):

    @verify_type(links=WWriterChainLink)
    def __init__(self, last_io_obj, *links):
        WIOChain.__init__(self, last_io_obj, *links)
        io.BufferedWriter.__init__(self, self.first_io())

    def flush(self):
        io.BufferedWriter.flush(self)
        for link in self:
            link.flush()

    def close(self):
        for link in self:
            link.close()

        io.BufferedWriter.close(self)


class WBufferedIOReader(io.BufferedReader):

    def __init__(self, raw):
        io.BufferedReader.__init__(self, raw)

    def writable(self, *args, **kwargs):
        return False

    def read(self, size=-1):
        if size == 0:
            return self.read_chunk(size)
        result_buffer = self.create_buffer()
        chunk_size = io.DEFAULT_BUFFER_SIZE
        read_chunk = True
        while read_chunk is True:
            next_chunk = self.read_chunk(chunk_size)
            if size > 0:
                if chunk_size >= size:
                    read_chunk = False
                size -= chunk_size
            elif next_chunk == b'':
                read_chunk = False
            result_buffer = self.append_buffer(result_buffer, next_chunk)

        return bytes(result_buffer)

    def read_chunk(self, size):
        return self.raw.read(size)

    @classmethod
    def create_buffer(cls):
        return b''

    @classmethod
    def append_buffer(cls, buffer, data):
        buffer += data
        return buffer


class WDiscardReaderResult(WBufferedIOReader):

    @classmethod
    def append_buffer(cls, buffer, data):
        return buffer


class WGzipReader(WBufferedIOReader):

    def __init__(self, raw):
        WBufferedIOReader.__init__(self, raw)
        self._WGzipReader__gzip = gzip.GzipFile(fileobj=raw)

    def read_chunk(self, size):
        return self._WGzipReader__gzip.read(size=size)

    def close(self, *args, **kwargs):
        self._WGzipReader__gzip.close()
        WBufferedIOReader.close(self)


class WBzip2Reader(WBufferedIOReader):

    def __init__(self, raw):
        WBufferedIOReader.__init__(self, raw)
        self._WBzip2Reader__bzip2 = bz2.BZ2File(raw)

    def read_chunk(self, size):
        return self._WBzip2Reader__bzip2.read(size=size)

    def close(self, *args, **kwargs):
        self._WBzip2Reader__bzip2.close()
        WBufferedIOReader.close(self)


class WHashCalculationReader(WBufferedIOReader, WHashIO):

    @verify_type(hash_name=str)
    def __init__(self, raw, hash_name):
        WBufferedIOReader.__init__(self, raw)
        WHashIO.__init__(self, hash_name)

    def read_chunk(self, size):
        result = WBufferedIOReader.read_chunk(self, size)
        self.update_hash(result)
        return result


class WResponsiveReader(WBufferedIOReader, WResponsiveIO):

    def __init__(self, raw, stop_event):
        WBufferedIOReader.__init__(self, raw)
        WResponsiveIO.__init__(self, stop_event)

    def read_chunk(self, size):
        if self.stop_event().is_set():
            raise WResponsiveIO.IOTerminated('Stop event was set')
        return WBufferedIOReader.read_chunk(self, size)


class WThrottlingReader(WBufferedIOReader, WThrottlingIO):

    @verify_type('paranoid', throttling_to=(int, float, None), maximum_timeout=(int, float, None))
    @verify_value('paranoid', maximum_timeout=lambda x: x is None or x > 0)
    def __init__(self, raw, throttling_to=None, maximum_timeout=None):
        WBufferedIOReader.__init__(self, raw)
        WThrottlingIO.__init__(self, throttling_to=throttling_to, maximum_timeout=maximum_timeout)
        self.start_counter()

    def close(self, *args, **kwargs):
        self.stop_counter()
        WBufferedIOReader.close(self, *args, **kwargs)

    def read_chunk(self, size):
        self.check_rate()
        result = WBufferedIOReader.read_chunk(self, size)
        self.increase_counter(len(result))
        return result


class WReaderChainLink(WIOChainLink):

    @verify_subclass(reader_cls=io.BufferedReader)
    def __init__(self, reader_cls, *args, **kwargs):
        WIOChainLink.__init__(self, reader_cls, *args, **kwargs)


class WReaderChain(WIOChain, io.BufferedReader):

    @verify_type(links=WReaderChainLink)
    def __init__(self, last_io_obj, *links):
        WIOChain.__init__(self, last_io_obj, *links)
        io.BufferedReader.__init__(self, self.first_io())

    def close(self):
        for link in self:
            link.close()

        io.BufferedReader.close(self)