# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/camelot/view/controls/delegates/manytoonechoicesdelegate.py
# Compiled at: 2013-04-11 17:47:52
from customdelegate import CustomDelegate
from camelot.view.controls import editors

class ManyToOneChoicesDelegate(CustomDelegate):
    """Display a ManyToOne field as a ComboBox, filling the list of choices with
  the objects of the target class. 
  
  .. image:: /_static/enumeration.png
  
  The items in the ComboBox are the unicode representation of the related objects.
  So these classes need an implementation of their __unicode__ method to show
  up in a human readable way in the ComboBox.
  """
    editor = editors.OneToManyChoicesEditor