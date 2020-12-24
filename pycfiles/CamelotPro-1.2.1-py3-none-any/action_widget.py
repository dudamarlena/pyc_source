# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/camelot/view/controls/action_widget.py
# Compiled at: 2013-04-11 17:47:52
__doc__ = '\nCreated on May 22, 2010\n\n@author: tw55413\n'
from PyQt4 import QtGui
from PyQt4 import QtCore
from camelot.admin.action.form_action import FormActionGuiContext
from camelot.view.model_thread import post

class AbstractActionWidget(object):

    def __init__(self, action, gui_context):
        """Helper class to construct widget that when triggered run an action.
        This class exists as a base class for custom ActionButton implementations.
        """
        from camelot.admin.action import State
        self.action = action
        self.gui_context = gui_context
        self.state = State()
        if isinstance(gui_context, FormActionGuiContext):
            gui_context.widget_mapper.model().dataChanged.connect(self.data_changed)
            gui_context.widget_mapper.currentIndexChanged.connect(self.current_row_changed)
        post(action.get_state, self.set_state, args=(self.gui_context.create_model_context(),))

    def set_state(self, state):
        self.state = state
        self.setEnabled(state.enabled)
        self.setVisible(state.visible)

    def current_row_changed(self, current_row):
        post(self.action.get_state, self.set_state, args=(
         self.gui_context.create_model_context(),))

    def data_changed(self, index1, index2):
        self.current_row_changed(index1.row())

    def run_action(self, mode=None):
        gui_context = self.gui_context.copy()
        gui_context.mode_name = mode
        self.action.gui_run(gui_context)

    def set_menu(self, state):
        """This method creates a menu for an object with as its menu items
        the different modes in which an action can be triggered.
        
        :param state: a `camelot.admin.action.State` object
        """
        if state.modes:
            menu = QtGui.QMenu()
            for mode in state.modes:
                mode_action = mode.render(menu)
                mode_action.triggered.connect(self.triggered)
                menu.addAction(mode_action)

            self.setMenu(menu)


HOVER_ANIMATION_DISTANCE = 20
NOTIFICATION_ANIMATION_DISTANCE = 8

class ActionLabel(QtGui.QLabel, AbstractActionWidget):
    entered = QtCore.pyqtSignal()
    left = QtCore.pyqtSignal()

    def __init__(self, action, gui_context, parent):
        QtGui.QLabel.__init__(self, parent)
        AbstractActionWidget.__init__(self, action, gui_context)
        self.setObjectName('ActionButton')
        self.setMouseTracking(True)
        self.interactive = False
        self.originalPosition = None
        self.selectionAnimationState = QtCore.QAbstractAnimation.Stopped
        self.setMaximumHeight(160)
        opacityEffect = QtGui.QGraphicsOpacityEffect(parent=self)
        opacityEffect.setOpacity(1.0)
        self.setGraphicsEffect(opacityEffect)
        hoverAnimationPart1 = QtCore.QPropertyAnimation(self, 'pos')
        hoverAnimationPart1.setObjectName('hoverAnimationPart1')
        hoverAnimationPart1.setDuration(500)
        hoverAnimationPart1.setEasingCurve(QtCore.QEasingCurve.Linear)
        hoverAnimationPart2 = QtCore.QPropertyAnimation(self, 'pos')
        hoverAnimationPart2.setObjectName('hoverAnimationPart2')
        hoverAnimationPart2.setDuration(1500)
        hoverAnimationPart2.setEasingCurve(QtCore.QEasingCurve.OutElastic)
        hoverAnimation = QtCore.QSequentialAnimationGroup(parent=self)
        hoverAnimation.setObjectName('hoverAnimation')
        hoverAnimation.setLoopCount(-1)
        hoverAnimation.addAnimation(hoverAnimationPart1)
        hoverAnimation.addAnimation(hoverAnimationPart2)
        selectionAnimationPart1 = QtCore.QPropertyAnimation(self, 'pos')
        selectionAnimationPart1.setObjectName('selectionAnimationPart1')
        selectionAnimationPart1.setDuration(200)
        selectionAnimationPart1.setEasingCurve(QtCore.QEasingCurve.Linear)
        selectionAnimationPart2 = QtCore.QPropertyAnimation(self, 'size')
        selectionAnimationPart2.setObjectName('selectionAnimationPart2')
        selectionAnimationPart2.setDuration(200)
        selectionAnimationPart2.setEasingCurve(QtCore.QEasingCurve.OutCubic)
        selectionAnimationPart3 = QtCore.QPropertyAnimation(self.graphicsEffect(), 'opacity')
        selectionAnimationPart3.setObjectName('selectionAnimationPart3')
        selectionAnimationPart3.setDuration(200)
        selectionAnimationPart3.setEasingCurve(QtCore.QEasingCurve.Linear)
        selectionAnimation = QtCore.QParallelAnimationGroup(parent=self)
        selectionAnimation.setObjectName('selectionAnimation')
        selectionAnimation.addAnimation(selectionAnimationPart1)
        selectionAnimation.addAnimation(selectionAnimationPart2)
        selectionAnimation.addAnimation(selectionAnimationPart3)
        selectionAnimation.stateChanged.connect(self.updateSelectionAnimationState)
        return

    def set_state(self, state):
        AbstractActionWidget.set_state(self, state)
        if state.icon:
            self.setPixmap(state.icon.getQPixmap())
            self.resize(self.pixmap().width(), self.pixmap().height())
        if state.notification:
            notificationAnimationPart1 = QtCore.QPropertyAnimation(self, 'pos')
            notificationAnimationPart1.setObjectName('notificationAnimationPart1')
            notificationAnimationPart1.setDuration(50)
            notificationAnimationPart1.setEasingCurve(QtCore.QEasingCurve.Linear)
            notificationAnimationPart2 = QtCore.QPropertyAnimation(self, 'pos')
            notificationAnimationPart2.setObjectName('notificationAnimationPart2')
            notificationAnimationPart2.setDuration(50)
            notificationAnimationPart2.setEasingCurve(QtCore.QEasingCurve.Linear)
            notificationAnimationPart3 = QtCore.QPropertyAnimation(self, 'pos')
            notificationAnimationPart3.setObjectName('notificationAnimationPart3')
            notificationAnimationPart3.setDuration(50)
            notificationAnimationPart3.setEasingCurve(QtCore.QEasingCurve.Linear)
            notificationAnimation = QtCore.QSequentialAnimationGroup(parent=self)
            notificationAnimation.setObjectName('notificationAnimation')
            notificationAnimation.setLoopCount(10)
            notificationAnimation.addAnimation(notificationAnimationPart1)
            notificationAnimation.addAnimation(notificationAnimationPart2)
            notificationAnimation.addAnimation(notificationAnimationPart3)
            notificationAnimationTimer = QtCore.QTimer(parent=self)
            notificationAnimationTimer.setObjectName('notificationAnimationTimer')
            notificationAnimationTimer.setInterval(1500)
            notificationAnimationTimer.setSingleShot(True)
            notificationAnimationTimer.timeout.connect(notificationAnimation.start)
            notificationAnimation.finished.connect(notificationAnimationTimer.start)
        self.resetLayout()

    def startHoverAnimation(self):
        hoverAnimationPart1 = self.findChild(QtCore.QPropertyAnimation, 'hoverAnimationPart1')
        if hoverAnimationPart1 is not None:
            hoverAnimationPart1.setStartValue(self.originalPosition)
            hoverAnimationPart1.setEndValue(self.originalPosition + QtCore.QPoint(0, -HOVER_ANIMATION_DISTANCE))
        hoverAnimationPart2 = self.findChild(QtCore.QPropertyAnimation, 'hoverAnimationPart2')
        if hoverAnimationPart2 is not None:
            hoverAnimationPart2.setStartValue(self.originalPosition + QtCore.QPoint(0, -HOVER_ANIMATION_DISTANCE))
            hoverAnimationPart2.setEndValue(self.originalPosition)
        hoverAnimation = self.findChild(QtCore.QSequentialAnimationGroup, 'hoverAnimation')
        if hoverAnimation is not None:
            hoverAnimation.start()
        return

    def stopHoverAnimation(self):
        hoverAnimation = self.findChild(QtCore.QSequentialAnimationGroup, 'hoverAnimation')
        if hoverAnimation is not None:
            hoverAnimation.stop()
        if self.originalPosition is not None:
            self.move(self.originalPosition)
        self.resetLayout()
        return

    def startSelectionAnimation(self):
        if self.state.notification:
            notificationAnimation = self.findChild(QtCore.QSequentialAnimationGroup, 'notificationAnimation')
            if notificationAnimation is not None:
                notificationAnimation.stop()
        else:
            hoverAnimation = self.findChild(QtCore.QSequentialAnimationGroup, 'hoverAnimation')
            if hoverAnimation is not None:
                hoverAnimation.stop()
        self.move(self.originalPosition)
        selectionAnimationPart1 = self.findChild(QtCore.QPropertyAnimation, 'selectionAnimationPart1')
        selectionAnimationPart2 = self.findChild(QtCore.QPropertyAnimation, 'selectionAnimationPart2')
        selectionAnimationPart3 = self.findChild(QtCore.QPropertyAnimation, 'selectionAnimationPart3')
        selectionAnimation = self.findChild(QtCore.QParallelAnimationGroup, 'selectionAnimation')
        if None not in (selectionAnimationPart1, selectionAnimationPart2,
         selectionAnimationPart3, selectionAnimation):
            selectionAnimationPart1.setStartValue(self.originalPosition)
            selectionAnimationPart1.setEndValue(self.originalPosition + QtCore.QPoint(-HOVER_ANIMATION_DISTANCE, -HOVER_ANIMATION_DISTANCE))
            selectionAnimationPart2.setStartValue(self.size())
            selectionAnimationPart2.setEndValue(self.size() + QtCore.QSize(40, 40))
            selectionAnimationPart3.setStartValue(1.0)
            selectionAnimationPart3.setEndValue(0.1)
            self.setScaledContents(True)
            selectionAnimation.start()
        return

    def updateSelectionAnimationState(self, newState, oldState):
        self.selectionAnimationState = newState
        if oldState == QtCore.QAbstractAnimation.Running and newState == QtCore.QAbstractAnimation.Stopped:
            self.run_action()
            self.resetLayout()

    def resetLayout(self):
        if self.state.notification:
            self.stopNotificationAnimation()
        if self.sender() and self.originalPosition:
            self.move(self.originalPosition)
        self.setScaledContents(False)
        if self.pixmap():
            self.resize(self.pixmap().width(), self.pixmap().height())
        self.graphicsEffect().setOpacity(1.0)
        if self.state.notification and self.originalPosition:
            self.startNotificationAnimation()

    def setInteractive(self, interactive):
        self.interactive = interactive
        self.originalPosition = self.mapToParent(QtCore.QPoint(0, 0))
        if self.state.notification:
            self.startNotificationAnimation()

    def enterEvent(self, event):
        if self.interactive:
            if self.state.notification:
                self.stopNotificationAnimation()
            self.startHoverAnimation()
            self.entered.emit()
        event.ignore()

    def leaveEvent(self, event):
        if self.interactive:
            self.stopHoverAnimation()
            if self.state.notification:
                self.startNotificationAnimation()
            self.left.emit()
        event.ignore()

    def onContainerMousePressEvent(self, event):
        if self.interactive and self.selectionAnimationState == QtCore.QAbstractAnimation.Stopped:
            self.startSelectionAnimation()
        event.ignore()

    def startNotificationAnimation(self):
        notificationAnimationPart1 = self.findChild(QtCore.QPropertyAnimation, 'notificationAnimationPart1')
        if notificationAnimationPart1 is not None:
            notificationAnimationPart1.setStartValue(self.originalPosition)
            notificationAnimationPart1.setEndValue(self.originalPosition + QtCore.QPoint(-NOTIFICATION_ANIMATION_DISTANCE, 0))
        notificationAnimationPart2 = self.findChild(QtCore.QPropertyAnimation, 'notificationAnimationPart2')
        if notificationAnimationPart2 is not None:
            notificationAnimationPart2.setStartValue(self.originalPosition + QtCore.QPoint(-NOTIFICATION_ANIMATION_DISTANCE, 0))
            notificationAnimationPart2.setEndValue(self.originalPosition + QtCore.QPoint(NOTIFICATION_ANIMATION_DISTANCE, 0))
        notificationAnimationPart3 = self.findChild(QtCore.QPropertyAnimation, 'notificationAnimationPart3')
        if notificationAnimationPart3 is not None:
            notificationAnimationPart3.setStartValue(self.originalPosition + QtCore.QPoint(NOTIFICATION_ANIMATION_DISTANCE, 0))
            notificationAnimationPart3.setEndValue(self.originalPosition)
        notificationAnimation = self.findChild(QtCore.QSequentialAnimationGroup, 'notificationAnimation')
        notificationAnimationTimer = self.findChild(QtCore.QTimer, 'notificationAnimationTimer')
        if notificationAnimation is not None and notificationAnimationTimer is not None:
            notificationAnimationTimer.start()
            notificationAnimation.start()
        return

    def stopNotificationAnimation(self):
        notificationAnimation = self.findChild(QtCore.QSequentialAnimationGroup, 'notificationAnimation')
        notificationAnimationTimer = self.findChild(QtCore.QTimer, 'notificationAnimationTimer')
        if notificationAnimation is not None and notificationAnimationTimer is not None:
            notificationAnimationTimer.stop()
            notificationAnimation.stop()
        return


class ActionAction(QtGui.QAction, AbstractActionWidget):

    def __init__(self, action, gui_context, parent):
        QtGui.QAction.__init__(self, parent)
        AbstractActionWidget.__init__(self, action, gui_context)
        if action.shortcut != None:
            self.setShortcut(action.shortcut)
        return

    @QtCore.pyqtSlot(object)
    def set_state(self, state):
        if state.verbose_name != None:
            self.setText(unicode(state.verbose_name))
        else:
            self.setText('')
        if state.icon != None:
            self.setIcon(state.icon.getQIcon())
        else:
            self.setIcon(QtGui.QIcon())
        if state.tooltip != None:
            self.setToolTip(unicode(state.tooltip))
        else:
            self.setToolTip('')
        self.setEnabled(state.enabled)
        self.setVisible(state.visible)
        self.set_menu(state)
        return


class ActionPushButton(QtGui.QPushButton, AbstractActionWidget):

    def __init__(self, action, gui_context, parent):
        """A :class:`QtGui.QPushButton` that when pressed, will run an 
        action.
        
        .. image:: /_static/actionwidgets/action_push_botton_application_enabled.png
        
        """
        QtGui.QPushButton.__init__(self, parent)
        AbstractActionWidget.__init__(self, action, gui_context)
        self.clicked.connect(self.triggered)

    @QtCore.pyqtSlot()
    def triggered(self):
        sender = self.sender()
        mode = None
        if isinstance(sender, QtGui.QAction):
            mode = unicode(sender.data().toString())
        self.run_action(mode)
        return

    @QtCore.pyqtSlot(QtCore.QModelIndex, QtCore.QModelIndex)
    def data_changed(self, index1, index2):
        AbstractActionWidget.data_changed(self, index1, index2)

    def set_state(self, state):
        super(ActionPushButton, self).set_state(state)
        if state.verbose_name != None:
            self.setText(unicode(state.verbose_name))
        if state.icon != None:
            self.setIcon(state.icon.getQIcon())
        else:
            self.setIcon(QtGui.QIcon())
        self.set_menu(state)
        return