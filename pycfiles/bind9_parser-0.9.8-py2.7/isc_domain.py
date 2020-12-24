# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bind9_parser/isc_domain.py
# Compiled at: 2019-11-22 14:50:11
"""
File: isc_domain.py

Element: domain

Title: Elements providing domain name syntaxes

Description: Provides domain-related grammar in PyParsing engine
             for ISC-configuration style

 For domain names to be valid, domain names MUST:

 * have a minimum of 3 and a maximum of 63 characters;
 * begin with a letter or a number and end with a letter or a number;
 * use the English character set and may contain letters (i.e., a-z, A-Z),
       numbers (i.e. 0-9) and dashes (-) or a combination of these;
 * neither begin with nor end with a dash (-);
 * not contain a dash in the third and fourth positions (e.g. www.ab- -cd.com);
 * not include a space (e.g. www.ab cd.com);
 * not include underscore (e.g www.ab_cd.com)

 * Also RFC4343 states that label (between periods) cannot be greater
   than 63 chars Nor total length of a fully-qualified domain name
   cannot exceed 253 chars.
 * Also, for input data purposes, a domain_label cannot have its case changed
   from its original upper or loewr case. Otherwise, you'd be breaking
   international IDN
 * Only the first label may only just contain "*", but never used asterisk
   in any other positions or labels of the domain or subdomain name.

Note: We cannot enforce TLD syntax because many option settings allows for
      just the domain label (congress) or its fully-qualified domain
      name (www.congress.gov). So, additional out-of-band syntax checking
      would be required for domain-label-syntax fields

      Same thing to its 2nd-level domain name, as TLD described above.

      Hostname, while restrictive in by some OS-imposed ban on dash/hyphen
      and underscore symbols, we too cannot enforce domain label syntax
      either because it may be a liberal 3rd-level subdomain naming
      convention such as '_53._tcp.example.com' or
      LetsEncrypt's '_acme-challenge.example.com'

      HOWEVER, if such a FQDN ends with a period ('.'), then we could
      enforce this with real-world FQDN naming convention for 2nd and TLD
      name syntax checking, but ... not here, not now.

      A deviation (or more accurately, expanding) from ISC DNS
      "domain_name" convention, we use:

        - TLD for top-level domain
        - DOMAIN for 2nd-level domain
        - SUBDOMAIN for 3rd-level (and lower) domain

      And DOMAIN-GENERIC for all 3 levels of domain names.
"""
from pyparsing import Optional, Word, Combine, srange, alphanums, ZeroOrMore, Literal, alphas, Char, Regex, OneOrMore
from bind9_parser.isc_utils import squote, dquote
g_test_over_63_chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789abc'
domain_charset_alphas = alphas
domain_charset_alphanums = alphanums
domain_charset_alphanums_underscore = alphanums + '_'
domain_charset_alphanums_dash = alphanums + '-'
domain_charset_alphanums_dash_underscore = alphanums + '_-'
domain_charset_wildcard = '*'
domain_alpha = Word(domain_charset_alphas)
domain_alpha.setName('<alpha>')
domain_alphanum = Word(domain_charset_alphanums)
domain_alphanum.setName('<alphanum>')
domain_alphanum_dash = Word(domain_charset_alphanums_dash)
domain_alphanum_dash.setName('<alphanum-hyphen>')
domain_alphanum_underscore = Word(domain_charset_alphanums_underscore)
domain_alphanum_underscore.setName('<alphanum-underscore>')
domain_alphanum_dash_underscore = Word(domain_charset_alphanums_dash_underscore)
domain_alphanum_dash_underscore.setName('<alphanum-hyphen-underscore>')
tld_label = Word(domain_charset_alphas, min=2, max=24)
tld_label_regex = '[A-Za-z]{3,24}'
tld_label.setName('<tdl-label>')
domain_label_regex = '[a-zA-Z0-9]{1,1}([a-zA-Z0-9\\-]{0,61}){0,1}[a-zA-Z0-9]{1,1}'
domain_label = Regex(domain_label_regex)
domain_label.setName('<level2-domain-label>')
subdomain_label_regex = '[A-Za-z0-9_]{1,1}(([A-Za-z0-9_\\-]{0,61}){0,1}[A-Za-z0-9_]{1,1}){0,1}'
subdomain_label = Regex(subdomain_label_regex)
subdomain_label.setName('<subdomain_label>')
domain_generic_label = Word(domain_charset_alphanums_dash_underscore, min=1, max=63)
domain_generic_label.setName('<domain_generic_label>')
domain_generic_label.setResultsName('domain_name')
domain_fqdn_regex = '((' + subdomain_label_regex + '\\.' + '){0,16}' + domain_label_regex + '\\.' + '){0,1}' + tld_label_regex
domain_fqdn = Regex(domain_fqdn_regex)
domain_fqdn.setName('<strict-fqdn>')
domain_fqdn.setResultsName('domain_name')
domain_generic_fqdn = Combine(domain_generic_label + ZeroOrMore(Literal('.') + domain_generic_label) + Optional(Char('.')))
domain_generic_fqdn.setName('<generic-fqdn>')
domain_generic_fqdn.setResultsName('domain_name')
quoted_domain_generic_fqdn = Combine(squote - domain_generic_fqdn - squote) | Combine(dquote - domain_generic_fqdn - dquote)
quoted_domain_generic_fqdn.setName('<quoted_domain_name>')
quotable_domain_generic_fqdn = Combine(squote - domain_generic_fqdn - squote) | Combine(dquote - domain_generic_fqdn - dquote) | domain_generic_fqdn
quotable_domain_generic_fqdn.setName('<quotable_domain_name>')
rr_fqdn_w_absolute = Combine(domain_generic_fqdn + Optional(Literal('.')))
rr_fqdn_w_absolute.setName('<rr-fqdn-with-abs>')
rr_fqdn_w_absolute.setResultsName('domain_name')
rr_domain_name_type = Combine(domain_generic_fqdn + Optional(Literal('.')))
rr_domain_name_type.setName('<rr-name>')
rr_domain_name_type.setResultsName('domain_name')
rr_domain_name_or_wildcard_type = rr_domain_name_type | Char(domain_charset_wildcard)
rr_domain_name_or_wildcard_type.setName('<rr-name-or-wildcard>')
rr_domain_name_or_wildcard_type.setResultsName('domain_name')
host_name_first_char = Char(srange('[a-zA-Z0-9]'))
host_name_first_char.setName('<one_char_hostname>')
host_name_two_chars = Combine(Char(srange('[a-zA-Z0-9]')) + Char(srange('[a-zA-Z0-9]')))
host_name_two_chars.setName('<two_char_hostname>')
charset_host_name_middle_chars = srange('[a-zA-Z0-9]') + '-'
host_name_long_type = Regex('[a-zA-Z0-9]{1}[a-zA-Z0-9\\-]{0,62}[a-zA-Z0-9]{1}')('hostname_long')
host_name_long_type.setName('<hostname_regex>')
host_name_just_the_hostname = (host_name_long_type | host_name_two_chars | host_name_first_char)('hostname_indice')
host_name = host_name_just_the_hostname | Combine(host_name_just_the_hostname + '.' + domain_fqdn)
host_name.setDebug()