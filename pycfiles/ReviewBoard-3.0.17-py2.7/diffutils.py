# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/diffviewer/diffutils.py
# Compiled at: 2020-02-11 04:03:56
from __future__ import unicode_literals
import fnmatch, logging, os, re, shutil, subprocess, tempfile
from difflib import SequenceMatcher
from django.core.exceptions import ObjectDoesNotExist
from django.utils import six
from django.utils.translation import ugettext as _
from djblets.log import log_timed
from djblets.siteconfig.models import SiteConfiguration
from djblets.util.contextmanagers import controlled_subprocess
from reviewboard.diffviewer.errors import PatchError
from reviewboard.scmtools.core import PRE_CREATION, HEAD
NEWLINE_CONVERSION_RE = re.compile(b'\\r(\\r?\\n)?')
NEWLINE_RE = re.compile(b'(?:\\n|\\r(?:\\r?\\n)?)')
ALPHANUM_RE = re.compile(b'\\w')
WHITESPACE_RE = re.compile(b'\\s')
_PATCH_GARBAGE_INPUT = b'patch: **** Only garbage was found in the patch input.'

def convert_to_unicode(s, encoding_list):
    """Returns the passed string as a unicode object.

    If conversion to unicode fails, we try the user-specified encoding, which
    defaults to ISO 8859-15. This can be overridden by users inside the
    repository configuration, which gives users repository-level control over
    file encodings.

    Ideally, we'd like to have per-file encodings, but this is hard. The best
    we can do now is a comma-separated list of things to try.

    Returns the encoding type which was used and the decoded unicode object.
    """
    if isinstance(s, bytearray):
        s = bytes(s)
    if isinstance(s, six.text_type):
        return (
         b'utf-8', s)
    if isinstance(s, six.string_types):
        try:
            enc = b'utf-8'
            return (enc, six.text_type(s, enc))
        except UnicodeError:
            for e in encoding_list:
                try:
                    return (
                     e, six.text_type(s, e))
                except (UnicodeError, LookupError):
                    pass

            try:
                enc = b'utf-8'
                return (enc, six.text_type(s, enc, errors=b'replace'))
            except UnicodeError:
                raise Exception(_(b"Diff content couldn't be converted to unicode using the following encodings: %s") % ([
                 b'utf-8'] + encoding_list))

    else:
        raise TypeError(b'Value to convert is unexpected type %s', type(s))


def convert_line_endings(data):
    if data == b'':
        return b''
    if data[(-1)] == b'\r':
        data = data[:-1]
    return NEWLINE_CONVERSION_RE.sub(b'\n', data)


def split_line_endings(data):
    r"""Splits a string into lines while preserving all non-CRLF characters.

    Unlike the string's splitlines(), this will only split on the following
    character sequences: \n, \r, \r\n, and \r\r\n.

    This is needed to prevent the sort of issues encountered with
    Unicode strings when calling splitlines(), which is that form feed
    characters would be split. patch and diff accept form feed characters
    as valid characters in diffs, and doesn't treat them as newlines, but
    splitlines() will treat it as a newline anyway.
    """
    lines = NEWLINE_RE.split(data)
    if not lines[(-1)]:
        lines = lines[:-1]
    return lines


def patch(diff, orig_file, filename, request=None):
    """Apply a diff to a file.

    This delegates out to ``patch`` because noone except Larry Wall knows how
    to patch.

    Args:
        diff (bytes):
            The contents of the diff to apply.

        orig_file (bytes):
            The contents of the original file.

        filename (unicode):
            The name of the file being patched.

        request (django.http.HttpRequest, optional):
            The HTTP request, for use in logging.

    Returns:
        bytes:
        The contents of the patched file.

    Raises:
        reviewboard.diffutils.errors.PatchError:
            An error occurred when trying to apply the patch.
    """
    log_timer = log_timed(b'Patching file %s' % filename, request=request)
    if not diff.strip():
        return orig_file
    else:
        tempdir = tempfile.mkdtemp(prefix=b'reviewboard.')
        try:
            orig_file = convert_line_endings(orig_file)
            diff = convert_line_endings(diff)
            fd, oldfile = tempfile.mkstemp(dir=tempdir)
            f = os.fdopen(fd, b'w+b')
            f.write(orig_file)
            f.close()
            newfile = b'%s-new' % oldfile
            process = subprocess.Popen([b'patch', b'-o', newfile, oldfile], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=tempdir)
            with controlled_subprocess(b'patch', process) as (p):
                stdout, stderr = p.communicate(diff)
                failure = p.returncode
            try:
                with open(newfile, b'rb') as (f):
                    new_file = f.read()
            except Exception:
                new_file = None

            if failure:
                rejects_file = b'%s.rej' % newfile
                try:
                    with open(rejects_file, b'rb') as (f):
                        rejects = f.read()
                except Exception:
                    rejects = None

                error_output = stderr.strip() or stdout.strip()
                base_filename = os.path.basename(filename)
                error_output = error_output.replace(rejects_file, b'%s.rej' % base_filename).replace(oldfile, base_filename)
                raise PatchError(filename, error_output, orig_file, new_file, diff, rejects)
            return new_file
        finally:
            shutil.rmtree(tempdir)
            log_timer.done()

        return


def get_original_file(filediff, request, encoding_list):
    """
    Get a file either from the cache or the SCM, applying the parent diff if
    it exists.

    SCM exceptions are passed back to the caller.
    """
    data = b''
    if not filediff.is_new:
        repository = filediff.diffset.repository
        data = repository.get_file(filediff.source_file, filediff.source_revision, base_commit_id=filediff.diffset.base_commit_id, request=request)
        encoding, data = convert_to_unicode(data, encoding_list)
        data = convert_line_endings(data)
        data = data.encode(encoding)
    if filediff.parent_diff and (not filediff.extra_data or not filediff.extra_data.get(b'parent_moved', False)) and not filediff.is_parent_diff_empty(cache_only=True):
        try:
            data = patch(filediff.parent_diff, data, filediff.source_file, request)
        except PatchError as e:
            if e.error_output == _PATCH_GARBAGE_INPUT and not filediff.is_parent_diff_empty():
                raise

    return data


def get_patched_file(source_data, filediff, request=None):
    """Return the patched version of a file.

    This will normalize the patch, applying any changes needed for the
    repository, and then patch the provided data with the patch contents.

    Args:
        source_data (bytes):
            The file contents to patch.

        filediff (reviewboard.diffviewer.models.filediff.FileDiff):
            The FileDiff representing the patch.

        request (django.http.HttpClient, optional):
            The HTTP request from the client.

    Returns:
        bytes:
        The patched file contents.
    """
    diff = filediff.diffset.repository.normalize_patch(patch=filediff.diff, filename=filediff.source_file, revision=filediff.source_revision)
    return patch(diff=diff, orig_file=source_data, filename=filediff.dest_file, request=request)


def get_revision_str(revision):
    if revision == HEAD:
        return b'HEAD'
    else:
        if revision == PRE_CREATION:
            return b''
        return _(b'Revision %s') % revision


def get_filenames_match_patterns(patterns, filenames):
    """Return whether any of the filenames match any of the patterns.

    This is used to compare a list of filenames to a list of
    :py:mod:`patterns <fnmatch>`. The patterns are case-sensitive.

    Args:
        patterns (list of unicode):
            The list of patterns to match against.

        filename (list of unicode):
            The list of filenames.

    Returns:
        bool:
        ``True`` if any filenames match any patterns. ``False`` if none match.
    """
    for pattern in patterns:
        for filename in filenames:
            if fnmatch.fnmatchcase(filename, pattern):
                return True

    return False


def get_matched_interdiff_files(tool, filediffs, interfilediffs):
    """Generate pairs of matched files for display in interdiffs.

    This compares a list of filediffs and a list of interfilediffs, attempting
    to best match up the files in both for display in the diff viewer.

    This will prioritize matches that share a common source filename,
    destination filename, and new/deleted state. Failing that, matches that
    share a common source filename are paired off.

    Any entries in ``interfilediffs` that don't have any match in ``filediffs``
    are considered new changes in the interdiff, and any entries in
    ``filediffs`` that don't have entries in ``interfilediffs`` are considered
    reverted changes.

    Args:
        tool (reviewboard.scmtools.core.SCMTool)
            The tool used for all these diffs.

        filediffs (list of reviewboard.diffviewer.models.FileDiff):
            The list of filediffs on the left-hand side of the diff range.

        interfilediffs (list of reviewboard.diffviewer.models.FileDiff):
            The list of filediffs on the right-hand side of the diff range.

    Yields:
        tuple:
        A paired off filediff match. This is a tuple containing two entries,
        each a :py:class:`~reviewboard.diffviewer.models.FileDiff` or ``None``.
    """
    parser = tool.get_parser(b'')
    _normfile = parser.normalize_diff_filename

    def _make_detail_key(filediff):
        return (
         _normfile(filediff.source_file),
         _normfile(filediff.dest_file),
         filediff.is_new,
         filediff.deleted)

    detail_interdiff_map = {}
    simple_interdiff_map = {}
    remaining_interfilediffs = set()
    for interfilediff in interfilediffs:
        source_file = _normfile(interfilediff.source_file)
        detail_key = _make_detail_key(interfilediff)
        remaining_interfilediffs.add(interfilediff)
        detail_interdiff_map[detail_key] = interfilediff
        simple_interdiff_map.setdefault(source_file, set()).add(interfilediff)

    remaining_filediffs = []
    for filediff in filediffs:
        source_file = _normfile(filediff.source_file)
        try:
            interfilediff = detail_interdiff_map.pop(_make_detail_key(filediff))
        except KeyError:
            remaining_filediffs.append(filediff)
            continue

        yield (filediff, interfilediff)
        if interfilediff:
            remaining_interfilediffs.discard(interfilediff)
            try:
                simple_interdiff_map.get(source_file, []).remove(interfilediff)
            except ValueError:
                pass

    new_remaining_filediffs = []
    for filediff in remaining_filediffs:
        source_file = _normfile(filediff.source_file)
        found_interfilediffs = [ temp_interfilediff for temp_interfilediff in simple_interdiff_map.get(source_file, []) if temp_interfilediff.dest_file == filediff.dest_file and filediff.source_file != filediff.dest_file
                               ]
        if found_interfilediffs:
            remaining_interfilediffs.difference_update(found_interfilediffs)
            for interfilediff in found_interfilediffs:
                simple_interdiff_map[source_file].remove(interfilediff)
                yield (filediff, interfilediff)

        else:
            new_remaining_filediffs.append(filediff)

    remaining_filediffs = new_remaining_filediffs
    new_remaining_filediffs = []
    for filediff in remaining_filediffs:
        source_file = _normfile(filediff.source_file)
        found_interfilediffs = [ temp_interfilediff for temp_interfilediff in simple_interdiff_map.get(source_file, []) if temp_interfilediff.is_new == filediff.is_new and temp_interfilediff.deleted == filediff.deleted
                               ]
        if found_interfilediffs:
            remaining_interfilediffs.difference_update(found_interfilediffs)
            for interfilediff in found_interfilediffs:
                simple_interdiff_map[source_file].remove(interfilediff)
                yield (filediff, interfilediff)

        else:
            new_remaining_filediffs.append(filediff)

    remaining_filediffs = new_remaining_filediffs
    for filediff in remaining_filediffs:
        source_file = _normfile(filediff.source_file)
        found_interfilediffs = [ temp_interfilediff for temp_interfilediff in simple_interdiff_map.get(source_file, []) if (filediff.is_new or not temp_interfilediff.is_new or not filediff.is_new and temp_interfilediff.is_new and filediff.dest_detail == temp_interfilediff.dest_detail) and (not filediff.deleted or temp_interfilediff.deleted)
                               ]
        if found_interfilediffs:
            remaining_interfilediffs.difference_update(found_interfilediffs)
            for interfilediff in found_interfilediffs:
                yield (
                 filediff, interfilediff)

        else:
            yield (
             filediff, None)

    for interfilediff in remaining_interfilediffs:
        yield (
         None, interfilediff)

    return


def get_diff_files(diffset, filediff=None, interdiffset=None, interfilediff=None, request=None, filename_patterns=None):
    """Return a list of files that will be displayed in a diff.

    This will go through the given diffset/interdiffset, or a given filediff
    within that diffset, and generate the list of files that will be
    displayed. This file list will contain a bunch of metadata on the files,
    such as the index, original/modified names, revisions, associated
    filediffs/diffsets, and so on.

    This can be used along with :py:func:`populate_diff_chunks` to build a full
    list containing all diff chunks used for rendering a side-by-side diff.

    Args:
        diffset (reviewboard.diffviewer.models.DiffSet):
            The diffset containing the files to return.

        filediff (reviewboard.diffviewer.models.FileDiff, optional):
            A specific file in the diff to return information for.

        interdiffset (reviewboard.diffviewer.models.DiffSet, optional):
            A second diffset used for an interdiff range.

        interfilediff (reviewboard.diffviewer.models.FileDiff, optional):
            A second specific file in ``interdiffset`` used to return
            information for. This should be provided if ``filediff`` and
            ``interdiffset`` are both provided. If it's ``None`` in this
            case, then the diff will be shown as reverted for this file.

        filename_patterns (list of unicode, optional):
            A list of filenames or :py:mod:`patterns <fnmatch>` used to
            limit the results. Each of these will be matched against the
            original and modified file of diffs and interdiffs.

    Returns:
        list of dict:
        A list of dictionaries containing information on the files to show
        in the diff, in the order in which they would be shown.
    """
    if filediff:
        filediffs = [
         filediff]
        if interdiffset:
            log_timer = log_timed(b'Generating diff file info for interdiffset ids %s-%s, filediff %s' % (
             diffset.id, interdiffset.id, filediff.id), request=request)
        else:
            log_timer = log_timed(b'Generating diff file info for diffset id %s, filediff %s' % (
             diffset.id, filediff.id), request=request)
    else:
        filediffs = list(diffset.files.select_related().all())
        if interdiffset:
            log_timer = log_timed(b'Generating diff file info for interdiffset ids %s-%s' % (
             diffset.id, interdiffset.id), request=request)
        else:
            log_timer = log_timed(b'Generating diff file info for diffset id %s' % diffset.id, request=request)
        tool = diffset.repository.get_scmtool()
        if interdiffset:
            if not filediff:
                interfilediffs = list(interdiffset.files.all())
            else:
                if interfilediff:
                    interfilediffs = [
                     interfilediff]
                else:
                    interfilediffs = []
                filediff_parts = []
                matched_filediffs = get_matched_interdiff_files(tool=tool, filediffs=filediffs, interfilediffs=interfilediffs)
                for temp_filediff, temp_interfilediff in matched_filediffs:
                    if temp_filediff:
                        filediff_parts.append((temp_filediff, temp_interfilediff,
                         True))
                    elif temp_interfilediff:
                        filediff_parts.append((temp_interfilediff, None, False))
                    else:
                        logging.error(b'get_matched_interdiff_files returned an entry with an empty filediff and interfilediff for diffset=%r, interdiffset=%r, filediffs=%r, interfilediffs=%r', diffset, interdiffset, filediffs, interfilediffs)
                        raise ValueError(b'Internal error: get_matched_interdiff_files returned an entry with an empty filediff and interfilediff! Please report this along with information from the server error log.')

        else:
            filediff_parts = [ (temp_filediff, None, False) for temp_filediff in filediffs
                             ]
        files = []
        for parts in filediff_parts:
            filediff, interfilediff, force_interdiff = parts
            newfile = filediff.is_new
            if interdiffset:
                if filediff and interfilediff and (filediff.diff == interfilediff.diff or filediff.deleted and interfilediff.deleted or filediff.patched_sha1 is not None and filediff.patched_sha1 == interfilediff.patched_sha1):
                    continue
                source_revision = _(b'Diff Revision %s') % diffset.revision
            else:
                source_revision = get_revision_str(filediff.source_revision)
            if interfilediff:
                dest_revision = _(b'Diff Revision %s') % interdiffset.revision
            elif force_interdiff:
                dest_revision = _(b'Diff Revision %s - File Reverted') % interdiffset.revision
            elif newfile:
                dest_revision = _(b'New File')
            else:
                dest_revision = _(b'New Change')
            if interfilediff:
                raw_depot_filename = filediff.dest_file
                raw_dest_filename = interfilediff.dest_file
            else:
                raw_depot_filename = filediff.source_file
                raw_dest_filename = filediff.dest_file
            depot_filename = tool.normalize_path_for_display(raw_depot_filename)
            dest_filename = tool.normalize_path_for_display(raw_dest_filename)
            if filename_patterns:
                if dest_filename == depot_filename:
                    filenames = [
                     dest_filename]
                else:
                    filenames = [
                     dest_filename, depot_filename]
                if not get_filenames_match_patterns(patterns=filename_patterns, filenames=filenames):
                    continue
            f = {b'depot_filename': depot_filename, 
               b'dest_filename': dest_filename or depot_filename, 
               b'revision': source_revision, 
               b'dest_revision': dest_revision, 
               b'filediff': filediff, 
               b'interfilediff': interfilediff, 
               b'force_interdiff': force_interdiff, 
               b'binary': filediff.binary, 
               b'deleted': filediff.deleted, 
               b'moved': filediff.moved, 
               b'copied': filediff.copied, 
               b'moved_or_copied': filediff.moved or filediff.copied, 
               b'newfile': newfile, 
               b'is_symlink': filediff.extra_data.get(b'is_symlink', False), 
               b'index': len(files), 
               b'chunks_loaded': False, 
               b'is_new_file': newfile and not interfilediff and not filediff.parent_diff}
            if force_interdiff:
                f[b'force_interdiff_revision'] = interdiffset.revision
            files.append(f)

    log_timer.done()
    if len(files) == 1:
        return files
    else:
        return get_sorted_filediffs(files, key=lambda f: f[b'interfilediff'] or f[b'filediff'])
        return


def populate_diff_chunks(files, enable_syntax_highlighting=True, request=None):
    """Populates a list of diff files with chunk data.

    This accepts a list of files (generated by get_diff_files) and generates
    diff chunk data for each file in the list. The chunk data is stored in
    the file state.
    """
    from reviewboard.diffviewer.chunk_generator import get_diff_chunk_generator
    for diff_file in files:
        generator = get_diff_chunk_generator(request, diff_file[b'filediff'], diff_file[b'interfilediff'], diff_file[b'force_interdiff'], enable_syntax_highlighting)
        chunks = list(generator.get_chunks())
        diff_file.update({b'chunks': chunks, 
           b'num_chunks': len(chunks), 
           b'changed_chunk_indexes': [], b'whitespace_only': len(chunks) > 0})
        for j, chunk in enumerate(chunks):
            chunk[b'index'] = j
            if chunk[b'change'] != b'equal':
                diff_file[b'changed_chunk_indexes'].append(j)
                meta = chunk.get(b'meta', {})
                if not meta.get(b'whitespace_chunk', False):
                    diff_file[b'whitespace_only'] = False

        diff_file.update({b'num_changes': len(diff_file[b'changed_chunk_indexes']), 
           b'chunks_loaded': True})


def get_file_from_filediff(context, filediff, interfilediff):
    """Return the files that corresponds to the filediff/interfilediff.

    This is primarily intended for use with templates. It takes a
    RequestContext for looking up the user and for caching file lists,
    in order to improve performance and reduce lookup times for files that have
    already been fetched.

    This function returns either exactly one file or ``None``.
    """
    interdiffset = None
    key = b'_diff_files_%s_%s' % (filediff.diffset.id, filediff.id)
    if interfilediff:
        key += b'_%s' % interfilediff.id
        interdiffset = interfilediff.diffset
    if key in context:
        files = context[key]
    else:
        assert b'user' in context
        request = context.get(b'request', None)
        files = get_diff_files(filediff.diffset, filediff, interdiffset, interfilediff=interfilediff, request=request)
        populate_diff_chunks(files, get_enable_highlighting(context[b'user']), request=request)
        context[key] = files
    if not files:
        return
    else:
        assert len(files) == 1
        return files[0]


def get_last_line_number_in_diff(context, filediff, interfilediff):
    """Determine the last virtual line number in the filediff/interfilediff.

    This returns the virtual line number to be used in expandable diff
    fragments.
    """
    f = get_file_from_filediff(context, filediff, interfilediff)
    last_chunk = f[b'chunks'][(-1)]
    last_line = last_chunk[b'lines'][(-1)]
    return last_line[0]


def _get_last_header_in_chunks_before_line(chunks, target_line):
    """Find the last header in the list of chunks before the target line."""

    def find_last_line_numbers(lines):
        """Return a tuple of the last line numbers in the given list of lines.

        The last line numbers are not always contained in the last element of
        the ``lines`` list. This is the case when dealing with interdiffs that
        have filtered out opcodes.

        See :py:func:`get_chunks_in_range` for a description of what is
        contained in each element of ``lines``.
        """
        last_left = None
        last_right = None
        for line in reversed(lines):
            if not last_right and line[4]:
                last_right = line[4]
            if not last_left and line[1]:
                last_left = line[1]
            if last_left and last_right:
                break

        return (
         last_left, last_right)

    def find_header(headers, offset, last_line):
        """Return the last header that occurs before a line.

        The offset parameter is the difference between the virtual number and
        and actual line number in the chunk. This is required because the
        header line numbers are original or patched line numbers, not virtual
        line numbers.
        """
        end_line = min(last_line, target_line)
        for header in reversed(headers):
            virtual_line = header[0] + offset
            if virtual_line < end_line:
                return {b'line': virtual_line, 
                   b'text': header[1]}

    header = {b'left': None, 
       b'right': None}
    for chunk in chunks:
        lines = chunk[b'lines']
        virtual_first_line = lines[0][0]
        if virtual_first_line <= target_line:
            if virtual_first_line == target_line:
                break
            last_left, last_right = find_last_line_numbers(lines)
            if b'left_headers' in chunk[b'meta'] and lines[0][1]:
                offset = virtual_first_line - lines[0][1]
                left_header = find_header(chunk[b'meta'][b'left_headers'], offset, last_left + offset)
                header[b'left'] = left_header or header[b'left']
            if b'right_headers' in chunk[b'meta'] and lines[0][4]:
                offset = virtual_first_line - lines[0][4]
                right_header = find_header(chunk[b'meta'][b'right_headers'], offset, last_right + offset)
                header[b'right'] = right_header or header[b'right']
        else:
            break

    return header


def get_last_header_before_line(context, filediff, interfilediff, target_line):
    """Get the last header that occurs before the given line.

    This returns a dictionary of ``left`` header and ``right`` header. Each
    header is either ``None`` or a dictionary with the following fields:

    ======== ==============================================================
    Field    Description
    ======== ==============================================================
    ``line`` Virtual line number (union of the original and patched files)
    ``text`` The header text
    ======== ==============================================================
    """
    f = get_file_from_filediff(context, filediff, interfilediff)
    return _get_last_header_in_chunks_before_line(f[b'chunks'], target_line)


def get_file_chunks_in_range(context, filediff, interfilediff, first_line, num_lines):
    """Generate the chunks within a range of lines in the specified filediff.

    This is primarily intended for use with templates. It takes a
    RequestContext for looking up the user and for caching file lists,
    in order to improve performance and reduce lookup times for files that have
    already been fetched.

    See :py:func:`get_chunks_in_range` for information on the returned state
    of the chunks.
    """
    f = get_file_from_filediff(context, filediff, interfilediff)
    if f:
        return get_chunks_in_range(f[b'chunks'], first_line, num_lines)
    else:
        return []


def get_chunks_in_range(chunks, first_line, num_lines):
    """Generate the chunks within a range of lines of a larger list of chunks.

    This takes a list of chunks, computes a subset of those chunks from the
    line ranges provided, and generates a new set of those chunks.

    Each returned chunk is a dictionary with the following fields:

    ============= ========================================================
    Variable      Description
    ============= ========================================================
    ``change``    The change type ("equal", "replace", "insert", "delete")
    ``numlines``  The number of lines in the chunk.
    ``lines``     The list of lines in the chunk.
    ``meta``      A dictionary containing metadata on the chunk
    ============= ========================================================

    Each line in the list of lines is an array with the following data:

    ======== =============================================================
    Index    Description
    ======== =============================================================
    0        Virtual line number (union of the original and patched files)
    1        Real line number in the original file
    2        HTML markup of the original file
    3        Changed regions of the original line (for "replace" chunks)
    4        Real line number in the patched file
    5        HTML markup of the patched file
    6        Changed regions of the patched line (for "replace" chunks)
    7        True if line consists of only whitespace changes
    ======== =============================================================
    """
    for i, chunk in enumerate(chunks):
        lines = chunk[b'lines']
        if lines[(-1)][0] >= first_line >= lines[0][0]:
            start_index = first_line - lines[0][0]
            if first_line + num_lines <= lines[(-1)][0]:
                last_index = start_index + num_lines
            else:
                last_index = len(lines)
            new_chunk = {b'index': i, 
               b'lines': chunk[b'lines'][start_index:last_index], 
               b'numlines': last_index - start_index, 
               b'change': chunk[b'change'], 
               b'meta': chunk.get(b'meta', {})}
            yield new_chunk
            first_line += new_chunk[b'numlines']
            num_lines -= new_chunk[b'numlines']
            assert num_lines >= 0
            if num_lines == 0:
                break


def get_enable_highlighting(user):
    user_syntax_highlighting = True
    if user.is_authenticated():
        try:
            profile = user.get_profile()
            user_syntax_highlighting = profile.syntax_highlighting
        except ObjectDoesNotExist:
            pass

    siteconfig = SiteConfiguration.objects.get_current()
    return siteconfig.get(b'diffviewer_syntax_highlighting') and user_syntax_highlighting


def get_line_changed_regions(oldline, newline):
    """Returns regions of changes between two similar lines."""
    if oldline is None or newline is None:
        return (None, None)
    differ = SequenceMatcher(None, oldline, newline)
    if differ.ratio() < 0.6:
        return (None, None)
    else:
        oldchanges = []
        newchanges = []
        back = (0, 0)
        for tag, i1, i2, j1, j2 in differ.get_opcodes():
            if tag == b'equal':
                if i2 - i1 < 3 or j2 - j1 < 3:
                    back = (
                     j2 - j1, i2 - i1)
                continue
            oldstart, oldend = i1 - back[0], i2
            newstart, newend = j1 - back[1], j2
            if oldchanges and oldstart <= oldchanges[(-1)][1] < oldend:
                oldchanges[-1] = (
                 oldchanges[(-1)][0], oldend)
            elif not oldline[oldstart:oldend].isspace():
                oldchanges.append((oldstart, oldend))
            if newchanges and newstart <= newchanges[(-1)][1] < newend:
                newchanges[-1] = (
                 newchanges[(-1)][0], newend)
            elif not newline[newstart:newend].isspace():
                newchanges.append((newstart, newend))
            back = (0, 0)

        return (oldchanges, newchanges)


def get_sorted_filediffs(filediffs, key=None):
    """Sorts a list of filediffs.

    The list of filediffs will be sorted first by their base paths in
    ascending order.

    Within a base path, they'll be sorted by base name (minus the extension)
    in ascending order.

    If two files have the same base path and base name, we'll sort by the
    extension in descending order. This will make :file:`*.h` sort ahead of
    :file:`*.c`/:file:`*.cpp`, for example.

    If the list being passed in is actually not a list of FileDiffs, it
    must provide a callable ``key`` parameter that will return a FileDiff
    for the given entry in the list. This will only be called once per
    item.
    """

    def cmp_filediffs(x, y):
        if x[0] != y[0]:
            return cmp(x[0], y[0])
        else:
            x_file, x_ext = os.path.splitext(x[1])
            y_file, y_ext = os.path.splitext(y[1])
            if x_file == y_file:
                return cmp(y_ext, x_ext)
            return cmp(x_file, y_file)

    def make_key(filediff):
        if key:
            filediff = key(filediff)
        filename = filediff.dest_file
        i = filename.rfind(b'/')
        if i == -1:
            return (b'', filename)
        else:
            return (
             filename[:i], filename[i + 1:])

    return sorted(filediffs, cmp=cmp_filediffs, key=make_key)


def get_displayed_diff_line_ranges(chunks, first_vlinenum, last_vlinenum):
    """Return the displayed line ranges based on virtual line numbers.

    This takes the virtual line numbers (the index in the side-by-side diff
    lines) and returns the human-readable line numbers, the chunks they're in,
    and mapped virtual line numbers.

    A virtual line range may start or end in a chunk not containing displayed
    line numbers (such as an "original" range starting/ending in an "insert"
    chunk). The resulting displayed line ranges will exclude these chunks.

    Args:
        chunks (list of dict):
            The list of chunks for the diff.

        first_vlinenum (int):
            The first virtual line number. This uses 1-based indexes.

        last_vlinenum (int):
            The last virtual line number. This uses 1-based indexes.

    Returns:
        tuple:
        A tuple of displayed line range information, containing 2 items.

        Each item will either be a dictionary of information, or ``None``
        if there aren't any displayed lines to show.

        The dictionary contains the following keys:

        ``display_range``:
            A tuple containing the displayed line range.

        ``virtual_range``:
            A tuple containing the virtual line range that ``display_range``
            maps to.

        ``chunk_range``:
            A tuple containing the beginning/ending chunks that
            ``display_range`` maps to.

    Raises:
        ValueError:
            The range provided was invalid.
    """
    if first_vlinenum < 0:
        raise ValueError(b'first_vlinenum must be >= 0')
    if last_vlinenum < first_vlinenum:
        raise ValueError(b'last_vlinenum must be >= first_vlinenum')
    orig_start_linenum = None
    orig_end_linenum = None
    orig_start_chunk = None
    orig_last_valid_chunk = None
    patched_start_linenum = None
    patched_end_linenum = None
    patched_start_chunk = None
    patched_last_valid_chunk = None
    for chunk in chunks:
        lines = chunk[b'lines']
        if not lines:
            logging.warning(b'get_displayed_diff_line_ranges: Encountered empty chunk %r', chunk)
            continue
        first_line = lines[0]
        last_line = lines[(-1)]
        chunk_first_vlinenum = first_line[0]
        chunk_last_vlinenum = last_line[0]
        if first_vlinenum > chunk_last_vlinenum:
            continue
        if last_vlinenum < chunk_first_vlinenum:
            break
        change = chunk[b'change']
        valid_for_orig = change != b'insert' and first_line[1]
        valid_for_patched = change != b'delete' and first_line[4]
        if valid_for_orig:
            orig_last_valid_chunk = chunk
            if not orig_start_chunk:
                orig_start_chunk = chunk
        if valid_for_patched:
            patched_last_valid_chunk = chunk
            if not patched_start_chunk:
                patched_start_chunk = chunk
        if chunk_first_vlinenum <= first_vlinenum <= chunk_last_vlinenum:
            offset = first_vlinenum - chunk_first_vlinenum
            if valid_for_orig:
                orig_start_linenum = first_line[1] + offset
                orig_start_vlinenum = first_line[0] + offset
            if valid_for_patched:
                patched_start_linenum = first_line[4] + offset
                patched_start_vlinenum = first_line[0] + offset
        elif first_vlinenum < chunk_first_vlinenum:
            if orig_start_linenum is None and valid_for_orig:
                orig_start_linenum = first_line[1]
                orig_start_vlinenum = first_line[0]
            if patched_start_linenum is None and valid_for_patched:
                patched_start_linenum = first_line[4]
                patched_start_vlinenum = first_line[0]

    if orig_last_valid_chunk:
        lines = orig_last_valid_chunk[b'lines']
        first_line = lines[0]
        last_line = lines[(-1)]
        offset = last_vlinenum - first_line[0]
        orig_end_linenum = min(last_line[1], first_line[1] + offset)
        orig_end_vlinenum = min(last_line[0], first_line[0] + offset)
        assert orig_end_linenum >= orig_start_linenum
        assert orig_end_vlinenum >= orig_start_vlinenum
        orig_range_info = {b'display_range': (
                            orig_start_linenum, orig_end_linenum), 
           b'virtual_range': (
                            orig_start_vlinenum, orig_end_vlinenum), 
           b'chunk_range': (
                          orig_start_chunk, orig_last_valid_chunk)}
    else:
        orig_range_info = None
    if patched_last_valid_chunk:
        lines = patched_last_valid_chunk[b'lines']
        first_line = lines[0]
        last_line = lines[(-1)]
        offset = last_vlinenum - first_line[0]
        patched_end_linenum = min(last_line[4], first_line[4] + offset)
        patched_end_vlinenum = min(last_line[0], first_line[0] + offset)
        assert patched_end_linenum >= patched_start_linenum
        assert patched_end_vlinenum >= patched_start_vlinenum
        patched_range_info = {b'display_range': (
                            patched_start_linenum, patched_end_linenum), 
           b'virtual_range': (
                            patched_start_vlinenum, patched_end_vlinenum), 
           b'chunk_range': (
                          patched_start_chunk, patched_last_valid_chunk)}
    else:
        patched_range_info = None
    return (orig_range_info, patched_range_info)