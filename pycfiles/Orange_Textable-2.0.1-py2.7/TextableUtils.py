# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\_textable\widgets\TextableUtils.py
# Compiled at: 2016-07-01 03:18:09
"""
Module TextableUtils.py
Copyright 2012-2016 LangTech Sarl (info@langtech.ch)
-----------------------------------------------------------------------------
This file is part of the Orange-Textable package v2.0.

Orange-Textable v2.0 is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Orange-Textable v2.0 is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Orange-Textable v2.0. If not, see <http://www.gnu.org/licenses/>.
-----------------------------------------------------------------------------
Provides classes:
- SendButton
- AdvancedSettings
- InfoBox
- BasicOptionsBox
- JSONMessage
- ContextField
- ContextListField
- ContextInputListField
- ContextInputIndex
- SegmentationListContextHandler
- SegmentationContextHandler
-----------------------------------------------------------------------------
Provides functions:
- pluralize
- updateMultipleInputs
- normalizeCarriageReturns
- getPredefinedEncodings
- getWidgetUuid
"""
__version__ = '0.12'
import re, os, uuid, textwrap
from Orange.OrangeWidgets import OWGUI
from Orange.OrangeWidgets import OWContexts

class SendButton(object):
    """A class encapsulating send button operations in Textable"""

    def __init__(self, widget, master, callback, checkboxValue='autoSend', changedFlag='settingsChanged', buttonLabel='Send', checkboxLabel='Send automatically', infoBoxAttribute=None, sendIfPreCallback=None, sendIfPostCallback=None):
        """Initialize a new Send Button instance"""
        self.widget = widget
        self.master = master
        self.callback = callback
        self.checkboxValue = checkboxValue
        self.changedFlag = changedFlag
        self.buttonLabel = buttonLabel
        self.checkboxLabel = checkboxLabel
        self.infoBoxAttribute = infoBoxAttribute
        self.sendIfPreCallback = sendIfPreCallback
        self.sendIfPostCallback = sendIfPostCallback

    def draw(self):
        """Draw the send button and stopper on window"""
        sendButton = OWGUI.button(widget=self.widget, master=self.master, label=self.buttonLabel, callback=self.callback, tooltip='Process input data and send results to output.')
        autoSendCheckbox = OWGUI.checkBox(widget=self.widget, master=self.master, value=self.checkboxValue, label=self.checkboxLabel, tooltip='Process and send data whenever settings change.')
        OWGUI.setStopper(master=self.master, sendButton=sendButton, stopCheckbox=autoSendCheckbox, changedFlag=self.changedFlag, callback=self.callback)
        self.resetSettingsChangedFlag()

    def sendIf(self):
        """Send data if autoSend is on, else register setting change"""
        if self.sendIfPreCallback is not None:
            self.sendIfPreCallback()
        if self.master.autoSend:
            self.callback()
        else:
            setattr(self.master, self.changedFlag, True)
        if self.sendIfPostCallback is not None:
            self.sendIfPostCallback()
        return

    def settingsChanged(self):
        """Notify setting change and send (if autoSend)"""
        if self.infoBoxAttribute is not None:
            infoBox = getattr(self.master, self.infoBoxAttribute)
            infoBox.settingsChanged()
        self.sendIf()
        return

    def resetSettingsChangedFlag(self):
        """Set master's settings change flag to False"""
        setattr(self.master, self.changedFlag, False)


class AdvancedSettings(object):
    """A class encapsulating advanced settings operations in Textable"""

    def __init__(self, widget, master, callback, checkboxValue='displayAdvancedSettings', basicWidgets=None, advancedWidgets=None):
        """Initialize a new advanced settings instance"""
        self.widget = widget
        self.master = master
        self.callback = callback
        self.checkboxValue = checkboxValue
        if basicWidgets is None:
            basicWidgets = list()
        self.basicWidgets = basicWidgets
        if advancedWidgets is None:
            advancedWidgets = list()
        self.advancedWidgets = advancedWidgets
        return

    def draw(self):
        """Draw the advanced settings checkbox on window"""
        OWGUI.separator(widget=self.widget, height=1)
        OWGUI.checkBox(widget=self.widget, master=self.master, value=self.checkboxValue, label='Advanced settings', callback=self.callback, tooltip='Toggle advanced settings on and off.')
        OWGUI.separator(widget=self.widget, height=1)

    def setVisible(self, bool):
        """Toggle between basic and advanced settings."""
        if bool:
            for widget in self.basicWidgets:
                widget.setVisible(not bool)

            for widget in self.advancedWidgets:
                widget.setVisible(bool)

        else:
            for widget in self.advancedWidgets:
                widget.setVisible(bool)

            for widget in self.basicWidgets:
                widget.setVisible(not bool)

        self.master.adjustSize()

    def basicWidgetsAppendSeparator(self, height=5):
        """Append a separator to the list of basic widgets."""
        self.basicWidgets.append(OWGUI.separator(widget=self.widget, height=height))

    def advancedWidgetsAppendSeparator(self, height=5):
        """Append a separator to the list of advanced widgets."""
        self.advancedWidgets.append(OWGUI.separator(widget=self.widget, height=height))


class InfoBox(object):
    """A class encapsulating info line management operations in Textable"""

    def __init__(self, widget, stringDataSent='Data correctly sent to output', stringNoDataSent='No data sent to output yet', stringSettingsChanged='Settings were changed', stringInputChanged='Input has changed', stringSeeWidgetState=", see 'Widget state' below.", stringClickSend=", please click 'Send' when ready.", wrappedWidth=30):
        """Initialize a new InfoBox instance"""
        self.widget = widget
        self.stringDataSent = stringDataSent
        self.stringNoDataSent = stringNoDataSent
        self.stringSettingsChanged = stringSettingsChanged
        self.stringInputChanged = stringInputChanged
        self.stringSeeWidgetState = stringSeeWidgetState
        self.stringClickSend = stringClickSend
        self.wrappedWidth = wrappedWidth
        iconDir = os.path.join(os.path.split(os.path.split(os.path.abspath(__file__))[0])[0], 'widgets', 'icons')
        self.okIconPath = os.path.join(iconDir, 'ok.png')
        self.warningIconPath = os.path.join(iconDir, 'warning.png')
        self.errorIconPath = os.path.join(iconDir, 'error.png')

    def draw(self):
        """Draw the InfoBox on window"""
        box = OWGUI.widgetBox(widget=self.widget, box=False, orientation='vertical', addSpace=False)
        OWGUI.separator(widget=box, height=2)
        self.stateLabel = OWGUI.widgetLabel(widget=box, label='')
        self.stateLabel.setWordWrap(True)
        self.initialMessage()

    def setText(self, message='', state='ok'):
        """Format and display message"""
        self.widget.topLevelWidget().warning(0)
        self.widget.topLevelWidget().error(0)
        if state == 'ok':
            iconPath = self.okIconPath
        elif state == 'warning':
            iconPath = self.warningIconPath
            self.widget.topLevelWidget().warning(0, message)
        elif state == 'error':
            iconPath = self.errorIconPath
            self.widget.topLevelWidget().error(0, message)
        self.stateLabel.setText("<html><img src='%s'>&nbsp;&nbsp;%s</html>" % (iconPath, message))
        self.widget.topLevelWidget().adjustSizeWithTimer()

    def initialMessage(self):
        """Display initial message"""
        self.setText(message=self.stringNoDataSent + self.stringClickSend, state='warning')

    def dataSent(self, message=''):
        """Display 'ok' message (and 'data sent' status)"""
        if message:
            self.setText(self.stringDataSent + ': ' + message)
        else:
            self.setText(self.stringDataSent + '.')

    def noDataSent(self, message='', warning='', error=''):
        """Display error message (and 'no data sent' status)"""
        self.customMessage(message, warning, error, self.stringNoDataSent)

    def customMessage(self, message='', warning='', error='', pre=''):
        """Display custom message"""
        if warning:
            mode = 'warning'
            completeMessage = pre + ': ' + warning
        elif error:
            mode = 'error'
            completeMessage = pre + ': ' + error
        elif message:
            mode = 'ok'
            completeMessage = pre + ': ' + message
        else:
            mode = 'ok'
            completeMessage = pre + '.'
        self.setText(completeMessage, mode)

    def settingsChanged(self):
        """Display 'Settings changed' message"""
        if not self.widget.topLevelWidget().autoSend:
            self.setText(self.stringSettingsChanged + self.stringClickSend, state='warning')

    def inputChanged(self):
        """Display 'Input changed' message"""
        if not self.widget.topLevelWidget().autoSend:
            self.setText(self.stringInputChanged + self.stringClickSend, state='warning')


class BasicOptionsBox(object):
    """A class encapsulating the basic options box in Textable widgets"""

    def __new__(cls, widget, master, addSpace=False):
        """Initialize a new BasicOptionsBox instance"""
        basicOptionsBox = OWGUI.widgetBox(widget=widget, box='Options', orientation='vertical', addSpace=addSpace)
        OWGUI.lineEdit(widget=basicOptionsBox, master=master, value='label', orientation='horizontal', label='Output segmentation label:', labelWidth=180, callback=master.sendButton.settingsChanged, tooltip='Label of the output segmentation.')
        OWGUI.separator(widget=basicOptionsBox, height=3)
        return basicOptionsBox


class JSONMessage(object):
    """A class encapsulating a JSON message for inter-widget communication"""

    def __init__(self, content=''):
        """Initialize a new JSON message instance"""
        self.content = content


def pluralize(input_string, criterion, plural='s', singular=''):
    """Replace every '@p' in a string with a given form (u's' by default) if
    some criterion is larger than 1, and by another form (u'' by default)
    otherwise.
    """
    replacement = plural if criterion > 1 else singular
    return re.compile('@p').sub(replacement, input_string)


def updateMultipleInputs(itemList, newItem, newId=None, removalCallback=None):
    """Process input when the widget can take multiple ones"""
    ids = [ x[0] for x in itemList ]
    if not newItem:
        if not ids.count(newId):
            return
        index = ids.index(newId)
        if removalCallback is not None:
            removalCallback(index)
        itemList.pop(index)
    elif ids.count(newId):
        index = ids.index(newId)
        itemList[index] = (newId, newItem)
    else:
        itemList.append((newId, newItem))
    return


def normalizeCarriageReturns(string):
    if os.name == 'nt':
        row_delimiter = '\r\n'
    elif os.name == 'mac':
        row_delimiter = '\r'
    else:
        row_delimiter = '\n'
    return string.replace('\n', row_delimiter)


def getPredefinedEncodings():
    """Return the list of predefined encodings"""
    return [
     'ascii',
     'iso-8859-1',
     'iso-8859-15',
     'utf-8',
     'windows-1252',
     'big5',
     'big5hkscs',
     'cp037',
     'cp424',
     'cp437',
     'cp500',
     'cp720',
     'cp737',
     'cp775',
     'cp850',
     'cp852',
     'cp855',
     'cp856',
     'cp857',
     'cp858',
     'cp860',
     'cp861',
     'cp862',
     'cp863',
     'cp864',
     'cp865',
     'cp866',
     'cp869',
     'cp874',
     'cp875',
     'cp932',
     'cp949',
     'cp950',
     'cp1006',
     'cp1026',
     'cp1140',
     'cp1250',
     'cp1251',
     'cp1252',
     'cp1253',
     'cp1254',
     'cp1255',
     'cp1256',
     'cp1257',
     'cp1258',
     'euc_jp',
     'euc_jis_2004',
     'euc_jisx0213',
     'euc_kr',
     'gb2312',
     'gbk',
     'gb18030',
     'hz',
     'iso2022_jp',
     'iso2022_jp_1',
     'iso2022_jp_2',
     'iso2022_jp_2004',
     'iso2022_jp_3',
     'iso2022_jp_ext',
     'iso2022_kr',
     'latin_1',
     'iso8859_2',
     'iso8859_3',
     'iso8859_4',
     'iso8859_5',
     'iso8859_6',
     'iso8859_7',
     'iso8859_8',
     'iso8859_9',
     'iso8859_10',
     'iso8859_13',
     'iso8859_14',
     'iso8859_15',
     'iso8859_16',
     'johab',
     'koi8_r',
     'koi8_u',
     'mac_cyrillic',
     'mac_greek',
     'mac_iceland',
     'mac_latin2',
     'mac_roman',
     'mac_turkish',
     'ptcp154',
     'shift_jis',
     'shift_jis_2004',
     'shift_jisx0213',
     'utf_32',
     'utf_32_be',
     'utf_32_le',
     'utf_16',
     'utf_16_be',
     'utf_16_le',
     'utf_7',
     'utf_8',
     'utf_8_sig']


class ContextField(object):
    """
    A simple field descriptor for storing a single value.

    :param str name: Attribute name in the widget to store.

    """

    def __init__(self, name):
        self.name = name

    def save(self, widget):
        """Return the value of the field from `widget`."""
        return widget.getdeepattr(self.name)

    def restore(self, widget, savedvalue):
        """Restore the `savedvalue` to `widget`."""
        setattr(widget, self.name, savedvalue)


class ContextListField(ContextField):
    """
    Context field for an item list with possible selection indices.

    This field descriptor can be used for storing a list of items
    (labels) and its selection state for a list view as constructed
    by :func:`OWGUI.listBox`

    :param str name:
        Attribute name of the item list in the widget (labels).
    :param str selected:
        Attribute name of a list of indices corresponding to
        selected items (default: `None` meaning there is no selection list).

    """

    def __init__(self, name, selected=None):
        ContextField.__init__(self, name)
        self.selected = selected

    def save(self, widget):
        """Return the value of the field from `widget`."""
        items = list(widget.getdeepattr(self.name))
        if self.selected is not None:
            selected = list(widget.getdeepattr(self.selected))
        else:
            selected = None
        return (
         items, selected)

    def restore(self, widget, savedvalue):
        """Restore the `savedvalue` to `widget`."""
        if len(savedvalue) == 2:
            items, selected = savedvalue
            setattr(widget, self.name, items)
            if self.selected is not None and selected is not None:
                setattr(widget, self.selected, selected)
        return


class ContextInputListField(ContextField):
    """
    Context field for a list of 'Segmentations inputs'.

    This field describes a widget's input list (a list of
    (inputid, Segmentation) tuples as managed by for instance
    :func:`updateMultipleInputs`). In particular it stores/restores
    the order of the input list.

    :param name str: Attribute name in the widget.

    .. note::
        This field can only be used by :class:`SegmentationListContextHandler`

    .. warning::
        When the context is opened (:func:`OWWidget.openContext`) the input
        list order can be changed and assigned back to the widget. For
        instance the following code can raise an assertion error ::

            before = self.inputs
            self.openContext("", self.inputs)
            assert before == self.inputs

        However ``assert set(before) == set(self.inputs)`` will always
        succeed.

    """

    def __init__(self, name):
        ContextField.__init__(self, name)

    def save(self, widget):
        raise NotImplementedError('Save must be performed by the ContextHandler')

    def restore(self, widget, savedvalue):
        raise NotImplementedError('Restore must be performed by the ContextHandler')


class ContextInputIndex(ContextField):
    """
    Context field for an index into the input Segmentations list.

    .. This is the same as :class:`ContextField`, but might be
       changed to support input index restore without permuting
       the input list (as done by `ContextInputListField`) and just
       change the stored index to point to the right item in the
       current list.

    """
    pass


class SegmentationListContextHandler(OWContexts.ContextHandler):
    """
    Segmentations list context handler.

    This Context handler matches settings on a list of
    (inputid, Segmentation) tuples as managed by for instance
    :func:`updateMultipleInputs`.

    :param str contextName: Context handler name.
    :param list fields:
        A list of :class:`ContextField`. As a convenience if the list
        contains any strings they are automatically converted to
        :class:`ContextField` instances.
    :param bool findImperfect:
        Unused, should always be the default ``False`` value (this parameter
        is only present for compatibility with the base class).

    """

    def __init__(self, contextName, fields=[], findImperfect=False, **kwargs):
        if findImperfect != False:
            raise ValueError("'findImperfect' is disabled")
        OWContexts.ContextHandler.__init__(self, contextName, findImperfect=False, syncWithGlobal=False, contextDataVersion=2, **kwargs)
        fields = [ ContextField(field) if isinstance(field, str) else field for field in fields
                 ]
        self.fields = fields
        self.inputListField = None
        inputListField = [ field for field in fields if isinstance(field, ContextInputListField)
                         ]
        if len(inputListField) == 1:
            self.inputListField = inputListField[0]
            self.fields.remove(self.inputListField)
        elif len(inputListField) > 1:
            raise ValueError("Only one 'ContextInputListField' is allowed")
        return

    def findOrCreateContext(self, widget, items):
        encoded = self.encode(self, items)
        context, isnew = OWContexts.ContextHandler.findOrCreateContext(self, widget, encoded)
        context.encoded = encoded
        if isnew:
            context.values = dict()
        return (context, isnew)

    def encode(self, widget, segmentationlist):
        """
        Encode a list of input segmentations for the receiving widget.

        Return a tuple of ```(widget.uuid, encoded_input)```.
        `encoded_input` is a list of  ```(label, annotations, uuid)```
        tuples where `label` is the segmentation label, `annotations` is
        a sorted tuple of segmentation annotation keys and `uuid` is the
        unique identifier if the unique input (source) widget.

       .. note::
            If the receiving widget does not have a uuid then the first
            element of the returned tuple (`widget.uuid`) will be None.

       :param OWWidget widget:
            Widget receiving the input.
        :param list segmentationlist:
            List of (inputid, Segmentation) tuples.

        """
        encoded = list()
        for inputid, segmentation in segmentationlist:
            label = segmentation.label
            annot = tuple(sorted(segmentation.get_annotation_keys()))
            uuid = getattr(inputid[2], 'uuid', None)
            encoded.append((label, annot, uuid))

        return (getattr(widget, 'uuid', None), encoded)

    def match(self, context, imperfect, encoded):
        """
        Match the `context` to the encoded input segmentations.

        Two contexts match if the receiving widget uuid matches the
        stored one and one input list encoding is a reordering of the
        other.

        """
        widget_uuid, inputs = encoded
        stored_uuid, stored_inputs = context.encoded
        if stored_uuid != widget_uuid:
            return 0
        if len(stored_inputs) == len(inputs):
            if set(stored_inputs) == set(inputs):
                return 2
        return 0

    def _permutation(self, seq1, seq2):
        assert len(seq1) == len(seq2) and set(seq1) == set(seq2)
        return [ seq1.index(el) for el in seq2 ]

    def settingsToWidget(self, widget, context):
        """
        Restore the saved `context` to `widget`.
        """
        OWContexts.ContextHandler.settingsToWidget(self, widget, context)
        if self.inputListField and self.inputListField.name in context.values:
            inputs = widget.getdeepattr(self.inputListField.name)
            _, encoded = self.encode(widget, inputs)
            _, stored = context.values[self.inputListField.name]

            def uuids(seq):
                return [ uuid for _, _, uuid in seq ]

            permutation = self._permutation(uuids(encoded), uuids(stored))
            permuted = [ inputs[p] for p in permutation ]
            setattr(widget, self.inputListField.name, permuted)
        for field in self.fields:
            if field.name not in context.values:
                continue
            field.restore(widget, context.values[field.name])

    def settingsFromWidget(self, widget, context):
        """
        Get the settings from a widget.
        """
        OWContexts.ContextHandler.settingsFromWidget(self, widget, context)
        if self.inputListField:
            inputs = self.encode(widget, widget.getdeepattr(self.inputListField.name))
            context.values[self.inputListField.name] = inputs
        for field in self.fields:
            context.values[field.name] = field.save(widget)


class SegmentationContextHandler(OWContexts.ContextHandler):
    """
    Context handler for a single :class:`Segmentation` instance.

    This context handler matches settings on a single instance of
    :class:`Segmentation`. Two segmentations are matched if they
    have the same label and annotation keys.

    :param str contextName: Context handler name.
    :param list fields:
        A list of :class:`ContextField`. As a convenience if the list
        contains any strings they are automatically converted to
        :class:`ContextField` instances.
    :param bool findImperfect:
        Unused, should always be the default ``False`` value (this parameter
        is only present for compatibility with the base class).

    """

    def __init__(self, contextName, fields=[], findImperfect=False, **kwargs):
        if findImperfect != False:
            raise ValueError("'findImperfect' is not supported")
        OWContexts.ContextHandler.__init__(self, contextName, findImperfect=False, contextDataVersion=2, **kwargs)
        self.fields = [ ContextField(field) if isinstance(field, str) else field for field in fields
                      ]

    def encode(self, segmentation):
        """
        Encode a `Segmentation` instance.

        Return a (label, annotations) tuple where `label` is the
        segmentation label and `annotations` is a tuple of sorted
        annotations keys.

        """
        return (
         segmentation.label,
         tuple(sorted(segmentation.get_annotation_keys())))

    def findOrCreateContext(self, widget, segmentation):
        encoded = self.encode(segmentation)
        context, isnew = OWContexts.ContextHandler.findOrCreateContext(self, widget, encoded)
        context.encoded = encoded
        if isnew:
            context.values = dict()
        return (context, isnew)

    def match(self, context, imperfect, encoded):
        """
        Match the `context` to the encoded segmentation context.

        Two contexts match if their encodings are structurally
        equal (==).

        """
        if context.encoded == encoded:
            return 2
        return 0

    def settingsToWidget(self, widget, context):
        for field in self.fields:
            if field.name in context.values:
                field.restore(widget, context.values[field.name])

    def settingsFromWidget(self, widget, context):
        for field in self.fields:
            context.values[field.name] = field.save(widget)


def getWidgetUuid(widget, uuid_name='uuid'):
    """
    Return a persistent universally unique id for a widget.

    :param widget: The OWWidget instance
    :param str uuid_name:
        Name of the uuid attribute (must be in widget's settingsList).

    .. note::
        This function should be called *after* `loadSettings()`.
        Follow this pattern in the widgets __init__ method::

            self.uuid = None
            self.loadSettings()
            self.uuid = getWidgetUuid(self, uuid_name="uuid")

    """
    settings = getattr(widget, '_settingsFromSchema', None)
    if settings is not None and uuid_name in widget.settingsList and uuid_name in settings:
        return settings[uuid_name]
    else:
        return uuid.uuid4()
        return