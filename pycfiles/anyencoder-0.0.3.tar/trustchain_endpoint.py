# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/martijndevos/Documents/anydex-core/pyipv8/ipv8/REST/trustchain_endpoint.py
# Compiled at: 2019-05-22 05:00:30
from __future__ import absolute_import
from binascii import unhexlify
from twisted.web import http
from .base_endpoint import BaseEndpoint
from ..attestation.trustchain.community import TrustChainCommunity

class TrustchainEndpoint(BaseEndpoint):
    """
    This endpoint is responsible for handing all requests regarding TrustChain.
    """

    def __init__(self, session):
        super(TrustchainEndpoint, self).__init__()
        trustchain_overlays = [ overlay for overlay in session.overlays if isinstance(overlay, TrustChainCommunity) ]
        if trustchain_overlays:
            self.putChild('recent', TrustchainRecentEndpoint(trustchain_overlays[0]))
            self.putChild('blocks', TrustchainBlocksEndpoint(trustchain_overlays[0]))
            self.putChild('users', TrustchainUsersEndpoint(trustchain_overlays[0]))


class TrustchainRecentEndpoint(BaseEndpoint):

    def __init__(self, trustchain):
        super(TrustchainRecentEndpoint, self).__init__()
        self.trustchain = trustchain

    def render_GET(self, request):
        limit = 10
        offset = 0
        if request.args and 'limit' in request.args:
            limit = int(request.args['limit'][0])
        if request.args and 'offset' in request.args:
            offset = int(request.args['offset'][0])
        return self.twisted_dumps({'blocks': [ dict(block) for block in self.trustchain.persistence.get_recent_blocks(limit=limit, offset=offset)
                   ]})


class TrustchainBlocksEndpoint(BaseEndpoint):

    def __init__(self, trustchain):
        super(TrustchainBlocksEndpoint, self).__init__()
        self.trustchain = trustchain

    def getChild(self, path, request):
        return TrustchainSpecificBlockEndpoint(self.trustchain, path)


class TrustchainSpecificBlockEndpoint(BaseEndpoint):

    def __init__(self, trustchain, block_hash):
        super(TrustchainSpecificBlockEndpoint, self).__init__()
        self.trustchain = trustchain
        try:
            self.block_hash = unhexlify(block_hash)
        except TypeError:
            self.block_hash = None

        return

    def render_GET(self, request):
        if not self.block_hash:
            request.setResponseCode(http.NOT_FOUND)
            return self.twisted_dumps({'error': 'the block with the provided hash could not be found'})
        block = self.trustchain.persistence.get_block_with_hash(self.block_hash)
        if not block:
            request.setResponseCode(http.NOT_FOUND)
            return self.twisted_dumps({'error': 'the block with the provided hash could not be found'})
        block_dict = dict(block)
        linked_block = self.trustchain.persistence.get_linked(block)
        if linked_block:
            block_dict['linked'] = dict(linked_block)
        return self.twisted_dumps({'block': block_dict})


class TrustchainUsersEndpoint(BaseEndpoint):

    def __init__(self, trustchain):
        super(TrustchainUsersEndpoint, self).__init__()
        self.trustchain = trustchain

    def getChild(self, path, request):
        return TrustchainSpecificUserEndpoint(self.trustchain, path)

    def render_GET(self, request):
        limit = 100
        if 'limit' in request.args:
            limit = int(request.args['limit'][0])
        users_info = self.trustchain.persistence.get_users(limit=limit)
        return self.twisted_dumps({'users': users_info})


class TrustchainSpecificUserEndpoint(BaseEndpoint):

    def __init__(self, trustchain, pub_key):
        super(TrustchainSpecificUserEndpoint, self).__init__()
        self.trustchain = trustchain
        self.pub_key = pub_key
        self.putChild('blocks', TrustchainSpecificUserBlocksEndpoint(self.trustchain, self.pub_key))


class TrustchainSpecificUserBlocksEndpoint(BaseEndpoint):

    def __init__(self, trustchain, pub_key):
        super(TrustchainSpecificUserBlocksEndpoint, self).__init__()
        self.trustchain = trustchain
        try:
            self.pub_key = unhexlify(pub_key)
        except TypeError:
            self.pub_key = None

        return

    def render_GET(self, request):
        if not self.pub_key:
            request.setResponseCode(http.NOT_FOUND)
            return self.twisted_dumps({'error': 'the user with the provided public key could not be found'})
        limit = 100
        if 'limit' in request.args:
            limit = int(request.args['limit'][0])
        latest_blocks = self.trustchain.persistence.get_latest_blocks(self.pub_key, limit=limit)
        blocks_list = []
        for block in latest_blocks:
            block_dict = dict(block)
            linked_block = self.trustchain.persistence.get_linked(block)
            if linked_block:
                block_dict['linked'] = dict(linked_block)
            blocks_list.append(block_dict)

        return self.twisted_dumps({'blocks': blocks_list})