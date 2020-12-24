# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.5/dist-packages/HdlLib/Utilities/PlotViewer.py
# Compiled at: 2017-07-08 08:29:58
# Size of source mod 2**32: 33533 bytes
import sys, os, shlex, logging, GraphicTools
from BugManager import BugTracking
import Threads, threading
try:
    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk, Gdk, GLib, Pango
except ImportError:
    import gtk as Gtk, glib as GLib, pango as Pango
    from gtk import gdk as Gdk

try:
    import urllib.request as UrlRequest
except ImportError:
    import urllib as UrlRequest

try:
    from matplotlib.backends.backend_gtkagg import FigureCanvasGTKAgg as FigureCanvas
    from matplotlib.backends.backend_gtkagg import NavigationToolbar2GTKAgg as NavigationToolbar
    from matplotlib.figure import Figure
    import matplotlib as pyplot
    from matplotlib.font_manager import FontProperties
except:
    logging.warning('No ploting Gtk backend. Import skipped.')

from GenericGUI import Interface
if sys.maxsize > 2 ** 32:
    ARCHI = '64'
else:
    ARCHI = '32'
if ARCHI == '32' and not sys.platform.startswith('win'):
    pass
else:
    URWPath = os.path.abspath(os.path.join(os.path.dirname(__file__), 'UniversalReadWriteStepByStep', 'results', 'windows' if sys.platform.startswith('win') else 'linux', '{0}bit'.format(ARCHI)))
    sys.path.append(URWPath)
    from bitstring import BitArray

class PlotViewer(Gtk.VBox):
    __doc__ = '\n\tGtk object to place in a container.\n\tDisplay Graph of data in AVA formatted files.\n\t'

    def __init__(self, FileDataDict={}, ValueDict={}, Layout=[], Titles={}, Interval={}, ChoosePathFunc=None, PopupFunc=None):
        """
                Initialize empty widget list, Canvas dimensions.
                """
        logging.info('Open Graph Visualizer GUI tool')
        if ChoosePathFunc:
            self.ChoosePath = ChoosePathFunc
        self.ErrorMsg = ''
        Gtk.VBox.__init__(self)
        MainPaned = Gtk.HPaned()
        self.pack_start(MainPaned, True, True, padding=5)
        Columns = {'Graph': ['GraphNb'], 
         'Name': ['Name'], 
         'Data col.': ['Data'], 
         'Validation col.': ['Valid'], 
         'Start cycle': ['Start'], 
         'End cycle': ['End'], 
         'File path': ['FilePath']}
        ColumnsOrder = [
         'Graph', 'Name', 'Data col.', 'Validation col.', 'Start cycle', 'End cycle', 'File path']
        DataTypes = {'Name': str, 
         'Data': int, 
         'Valid': int, 
         'GraphNb': int, 
         'Start': int, 
         'End': int, 
         'FilePath': str}
        DataOrder = [
         'GraphNb', 'Name', 'Data', 'Valid', 'Start', 'End', 'FilePath']
        self.DataTreeView, FrameSrc = GraphicTools.TreeView(Title='Data to visualize :', Columns=Columns, ColumnsOrder=ColumnsOrder, DataTypes=DataTypes, DataOrder=DataOrder, Headers=True, Editable={'GraphNb': [self.RowCellEdited, 'GraphNb'], 'Name': [self.RowCellEdited, 'Name'], 'Data': [self.RowCellEdited, 'Data'], 'Valid': [self.RowCellEdited, 'Valid'], 'Start': [self.RowCellEdited, 'Start'], 'End': [self.RowCellEdited, 'End']})
        MainPaned.pack1(FrameSrc, resize=True, shrink=True)
        GraphBox = Gtk.VBox()
        MainPaned.pack2(GraphBox, resize=False, shrink=True)
        S = Gtk.ScrolledWindow()
        GraphBox.pack_start(S, True, True)
        self.Figure = Figure(figsize=(5, 4), dpi=100)
        self.Canvas = FigureCanvas(self.Figure)
        S.add_with_viewport(self.Canvas)

        def SetToolBar():
            ToolBar = NavigationToolbar(self.Canvas, self.get_toplevel())
            GraphBox.pack_start(ToolBar, False, False)
            self.InitProgress()

        GLib.idle_add(SetToolBar)
        TARGET_TYPE_URI_LIST = 80
        self.DataTreeView.enable_model_drag_dest([('text/uri-list', 0, TARGET_TYPE_URI_LIST)], Gtk.gdk.ACTION_COPY)
        self.DataTreeView.connect('drag-data-received', self.TreeDragDataReceived)
        self.DataTreeView.connect('button_press_event', self.PopupHMenu)
        self.FileDataDict = FileDataDict
        self.ValueDict = ValueDict
        self.Layout = Layout
        self.Interval = Interval
        self.Titles = Titles
        self.UpdateGraph()
        self.UpdateDataTreeView()
        self.CurrentCycle = 0
        self.EndCycle = 0
        GraphBox.set_usize(600, 200)
        self.show_all()

    @BugTracking
    def UpdateGraph(self):
        """
                Display values in graph.
                """
        logging.debug('Clear figure.')
        self.Figure.clf()
        if len(self.Layout) == 0:
            self.Canvas.draw()
            return
        NbGraph = int(max([x[1] for x in self.Layout])) + 1
        self.Canvas.set_size_request(600 * NbGraph, 600)
        fontP = FontProperties()
        fontP.set_size('xx-small')
        for Name, PlotNb in self.Layout:
            if Name not in [x[0] for x in self.Layout]:
                logging.warning("Name '{0}' not in Layout ({1}).".format(Name, self.Layout))
                G = self.Figure.add_subplot(1, NbGraph, 1)
            else:
                G = self.Figure.add_subplot(1, NbGraph, PlotNb + 1)
            OldTitle = G.title.get_text()
            if PlotNb in self.Titles:
                G.title.set_text(self.Titles[PlotNb])
            G.plot(list(range(len(self.ValueDict[Name]))), self.ValueDict[Name], '-', label=Name)
            Legend = G.legend(loc=0, ncol=1, bbox_to_anchor=(0, 0, 1, 1), prop=fontP, fancybox=True, shadow=False, title='Legend')
            G.xaxis.label.set_text('Sample')
            G.yaxis.label.set_text('Value')

        self.Figure.patch.set_facecolor('#EEEEEE')
        self.Canvas.draw()

    @BugTracking
    def UpdateDataTreeView(self):
        """
                Clear and fill the Treeview with sources items.
                """
        Model = self.DataTreeView.get_model()
        Model.clear()
        for LayoutName, Graph in self.Layout:
            logging.debug("Plot name: '{0}' in graph {1}.".format(LayoutName, Graph))
            for FilePath, DataDict in self.FileDataDict.items():
                logging.debug("FilePath: '{0}'.".format(FilePath))
                logging.debug("DataDict: '{0}'.".format(DataDict))
                if LayoutName in DataDict:
                    DataValue = DataDict[LayoutName][0]
                    ValidCol = DataDict[LayoutName][1]
                    logging.debug('Add plot to treeview')
                    Parent = Model.append(None, row=(Graph, LayoutName, int(DataValue), int(ValidCol), int(self.Interval[LayoutName][0]), int(self.Interval[LayoutName][1]), FilePath))
                    break

        self.DataTreeView.expand_all()
        return False

    @BugTracking
    def RowCellEdited(self, CellRenderer, Path, Value, ColumnName):
        """
                Display values in graph.
                """
        Model = self.DataTreeView.get_model()
        TreeIter = Model.get_iter(Path)
        DataOrder = [
         'GraphNb', 'Name', 'Data', 'Valid', 'FilePath']
        if ColumnName is 'Name':
            OldValue = Model.get_value(TreeIter, DataOrder.index(ColumnName))
            if OldValue == Value:
                logging.debug('Value unchanged.')
                return False
            self.ValueDict[Value] = self.ValueDict.pop(OldValue)
            for i, (DataName, Graph) in enumerate(self.Layout):
                if DataName == OldValue:
                    self.Layout[i] = (
                     Value, Graph)

            for Path, DataDict in self.FileDataDict.items():
                if OldValue in DataDict:
                    DataDict[Value] = DataDict.pop(OldValue)

            Model.set_value(TreeIter, DataOrder.index(ColumnName), str(Value))
        else:
            if ColumnName is 'GraphNb':
                Name = Model.get_value(TreeIter, 1)
                for i in range(len(self.Layout)):
                    if self.Layout[i][0] == Name:
                        self.Layout[i] = (
                         self.Layout[i][0], int(Value))
                        break

                Model.set_value(TreeIter, DataOrder.index(ColumnName), int(Value))
            else:
                if ColumnName is 'Data':
                    Name = Model.get_value(TreeIter, 1)
                    for Path, DataDict in self.FileDataDict.items():
                        if Name in DataDict:
                            DataDict[Name] = (
                             int(Value), DataDict[Name][1])
                            self.ValueDict.update(GetDataFromFile(Path, self.FileDataDict[Path]))
                            break

                    Model.set_value(TreeIter, DataOrder.index(ColumnName), int(Value))
                else:
                    if ColumnName is 'Valid':
                        Name = Model.get_value(TreeIter, 1)
                        for Path, DataDict in self.FileDataDict.items():
                            if Name in DataDict:
                                DataDict[Name] = (
                                 DataDict[Name][0], int(Value))
                                self.ValueDict.update(GetDataFromFile(Path, self.FileDataDict[Path]))
                                break

                        Model.set_value(TreeIter, DataOrder.index(ColumnName), int(Value))
                    else:
                        if ColumnName is 'FilePath':
                            OldValue = Model.get_value(TreeIter, DataOrder.index(ColumnName))
                            if OldValue == Value:
                                logging.debug('Value unchanged.')
                                return False
                            Name = Model.get_value(TreeIter, 1)
                            for Path in list(self.FileDataDict.keys()):
                                if Name in self.FileDataDict[Path]:
                                    self.FileDataDict[Value] = self.FileDataDict.pop(OldValue)
                                    self.ValueDict.update(GetDataFromFile(Path, self.FileDataDict[Path]))
                                    break

                            Model.set_value(TreeIter, DataOrder.index(ColumnName), int(Value))
                        else:
                            if ColumnName is 'Start':
                                Name = Model.get_value(TreeIter, 1)
                                self.Interval[Name] = (int(Value), self.Interval[Name][1])
                                Model.set_value(TreeIter, DataOrder.index(ColumnName), int(Value))
                            else:
                                if ColumnName is 'End':
                                    Name = Model.get_value(TreeIter, 1)
                                    self.Interval[Name] = (self.Interval[Name][0], int(Value))
                                    Model.set_value(TreeIter, DataOrder.index(ColumnName), int(Value))
                                else:
                                    self.UpdateGraph()
                                    logging.error('Unknown column name edited: skipped.')
                                    return False
        self.UpdateGraph()
        return False

    @BugTracking
    def TreeDragDataReceived(self, TreeView, context, x, y, selection, info, timestamp):
        """
                Manage drag and drop in TreeView
                """
        logging.info('Dropped items in source treeview !')
        uri = selection.data.strip('\r\n\x00')
        URIList = uri.split()
        logging.info('Got URI : {0} !'.format(URIList))
        self.AddNewPlot(None, FilePathList=[URI2Path(URI) for URI in URIList])
        return True

    @BugTracking
    def PopupHMenu(self, TreeView, Event=None):
        """
                Callback called when the user press a button over a row check if it's the right button and emit a signal on that case
                """
        Selection = TreeView.get_selection()
        PopupMenuItems = {}
        Order = []
        if Event:
            Path = TreeView.get_path_at_pos(int(Event.x), int(Event.y))
            if Event.button == 3:
                Icon = Gtk.Image()
                Icon.set_from_stock(Gtk.STOCK_ADD, Gtk.ICON_SIZE_MENU)
                PopupMenuItems['Add plot'] = {'Icon': Icon, 'Handler': self.AddNewPlot, 'Args': []}
                Order.append('Add plot')
                if Path is not None:
                    Icon = Gtk.Image()
                    Icon.set_from_stock(Gtk.STOCK_REMOVE, Gtk.ICON_SIZE_MENU)
                    PopupMenuItems['Remove plot'] = {'Icon': Icon, 'Handler': self.RemovePlot, 'Args': [Event]}
                    Order.append('Remove plot')
        else:
            logging.warning('Special menu event not supported yet')
        if len(PopupMenuItems) > 0:
            HMenu = GraphicTools.PopupMenu(PopupMenuItems, Order)
            if Event:
                HMenu.popup(None, None, None, Event.button, Event.time)
            else:
                HMenu.popup(None, None, None, 0, 0)
            return False

    @BugTracking
    def AddNewPlot(self, MenuItem, FilePathList=[]):
        """
                Callback called when the user press a button over a row check if it's the right button and emit a signal on that case
                """
        logging.debug('MenuItem AddNewPlot clicked')
        if len(FilePathList) == 0:
            FilePathList.append(None)
        for FP in FilePathList:
            Param = self.NewPlotDialog(Parent=self.get_toplevel(), Title='Add a new plot', FilePath=FP)
            if Param is None:
                pass
            else:
                GraphNb, DataName, DataValueCol, DataValidCol, Start, End, FilePath = Param
                if FilePath in self.FileDataDict:
                    self.FileDataDict[FilePath].update({DataName: (DataValueCol, DataValidCol)})
                else:
                    self.FileDataDict[FilePath] = {DataName: (DataValueCol, DataValidCol)}
                self.Interval[DataName] = (
                 Start, End)
                self.GetDataFromFile(DataName, GraphNb, FilePath, self.FileDataDict[FilePath])

        return False

    @BugTracking
    def GetNbDataInGraph(self, GraphNb):
        """
                return number of data to be plotted in a specified graph
                """
        Cnt = 0
        for Name, Graph in self.Layout:
            if Graph == GraphNb:
                Cnt += 1

        return Cnt

    def DialogDestroyed(self, Dialog):
        """
                Hide the progress bar and stop data fetching
                """
        logging.info('End of data fetching')
        self.StopRequest.set()
        self.PGDialog.hide()

    def InitProgress(self):
        """
                Create a progress bar
                """
        self.Stop = False
        self.PGDialog = Gtk.Dialog(title='Loading data...', parent=self.get_toplevel(), flags=Gtk.DIALOG_MODAL, buttons=None)
        self.PG = Gtk.ProgressBar(adjustment=None)
        self.PG.set_orientation(Gtk.PROGRESS_LEFT_TO_RIGHT)
        self.PGDialog.action_area.pack_start(self.PG, True, True, 0)
        self.PGDialog.hide()
        self.PGDialog.connect('destroy', self.DialogDestroyed)
        self.PGDialog.connect('close', self.DialogDestroyed)
        self.PGDialog.connect('response', self.DialogDestroyed)
        self.StopRequest = threading.Event()

    def UpdateProgress(self):
        """
                Given a FilePath, retrieve data stimuli/trace vectors.
                """
        if self.EndCycle == 0:
            return
        else:
            Fraction = float(self.CurrentCycle) / float(self.EndCycle)
            self.PG.set_fraction(Fraction)
            Text = '{0}/{1} ({2}%)'.format(self.CurrentCycle, self.EndCycle, int(Fraction * 100))
            self.PG.set_text(Text)
            if self.CurrentCycle < self.EndCycle:
                self.PGDialog.show_all()
                self.get_toplevel().window.set_cursor(Gtk.gdk.Cursor(Gtk.gdk.WATCH))
                return True
            self.CurrentCycle = 0
            self.PGDialog.hide()
            self.get_toplevel().window.set_cursor(None)
            return False

    def GetDataFromFile(self, DataName, GraphNb, FilePath, DataDict, Start=0, End=-1):
        """
                Given a FilePath, retrieve data stimuli/trace vectors.
                """
        self.StopRequest.clear()
        self.Stop = False
        if End > 0:
            self.EndCycle = End - Start
        else:
            self.EndCycle = sum(1 for line in open(FilePath))

        def ExtractData():
            Values = {}
            with open(FilePath, 'r') as (DataFile):
                for Name, T in DataDict.items():
                    Values[Name] = []

                for i, Line in enumerate(DataFile.readlines()):
                    if i < Start:
                        continue
                    else:
                        if self.EndCycle is None:
                            pass
                        else:
                            if i > self.EndCycle:
                                break
                            Items = shlex.split(Line)
                            self.CurrentCycle = i - Start + 1
                            if len(Items) == 0:
                                continue
                            elif len(shlex.split(Line, comments='--')) == 0:
                                continue
                    for Name, (Data, Valid) in DataDict.items():
                        IndexMax = len(Items) - 1
                        Valid = int(Valid)
                        if Valid == -1:
                            if IndexMax < int(Data):
                                logging.warning('[{0} | Data {1}] Ignore line {2} (no enough items in line)'.format(os.path.basename(FilePath), Name, i))
                                continue
                                IsValid = True
                        if IndexMax < max(int(Data), Valid):
                            logging.warning('[{0} | Data {1}] Ignore line {2} (no enough items in line)'.format(os.path.basename(FilePath), Name, i))
                            continue
                            V = Items[Valid]
                            try:
                                Val, Base = reversed(V.split('#'))
                                IsValid = bool(int(Val, int(Base)))
                            except:
                                try:
                                    IsValid = bool(int(V))
                                except:
                                    logging.error("Syntax error. Ignored line '{0}'.".format(i))
                                    continue

                            if IsValid is True:
                                D = Items[Data]
                                try:
                                    Val, Base = reversed(D.split('#'))
                                    try:
                                        BaseInt = int(Base)
                                    except:
                                        BaseInt = 10

                                    Vint = int(Val, BaseInt)
                                    if Base is '2' and Val.startswith('1'):
                                        Vint = -(pow(2, len(Val)) - int(Val, 2) + 1)
                                        Values[Name].append(Vint)
                                        continue
                                    Values[Name].append(Vint)
                                except:
                                    try:
                                        Vint = int(D)
                                        Values[Name].append(Vint)
                                    except:
                                        logging.error("Syntax error. Ignored line '{0}'.".format(i))
                                        continue

            self.ValueDict.update(Values, Start=self.Interval[DataName][0], End=self.Interval[DataName][1])
            self.Layout.append((DataName, GraphNb))
            GLib.idle_add(self.UpdateGraph)
            GLib.idle_add(self.UpdateDataTreeView)

        def CExtractData():
            Values = {}
            IgnoredLines = []
            for Name, T in DataDict.items():
                Values[Name] = []

            NameList = URW.AdacsysOrderChemiNames()
            NameList.append(URW.AdacsysChemiName(DataName, URW.Intervalle(0, 63)))
            Src = URW.UniversalSourceAva(FilePath, NameList)
            Src.init()
            BF = URW.BitField()
            Bits = '00000000'
            BF.set(Bits, 8)
            self.CurrentCycle = 0
            self.CurrentCycle = 0
            Repetitions = 0
            logging.debug('Start fetching values')
            while Src:
                self.CurrentCycle += 1
                if self.CurrentCycle >= self.EndCycle:
                    break
                elif self.StopRequest.isSet():
                    break
                BF.setCurrentPosition(BF.LEFT)
                if not Src.exportBitField(BF, Repetitions):
                    IgnoredLines.append(self.CurrentCycle)
                    break
                else:
                    Val = ''.join([bin(ord(B))[2:] for B in Bits])
                    Val = BitArray(bin=Val)
                    Values[Name].append(Val.int)

            self.CurrentCycle = self.EndCycle
            if len(IgnoredLines):
                if len(IgnoredLines) > 5:
                    logging.debug('Unable to read lines {0}.'.format(IgnoredLines))
            else:
                logging.debug('Unable to read {0} lines.'.format(len(IgnoredLines)))
            logging.debug('End of file')
            self.ValueDict.update(Values, Start=self.Interval[DataName][0], End=self.Interval[DataName][1])
            self.Layout.append((DataName, GraphNb))
            GLib.idle_add(self.UpdateGraph)
            GLib.idle_add(self.UpdateDataTreeView)

        Threads.LaunchAsThread(Name='ExtractData', function=CExtractData, arglist=[])
        GLib.timeout_add(100, self.UpdateProgress)
        return True

    def GetDataFromAVAFiles(self, FileDataDict):
        """
                Given a Data dictionary, retrieve data stimuli/trace vectors.
                """
        Values = {}
        shlex.commenters = '//'
        for FilePath, DataDict in FileDataDict.items():
            if FilePath is None:
                pass
            else:
                Values.update(GetDataFromFile(FilePath, DataDict))

        return Values

    @BugTracking
    def RemovePlot(self, MenuItem, Event):
        """
                Event called on MenuItem clicked event.
                """
        logging.debug('MenuItem remove src clicked')
        Model, PathList = self.DataTreeView.get_selection().get_selected_rows()
        for Path in PathList:
            Iterator = Model.get_iter(Path)
            GraphNb = Model.get_value(Iterator, 0)
            DataName = Model.get_value(Iterator, 1)
            DataValueCol = Model.get_value(Iterator, 2)
            DataValidCol = Model.get_value(Iterator, 3)
            Start = Model.get_value(Iterator, 4)
            End = Model.get_value(Iterator, 5)
            FilePath = Model.get_value(Iterator, 6)
            logging.debug("Selected for removal: Graph:'{0}', DataName:'{1}', DataValueCol:'{2}', DataValidCol:'{3}', FilePath:'{4}', FilePath:'{5}', FilePath:'{6}'".format(GraphNb, DataName, DataValueCol, DataValidCol, Start, End, FilePath))
            self.FileDataDict[FilePath].pop(DataName)
            if len(self.FileDataDict[FilePath]) == 0:
                self.FileDataDict.pop(FilePath)
            self.ValueDict.pop(DataName)
            for i in range(len(self.Layout)):
                logging.debug('LAYOUT:{0}'.format(self.Layout))
                logging.debug('i:{0}'.format(i))
                logging.debug('self.Layout[i]:{0}'.format(self.Layout[i]))
                logging.debug('self.Layout[i][0]:{0}'.format(self.Layout[i][0]))
                if self.Layout[i][0] == DataName:
                    E = self.Layout.pop(i)
                    logging.debug('Pop Element {0}'.format(E))
                    break

            self.Interval.pop(DataName)

        self.UpdateGraph()
        self.UpdateDataTreeView()
        return False

    def CheckValues(self, GraphNb, DataName, DataValueCol, DataValidCol, Start, End, FilePath):
        """
                Check value
                """
        if DataName in self.ValueDict:
            Msg = 'New data name already used.'
            logging.error(Msg)
            return (
             False, Msg)
        if FilePath is None:
            Msg = 'No file path specified.'
            logging.error(Msg)
            return (
             False, Msg)
        return (True, '')

    def NewPlotDialog(self, Parent, Title, FilePath=None):
        """
                Create and return a dialog for getting information about an architecture.
                """
        D = Gtk.Dialog(Title, Parent, Gtk.DIALOG_MODAL, (Gtk.STOCK_CANCEL, Gtk.RESPONSE_CANCEL))
        D.add_button(Gtk.STOCK_OK, Gtk.RESPONSE_OK)
        DialogBox = D.get_content_area()
        DBox = Gtk.HBox()
        DialogBox.pack_start(DBox)
        A = Gtk.Adjustment(value=0, lower=0, upper=99, step_incr=1, page_incr=5, page_size=0)
        GraphSpin = Gtk.SpinButton(A, 0, 0)
        GraphSpin.set_value(0)
        GraphSpin.set_wrap(True)
        NameEntry = Gtk.Entry()
        NameEntry.set_text('DataName')
        NameEntry.set_activates_default(True)
        A = Gtk.Adjustment(value=0, lower=0, upper=99, step_incr=1, page_incr=5, page_size=0)
        DataValueSpin = Gtk.SpinButton(A, 0, 0)
        DataValueSpin.set_value(0)
        DataValueSpin.set_wrap(True)
        A = Gtk.Adjustment(value=-1, lower=-1, upper=99, step_incr=1, page_incr=5, page_size=0)
        DataValidSpin = Gtk.SpinButton(A, 0, 0)
        DataValidSpin.set_wrap(True)
        A = Gtk.Adjustment(value=0, lower=0, upper=99999999999, step_incr=1, page_incr=100, page_size=0)
        StartSpin = Gtk.SpinButton(A, 0, 0)
        StartSpin.set_wrap(True)
        A = Gtk.Adjustment(value=-1, lower=-1, upper=99999999999, step_incr=1, page_incr=100, page_size=0)
        EndSpin = Gtk.SpinButton(A, 0, 0)
        EndSpin.set_wrap(True)

        def SetDefaultDataName(*Args):
            FilePath = FilePathChooser.get_filename()
            BaseName = os.path.basename(FilePath)
            try:
                DName = BaseName[:BaseName.index('.')]
            except:
                DName = BaseName

            NameEntry.set_text(DName)

        FilePathChooser = Gtk.FileChooserButton('Choose DUT top VHDL source file', backend=None)
        FilePathChooser.connect('file-set', SetDefaultDataName)
        if FilePath is not None and os.path.isfile(FilePath):
            FilePathChooser.set_filename(FilePath)
            BaseName = os.path.basename(FilePath)
            try:
                DName = BaseName[:BaseName.index('.')]
            except:
                DName = BaseName

            NameEntry.set_text(DName)
        B = Gtk.VBox()
        B.pack_start(Gtk.Label('Graph:'), False, 0)
        B.pack_start(GraphSpin, False, False, 0)
        DBox.pack_start(B, False, False, 0)
        B = Gtk.VBox()
        B.pack_start(Gtk.Label('Data Name:'), False, 0)
        B.pack_start(NameEntry, False, 0)
        DBox.pack_start(B, False, False, 0)
        B = Gtk.VBox()
        B.pack_start(Gtk.Label('Data column:'), False, 0)
        B.pack_start(DataValueSpin, False, False, 0)
        DBox.pack_start(B, False, False, 0)
        B = Gtk.VBox()
        B.pack_start(Gtk.Label('Validation column:'), False, 0)
        B.pack_start(DataValidSpin, False, 0)
        DBox.pack_start(B, False, False, 0)
        B = Gtk.VBox()
        B.pack_start(Gtk.Label('Start cycle:'), False, 0)
        B.pack_start(StartSpin, False, 0)
        DBox.pack_start(B, False, False, 0)
        B = Gtk.VBox()
        B.pack_start(Gtk.Label('End cycle:'), False, 0)
        B.pack_start(EndSpin, False, 0)
        DBox.pack_start(B, False, False, 0)
        B = Gtk.VBox()
        B.pack_start(Gtk.Label('Source file:'), False, 0)
        B.pack_start(FilePathChooser, False, False, 0)
        DBox.pack_start(B, False, False, 0)
        D.show_all()
        D.set_default(D.action_area.get_children()[0])
        while True:
            response = D.run()
            if response == Gtk.RESPONSE_OK:
                GraphNb = int(GraphSpin.get_value())
                DataName = NameEntry.get_text()
                DataValueCol = int(DataValueSpin.get_value())
                DataValidCol = int(DataValidSpin.get_value())
                Start = int(StartSpin.get_value())
                End = int(EndSpin.get_value())
                FilePath = FilePathChooser.get_filename()
                logging.info("Add plot (Graph:'{0}', DataName:'{1}', DataValueCol:'{2}', DataValidCol:'{3}', FilePath:'{4}')".format(GraphNb, DataName, DataValueCol, DataValidCol, FilePath))
                OK, Msg = self.CheckValues(GraphNb, DataName, DataValueCol, DataValidCol, Start, End, FilePath)
                if not OK:
                    self.Popup('Value error', Msg, 'error')
                    continue
                else:
                    D.destroy()
                    return (GraphNb, DataName, DataValueCol, DataValidCol, Start, End, FilePath)
            else:
                logging.debug('Cancelled plot add.')
                break

        D.destroy()

    def Popup(self, title, text, dialog_type='info'):
        """show a dialog with title and text specified"""
        if dialog_type == 'check':
            text += "\n\nClic on 'OK' to continue"
            logging.debug('[GUI] {0}: {1}'.format(title, text))
            dialog = Gtk.MessageDialog(self.get_toplevel(), Gtk.DIALOG_MODAL, Gtk.MESSAGE_INFO, Gtk.BUTTONS_CANCEL, text)
            dialog.add_button(Gtk.STOCK_OK, Gtk.RESPONSE_OK)
        else:
            if dialog_type == 'info':
                logging.debug('[GUI] info Popup <INFO: {0}>'.format(title))
                dialog = Gtk.MessageDialog(self.get_toplevel(), Gtk.DIALOG_MODAL, Gtk.MESSAGE_INFO, Gtk.BUTTONS_OK, '\n{0}\n'.format(text))
            else:
                if dialog_type == 'result':
                    logging.debug('[GUI] result Popup :{0}'.format(text))
                    dialog = Gtk.MessageDialog(self.get_toplevel(), Gtk.DIALOG_MODAL, Gtk.MESSAGE_INFO, Gtk.BUTTONS_OK, '\n{0}\n'.format(text))
                else:
                    if dialog_type == 'warning':
                        logging.debug('[GUI] warning Popup <# WARNING: {0}>'.format(title))
                        dialog = Gtk.MessageDialog(self.get_toplevel(), Gtk.DIALOG_MODAL, Gtk.MESSAGE_WARNING, Gtk.BUTTONS_CLOSE, text)
                    else:
                        if dialog_type == 'error':
                            logging.debug('[GUI] error Popup <# ERROR: {0}>'.format(title))
                            dialog = Gtk.MessageDialog(self.get_toplevel(), Gtk.DIALOG_MODAL, Gtk.MESSAGE_ERROR, Gtk.BUTTONS_CLOSE, '\n{0}'.format(text))
                            self.ErrorMsg = self.ErrorMsg.strip()
                            if self.ErrorMsg != '':
                                if len(self.ErrorMsg) >= 3000:
                                    self.ErrorMsg = self.ErrorMsg[:3000]
                                DBox = dialog.get_content_area()
                                ExpBox = Gtk.Expander(label='More details')
                                DBox.pack_start(ExpBox, False, False)
                                TextView = Gtk.TextView()
                                TextView.set_wrap_mode(Gtk.WRAP_WORD)
                                ExpBox.add(TextView)
                                TxtBuf = TextView.get_buffer()
                                TxtBuf.insert(TxtBuf.get_end_iter(), self.ErrorMsg.replace('\x00', '').decode('utf-8', 'replace').encode('utf-8'))
                                ExpBox.set_expanded(False)
                        else:
                            if dialog_type == 'question':
                                logging.debug('[GUI] question Popup <INFO: {0}>'.format(title))
                                dialog = Gtk.MessageDialog(self.get_toplevel(), Gtk.DIALOG_MODAL, Gtk.MESSAGE_INFO, Gtk.BUTTONS_YES_NO, '\n{0}\n'.format(text))
                            else:
                                if dialog_type == 'input':
                                    logging.debug('[GUI] input Popup <{0}>'.format(title))
                                    dialog = Gtk.InputDialog(self.get_toplevel(), Gtk.DIALOG_MODAL, Gtk.MESSAGE_QUESTION, Gtk.BUTTONS_CANCEL, '\n{0}'.format(text))
                                    dialog.add_button(Gtk.STOCK_OK, Gtk.RESPONSE_OK)
                                else:
                                    dialog = Gtk.MessageDialog(self.get_toplevel(), Gtk.DIALOG_MODAL, Gtk.MESSAGE_INFO, Gtk.BUTTONS_OK, text)
        dialog.show_all()
        dialog.set_title(title)
        response = dialog.run()
        dialog.destroy()
        return response

    @BugTracking
    def ChoosePath(self, Multiple=True, Folder=False, Save=False):
        """Open a dialog to choose a directory(ies) or a file(s) (default). Return the path or the list of path if multiple selections, None if cancelling."""
        logging.debug('GUI: Open Filechooser')
        if Folder:
            filechooserdialog = Gtk.FileChooserDialog(title='Select directory', parent=self.get_toplevel(), action=Gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER, buttons=(Gtk.STOCK_CANCEL, Gtk.RESPONSE_CANCEL, Gtk.STOCK_OPEN, Gtk.RESPONSE_OK), backend=None)
        else:
            if Save:
                filechooserdialog = Gtk.FileChooserDialog(title='Save as...', parent=self.get_toplevel(), action=Gtk.FILE_CHOOSER_ACTION_SAVE, buttons=(Gtk.STOCK_CANCEL, Gtk.RESPONSE_CANCEL, Gtk.STOCK_SAVE, Gtk.RESPONSE_OK), backend=None)
            else:
                filechooserdialog = Gtk.FileChooserDialog(title='Select file', parent=self.get_toplevel(), action=Gtk.FILE_CHOOSER_ACTION_OPEN, buttons=(Gtk.STOCK_CANCEL, Gtk.RESPONSE_CANCEL, Gtk.STOCK_OPEN, Gtk.RESPONSE_OK), backend=None)
        filechooserdialog.set_select_multiple(Multiple)
        if filechooserdialog.run() == Gtk.RESPONSE_OK:
            if Multiple:
                choosen = filechooserdialog.get_filenames()
            else:
                choosen = filechooserdialog.get_filename()
            filechooserdialog.destroy()
            return choosen
        else:
            filechooserdialog.destroy()
            logging.debug('GUI: Choose file cancelled')
            return


def URI2Path(uri):
    path = ''
    if uri.startswith('file:\\\\\\'):
        path = uri[8:]
    else:
        if uri.startswith('file://'):
            path = uri[7:]
        elif uri.startswith('file:'):
            path = uri[5:]
    path = UrlRequest.url2pathname(path)
    path = path.strip('\r\n\x00')
    return path


class PlotGUI(Interface):
    __doc__ = 'This is the GUI builder for AVA GUI'

    def __init__(self, Title, Version='RD', CloseFunctions=[], ResourcesDirs=[], Width=1000, Height=500):
        Interface.__init__(self, Title=Title, CloseFunctions=CloseFunctions, ResourcesDirs=ResourcesDirs)
        self.MainWindow = Gtk.Window()
        self.MainWindow.connect('destroy', self.on_MainWindow_destroy)
        self.MainWindow.set_title(Title)
        self.MainWindow.set_icon_from_file(self.Bundle.Get('adacsys_icon.ico'))
        self.MainWindow.set_default_size(Width, Height)
        self.Visualizer = PlotViewer(FileDataDict={}, ValueDict={}, Layout=[], Titles={})
        self.MainWindow.add(self.Visualizer)
        self.MainWindow.show_all()


def StandAlone():
    """
        Display values in graph.
        """
    G = PlotGUI(Title='Adacsys Graph Visualizer', Version='RD', CloseFunctions=[], ResourcesDirs=['./GenericGUI'])
    G.Start()


if __name__ == '__main__':
    from Utilities import ConsoleInterface
    ConsoleInterface.ConfigLogging(Version='1.0', ModuleName='pySystems')
    StandAlone()