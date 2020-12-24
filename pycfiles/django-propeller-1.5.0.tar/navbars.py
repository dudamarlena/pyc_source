# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/thorsten/code/django-propeller/django_propeller_demo/navbars.py
# Compiled at: 2017-03-24 13:36:01
from django_propeller.navbar import NavBar, NavBarLinkItem, NavBarDropDownItem, NavBarDropDownDivider

class MainNavBar(NavBar):
    brandname = 'django-propeller'
    brandurl = 'https://github.com/tfroehlich82/django-propeller'
    items = [
     NavBarLinkItem('Home', 'home'),
     NavBarLinkItem('Typography', 'typo'),
     NavBarLinkItem('Cards', 'cards'),
     NavBarLinkItem('Buttons', 'buttons'),
     NavBarLinkItem('Floating Action Buttons', 'fabs'),
     NavBarLinkItem('Navbar', 'navbar'),
     NavBarDropDownItem('Forms', [
      NavBarLinkItem('Form', 'form_default'),
      NavBarLinkItem('Formset', 'formset_default'),
      NavBarLinkItem('Form by field', 'form_by_field'),
      NavBarLinkItem('Form horizontal', 'form_horizontal'),
      NavBarLinkItem('Form inline', 'form_inline'),
      NavBarLinkItem('Form with files', 'form_with_files')]),
     NavBarLinkItem('Pagination', 'pagination'),
     NavBarLinkItem('Miscellaneous', 'misc')]


class DemoNavBar1(NavBar):
    brandname = 'Brand'
    items = [
     NavBarLinkItem('Link'),
     NavBarLinkItem('Link'),
     NavBarDropDownItem('DropDown', [
      NavBarLinkItem('Action'),
      NavBarLinkItem('Another action'),
      NavBarLinkItem('Something else here'),
      NavBarDropDownDivider(),
      NavBarLinkItem('Separated link'),
      NavBarDropDownDivider(),
      NavBarLinkItem('One more separated link')])]


class DemoNavBar2(DemoNavBar1):
    style_inverse = False