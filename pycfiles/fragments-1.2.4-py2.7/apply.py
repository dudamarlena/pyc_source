# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-x86_64/egg/fragments/apply.py
# Compiled at: 2012-11-06 05:50:09
from __future__ import unicode_literals
import os, argparse
from . import _iterate_over_files, _smart_open
from .precisecodevillemerge import Weave
from .config import FragmentsConfig
from .diff import _diff_group, _split_diff
from .color import Prompt

def apply(*args):
    """
    Apply changes in SOURCE_FILENAME that were made since last commit, where possible.
    Limit application to TARGET_FILENAME(s) if specified.
    Files that conflict in their entirety will be skipped.
    Smaller conflicts will be written to the file as conflict sections.

    In interactive mode, you can use the following commands:

        y - include this change
        n - do not include this change
        a - include this change and all remaining changes
        d - done, do not include this change nor any remaining changes
        j - leave this change undecided, see next undecided change
        k - leave this change undecided, see previous undecided change
        ? - interactive apply mode help
    """
    parser = argparse.ArgumentParser(prog=b'%s %s' % (__package__, apply.__name__), description=apply.__doc__)
    parser.add_argument(b'SOURCE_FILENAME', help=b'file containing changes to be applied')
    parser.add_argument(b'TARGET_FILENAME', help=b'file(s) to apply changes to', nargs=b'*')
    parser.add_argument(b'-U', b'--unified', type=int, dest=b'NUM', default=3, action=b'store', help=b'number of lines of context to show')
    group = parser.add_mutually_exclusive_group()
    group.add_argument(b'-i', b'--interactive', action=b'store_true', default=True, dest=b'interactive', help=b'interactively select changes to apply')
    group.add_argument(b'-a', b'--automatic', action=b'store_false', default=False, dest=b'interactive', help=b'automatically apply all changes')
    args = parser.parse_args(args)
    config = FragmentsConfig()
    weave = Weave()
    changed_path = os.path.realpath(args.SOURCE_FILENAME)
    changed_key = os.path.relpath(changed_path, config.root)
    if changed_key not in config[b'files']:
        yield b"Could not apply changes in '%s', it is not being followed" % os.path.relpath(changed_path)
        return
    else:
        if not os.access(changed_path, os.R_OK | os.W_OK):
            yield b"Could not apply changes in '%s', it no longer exists on disk" % os.path.relpath(changed_path)
            return
        old_path = os.path.join(config.directory, config[b'files'][changed_key])
        if not os.access(old_path, os.R_OK | os.W_OK):
            yield b"Could not apply changes in '%s', it has never been committed" % os.path.relpath(changed_path)
            return
        old_revision = 1
        with _smart_open(old_path, b'r') as (old_file):
            weave.add_revision(old_revision, old_file.readlines(), [])
        new_revision = 2
        with _smart_open(changed_path, b'r') as (new_file):
            weave.add_revision(new_revision, new_file.readlines(), [])
        diff = weave.merge(old_revision, new_revision)
        preserve_changes = {}
        discard_changes = {}
        display_groups = list(_split_diff(diff, context_lines=args.NUM))
        index = 0
        apply_all = None
        while display_groups:
            display_group = display_groups[index]
            if apply_all is None:
                for dl in _diff_group(display_group):
                    yield dl

            while True:
                if args.interactive and apply_all is None:
                    response = yield Prompt(b'Apply this change? [ynadjk?]')
                    if not response:
                        continue
                    response = response.lower()
                if not args.interactive or response.startswith(b'y') or apply_all == True:
                    for old_line, new_line, line_or_conflict in display_group:
                        if isinstance(line_or_conflict, tuple):
                            preserve_changes[(old_line, new_line)] = line_or_conflict

                    display_groups.pop(index)
                    break
                elif response.startswith(b'n') or apply_all == False:
                    for old_line, new_line, line_or_conflict in display_group:
                        if isinstance(line_or_conflict, tuple):
                            discard_changes[(old_line, new_line)] = line_or_conflict

                    display_groups.pop(index)
                    break
                elif response == b'j':
                    index = (index + 1) % len(display_groups)
                    break
                elif response == b'k':
                    index = (index - 1) % len(display_groups)
                    break
                elif response == b'a':
                    index = 0
                    apply_all = True
                    break
                elif response == b'd':
                    index = 0
                    apply_all = False
                    break
                elif response == b'?':
                    for l in apply.__doc__.split(b'\n')[-8:-1]:
                        yield l.strip()

        if not preserve_changes:
            yield b"No changes in '%s' to apply." % os.path.relpath(changed_path)
            return
        changes_to_apply = []
        i = 0
        old_line = 0
        new_line = 0
        while i < len(diff):
            line_or_conflict = diff[i]
            if isinstance(line_or_conflict, tuple):
                old, new = line_or_conflict
                if (old_line, new_line) in preserve_changes:
                    changes_to_apply.extend(new)
                elif (
                 old_line, new_line) in discard_changes:
                    changes_to_apply.extend(old)
                else:
                    raise Exception(b'Catastrophic error in selecting diff chunks. Please report a bug.')
                old_line += len(old)
                new_line += len(new)
                i += 1
            else:
                old_line += 1
                new_line += 1
                i += 1
                changes_to_apply.append(line_or_conflict)

        current_revision = changed_revision = 3
        weave.add_revision(changed_revision, changes_to_apply, [1])
        for other_path in _iterate_over_files(args.TARGET_FILENAME, config):
            other_key = os.path.relpath(other_path, config.root)
            if other_path == changed_path:
                continue
            current_revision += 1
            with _smart_open(other_path, b'r') as (other_file):
                weave.add_revision(current_revision, other_file.readlines(), [])
            merge_result = weave.cherry_pick(changed_revision, current_revision)
            if len(merge_result) == 1 and isinstance(merge_result[0], tuple):
                yield b"Changes in '%s' cannot apply to '%s', skipping" % (os.path.relpath(changed_path), os.path.relpath(other_path))
            elif tuple in set(type(mr) for mr in merge_result):
                with _smart_open(other_path, b'w') as (other_file):
                    for line_or_conflict in merge_result:
                        if isinstance(line_or_conflict, tuple):
                            other_file.write(b'>>>>>>>\n')
                            for line in line_or_conflict[0]:
                                other_file.write(line)

                            other_file.write(b'=======\n')
                            for line in line_or_conflict[1]:
                                other_file.write(line)

                            other_file.write(b'>>>>>>>\n')
                        else:
                            other_file.write(line_or_conflict)

                yield b"Conflict merging '%s' into '%s'" % (os.path.relpath(changed_path), os.path.relpath(other_path))
            else:
                with _smart_open(other_path, b'w') as (other_file):
                    other_file.writelines(merge_result)
                yield b"Changes in '%s' applied cleanly to '%s'" % (os.path.relpath(changed_path), os.path.relpath(other_path))

        return