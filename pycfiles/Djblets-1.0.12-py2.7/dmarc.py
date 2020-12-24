# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/djblets/mail/dmarc.py
# Compiled at: 2019-06-12 01:17:17
"""Functions for looking up DMARC entries in DNS."""
from __future__ import unicode_literals
import logging, pkg_resources
from dns import resolver as dns_resolver
from publicsuffix import PublicSuffixList
from djblets.cache.backend import DEFAULT_EXPIRATION_TIME, cache_memoize
logger = logging.getLogger(__name__)

class DmarcPolicy(object):
    """Types of DMARC policies.

    These policies define what happens if an e-mail fails sender verification
    (such as if the :mailheader:`From` address is spoofed).
    """
    UNSET = 0
    NONE = 1
    QUARANTINE = 2
    REJECT = 3
    _POLICY_TYPE_MAP = {b'none': NONE, 
       b'quarantine': QUARANTINE, 
       b'reject': REJECT}

    @classmethod
    def parse(cls, policy_str):
        """Return a policy type from a value in a DMARC record.

        Args:
            policy_str (unicode):
                The policy type from the record.

        Returns:
            int:
            One of :py:attr:`UNSET`, :py:attr:`NONE`, :py:attr:`QUARANTINE`,
            or :py:attr:`REJECT`.
        """
        return cls._POLICY_TYPE_MAP.get(policy_str.lower(), cls.UNSET)


class DmarcRecord(object):
    """Information on a DMARC record for a subdomain or organization domain.

    This is a parsed representation of the contents of a standard DMARC TXT
    record. It contains information that software can use to determine what
    will happen if a sender spoofs a From address, or if the e-mail otherwise
    fails sender verification.

    Senders can make use of this to determine whether they can safely spoof a
    :mailheader:`From` address (for legitimate reasons, such as to send an
    e-mail on behalf of a user when posting on a service), or whether they
    should fall back to an alternative means (such as using a noreply address
    and setting the :mailheader:`Reply-To` header).
    """

    def __init__(self, hostname, policy, subdomain_policy=DmarcPolicy.UNSET, pct=100, fields={}):
        """Initialize the record.

        Args:
            hostname (unicode):
                The hostname containing the ``_dmarc.`` TXT record.

            policy (int):
                The sender policy defined for the record.

            subdomain_policy (int, optional):
                The sender policy defined for subdomains on this domain.

            pct (int, optional):
                The percentage (as a number from 0-100) of e-mails that should
                be subject to the sender policy.

            fields (dict, optional):
                Additional fields from the record.
        """
        self.hostname = hostname
        self.policy = policy
        self.subdomain_policy = subdomain_policy
        self.pct = pct
        self.fields = fields

    def __eq__(self, other):
        """Return whether two records are equal.

        Records are considered equal if they have the same
        :py:attr:`hostname` and :py:attr:`fields`.

        Args:
            other (DmarcRecord):
                The record to compare to.

        Returns:
            bool:
            ``True`` if the two records are equal. ``False`` if they are not.
        """
        return self.hostname == other.hostname and self.fields == other.fields

    @classmethod
    def parse(cls, hostname, txt_record):
        """Return a DmarcRecord from a DMARC TXT record.

        Args:
            hostname (unicode):
                The hostname owning the ``_dmarc.`` TXT record.

            txt_record (unicode):
                The TXT record contents representing the DMARC configuration.

        Returns:
            DmarcRecord:
            The parsed record, if this is a valid DMARC record. If this
            is not valid, ``None`` will be returned instead.
        """
        if not txt_record.startswith(b'"v=DMARC1'):
            return None
        else:
            fields = {}
            for part in txt_record.strip(b'"').split(b';'):
                try:
                    key, value = part.split(b'=', 1)
                except ValueError:
                    continue

                key = key.strip()
                value = value.strip()
                if key and value:
                    fields[key] = value

            policy = DmarcPolicy.parse(fields.get(b'p', b''))
            subdomain_policy = DmarcPolicy.parse(fields.get(b'sp', b''))
            try:
                pct = int(fields.get(b'pct', b'100'))
            except ValueError:
                pct = 100

            return cls(hostname=hostname, policy=policy, subdomain_policy=subdomain_policy, pct=pct, fields=fields)


def _fetch_dmarc_record(hostname, use_cache, cache_expiration):
    """Fetch a DMARC record from DNS, optionally caching it.

    This will query DNS for the DMARC record for a given hostname, returning
    the string contents of the record.

    The contents can be cached, preventing the need for subsequent DNS queries.

    This is used internally by :py:func:`get_dmarc_record`.

    Args:
        hostname (unicode):
            The hostname to fetch the record from.

        use_cache (bool, optional):
            Whether to use the cache for looking up and storing record data.

        cache_expiration (int, optional):
            The expiration time for cached data.

    Returns:
        DmarcRecord:
        The DMARC record. If it could not be found, or DNS lookup failed,
        ``None`` will be returned instead.
    """

    def _fetch_record():
        try:
            return dns_resolver.query(b'_dmarc.%s' % hostname, b'TXT')[0].to_text()
        except (IndexError, dns_resolver.NXDOMAIN, dns_resolver.NoAnswer, dns_resolver.NoNameservers):
            raise ValueError

    try:
        if use_cache:
            record_str = cache_memoize(b'dmarc-record-%s' % hostname, lambda : _fetch_record(), expiration=cache_expiration)
        else:
            record_str = _fetch_record()
    except ValueError:
        record_str = None

    if record_str:
        return DmarcRecord.parse(hostname, record_str)
    else:
        return


def get_dmarc_record(hostname, use_cache=True, cache_expiration=DEFAULT_EXPIRATION_TIME):
    """Return a DMARC record for a given hostname.

    This will query the DNS records for a hostname, returning a parsed version
    of the DMARC record, if found. If a record could not be found for the
    hostname, the organizational domain will be used instead (which is
    generally example.com for foo.bar.example.com, but this depends on the
    domain in question).

    By default, the fetched record from DNS is cached, allowing this to be
    called multiple times without repeated DNS queries. This is optional,
    as is the expiration time for the cached data (which defaults to 1 month).

    Args:
        hostname (unicode):
            The hostname to look up the DMARC information from.

        use_cache (bool, optional):
            Whether to use the cache for looking up and storing record data.

        cache_expiration (int, optional):
            The expiration time for cached data.

    Returns:
        DmarcRecord:
        The DMARC record. If it could not be found, ``None`` will be returned
        instead.
    """
    record = _fetch_dmarc_record(hostname=hostname, use_cache=use_cache, cache_expiration=cache_expiration)
    if not record:
        filename = b'mail/public_suffix_list.dat'
        try:
            psl = PublicSuffixList(pkg_resources.resource_stream(b'djblets', filename))
        except IOError as e:
            logger.error(b'Unable to read public domain suffix list file "%s" from Djblets package: %s', filename, e)
        else:
            new_hostname = psl.get_public_suffix(hostname)
            if new_hostname != hostname:
                record = _fetch_dmarc_record(hostname=new_hostname, use_cache=use_cache, cache_expiration=cache_expiration)
    return record


def is_email_allowed_by_dmarc(email_address):
    """Return whether DMARC rules safely allow sending using an e-mail address.

    This will take an e-mail address (which must be in the form of
    ``name@domain``, ideally parsed by :py:func:`mail.utils.parseaddr`) and
    check to see if there are any DMARC rules that could prevent the e-mail
    from being sent/received if it were to fail sender verification.

    Callers can use this to decide whether they can safely send using a user's
    e-mail address, or whether they need to send using the service's address.

    Args:
        email_address (unicode):
            The e-mail address for the From field.

    Returns:
        bool:
        ``True`` if the e-mail address can be safely used in a
        :mailheader:`From` header. ``False`` if it should not be used.
    """
    hostname = email_address.split(b'@')[(-1)]
    bad_policies = (DmarcPolicy.QUARANTINE, DmarcPolicy.REJECT)
    dmarc_record = get_dmarc_record(hostname)
    return not (dmarc_record and dmarc_record.pct > 0 and (dmarc_record.hostname == hostname and dmarc_record.policy in bad_policies or dmarc_record.hostname != hostname and hostname.endswith(dmarc_record.hostname) and dmarc_record.subdomain_policy in bad_policies))