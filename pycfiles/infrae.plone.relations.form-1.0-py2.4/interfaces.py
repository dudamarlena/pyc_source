# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.freebsd-7.0-STABLE-i386/egg/infrae/plone/relations/form/interfaces.py
# Compiled at: 2008-06-12 04:00:15
__author__ = 'sylvain@infrae.com'
__format__ = 'plaintext'
__version__ = '$Id: interfaces.py 29119 2008-06-11 10:34:14Z sylvain $'
from zope.app.form.interfaces import IInputWidget, IDisplayWidget
from zope.interface import Interface, Attribute
from zope.i18nmessageid import MessageFactory
_ = MessageFactory('plone')

class IPloneRelationDisplayWidget(IDisplayWidget):
    """A widget to display plone relation.
    """
    __module__ = __name__


class IPloneRelationObjectIdManager(Interface):
    """Manage object's id.
    """
    __module__ = __name__

    def getObjectFromId(id):
        """With the given id, return object.
        """
        pass

    def getIdFromObject(self, obj):
        """With the object, return object.
        """
        pass


class IPloneRelationEditWidget(IInputWidget):
    """A widget to edit plone relation.
    """
    __module__ = __name__
    plone = Attribute(_('Plone site context'))
    field = Attribute(_('Field being rendered'))


class IPloneRelationEditWidgetView(Interface):
    """Helper view for edit widget.
    """
    __module__ = __name__
    plone = Attribute(_('Plone site context.'))
    add_widget = Attribute(_('Widget used to add new values'))
    add_widget_args = Attribute(_('Options for add widget'))
    edit_context = Attribute(_('Widget to edit context'))

    def getName():
        """Return the name of the widget.
        """
        pass

    def getPloneContext():
        """Like plone property, but for page template as you can't
           acces property in a Zope 2 page template...
        """
        pass

    def getRelationCount():
        """Return the number of relation in the widget.
        """
        pass

    def getRelationToRender():
        """Return the relation data to render.
        """
        pass

    def canAddValues():
        """Return true if the user is allowed to add new values.
        """
        pass

    def hasValue(value):
        """Check if value is already in the relation.
        """
        pass

    def relationIsUnique():
        """Return true if the relation must contains simple items.
        """
        pass

    def relationUseContext():
        """Return true if the relation use context items.
        """
        pass

    def relationAsOneItem():
        """Return true if the relation as only one item for the
           moment.
        """
        pass

    def renderEditContext():
        """Render a box to edit context of a relation.
        """
        pass

    def renderAddWidget():
        """Render the add widget.
        """
        pass


class IPloneRelationSubWidget(Interface):
    """Base interface for plone relation sub widget.
    """
    __module__ = __name__

    def hasInput():
        """Return true if the widget have input (after being called).
        """
        pass

    def getInputValue():
        """Return input value.
        """
        pass


class IPloneRelationEditContext(IPloneRelationSubWidget):
    """Subwidget to edit context on a relation.
    """
    __module__ = __name__
    context_schema = Attribute(_('Schema of the object'))
    context_factory = Attribute(_('Factory for new context object'))

    def setPrefix(uid):
        """Set a prefix for field (to prevent collision).
        """
        pass

    def setRenderedValue(obj):
        """Set the object to render.
        """
        pass

    def applyChanges(obj):
        """Apply changes on given object.
        """
        pass

    def error():
        """Return the error on the widget.
        """
        pass


class IPloneRelationAddWidget(IPloneRelationSubWidget):
    """Subwidget to add new relation. This is build using a
       IPloneRelationEditWidgetView as context.
    """
    __module__ = __name__