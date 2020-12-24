# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /var/lib/jenkins/jobs/Diacamma_generic/workspace/financial/diacamma/invoice/printmodel/Bill_0001.py
# Compiled at: 2020-03-20 14:10:57
# Size of source mod 2**32: 7899 bytes
"""
Printmodel django module for invoice

@author: Laurent GAY
@organization: sd-libre.fr
@contact: info@sd-libre.fr
@copyright: 2016 sd-libre.fr
@license: This file is part of Lucterios.

Lucterios is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Lucterios is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Lucterios.  If not, see <http://www.gnu.org/licenses/>.
"""
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from diacamma.invoice.models import Bill
name = _('bill')
kind = 2
modelname = Bill.get_long_name()
value = '\n<model hmargin="10.0" vmargin="10.0" page_width="210.0" page_height="297.0">\n<header extent="25.0">\n<text height="20.0" width="120.0" top="5.0" left="70.0" padding="1.0" spacing="0.0" border_color="black" border_style="" border_width="0.2" text_align="center" line_height="20" font_family="sans-serif" font_weight="" font_size="20">\n{[b]}#OUR_DETAIL.name{[/b]}\n</text>\n<image height="25.0" width="30.0" top="0.0" left="10.0" padding="1.0" spacing="0.0" border_color="black" border_style="" border_width="0.2">\n#OUR_DETAIL.image\n</image>\n</header>\n<bottom extent="10.0">\n<text height="10.0" width="190.0" top="00.0" left="0.0" padding="1.0" spacing="0.0" border_color="black" border_style="" border_width="0.2" text_align="center" line_height="8" font_family="sans-serif" font_weight="" font_size="8">\n{[italic]}\n#OUR_DETAIL.address - #OUR_DETAIL.postal_code #OUR_DETAIL.city - #OUR_DETAIL.tel1 #OUR_DETAIL.tel2 #OUR_DETAIL.email{[br/]}#OUR_DETAIL.identify_number\n{[/italic]}\n</text>\n</bottom>\n<body>\n<text height="8.0" width="190.0" top="0.0" left="0.0" padding="1.0" spacing="0.0" border_color="black" border_style="" border_width="0.2" text_align="center" line_height="15" font_family="sans-serif" font_weight="" font_size="15">\n{[b]}#type_bill #num_txt{[/b]}\n</text>\n<text height="8.0" width="190.0" top="8.0" left="0.0" padding="1.0" spacing="0.0" border_color="black" border_style="" border_width="0.2" text_align="center" line_height="13" font_family="sans-serif" font_weight="" font_size="13">\n#date\n</text>\n<text height="20.0" width="100.0" top="25.0" left="80.0" padding="1.0" spacing="0.0" border_color="black" border_style="" border_width="0.2" text_align="center" line_height="11" font_family="sans-serif" font_weight="" font_size="11">\n{[b]}#third.contact.str{[/b]}{[br/]}#third.contact.address{[br/]}#third.contact.postal_code #third.contact.city\n</text>\n<table height="100.0" width="190.0" top="55.0" left="0.0" padding="1.0" spacing="0.0" border_color="black" border_style="" border_width="0.2">\n    <columns width="20.0" display_align="center" border_color="black" border_style="solid" border_width="0.2" text_align="center" line_height="10" font_family="sans-serif" font_weight="" font_size="9">\n    {[b]}%(article)s{[/b]}\n    </columns>\n    <columns width="90.0" display_align="center" border_color="black" border_style="solid" border_width="0.2" text_align="center" line_height="10" font_family="sans-serif" font_weight="" font_size="9">\n    {[b]}%(designation)s{[/b]}\n    </columns>\n    <columns width="20.0" display_align="center" border_color="black" border_style="solid" border_width="0.2" text_align="center" line_height="10" font_family="sans-serif" font_weight="" font_size="9">\n    {[b]}%(price)s{[/b]}\n    </columns>\n    <columns width="15.0" display_align="center" border_color="black" border_style="solid" border_width="0.2" text_align="center" line_height="10" font_family="sans-serif" font_weight="" font_size="9">\n    {[b]}%(Qty)s{[/b]}\n    </columns>\n    <columns width="20.0" display_align="center" border_color="black" border_style="solid" border_width="0.2" text_align="center" line_height="10" font_family="sans-serif" font_weight="" font_size="9">\n    {[b]}%(reduce)s{[/b]}\n    </columns>\n    <columns width="20.0" display_align="center" border_color="black" border_style="solid" border_width="0.2" text_align="center" line_height="10" font_family="sans-serif" font_weight="" font_size="9">\n    {[b]}%(total)s{[/b]}\n    </columns>\n    <rows data="detail_set">\n        <cell display_align="center" border_color="black" border_style="solid" border_width="0.2" text_align="start" line_height="7" font_family="sans-serif" font_weight="" font_size="7">\n#article.reference\n        </cell>\n        <cell display_align="center" border_color="black" border_style="solid" border_width="0.2" text_align="start" line_height="7" font_family="sans-serif" font_weight="" font_size="7">\n#designation\n        </cell>\n        <cell display_align="center" border_color="black" border_style="solid" border_width="0.2" text_align="end" line_height="7" font_family="sans-serif" font_weight="" font_size="7">\n#price_txt\n        </cell>\n        <cell display_align="center" border_color="black" border_style="solid" border_width="0.2" text_align="end" line_height="7" font_family="sans-serif" font_weight="" font_size="7">\n#quantity #unit\n        </cell>\n        <cell display_align="center" border_color="black" border_style="solid" border_width="0.2" text_align="end" line_height="7" font_family="sans-serif" font_weight="" font_size="7">\n#reduce_txt\n        </cell>\n        <cell display_align="center" border_color="black" border_style="solid" border_width="0.2" text_align="end" line_height="7" font_family="sans-serif" font_weight="" font_size="7">\n#total\n        </cell>\n    </rows>\n</table>\n<text height="15.0" width="100.0" top="220.0" left="00.0" padding="1.0" spacing="0.0" border_color="black" border_style="" border_width="0.2" text_align="right" line_height="9" font_family="sans-serif" font_weight="" font_size="9">\n{[i]}#title_vta_details{[/i]}{[br/]}\n{[i]}%(total VAT)s{[/i]}{[br/]}\n{[i]}%(total excl. taxes)s{[/i]}{[br/]}\n</text>\n<text height="15.0" width="15.0" top="220.0" left="100.0" padding="1.0" spacing="0.0" border_color="black" border_style="" border_width="0.2" text_align="right" line_height="9" font_family="sans-serif" font_weight="" font_size="9">\n#vta_details{[br/]}\n#vta_sum{[br/]}\n#total_excltax{[br/]}\n</text>\n<text height="15.0" width="30.0" top="220.0" left="140.0" padding="1.0" spacing="0.0" border_color="black" border_style="" border_width="0.2" text_align="right" line_height="9" font_family="sans-serif" font_weight="" font_size="9">\n{[u]}{[b]}%(total incl. taxes)s{[/b]}{[/u]}{[br/]}\n{[u]}{[b]}%(total payed)s{[/b]}{[/u]}{[br/]}\n{[u]}{[b]}%(rest to pay)s{[/b]}{[/u]}{[br/]}\n</text>\n<text height="15.0" width="20.0" top="220.0" left="170.0" padding="1.0" spacing="0.0" border_color="black" border_style="" border_width="0.2" text_align="right" line_height="9" font_family="sans-serif" font_weight="" font_size="9">\n{[u]}#total_incltax{[/u]}{[br/]}\n{[u]}#total_payed{[/u]}{[br/]}\n{[u]}#total_rest_topay{[/u]}{[br/]}\n</text>\n<text height="20.0" width="100.0" top="220.0" left="0.0" padding="1.0" spacing="0.0" border_color="black" border_style="" border_width="0.2" text_align="left" line_height="9" font_family="sans-serif" font_weight="" font_size="9">\n#comment\n</text>\n</body>\n</model>\n' % {'article': _('article'), 
 'designation': _('designation'), 
 'price': _('price'), 
 'Qty': _('Qty'), 
 'reduce': 'reduce', 
 'total': 'total', 
 'total VAT': _('total VAT'), 
 'total excl. taxes': _('total excl. taxes'), 
 'total incl. taxes': _('total incl. taxes'), 
 'total payed': _('total payed'), 
 'rest to pay': _('rest to pay')}