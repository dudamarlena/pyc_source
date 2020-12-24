# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /var/lib/jenkins/jobs/Diacamma_generic/workspace/asso/diacamma/member/printmodel/Adherent_0007.py
# Compiled at: 2020-03-20 14:11:02
# Size of source mod 2**32: 2186 bytes
"""
Printmodel django module for accounting

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
from diacamma.member.models import Adherent
name = _('card with image')
kind = 1
modelname = Adherent.get_long_name()
value = '<model>\n<body>\n<image height="25.0" width="25.0" top="5.0" left="2.0" padding="1.0" spacing="0.0" border_color="black" border_style="" border_width="0.2">\n#image\n</image>\n<text height="10.0" width="40.0" top="2.0" left="30.0" padding="1.0" spacing="0.0" border_color="black" border_style="" border_width="0.2" text_align="center" line_height="12" font_family="sans-serif" font_weight="" font_size="12">\n{[underline]}\n#firstname #lastname\n{[/underline]}\n</text>\n<text height="10.0" width="40.0" top="15.0" left="30.0" padding="1.0" spacing="0.0" border_color="black" border_style="" border_width="0.2" text_align="center" line_height="10" font_family="sans-serif" font_weight="" font_size="10">\n{[bold]}\n#subscription_set.license_set.team #subscription_set.license_set.activity #subscription_set.license_set.value\n{[/bold]}\n</text>\n<text height="10.0" width="40.0" top="28.0" left="30.0" padding="1.0" spacing="0.0" border_color="black" border_style="" border_width="0.2" text_align="center" line_height="11" font_family="sans-serif" font_weight="" font_size="11">\n{[italic]}\n#birthday\n{[/italic]}\n</text>\n</body>\n</model>'
mode = 1