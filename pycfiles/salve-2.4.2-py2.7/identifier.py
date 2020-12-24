# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-armv7l/egg/salve/block/identifier.py
# Compiled at: 2015-11-06 23:45:35
import salve
from salve.exceptions import BlockException
from salve.block.file import FileBlock
from salve.block.directory import DirBlock
from salve.block.manifest import ManifestBlock
identifier_map = {'file': FileBlock, 
   'manifest': ManifestBlock, 
   'directory': DirBlock}

def block_from_identifier(id_token):
    """
    Given an identifier, constructs a block of the appropriate
    type and returns it.
    Fails if the identifier is unknown, or the token given is
    not an identifier.

    Args:
        @id_token
        The Token which is a block identifier. Consists of a string and
        little else.
    """
    from salve.parser import Token
    assert isinstance(id_token, Token)
    ctx = id_token.file_context
    if id_token.ty != Token.types.IDENTIFIER:
        raise BlockException('Cannot create block from non-identifier: ' + str(id_token), ctx)
    salve.logger.info(('{0}: Generating Block From Identifier Token: {1}').format(str(ctx), str(id_token)))
    val = id_token.value.lower()
    try:
        return identifier_map[val](ctx)
    except KeyError:
        raise BlockException('Unknown block identifier ' + val, ctx)