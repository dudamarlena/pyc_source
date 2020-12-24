# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/qtalchemy/foreign_key.py
# Compiled at: 2014-02-03 14:10:41
from PySide import QtCore, QtGui
from sqlalchemy.orm import mapper, create_session, relation, object_session, Query
from .user_attr import UserAttr
from .PyQtModels import QueryTableModel, attrReadonly
from .input_yoke import InputYoke
from qtalchemy.widgets import PBKeyEdit

class PopupKeyListing(PBKeyEdit):

    def __init__(self, parent, Session, foreignAttr):
        PBKeyEdit.__init__(self, parent)
        self.Session = Session
        self.foreignAttr = foreignAttr
        self.popupList = None
        self.textEdited.connect(self.refinePopup)
        self.buttonPressed.connect(self.search)
        self._initPopup()
        return

    def _initPopup(self):
        if self.popupList is not None:
            return
        else:
            self.popupList = QtGui.QListView()
            self.popupList.setParent(None, QtCore.Qt.Popup)
            self.popupList.setFocusPolicy(QtCore.Qt.NoFocus)
            self.popupList.setFocusProxy(self)
            self.popupList.installEventFilter(self)
            self.popupList.clicked.connect(self.modelSelection)
            self.popupList.activated.connect(self.modelSelection)
            self.query = self.foreignAttr.getSelection()
            self.popupModel = QueryTableModel(self.query, ['name'])
            self.popupList.setModel(self.popupModel)
            return

    def shutdown(self, obj):
        if self.popupList is not None:
            self.popupList.hide()
            self.popupList.close()
            self.popupList = None
        return

    def event(self, e):
        if e.type() in [QtCore.QEvent.Hide]:
            self.shutdown(self)
        return PBKeyEdit.event(self, e)

    def eventFilter(self, o, e):
        if o is not self.popupList:
            return PBKeyEdit.eventFilter(self, o, e)
        if e.type() == QtCore.QEvent.KeyPress:
            if e.key() == QtCore.Qt.Key_Escape:
                self.popupList.hide()
                return True
            self.event(e)
            if e.isAccepted():
                return True
        if e.type() == QtCore.QEvent.MouseButtonPress:
            if self.popupList.isVisible() and not self.popupList.underMouse():
                self.popupList.hide()
        return False

    def modelSelection(self, index):
        self.setText(index.internalPointer().name)
        self.popupList.hide()

    def refinePopup(self, text):
        q = self.query.filter(self.foreignAttr.keyCol().ilike(('{0}%').format(text.replace('%', '%%'))))
        session = self.Session()
        q.session = session
        keys = q.limit(10).all()
        session.close()
        if len(keys) > 0:
            self.popupModel.reset_content_from_list(keys)
            rect = self.rect()
            self.popupList.move(self.mapToGlobal(rect.bottomLeft()))
            self.popupList.show()
            self.setFocus(QtCore.Qt.PopupFocusReason)
        else:
            self.popupList.hide()

    def search(self):
        self.foreignAttr.search(self, self.row)


class ForeignKeyReferral(UserAttr):
    """
    A ForeignKeyReferralEx UserAttr provides a display for a user-centric key 
    matching back to a database foreign key which is not expected to be 
    user-friendly.  This also wraps in the ability for search method which is 
    expected to display a dialog with a list of entities which can be chosen 
    in this attribute.

    :param atype:  python type of displayed key
    :param label:  widget label for UI
    :param backref:  python attribute name in the ModelObject holding the referred key object
    :param class_:  python class of referred key object
    :param userkey:  python attribute name of class_ to display or callable taking parameter of type class_
    :param entity:  The domain entity class this foreign key represents a member of.
    """

    def __init__(self, atype, label, backref, class_, userkey, entity=None, filter_query=None, readonly=False):
        self.backref = backref
        self.class_ = class_
        self.userkey = userkey
        self.filter_query = filter_query
        self.entityCls = entity
        UserAttr.__init__(self, atype, label, readonly=readonly)
        self.proxies = {}

    def fget(self, row):
        target = getattr(row, self.backref)
        if target is None:
            return
        else:
            if callable(self.userkey):
                return self.userkey(target)
            else:
                return getattr(target, self.userkey)

            return

    def fset(self, row, value):
        if value is None:
            setattr(row, self.backref, None)
            return
        else:
            s = self.session(row)
            try:
                setattr(row, self.backref, s.query(self.class_).filter(getattr(self.class_, self.userkey).ilike(value)).one())
            except Exception as e:
                setattr(row, self.backref, None)

            return

    def keyCol(self):
        return getattr(self.class_, self.userkey)

    def getSelection(self):
        q = Query((self.keyCol().label('name'),))
        if self.filter_query:
            q = self.filter_query(q)
        return q

    def yoke_specifier(self):
        if self.entityCls is None:
            return 'foreign_key_combo'
        else:
            return 'foreign_key'
            return

    def WidgetFactory(self, parent, index):
        if self.entityCls is not None:
            w = PopupKeyListing(parent, None, self)
            w.model_index = index
        else:
            w = QtGui.QComboBox(parent)
            w.setEditable(True)
        return w

    def WidgetBind(self, widget, row):
        Session = self.session_maker(row)
        if isinstance(widget, PopupKeyListing):
            widget.Session = Session
            widget.row = row
        if isinstance(widget, QtGui.QComboBox):
            col_model = QueryTableModel(self.getSelection(), ssrc=Session)
            col_model.reset_content_from_session()
            widget.setModel(col_model)

    def search(self, widget, row):
        Session = self.session_maker(row)
        index = None
        parent = None
        try:
            index = widget.model_index
            parent = widget.parent()
        except:
            pass

        from .PBSearchDialog import PBSearchDialog
        srch = PBSearchDialog(Session, self.entityCls, widget.parent())
        srch.setWindowModality(QtCore.Qt.ApplicationModal)
        srch.show()
        srch.exec_()
        result = srch.selectedItem(self.class_, self.session(row))
        if result is not None:
            if index is not None:
                index.model().ensureNoFlipper(index)
            setattr(row, self.backref, result)
            if index is None:
                widget.setText(self.fget(row))
            else:
                parent.setFocus()
        return


class ForeignKeyEditYoke(InputYoke):

    def __init__(self, mapper, attr):
        InputYoke.__init__(self, mapper)
        self.attr = attr
        mapper.reverse_yoke(attr, self)

    def Factory(self):
        self.widget = PBKeyEdit()
        self._baseAdoptWidget(self.widget)
        self.widget.editingFinished.connect(self.Save)
        self.widget.buttonPressed.connect(self.Search)
        if attrReadonly(self.mapper.cls, self.attr):
            self.widget.setReadOnly(True)
        return self.widget

    def AdoptWidget(self, widget):
        self.widget = widget
        self._baseAdoptWidget(self.widget)
        self.widget.editingFinished.connect(self.Save)
        self.widget.buttonPressed.connect(self.Search)
        if attrReadonly(self.mapper.cls, self.attr):
            self.widget.setReadOnly(True)

    def Search(self):
        user_attr = getattr(self.mapper.cls, self.attr)
        row = self.mapper.obj
        Session = user_attr.session_maker(row)
        index = None
        parent = None
        try:
            index = self.widget.model_index
            parent = self.widget.parent()
        except:
            pass

        from . import PBSearchDialog
        srch = PBSearchDialog(Session, user_attr.entityCls, self.widget.parent())
        srch.setWindowModality(QtCore.Qt.ApplicationModal)
        srch.show()
        srch.exec_()
        result = srch.selectedItem(user_attr.class_, user_attr.session(row))
        if result is not None:
            setattr(row, user_attr.backref, result)
            if index is None:
                self.widget.setText(user_attr.fget(row))
            else:
                parent.setFocus()
        return

    def Bind(self):
        user_attr = getattr(self.mapper.cls, self.attr)
        Session = user_attr.session_maker(self.mapper.obj)
        col_model = QueryTableModel(user_attr.getSelection(), ssrc=Session)
        col_model.setParent(self.widget)
        col_model.reset_content_from_session()
        col_completer = QtGui.QCompleter(self.widget)
        col_completer.setCompletionMode(QtGui.QCompleter.InlineCompletion)
        col_completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.widget.setCompleter(col_completer)
        col_completer.setModel(col_model)
        if isinstance(self.widget, QtGui.QLineEdit):
            self.widget.setText(self.mapper.getObjectAttr(self.attr))
        else:
            self.widget.setEditText(self.mapper.getObjectAttr(self.attr))

    def Save(self):
        if attrReadonly(self.mapper.cls, self.attr):
            return
        if isinstance(self.widget, QtGui.QLineEdit):
            self.mapper.setObjectAttr(self.attr, self.widget.text())
        else:
            self.mapper.setObjectAttr(self.attr, self.widget.currentText())


class ForeignKeyComboYoke(InputYoke):

    def __init__(self, mapper, attr):
        InputYoke.__init__(self, mapper)
        self.attr = attr
        mapper.reverse_yoke(attr, self)

    def Factory(self):
        self.widget = QtGui.QComboBox()
        self._baseAdoptWidget(self.widget)
        self.widget.setEditable(True)
        return self.widget

    def AdoptWidget(self, widget):
        self.widget = widget
        self._baseAdoptWidget(self.widget)
        self.widget.setEditable(True)
        if hasattr(self.widget, 'setReadOnly') and attrReadonly(self.mapper.cls, self.attr):
            self.widget.setReadOnly(True)
        return self.widget

    def Bind(self):
        user_attr = getattr(self.mapper.cls, self.attr)
        Session = user_attr.session_maker(self.mapper.obj)
        col_model = QueryTableModel(user_attr.getSelection(), ssrc=Session)
        col_model.reset_content_from_session()
        self.widget.setModel(col_model)
        self.widget.setEditText(self.mapper.getObjectAttr(self.attr))

    def Save(self):
        if attrReadonly(self.mapper.cls, self.attr):
            return
        self.mapper.setObjectAttr(self.attr, self.widget.currentText())


class ForeignKeyValidator(QtGui.QValidator):

    def __init__(self, parent=None, fk=None, session=None):
        QtGui.QValidator.__init__(self, parent)
        self.fkr = fk
        self.session = session

    def fixup(self, input):
        like_me = self.session.query(self.fkr.header_name).filter(self.fkr.header_name.ilike(str(input))).all()
        if len(like_me) == 1:
            input.replace(0, 6, QtCore.QString(like_me[0].vid))

    def validate(self, input, pos):
        try:
            like_me = self.session.query(self.fkr.header_name).filter(self.fkr.header_name.ilike(str(input))).one()
            input.replace(0, 6, QtCore.QString(like_me[0].vid))
            return (QtGui.QValidator.Acceptable, pos)
        except:
            return (
             QtGui.QValidator.Intermediate, pos)