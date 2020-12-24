# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/will/.virtualenvs/datasight-backend/lib/python2.7/site-packages/dejavu/__init__.py
# Compiled at: 2015-04-19 17:14:05
from dejavu.database import get_database, Database
import dejavu.decoder as decoder, fingerprint, multiprocessing, os, traceback, sys

class Dejavu(object):
    SONG_ID = 'song_id'
    SONG_NAME = 'song_name'
    CONFIDENCE = 'confidence'
    MATCH_TIME = 'match_time'
    OFFSET = 'offset'
    OFFSET_SECS = 'offset_seconds'

    def __init__(self, config):
        super(Dejavu, self).__init__()
        self.config = config
        db_cls = get_database(config.get('database_type', None))
        self.db = db_cls(**config.get('database', {}))
        self.db.setup()
        self.limit = self.config.get('fingerprint_limit', None)
        if self.limit == -1:
            self.limit = None
        self.get_fingerprinted_songs()
        return

    def get_fingerprinted_songs(self):
        self.songs = self.db.get_songs()
        self.songhashes_set = set()
        for song in self.songs:
            song_hash = song[Database.FIELD_FILE_SHA1]
            self.songhashes_set.add(song_hash)

    def fingerprint_directory(self, path, extensions, nprocesses=None):
        try:
            nprocesses = nprocesses or multiprocessing.cpu_count()
        except NotImplementedError:
            nprocesses = 1
        else:
            nprocesses = 1 if nprocesses <= 0 else nprocesses

        pool = multiprocessing.Pool(nprocesses)
        filenames_to_fingerprint = []
        for filename, _ in decoder.find_files(path, extensions):
            if decoder.unique_hash(filename) in self.songhashes_set:
                print '%s already fingerprinted, continuing...' % filename
                continue
            filenames_to_fingerprint.append(filename)

        worker_input = zip(filenames_to_fingerprint, [
         self.limit] * len(filenames_to_fingerprint))
        iterator = pool.imap_unordered(_fingerprint_worker, worker_input)
        while True:
            try:
                song_name, hashes, file_hash = iterator.next()
            except multiprocessing.TimeoutError:
                continue
            except StopIteration:
                break
            except:
                print 'Failed fingerprinting'
                traceback.print_exc(file=sys.stdout)
            else:
                sid = self.db.insert_song(song_name, file_hash)
                self.db.insert_hashes(sid, hashes)
                self.db.set_song_fingerprinted(sid)
                self.get_fingerprinted_songs()

        pool.close()
        pool.join()

    def fingerprint_file(self, filepath, song_name=None):
        songname = decoder.path_to_songname(filepath)
        song_hash = decoder.unique_hash(filepath)
        song_name = song_name or songname
        if song_hash in self.songhashes_set:
            print '%s already fingerprinted, continuing...' % song_name
        else:
            song_name, hashes, file_hash = _fingerprint_worker(filepath, self.limit, song_name=song_name)
            sid = self.db.insert_song(song_name, file_hash)
            self.db.insert_hashes(sid, hashes)
            self.db.set_song_fingerprinted(sid)
            self.get_fingerprinted_songs()

    def find_matches(self, samples, Fs=fingerprint.DEFAULT_FS):
        hashes = fingerprint.fingerprint(samples, Fs=Fs)
        return self.db.return_matches(hashes)

    def align_matches(self, matches):
        """
            Finds hash matches that align in time with other matches and finds
            consensus about which hashes are "true" signal from the audio.

            Returns a dictionary with match information.
        """
        diff_counter = {}
        largest = 0
        largest_count = 0
        song_id = -1
        for tup in matches:
            sid, diff = tup
            if diff not in diff_counter:
                diff_counter[diff] = {}
            if sid not in diff_counter[diff]:
                diff_counter[diff][sid] = 0
            diff_counter[diff][sid] += 1
            if diff_counter[diff][sid] > largest_count:
                largest = diff
                largest_count = diff_counter[diff][sid]
                song_id = sid

        song = self.db.get_song_by_id(song_id)
        if song:
            songname = song.get(Dejavu.SONG_NAME, None)
        else:
            return
        nseconds = round(float(largest) / fingerprint.DEFAULT_FS * fingerprint.DEFAULT_WINDOW_SIZE * fingerprint.DEFAULT_OVERLAP_RATIO, 5)
        song = {Dejavu.SONG_ID: song_id, 
           Dejavu.SONG_NAME: songname, 
           Dejavu.CONFIDENCE: largest_count, 
           Dejavu.OFFSET: int(largest), 
           Dejavu.OFFSET_SECS: nseconds, 
           Database.FIELD_FILE_SHA1: song.get(Database.FIELD_FILE_SHA1, None)}
        return song

    def recognize(self, recognizer, *options, **kwoptions):
        r = recognizer(self)
        return r.recognize(*options, **kwoptions)


def _fingerprint_worker(filename, limit=None, song_name=None):
    try:
        filename, limit = filename
    except ValueError:
        pass

    songname, extension = os.path.splitext(os.path.basename(filename))
    song_name = song_name or songname
    channels, Fs, file_hash = decoder.read(filename, limit)
    result = set()
    channel_amount = len(channels)
    for channeln, channel in enumerate(channels):
        print 'Fingerprinting channel %d/%d for %s' % (channeln + 1,
         channel_amount,
         filename)
        hashes = fingerprint.fingerprint(channel, Fs=Fs)
        print 'Finished channel %d/%d for %s' % (channeln + 1, channel_amount,
         filename)
        result |= set(hashes)

    return (song_name, result, file_hash)


def chunkify(lst, n):
    """
    Splits a list into roughly n equal parts.
    http://stackoverflow.com/questions/2130016/splitting-a-list-of-arbitrary-size-into-only-roughly-n-equal-parts
    """
    return [ lst[i::n] for i in xrange(n) ]