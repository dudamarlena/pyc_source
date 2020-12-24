# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/dask_igzip/text.py
# Compiled at: 2018-06-20 12:00:16
# Size of source mod 2**32: 7994 bytes
import json, logging, os.path, dask.bag.core, dask.base, dask.bytes.core, indexed_gzip as igzip, toolz
from dask.delayed import delayed
log = logging.getLogger(__name__)
delayed = delayed(pure=True)

class InfosManager:
    __doc__ = 'Manage infos about lines\n    '

    @property
    def lines_index_path(self):
        """path of the lines index
        """
        return '%s.lines-index-%d' % (self.urlpath, self.chunk_size)

    _lines_infos = None

    def set_lines_info(self, count, line_index):
        """register lines infos
        """
        with open(self.lines_index_path, 'w') as (f):
            f.write(json.dumps({'count':count,  'chunks':len(line_index)}) + '\n')
            f.write(json.dumps({'index': line_index}) + '\n')

    def get_lines_info(self, name):
        """loads lines info, trying to avoid loading full index if not necessary
        """
        if self._lines_infos is not None:
            try:
                return self._lines_infos[name]
            except KeyError:
                pass

        self._lines_infos = {}
        try:
            with open(self.lines_index_path) as (f):
                while name not in self._lines_infos:
                    self._lines_infos.update(json.loads(next(f)))

        except FileNotFoundError:
            raise RuntimeError('Use ensure_indexes before using %r' % self)

        return self._lines_infos[name]

    @property
    def lines_index(self):
        """the lines index giving start of chunks
        """
        return self.get_lines_info('index')

    @property
    def lines_count(self):
        """number of lines in file
        """
        return self.get_lines_info('count')

    @property
    def chunks_count(self):
        """number of chunks file will be split into
        """
        return self.get_lines_info('chunks')


class IGzipReader(InfosManager):
    __doc__ = 'Indexed Gzip Reader.\n\n    It handles informations on the file,\n    as well as indexing,\n    and reading a chunk.\n\n    :param str urlpath: path of file\n    :param int chunk_size: number of line per chunk\n    :param spacing: optional param for indexed_gzip,\n      specifying the density of index\n      (a low number means a bigger index with more speed potential)\n    '

    def __init__(self, urlpath, chunk_size, spacing=1048576):
        self.urlpath = urlpath
        self.chunk_size = chunk_size
        self.spacing = spacing

    @property
    def igzip_index_path(self):
        """path of the gzip index
        """
        return '%s.gzidx' % (os.path.splitext(self.urlpath)[0],)

    def ensure_indexes(self):
        """build indexes if they don't exists yet, and save them.

        Indexes depends on spacing, and chunk_size.
        """
        if not os.path.exists(self.igzip_index_path):
            log.warning('Generating gzip index for %s' % self.urlpath)
            with igzip.IndexedGzipFile((self.urlpath), spacing=(self.spacing)) as (fobj):
                fobj.build_full_index()
                fobj.export_index(self.igzip_index_path)
        if not os.path.exists(self.lines_index_path):
            log.warning('Generating lines index for %s' % self.urlpath)
            with igzip.IndexedGzipFile((self.urlpath), index_file=(self.igzip_index_path)) as (fobj):
                line_index = []
                line_index.append(fobj.tell())
                for i, l in enumerate(fobj):
                    if (i + 1) % self.chunk_size == 0:
                        line_index.append(fobj.tell())

                count = i + 1
            self.set_lines_info(count, line_index)

    def __call__(self, chunk, limit=None):
        """read chunk in file

        :param int chunk: chunk number
        :param int limit: maximum number of lines to read. May be None.
        :return list: read lines
        """
        line_index = self.lines_index
        start = line_index[chunk]
        limit = self.chunk_size if limit is None or limit > self.chunk_size else limit
        data = []
        with igzip.IndexedGzipFile((self.urlpath), index_file=(self.igzip_index_path)) as (fobj):
            fobj.seek(start)
            for i, text in zip(range(limit), fobj):
                data.append(text)

        return data


def _read_chunk(urlpath, chunk_size, chunk, limit=None):
    """read a chunk in file.

    :param str urlpath: file path
    :param int chunk_size: number of lines per chunk
    :param int chunk: chunk number to read
    :prama int limit: if not None, limit the number of lines read

    :return list: read lines
    """
    return IGzipReader(urlpath=urlpath, chunk_size=chunk_size)(chunk, limit)


def read_lines(urlpath, chunk_size=None, storage_options=None, limit=None):
    """build read lines delayed for a set in a set of file

    For parameters, see :py:func:`read_text`

    :return list: delayed reads
    """
    spacing = storage_options.get('index_spacing', 1048576) if storage_options else 1048576
    fs, fs_token, paths = dask.bytes.core.get_fs_token_paths(urlpath,
      mode='rb', storage_options=storage_options)
    all_chunks = []
    lines_count = 0
    for path in paths:
        reader = IGzipReader(urlpath=path, chunk_size=chunk_size, spacing=spacing)
        reader.ensure_indexes()
        file_count = reader.lines_count
        if limit is not None:
            if file_count + lines_count > limit:
                file_limit = limit - lines_count
                num_chunks = file_limit // chunk_size
                remainder = file_limit % chunk_size
            else:
                num_chunks = reader.chunks_count
                remainder = 0
            chunks = [(i, None) for i in range(num_chunks)]
            if remainder:
                chunks.append((num_chunks, remainder))
            else:
                if chunks:
                    all_chunks.append(chunks)
                lines_count += file_count
                if limit is not None:
                    if remainder or lines_count >= limit:
                        break

    delayed_read = delayed(_read_chunk)
    out = []
    for path, chunks in zip(paths, all_chunks):
        token = dask.base.tokenize(fs_token, path, fs.ukey(path), 'igzip', chunks)
        keys = ['read-block-%s-%s' % (chunk[0], token) for chunk in chunks]
        out.append([delayed_read(path, chunk_size, chunk, limit, dask_key_name=key) for (chunk, limit), key in zip(chunks, keys)])

    return (False, out)


def read_text(urlpath, collection=True, chunk_size=None, storage_options=None, encoding=None, errors='strict', limit=None):
    """Given a collection of urls corresponding to gzip files,
    read their lines, and build a bag.

    :param urlpath: file(s) path
    :type urlpath: str or list of str
    :param bool collection: if False return a list of delayed
    :param chunk_size: number of lines per chunk
    :param storage_options: you may set the "spacing" for indexed gzip here.
    :param encoding: characters encoding, if None returns bytes
    :param errors: how to treat encoding errors
    :param limit: limit the global number of lines read

    :return: a bag or list of delayed

    .. note::

        `chunk_size` is an indication, on files boundary chunks are smaller.
    """
    _, blocks = read_lines(urlpath,
      chunk_size=chunk_size, storage_options=storage_options, limit=limit)
    if encoding:
        ddecode = delayed(decode)
        blocks = [ddecode(block, encoding, errors) for block in toolz.concat(blocks)]
    else:
        blocks = list(toolz.concat(blocks))
    if not collection:
        return blocks
    else:
        return dask.bag.core.from_delayed(blocks)


def decode(lines, encoding, errors):
    return [line.decode(encoding, errors) for line in lines]