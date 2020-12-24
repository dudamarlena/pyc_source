# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\dev\cocos2020\tools\autotest\helpers.py
# Compiled at: 2020-01-10 23:58:31
# Size of source mod 2**32: 33415 bytes
from __future__ import division, print_function, unicode_literals
import sys, os, re, copy, time, hashlib, pprint
import remembercases.db as dbm
import remembercases.doers as doers
import remembercases.snapshot_taker as st
import remembercases.proxy as proxy
from cocos import compat

def text_props_simple(text, propnames):
    """
    calculate several props from the text and return into a dictionary
    with key the prop name and value the one calculted from text for this prop
    """
    propdict = {}
    for name in propnames:
        func = getattr(sys.modules[text_props_simple.__module__], name)
        propdict[name] = func(text)
    else:
        return propdict


c_rgx_timedependent = re.compile('(time)|(action)|(schedule)', re.MULTILINE)

def timedependent(text):
    return c_rgx_timedependent.search(text) is not None


c_rgx_on_something = re.compile(' on_([a-z_]+)', re.MULTILINE)

def interactive--- This code section failed: ---

 L.  37         0  LOAD_CONST               0
                2  STORE_FAST               'n'

 L.  39         4  LOAD_GLOBAL              c_rgx_on_something
                6  LOAD_METHOD              search
                8  LOAD_FAST                'text'
               10  LOAD_FAST                'n'
               12  CALL_METHOD_2         2  ''
               14  STORE_FAST               'match'

 L.  40        16  LOAD_FAST                'match'
               18  LOAD_CONST               None
               20  COMPARE_OP               is-not
               22  POP_JUMP_IF_FALSE    50  'to 50'
               24  LOAD_FAST                'match'
               26  LOAD_METHOD              group
               28  CALL_METHOD_0         0  ''
               30  LOAD_CONST               (' on_enter', ' on_exit')
               32  COMPARE_OP               in
               34  POP_JUMP_IF_FALSE    50  'to 50'

 L.  41        36  LOAD_FAST                'match'
               38  LOAD_METHOD              end
               40  CALL_METHOD_0         0  ''
               42  STORE_FAST               'n'
               44  JUMP_BACK             4  'to 4'

 L.  43        46  BREAK_LOOP           50  'to 50'
               48  JUMP_BACK             4  'to 4'
             50_0  COME_FROM            34  '34'
             50_1  COME_FROM            22  '22'

 L.  44        50  LOAD_FAST                'match'
               52  LOAD_CONST               None
               54  COMPARE_OP               is-not
               56  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 56


def uses_random(text):
    return text.find('random') > -1


def has_testinfo(text):
    return text.find('testinfo') > -1


c_rgx_testinfo = re.compile('^testinfo\\s*=\\s*(\\".*)$', re.MULTILINE)

def testinfo_payload(text):
    match = c_rgx_testinfo.search(text)
    if match is None:
        return
    tinfo = match.group(1)
    tinfo = tinfo[1:tinfo.find('"', 1)]
    tinfo = str(tinfo)
    return tinfo


def new_db(filename_persist=None):
    """Instantiates and saves a new db
    
    :Parameters:
        `filename_persist` : str
            filename used to persist the new db, defaults to None

    if filename_persist is None, the new db is not stored to disk
    If file exists a ValueError is raised.
    The new db is an instance of remembercases.TestbedEntityPropDB.
    The stored db is retrieved to ensure it can be read.
    
    """
    if filename_persist:
        if os.path.exists(filename_persist):
            msg = 'initial_recon refuses to overwrite an existing file: %s'
            msg = msg % filename_persist
            raise ValueError(msg)
    db = dbm.TestbedEntityPropDB
    if filename_persist:
        dbm.db_save(db, filename_persist)
        new = dbm.db_load(filename_persist)
    return db


def new_testbed(db, testbed, basepath):
    """Creates, initializes (and set as db's default_tesbed) a testbed

    :Parameters:
        `db` : remembercases.TestbedEntityPropDB
            The db where the testbed will be added.
        `testbed` : str
            name for the new testbed; if duplicates an existing name an
            dbm.ErrorDuplicatedTestbed will be raised and the db will not
            be modified.            
        `basepath` : str
            directory name that will be the testbed's basepath

    After the testbed is created, it is set as the db's default_testbed.
    
    The testbed is initialized by adding some group of props, and their
    props are added to the testbed.

    An entry "new_testbed" with details about the operation is added to the
    db history.

    The testbed basepath will be used to calculate the canonical name for
    entities in the testbed that are files.
    The canonical name is the the relative path from basepath, with '/'
    path separators irrespective to the os.sep
    No check is performed over the basepath parameter.
    
    """
    db.add_testbed(testbed, basepath)
    db.set_default_testbed(testbed)
    default_groups = {'scan':[
      'IOerror',
      'timedependent',
      'interactive',
      'uses_random',
      'has_testinfo',
      'static',
      'testinfo',
      'expected_snapshots',
      'testinfo_diagnostic',
      'md5_at_testinfo'], 
     'snapshots_capture':[
      'snapshots_success',
      'snapshots_diagnostic',
      'missing_snapshots'], 
     'testrun':[
      'testrun_success',
      'testrun_diagnostic',
      'testrun_md5']}
    for groupname in default_groups:
        db.add_group(groupname, (default_groups[groupname]), addprops=True)
    else:
        text_history = 'testbed: %s\nbasepath: %s\n\n' % (testbed, basepath) + '\nAdded prop groups:\n' + doers.pprint_to_string(default_groups)
        db.history_add('new_testbed', text_history)


def canonical_names_from_filenames(db, filenames):
    r"""Convert filenames to the canonical form

    :Parameters:
        `db` : remembercases.TestbedEntityPropDB
        `filenames` : iterable yielding filenames

    :return: A list expressing the filenames in the canonical form.

    The canonical form is the relative path from the basepath in the db's
    default_tesbed, with dir separators always '/' irrespective of os.sep

    A typical example transformation is::
    
        ..\..   est     est_base.py -> test     est_base.py

    """
    return [db.canonical_fname(s) for s in filenames]


def add_entities(db, filename_persist, targets):
    """Adds entities to the db 's default testbed

    :Parameters:
        `db` : remembercases.TestbedEntityPropDB
        `filename_persist` : filename used to persist the new db
        `names` : iterable yielding entity names
    """
    for name in targets:
        db.add_entity(name)
    else:
        db.history_add('add_acripts', '\n'.join(targets))
        if filename_persist:
            dbm.db_save(db, filename_persist)


def scanprops_from_text(text, fname):
    base_text_props = ['timedependent',
     'interactive',
     'uses_random',
     'has_testinfo']
    if text is None:
        propdict = {'IOerror': True}
        return propdict
    propdict = text_props_simple(text, base_text_props)
    propdict['static'] = not propdict['timedependent'] and not propdict['interactive']
    testinfo = testinfo_payload(text)
    if testinfo is not None:
        propdict['testinfo'] = testinfo
        basename = os.path.basename(fname)
        diagnostic, expected_snapshots = st.ScreenSampler.validated_info(testinfo, basename)
        propdict['testinfo_diagnostic'] = diagnostic
        propdict['expected_snapshots'] = expected_snapshots
    propdict['md5_at_testinfo'] = doers.md5_hex_for_text(text)
    return propdict


def scanprops_from_fname(fname):
    try:
        text = doers.load_text(fname)
    except:
        text = None
    else:
        return scanprops_from_text(text, fname)


def update_scanprops(db, filename_persist, candidates):
    """
    For each script in candidates the props in 'scan' group are calculated and
    stored as script props.

    candidates should be known entities in the db
    """
    known_scripts, unknowns = db.entities(candidates=candidates)
    for script in known_scripts:
        fname = db.fname_from_canonical(script)
        scanprops = scanprops_from_fname(fname)
        db.set_groupdict(script, 'scan', scanprops)
    else:
        text = '\n'.join(known_scripts)
        db.history_add('update_scanprops', text)
        if filename_persist:
            dbm.db_save(db, filename_persist)
        return (
         known_scripts, unknowns)


def update_snapshots(db, filename_persist, target_scripts, snapshots_dir):
    """
    runs the scripts in target scripts, taking snapshots as indicated by the
    testinfo in the script, and updating the snapshots related info in the db.

    Params:
        db:
            a remembercases.TestbedEntityPropDB object
        filename_persist:
            filename to persist the db after updating
        target_scripts:
            iterable yielding scripts. If None, all scripts known in the
            default testbed are assumed.
        snapshots_dir:
            directory to store the snapshots

    Returns (valid_scripts, rejected) where:

        valid_scripts :
            scripts in target_scripts that are known in the default testbed and
            have valid testinfo

        rejected :
            scripts in target_scripts that are unknown in the default testbed or
            dont have valid testinfo
        
    Db operations are done over the default testbed, which should have been
    set bejore calling here.
    
    For each valid entity the following props are set:
        'snapshots_success':
            bool, True if (no traceback or timeout when running the script,
            also all expected snapshots had been produced), else False
        'snapshots_diagnostic':
            string, '' means no errors, else description of failure while
            trying to take snapshots
        'missing_snapshots':
            list of missing snapshots filenames
    """
    proxy_abspath = os.path.abspath('proxy_snapshots.py')
    if not os.path.exists(proxy_abspath):
        raise ValueError('proxy script not found:%s' % proxy_abspath)
    snapshots_abspath = os.path.abspath(snapshots_dir)
    if not os.path.exists(snapshots_abspath):
        os.makedirs(snapshots_abspath)
    valid_scripts, rejected = db.entities(fn_allow=fn_allow_testinfo_valid, candidates=target_scripts)
    for script in valid_scripts:
        stored_testinfo = db.get_prop_value(script, 'testinfo')
        expected_snapshots = db.get_prop_value(script, 'expected_snapshots')
        for name in expected_snapshots:
            p = os.path.join(snapshots_abspath, name)
            if os.path.exists(p):
                os.remove(p)
            fname = db.fname_from_canonical(script)
            timeout_hit, err = proxy.proxy_run(proxy_abspath, fname, [stored_testinfo, snapshots_abspath])
            missing = [s for s in expected_snapshots if not os.path.exists(os.path.join(snapshots_abspath, s))]
            db.set_prop_value(script, 'missing_snapshots', missing)
            snapshots_success = err == '' and not timeout_hit and len(missing) == 0
            db.set_prop_value(script, 'snapshots_success', snapshots_success)
            snapshots_diagnostic = ''
            if not snapshots_success:
                if timeout_hit:
                    err = 'Timeout hit. Remember in this case it is posible not all stderr captured.\n' + err
                if len(missing):
                    missing = [os.path.basename(s) for s in missing]
                    err += '\nNot all snapshots captured - missing snapshots:\n'
                    err += '\n'.join(missing)
                snapshots_diagnostic = err
                print('err:', err)
            db.set_prop_value(script, 'snapshots_diagnostic', snapshots_diagnostic)
        else:
            text = '\n'.join(valid_scripts)
            db.history_add('update_snapshots', text)
            if filename_persist:
                dbm.db_save(db, filename_persist)
            return (
             valid_scripts, rejected)


def re_scan_and_shoot(db, filename_persist, target_scripts, snapshots_dir):
    db.history_add('the next scan and snapshots is a redo scan + snapshots', '-')
    known_scripts, unknowns = db.entities(candidates=target_scripts)
    for script in known_scripts:
        try:
            snaps = db.get_prop_value(script, 'expected_snapshots')
            for name in snaps:
                p = os.path.join(snapshots_dir, name)
                if os.path.exists(p):
                    os.remove(p)

        except dbm.ErrorUnknownPropInEntity:
            pass

    else:
        update_scanprops(db, filename_persist, known_scripts)
        update_snapshots(db, filename_persist, known_scripts, snapshots_dir)


def _update_testrun(db, testrun_props_by_candidate, snapshots_dir):
    """
    the propdict for each candidate must have been tested for keys in testrun
    """
    known_scripts, unknowns = db.entities(candidates=testrun_props_by_candidate)
    ignored = set()
    for script in known_scripts:
        fname = db.fname_from_canonical(script)
        propdict = scanprops_from_fname(fname)
        if propdict != db.get_groupdict(script, 'scan'):
            ignored.add(script)
        else:
            d = copy.deepcopy(testrun_props_by_candidate[script])
            d['testrun_md5'] = propdict['md5_at_testinfo']
            db.set_groupdict(script, 'testrun', d)
    else:
        checked_in = set([k for k in known_scripts if k not in ignored])
        return (checked_in, ignored, unknowns)


def update_testrun__pass(db, filename_persist, candidates, snapshots_dir, snapshots_reference_dir=None):
    """
    snapshots_reference_dir : dir to move snapshots; if None no move
    """
    if snapshots_reference_dir:
        if not os.path.isdir(snapshots_dir):
            raise ValueError('snapshot dir not found or not a dir:%s' % snapshots_dir)
        if not os.path.exists(snapshots_reference_dir):
            os.makedirs(snapshots_reference_dir)
    pass_dict = {'testrun_success':'pass',  'testrun_diagnostic':''}
    testrun_props_by_candidate = dict([(k, pass_dict) for k in candidates])
    checked_in, ignored, unknown = _update_testrun(db, testrun_props_by_candidate, snapshots_dir)
    move_failed = set()
    if snapshots_reference_dir:
        for script in checked_in:
            snapshots = db.get_prop_value(script, 'expected_snapshots')
            moved, cant_move = doers.move_files(snapshots, snapshots_dir, snapshots_reference_dir)
            if cant_move:
                db.del_groupdict(script, 'testrun')
                move_failed.add(script)

    checked_in -= move_failed
    text_1 = doers.pprint_to_string(checked_in)
    text_2 = doers.pprint_to_string(move_failed)
    text_3 = doers.pprint_to_string(unknown)
    text_history = '\n'.join(['checked_in:', text_1,
     'move_failed:', text_2,
     'unknown:', text_3])
    db.history_add('update_testrun__pass', text_history)
    if filename_persist:
        dbm.db_save(db, filename_persist)
    return (checked_in, unknown, move_failed)


def update_testrun__bad(db, filename_persist, testrun_props_by_candidate, snapshots_dir, snapshots_reference_dir=None):
    """
    snapshots_reference_dir : dir to move snapshots; if None no move
    """
    if snapshots_reference_dir:
        if not os.path.isdir(snapshots_dir):
            raise ValueError('snapshot dir not found or not a dir:%s' % snapshots_dir)
        if not os.path.exists(snapshots_reference_dir):
            os.makedirs(snapshots_reference_dir)
    checked_in, ignored, unknown = _update_testrun(db, testrun_props_by_candidate, snapshots_dir)
    move_failed = set()
    if snapshots_reference_dir:
        for script in checked_in:
            snapshots = db.get_prop_value(script, 'expected_snapshots')
            moved, cant_move = doers.move_files(snapshots, snapshots_dir, snapshots_reference_dir)
            if cant_move:
                move_failed.add(script)

    text_1 = doers.pprint_to_string(checked_in)
    text_2 = doers.pprint_to_string(move_failed)
    text_3 = doers.pprint_to_string(unknown)
    text_history = '\n'.join(['checked_in:', text_1,
     'move_failed:', text_2,
     'unknown:', text_3])
    db.history_add('update_testrun__bad', text_history)
    if filename_persist:
        dbm.db_save(db, filename_persist)
    return (checked_in, unknown, move_failed)


def snapshots_compare(db, fn_snapshots_dist, threshold, candidates, max_tries, reference_dir, samples_dir):
    """does snapshots for candidates and compares with reference snapshots

    :Parameters:
        db: remembercases.TestbedEntityPropDB
            The db which holds info about scripts.
            The default_testbed should have been set to the desired testbed,
            comparison will use info about candidates in the default testbed.
        fn_snapshots_dist : callable
            callable that receives paths to two images and returns a float
            meaning distance between images
        threshold : float >= 0
            images don't match if fn_snapshots_dist(img1, img1) > threshold
        candidates : 
            iterable yielding scripts.
            If None, all scripts known in the default testbed are assumed.
            Their testinfo must be present and up to date, except for maybe md5.
        max_tries: int > 0
            how many times try the (take snapshots + comparison). This is
            handy because very rarely the capture fails. Sugested value is 3
        reference_dir:
            directory with the reference snapshots
        samples_dir:
            directory to write the fresh snapshots (will remain dirty)

    :returns:
        equals, unequals, untested : sets
            A script will be in untested when not known to the db,
            doesn't have a valid testinfo or does not want snapshots
    """
    assert max_tries > 0
    if not os.path.exists(samples_dir):
        os.makedirs(samples_dir)
    samples_abspath = os.path.abspath(samples_dir)
    knowns, unknowns = db.entities(fn_allow=fn_allow_wants_snapsots, candidates=candidates)
    equals = set()
    unequals = set(knowns)
    untested = unknowns | set(candidates) - unequals
    for i in range(max_tries):
        db.clone_testbed(None, 'tmp')
        old_testbed = db.set_default_testbed('tmp')
        update_snapshots(db, None, unequals, samples_dir)

    for name in unequals:
        match = db.get_prop_value(name, 'snapshots_success')
        if match:
            for snap in db.get_prop_value(name, 'expected_snapshots'):
                snap_ref = os.path.join(reference_dir, snap)
                snap_tmp = os.path.join(samples_abspath, snap)

            if fn_snapshots_dist(snap_ref, snap_tmp) > threshold:
                match = False
                break
        else:
            if match:
                equals.add(name)
            db.del_testbed('tmp')
            db.set_default_testbed(old_testbed)
            unequals -= equals
            if not unequals:
                break
            return (
             equals, unequals, untested)


def compare_testbeds_by_entities(db1_fname, db1_testbed, db2_fname, db2_testbed):
    db1 = dbm.db_load(db1_fname, default_testbed=db1_testbed)
    db2 = dbm.db_load(db2_fname, default_testbed=db2_testbed)
    ents1, unknown = db1.entities
    ents2, unknown = db2.entities
    common_entities = ents1 & ents2
    only_in_1 = ents1 - common_entities
    only_in_2 = ents2 - common_entities
    f1 = db1.get_propdict
    f2 = db2.get_propdict
    equals = set([entity for entity in common_entities if f1(entity) == f2(entity)])
    differents = common_entities - equals
    return (common_entities, only_in_1, only_in_2, equals, differents)


def measure_repeteability(db, candidates, limit, samples_dir, required_md5=None):
    """
    :Parameters:
        limit : int or float
            int means count of snapdhots runs
            float means times in minutes, will be surpased to end the round
    """
    start_time = time.time
    scripts, unknowns = db.entities(fn_allow=fn_allow_testinfo_valid, candidates=candidates)
    f = db.get_prop_value
    snapshots = [snap for name in scripts for snap in f(name, 'expected_snapshots')]
    stats_by_snapshot_name = dict([(snap, {}) for snap in snapshots])
    stats_by_script_name = dict([(name, {'timeouts':0,  'errs':0}) for name in scripts if f(name, 'expected_snapshots')])
    scripts = [name for name in stats_by_script_name]
    hasher = hashlib.md5
    for name in stats_by_script_name:
        hasher.update(compat.asciibytes(db.get_prop_value(name, 'md5_at_testinfo')))
    else:
        overall_md5 = hasher.hexdigest
        if required_md5:
            assert required_md5 == overall_md5
        if not os.path.exists(samples_dir):
            os.makedirs(samples_dir)
        snapshots_abspath = os.path.abspath(samples_dir)
        proxy_abspath = os.path.abspath('proxy_snapshots.py')
        if not os.path.exists(proxy_abspath):
            raise ValueError('proxy script not found:%s' % proxy_abspath)
        rounds = 0

    if isinstance(limit, float):
        limit_seconds = limit * 60
        f_continue = lambda : time.time - start_time < limit_seconds
    else:
        if isinstance(limit, int):
            f_continue = lambda : rounds < limit
        else:
            raise ValueError
            while f_continue():
                for name in scripts:
                    fname = db.fname_from_canonical(name)
                    stored_testinfo = db.get_prop_value(name, 'testinfo')
                    timeout_hit, err = proxy.proxy_run(proxy_abspath, fname, [
                     stored_testinfo, snapshots_abspath])
                    if timeout_hit:
                        stats_by_script_name[name]['timeouts'] += 1
                    if err:
                        stats_by_script_name[name]['errs'] += 1
                    sbs = stats_by_snapshot_name
                    for snap in stats_by_snapshot_name:
                        sname = os.path.join(snapshots_abspath, snap)
                        if os.path.exists(sname):
                            try:
                                f = open(sname, 'rb')
                                data = f.read
                                f.close
                                md5 = doers.md5_hex(data)
                                sbs[snap][md5] = sbs[snap].setdefault(md5, 0) + 1
                            except Exception:
                                pass
                            else:
                                try:
                                    os.remove(sname)
                                except Exception:
                                    pass

                    else:
                        rounds += 1

            elapsed = time.time - start_time
            return (overall_md5, elapsed, rounds, stats_by_script_name,
             stats_by_snapshot_name)


def info_outdated_strong--- This code section failed: ---

 L. 673         0  LOAD_GLOBAL              get_scripts
                2  LOAD_FAST                'db'
                4  LOAD_STR                 'testrun_present'
                6  CALL_FUNCTION_2       2  ''
                8  UNPACK_SEQUENCE_2     2 
               10  STORE_FAST               'have_testrun'
               12  STORE_FAST               'no_comply'

 L. 675        14  LOAD_GLOBAL              set
               16  CALL_FUNCTION_0       0  ''
               18  STORE_FAST               'outdated'

 L. 676        20  LOAD_FAST                'have_testrun'
               22  GET_ITER         
             24_0  COME_FROM           112  '112'
               24  FOR_ITER            126  'to 126'
               26  STORE_FAST               'name'

 L. 677        28  LOAD_FAST                'db'
               30  LOAD_METHOD              fname_from_canonical
               32  LOAD_FAST                'name'
               34  CALL_METHOD_1         1  ''
               36  STORE_FAST               'fname'

 L. 678        38  SETUP_FINALLY        54  'to 54'

 L. 679        40  LOAD_GLOBAL              doers
               42  LOAD_METHOD              load_text
               44  LOAD_FAST                'fname'
               46  CALL_METHOD_1         1  ''
               48  STORE_FAST               'text'
               50  POP_BLOCK        
               52  JUMP_FORWARD         88  'to 88'
             54_0  COME_FROM_FINALLY    38  '38'

 L. 680        54  DUP_TOP          
               56  LOAD_GLOBAL              Exception
               58  COMPARE_OP               exception-match
               60  POP_JUMP_IF_FALSE    86  'to 86'
               62  POP_TOP          
               64  POP_TOP          
               66  POP_TOP          

 L. 681        68  LOAD_FAST                'outdated'
               70  LOAD_METHOD              add
               72  LOAD_FAST                'name'
               74  CALL_METHOD_1         1  ''
               76  POP_TOP          

 L. 682        78  POP_EXCEPT       
               80  JUMP_BACK            24  'to 24'
               82  POP_EXCEPT       
               84  JUMP_FORWARD         88  'to 88'
             86_0  COME_FROM            60  '60'
               86  END_FINALLY      
             88_0  COME_FROM            84  '84'
             88_1  COME_FROM            52  '52'

 L. 683        88  LOAD_GLOBAL              doers
               90  LOAD_METHOD              md5_hex_for_text
               92  LOAD_FAST                'text'
               94  CALL_METHOD_1         1  ''
               96  STORE_FAST               'actual_md5'

 L. 684        98  LOAD_FAST                'actual_md5'
              100  LOAD_FAST                'db'
              102  LOAD_METHOD              get_prop_value
              104  LOAD_FAST                'name'
              106  LOAD_STR                 'testrun_md5'
              108  CALL_METHOD_2         2  ''
              110  COMPARE_OP               !=
              112  POP_JUMP_IF_FALSE    24  'to 24'

 L. 685       114  LOAD_FAST                'outdated'
              116  LOAD_METHOD              add
              118  LOAD_FAST                'name'
              120  CALL_METHOD_1         1  ''
              122  POP_TOP          
              124  JUMP_BACK            24  'to 24'

 L. 687       126  LOAD_FAST                'outdated'
              128  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_EXCEPT' instruction at offset 82


def fn_allow_all(propdict):
    return True


def fn_allow_testinfo_valid(propdict):
    return 'testinfo_diagnostic' in propdict and propdict['testinfo_diagnostic'] == ''


def fn_allow_testinfo_missing(propdict):
    return 'testinfo' not in propdict


def fn_allow_testinfo_invalid(propdict):
    return 'testinfo_diagnostic' in propdict and propdict['testinfo_diagnostic'] != ''


def fn_allow_snapshots_success(propdict):
    return 'snapshots_success' in propdict and propdict['snapshots_success']


def fn_allow_snapshots_failure(propdict):
    return 'snapshots_success' in propdict and not propdict['snapshots_success']


def fn_allow_expected_snapshots_present(propdict):
    return 'expected_snapshots' in propdict


def fn_allow_wants_snapsots(propdict):
    return 'expected_snapshots' in propdict and len(propdict['expected_snapshots']) > 0


def fn_allow_IOerror(propdict):
    return 'IOerror' in propdict and propdict['IOerror']


def fn_allow_testrun_pass(propdict):
    return 'testrun_success' in propdict and propdict['testrun_success'] == 'pass'


def fn_allow_testrun_not_pass(propdict):
    return 'testinfo_diagnostic' in propdict and propdict['testinfo_diagnostic'] == '' and ('testrun_success' not in propdict or propdict['testrun_success'] != 'pass')


def fn_allow_new_no_interactive(propdict):
    return 'testinfo' not in propdict and 'interactive' in propdict and not propdict['interactive']


def fn_allow_no_props(propdict):
    return len(propdict) == 0


def fn_allow_testrun_present(propdict):
    return 'testrun_success' in propdict


def fn_allow_outdated_weak(propdict):
    return 'testrun_md5' in propdict and 'testinfo_md5' in propdict and propdict['testrun_md5'] == propdict['testinfo_md5']


def fn_allow_not_inspected(propdict):
    return 'testinfo_diagnostic' in propdict and 'testrun_success' not in propdict


def get_scripts(db, selector, candidates=None, testbed=None):
    was_unknown = selector == 'unknown'
    if was_unknown:
        selector = 'all'
    func_name = 'fn_allow_%s' % selector
    func = getattr(sys.modules[text_props_simple.__module__], func_name)
    selected, unknown = db.entities(fn_allow=func, candidates=candidates,
      testbed=testbed)
    if was_unknown:
        selected = unknown
        unknown = set()
    return (selected, unknown)


def section(db, selector, candidates=None, verbose=None, testbed=None):
    headers = {'testinfo_valid':'Scripts that have testinfo and it is valid', 
     'testinfo_invalid':'Scripts that have testinfo and it is not valid', 
     'testinfo_missing':"Scripts that don't have testinfo", 
     'all':'All scripts', 
     'snapshots_success':'Scripts that have taken snapshots succesfuly', 
     'snapshots_failure':'Scripts that atempted to take snapshots but failed', 
     'expected_snapshots_present':"Scripts that have prop 'expected_snapshots' present", 
     'wants_snapsots':'Scripts with should take one or more snapshots', 
     'unknown':'Scripts not known to the db', 
     'IOerror':"Scripts that can't be readed", 
     'testrun_pass':'Scripts showing correct behavior and snapshots reflect that', 
     'testrun_not_pass':"Scripts which have valid testinfo and don't have testrun_success=='pass'", 
     'new_no_interactive':'No testinfo, no interactive', 
     'no_props':'No props set', 
     'testrun_present':'Scripts that have been inspected', 
     'outdated_weak':'Scripts with different MD5 in testinfo and testrun', 
     'not_inspected':'Scripts with testinfo valid without testrun info'}
    scripts, unknown = get_scripts(db, selector, candidates, testbed)
    scripts = sorted(scripts)
    if candidates is None:
        num_candidates = db.num_entities(testbed)
    else:
        num_candidates = len(candidates)
    text_parts = []
    if verbose:
        prefix = ': '
    else:
        prefix = ''
    header_tail = '(%d / %d)' % (len(scripts), num_candidates)
    text_parts.append('%s%s %s' % (prefix, headers[selector], header_tail))
    if verbose:
        text_parts.append('\n')
        text_parts.extend(scripts)
    text = '\n'.join(text_parts)
    return text


def rpt(db, selectors, candidates=None, verbose=True, testbed=None):
    text_parts = [
     '\n']
    for selection in selectors:
        text_parts.append(section(db, selection, candidates, verbose, testbed))
    else:
        text = '\n'.join(text_parts)
        return text


def rpt_detail_diagnostics(db, selector, candidates=None, testbed=None):
    prop = {'snapshots_failure':'snapshots_diagnostic',  'testinfo_invalid':'testinfo_diagnostic', 
     'testrun_success':'testrun_diagnostic'}
    if selector not in prop:
        return '\nNo detailed report available for selector = ' + selector
    scripts, unknown = get_scripts(db, selector, candidates, testbed)
    scripts = sorted(scripts)
    text_parts = ['\n\nDetails %s errors' % selector]
    for entity in scripts:
        text_parts.append('\n%s\n' % entity)
        text_parts.append(db.get_prop_value(entity, (prop[selector]), testbed=testbed))
        text_parts.append('------------------------------------------------------------------------------')
    else:
        text = '\n'.join(text_parts)
        return text


def rpt_all_props(db, candidates, testbed=None):
    scripts, unknowns = db.entities(candidates=candidates)
    text_parts = []
    separator = '------------------------------------------------------------------------------'
    for name in scripts:
        text_parts.append(name)
        text = doers.pprint_to_string(db.get_propdict(name, testbed=testbed))
        text_parts.append(text)
        text_parts.append(separator)
    else:
        if unknowns:
            text_parts.append('unknown entities')
            text_parts.append(doers.pprint_to_string(unknowns))
        text = '\n'.join(text_parts)
        return text


def rpt_testrun_outdated_strong(db):
    parts = [e for e in info_outdated_strong(db)]
    parts.sort
    parts.insert(0, ': Scripts with outdated testrun info (strong)\n')
    text = '\n'.join(parts)
    return text


def rpt_compare_testbeds_by_entities(db1_fname, db1_testbed, db2_fname, db2_testbed, verbose=False):
    res = compare_testbeds_by_entities(db1_fname, db1_testbed, db2_fname, db2_testbed)
    common_entities, only_in_1, only_in_2, equals, differents = res
    text_parts = []
    if only_in_1:
        text_parts.append('Only in 1')
        li = [e for e in only_in_1]
        li.sort
        text_parts.extend(li)
    if only_in_2:
        text_parts.append('\nOnly in 2')
        li = [e for e in only_in_2]
        li.sort
        text_parts.extend(li)
    else:
        if not only_in_1:
            if not only_in_2:
                text_parts.append('\nSame entitities in both tesbeds')
        if common_entities:
            if verbose:
                text_parts.append('\nEntities in both testbeds with equal (props: values)')
                li = [e for e in common_entities]
                li.sort
                text_parts.extend(li)
            else:
                msg = '\nEntities in both testbeds with equal (props: values), quantity: %d'
                msg = msg % len(common_entities)
                text_parts.append(msg)
    if differents:
        text_parts.append('\nEntities in both testbeds that differs in props')
        li = [e for e in differents]
        li.sort
        text_parts.extend(li)
    text = '\n'.join(text_parts)
    return text