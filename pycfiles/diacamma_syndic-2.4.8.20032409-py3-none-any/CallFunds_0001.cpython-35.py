# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /var/lib/jenkins/jobs/Diacamma_generic/workspace/syndic/diacamma/condominium/printmodel/CallFunds_0001.py
# Compiled at: 2020-03-20 14:11:00
# Size of source mod 2**32: 10340 bytes
"""
Printmodel django module for condominium

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
from diacamma.condominium.models import CallFunds
name = _('call of funds')
kind = 2
modelname = CallFunds.get_long_name()
value = '\n<model hmargin="10.0" vmargin="10.0" page_width="210.0" page_height="297.0">\n<header extent="25.0">\n<text height="20.0" width="120.0" top="5.0" left="70.0" padding="1.0" spacing="0.0" border_color="black" border_style="" border_width="0.2" text_align="center" line_height="20" font_family="sans-serif" font_weight="" font_size="20">\n{[b]}#OUR_DETAIL.name{[/b]}\n</text>\n<image height="25.0" width="30.0" top="0.0" left="10.0" padding="1.0" spacing="0.0" border_color="black" border_style="" border_width="0.2">\n#OUR_DETAIL.image\n</image>\n</header>\n<bottom extent="10.0">\n<text height="10.0" width="190.0" top="00.0" left="0.0" padding="1.0" spacing="0.0" border_color="black" border_style="" border_width="0.2" text_align="center" line_height="8" font_family="sans-serif" font_weight="" font_size="8">\n{[italic]}\n#OUR_DETAIL.address - #OUR_DETAIL.postal_code #OUR_DETAIL.city - #OUR_DETAIL.tel1 #OUR_DETAIL.tel2 #OUR_DETAIL.email{[br/]}#OUR_DETAIL.identify_number\n{[/italic]}\n</text>\n</bottom>\n<body>\n<text height="8.0" width="190.0" top="0.0" left="0.0" padding="1.0" spacing="0.0" border_color="black" border_style="" border_width="0.2" text_align="center" line_height="15" font_family="sans-serif" font_weight="" font_size="15">\n{[b]}%(callfunds)s #num{[/b]}\n</text>\n<text height="8.0" width="190.0" top="8.0" left="0.0" padding="1.0" spacing="0.0" border_color="black" border_style="" border_width="0.2" text_align="center" line_height="13" font_family="sans-serif" font_weight="" font_size="13">\n#date\n</text>\n<text height="20.0" width="100.0" top="25.0" left="80.0" padding="1.0" spacing="0.0" border_color="black" border_style="" border_width="0.2" text_align="center" line_height="11" font_family="sans-serif" font_weight="" font_size="11">\n{[b]}#owner.third.contact.str{[/b]}{[br/]}#owner.third.contact.address{[br/]}#owner.third.contact.postal_code #owner.third.contact.city\n</text>\n<table height="100.0" width="170.0" top="70.0" left="10.0" padding="1.0" spacing="0.0" border_color="black" border_style="" border_width="0.2">\n    <columns width="20.0" display_align="center" border_color="black" border_style="solid" border_width="0.2" text_align="center" line_height="10" font_family="sans-serif" font_weight="" font_size="9">\n    {[b]}%(set)s{[/b]}\n    </columns>\n    <columns width="82.0" display_align="center" border_color="black" border_style="solid" border_width="0.2" text_align="center" line_height="10" font_family="sans-serif" font_weight="" font_size="9">\n    {[b]}%(designation)s{[/b]}\n    </columns>\n    <columns width="17.0" display_align="center" border_color="black" border_style="solid" border_width="0.2" text_align="center" line_height="10" font_family="sans-serif" font_weight="" font_size="9">\n    {[b]}%(totalamount)s{[/b]}\n    </columns>\n    <columns width="17.0" display_align="center" border_color="black" border_style="solid" border_width="0.2" text_align="center" line_height="10" font_family="sans-serif" font_weight="" font_size="9">\n    {[b]}%(partsum)s{[/b]}\n    </columns>\n    <columns width="17.0" display_align="center" border_color="black" border_style="solid" border_width="0.2" text_align="center" line_height="10" font_family="sans-serif" font_weight="" font_size="9">\n    {[b]}%(partition)s{[/b]}\n    </columns>\n    <columns width="17.0" display_align="center" border_color="black" border_style="solid" border_width="0.2" text_align="center" line_height="10" font_family="sans-serif" font_weight="" font_size="9">\n    {[b]}%(price)s{[/b]}\n    </columns>\n    <rows data="calldetail_set">\n        <cell display_align="center" border_color="black" border_style="solid" border_width="0.2" text_align="start" line_height="7" font_family="sans-serif" font_weight="" font_size="7">\n#set\n        </cell>\n        <cell display_align="center" border_color="black" border_style="solid" border_width="0.2" text_align="start" line_height="7" font_family="sans-serif" font_weight="" font_size="7">\n#designation\n        </cell>\n        <cell display_align="center" border_color="black" border_style="solid" border_width="0.2" text_align="end" line_height="7" font_family="sans-serif" font_weight="" font_size="7">\n#total_amount\n        </cell>\n        <cell display_align="center" border_color="black" border_style="solid" border_width="0.2" text_align="end" line_height="7" font_family="sans-serif" font_weight="" font_size="7">\n#set.total_part\n        </cell>\n        <cell display_align="center" border_color="black" border_style="solid" border_width="0.2" text_align="end" line_height="7" font_family="sans-serif" font_weight="" font_size="7">\n#owner_part\n        </cell>\n        <cell display_align="center" border_color="black" border_style="solid" border_width="0.2" text_align="end" line_height="7" font_family="sans-serif" font_weight="" font_size="7">\n#price_txt\n        </cell>\n    </rows>\n</table>\n<text height="15.0" width="30.0" top="190.0" left="140.0" padding="1.0" spacing="0.0" border_color="black" border_style="" border_width="0.2" text_align="right" line_height="9" font_family="sans-serif" font_weight="" font_size="9">\n{[u]}{[b]}%(total)s{[/b]}{[/u]}{[br/]}\n</text>\n<text height="15.0" width="20.0" top="190.0" left="170.0" padding="1.0" spacing="0.0" border_color="black" border_style="" border_width="0.2" text_align="right" line_height="9" font_family="sans-serif" font_weight="" font_size="9">\n{[u]}#total{[/u]}{[br/]}\n</text>\n<text height="20.0" width="100.0" top="190.0" left="0.0" padding="1.0" spacing="0.0" border_color="black" border_style="" border_width="0.2" text_align="left" line_height="9" font_family="sans-serif" font_weight="" font_size="9">\n#comment\n</text>\n<text height="5.0" width="130.0" top="200.0" left="00.0" padding="1.0" spacing="0.0" border_color="black" border_style="" border_width="0.2" text_align="center" line_height="9" font_family="sans-serif" font_weight="" font_size="9">\n{[u]}{[i]}%(situation)s{[/i]}{[/u]}\n</text>\n<text height="15.0" width="50.0" top="205.0" left="00.0" padding="1.0" spacing="0.0" border_color="black" border_style="" border_width="0.2" text_align="right" line_height="9" font_family="sans-serif" font_weight="" font_size="9">\n{[i]}%(total_initial)s{[/i]}{[br/]}\n{[i]}%(total_call)s{[/i]}{[br/]}\n{[i]}%(total_payed)s{[/i]}{[br/]}\n{[i]}%(total_estimate)s{[/i]}{[br/]}\n{[br/]}\n{[i]}%(total_cash_advance_call)s{[/i]}{[br/]}\n{[i]}%(total_cash_advance_payoff)s{[/i]}{[br/]}\n</text>\n<text height="15.0" width="15.0" top="205.0" left="50.0" padding="1.0" spacing="0.0" border_color="black" border_style="" border_width="0.2" text_align="right" line_height="9" font_family="sans-serif" font_weight="" font_size="9">\n#owner.total_current_initial{[br/]}\n#owner.total_current_call{[br/]}\n#owner.total_current_payoff{[br/]}\n#owner.total_current_owner{[br/]}\n{[br/]}\n#owner.total_cash_advance_call{[br/]}\n#owner.total_cash_advance_payoff{[br/]}\n</text>\n\n<text height="15.0" width="60.0" top="205.0" left="70.0" padding="1.0" spacing="0.0" border_color="black" border_style="" border_width="0.2" text_align="right" line_height="9" font_family="sans-serif" font_weight="" font_size="9">\n{[i]}%(total_excep_initial)s{[/i]}{[br/]}\n{[i]}%(total_excep_call)s{[/i]}{[br/]}\n{[i]}%(total_excep_payed)s{[/i]}{[br/]}\n{[i]}%(total_excep_estimate)s{[/i]}{[br/]}\n{[br/]}\n{[i]}%(total_fund_works_call)s{[/i]}{[br/]}\n{[i]}%(total_fund_works_payoff)s{[/i]}{[br/]}\n</text>\n<text height="15.0" width="15.0" top="205.0" left="130.0" padding="1.0" spacing="0.0" border_color="black" border_style="" border_width="0.2" text_align="right" line_height="9" font_family="sans-serif" font_weight="" font_size="9">\n#owner.total_exceptional_initial{[br/]}\n#owner.total_exceptional_call{[br/]}\n#owner.total_exceptional_payoff{[br/]}\n#owner.total_exceptional_owner{[br/]}\n{[br/]}\n#owner.total_fund_works_call{[br/]}\n#owner.total_fund_works_payoff{[br/]}\n</text>\n\n<text height="10.0" width="190.0" top="235.0" left="0.0" padding="1.0" spacing="0.0" border_color="black" border_style="" border_width="0.2\n" text_align="center" line_height="11" font_family="sans-serif" font_weight="" font_size="11">\n{[b]}{[u]}%(sumtopay)s : #owner.sumtopay{[/u]}{[/b]}\n</text>\n\n</body>\n</model>\n' % {'callfunds': _('call of funds'), 
 'set': _('set'), 
 'designation': _('designation'), 
 'totalamount': _('total'), 
 'partsum': _('tantime sum'), 
 'partition': _('tantime'), 
 'price': _('amount'), 
 'situation': _('situation at #owner.date_current'), 
 'total_initial': _('current initial state'), 
 'total_call': _('current total call for funds'), 
 'total_payed': _('current total payoff'), 
 'total_estimate': _('current total owner'), 
 'total_excep_initial': _('exceptional initial state'), 
 'total_excep_call': _('exceptional total call for funds'), 
 'total_excep_payed': _('exceptional total payoff'), 
 'total_excep_estimate': _('exceptional total owner'), 
 'total_cash_advance_call': _('cash advance total call for funds'), 
 'total_cash_advance_payoff': _('cash advance total payoff'), 
 'total_fund_works_call': _('fund for works total call for funds'), 
 'total_fund_works_payoff': _('fund for works total payoff'), 
 'total': _('total'), 
 'sumtopay': _('sum to pay')}