# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bauble/plugins/plants/itf2.py
# Compiled at: 2016-08-21 21:14:39
try:
    from bauble.i18n import _
except:
    _ = lambda x: x

accsta_dict = (
 ('', ''),
 (
  'C', _('Current accession in the living collection')),
 (
  'D', _('Non‑current accession of the living collection due to death')),
 (
  'T', _('Non‑current accession due to transfer to another record system, normally of another garden')),
 (
  'S', _('Stored in a dormant state')),
 (
  'O', _('Other accession status  - different from those above.')))
acct_dict = (
 ('', ''),
 (
  'P', _('Whole plant')),
 (
  'S', _('Seed or Spore')),
 (
  'V', _('Vegetative part')),
 (
  'T', _('Tissue culture ')),
 (
  'O', _('Other')))
hybrid_marker = (
 (
  '', _('not a hybrid')),
 (
  'H', _('H - hybrid formula')),
 (
  '×', _('× - nothotaxon')),
 (
  '+', _('+ - graft chimera')))
aggregate = (
 (
  '', _('not a complex')),
 (
  'agg.', _('aggregate taxon')))
acc_spql = (
 (None, ''),
 (
  's. lat.', _('aggregrate species (sensu lato)')),
 (
  's. str.', _('segregate species (sensu stricto)')))
vlev_dict = (
 (None, ''),
 (
  'U', _('It is not known if the name of the plant has been checked by an authority.')),
 (
  '0', _('The name of the plant has not been determined by any authority')),
 (
  '1', _('The name of the plant has been determined by comparison with other named plants')),
 (
  '2', _('The name of the plant has been determined by a taxonomist or other competent person using the facilities of a library and/or herbarium, or other documented living material')),
 (
  '3', _('The name of the plant has been determined by a taxonomist who is currently or has been recently involved in a revision of the family or genus')),
 (
  '4', _('The plant represents all or part of the type material on which the name was based, or the plant has been derived therefore by asexual propagation')))
prot_dict = (
 (None, ''),
 (
  'W', _('Accession of wild source')),
 (
  'Z', _('Propagule(s) from a wild source plant')),
 (
  'G', _('Accession not of wild source')),
 (
  'U', _('Insufficient data to determine')))
prohis_dict = (
 (None, ''),
 (
  'I', _('Individual wild plant(s)')),
 (
  'S', _('Plant material arising from sexual reproduction (excluding apomixis)')),
 (
  'SA', _('From open breeding')),
 (
  'SB', _('From controlled breeding')),
 (
  'SC', _('From plants that are isolated and definitely self-pollinated')),
 (
  'V', _('Plant material derived asexually')),
 (
  'VA', _('From vegetative reproduction')),
 (
  'VB', _('From apomictic cloning (agamospermy)')),
 (
  'U', _('Propagation history uncertain, or no information')))
wpst_dict = (
 (None, ''),
 (
  'Wild native', _('Endemic found within its indigenous range')),
 (
  'Wild non-native', _('Plant found outside its indigenous range')),
 (
  'Cultivated native', _('Endemic, cultivated and reintroduced or translocated within indigenous range')),
 (
  'Cultivated non-native', _('cultivated, found outside indigenous range')))
dont_dict = (
 (
  'E', _('Expedition')),
 (
  'G', _('Gene bank')),
 (
  'B', _('Botanic Garden or Arboretum')),
 (
  'R', _('Other research, field or experimental station')),
 (
  'S', _('Staff of this botanic garden')),
 (
  'U', _('University Department')),
 (
  'H', _('Horticultural Association or Garden Club')),
 (
  'M', _('Municipal department')),
 (
  'N', _('Nursery or other commercial establishment')),
 (
  'I', _('Individual')),
 (
  'O', _('Other')),
 (
  'U', _('Unknown')))
per_dict = (
 (None, ''),
 (
  'M', _('Monocarpic plants')),
 (
  'MA', _('Annuals')),
 (
  'MB', _('Biennials and short-lived perennials')),
 (
  'ML', _('Long-lived monocarpic plants')),
 (
  'P', _('Polycarpic plants')),
 (
  'PD', _('Deciduous polycarpic plants')),
 (
  'PE', _('Evergreen polycarpic plants')),
 (
  'U', _('Uncertain which of the above applies.')))
brs_dict = (
 (None, ''),
 (
  'M', _("'Male', defined as plants that do not produce functional female flowers")),
 (
  'F', _("'Female', defined as plants that do not produce functional male flowers")),
 (
  'B', _("The accession includes both 'male' and 'female' individuals as described above")),
 (
  'Q', _('Dioecious plant of unknown sex')),
 (
  'H', _('The accession reproduces sexually, and possesses hermaphrodite flowers or is monoecious')),
 (
  'H1', _('The accession reproduces sexually, and possesses hermaphrodite flowers or is monoecious, but is known to be self-incompatible.')),
 (
  'A', _('The accession reproduces by agamospermy')),
 (
  'U', _('Insufficient information to determine breeding system')))