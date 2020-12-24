# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sfs/ops/ops_merge.py
# Compiled at: 2018-12-28 05:37:12
# Size of source mod 2**32: 17502 bytes
"""CLI for merging directories in an SFS"""
import collections, itertools, os, shutil, time
import sfs.core as core
import sfs.events as events
import sfs.exceptions as exceptions
import sfs.file_system as fs
import sfs.helper as helper
import sfs.log_utils as log
import sfs.ops.helper as ops_helper
constants = {'MERGE_FILE_EXTENSION':'.merge', 
 'MERGE_MODES':{'KEEP_TARGET':'keep-target', 
  'KEEP_SOURCE':'keep-source', 
  'KEEP_BOTH':'keep-both'}}
commands = {'MERGE': 'merge'}
messages = {'MERGE': {'HELP':'Merge a source directory into a target directory in an SFS. These directories cannot be nested', 
           'HELP_OPT':{'TARGET':'Path of target directory to merge files in to', 
            'SOURCE':'Path of source directory to copy files from', 
            'HANDLE_CONFLICTS':'Specify whether to delete target or source files on conflicts or keep both', 
            'CONTINUE':'Stop merge if there are conflicting files or links and save the conflicts to a JSON file. The file can manually edited to configure handling of conflicts before proceeding with the merge operation', 
            'USE_JSON':'Use the generated JSON file for handling conflicts', 
            'OVERRIDE_JSON':'Override the generated JSON file if it exists', 
            'DEL_JSON':'Delete the generated JSON file after the merge operation completes', 
            'DEL_SOURCE':'Delete the source directory after the merge operation completes'}, 
           'ERROR':{'NOT_IN_SFS':'Path is not in an SFS', 
            'INVALID_PATH':'Not a directory', 
            'JSON_EXISTS':'JSON already exists in target directory', 
            'JSON_NOT_FOUND':'JSON already exists in target directory', 
            'NESTED_DIR':'Target and source directories cannot be nested', 
            'INVALID_CONFLICTS':'Conflicts still exist while using Conflicts JSON. Conflicting files'}, 
           'OUTPUT':{'CONFLICT_COUNT':'No of conflicts: ', 
            'JSON_PATH':'Conflicts have been saved to JSON file: ', 
            'DIRS_CREATED':'No of directories created: ', 
            'DIRS_DELETED':'No of directories deleted: ', 
            'FILES_MERGED':'No of files merged: ', 
            'LINKS_MERGED':'No of links merged: ', 
            'NODES_DELETED':'No of target files and links deleted: ', 
            'NODES_RENAMED':'No of target files and links renamed: ', 
            'SOURCE_DELETED':'Source directory deleted. Deletions: '}}}

@events.subscriber(events.events['CLI_REGISTRY'])
def _merge_ops_cli(parser, parents=()):
    merge = parser.add_parser((commands['MERGE']),
      parents=parents,
      help=(messages['MERGE']['HELP']))
    merge.add_argument('target', help=(messages['MERGE']['HELP_OPT']['TARGET']))
    merge.add_argument('source', help=(messages['MERGE']['HELP_OPT']['SOURCE']))
    merge.add_argument('-k',
      '--on-conflict', choices=(constants['MERGE_MODES'].values()), default=(constants['MERGE_MODES']['KEEP_TARGET']),
      help=(messages['MERGE']['HELP_OPT']['HANDLE_CONFLICTS']))
    merge.add_argument('-c',
      '--continue', dest='no_stop', action='store_true', help=(messages['MERGE']['HELP_OPT']['CONTINUE']))
    merge.add_argument('-j',
      '--json', action='store_true', help=(messages['MERGE']['HELP_OPT']['USE_JSON']))
    merge.add_argument('-o',
      '--override', action='store_true', help=(messages['MERGE']['HELP_OPT']['OVERRIDE_JSON']))
    merge.add_argument('-d',
      '--del-json', action='store_true', help=(messages['MERGE']['HELP_OPT']['DEL_JSON']))
    merge.add_argument('-s',
      '--del-source', action='store_true', help=(messages['MERGE']['HELP_OPT']['DEL_SOURCE']))


@ops_helper.cli_command(commands['MERGE'])
def _merge_command_handler(args):
    """Merge contents of a source directory into a target directory inside an SFS recursively including links files and
     sub-directories

     In case of conflicts, the process terminates after saving conflicting files to a JSON. The file can be edited and
     used for completing the merge operation. If 'args.no_stop' is True, the conflicts are not saved and the merge
     proceeds with default conflict resolution
    'args.on_conflict' can be used to set the conflict resolution: keep_target ignores source file, keep_source deletes
    target file while keep_both keeps both target and source files
    'args.json' when True merges using the generated conflicts JSON file
    'args.override' when True overrides the existing JSON file if one exists. Otherwise, a validation error is thrown
    'args.del_json' when True deletes the conflicts JSON after a successful merge
    'args.del_source' when True deletes the source directory after a successful merge
    """
    target = fs.expand_path(args.target)
    source = fs.expand_path(args.source)
    read_conflicts = args.json
    save_conflicts = not args.json and not args.no_stop
    log.logger.debug('Target: "%s", Source: "%s", On Conflict: "%s", Continue: "%s", Use JSON: "%s",Override JSON: "%s", Delete JSON: "%s", Delete Source: "%s", Read Conflicts: "%s", Save Conflicts: "%s"', target, source, args.on_conflict, args.no_stop, args.json, args.override, args.del_json, args.del_source, read_conflicts, save_conflicts)
    if not (os.path.isdir(target) and os.path.isdir(source)):
        raise exceptions.CLIValidationException(messages['MERGE']['ERROR']['INVALID_PATH'])
    sfs = core.SFS.get_by_path(target)
    if not (sfs is None or fs.is_parent_dir(source, sfs.root)):
        raise exceptions.CLIValidationException(messages['MERGE']['ERROR']['NOT_IN_SFS'])
    if not fs.is_parent_dir(source, target):
        if fs.is_parent_dir(target, source):
            raise exceptions.CLIValidationException(messages['MERGE']['ERROR']['NESTED_DIR'])
        json_path = get_json_path(target)
        log.logger.debug('JSON Path: %s', json_path)
        if read_conflicts:
            if not os.path.isfile(json_path):
                raise exceptions.CLIValidationException(messages['MERGE']['ERROR']['JSON_NOT_FOUND'])
            conflicts_json = fs.load_json(json_path)
            conflicts = list(map(lambda dct: MergeConflict.from_dict(dct), conflicts_json))
            valid_status = validate_merge_conflicts(target, source, conflicts)
            if valid_status is not True:
                raise exceptions.CLIValidationException(('{}: "{}", "{}"'.format)(messages['MERGE']['ERROR']['INVALID_CONFLICTS'], *valid_status))
        else:
            conflicts = get_merge_conflicts(sfs, target, source, keep=(args.on_conflict))
        if len(conflicts) > 0 and save_conflicts:
            if os.path.isfile(json_path):
                if not args.override:
                    raise exceptions.CLIValidationException(messages['MERGE']['ERROR']['JSON_EXISTS'])
            conflicts_json = list(map(lambda con: con.to_dict(), sorted(conflicts, key=(lambda con: con.path))))
            fs.save_json(conflicts_json, json_path)
            log.cli_output('{}{}'.format(messages['MERGE']['OUTPUT']['CONFLICT_COUNT'], len(conflicts)))
            log.cli_output('{}{}'.format(messages['MERGE']['OUTPUT']['JSON_PATH'], json_path))
    else:
        merge_stats = merge(target, source, conflicts)
        log.cli_output('{}{}'.format(messages['MERGE']['OUTPUT']['CONFLICT_COUNT'], len(conflicts)))
        for prop in ('DIRS_CREATED', 'DIRS_DELETED', 'FILES_MERGED', 'LINKS_MERGED',
                     'NODES_DELETED', 'NODES_RENAMED'):
            log.cli_output('{}{}'.format(messages['MERGE']['OUTPUT'][prop], merge_stats[prop]))

    if args.del_json:
        if os.path.isfile(json_path):
            os.unlink(json_path)
    if args.del_source:
        source_count = fs.count_nodes(source)
        shutil.rmtree(source)
        log.cli_output('{}{}'.format(messages['MERGE']['OUTPUT']['SOURCE_DELETED'], source_count['links'] + source_count['files']))


class MergeConflict:

    class FileStats:

        def __init__(self, name, size=None, ctime=None, is_link=True, is_dir=False, source_path=None, source_size=None, source_ctime=None, keep=True):
            self.name = name
            self.size = size
            self.ctime = ctime
            self.is_link = is_link
            self.is_dir = is_dir
            self.source_path = source_path
            self.source_size = source_size
            self.source_ctime = source_ctime
            self.keep = keep

    def __init__(self, path, target, source):
        self.path = path
        self.target = target
        self.source = source

    def to_dict(self):
        d = collections.OrderedDict()
        d['Path'] = self.path
        d['Target'] = collections.OrderedDict()
        d['Source'] = collections.OrderedDict()
        for _dict, obj in zip([d['Target'], d['Source']], [self.target, self.source]):
            _dict['Name'] = obj.name
            _dict['Type'] = 'Symlink' if obj.is_link else 'Directory' if obj.is_dir else 'File'
            _dict['Size'] = helper.with_default(helper.get_readable_size, 'na')(obj.size)
            _dict['Last Modified'] = helper.with_default(time.ctime, 'na')(obj.ctime)
            if obj.is_link:
                _dict['Source Path'] = helper.with_default(obj.source_path, 'na')
                _dict['Source Size'] = helper.with_default(helper.get_readable_size, 'na')(obj.source_size)
                _dict['Source Last Modified'] = helper.with_default(time.ctime, 'na')(obj.source_ctime)
            _dict['Keep'] = 1 if obj.keep else 0

        return d

    @staticmethod
    def from_dict(json_dict):
        log.logger.debug(json_dict)
        target = MergeConflict.FileStats((json_dict['Target']['Name']), keep=(json_dict['Target']['Keep'] != 0))
        source = MergeConflict.FileStats((json_dict['Source']['Name']), keep=(json_dict['Source']['Keep'] != 0))
        return MergeConflict(json_dict['Path'], target, source)


def _generate_merge_paths(target, source, base_path=None):
    """Recursively enumerates all common directories in the sub-tree of target and source
    The enumerated directories are the ones with potential merge conflicts
    """
    base_path = target if base_path is None else base_path
    target_nodes = fs.separate_nodes(fs.scan_dir(target))
    source_nodes = fs.separate_nodes(fs.scan_dir(source))
    yield (os.path.relpath(target, base_path), target_nodes, source_nodes)
    target_dirs = {node.name:node for node in target_nodes.dirs}
    for node in source_nodes.dirs:
        if node.name in target_dirs:
            yield from _generate_merge_paths((target_dirs[node.name].path), (node.path), base_path=base_path)


def get_renamed_filename(name):
    """Rename a file uniquely for merging"""
    return '{}.merged.{}'.format(name, round(time.time()))


def validate_merge_conflicts--- This code section failed: ---

 L. 241         0  LOAD_CLOSURE             'target'
                2  BUILD_TUPLE_1         1 
                4  LOAD_DICTCOMP            '<code_object <dictcomp>>'
                6  LOAD_STR                 'validate_merge_conflicts.<locals>.<dictcomp>'
                8  MAKE_FUNCTION_8          'closure'
               10  LOAD_FAST                'conflicts'
               12  GET_ITER         
               14  CALL_FUNCTION_1       1  '1 positional argument'
               16  STORE_FAST               'conflicts_dict'

 L. 242        18  SETUP_LOOP          272  'to 272'
               20  LOAD_GLOBAL              _generate_merge_paths
               22  LOAD_DEREF               'target'
               24  LOAD_FAST                'source'
               26  CALL_FUNCTION_2       2  '2 positional arguments'
               28  GET_ITER         
               30  FOR_ITER            270  'to 270'
               32  UNPACK_SEQUENCE_3     3 
               34  STORE_FAST               'rel_path'
               36  STORE_FAST               'target_nodes'
               38  STORE_FAST               'source_nodes'

 L. 243        40  BUILD_MAP_0           0 
               42  STORE_FAST               'nodes_dict'

 L. 244        44  SETUP_LOOP          268  'to 268'
               46  LOAD_GLOBAL              enumerate
               48  LOAD_FAST                'target_nodes'
               50  LOAD_FAST                'source_nodes'
               52  BUILD_LIST_2          2 
               54  CALL_FUNCTION_1       1  '1 positional argument'
               56  GET_ITER         
               58  FOR_ITER            266  'to 266'
               60  UNPACK_SEQUENCE_2     2 
               62  STORE_FAST               'i'
               64  STORE_FAST               'nodes'

 L. 245        66  LOAD_FAST                'i'
               68  LOAD_CONST               0
               70  COMPARE_OP               ==
               72  STORE_FAST               'is_target'

 L. 246        74  SETUP_LOOP          264  'to 264'
               76  LOAD_GLOBAL              itertools
               78  LOAD_ATTR                chain
               80  LOAD_FAST                'nodes'
               82  CALL_FUNCTION_EX      0  'positional arguments only'
               84  GET_ITER         
               86  FOR_ITER            262  'to 262'
               88  STORE_FAST               'node'

 L. 247        90  LOAD_GLOBAL              fs
               92  LOAD_METHOD              expand_path
               94  LOAD_GLOBAL              os
               96  LOAD_ATTR                path
               98  LOAD_METHOD              join
              100  LOAD_DEREF               'target'
              102  LOAD_FAST                'rel_path'
              104  LOAD_FAST                'node'
              106  LOAD_ATTR                name
              108  CALL_METHOD_3         3  '3 positional arguments'
              110  CALL_METHOD_1         1  '1 positional argument'
              112  STORE_FAST               'node_target'

 L. 248       114  LOAD_FAST                'node_target'
              116  LOAD_FAST                'conflicts_dict'
              118  COMPARE_OP               in
              120  POP_JUMP_IF_FALSE   160  'to 160'

 L. 249       122  LOAD_GLOBAL              getattr
              124  LOAD_FAST                'conflicts_dict'
              126  LOAD_FAST                'node_target'
              128  BINARY_SUBSCR    
              130  LOAD_FAST                'is_target'
              132  POP_JUMP_IF_FALSE   138  'to 138'
              134  LOAD_STR                 'target'
              136  JUMP_FORWARD        140  'to 140'
            138_0  COME_FROM           132  '132'
              138  LOAD_STR                 'source'
            140_0  COME_FROM           136  '136'
              140  CALL_FUNCTION_2       2  '2 positional arguments'
              142  STORE_FAST               'node_stats'

 L. 250       144  LOAD_FAST                'node_stats'
              146  LOAD_ATTR                keep
              148  POP_JUMP_IF_TRUE    152  'to 152'

 L. 251       150  CONTINUE             86  'to 86'
            152_0  COME_FROM           148  '148'

 L. 252       152  LOAD_FAST                'node_stats'
              154  LOAD_ATTR                name
              156  STORE_FAST               'node_name'
              158  JUMP_FORWARD        166  'to 166'
            160_0  COME_FROM           120  '120'

 L. 254       160  LOAD_FAST                'node'
              162  LOAD_ATTR                name
              164  STORE_FAST               'node_name'
            166_0  COME_FROM           158  '158'

 L. 255       166  LOAD_FAST                'node_name'
              168  LOAD_FAST                'nodes_dict'
              170  COMPARE_OP               in
              172  POP_JUMP_IF_FALSE   248  'to 248'

 L. 256       174  LOAD_FAST                'nodes_dict'
              176  LOAD_FAST                'node_name'
              178  BINARY_SUBSCR    
              180  UNPACK_SEQUENCE_2     2 
              182  STORE_FAST               'other_node'
              184  STORE_FAST               'other_is_target'

 L. 257       186  LOAD_FAST                'is_target'
              188  POP_JUMP_IF_TRUE    236  'to 236'
              190  LOAD_FAST                'other_is_target'
              192  POP_JUMP_IF_FALSE   236  'to 236'

 L. 258       194  LOAD_FAST                'other_node'
              196  LOAD_ATTR                is_dir
              198  POP_JUMP_IF_FALSE   236  'to 236'
              200  LOAD_FAST                'node'
              202  LOAD_ATTR                is_dir
              204  POP_JUMP_IF_FALSE   236  'to 236'

 L. 259       206  LOAD_FAST                'node'
              208  LOAD_ATTR                name
              210  LOAD_FAST                'other_node'
              212  LOAD_ATTR                name
              214  DUP_TOP          
              216  ROT_THREE        
              218  COMPARE_OP               ==
              220  POP_JUMP_IF_FALSE   230  'to 230'
              222  LOAD_FAST                'node_name'
              224  COMPARE_OP               ==
              226  POP_JUMP_IF_FALSE   236  'to 236'
              228  JUMP_BACK            86  'to 86'
            230_0  COME_FROM           220  '220'
              230  POP_TOP          
              232  JUMP_FORWARD        236  'to 236'

 L. 260       234  CONTINUE             86  'to 86'
            236_0  COME_FROM           232  '232'
            236_1  COME_FROM           226  '226'
            236_2  COME_FROM           204  '204'
            236_3  COME_FROM           198  '198'
            236_4  COME_FROM           192  '192'
            236_5  COME_FROM           188  '188'

 L. 261       236  LOAD_FAST                'node'
              238  LOAD_ATTR                path
              240  LOAD_FAST                'other_node'
              242  LOAD_ATTR                path
              244  BUILD_TUPLE_2         2 
              246  RETURN_VALUE     
            248_0  COME_FROM           172  '172'

 L. 262       248  LOAD_FAST                'node'
              250  LOAD_FAST                'is_target'
              252  BUILD_TUPLE_2         2 
              254  LOAD_FAST                'nodes_dict'
              256  LOAD_FAST                'node_name'
              258  STORE_SUBSCR     
              260  JUMP_BACK            86  'to 86'
              262  POP_BLOCK        
            264_0  COME_FROM_LOOP       74  '74'
              264  JUMP_BACK            58  'to 58'
              266  POP_BLOCK        
            268_0  COME_FROM_LOOP       44  '44'
              268  JUMP_BACK            30  'to 30'
              270  POP_BLOCK        
            272_0  COME_FROM_LOOP       18  '18'

 L. 263       272  LOAD_CONST               True
              274  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_TOP' instruction at offset 230


def get_merge_conflicts(sfs, target, source, keep=constants['MERGE_MODES']['KEEP_TARGET']):
    """Compute the merge conflicts in target and source directory using conflict resolution specified through 'keep'"""
    conflicts = []
    for path, target_nodes, source_nodes in _generate_merge_paths(target, source):
        target_nodes_dict = {node.name:node for node in (itertools.chain)(*target_nodes)}
        for source_node in (itertools.chain)(*source_nodes):
            if not source_node.name not in target_nodes_dict:
                if source_node.is_dir:
                    if target_nodes_dict[source_node.name].is_dir:
                        continue
                node_stats = []
                for i, curr_node in enumerate([target_nodes_dict[source_node.name], source_node]):
                    is_source = i == 1
                    name = get_renamed_filename(curr_node.name) if is_source else curr_node.name
                    source_path = source_stats = None
                    if curr_node.is_symlink:
                        source_path = os.readlink(curr_node.path)
                        col = sfs.get_collection_by_path(source_path)
                        if col is not None:
                            source_stats = col.get_stats(source_path)
                    curr_keep = keep == constants['MERGE_MODES']['KEEP_BOTH'] or keep == constants['MERGE_MODES']['KEEP_SOURCE'] and is_source or keep == constants['MERGE_MODES']['KEEP_TARGET'] and not is_source
                    node_stats.append(MergeConflict.FileStats(name,
                      size=(curr_node.stat.size),
                      ctime=(curr_node.stat.ctime),
                      is_link=(curr_node.is_symlink),
                      is_dir=(curr_node.is_dir),
                      source_path=source_path,
                      source_size=(None if source_stats is None else source_stats.size),
                      source_ctime=(None if source_stats is None else source_stats.ctime),
                      keep=curr_keep))

                conflicts.append(MergeConflict(os.path.join(path, source_node.name), *node_stats))

    return conflicts


def merge(target, source, conflicts):
    """Merge source directory into target directory handling conflicts as specified in 'conflicts'"""
    conflicts_dict = {fs.expand_path(os.path.join(target, c.path)):c for c in conflicts}
    merge_stats = collections.defaultdict(int)
    for rel_path, target_nodes, source_nodes in _generate_merge_paths(target, source):
        target_nodes_dict = {node.name:node for node in (itertools.chain)(*target_nodes)}
        for source_node in (itertools.chain)(*source_nodes):
            target_node_path = fs.expand_path(os.path.jointargetrel_pathsource_node.name)
            conflict = conflicts_dict[target_node_path] if target_node_path in conflicts_dict else None
            if conflict:
                target_node = target_nodes_dict[source_node.name]
                if not conflict.target.keep:
                    if target_node.is_dir:
                        counts = fs.count_nodes(target_node.path)
                        merge_stats['NODES_DELETED'] += counts['files'] + counts['links']
                        merge_stats['DIRS_DELETED'] += 1 + counts['dirs']
                        shutil.rmtree(target_node.path)
                    else:
                        os.unlink(target_node.path)
                        merge_stats['NODES_DELETED'] += 1
                if target_node.name != conflict.target.name:
                    rename_path = os.path.jointargetrel_pathconflict.target.name
                    os.rename(target_node.path, rename_path)
                    merge_stats['NODES_RENAMED'] += 1
            if conflict:
                if not conflict.source.keep:
                    continue
                source_name = source_node.name if conflict is None else conflict.source.name
                merge_path = os.path.jointargetrel_pathsource_name
                if source_node.is_symlink:
                    fs.copy_symlink(source_node.path, merge_path)
                    merge_stats['LINKS_MERGED'] += 1
                elif source_node.is_file:
                    shutil.copy2(source_node.path, merge_path)
                    merge_stats['FILES_MERGED'] += 1
                else:
                    counts = os.path.isdir(merge_path) or fs.count_nodes(source_node.path)
                    merge_stats['LINKS_MERGED'] += counts['links']
                    merge_stats['FILES_MERGED'] += counts['files']
                    merge_stats['DIRS_CREATED'] += 1 + counts['dirs']
                    shutil.copytree((source_node.path), merge_path, symlinks=True)

    return merge_stats


def get_json_path(target_dir):
    """Compute path of merge conflicts JSON in the target directory"""
    return os.path.join(target_dir, os.path.basename(target_dir) + constants['MERGE_FILE_EXTENSION'] + core.constants['SFS_FILE_EXTENSION'])