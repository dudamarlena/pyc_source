# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/tau/selectorstrings/interfaces.py
# Compiled at: 2010-12-21 05:27:01
"""Declaration of various object interfaces.
"""
from zope.interface import Interface
from zope.schema import TextLine

class ISelectorStringDirective(Interface):
    """Schema for a simple, single ZCML directive for declaring a vocabulary of strings.

       This schema determines the XML attributes accepted by the ZCML
       directive and how they are parsed/validated.

       Example of the directive:

         <selectorstring
             cluster="docfolders"
             label="Personal Photos"
             value="/home/jeff/photos/"
             />
    """
    cluster = TextLine(title='Cluster', description='The name of the cluster under which to group this label/value.', required=False)
    label = TextLine(title='Label', description='An optional label to display to the user making the choice.', required=False)
    value = TextLine(title='Value', description='A string representing the actual value used internally.', required=True)


class ISelectorClusterDirective(Interface):
    """Schema for a complex, nested ZCML directive for declaring a vocabulary of strings.

       This schema determines the XML attributes accepted by the ZCML
       directive and how they are parsed/validated.

       Example of the directive:

         <selectorcluster                 <---- just the outer directive
             name="sitevids">

             <selectorstring
                 label="Delta Path"
                 value="/delta/"
                 />

             <selectorstring
                 label="Omega Path"
                 value="/omega/"
                 />

         </selectorcluster>
    """
    name = TextLine(title='Cluster', description='The name of this cluster for grouping labels/values.', required=True)


class ISelectorStringSubdirective(Interface):
    """Schema for the ZCML directives nested inside the top-level cluster directive.

       This schema determines the XML attributes accepted by the ZCML
       directive and how they are parsed/validated.

       Example of the directive:

         <selectorcluster
             name="sitevids">

             <selectorstring              <---- just the inner directive
                 label="Delta Path"
                 value="/delta/"
                 />

             <selectorstring
                 label="Omega Path"
                 value="/omega/"
                 />

         </selectorcluster>
    """
    label = TextLine(title='Label', description='An optional label to display to the user making the choice.', required=False)
    value = TextLine(title='Value', description='A string representing the actual value used internally.', required=True)


class IClusterOfSelectors(Interface):
    """An empty interface for tracking registered clusters in the registry.

       We tag instances of our Cluster class with this interface so we can
       retrieve them again from Zope's interface registry.  This retrieval
       also uses a name along with the interface where the name reflects the
       name of the cluster.

       Example::

         cluster = queryUtility(IClusterOfSelectors, name=clustername)
    """
    pass