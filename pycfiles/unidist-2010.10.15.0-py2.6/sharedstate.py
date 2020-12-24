# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/unidist/sharedstate.py
# Compiled at: 2010-10-15 01:55:45
"""
sharedstate

Shared State module.  Get access to shared state.

All state has a namespace, and then the state id.  sharecounter is used to
procure new state ids, so it can be incremented atomically and shared with
other procblock programs.

TODO(g): Implement serialization, archiving, snapshotting, and replication to
sharestate.  This will allow us flexibility in many things.  This is not
necessarily going to be the best scaling solution, but it will work and provide
a way to keep state and distribute.  Name spaces should have this specified
individually.  If not specified, state will not be archived, serialized,
snapshotted or replicated.

  * Use the "archive" and "snapshot" modules for this, so archival and
      snapshotting is universal.  Ensure a process restart will do the right
      thing in attempting to restore from snapshot, then archive, if present.
      
      TODO(g): Merge achive and snapshot.  They are the same technology.  If we
          really want to keep state, then we must archive each transactions and
          snapshot to avoid having to replay too many archives.
"""
import threading, time, run, yaml, os, logging, glob, re
from log import log
import threadsafedict, threadsafelist
MAX_SEARCH_DEPTH = 10
SHARED_STATE = threadsafedict.ThreadSafeDict()
SHARED_STATE_LOCKS = threadsafedict.ThreadSafeDict_IgnoreOverwrites()

class StateBucketDoesntExist(Exception):
    """This state bucket does not exist, so it cannot by returned."""
    pass


class StateBucketNotFound(Exception):
    """This state bucket was not found.  Different than it having a value of None."""
    pass


class StateKeyNotFound(Exception):
    """This state key was not found.  Different than it having a value of None."""
    pass


def _LockState(bucket):
    global SHARED_STATE_LOCKS
    if bucket not in SHARED_STATE_LOCKS:
        SHARED_STATE_LOCKS[bucket] = threading.Lock()
    SHARED_STATE_LOCKS[bucket].acquire()


def _UnlockState(bucket):
    if bucket not in SHARED_STATE_LOCKS:
        raise StateDoesntExist('Not found: %s' % bucket)
    SHARED_STATE_LOCKS[bucket].release()


def _EnsureBucketExists(bucket):
    global SHARED_STATE
    _LockState(bucket)
    if bucket not in SHARED_STATE:
        SHARED_STATE[bucket] = threadsafedict.ThreadSafeDict()
    _UnlockState(bucket)


def _Search_Dict(data, value, depth=0):
    """Search for the value in data (dict)."""
    results = []
    if depth > MAX_SEARCH_DEPTH:
        return []
    matched_data = False
    for key in data:
        key_data = data[key]
        if type(key_data) == type({}) or isinstance(key_data, threadsafedict.ThreadSafeDict):
            results += _Search_Dict(key_data, value, depth=depth + 1)
        elif not matched_data and _Search_NonDict_IsMatch(key_data, value):
            matched_data = True
            results.append(data)

    return results


def _Search_NonDict_IsMatch(data, value):
    """Looks at data in a non-dictionary, and returns Boolean if anything mathches"""
    if type(data) == type([]) or isinstance(data, threadsafelist.ThreadSafeList):
        for item in data:
            if re.findall(value, str(item), re.IGNORECASE):
                return True

        return False
    else:
        if re.findall(value, str(data), re.IGNORECASE):
            return True
        return False


def RegisterDefaultSave(bucket, save):
    """Registers a default save file for a specified bucket."""
    Set('__sharedstate.save.registered', bucket, save)
    log('Registered Shared State Save: Bucket: %s  Save: %s' % (bucket, save))


def GetRegisteredSave(bucket):
    """If registered, returns the save file.  None if not found."""
    _EnsureBucketExists('__sharedstate.save.registered')
    if bucket in SHARED_STATE['__sharedstate.save.registered']:
        return SHARED_STATE['__sharedstate.save.registered'][bucket]
    else:
        return
        return


def Search(value, bucket_regex=None, key_regex=None):
    """Searchs through the specified bucket and key regexs."""
    results = []
    buckets = GetBuckets()
    for bucket in buckets:
        if bucket_regex:
            match = re.findall(bucket_regex, bucket, re.IGNORECASE)
        else:
            match = True
        if match:
            bucket_data = GetBucketData(bucket)
            if type(bucket_data) == type({}) or isinstance(bucket_data, threadsafedict.ThreadSafeDict):
                results += _Search_Dict(bucket_data, value, depth=0)

    return results


def GetBuckets():
    """Returns a list of strings, names of buckets."""
    return SHARED_STATE.keys()


def BucketExists(bucket):
    """A bucket exists.
  
  Args:
    bucket: string, name of bucket for state variables
  """
    try:
        _LockState(bucket)
        exists = bucket in SHARED_STATE
        return exists
    finally:
        _UnlockState(bucket)


def KeyExists(bucket, key, strict=False):
    """A key exists inside a bucket.
  
  Args:
    bucket: string, name of bucket for state variables
    key: string or any, key to store data against.  Any valid dict key.
    string: boolean (default=False), if True, will raise StateBucketDoesntExist,
        if False, returns False, in case the bucket doesnt exist
  """
    if not BucketExists(bucket):
        if strict:
            raise StateBucketDoesntExist('Bucket doesnt exist: %s' % bucket)
        else:
            return False
    exists = key in SHARED_STATE[bucket]
    return exists


def RemoveKey(bucket, key, strict=False, save=None, backups=2, delay=0, remote_node_sync=None, remote_node_url=None, remote_node_delay=None):
    """Removes a key from a bucket.
  
  Args:
    bucket: string, name of bucket for state variables
    key: string or any, key to store data against.  Will remove this key.
    string: boolean (default=False), if True, will raise StateBucketDoesntExist,
        if False, returns False, in case the bucket doesnt exist
  """
    if save == None:
        save = GetRegisteredSave(bucket)
    if not BucketExists(bucket):
        if strict:
            raise StateBucketDoesntExist('Bucket doesnt exist: %s' % bucket)
        else:
            return False
    if key in SHARED_STATE[bucket]:
        del SHARED_STATE[bucket][key]
        if save:
            if '%s' in save:
                save = save.replace('%s', '%(key)s')
            if '%(key)s' in save:
                save_path = save % {'key': run.MakePathSafeToCreate(key)}
                os.unlink(save_path)
                log('Removed key save file: %s' % save_path)
            else:
                Save(bucket, key, save=save, backups=backups, delay=delay, remote_node_sync=remote_node_sync, remote_node_url=remote_node_url, remote_node_delay=remote_node_delay)
    elif strict:
        raise StateKeyNotFound((bucket, key))
    return True


def GetBucketKeys(bucket, strict=False):
    """Returns the keys in a bucket.
  
  Args:
    bucket: string, name of bucket for state variables
  
  NOTE(g): Having a "GetKeys()" function is rejected, due to it being confusing.
  """
    if not BucketExists(bucket):
        if strict:
            raise StateBucketDoesntExist('Bucket doesnt exist: %s' % bucket)
        else:
            return []
    keys = SHARED_STATE[bucket].keys()
    return keys


def GetBucketData(bucket, default=None):
    """Returns the data in a bucket.
  
  Args:
    bucket: string, name of bucket for state variables
  
  NOTE(g): Having a "GetKeys()" function is rejected, due to it being confusing.
  """
    if not BucketExists(bucket):
        if default == None:
            raise StateBucketDoesntExist('Bucket doesnt exist: %s' % bucket)
        else:
            return default
    return SHARED_STATE[bucket]


def Load(bucket, path, clear=True, critical=False):
    """TODO(g): Figure out how the names work.  I like this format as well.
      I guess I could just leave them both, and people could pick what they
      want to use, but I dont like having repitition...
  """
    return ImportSave(bucket, path, clear=clear, critical=critical)


def ImportSave(bucket, save, clear=True, critical=False, imported_data=None):
    """Imports the saved data file.  Tests for presence of "%(key)s" to load
  a single file, or process all the files.
  
  If a single file is to be loaded, and it does not contain keys (not a dict
  formated YAML file), then all the data will be stored in the key "default".
  
  Args:
    bucket: string, bucket to import into
    save: string, path to load save YAML file from
    clear: boolean (default=True), if True, this will clear the current bucket
        before loading the new data
    critical: boolean (default=False), if True, and there is an error loading
        the save file, then an Exception will be raised.  If False, then the
        function returns and execution carries on without the state loaded.
    imported_data: any (default=None), if set, this will become the new data.
        Why have this?  Because if you want to mark-up the data in your own
        way and yet use the rest of this function's features, this is why.
        Specially, procblock.procyaml.Import() does special cool things, but
        I want unidist to stand alone from procblock, so I am not going to
        import that function.
  
  TODO(g): Does this need a better name?  Im using it initially to populate the
      YAML files I saved set, back in...  Load?
  """
    if clear:
        _EnsureBucketExists(bucket)
        SHARED_STATE[bucket] = threadsafedict.ThreadSafeDict()
    if '%(keys)' in save:
        save = save.replace('%(key)s', '%s')
    if '%s' not in save:
        if os.path.isfile(save):
            try:
                if not imported_data:
                    fp = open(save, 'r')
                    data = yaml.load(fp)
                    fp.close()
                else:
                    data = imported_data
            except Exception, e:
                log('Failed to import file: %s: %s' % (save, e), logging.ERROR)
                if critical:
                    raise Exception('Failed to import file: %s: %s' % (save, e))
                else:
                    log('Failed to import file: %s: %s' % (save_path, e), logging.ERROR)
                    return
            else:
                if type(data) == dict:
                    for key in data:
                        Set(bucket, key, data[key])

                else:
                    _EnsureBucketExists(bucket)
        else:
            log('sharedstate import not found: %s' % save)
    else:
        save_glob = save.replace('%s', '*')
        files = glob.glob(save_glob)
        save_regex = save.replace('%s', '(.*)')
    for filepath in files:
        found = re.findall(save_regex, filepath)
        if found:
            key = found[0]
            if os.path.isfile(filepath):
                try:
                    if not imported_data:
                        fp = open(filepath, 'r')
                        data = yaml.load(fp)
                        fp.close()
                    else:
                        data = imported_data
                except Exception, e:
                    if critical:
                        raise Exception('Failed to import file: %s: %s' % (save_path, e))
                    else:
                        log('Failed to import file: %s: %s' % (filepath, e), logging.ERROR)
                        continue
                else:
                    log('Imported Bucket: %s  Key: %s:  %s' % (bucket, key, filepath))
                    Set(bucket, key, data)


def Save(bucket, key=None, save=None, backups=2, delay=0, remote_node_sync=None, remote_node_url=None, remote_node_delay=30):
    """Save this bucket and key, as specified.
  
  Args:
    bucket: string, name of bucket for state variables
    key: string or any (optional), key to store data against.  Any valid dict key.
        If not specified, then all the keys will be saved.  This could be slow
        for key series data, so be aware.
    save: string (optional, default=None), the file path to save YAML files for
        this content.
        If "%(key)s" substring is present, each key in this bucket will be saved
        to it's own YAML file.  If it is not present, then all keys for a bucket
        will save into this one file.
    delay: number, seconds to delay in saving after a change, to incorporate
        many potential changes and minimize writes
    backups: int, the number of backups to keep of the saved file, in case of
        damage or other desire for change rollback.  Set backups=None to save,
        but not perform a backup
    remote_node_sync: list of strings (optional), list of hosts to remotely
        connect to on changes and replicate the changes
    remote_node_url: string, URL to RPC call for making this sync
    remote_node_delay: number, seconds to delay in replicating data after change
  """
    import stack
    log(stack.Mini(5))
    _EnsureBucketExists(bucket)
    if save == None:
        save = GetRegisteredSave(bucket)
    if not save:
        log('No save file specified: %s: %s' % (bucket, key), logging.WARN)
        return
    else:
        if '%s' in save:
            save = save.replace('%s', '%(key)s')
        if '%(key)s' in save:
            if key:
                keys = [
                 key]
            else:
                keys = GetBucketKeys(bucket)
            for key in keys:
                shared_save_key = '%s.%s.' % (bucket.replace('.', '_'), key)
                last_saved = Get('__sharedstate.saved', shared_save_key, default=0)
                if not delay or time.time() - last_saved >= delay:
                    save_final = save % {'key': run.MakePathSafeToCreate(key)}
                    log('Saved sharedstate with key: %s: %s: %s' % (bucket, key, save_final))
                    temp_save = '%s.tmp' % save_final
                    fp = open(temp_save, 'w')
                    yaml.dump(SHARED_STATE[bucket][key], fp)
                    fp.close()
                    os.rename(temp_save, save_final)

        else:
            shared_save_key = '%s.' % bucket.replace('.', '_')
            last_saved = Get('__sharedstate.saved', shared_save_key, default=0)
            temp_save = '%s.tmp' % save
            fp = open(temp_save, 'w')
            yaml.dump(dict(SHARED_STATE[bucket]), fp)
            fp.close()
            os.rename(temp_save, save)
            log('Saved sharedstate: %s: %s' % (bucket, save))
        Set('__sharedstate.saved', shared_save_key, time.time())
        return


def Set(bucket, key, value, save=None, backups=2, delay=0, remote_node_sync=None, remote_node_url=None, remote_node_delay=30):
    """Lock the shared control access to locks.  This way we can safely acquire
  an individual lock or create a new lock without a race condition.
  
  Args:
    bucket: string, name of bucket for state variables
    key: string or any, key to store data against.  Any valid dict key.
    value: any, any object to be stored in shared state
    save: string (optional, default=None), the file path to save YAML files for
        this content.
        If "%(key)s" substring is present, each key in this bucket will be saved
        to it's own YAML file.  If it is not present, then all keys for a bucket
        will save into this one file.
    delay: number, seconds to delay in saving after a change, to incorporate
        many potential changes and minimize writes
    backups: int, the number of backups to keep of the saved file, in case of
        damage or other desire for change rollback.  Set backups=None to save,
        but not perform a backup
    remote_node_sync: list of strings (optional), list of hosts to remotely
        connect to on changes and replicate the changes
    remote_node_url: string, URL to RPC call for making this sync
    remote_node_delay: number, seconds to delay in replicating data after change
  """
    _EnsureBucketExists(bucket)
    if save == None:
        save = GetRegisteredSave(bucket)
    SHARED_STATE[bucket][key] = value
    if save:
        Save(bucket, key, save=save, backups=backups, delay=delay, remote_node_sync=remote_node_sync, remote_node_url=remote_node_url, remote_node_delay=remote_node_delay)
    return value


def SetIfDoesntExist(bucket, key, value):
    """Returns boolean, whether the value was set or not.
  
  Args:
    bucket: string, name of bucket for state variables
    key: string or any, key to store data against.  Any valid dict key.
    value: any, any object to be stored in shared state
  """
    try:
        if not KeyExists(bucket, key):
            Set(bucket, key, value)
            return True
        else:
            return False
    except StateBucketDoesntExist, e:
        Set(bucket, key, value)
        return True


def Get(bucket, key, default=StateKeyNotFound):
    """Lock the shared control access to locks.  This way we can safely acquire
  an individual lock or create a new lock without a race condition.
  
  Args:
    bucket: string, name of bucket for state variables
    key: string or any, key to store data against.  Any valid dict key.
    default: any value (optional), if set and there is no data in this key,
        then this value will be set in the key and returned.
  
  NOTE(g): Do not try to implement the "strict=False" system for raising the
      Exception, it doesnt fit this function well, but using a default does
  """
    save_path = BucketExists(bucket) or GetRegisteredSave(bucket)
    if save_path:
        ImportSave(bucket, save)
        if KeyExists(bucket, key):
            return SHARED_STATE[bucket][key]
        if default == StateKeyNotFound:
            raise StateBucketDoesntExist('Bucket doesnt exist: %s' % bucket)
        else:
            Set(bucket, key, default)
            return default
    elif KeyExists(bucket, key) or default != StateKeyNotFound:
        Set(bucket, key, default)
        return default
    else:
        return SHARED_STATE[bucket][key]


def GetSet(bucket, key, value):
    """Returns boolean if this named lock is locked.  If doesnt exist, still False
  
  Args:
    bucket: string, name of bucket for state variables
    key: string or any, key to store data against.  Any valid dict key.
    value: any, any object to be stored in shared state
  """
    _EnsureBucketExists(bucket)
    previous_value = SHARED_STATE[bucket].GetSet(key, value)
    return previous_value


if __name__ == '__main__':
    print BucketExists('sofa')
    print Set('sofa', 'barn', 15)
    print BucketExists('sofa')
    print Get('sofa', 'barn')
    print Set('sofa', 'bush', 'Tundra!')
    print GetSet('sofa', 'bush', 'Tornado!')
    print GetSet('sofa', 'bush', 'Ohio!')
    print GetBucketKeys('sofa')
    print KeyExists('sofa', 'bush')
    print KeyExists('sofa', 'bush2')
    try:
        print KeyExists('sortaaaa', 'bush2')
    except StateBucketDoesntExist, e:
        print e