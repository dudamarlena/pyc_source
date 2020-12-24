# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/djblets/util/json_utils.py
# Compiled at: 2019-06-12 01:17:17
from __future__ import unicode_literals
from copy import deepcopy
from django.utils import six
from django.utils.translation import ugettext as _

class JSONPatchError(Exception):
    """An error occurred while patching an object.

    Attributes:
        doc (dict or list):
            The original JSON document the patch was being applied to. This
            won't contain the patched modifications.

        patch (object):
            The patch being applied. The value depends on the type of patch.

        patch_entry_index (int, optional):
            The index of the patch being applied. This can be ``None``
            if the error doesn't apply to a specific entry.
    """

    def __init__(self, msg, doc, patch, patch_entry_index=None):
        """Initialize the error.

        Args:
            msg (unicode):
                The error message.

            doc (dict or list):
                The original JSON document the patch was being applied to. This
                won't contain the patched modifications.
                patch.

            patch (object):
                The patch being applied. The value depends on the patch.

            patch_entry_index (int, optional):
                The index of the patch being applied. This can be ``None``
                if the error doesn't apply to a specific entry.
        """
        super(JSONPatchError, self).__init__(msg)
        self.doc = doc
        self.patch = patch
        self.patch_entry_index = patch_entry_index


class JSONPatchPathError(JSONPatchError):
    """Error with a path in a JSON Patch."""

    def __init__(self, msg, path, **kwargs):
        """Initialize the error.

        Args:
            msg (unicode):
                The error message describing the path failure.

            path (unicode):
                The path that had an error.

            **kwargs (dict):
                Additional keyword arguments to pass to the parent
                class.
        """
        super(JSONPatchPathError, self).__init__(msg, **kwargs)
        self.path = path


class JSONPatchAccessError(JSONPatchPathError):
    """Access error reading from or writing to part of an object."""
    pass


class JSONPatchReadAccessError(JSONPatchAccessError):
    """Access error reading from part of an object."""
    pass


class JSONPatchWriteAccessError(JSONPatchAccessError):
    """Access error writing to part of an object."""
    pass


class JSONPatchTestError(JSONPatchPathError):
    """Test condition failed when applying a JSON Patch."""
    pass


class JSONPointerError(Exception):
    """Base class for JSON Pointer errors."""
    pass


class JSONPointerSyntaxError(JSONPointerError):
    """Syntax error in a JSON Pointer path."""
    pass


class JSONPointerLookupError(JSONPointerError):
    """Error looking up data from a JSON Pointer path."""

    def __init__(self, msg, parent, token, token_index, tokens):
        """Initialize the error.

        Args:
            msg (unicode):
                The error message.

            parent (object):
                The parent object. This may be a dictionary or a list.

            token (unicode):
                The last resolvable token in the path. This will be ``None``
                if the first token failed.

            token_index (int):
                The 0-based index of the last resolvable token in the path.
                This will be ``None`` if the first token failed.

            tokens (list of unicode):
                The list of tokens comprising the full path.
        """
        super(JSONPointerLookupError, self).__init__(msg)
        self.parent = parent
        self.token = token
        self.token_index = token_index
        self.tokens = tokens


class JSONPointerEndOfList(object):
    """A representation of the end of a list.

    This is used by the JSON Pointer functions to represent the very end of
    a list (not the last item). This is used primarily when specifying an
    insertion point, with this value repersenting appending to a list.
    """

    def __init__(self, json_list):
        """Initialize the object.

        Args:
            json_list (list):
                The list this object represents.
        """
        self.json_list = json_list

    def __eq__(self, other_list):
        """Return whether two instances are equal.

        Instances are equal if both of their lists are equal.

        Args:
            other_list (JSONPointerEndOfList):
                The other instance to compare to for equality.

        Returns:
            bool:
            ``True`` if the two lists are equal.
        """
        try:
            return self.json_list == other_list.json_list
        except AttributeError:
            return False

    def __repr__(self):
        """Return a string representation of the instance.

        Returns:
            unicode:
            A string representation of the instance.
        """
        return b'JSONPointerEndOfList<%r>' % self.json_list


def json_merge_patch(doc, patch, can_write_key_func=None):
    """Apply a JSON Merge Patch to a value.

    This is an implementation of the proposed JSON Merge Patch standard
    (:rfc:`7396`), which is a simple algorithm for applying changes to a
    JSON-compatible data structure.

    This will attempt to merge the contents of the ``patch`` object into the
    ``doc`` object as best as possible, using the following rules:

    * If a key in ``patch`` matches a key in ``doc``, and the value is
      ``None``, the key in ``doc`` is removed.

    * If a key in ``patch`` matches a key in ``doc``, and the value is a
      dictionary, this method will be called on the values in each and the
      result will be stored as the new value.

    * If a key in ``patch`` matches a key in ``doc``, and the value is not a
      dictionary, the value from ``patch`` will replace the value in
      ``doc``.

    * If ``patch`` is a dictionary but ``doc`` is not, then ``patch`` will
      be returned directly.

    * If ``patch`` is a dictionary but ``doc`` is not, then ``doc`` will
      be discarded and the JSON Merge Patch will be applied to a new empty
      dictionary.

    * If ``patch`` is not a dictionary, then ``patch`` will be returned
      directly.

    Args:
        doc (object):
            The JSON-compatible document object the patch is being applied to.
            This will usually be a :js:class:`dict`.

        patch (object):
            The JSON-compatible patch to apply.

        can_write_key_func (callable, optional):
            An optional function to call for each key to determine if the
            key can be written in the new dictionary. This must take the
            following form:

            .. code-block:: python

               def can_write_key(doc, patch, path, **kwargs):
                   ...

            This must return a boolean indicating if the key can be written, or
            may raise a :py:class:`JSONPatchError` to abort the patching
            process. If the function returns ``False``, the key will simply be
            skipped.

    Returns:
        object:
        The resulting object. This will be the same type as ``patch``.

    Raises:
        JSONPatchError:
            There was an error patching the document. This is only raised by
            ``can_write_key_func`` implementations.

        ValueError:
            A provided parameter was incorrect.
    """

    def _merge_patch(cur_doc, cur_patch, parent_path=()):
        if isinstance(cur_patch, dict):
            if isinstance(cur_doc, dict):
                new_doc = cur_doc.copy()
            else:
                new_doc = {}
            for key, value in six.iteritems(cur_patch):
                path = parent_path + (key,)
                if can_write_key_func and not can_write_key_func(doc=doc, patch=patch, path=path):
                    continue
                if value is None:
                    new_doc.pop(key, None)
                else:
                    new_doc[key] = _merge_patch(new_doc.get(key), value, path)

            return new_doc
        return cur_patch
        return

    if can_write_key_func and not callable(can_write_key_func):
        raise ValueError(b'can_write_key_func must be callable')
    return _merge_patch(doc, patch)


def _json_patch_add(obj, key, value, doc, patch, patch_entry_index, path):
    """Add a value to a JSON object from a patch.

    This will add a value to a dictionary or list based on the rules of a
    JSON Patch operation.

    If working on a list, ``-`` is considered a valid key, which will result
    in the object being appended to the list.

    Args:
        obj (dict or list):
            The object that the value is being added to.

        key (unicode):
            The key (for dictionaries) or index (for lists) for the value.
            This also allows for a special ``-`` for lists, indicating that
            the value should be appended to the list.

        value (object):
            The value to add to the object.

        doc (dict or list):
            The root JSON document being patched.

        patch (dict or list):
            The main patch being applied.

        patch_entry_index (int):
            The patch entry index for this operation.

        path (unicode):
            The path being updated.

    Raises:
        JSONPatchError:
            There was an error adding the value to the object. Details are
            in the message.
    """
    if isinstance(obj, list):
        if key == b'-':
            obj.append(value)
        else:
            key = int(key)
            if key > len(obj):
                raise JSONPatchPathError(_(b'Cannot insert into index %(index)d in path "%(path)s" for patch entry %(entry)d') % {b'index': key, 
                   b'path': path, 
                   b'entry': patch_entry_index}, doc=doc, patch=patch, patch_entry_index=patch_entry_index, path=path)
            obj.insert(key, value)
    elif isinstance(obj, dict):
        obj[key] = value
    else:
        raise JSONPatchPathError(_(b'Unable to add key "%(key)s" to a non-dictionary/list in path "%(path)s" for patch entry %(entry)d') % {b'key': key, 
           b'path': path, 
           b'entry': patch_entry_index}, doc=doc, patch=patch, patch_entry_index=patch_entry_index, path=path)


def _json_patch_remove(obj, key, doc, patch, patch_entry_index, path):
    """Remove a value from a JSON object from a patch.

    This will remove the value from a dictionary or list based on the rules of
    a JSON Patch operation.

    Args:
        obj (dict or list):
            The object that the value is being added to.

        key (unicode):
            The key (either a dictionary key or a list index) to remove.

        doc (dict or list):
            The root JSON document being patched.

        patch (dict or list):
            The main patch being applied.

        patch_entry_index (int):
            The patch entry index for this operation.

        path (unicode):
            The path being updated.

    Raises:
        JSONPatchError:
            There was an error adding the value to the object. Details are
            in the message.
    """
    if isinstance(obj, list):
        key = int(key)
    try:
        del obj[key]
    except KeyError:
        raise JSONPatchPathError(_(b'Cannot remove non-existent key "%(key)s" in path "%(path)s" for patch entry %(entry)d') % {b'key': key, 
           b'path': path, 
           b'entry': patch_entry_index}, doc=doc, patch=patch, patch_entry_index=patch_entry_index, path=path)


def json_patch(doc, patch, can_read_key_func=None, can_write_key_func=None):
    """Apply a JSON Patch to a value.

    A JSON Patch (:rfc:`6902`), similar to a JSON Merge Patch, is used to make
    changes to an existing JSON-compatible data structure. JSON Patches are
    composed of a list of operations which can add a new value, remove a value,
    replace an existing value, move a value, copy a value, or test that a path
    has a given value. All operations must pass for a patch to apply.

    A full description of the operations are available in the RFC or from
    http://jsonpatch.com/.

    Args:
        doc (dict or list):
            The root JSON document to apply the patch to. This will not be
            modified itself.

        patch (list of dict):
            The list of operations to apply to the JSON document.

        can_read_key_func (callable, optional):
            An optional function to call for each path to determine if the
            path can be read from the document. This is in the following form:

            .. code-block:: python

               def can_read_key(doc, patch, patch_entry, path, **kwargs):
                   ...

            It must return a boolean indicating if the key can be written.

        can_write_key_func (callable, optional):
            An optional function to call for each path to determine if the
            path can be written to the document. This takes the same form as
            ``can_read_key_func``.

            If not provided, it will default to ``can_read_key_func``.

    Returns:
        dict or list:
        The resulting JSON document after the patch is applied.

    Raises:
        JSONPatchError:
            An error occurred patching the JSON document.
    """
    if not isinstance(patch, list):
        raise JSONPatchError(b'The patch must be a list of operations to perform', doc=doc, patch=patch)
    new_doc = deepcopy(doc)
    if can_read_key_func and not callable(can_read_key_func):
        raise ValueError(b'can_read_key_func must be callable')
    if not can_write_key_func:
        can_write_key_func = can_read_key_func
    else:
        if not callable(can_write_key_func):
            raise ValueError(b'can_write_key_func must be callable')
        for i, patch_entry in enumerate(patch):
            if not isinstance(patch_entry, dict):
                raise JSONPatchError(_(b'Patch entry %(entry)d must be a dictionary instead of %(type)s') % {b'type': type(patch_entry).__name__, 
                   b'entry': i}, doc=doc, patch=patch, patch_entry_index=i)
            value = None
            from_path = None
            from_path_info = None
            from_all_tokens = None
            try:
                op = patch_entry[b'op']
                path = patch_entry[b'path']
                if op in ('add', 'replace', 'test'):
                    value = patch_entry[b'value']
                elif op in ('copy', 'move'):
                    from_path = patch_entry[b'from']
            except KeyError as e:
                raise JSONPatchError(_(b'Missing key "%(key)s" for patch entry %(entry)d') % {b'key': e.args[0], 
                   b'entry': i}, doc=doc, patch=patch, patch_entry_index=i)

            try:
                path_info = json_get_pointer_info(new_doc, path)
            except JSONPointerSyntaxError as e:
                raise JSONPatchPathError(_(b'Syntax error in path "%(path)s" for patch entry %(entry)d: %(error)s') % {b'path': path, 
                   b'entry': i, 
                   b'error': e}, doc=doc, patch=patch, patch_entry_index=i, path=path)

            all_tokens = tuple(path_info[b'all_tokens'])
            lookup_error = path_info[b'lookup_error']
            if lookup_error:
                if op in ('remove', 'test') or len(path_info[b'unresolved_tokens']) > 1:
                    raise JSONPatchPathError(_(b'Invalid path "%(path)s" for patch entry %(entry)d: %(error)s') % {b'path': path, 
                       b'entry': i, 
                       b'error': lookup_error}, doc=doc, patch=patch, patch_entry_index=i, path=path)
            elif isinstance(path_info[b'value'], JSONPointerEndOfList) and op not in ('add',
                                                                                      'copy',
                                                                                      'move'):
                raise JSONPatchPathError(_(b'Cannot perform operation "%(op)s" on end of list at "%(path)s" for patch entry %(entry)d') % {b'op': op, 
                   b'path': path, 
                   b'entry': i}, doc=doc, patch=patch, patch_entry_index=i, path=path)
            if op == b'test':
                if can_read_key_func and not can_read_key_func(doc=new_doc, patch_entry=patch_entry, path=all_tokens):
                    raise JSONPatchReadAccessError(_(b'Cannot read from path "%(path)s" for patch entry %(entry)d') % {b'path': path, 
                       b'entry': i}, doc=doc, patch=patch, patch_entry_index=i, path=path)
            else:
                if can_write_key_func and not can_write_key_func(doc=new_doc, patch_entry=patch_entry, path=all_tokens):
                    raise JSONPatchWriteAccessError(_(b'Cannot write to path "%(path)s" for patch entry %(entry)d') % {b'path': path, 
                       b'entry': i}, doc=doc, patch=patch, patch_entry_index=i, path=path)
                if op in ('copy', 'move'):
                    if from_path == path:
                        continue
                    try:
                        from_path_info = json_get_pointer_info(new_doc, from_path)
                    except JSONPointerSyntaxError as e:
                        raise JSONPatchPathError(_(b'Syntax error in from path "%(path)s" for patch entry %(entry)d: %(error)s') % {b'path': from_path, 
                           b'entry': i, 
                           b'error': e}, doc=doc, patch=patch, patch_entry_index=i, path=from_path)

                    lookup_error = from_path_info[b'lookup_error']
                    if lookup_error:
                        raise JSONPatchPathError(_(b'Invalid from path "%(path)s" for patch entry %(entry)d: %(error)s') % {b'path': from_path, 
                           b'entry': i, 
                           b'error': lookup_error}, doc=doc, patch=patch, patch_entry_index=i, path=from_path)
                    if isinstance(from_path_info[b'value'], JSONPointerEndOfList):
                        raise JSONPatchPathError(_(b'Cannot perform operation "%(op)s" from end of list at "%(path)s" for patch entry %(entry)d') % {b'op': op, 
                           b'path': from_path, 
                           b'entry': i}, doc=doc, patch=patch, patch_entry_index=i, path=from_path)
                    from_all_tokens = tuple(from_path_info[b'all_tokens'])
                    if op == b'move':
                        if can_write_key_func and not can_write_key_func(doc=new_doc, patch_entry=patch_entry, path=from_all_tokens):
                            raise JSONPatchWriteAccessError(_(b'Cannot write to path "%(path)s" for patch entry %(entry)d') % {b'path': from_path, 
                               b'entry': i}, doc=doc, patch=patch, patch_entry_index=i, path=from_path)
                    elif can_read_key_func and not can_read_key_func(doc=new_doc, patch_entry=patch_entry, path=from_all_tokens):
                        raise JSONPatchReadAccessError(_(b'Cannot read from path "%(path)s" for patch entry %(entry)d') % {b'path': from_path, 
                           b'entry': i}, doc=doc, patch=patch, patch_entry_index=i, path=from_path)
                parent = path_info[b'parent']
                try:
                    last_token = all_tokens[(-1)]
                except IndexError:
                    last_token = None

            if op == b'add':
                _json_patch_add(obj=parent, key=last_token, value=value, doc=doc, patch=patch, patch_entry_index=i, path=path)
            elif op == b'remove':
                _json_patch_remove(obj=parent, key=last_token, doc=doc, patch=patch, patch_entry_index=i, path=path)
            elif op == b'replace':
                if parent is None:
                    new_doc = value
                else:
                    _json_patch_remove(obj=parent, key=last_token, doc=doc, patch=patch, patch_entry_index=i, path=path)
                    _json_patch_add(obj=parent, key=last_token, value=value, doc=doc, patch=patch, patch_entry_index=i, path=path)
            elif op == b'copy':
                _json_patch_add(obj=parent, key=last_token, value=deepcopy(from_path_info[b'value']), doc=doc, patch=patch, patch_entry_index=i, path=path)
            elif op == b'move':
                num_from_tokens = len(from_all_tokens)
                if len(all_tokens) > num_from_tokens and all_tokens[:num_from_tokens] == from_all_tokens:
                    raise JSONPatchPathError(_(b'Cannot move values into their own children at patch entry %(entry_id)d') % {b'entry_id': i}, doc=doc, patch=patch, patch_entry_index=i, path=from_path)
                _json_patch_remove(obj=from_path_info[b'parent'], key=from_all_tokens[(-1)], doc=doc, patch=patch, patch_entry_index=i, path=from_path)
                _json_patch_add(obj=parent, key=last_token, value=from_path_info[b'value'], doc=doc, patch=patch, patch_entry_index=i, path=path)
            elif op == b'test':
                if path_info[b'value'] != value:
                    raise JSONPatchTestError(_(b'Test failed for path "%(path)s" at patch entry %(entry_id)d. Expected %(expected_value)r and got %(found_value)r.') % {b'path': path, 
                       b'entry_id': i, 
                       b'expected_value': value, 
                       b'found_value': path_info[b'value']}, doc=doc, patch=patch, patch_entry_index=i, path=path)

    return new_doc


def json_get_pointer_info(obj, path):
    """Return information from a JSON object based on a JSON Pointer path.

    JSON Pointers are a standard way of specifying a path to data within a
    JSON object. This method takes a JSON Pointer path and returns information
    from the given object based on that path.

    Pointer paths consist of dictionary keys, array indexes, or a special ``-``
    token (representing the end of a list, after the last item) separated by
    ``/`` tokens. There are also two special escaped values: ``~0``,
    representing a ``~`` character, and ``~1``, representing a ``/`` character.

    Paths must start with ``/``, or must be an empty string (which will match
    the provided object). If the path has a trailing ``/``, then the final
    token is actually an empty string (matching an empty key in a dictionary).

    If the Pointer does not resolve to a complete path (for instance, a key
    specified in the path is missing), the resulting information will return
    the keys that could be resolved, keys that could not be resolved, the
    object where it left off, and an error message. This allows implementations
    to determine which part of a path does not yet exist, potentially for the
    purpose of inserting data at that key in the path.

    Args:
        obj (object or list):
            The object or list representing the starting object for the path.

        path (unicode):
            The Pointer path for the lookup.

    Returns:
        dict:
        Information about the object and what the path was able to match. This
        has the following keys:

        ``value`` (:py:class:`object`):
            The resulting value from the path, if the path was fully resolved.

            This will be a :py:class:`JSONPointerEndOfList` if the last part of
            the path was a ``-`` token (representing the very end of
            a list).

        ``tokens`` (:py:class:`list`):
            The normalized (unescaped) list of path tokens that comprise the
            full path.

        ``parent`` (:py:class:`object`):
            The parent object for either the most-recently resolved value.

        ``resolved`` (:py:class:`list`):
            The list of resolved objects from the original JSON object. This
            will contain each key, array item, or other value that was found,
            in path order.

        ``lookup_error`` (:py:class:`unicode`):
            The error message, if any, if failing to resolve the full path.

    Raises:
        JSONPointerSyntaxError:
            There was a syntax error with a token in the path.
    """
    if path != b'' and not path.startswith(b'/'):
        raise JSONPointerSyntaxError(_(b'Paths must either be empty or start with a "/"'))
    tokens = path.split(b'/')[1:]
    norm_tokens = [ token.replace(b'~1', b'/').replace(b'~0', b'~') for token in tokens
                  ]
    resolved = [
     obj]
    lookup_error = None
    parent = None
    for i, token in enumerate(norm_tokens):
        parent = obj
        if isinstance(obj, dict):
            try:
                obj = obj[token]
            except KeyError:
                lookup_error = _(b'Dictionary key "%(key)s" not found in "%(path)s"') % {b'key': token, 
                   b'path': b'/%s' % (b'/').join(tokens[:i])}

        elif isinstance(obj, list):
            if token == b'-':
                obj = JSONPointerEndOfList(obj)
            else:
                if token != b'0' and token.startswith(b'0'):
                    raise JSONPointerSyntaxError(_(b'List index "%s" must not begin with "0"') % token)
                try:
                    token = int(token)
                except ValueError:
                    raise JSONPointerSyntaxError(_(b'%(index)r is not a valid list index in "%(path)s"') % {b'index': token, 
                       b'path': b'/%s' % (b'/').join(tokens[:i])})

                if token < 0:
                    raise JSONPointerSyntaxError(_(b'Negative indexes into lists are not allowed'))
                try:
                    obj = obj[token]
                except IndexError:
                    lookup_error = _(b'%(index)d is outside the list in "%(path)s"') % {b'index': token, 
                       b'path': b'/%s' % (b'/').join(tokens[:i])}

        else:
            lookup_error = _(b'Cannot resolve path within unsupported type "%(type)s" at "%(path)s"') % {b'type': type(obj).__name__, 
               b'path': b'/%s' % (b'/').join(tokens[:i])}
        if lookup_error:
            obj = None
            break
        resolved.append(obj)

    return {b'value': obj, 
       b'parent': parent, 
       b'all_tokens': norm_tokens, 
       b'resolved_values': resolved, 
       b'resolved_tokens': norm_tokens[:len(resolved) - 1], 
       b'unresolved_tokens': norm_tokens[len(resolved) - 1:], 
       b'lookup_error': lookup_error}


def json_resolve_pointer(obj, path):
    """Return the value from a JSON object based on a JSON Pointer path.

    See :py:func:`json_get_pointer_info` for information on how a Pointer
    path is constructed. Unlike that function, this requires a fully-resolved
    path.

    Args:
        obj (object or list):
            The object or list representing the starting object for the path.

        path (unicode):
            The Pointer path for the lookup.

    Returns:
        object:
        The resulting value from the object, based on the path.

        This will be a :py:class:`JSONPointerEndOfList` if the last part of
        the path was a ``-`` token (representing the very end of
        a list).

    Raises:
        JSONPointerLookupError:
            The path could not be fully resolved.

        JSONPointerSyntaxError:
            There was a syntax error with a token in the path.
    """
    info = json_get_pointer_info(obj, path)
    lookup_error = info[b'lookup_error']
    if lookup_error:
        tokens = info[b'all_tokens']
        parent = info[b'parent']
        if parent is None:
            token_index = None
            token = None
        else:
            token_index = len(info[b'resolved_tokens']) - 1
            token = tokens[token_index]
        raise JSONPointerLookupError(lookup_error, parent=parent, token=token, token_index=token_index, tokens=tokens)
    return info[b'value']