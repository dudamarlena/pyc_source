# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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