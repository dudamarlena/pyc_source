# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/martijndevos/Documents/anydex-core/anydex/../pyipv8/ipv8/REST/attestation_endpoint.py
# Compiled at: 2019-06-07 08:10:38
from __future__ import absolute_import
from base64 import b64decode, b64encode
from hashlib import sha1
from six.moves import xrange
from twisted.internet.defer import Deferred, succeed
from twisted.web import http
from . import json_util as json
from .base_endpoint import BaseEndpoint
from ..attestation.identity.community import IdentityCommunity
from ..attestation.wallet.community import AttestationCommunity
from ..database import database_blob
from ..keyvault.crypto import default_eccrypto
from ..peer import Peer
from ..util import cast_to_bin, cast_to_unicode

class AttestationEndpoint(BaseEndpoint):
    """
    This endpoint is responsible for handing all requests regarding attestation.
    """

    def __init__(self, session):
        super(AttestationEndpoint, self).__init__()
        self.session = session
        attestation_overlays = [ overlay for overlay in session.overlays if isinstance(overlay, AttestationCommunity) ]
        identity_overlays = [ overlay for overlay in session.overlays if isinstance(overlay, IdentityCommunity) ]
        self.persistent_key = None
        if attestation_overlays and identity_overlays:
            self.attestation_overlay = attestation_overlays[0]
            self.attestation_overlay.set_attestation_request_callback(self.on_request_attestation)
            self.attestation_overlay.set_attestation_request_complete_callback(self.on_attestation_complete)
            self.attestation_overlay.set_verify_request_callback(self.on_verify_request)
            self.identity_overlay = identity_overlays[0]
            self.persistent_key = self.identity_overlay.my_peer
        self.attestation_requests = {}
        self.verify_requests = {}
        self.verification_output = {}
        self.attestation_metadata = {}
        return

    def on_request_attestation(self, peer, attribute_name, metadata):
        """
        Return the measurement of an attribute for a certain peer.
        """
        deferred = Deferred()
        self.attestation_requests[(b64encode(peer.mid), cast_to_bin(attribute_name))] = (
         deferred, b64encode(json.dumps(metadata).encode('utf-8')))
        self.attestation_metadata[(peer, attribute_name)] = metadata
        return deferred

    def on_attestation_complete(self, for_peer, attribute_name, attribute_hash, id_format, from_peer=None):
        """
        Callback for when an attestation has been completed for another peer.
        We can now sign for it.
        """
        metadata = self.attestation_metadata.get((for_peer, attribute_name), None)
        if for_peer.mid == self.identity_overlay.my_peer.mid:
            self.identity_overlay.request_attestation_advertisement(from_peer, attribute_hash, attribute_name, id_format, metadata)
        else:
            self.identity_overlay.add_known_hash(attribute_hash, attribute_name, for_peer.public_key.key_to_bin(), metadata)
        return

    def on_verify_request(self, peer, attribute_hash):
        """
        Return the measurement of an attribute for a certain peer.
        """
        block = self.identity_overlay.get_attestation_by_hash(attribute_hash)
        if not block:
            return succeed(None)
        else:
            attribute_name = block.transaction['name']
            deferred = Deferred()
            self.verify_requests[(b64encode(peer.mid), attribute_name)] = deferred
            return deferred

    def on_verification_results(self, attribute_hash, values):
        """
        Callback for when verification has concluded.
        """
        references = self.verification_output[attribute_hash]
        out = []
        for i in range(len(references)):
            out.append((references[i][0] if isinstance(references[i], tuple) else references[i], values[i]))

        self.verification_output[attribute_hash] = out

    def get_peer_from_mid(self, mid_b64):
        """
        Find a peer by base64 encoded mid.
        """
        mid = b64decode(mid_b64)
        peers = self.session.network.verified_peers[:]
        matches = [ p for p in peers if p.mid == mid ]
        if matches:
            return matches[0]
        else:
            return

    def _drop_identity_table_data(self, keys_to_keep):
        """
        Remove all metadata (TrustChain blocks) from the identity community.

        :param keys_to_keep: list of keys to not remove for
        :type keys_to_keep: [str]
        :return: the list of attestation hashes which have been removed
        :rtype: [database_blob]
        """
        if not keys_to_keep:
            block_selection_stmt = ''
            params = ()
        else:
            value_insert = ('AND').join('public_key != ? AND link_public_key != ?' for _ in xrange(len(keys_to_keep)))
            block_selection_stmt = ' WHERE ' + value_insert + ' ORDER BY block_timestamp'
            params = ()
            for key in keys_to_keep:
                params += (database_blob(key), database_blob(key))

        blocks_to_remove = self.identity_overlay.persistence._getall(block_selection_stmt, params)
        attestation_hashes = [ database_blob(b.transaction['hash']) for b in blocks_to_remove ]
        self.identity_overlay.persistence.execute('DELETE FROM blocks' + ' WHERE block_hash IN (SELECT block_hash FROM blocks ' + block_selection_stmt + ')', params)
        self.identity_overlay.persistence.commit()
        return attestation_hashes

    def _drop_attestation_table_data(self, attestation_hashes):
        """
        Remove all attestation data (claim based keys and ZKP blobs) by list of attestation hashes.

        :param attestation_hashes: hashes to remove
        :type attestation_hashes: [database_blob]
        :returns: None
        """
        if not attestation_hashes:
            return
        self.attestation_overlay.database.execute('DELETE FROM %s' % self.attestation_overlay.database.db_name + ' WHERE hash IN (' + (', ').join(c for c in '?' * len(attestation_hashes)) + ')', attestation_hashes)
        self.attestation_overlay.database.commit()

    def render_GET(self, request):
        """
        type=drop_identity
        type=outstanding -> [(mid_b64, attribute_name)]
        type=outstanding_verify -> [(mid_b64, attribute_name)]
        type=verification_output -> {hash_b64: [(value_b64, match)]}
        type=peers -> [mid_b64]
        type=attributes&mid=mid_b64 -> [(attribute_name, attribute_hash)]
        """
        if not request.args or 'type' not in request.args:
            request.setResponseCode(http.BAD_REQUEST)
            return self.twisted_dumps({'error': 'parameters or type missing'})
        else:
            if request.args['type'][0] == 'outstanding':
                formatted = []
                for k, v in self.attestation_requests.items():
                    formatted.append(k + (v[1],))

                return self.twisted_dumps([ (x.decode('utf-8'), y.decode('utf-8'), z.decode('utf-8')) for x, y, z in formatted ])
            if request.args['type'][0] == 'outstanding_verify':
                formatted = self.verify_requests.keys()
                return self.twisted_dumps([ (x.decode('utf-8'), y.decode('utf-8')) for x, y in formatted ])
            if request.args['type'][0] == 'verification_output':
                formatted = {}
                for k, v in self.verification_output.items():
                    formatted[b64encode(k).decode('utf-8')] = [ (b64encode(a).decode('utf-8'), m) for a, m in v ]

                return self.twisted_dumps(formatted)
            if request.args['type'][0] == 'peers':
                peers = self.session.network.get_peers_for_service(self.identity_overlay.master_peer.mid)
                return self.twisted_dumps([ b64encode(p.mid).decode('utf-8') for p in peers ])
            if request.args['type'][0] == 'attributes':
                if 'mid' in request.args:
                    mid_b64 = request.args['mid'][0]
                    peer = self.get_peer_from_mid(mid_b64)
                else:
                    peer = self.identity_overlay.my_peer
                if peer:
                    blocks = self.identity_overlay.persistence.get_latest_blocks(peer.public_key.key_to_bin(), 200)
                    trimmed = {}
                    for b in blocks:
                        owner = b.public_key
                        if owner != peer.public_key.key_to_bin() or b.link_sequence_number != 0:
                            continue
                        attester = b64encode(sha1(b.link_public_key).digest())
                        previous = trimmed.get((attester, b.transaction['name']), None)
                        if not previous or previous.sequence_number < b.sequence_number:
                            trimmed[(attester, b.transaction['name'])] = b

                    return self.twisted_dumps([ (b.transaction['name'].decode('utf-8'), b64encode(b.transaction['hash']).decode('utf-8'), {cast_to_unicode(k):cast_to_unicode(v) for k, v in b.transaction['metadata'].items()}, b64encode(sha1(b.link_public_key).digest()).decode('utf-8')) for b in trimmed.values()
                                              ])
            if request.args['type'][0] == 'drop_identity':
                to_keep = [
                 self.persistent_key.public_key.key_to_bin()]
                if 'keep' in request.args:
                    to_keep += [self.identity_overlay.my_peer.public_key.key_to_bin()]
                attestation_hashes = self._drop_identity_table_data(to_keep)
                self._drop_attestation_table_data(attestation_hashes)
                self.attestation_requests.clear()
                my_new_peer = Peer(default_eccrypto.generate_key('curve25519'))
                for overlay in self.session.overlays:
                    overlay.my_peer = my_new_peer

            return self.twisted_dumps({'success': True})

    def render_POST(self, request):
        """
        type=request&mid=mid_b64&attibute_name=attribute_name&id_format=id_format
        type=allow_verify&mid=mid_b64&attibute_name=attribute_name
        type=attest&mid=mid_b64&attribute_name=attribute_name&attribute_value=attribute_value_b64
        type=verify&mid=mid_b64&attribute_hash=attribute_hash_b64&id_format=id_format
                   &attribute_values=attribute_value_b64,...
        """
        if not request.args or 'type' not in request.args:
            request.setResponseCode(http.BAD_REQUEST)
            return self.twisted_dumps({'error': 'parameters or type missing'})
        if request.args['type'][0] == 'request':
            mid_b64 = request.args['mid'][0]
            attribute_name = request.args['attribute_name'][0]
            id_format = request.args.get('id_format', ['id_metadata'])[0].decode('utf-8')
            peer = self.get_peer_from_mid(mid_b64)
            if peer:
                key = self.attestation_overlay.get_id_algorithm(id_format).generate_secret_key()
                metadata = {'id_format': id_format}
                if 'metadata' in request.args:
                    metadata_unicode = json.loads(b64decode(request.args['metadata'][0]))
                    for k, v in metadata_unicode.items():
                        metadata[cast_to_bin(k)] = cast_to_bin(v)

                self.attestation_metadata[(self.identity_overlay.my_peer, attribute_name)] = metadata
                self.attestation_overlay.request_attestation(peer, attribute_name, key, metadata)
        elif request.args['type'][0] == 'attest':
            mid_b64 = request.args['mid'][0]
            attribute_name = request.args['attribute_name'][0]
            attribute_value_b64 = request.args['attribute_value'][0]
            outstanding = self.attestation_requests.pop((mid_b64, attribute_name))
            outstanding[0].callback(b64decode(attribute_value_b64))
        elif request.args['type'][0] == 'allow_verify':
            mid_b64 = request.args['mid'][0]
            attribute_name = request.args['attribute_name'][0]
            outstanding = self.verify_requests.pop((mid_b64, attribute_name))
            outstanding.callback(True)
        elif request.args['type'][0] == 'verify':
            mid_b64 = request.args['mid'][0]
            attribute_hash = b64decode(request.args['attribute_hash'][0])
            reference_values = [ b64decode(v) for v in request.args['attribute_values'][0].split(',') ]
            id_format = request.args.get('id_format', ['id_metadata'])[0].decode('utf-8')
            peer = self.get_peer_from_mid(mid_b64)
            if peer:
                self.verification_output[b64decode(request.args['attribute_hash'][0])] = [ (b64decode(v), 0.0) for v in request.args['attribute_values'][0].split(',') ]
                self.attestation_overlay.verify_attestation_values(peer.address, attribute_hash, reference_values, self.on_verification_results, id_format)
        return self.twisted_dumps({'success': True})