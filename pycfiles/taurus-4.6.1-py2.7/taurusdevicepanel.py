# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/taurus/qt/qtgui/panel/taurusdevicepanel.py
# Compiled at: 2019-08-19 15:09:30
"""
TaurusDevicePanel.py:
"""
from builtins import str
import re, traceback, click
from future.utils import string_types
import taurus
from taurus.external.qt import Qt
from taurus import tauruscustomsettings
from taurus.core.taurusbasetypes import TaurusDevState, TaurusElementType
from taurus.core.taurusattribute import TaurusAttribute
from taurus.core.taurusdevice import TaurusDevice
from taurus.qt.qtgui.container import TaurusWidget
from taurus.qt.qtgui.taurusgui import TaurusGui
from taurus.qt.qtgui.display import TaurusLabel
from taurus.qt.qtgui.panel.taurusform import TaurusForm
from taurus.qt.qtgui.panel.taurusform import TaurusCommandsForm
from taurus.qt.qtgui.util.ui import UILoadable
from taurus.qt.qtgui.icon import getCachedPixmap
__all__ = [
 'TaurusDevicePanel', 'TaurusDevPanel']
__docformat__ = 'restructuredtext'
STATUS_HEIGHT = 170
SPLIT_SIZES = [15, 65, 20]
IMAGE_SIZE = (200, 100)

def matchCl(m, k):
    return re.match(m.lower(), k.lower())


def searchCl(m, k):
    if m.startswith('^') or m.startswith('(^') or '(?!^' in m:
        return matchCl(m, k)
    return re.search(m.lower(), k.lower())


def get_regexp_dict(dct, key, default=None):
    for k, v in dct.items():
        if matchCl(k, key):
            return v

    for k, v in dct.items():
        if k.lower() in key.lower():
            return v

    if default is not None:
        return default
    else:
        raise Exception('KeyNotFound:%s' % key)
        return


def get_eqtype(dev):
    """ It extracts the eqtype from a device name like domain/family/eqtype-serial"""
    try:
        eq = str(dev).split('/')[(-1)].split('-', 1)[0].upper()
    except:
        eq = ''

    return eq


def str_to_filter(seq):
    try:
        f = eval(seq)
    except:
        f = seq

    if isinstance(f, string_types):
        return {'.*': [f]}
    else:
        if isinstance(f, list):
            return {'.*': f}
        return f


def get_White_palette():
    palette = Qt.QPalette()
    brush = Qt.QBrush(Qt.QColor(255, 255, 255))
    brush.setStyle(Qt.Qt.SolidPattern)
    palette.setBrush(Qt.QPalette.Active, Qt.QPalette.Base, brush)
    brush = Qt.QBrush(Qt.QColor(255, 255, 255))
    brush.setStyle(Qt.Qt.SolidPattern)
    palette.setBrush(Qt.QPalette.Active, Qt.QPalette.Window, brush)
    brush = Qt.QBrush(Qt.QColor(255, 255, 255))
    brush.setStyle(Qt.Qt.SolidPattern)
    palette.setBrush(Qt.QPalette.Inactive, Qt.QPalette.Base, brush)
    brush = Qt.QBrush(Qt.QColor(255, 255, 255))
    brush.setStyle(Qt.Qt.SolidPattern)
    palette.setBrush(Qt.QPalette.Inactive, Qt.QPalette.Window, brush)
    brush = Qt.QBrush(Qt.QColor(255, 255, 255))
    brush.setStyle(Qt.Qt.SolidPattern)
    palette.setBrush(Qt.QPalette.Disabled, Qt.QPalette.Base, brush)
    brush = Qt.QBrush(Qt.QColor(255, 255, 255))
    brush.setStyle(Qt.Qt.SolidPattern)
    palette.setBrush(Qt.QPalette.Disabled, Qt.QPalette.Window, brush)
    return palette


class TaurusDevicePanel(TaurusWidget):
    """
    TaurusDevPanel is a Taurus Application inspired in Jive and Atk Panel.

    It Provides a Device selector and a panel for displaying information from
    the selected device.
    """
    READ_ONLY = False
    _attribute_filter = {}
    _command_filter = {}
    _icon_map = {}

    @classmethod
    def setIconMap(klass, filters):
        """A dictionary like {device_regexp:pixmap_url}"""
        klass._icon_map = filters

    @classmethod
    def getIconMap(klass):
        return klass._icon_map

    @classmethod
    def setAttributeFilters(klass, filters):
        """
        It will set the attribute filters
        filters will be like: {device_regexp:[attribute_regexps]}
        example: {'.*/VGCT-.*': ['ChannelState','p[0-9]']}
        """
        klass._attribute_filter.update(filters)

    @classmethod
    def getAttributeFilters(klass):
        return klass._attribute_filter

    @classmethod
    def setCommandFilters(klass, filters):
        """
        It will set the command filters
        filters will be like: {device_regexp:[command_regexps]}
        example::

          {'.*/IPCT-.*': (
                           ('setmode',('SERIAL','LOCAL','STEP','FIXED','START','PROTECT')),
                           ('onhv1',()), ('offhv1',()), ('onhv2',()), ('offhv2',()),
                           ('sendcommand',())
                         ),}

        """
        klass._command_filter.update(filters)

    @classmethod
    def getCommandFilters(klass):
        return klass._command_filter

    def __init__(self, parent=None, model=None, palette=None, bound=True):
        TaurusWidget.__init__(self, parent)
        if palette:
            self.setPalette(palette)
        self.setLayout(Qt.QGridLayout())
        self.bound = bound
        self._dups = []
        self.setWindowTitle('TaurusDevicePanel')
        self._label = Qt.QLabel()
        self._label.font().setBold(True)
        self._stateframe = TaurusWidget(self)
        self._stateframe.setLayout(Qt.QGridLayout())
        self._stateframe.layout().addWidget(Qt.QLabel('State'), 0, 0, Qt.Qt.AlignCenter)
        self._statelabel = TaurusLabel(self._stateframe)
        self._statelabel.setMinimumWidth(100)
        self._statelabel.setBgRole('rvalue')
        self._stateframe.layout().addWidget(self._statelabel, 0, 1, Qt.Qt.AlignCenter)
        self._statusframe = Qt.QScrollArea(self)
        self._status = TaurusLabel(self._statusframe)
        self._status.setBgRole('none')
        self._status.setAlignment(Qt.Qt.AlignLeft)
        self._status.setFixedHeight(2000)
        self._status.setFixedWidth(5000)
        self._statusframe.setHorizontalScrollBarPolicy(Qt.Qt.ScrollBarAlwaysOn)
        self._statusframe.setVerticalScrollBarPolicy(Qt.Qt.ScrollBarAlwaysOn)
        self._statusframe.setWidget(self._status)
        self._statusframe.setPalette(get_White_palette())
        self._attrsframe = Qt.QTabWidget(self)
        self._splitter = Qt.QSplitter(Qt.Qt.Vertical, self)
        self._attrs, self._comms = (None, None)
        self.layout().addWidget(self._splitter, 0, 0)
        self._header = Qt.QFrame()
        self._header.setFixedHeight(1.1 * IMAGE_SIZE[1])
        self._header.setLayout(Qt.QGridLayout())
        self._dup = Qt.QPushButton()
        qpixmap = Qt.QIcon('actions:window-new.svg')
        self._dup.setIcon(Qt.QIcon(qpixmap))
        self._dup.setIconSize(Qt.QSize(15, 15))
        self._dup.pressed.connect(self.duplicate)
        self._image = Qt.QLabel()
        self._header.layout().addWidget(self._image, 0, 0, 2, 1, Qt.Qt.AlignCenter)
        self._header.layout().addWidget(self._label, 0, 1, Qt.Qt.AlignLeft)
        self._header.layout().addWidget(self._stateframe, 1, 1, 1, 2, Qt.Qt.AlignLeft)
        self._header.layout().addWidget(self._dup, 0, 2, Qt.Qt.AlignRight)
        self._splitter.insertWidget(0, self._header)
        self._splitter.insertWidget(1, self._attrsframe)
        self._splitter.insertWidget(2, self._statusframe)
        self._splitter.setSizes(SPLIT_SIZES)
        [ self._splitter.setStretchFactor(i, v) for i, v in enumerate(SPLIT_SIZES)
        ]
        self._splitter.setCollapsible(0, False)
        self._splitter.setCollapsible(1, False)
        if model:
            self.setModel(model)
        return

    def loadConfigFile(self, ifile=None):
        self.debug('In TaurusDevicePanel.loadConfigFile(%s)' % ifile)
        if isinstance(ifile, string_types) and ifile.endswith('.py'):
            from imp import load_source
            config_file = load_source('config_file', ifile)
            af, cf, im = [ getattr(config_file, x, None) for x in ('AttributeFilters',
                                                                   'CommandFilters',
                                                                   'IconMap')
                         ]
            if af is not None:
                self.setAttributeFilters(af)
            if cf is not None:
                self.setCommandFilters(cf)
            if im is not None:
                self.setIconMap(im)
        else:
            TaurusWidget.loadConfigFile(self, ifile)
        self.debug('AttributeFilters are:\n%s' % self.getAttributeFilters())
        return

    def duplicate(self):
        self._dups.append(TaurusDevicePanel(bound=False))
        self._dups[(-1)].setModel(self.getModel())
        self._dups[(-1)].show()

    @Qt.pyqtSlot('QString')
    def setModel(self, model, pixmap=None):
        model, modelclass, raw = str(model).strip(), '', model
        if model:
            model = model and model.split()[0] or ''
            modelclass = taurus.Factory().findObjectClass(model)
        self.trace('In TaurusDevicePanel.setModel(%s(%s),%s)' % (
         raw, modelclass, pixmap))
        if model == self.getModel():
            return
        else:
            if raw is None or not model or not modelclass:
                if self.getModel():
                    self.detach()
                return
            if issubclass(modelclass, TaurusAttribute):
                model = model.rsplit('/', 1)[0]
            elif not issubclass(modelclass, TaurusDevice):
                self.warning('TaurusDevicePanel accepts only Device models')
                return
            try:
                taurus.Device(model).ping()
                if self.getModel():
                    self.detach()
                TaurusWidget.setModel(self, model)
                model_obj = self.getModelObj()
                simple_name = model_obj.getSimpleName().upper()
                self.setWindowTitle(simple_name)
                model = self.getModel()
                self._label.setToolTip(model_obj.getFullName().upper())
                self._label.setText(simple_name)
                font = self._label.font()
                font.setPointSize(15)
                self._label.setFont(font)
                if pixmap is None and self.getIconMap():
                    for k, v in self.getIconMap().items():
                        if searchCl(k, model):
                            pixmap = v

                if pixmap is not None:
                    qpixmap = Qt.QPixmap(pixmap)
                    if qpixmap.height() > 0.9 * IMAGE_SIZE[1]:
                        qpixmap = qpixmap.scaledToHeight(0.9 * IMAGE_SIZE[1])
                    if qpixmap.width() > 0.9 * IMAGE_SIZE[0]:
                        qpixmap = qpixmap.scaledToWidth(0.9 * IMAGE_SIZE[0])
                else:
                    logo = getattr(tauruscustomsettings, 'ORGANIZATION_LOGO', 'logos:taurus.png')
                    qpixmap = getCachedPixmap(logo)
                self._image.setPixmap(qpixmap)
                if hasattr(self, '_statelabel'):
                    self._statelabel.setModel(model + '/state')
                self._status.setModel(model + '/status')
                try:
                    self._attrsframe.clear()
                    filters = get_regexp_dict(TaurusDevicePanel._attribute_filter, model, ['.*'])
                    if hasattr(filters, 'keys'):
                        filters = list(filters.items())
                    if filters and isinstance(filters[0], (list, tuple)):
                        self._attrs = []
                        for tab, attrs in filters:
                            self._attrs.append(self.get_attrs_form(device=model, filters=attrs, parent=self))
                            self._attrsframe.addTab(self._attrs[(-1)], tab)

                    else:
                        if self._attrs and isinstance(self._attrs, list):
                            self._attrs = self._attrs[0]
                        self._attrs = self.get_attrs_form(device=model, form=self._attrs, filters=filters, parent=self)
                        if self._attrs:
                            self._attrsframe.addTab(self._attrs, 'Attributes')
                    if not TaurusDevicePanel.READ_ONLY:
                        self._comms = self.get_comms_form(model, self._comms, self)
                        if self._comms:
                            self._attrsframe.addTab(self._comms, 'Commands')
                    if SPLIT_SIZES:
                        self._splitter.setSizes(SPLIT_SIZES)
                except:
                    self.warning(traceback.format_exc())
                    qmsg = Qt.QMessageBox(Qt.QMessageBox.Critical, '%s Error' % model, '%s not available' % model, Qt.QMessageBox.Ok, self)
                    qmsg.setDetailedText(traceback.format_exc())
                    qmsg.show()

            except:
                self.warning(traceback.format_exc())
                qmsg = Qt.QMessageBox(Qt.QMessageBox.Critical, '%s Error' % model, '%s not available' % model, Qt.QMessageBox.Ok, self)
                qmsg.show()

            return

    def detach(self):
        self.trace('In TaurusDevicePanel(%s).detach()' % self.getModel())
        _detached = []
        import taurus.qt.qtgui.container, taurus.qt.qtgui.base

        def detach_recursive(obj):
            if obj in _detached:
                return
            else:
                if isinstance(obj, taurus.qt.qtgui.container.TaurusBaseContainer):
                    for t in obj.taurusChildren():
                        detach_recursive(t)

                if obj is not self and isinstance(obj, taurus.qt.qtgui.base.TaurusBaseWidget):
                    try:
                        if getattr(obj, 'model', None):
                            obj.setModel([] if isinstance(obj, TaurusForm) else '')
                    except:
                        self.warning('detach of %s failed!' % obj)
                        self.warning(traceback.format_exc())

                _detached.append(obj)
                return

        detach_recursive(self)
        try:
            self._label.setText('')
            self._label.setToolTip('')
            if hasattr(self, '_statelabel'):
                self._statelabel.setModel('')
            self._status.setModel('')
            self._image.setPixmap(Qt.QPixmap())
        except:
            self.warning(traceback.format_exc())

    def get_attrs_form(self, device, form=None, filters=None, parent=None):
        filters = filters or get_regexp_dict(TaurusDevicePanel._attribute_filter, device, ['.*'])
        self.trace('In TaurusDevicePanel.get_attrs_form(%s,%s)' % (
         device, filters))
        allattrs = sorted(str(a) for a in taurus.Device(device).get_attribute_list() if str(a).lower() not in ('state',
                                                                                                               'status'))
        attrs = []
        for a in filters:
            for t in allattrs:
                if a and searchCl(a.strip(), t.strip()):
                    aname = '%s/%s' % (device, t)
                    if aname not in attrs:
                        attrs.append(aname)

        if attrs:
            if form is None:
                form = TaurusForm(parent)
            else:
                if hasattr(form, 'setModel'):
                    form.setModel([])
                form.setWithButtons(False)
                form.setWindowTitle(device)
                try:
                    form.setModel(attrs)
                except Exception:
                    self.warning('TaurusDevicePanel.ERROR: Unable to setModel for TaurusDevicePanel.attrs_form!!: %s' % traceback.format_exc())

            return form
        return
        return

    def get_comms_form(self, device, form=None, parent=None):
        self.trace('In TaurusDevicePanel.get_comms_form(%s)' % device)
        params = get_regexp_dict(TaurusDevicePanel._command_filter, device, [])
        if TaurusDevicePanel._command_filter and not params:
            self.debug('TaurusDevicePanel.get_comms_form(%s): By default an unknown device type will display no commands' % device)
            return None
        else:
            if not form:
                form = TaurusCommandsForm(parent)
            else:
                if hasattr(form, 'setModel'):
                    form.setModel('')
                try:
                    form.setModel(device)
                    if params:
                        form.setSortKey(lambda x, vals=[ s[0].lower() for s in params ]: vals.index(x.cmd_name.lower()) if str(x.cmd_name).lower() in vals else 100)
                        form.setViewFilters([
                         lambda c: str(c.cmd_name).lower() not in ('state', 'status') and any(searchCl(s[0], str(c.cmd_name)) for s in params)])
                        form.setDefaultParameters(dict((k, v) for k, v in (params if not hasattr(params, 'items') else list(params.items())) if v))
                    for wid in form._cmdWidgets:
                        if not hasattr(wid, 'getCommand') or not hasattr(wid, 'setDangerMessage'):
                            continue
                        if re.match('.*(on|off|init|open|close).*', str(wid.getCommand().lower())):
                            wid.setDangerMessage('This action may affect other systems!')

                    form._splitter.setSizes([80, 20])
                except Exception:
                    self.warning('Unable to setModel for TaurusDevicePanel.comms_form!!: %s' % traceback.format_exc())

            return form


def filterNonExported(obj):
    from taurus.core.tango.tangodatabase import TangoDevInfo
    if not isinstance(obj, TangoDevInfo) or obj.exported():
        return obj
    return


@UILoadable(with_ui='_ui')
class TaurusDevPanel(TaurusGui):
    """
    TaurusDevPanel is a Taurus Application inspired in Jive and Atk Panel.

    It Provides a Device selector and several dockWidgets for interacting and
    displaying information from the selected device.
    """
    HELP_MENU_ENABLED = False

    def __init__(self, parent=None, designMode=False):
        TaurusGui.__init__(self, parent)
        self.loadUi()
        import taurus.qt.qtgui.tree
        TaurusDbTreeWidget = taurus.qt.qtgui.tree.TaurusDbTreeWidget
        self.deviceTree = TaurusDbTreeWidget(perspective=TaurusElementType.Device)
        self.deviceTree.getQModel().setSelectables([
         TaurusElementType.Member])
        self.setCentralWidget(self.deviceTree)
        self.registerConfigDelegate(self._ui.taurusCommandsForm)
        self.loadSettings()
        self.createActions()
        self.deviceTree.currentItemChanged.connect(self.onItemSelectionChanged)
        self.updatePerspectivesMenu()
        if not designMode:
            self.splashScreen().finish(self)

    def createActions(self):
        """create actions"""
        self.showAttrAction = self.viewMenu.addAction(self._ui.attrDW.toggleViewAction())
        self.showCommandsAction = self.viewMenu.addAction(self._ui.commandsDW.toggleViewAction())

    def setTangoHost(self, host):
        """extended from :class:setTangoHost"""
        TaurusGui.setTangoHost(self, host)
        self.deviceTree.setModel(host)

    def onItemSelectionChanged(self, current, previous):
        itemData = current.itemData()
        from taurus.core.tango.tangodatabase import TangoDevInfo
        if isinstance(itemData, TangoDevInfo):
            self.onDeviceSelected(itemData)

    def onDeviceSelected(self, devinfo):
        devname = devinfo.name()
        msg = 'Connecting to "%s"...' % devname
        self.statusBar().showMessage(msg)
        if not devinfo.exported():
            msg = 'Connection to "%s" failed (not exported)' % devname
            self.statusBar().showMessage(msg)
            self.info(msg)
            Qt.QMessageBox.warning(self, 'Device unreachable', msg)
            self.setModel('')
            return
        self.setDevice(devname)

    def setDevice(self, devname):
        """set the device to be shown by the commands and attr forms"""
        self.setModel(devname)
        self._ui.attrDW.setWindowTitle('Attributes - %s' % devname)
        self._ui.commandsDW.setWindowTitle('Commands - %s' % devname)

    def setModel(self, name):
        """Reimplemented to delegate model to the commands and attrs forms"""
        TaurusGui.setModel(self, name)
        self._ui.taurusAttrForm.setModel(name)
        self._ui.taurusCommandsForm.setModel(name)

    @classmethod
    def getQtDesignerPluginInfo(cls):
        ret = TaurusGui.getQtDesignerPluginInfo()
        ret['module'] = 'taurus.qt.qtgui.panel'
        return ret


@click.command('device')
@click.argument('dev', nargs=1, default=None, required=False)
@click.option('-f', '--filter', help='regexp to filter for attributes to show ' + '(it can be passed more than once)', multiple=True)
@click.option('--config', 'config_file', type=click.File('rb'), help='configuration file for initialization')
def device_cmd(dev, filter, config_file):
    """Show a Device Panel"""
    import sys
    from taurus.qt.qtgui.application import TaurusApplication
    app = TaurusApplication(cmd_line_parser=None, app_name='TaurusDevicePanel')
    w = TaurusDevicePanel()
    w.show()
    if dev is None:
        from taurus.qt.qtgui.panel import TaurusModelChooser
        models, ok = TaurusModelChooser.modelChooserDlg(w, selectables=[TaurusElementType.Member], singleModel=True)
        dev = models[0] if ok and models else None
    if config_file is not None:
        w.loadConfigFile(config_file)
    elif dev and filter:
        w.setAttributeFilters({dev: list(filter)})
    w.setModel(dev)
    sys.exit(app.exec_())
    return


@click.command('panel')
@click.option('--tango-host', 'tango_host', default=None, help="Tango Host name (the system's default if not given)")
@click.option('-d', '--dev', default=None, help='pre-selected device')
@click.option('-t', '--trend', is_flag=True, help='Create a temporal trend widget')
def panel_cmd(tango_host, dev, trend):
    """
    Show a TaurusPanel (a Taurus application inspired in Jive and Atk Panel)
    """
    from taurus.qt.qtgui.application import TaurusApplication
    import sys
    app = TaurusApplication(cmd_line_parser=None, app_name='tauruspanel')
    w = TaurusDevPanel()
    if tango_host is None:
        from taurus import Factory
        tango_host = Factory('tango').getAuthority().getFullName()
    w.setTangoHost(tango_host)
    if dev is not None:
        w.setDevice(dev)
    if trend is True:
        try:
            from taurus.qt.qtgui.qwt5 import TaurusTrend
            w.info('Using qwt5 back-end')
        except:
            try:
                from taurus.qt.qtgui.tpg import TaurusTrend
                w.info('Using tpg back-end')
            except:
                TaurusTrend = None
                w.warning('TaurusTrend widget is not available')

        if TaurusTrend is not None:
            plot = TaurusTrend()
            w.createPanel(plot, 'TaurusTrend', permanent=False)
    w.show()
    sys.exit(app.exec_())
    return