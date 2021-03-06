# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/couchish/filehandling.py
# Compiled at: 2010-01-26 08:15:03
__doc__ = '\nViews we can build:\n    * by type, one view should be ok\n    * x_by_y views, from config (optional)\n    * ref and ref reversed views, one pair per relationship\n'
from dottedish import dotted, flatten, dotteddict, api, dottedlist
from couchdbsession import a8n
import base64, uuid
from schemaish.type import File
from StringIO import StringIO
import shutil
from couchish import jsonutil

def get_attr(prefix, parent=None):
    if parent is None:
        segments = [ str(segment) for segment in prefix ]
        return ('.').join(segments)
    else:
        if prefix is None:
            return parent
        segments = [ str(segment) for segment in prefix ]
        if parent != '':
            segments += parent.split('.')
        attr = ('.').join(segments)
        return attr


def get_files(data, original=None, prefix=None):
    files = {}
    inlinefiles = {}
    original_files = {}
    get_files_from_original(data, original, files, inlinefiles, original_files, prefix)
    get_files_from_data(data, original, files, inlinefiles, original_files, prefix)
    return (
     data, files, inlinefiles, original_files)


def has_unmodified_signature(f):
    if f.file is None:
        return True
    else:
        return False


def dotted_or_emptydict(d):
    if d is None:
        return {}
    else:
        try:
            return dotted(d)
        except TypeError:
            return d

        return


def get_files_from_data(data, original, files, inlinefiles, original_files, prefix):
    if isinstance(data, File):
        get_file_from_item(data, original, files, inlinefiles, original_files, get_attr(prefix))
        return
    else:
        if not isinstance(data, dict) and not isinstance(data, list):
            return
        dd = dotted_or_emptydict(data)
        ddoriginal = dotted_or_emptydict(original)
        if not dd:
            return
        for (k, f) in flatten(dd):
            if isinstance(f, File):
                if isinstance(ddoriginal.get(k), File):
                    of = ddoriginal[k]
                else:
                    of = None
                get_file_from_item(f, of, files, inlinefiles, original_files, get_attr(prefix, k))

        return


api.wrap.when_type(a8n.List)(dottedlist.wrap_list)
api.wrap.when_type(a8n.Dictionary)(dotteddict.wrap_dict)

def get_file_from_item(f, of, files, inlinefiles, original_files, fullprefix):
    if f.file is None:
        f.id = of.id
        if f.mimetype is None:
            f.mimetype = of.mimetype
        if f.filename is None:
            f.filename = of.filename
        if not hasattr(f, 'metadata') or f.metadata is None or f.metadata == {}:
            f.metadata = getattr(of, 'metadata', None)
    else:
        if of and hasattr(of, 'id'):
            f.id = of.id
        else:
            f.id = uuid.uuid4().hex
        if getattr(f, 'inline', False) is True:
            filestore = inlinefiles
        else:
            filestore = files
        if hasattr(f, 'inline'):
            del f.inline
        if getattr(f, 'b64', None):
            filestore[fullprefix] = jsonutil.CouchishFile(f.file, f.filename, f.mimetype, f.id, metadata=f.metadata, b64=True)
            del f.b64
        else:
            fh = StringIO()
            shutil.copyfileobj(f.file, fh)
            fh.seek(0)
            filestore[fullprefix] = jsonutil.CouchishFile(fh, f.filename, f.mimetype, f.id, metadata=f.metadata)
        del f.file
    return


def get_file_from_original(f, of, files, inlinefiles, original_files, fullprefix):
    if not isinstance(f, File):
        original_files[fullprefix] = of


def get_files_from_original(data, original, files, inlinefiles, original_files, prefix):
    if isinstance(original, File):
        get_file_from_original(data, original, files, inlinefiles, original_files, get_attr(prefix))
        return
    if not isinstance(original, dict) and not isinstance(original, list):
        return
    dd = dotted_or_emptydict(data)
    ddoriginal = dotted_or_emptydict(original)
    if not ddoriginal:
        return
    for (k, of) in flatten(ddoriginal):
        if isinstance(of, File):
            f = dd.get(k)
            get_file_from_original(f, of, files, inlinefiles, original_files, get_attr(prefix, k))


def _parse_changes_for_files(session, deletions, additions, changes):
    """ returns deletions, additions """
    all_separate_files = {}
    all_inline_files = {}
    for addition in additions:
        (addition, files, inlinefiles, original_files_notused) = get_files(addition)
        if files:
            all_separate_files.setdefault(addition['_id'], {}).update(files)
        if inlinefiles:
            all_inline_files.setdefault(addition['_id'], {}).update(inlinefiles)
        _extract_inline_attachments(addition, inlinefiles)

    all_original_files = {}
    changes = list(changes)
    for (n, changeset) in enumerate(changes):
        (d, cs) = changeset
        cs = list(cs)
        for (m, c) in enumerate(cs):
            if c['action'] in ('edit', 'create', 'remove'):
                (c['value'], files, inlinefiles, original_files) = get_files(c.get('value'), original=c.get('was'), prefix=c['path'])
                cs[m] = c
                if files:
                    all_separate_files.setdefault(d['_id'], {}).update(files)
                if inlinefiles:
                    all_inline_files.setdefault(d['_id'], {}).update(inlinefiles)
                all_original_files.setdefault(d['_id'], {}).update(original_files)
                _extract_inline_attachments(d, inlinefiles)

        changes[n] = (
         d, cs)

    return (
     all_original_files, all_separate_files)


def _extract_inline_attachments(doc, files):
    """
    Move the any attachment data that we've found into the _attachments attribute
    """
    for (attr, f) in files.items():
        if f.b64:
            data = f.file.replace('\n', '')
        else:
            data = base64.encodestring(f.file.read()).replace('\n', '')
            f.file.close()
        del f.file
        del f.b64
        del f.inline
        del f.doc_id
        doc.setdefault('_attachments', {})[f.id] = {'content_type': f.mimetype, 'data': data}


def _handle_separate_attachments(session, deletions, additions):
    """
    add attachments that aren't inline and remove any attachments without references
    """
    for (id, attrfiles) in additions.items():
        doc = session.get(id)
        stubdoc = {'_id': doc['_id'], '_rev': doc['_rev']}
        for (attr, f) in attrfiles.items():
            data = ''
            if f.file:
                if f.b64:
                    data = base64.decodestring(f.file)
                else:
                    data = f.file.read()
                    f.file.close()
            session._db.put_attachment(stubdoc, data, filename=f.id, content_type=f.mimetype)
            del f.file
            del f.b64
            del f.inline
            del f.doc_id

    for (id, attrfiles) in deletions.items():
        doc = session._db.get(id)
        for (attr, f) in attrfiles.items():
            session._db.delete_attachment(doc, f.id)

    additions = {}
    deletions = {}