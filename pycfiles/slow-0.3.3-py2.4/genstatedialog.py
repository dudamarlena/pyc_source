# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/slow/qtgui/genstatedialog.py
# Compiled at: 2006-01-31 15:27:33
import sys
from qt import *
from custom_widgets import IterableComboBox as QComboBox
image0_data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10\x00\x00\x00\x10\x08\x06\x00\x00\x00\x1f\xf3\xffa\x00\x00\x02\xe6IDAT8\x8du\x92Kh\\U\x18\xc7\x7f\xf79wfn\xae\xd3:Mb\xaeLZM\x14\x14m\xd0H\x15\x9f)RHWbE\xac\x88\xb4"\x14DQT\x04\xb1\x15\x17\x8a\x8a\x96.b)\xbap\xe1Bj\xa8\xa9\xad\xc4\x9a\x9a\xb6\x93\xaa\xe0"\xd6\xd0\x12\n\x13\xd3\x84<\x9cI&\xf3\xc8dfr3\xf7q\\\xa4\x13Zm~\xf0\xad\xce\xf9~\xe7;\xffs$\xae\xe1\x85S\xd5\xb6yC\xfeD^\xf1\x9d\\\xff\xb7/\xb5l{\xe6\x15\xd7\xf5G~\xda\x1bO\xb2\x0e\x12\xc0\x9eA\xa79\xf0\xc5\xab\x9e+\x8a\'\r\xe33\x12\x82\xd6\xf4J\xaed(7)5_\xb5\x93\x97\x9e\xfa\xfd\xc0\xb6\x13\xeb\n\xbaO\xaf\x1c\x1bJh\xbb\x9aK>\x931\x05k\xb4\x849WA\xd6\x14\xbc\x96(\xe6\xb2_m\xc8\xd6~a\xc9\xb9\xf2\xe7\xdb\x897\xff\'\xe8<R\x1b\x1b6\xb56:\xc0\x1e\x9ceS\xb1\x84$\x05\xab\x1bd\x99\xd0F\x8b\xf1\x8eF\xd4\x7f\xaa\x84\xfb\xbe\xdb>~t\xdf\xb9\xba@\xde\xfdc\xe5\xc1Dc\xcd\xb0\xa2\x01j\xc1gSei\xba\xb6\xf8\xd7{\xce\xc2\xf0\x8b\x92\x9a;\x14\xbeE\xcf\xa9f\xc0\xd6\xa9\x02\x86\xae\xa24\xde\xf3\xd0uw\xe8:\xbe|\x8c\xf3Bp^\x08m\xc0\x13\xed{\xfb>\x00\xf4\xfa\xfa}\x1f~o\xef\x18H\xff\xd1\x9d\xcc\x8b\xee3Ua\xf6V\x84\xfd\xd1\xecD\xfc\xb1\x03\x16\x80\xbc</\xe2\xfc\rd\xc1\x15\nr\xfb\xddO\x00^]pa\xff\xaeYYwvFo\x8d\xcemh\xd2\x10\xb10\xf9xl\xb3\xde\xd8\xf9\x1c\x80\xac\xcaA\xc6\x9a\xf1QF\x05T`\xbe\xb5\xf5\xf1G>O\xbds\xed\x94?wm\xc9\xabQ\xfd\x0b\xddP\x91\x1c\t\xf3\xf2Tj\xee\xd4j\x0e\xb2\x19\xe4\xde\xbf\xab:\xf0r\xfb\x86R\x96\n\x14\xa4\x10cM\xad\x1f\xef\xf8&\xdb\xf3\xec\xf1\xa5x]\xa2;Lf3P.C\xc5n\xbe#\xf6t\xff\xee\xb5W\xe8\xea\xc9\x983z$=\xa65\x98\xf5\x06\x03\xc1\xeda\xcf\xbb9"\x8dh\xba\xe2\x15]\xa9\xe3b\x1e\xc3\x15\x80\x02f\xf2\xc2\xaf\xe5\xaf\xef\xdf\xa9\x02\x04\xbexr\xce6L\x8a@\x040\xc0\xc9H\x8c\x164\x95\x02\x9d\xd7\xa5\xde\x02\xda\xc2"L\\\x1a\x02j2\x80\xef\x8bA;]LY\xcd\x0e[\xa6\xa6\xa7-\xb9\nw\x02\xe2j\xdd\xb6\xda\x88\x80hr\x96P\xdf\xd9#\xe5s{z\xd6\x04\xbf\xbd\xd5R\xd6S\x13\xdb\xed\xde3\xefN\xbc\x91x\xb8\xe9\x87\x91}f\xa6\x02\x12\xa8n\x8d\x88S\x84\xad\x02l\xf0\xb4`\xb96>\xd0\x0b\xcc\xdf\xe0g\xaf\xd2\xf6ZjsC\xff\xa2\xe0J 6\xeeOM\xc5\x1e=\xf8|\xe4\xab\xb4\x17:<\xe3\x84\x1f8\xf8:\xb0\x96\x95z#\x81\xef\x05\x0b\r\'/\x7f\xa9\x0f\x85\xeeu\xcf\x1e=T\x1a\xfe\xf4\x84eu\x94\xdd\xd1\xc3\xf9\x95\xc9\xbe\x8b@y\xdd\xd3\xffC\xe8j\xad\xcb\xbfY\xcc1\xcf\x1e\x17`)\x00\x00\x00\x00IEND\xaeB`\x82'
image1_data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10\x00\x00\x00\x10\x08\x06\x00\x00\x00\x1f\xf3\xffa\x00\x00\x02\x17IDAT8\x8d\xa5\x93\xbfK\x1cA\x18\x86\x9f\x99\xdd\xbb]\xcd\x9d$9\x04QH\x0c\x1c\xa8\xd8\xd8&m M8\x08\x81\xe0\x1f\x91\xc6\xb3Laaa{\xfe\x01vvi\x85X\x98\x88\xd7\xe4\x8c\x86\xfc@P\xd2$\x06\x84\x95\x80\x845\xba\xee\xee\xec\xce\x97\xe2r\xa7\xe7\xd9\xe5mf\x18\xe6}\xe6\xfb\xe6\x9dQ\x8dFC\xf8\x0f\xb9\x00ssslo\x0b"\x821\n\xd7\x85\xbd=a\x7f\x1f\xd2\x14\x8c\xd1}\xc6\x95\x15X^^n\x03\x00\xa6\xa7\x05\x11\x85H{\x9c\x98\x00c\x04\xa5\x04\x91\x1c\xa5\xdasc\x84<\x17`\xe0\xb2\x02\x80r\xb9s\x8a"\xb7\x16\x80\xcc\n\xd6dD\x91%M-\xc7\xc7\x96rY\x18\x1e\xbf\xd5\xdb\xc2M:\x0eR\x0e\x0erNO\xc1\xf7]<\xafH\x18\x1a\xa6\xa6\x12l\x1cC\xa9\x04@_s&\xcb\xf8\xfc\xe9\x82\xcd\xcd\x0c\x11ar\x12D\x0cQ\xa4)\x14\x0ccc\x0e\xc9\xf9yw\x7f\x0f \xb7\x96\xaf_\x12Z-\x87j\x15\x1e=\x1e\xe4\xde\x03M\x9ajNN\x84\x91\x11K\xeah\xd4\x15O\x0f\xe0\xc7\xf7\x84f\xd3\xa1R\xc9\x99\x99q\xd1@pd8:rI\x12\xc3\xe8(\xd84\xc5q\x9c~@b-\xbb\xbbB\x18\x16\xa8VA{ER`g\x07\x0e\x0f]\xac\xcd(\r\x0f\x82\xd6\xa0.k\xe8^\xe2\x9d\x0f\x0e\x8c\x03\xe3\xf0TB\xfe\x84!\xcd\r\xcd\xd6\xdb2\xe2h*\x15\xc3\xc7\xa6%\x08,\xcf\x9e\xfb7\xa7\xb0V]\xa0\xb6\xba\xc8\xda\xcf"\x8e\x9batFA\t\nh\xbd\x1b\xe0\xf6\xdd\x98\'5\xcbY\x12S*\xb5\xa3T\x03\xef\x91\xeb\x80\x8e\xbe\xbd\x08y\xf3Z\xa3\x95\xc3\xfd\x89\x0b~\x9fm\xf4$\x16\x04A\x1b\xb0V]\xb8\x9e&\xb5\xd5E~\xbd\x8c\xc9\x93\x84\xa2\xefs\x1a\xc7l\xad\xaf3;;\x0b\xb4\x9fq\xbd^/\xba\xb4\xa0\xd6Z\x84\x87\xfd\x15\xb8"\xb8\x9e\x87\x02t\x92t\xd7\xff\x99\x15\x80^\xd2\r\xa2\xf9\xde\x0f\x19\xcd\x0b\xd1\xbc\xe0\xfb>\xbe\xe7\xe1\x15\x8b\x0c\r\r\xf5\x99\x01T\xe7;\xbf\xb2\xf5.`I7\xfaZ\xea\xe8\xaa\x19\xe0/\xeb\xd0\xf5!5?\x01a\x00\x00\x00\x00IEND\xaeB`\x82'
image2_data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10\x00\x00\x00\x10\x08\x06\x00\x00\x00\x1f\xf3\xffa\x00\x00\x02yIDAT8\x8dm\x93\xb1K\x1ba\x18\xc6\x7f\xdf\xddw\x97\xe4P\xab\xd4j\xee\xaaqpPT\xaa$\xfe\r\x0en\x0e\x82\x83Pt\xb0Rts\xeb\xa0\xe0\xe0\x1f\x10:\x14\\2\xeb\xaaH\nM\xf7Vt\xa8\xa8\x88\x83\x04\x15\xc5\xf3\xaaF\x13/\xb9\xbb\x0e\x97\xa8\x91\xbe\xf0\xf0\xbd\xbc|\xcf\xc3\xfb\xbe\x0f\xafH&\x93\xbc\x8c\x0c\xf4\n\x98\xf0\x00\x0f\xf0_\xbc\x7fa\xfd\x0b\xec\x01A\xed\xbfx)\x90\x81\xde\x88a\xe4\xac\xf1\xf1\xb8P\xd5:\xe1\x8a\xe7q\xb0\xb6v\xf5\xe7\xe1a\xf4+\xfc\xae\x89\xc8:r,\x96\xebZ\\\x8c\xeb\xfd\xfd\xfc/\x06\xfb\xfaZ+KK\x9b\x9f\x8a\xc5\xd1oU\x11\xd54\xcd\x90\x1c\x89\xe4\xba\xe6\xe7\xe3zg\'\xb8.\xdc\xdc@\xa1\xf0\x8cR\t\x19\x8d\xf2\xae\xbb\xdbx\xdc\xde\x1e\xeb\xf0\xbc\xdc\x0e\x9c\xabY\xd3\xec\x8d\xe8z\xaekr2\xae\xb7\xb7C[\x1b\xf4\xf4@>\x0f\x17\x17pw\x07\x91\x08\x0c\x0e\xc2\xed-\xf2\xfe\x9e\xb6D\xc2(\xed\xed\x8d\xbd\xf7\xbc\x9c\x02LX\x03\x03q]\xd3\xe0\xf2\x12\x12\tPUH\xa5 \x08B\xa4Ra-\x91\xc0?>F\x1e\x1d\xf1\xe1\xcd\x9bV\x03\xa6\xa5\x07\x88B\x01NO\xc3AWWaj\n\x1a\x1bad$\xacII`\xdb<\xce\xcf\xe3\x1f\x1e\x86\xdb\x07\\\xd0\x14\x1f\xe0\xf66l9\x9f\x87\xdd]XY\tw\xa0\xeb\xa0\xeb\x04\xb6Mif\xe6\x89L\xd5\x02\x1f\x90^M\xc0u\x9f\xd7\xdd\xd2\x12\xce]\x8bX\x0c\xa5\xb9\x19\xef\x95+>\x10v\xf0\xf0@\xe08!\x12\tX^\x86h\x94\xc0\xb6\tl\x1ba\x18\xe8\xe94\xfa\xd0\x10\xb2\xea\xbd\xac\tx\x00\x8a\x02B@c#"\x9d\x06\xc3\x80\xebk\x98\x9d\rq}\x8d0\x0cd:\x8d\xd6\xd4\x84\xa6(\x04\x8a\x12\n\xdc\xc0\xfa\x1e\\\x95\x1b\x1a\x10\xaa\n\x99\x0c8\x0e,, \x1c\x07Q\xcdq\x1c\xc8d\x10\xaaJ\xa9\xa1\x81\x9f\xe0\xecCV$\x93I\xf1\x19\x86\xfb4m3eY\xad\xba\x94\x10\x8dB\xa9T?p\xb5V\xacT\xd8:;s6\xca\xe5\xb9\x1d\xc8\xaa\xa6i\xf2\x0b\xce;|?\xe7>>\x8e\xc5-\xcb\x90\xd1(\xc4b\xf5\xd04\x8a\xaa\xca\xd6\xc9\x89\xb3\xe1\xbas;\x90\x05l\xd54M\x00\xb6\xe1\xdc\xaaTr\xa5Ba\xec\xade\x19\x9e\xaeS\x96\x92\xb2\x94\xb8RR\x14\x82\xef\xfb\xfb\xceF\xb1\xf8D\x06\x02\xf1\xea\x9c\xc5G\x186`\xda\x05\xcd\xaf\xfa];\xe7\x03\xc8n\xc3\x8f\x1a\x19\xe0\x1f\x17&\x01\xbe\xf9\x92P\x85\x00\x00\x00\x00IEND\xaeB`\x82'

class EDSMStateDialog(QDialog):
    __module__ = __name__

    def __init__(self, parent=None, name=None, modal=0, fl=0):
        QDialog.__init__(self, parent, name, modal, fl)
        self.image0 = QPixmap()
        self.image0.loadFromData(image0_data, 'PNG')
        self.image1 = QPixmap()
        self.image1.loadFromData(image1_data, 'PNG')
        self.image2 = QPixmap()
        self.image2.loadFromData(image2_data, 'PNG')
        if not name:
            self.setName('EDSMStateDialog')
        self.setSizePolicy(QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred, 0, 0, self.sizePolicy().hasHeightForWidth()))
        self.setIcon(self.image0)
        EDSMStateDialogLayout = QGridLayout(self, 1, 1, 11, 6, 'EDSMStateDialogLayout')
        self.object_name = QLineEdit(self, 'object_name')
        EDSMStateDialogLayout.addWidget(self.object_name, 0, 1)
        self.object_name_textlabel = QLabel(self, 'object_name_textlabel')
        EDSMStateDialogLayout.addWidget(self.object_name_textlabel, 0, 0)
        self.groupBox5 = QGroupBox(self, 'groupBox5')
        self.groupBox5.setColumnLayout(0, Qt.Vertical)
        self.groupBox5.layout().setSpacing(6)
        self.groupBox5.layout().setMargin(11)
        groupBox5Layout = QGridLayout(self.groupBox5.layout())
        groupBox5Layout.setAlignment(Qt.AlignTop)
        self.class_name = QComboBox(0, self.groupBox5, 'class_name')
        self.class_name.setEditable(1)
        self.class_name.setInsertionPolicy(QComboBox.NoInsertion)
        self.class_name.setAutoCompletion(1)
        self.class_name.setDuplicatesEnabled(0)
        groupBox5Layout.addWidget(self.class_name, 0, 1)
        self.language_name = QComboBox(0, self.groupBox5, 'language_name')
        groupBox5Layout.addWidget(self.language_name, 1, 1)
        self.init_code = QTextEdit(self.groupBox5, 'init_code')
        init_code_font = QFont(self.init_code.font())
        init_code_font.setFamily('Monospace')
        init_code_font.setPointSize(8)
        self.init_code.setFont(init_code_font)
        groupBox5Layout.addWidget(self.init_code, 2, 1)
        self.class_name_textlabel = QLabel(self.groupBox5, 'class_name_textlabel')
        groupBox5Layout.addWidget(self.class_name_textlabel, 0, 0)
        self.language_name_textlabel = QLabel(self.groupBox5, 'language_name_textlabel')
        groupBox5Layout.addWidget(self.language_name_textlabel, 1, 0)
        self.init_code_textlabel = QLabel(self.groupBox5, 'init_code_textlabel')
        groupBox5Layout.addWidget(self.init_code_textlabel, 2, 0)
        EDSMStateDialogLayout.addMultiCellWidget(self.groupBox5, 2, 2, 0, 1)
        self.groupBox4 = QGroupBox(self, 'groupBox4')
        self.groupBox4.setSizePolicy(QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed, 0, 0, self.groupBox4.sizePolicy().hasHeightForWidth()))
        self.groupBox4.setColumnLayout(0, Qt.Vertical)
        self.groupBox4.layout().setSpacing(6)
        self.groupBox4.layout().setMargin(11)
        groupBox4Layout = QGridLayout(self.groupBox4.layout())
        groupBox4Layout.setAlignment(Qt.AlignTop)
        self.output_queues = QListBox(self.groupBox4, 'output_queues')
        groupBox4Layout.addWidget(self.output_queues, 1, 1)
        self.output_queues_textlabel = QFrame(self.groupBox4, 'output_queues_textlabel')
        self.output_queues_textlabel.setFrameShape(QFrame.StyledPanel)
        self.output_queues_textlabel.setFrameShadow(QFrame.Raised)
        self.output_queues_textlabel.setLineWidth(0)
        output_queues_textlabelLayout = QGridLayout(self.output_queues_textlabel, 1, 1, 0, 3, 'output_queues_textlabelLayout')
        self.add_output_queue_button = QPushButton(self.output_queues_textlabel, 'add_output_queue_button')
        self.add_output_queue_button.setEnabled(0)
        self.add_output_queue_button.setSizePolicy(QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum, 0, 0, self.add_output_queue_button.sizePolicy().hasHeightForWidth()))
        self.add_output_queue_button.setPixmap(self.image1)
        output_queues_textlabelLayout.addWidget(self.add_output_queue_button, 0, 1)
        self.remove_output_queue_button = QPushButton(self.output_queues_textlabel, 'remove_output_queue_button')
        self.remove_output_queue_button.setEnabled(0)
        self.remove_output_queue_button.setPixmap(self.image2)
        output_queues_textlabelLayout.addWidget(self.remove_output_queue_button, 1, 1)
        self.output_queues_label = QLabel(self.output_queues_textlabel, 'output_queues_label')
        self.output_queues_label.setLineWidth(0)
        self.output_queues_label.setMargin(0)
        output_queues_textlabelLayout.addMultiCellWidget(self.output_queues_label, 0, 1, 0, 0)
        groupBox4Layout.addWidget(self.output_queues_textlabel, 1, 0)
        self.input_queues_textlabel = QFrame(self.groupBox4, 'input_queues_textlabel')
        self.input_queues_textlabel.setFrameShape(QFrame.StyledPanel)
        self.input_queues_textlabel.setFrameShadow(QFrame.Raised)
        self.input_queues_textlabel.setLineWidth(0)
        input_queues_textlabelLayout = QGridLayout(self.input_queues_textlabel, 1, 1, 0, 3, 'input_queues_textlabelLayout')
        self.add_input_queue_button = QPushButton(self.input_queues_textlabel, 'add_input_queue_button')
        self.add_input_queue_button.setEnabled(0)
        self.add_input_queue_button.setSizePolicy(QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum, 0, 0, self.add_input_queue_button.sizePolicy().hasHeightForWidth()))
        self.add_input_queue_button.setPixmap(self.image1)
        input_queues_textlabelLayout.addWidget(self.add_input_queue_button, 0, 1)
        self.remove_input_queue_button = QPushButton(self.input_queues_textlabel, 'remove_input_queue_button')
        self.remove_input_queue_button.setEnabled(0)
        self.remove_input_queue_button.setPixmap(self.image2)
        input_queues_textlabelLayout.addWidget(self.remove_input_queue_button, 1, 1)
        self.input_queues_label = QLabel(self.input_queues_textlabel, 'input_queues_label')
        self.input_queues_label.setLineWidth(0)
        self.input_queues_label.setMargin(0)
        input_queues_textlabelLayout.addMultiCellWidget(self.input_queues_label, 0, 1, 0, 0)
        groupBox4Layout.addWidget(self.input_queues_textlabel, 1, 2)
        self.input_queues = QListBox(self.groupBox4, 'input_queues')
        groupBox4Layout.addWidget(self.input_queues, 1, 3)
        self.queue_name = QLineEdit(self.groupBox4, 'queue_name')
        groupBox4Layout.addMultiCellWidget(self.queue_name, 0, 0, 1, 3)
        self.queue_name_textlabel = QLabel(self.groupBox4, 'queue_name_textlabel')
        groupBox4Layout.addWidget(self.queue_name_textlabel, 0, 0)
        EDSMStateDialogLayout.addMultiCellWidget(self.groupBox4, 1, 1, 0, 1)
        Layout1 = QHBoxLayout(None, 0, 6, 'Layout1')
        self.buttonHelp = QPushButton(self, 'buttonHelp')
        self.buttonHelp.setAutoDefault(1)
        Layout1.addWidget(self.buttonHelp)
        Horizontal_Spacing2 = QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        Layout1.addItem(Horizontal_Spacing2)
        self.buttonOk = QPushButton(self, 'buttonOk')
        self.buttonOk.setAutoDefault(1)
        self.buttonOk.setDefault(1)
        Layout1.addWidget(self.buttonOk)
        self.buttonCancel = QPushButton(self, 'buttonCancel')
        self.buttonCancel.setAutoDefault(1)
        Layout1.addWidget(self.buttonCancel)
        EDSMStateDialogLayout.addMultiCellLayout(Layout1, 3, 3, 0, 1)
        self.languageChange()
        self.resize(QSize(382, 340).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)
        self.connect(self.buttonOk, SIGNAL('clicked()'), self.accept)
        self.connect(self.buttonCancel, SIGNAL('clicked()'), self.reject)
        self.connect(self.language_name, SIGNAL('activated(const QString&)'), self.language_name_activated)
        self.connect(self.output_queues, SIGNAL('selectionChanged()'), self.output_queues_selectionChanged)
        self.connect(self.input_queues, SIGNAL('selectionChanged()'), self.input_queues_selectionChanged)
        self.connect(self.queue_name, SIGNAL('textChanged(const QString&)'), self.queue_name_textChanged)
        self.connect(self.add_input_queue_button, SIGNAL('clicked()'), self.add_input_queue_button_clicked)
        self.connect(self.add_output_queue_button, SIGNAL('clicked()'), self.add_output_queue_button_clicked)
        self.connect(self.remove_input_queue_button, SIGNAL('clicked()'), self.remove_input_queue_button_clicked)
        self.connect(self.remove_output_queue_button, SIGNAL('clicked()'), self.remove_output_queue_button_clicked)
        self.setTabOrder(self.object_name, self.class_name)
        self.setTabOrder(self.class_name, self.init_code)
        self.setTabOrder(self.init_code, self.buttonOk)
        self.setTabOrder(self.buttonOk, self.buttonCancel)
        self.setTabOrder(self.buttonCancel, self.buttonHelp)
        self.object_name_textlabel.setBuddy(self.object_name)
        self.init_code_textlabel.setBuddy(self.init_code)
        self.queue_name_textlabel.setBuddy(self.object_name)
        return

    def languageChange(self):
        self.setCaption(self.__tr('EDSM State Dialog'))
        self.object_name_textlabel.setText(self.__tr('Name:'))
        self.groupBox5.setTitle(self.__tr('Implementation'))
        self.language_name.clear()
        self.language_name.insertItem(self.__tr('Python'))
        self.class_name_textlabel.setText(self.__tr('Class:'))
        self.language_name_textlabel.setText(self.__tr('Language:'))
        self.init_code_textlabel.setText(self.__tr('Init code:'))
        self.groupBox4.setTitle(self.__tr('Queues'))
        self.add_output_queue_button.setText(QString.null)
        QToolTip.add(self.add_output_queue_button, self.__tr('Apply'))
        self.remove_output_queue_button.setText(QString.null)
        self.output_queues_label.setText(self.__tr('Output'))
        self.add_input_queue_button.setText(QString.null)
        QToolTip.add(self.add_input_queue_button, self.__tr('Apply'))
        self.remove_input_queue_button.setText(QString.null)
        self.input_queues_label.setText(self.__tr('Input'))
        self.queue_name_textlabel.setText(self.__tr('New Queue'))
        self.buttonHelp.setText(self.__tr('&Help'))
        self.buttonHelp.setAccel(self.__tr('F1'))
        self.buttonOk.setText(self.__tr('&OK'))
        self.buttonOk.setAccel(QString.null)
        self.buttonCancel.setText(self.__tr('&Cancel'))
        self.buttonCancel.setAccel(QString.null)

    def language_name_activated(self, a0):
        print 'EDSMStateDialog.language_name_activated(const QString&): Not implemented yet'

    def output_queues_selectionChanged(self):
        print 'EDSMStateDialog.output_queues_selectionChanged(): Not implemented yet'

    def input_queues_selectionChanged(self):
        print 'EDSMStateDialog.input_queues_selectionChanged(): Not implemented yet'

    def queue_name_textChanged(self, a0):
        print 'EDSMStateDialog.queue_name_textChanged(const QString&): Not implemented yet'

    def add_input_queue_button_clicked(self):
        print 'EDSMStateDialog.add_input_queue_button_clicked(): Not implemented yet'

    def add_output_queue_button_clicked(self):
        print 'EDSMStateDialog.add_output_queue_button_clicked(): Not implemented yet'

    def remove_input_queue_button_clicked(self):
        print 'EDSMStateDialog.remove_input_queue_button_clicked(): Not implemented yet'

    def remove_output_queue_button_clicked(self):
        print 'EDSMStateDialog.remove_output_queue_button_clicked(): Not implemented yet'

    def __tr(self, s, c=None):
        return qApp.translate('EDSMStateDialog', s, c)


if __name__ == '__main__':
    a = QApplication(sys.argv)
    QObject.connect(a, SIGNAL('lastWindowClosed()'), a, SLOT('quit()'))
    w = EDSMStateDialog()
    a.setMainWidget(w)
    w.show()
    a.exec_loop()