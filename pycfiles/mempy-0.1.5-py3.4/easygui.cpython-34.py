# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\mempy\lib\easygui.py
# Compiled at: 2014-12-19 20:40:58
# Size of source mod 2**32: 103101 bytes
"""

.. moduleauthor:: Stephen Raymond Ferg
.. default-domain:: py
.. highlight:: python

Version |release|

ABOUT EASYGUI
=============

EasyGui provides an easy-to-use interface for simple GUI interaction
with a user.  It does not require the programmer to know anything about
tkinter, frames, widgets, callbacks or lambda.  All GUI interactions are
invoked by simple function calls that return results.

.. warning:: Using EasyGui with IDLE

    You may encounter problems using IDLE to run programs that use EasyGui. Try it
    and find out.  EasyGui is a collection of Tkinter routines that run their own
    event loops.  IDLE is also a Tkinter application, with its own event loop.  The
    two may conflict, with unpredictable results. If you find that you have
    problems, try running your EasyGui program outside of IDLE.

.. note:: EasyGui requires Tk release 8.0 or greater.

LICENSE INFORMATION
===================
EasyGui version |version|

Copyright (c) 2014, Stephen Raymond Ferg

All rights reserved.

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

    1. Redistributions of source code must retain the above copyright notice,
       this list of conditions and the following disclaimer.

    2. Redistributions in binary form must reproduce the above copyright notice,
       this list of conditions and the following disclaimer in the documentation and/or
       other materials provided with the distribution.

    3. The name of the author may not be used to endorse or promote products derived
       from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE AUTHOR "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
ARE DISCLAIMED. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT,
INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING
IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

ABOUT THE EASYGUI LICENSE
-------------------------
| This license is what is generally known as the "modified BSD license",
| aka "revised BSD", "new BSD", "3-clause BSD".
| See http://www.opensource.org/licenses/bsd-license.php
|
| This license is GPL-compatible.
| See `<http://en.wikipedia.org/wiki/License_compatibility>`_
| See http://www.gnu.org/licenses/license-list.html#GPLCompatibleLicenses
|
| The BSD License is less restrictive than GPL.
| It allows software released under the license to be incorporated into proprietary products.
| Works based on the software may be released under a proprietary license or as closed source software.
| `<http://en.wikipedia.org/wiki/BSD_licenses#3-clause_license_.28.22New_BSD_License.22.29>`_

API
===
"""
eg_version = __doc__.split()[1]
__all__ = [
 'ynbox',
 'ccbox',
 'boolbox',
 'indexbox',
 'msgbox',
 'buttonbox',
 'integerbox',
 'multenterbox',
 'enterbox',
 'exceptionbox',
 'choicebox',
 'codebox',
 'textbox',
 'diropenbox',
 'fileopenbox',
 'filesavebox',
 'passwordbox',
 'multpasswordbox',
 'multchoicebox',
 'abouteasygui',
 'eg_version',
 'egdemo',
 'EgStore']
import os, sys, string, pickle, traceback
if sys.hexversion >= 33947888:
    runningPython26 = True
else:
    runningPython26 = False
if sys.hexversion >= 50331888:
    runningPython3 = True
else:
    runningPython3 = False
try:
    from PIL import Image as PILImage
    from PIL import ImageTk as PILImageTk
except:
    pass

if runningPython3:
    from tkinter import *
    import tkinter.filedialog as tk_FileDialog
    from io import StringIO
else:
    from Tkinter import *
    import tkFileDialog as tk_FileDialog
    from StringIO import StringIO
if runningPython3:
    basestring = str

def write(*args):
    args = [str(arg) for arg in args]
    args = ' '.join(args)
    sys.stdout.write(args)


def writeln(*args):
    write(*args)
    sys.stdout.write('\n')


if TkVersion < 8.0:
    stars = '*' * 75
    writeln('\n\n\n' + stars + '\nYou are running Tk version: ' + str(TkVersion) + '\nYou must be using Tk version 8.0 or greater to use EasyGui.\nTerminating.\n' + stars + '\n\n\n')
    sys.exit(0)
rootWindowPosition = '+300+200'
PROPORTIONAL_FONT_FAMILY = ('MS', 'Sans', 'Serif')
MONOSPACE_FONT_FAMILY = 'Courier'
PROPORTIONAL_FONT_SIZE = 10
MONOSPACE_FONT_SIZE = 9
TEXT_ENTRY_FONT_SIZE = 12
STANDARD_SELECTION_EVENTS = [
 'Return', 'Button-1', 'space']
__choiceboxMultipleSelect = None
__replyButtonText = None
__choiceboxResults = None
__firstWidget = None
__enterboxText = None
__enterboxDefaultText = ''
__multenterboxText = ''
choiceboxChoices = None
choiceboxWidget = None
entryWidget = None
boxRoot = None

def ynbox(msg='Shall I continue?', title=' ', choices=('[<F1>]Yes', '[<F2>]No'), image=None, default_choice='[<F1>]Yes', cancel_choice='[<F2>]No'):
    """
    Display a msgbox with choices of Yes and No.

    The returned value is calculated this way::

        if the first choice ("Yes") is chosen, or if the dialog is cancelled:
            return True
        else:
            return False

    If invoked without a msg argument, displays a generic request for a confirmation
    that the user wishes to continue.  So it can be used this way::

        if ynbox():
            pass # continue
        else:
            sys.exit(0)  # exit the program

    :param msg: the msg to be displayed
    :type msg: str
    :param str title: the window title
    :param list choices: a list or tuple of the choices to be displayed
    :param str image: Filename of image to display
    :param str default_choice: The choice you want highlighted when the gui appears
    :param str cancel_choice: If the user presses the 'X' close, which button should be pressed

    :return: True if 'Yes' or dialog is cancelled, False if 'No'
    """
    return boolbox(msg=msg, title=title, choices=choices, image=image, default_choice=default_choice, cancel_choice=cancel_choice)


def ccbox(msg='Shall I continue?', title=' ', choices=('C[o]ntinue', 'C[a]ncel'), image=None, default_choice='Continue', cancel_choice='Cancel'):
    """
    Display a msgbox with choices of Continue and Cancel.

    The returned value is calculated this way::

        if the first choice ("Continue") is chosen, or if the dialog is cancelled:
            return True
        else:
            return False

    If invoked without a msg argument, displays a generic request for a confirmation
    that the user wishes to continue.  So it can be used this way::

        if ccbox():
            pass # continue
        else:
            sys.exit(0)  # exit the program

    :param str msg: the msg to be displayed
    :param str title: the window title
    :param list choices: a list or tuple of the choices to be displayed
    :param str image: Filename of image to display
    :param str default_choice: The choice you want highlighted when the gui appears
    :param str cancel_choice: If the user presses the 'X' close, which button should be pressed

    :return: True if 'Continue' or dialog is cancelled, False if 'Cancel'
    """
    return boolbox(msg=msg, title=title, choices=choices, image=image, default_choice=default_choice, cancel_choice=cancel_choice)


def boolbox(msg='Shall I continue?', title=' ', choices=('[Y]es', '[N]o'), image=None, default_choice='Yes', cancel_choice='No'):
    """
    Display a boolean msgbox.

    The returned value is calculated this way::

        if the first choice is chosen, or if the dialog is cancelled:
            returns True
        else:
            returns False

    :param str msg: the msg to be displayed
    :param str title: the window title
    :param list choices: a list or tuple of the choices to be displayed
    :param str image: Filename of image to display
    :param str default_choice: The choice you want highlighted when the gui appears
    :param str cancel_choice: If the user presses the 'X' close, which button should be pressed
    :return: True if first button pressed or dialog is cancelled, False if second button is pressed
    """
    if len(choices) != 2:
        raise AssertionError('boolbox takes exactly 2 choices!  Consider using indexbox instead')
    reply = buttonbox(msg=msg, title=title, choices=choices, image=image, default_choice=default_choice, cancel_choice=cancel_choice)
    if reply == choices[0]:
        return True
    else:
        return False


def indexbox(msg='Shall I continue?', title=' ', choices=('Yes', 'No'), image=None, default_choice='Yes', cancel_choice='No'):
    """
    Display a buttonbox with the specified choices.

    :param str msg: the msg to be displayed
    :param str title: the window title
    :param list choices: a list or tuple of the choices to be displayed
    :param str image: Filename of image to display
    :param str default_choice: The choice you want highlighted when the gui appears
    :param str cancel_choice: If the user presses the 'X' close, which button should be pressed
    :return: the index of the choice selected, starting from 0
    """
    reply = buttonbox(msg=msg, title=title, choices=choices, image=image, default_choice=default_choice, cancel_choice=cancel_choice)
    if reply is None:
        return
    for i, choice in enumerate(choices):
        if reply == choice:
            return i

    msg = 'There is a program logic error in the EasyGui code for indexbox.\nreply={0}, choices={1}'.format(reply, choices)
    raise AssertionError(msg)


def msgbox(msg='(Your message goes here)', title=' ', ok_button='OK', image=None, root=None):
    """
    Display a message box

    :param str msg: the msg to be displayed
    :param str title: the window title
    :param str ok_button: text to show in the button
    :param str image: Filename of image to display
    :param tk_widget root: Top-level Tk widget
    :return: the text of the ok_button
    """
    assert isinstance(ok_button, basestring), "The 'ok_button' argument to msgbox must be a string."
    return buttonbox(msg=msg, title=title, choices=[
     ok_button], image=image, root=root, default_choice=ok_button, cancel_choice=ok_button)


def buttonbox(msg='', title=' ', choices=('Button[1]', 'Button[2]', 'Button[3]'), image=None, root=None, default_choice=None, cancel_choice=None):
    """
    Display a msg, a title, an image, and a set of buttons.
    The buttons are defined by the members of the choices list.

    :param str msg: the msg to be displayed
    :param str title: the window title
    :param list choices: a list or tuple of the choices to be displayed
    :param str image: Filename of image to display
    :param str default_choice: The choice you want highlighted when the gui appears
    :param str cancel_choice: If the user presses the 'X' close, which button should be pressed
    :return: the text of the button that the user selected
    """
    global __replyButtonText
    global boxRoot
    global buttonsFrame
    global rootWindowPosition
    if default_choice is None:
        default_choice = choices[0]
    __replyButtonText = choices[0]
    if root:
        root.withdraw()
        boxRoot = Toplevel(master=root)
        boxRoot.withdraw()
    else:
        boxRoot = Tk()
        boxRoot.withdraw()
    boxRoot.title(title)
    boxRoot.iconname('Dialog')
    boxRoot.geometry(rootWindowPosition)
    boxRoot.minsize(400, 100)
    messageFrame = Frame(master=boxRoot)
    messageFrame.pack(side=TOP, fill=BOTH)
    if image:
        tk_Image = None
        try:
            tk_Image = __load_tk_image(image)
        except Exception as inst:
            print(inst)

        if tk_Image:
            imageFrame = Frame(master=boxRoot)
            imageFrame.pack(side=TOP, fill=BOTH)
            label = Label(imageFrame, image=tk_Image)
            label.image = tk_Image
            label.pack(side=TOP, expand=YES, fill=X, padx='1m', pady='1m')
    buttonsFrame = Frame(master=boxRoot)
    buttonsFrame.pack(side=TOP, fill=BOTH)
    messageWidget = Message(messageFrame, text=msg, width=400)
    messageWidget.configure(font=(PROPORTIONAL_FONT_FAMILY, PROPORTIONAL_FONT_SIZE))
    messageWidget.pack(side=TOP, expand=YES, fill=X, padx='3m', pady='3m')
    __put_buttons_in_buttonframe(choices, default_choice, cancel_choice)
    boxRoot.deiconify()
    boxRoot.mainloop()
    boxRoot.destroy()
    if root:
        root.deiconify()
    return __replyButtonText


def integerbox(msg='', title=' ', default='', lowerbound=0, upperbound=99, image=None, root=None):
    """
    Show a box in which a user can enter an integer.

    In addition to arguments for msg and title, this function accepts
    integer arguments for "default", "lowerbound", and "upperbound".

    The default argument may be None.

    When the user enters some text, the text is checked to verify that it
    can be converted to an integer between the lowerbound and upperbound.

    If it can be, the integer (not the text) is returned.

    If it cannot, then an error msg is displayed, and the integerbox is
    redisplayed.

    If the user cancels the operation, None is returned.

    :param str msg: the msg to be displayed
    :param str title: the window title
    :param str default: The default value to return
    :param int lowerbound: The lower-most value allowed
    :param int upperbound: The upper-most value allowed
    :param str image: Filename of image to display
    :param tk_widget root: Top-level Tk widget
    :return: the integer value entered by the user

    """
    if not msg:
        msg = 'Enter an integer between {0} and {1}'.format(lowerbound, upperbound)
    exception_string = 'integerbox "{0}" must be an integer.  It is >{1}< of type {2}'
    if default:
        try:
            default = int(default)
        except ValueError:
            raise ValueError(exception_string.format('default', default, type(default)))

    try:
        lowerbound = int(lowerbound)
    except ValueError:
        raise ValueError(exception_string.format('lowerbound', lowerbound, type(lowerbound)))

    try:
        upperbound = int(upperbound)
    except ValueError:
        raise ValueError(exception_string.format('upperbound', upperbound, type(upperbound)))

    while 1:
        reply = enterbox(msg, title, str(default), image=image, root=root)
        if reply is None:
            return
        else:
            try:
                reply = int(reply)
            except:
                msgbox('The value that you entered:\n\t"{}"\nis not an integer.'.format(reply), 'Error')
                continue

            if reply < lowerbound:
                msgbox('The value that you entered is less than the lower bound of {}.'.format(lowerbound), 'Error')
                continue
            if reply > upperbound:
                msgbox('The value that you entered is greater than the upper bound of {}.'.format(upperbound), 'Error')
                continue
            return reply


def multenterbox(msg='Fill in values for the fields.', title=' ', fields=(), values=()):
    r"""
    Show screen with multiple data entry fields.

    If there are fewer values than names, the list of values is padded with
    empty strings until the number of values is the same as the number of names.

    If there are more values than names, the list of values
    is truncated so that there are as many values as names.

    Returns a list of the values of the fields,
    or None if the user cancels the operation.

    Here is some example code, that shows how values returned from
    multenterbox can be checked for validity before they are accepted::

        msg = "Enter your personal information"
        title = "Credit Card Application"
        fieldNames = ["Name","Street Address","City","State","ZipCode"]
        fieldValues = []  # we start with blanks for the values
        fieldValues = multenterbox(msg,title, fieldNames)

        # make sure that none of the fields was left blank
        while 1:
            if fieldValues is None: break
            errmsg = ""
            for i in range(len(fieldNames)):
                if fieldValues[i].strip() == "":
                    errmsg += ('"%s" is a required field.\n\n' % fieldNames[i])
            if errmsg == "":
                break # no problems found
            fieldValues = multenterbox(errmsg, title, fieldNames, fieldValues)

        writeln("Reply was: %s" % str(fieldValues))

    :param str msg: the msg to be displayed.
    :param str title: the window title
    :param list fields: a list of fieldnames.
    :param list values: a list of field values
    :return: String
    """
    return __multfillablebox(msg, title, fields, values, None)


def multpasswordbox(msg='Fill in values for the fields.', title=' ', fields=tuple(), values=tuple()):
    r"""
    Same interface as multenterbox.  But in multpassword box,
    the last of the fields is assumed to be a password, and
    is masked with asterisks.

    :param str msg: the msg to be displayed.
    :param str title: the window title
    :param list fields: a list of fieldnames.
    :param list values: a list of field values
    :return: String

    **Example**

    Here is some example code, that shows how values returned from
    multpasswordbox can be checked for validity before they are accepted::

        msg = "Enter logon information"
        title = "Demo of multpasswordbox"
        fieldNames = ["Server ID", "User ID", "Password"]
        fieldValues = []  # we start with blanks for the values
        fieldValues = multpasswordbox(msg,title, fieldNames)

        # make sure that none of the fields was left blank
        while 1:
            if fieldValues is None: break
            errmsg = ""
            for i in range(len(fieldNames)):
                if fieldValues[i].strip() == "":
                    errmsg = errmsg + ('"%s" is a required field.\n\n' % fieldNames[i])
                if errmsg == "": break # no problems found
            fieldValues = multpasswordbox(errmsg, title, fieldNames, fieldValues)

        writeln("Reply was: %s" % str(fieldValues))

    """
    return __multfillablebox(msg, title, fields, values, '*')


def bindArrows(widget):
    widget.bind('<Down>', tabRight)
    widget.bind('<Up>', tabLeft)
    widget.bind('<Right>', tabRight)
    widget.bind('<Left>', tabLeft)


def tabRight(event):
    boxRoot.event_generate('<Tab>')


def tabLeft(event):
    boxRoot.event_generate('<Shift-Tab>')


def __multfillablebox(msg='Fill in values for the fields.', title=' ', fields=(), values=(), mask=None):
    global __multenterboxText
    global boxRoot
    global cancelButton
    global entryWidget
    global entryWidgets
    global okButton
    choices = [
     'OK', 'Cancel']
    if len(fields) == 0:
        return
    fields = list(fields[:])
    values = list(values[:])
    if len(values) == len(fields):
        pass
    else:
        if len(values) > len(fields):
            fields = fields[0:len(values)]
        else:
            while len(values) < len(fields):
                values.append('')

        boxRoot = Tk()
        boxRoot.protocol('WM_DELETE_WINDOW', denyWindowManagerClose)
        boxRoot.title(title)
        boxRoot.iconname('Dialog')
        boxRoot.geometry(rootWindowPosition)
        boxRoot.bind('<Escape>', __multenterboxCancel)
        messageFrame = Frame(master=boxRoot)
        messageFrame.pack(side=TOP, fill=BOTH)
        messageWidget = Message(messageFrame, width='4.5i', text=msg)
        messageWidget.configure(font=(PROPORTIONAL_FONT_FAMILY, PROPORTIONAL_FONT_SIZE))
        messageWidget.pack(side=RIGHT, expand=1, fill=BOTH, padx='3m', pady='3m')
        entryWidgets = list()
        lastWidgetIndex = len(fields) - 1
        for widgetIndex in range(len(fields)):
            argFieldName = fields[widgetIndex]
            argFieldValue = values[widgetIndex]
            entryFrame = Frame(master=boxRoot)
            entryFrame.pack(side=TOP, fill=BOTH)
            labelWidget = Label(entryFrame, text=argFieldName)
            labelWidget.pack(side=LEFT)
            entryWidget = Entry(entryFrame, width=40, highlightthickness=2)
            entryWidgets.append(entryWidget)
            entryWidget.configure(font=(PROPORTIONAL_FONT_FAMILY, TEXT_ENTRY_FONT_SIZE))
            entryWidget.pack(side=RIGHT, padx='3m')
            bindArrows(entryWidget)
            entryWidget.bind('<Return>', __multenterboxGetText)
            entryWidget.bind('<Escape>', __multenterboxCancel)
            if widgetIndex == lastWidgetIndex:
                if mask:
                    entryWidgets[widgetIndex].configure(show=mask)
                entryWidgets[widgetIndex].insert(0, argFieldValue)
                widgetIndex += 1

        buttonsFrame = Frame(master=boxRoot)
        buttonsFrame.pack(side=BOTTOM, fill=BOTH)
        okButton = Button(buttonsFrame, takefocus=1, text='OK')
        bindArrows(okButton)
        okButton.pack(expand=1, side=LEFT, padx='3m', pady='3m', ipadx='2m', ipady='1m')
        commandButton = okButton
        handler = __multenterboxGetText
        for selectionEvent in STANDARD_SELECTION_EVENTS:
            commandButton.bind('<%s>' % selectionEvent, handler)

        cancelButton = Button(buttonsFrame, takefocus=1, text='Cancel')
        bindArrows(cancelButton)
        cancelButton.pack(expand=1, side=RIGHT, padx='3m', pady='3m', ipadx='2m', ipady='1m')
        commandButton = cancelButton
        handler = __multenterboxCancel
        for selectionEvent in STANDARD_SELECTION_EVENTS:
            commandButton.bind('<%s>' % selectionEvent, handler)

        entryWidgets[0].focus_force()
        boxRoot.mainloop()
        boxRoot.destroy()
    return __multenterboxText


def __multenterboxGetText(event):
    global __multenterboxText
    __multenterboxText = list()
    for entryWidget in entryWidgets:
        __multenterboxText.append(entryWidget.get())

    boxRoot.quit()


def __multenterboxCancel(event):
    global __multenterboxText
    __multenterboxText = None
    boxRoot.quit()


def enterbox(msg='Enter something.', title=' ', default='', strip=True, image=None, root=None):
    """
    Show a box in which a user can enter some text.

    You may optionally specify some default text, which will appear in the
    enterbox when it is displayed.

    Example::

        reply = enterbox(....)
        if reply:
            ...
        else:
            ...

    :param str msg: the msg to be displayed.
    :param str title: the window title
    :param str default: value returned if user does not change it
    :param bool strip: If True, the return value will have its whitespace stripped before being returned
    :return: the text that the user entered, or None if he cancels the operation.
    """
    result = __fillablebox(msg, title, default=default, mask=None, image=image, root=root)
    if result:
        if strip:
            result = result.strip()
    return result


def passwordbox(msg='Enter your password.', title=' ', default='', image=None, root=None):
    """
    Show a box in which a user can enter a password.
    The text is masked with asterisks, so the password is not displayed.

    :param str msg: the msg to be displayed.
    :param str title: the window title
    :param str default: value returned if user does not change it
    :return: the text that the user entered, or None if he cancels the operation.
    """
    return __fillablebox(msg, title, default, mask='*', image=image, root=root)


def __load_tk_image(filename):
    """
    Load in an image file and return as a tk Image.

    :param filename: image filename to load
    :return: tk Image object
    """
    if filename is None:
        return
    if not os.path.isfile(filename):
        raise ValueError('Image file {} does not exist.'.format(filename))
    tk_image = None
    filename = os.path.normpath(filename)
    _, ext = os.path.splitext(filename)
    try:
        pil_image = PILImage.open(filename)
        tk_image = PILImageTk.PhotoImage(pil_image)
    except:
        try:
            tk_image = PhotoImage(file=filename)
        except:
            msg = 'Cannot load {}.  Check to make sure it is an image file.'.format(filename)
            try:
                _ = PILImage
            except:
                msg += "\nPIL library isn't installed.  If it isn't installed, only .gif files can be used."

            raise ValueError(msg)

    return tk_image


def __fillablebox(msg, title='', default='', mask=None, image=None, root=None):
    """
    Show a box in which a user can enter some text.
    You may optionally specify some default text, which will appear in the
    enterbox when it is displayed.
    Returns the text that the user entered, or None if he cancels the operation.
    """
    global __enterboxDefaultText
    global __enterboxText
    global boxRoot
    global cancelButton
    global entryWidget
    global okButton
    if title is None:
        title == ''
    if default is None:
        default = ''
    __enterboxDefaultText = default
    __enterboxText = __enterboxDefaultText
    if root:
        root.withdraw()
        boxRoot = Toplevel(master=root)
        boxRoot.withdraw()
    else:
        boxRoot = Tk()
        boxRoot.withdraw()
    boxRoot.protocol('WM_DELETE_WINDOW', denyWindowManagerClose)
    boxRoot.title(title)
    boxRoot.iconname('Dialog')
    boxRoot.geometry(rootWindowPosition)
    boxRoot.bind('<Escape>', __enterboxCancel)
    messageFrame = Frame(master=boxRoot)
    messageFrame.pack(side=TOP, fill=BOTH)
    try:
        tk_Image = __load_tk_image(image)
    except Exception as inst:
        print(inst)
        tk_Image = None

    if tk_Image:
        imageFrame = Frame(master=boxRoot)
        imageFrame.pack(side=TOP, fill=BOTH)
        label = Label(imageFrame, image=tk_Image)
        label.image = tk_Image
        label.pack(side=TOP, expand=YES, fill=X, padx='1m', pady='1m')
    buttonsFrame = Frame(master=boxRoot)
    buttonsFrame.pack(side=TOP, fill=BOTH)
    entryFrame = Frame(master=boxRoot)
    entryFrame.pack(side=TOP, fill=BOTH)
    buttonsFrame = Frame(master=boxRoot)
    buttonsFrame.pack(side=TOP, fill=BOTH)
    messageWidget = Message(messageFrame, width='4.5i', text=msg)
    messageWidget.configure(font=(PROPORTIONAL_FONT_FAMILY, PROPORTIONAL_FONT_SIZE))
    messageWidget.pack(side=RIGHT, expand=1, fill=BOTH, padx='3m', pady='3m')
    entryWidget = Entry(entryFrame, width=40)
    bindArrows(entryWidget)
    entryWidget.configure(font=(PROPORTIONAL_FONT_FAMILY, TEXT_ENTRY_FONT_SIZE))
    if mask:
        entryWidget.configure(show=mask)
    entryWidget.pack(side=LEFT, padx='3m')
    entryWidget.bind('<Return>', __enterboxGetText)
    entryWidget.bind('<Escape>', __enterboxCancel)
    entryWidget.insert(0, __enterboxDefaultText)
    okButton = Button(buttonsFrame, takefocus=1, text='OK')
    bindArrows(okButton)
    okButton.pack(expand=1, side=LEFT, padx='3m', pady='3m', ipadx='2m', ipady='1m')
    commandButton = okButton
    handler = __enterboxGetText
    for selectionEvent in STANDARD_SELECTION_EVENTS:
        commandButton.bind('<{}>'.format(selectionEvent), handler)

    cancelButton = Button(buttonsFrame, takefocus=1, text='Cancel')
    bindArrows(cancelButton)
    cancelButton.pack(expand=1, side=RIGHT, padx='3m', pady='3m', ipadx='2m', ipady='1m')
    commandButton = cancelButton
    handler = __enterboxCancel
    for selectionEvent in STANDARD_SELECTION_EVENTS:
        commandButton.bind('<{}>'.format(selectionEvent), handler)

    entryWidget.focus_force()
    boxRoot.deiconify()
    boxRoot.mainloop()
    if root:
        root.deiconify()
    boxRoot.destroy()
    return __enterboxText


def __enterboxGetText(event):
    global __enterboxText
    __enterboxText = entryWidget.get()
    boxRoot.quit()


def __enterboxRestore(event):
    entryWidget.delete(0, len(entryWidget.get()))
    entryWidget.insert(0, __enterboxDefaultText)


def __enterboxCancel(event):
    global __enterboxText
    __enterboxText = None
    boxRoot.quit()


def denyWindowManagerClose():
    """ don't allow WindowManager close
    """
    x = Tk()
    x.withdraw()
    x.bell()
    x.destroy()


def multchoicebox(msg='Pick as many items as you like.', title=' ', choices=(), **kwargs):
    """
    Present the user with a list of choices.
    allow him to select multiple items and return them in a list.
    if the user doesn't choose anything from the list, return the empty list.
    return None if he cancelled selection.

    :param str msg: the msg to be displayed
    :param str title: the window title
    :param list choices: a list or tuple of the choices to be displayed
    :return: List containing choice selected or None if cancelled

    """
    global __choiceboxMultipleSelect
    if len(choices) == 0:
        choices = [
         'Program logic error - no choices were specified.']
    __choiceboxMultipleSelect = 1
    return __choicebox(msg, title, choices)


def choicebox(msg='Pick something.', title=' ', choices=()):
    """
    Present the user with a list of choices.
    return the choice that he selects.

    :param str msg: the msg to be displayed
    :param str title: the window title
    :param list choices: a list or tuple of the choices to be displayed
    :return: List containing choice selected or None if cancelled
    """
    global __choiceboxMultipleSelect
    if len(choices) == 0:
        choices = [
         'Program logic error - no choices were specified.']
    __choiceboxMultipleSelect = 0
    return __choicebox(msg, title, choices)


def __choicebox(msg, title, choices):
    """
    internal routine to support choicebox() and multchoicebox()
    """
    global __choiceboxResults
    global boxRoot
    global choiceboxChoices
    global choiceboxWidget
    choices = list(choices[:])
    if len(choices) == 0:
        choices = [
         'Program logic error - no choices were specified.']
    defaultButtons = [
     'OK', 'Cancel']
    choices = [str(c) for c in choices]
    lines_to_show = min(len(choices), 20)
    lines_to_show = 20
    if title is None:
        title = ''
    __choiceboxResults = None
    boxRoot = Tk()
    screen_width = boxRoot.winfo_screenwidth()
    screen_height = boxRoot.winfo_screenheight()
    root_width = int(screen_width * 0.8)
    root_height = int(screen_height * 0.5)
    root_xpos = int(screen_width * 0.1)
    root_ypos = int(screen_height * 0.05)
    boxRoot.title(title)
    boxRoot.iconname('Dialog')
    rootWindowPosition = '+0+0'
    boxRoot.geometry(rootWindowPosition)
    boxRoot.expand = NO
    boxRoot.minsize(root_width, root_height)
    rootWindowPosition = '+{0}+{1}'.format(root_xpos, root_ypos)
    boxRoot.geometry(rootWindowPosition)
    message_and_buttonsFrame = Frame(master=boxRoot)
    message_and_buttonsFrame.pack(side=TOP, fill=X, expand=NO)
    messageFrame = Frame(message_and_buttonsFrame)
    messageFrame.pack(side=LEFT, fill=X, expand=YES)
    buttonsFrame = Frame(message_and_buttonsFrame)
    buttonsFrame.pack(side=RIGHT, expand=NO, pady=0)
    choiceboxFrame = Frame(master=boxRoot)
    choiceboxFrame.pack(side=BOTTOM, fill=BOTH, expand=YES)
    messageWidget = Message(messageFrame, anchor=NW, text=msg, width=int(root_width * 0.9))
    messageWidget.configure(font=(PROPORTIONAL_FONT_FAMILY, PROPORTIONAL_FONT_SIZE))
    messageWidget.pack(side=LEFT, expand=YES, fill=BOTH, padx='1m', pady='1m')
    choiceboxWidget = Listbox(choiceboxFrame, height=lines_to_show, borderwidth='1m', relief='flat', bg='white')
    if __choiceboxMultipleSelect:
        choiceboxWidget.configure(selectmode=MULTIPLE)
    choiceboxWidget.configure(font=(PROPORTIONAL_FONT_FAMILY, PROPORTIONAL_FONT_SIZE))
    rightScrollbar = Scrollbar(choiceboxFrame, orient=VERTICAL, command=choiceboxWidget.yview)
    choiceboxWidget.configure(yscrollcommand=rightScrollbar.set)
    bottomScrollbar = Scrollbar(choiceboxFrame, orient=HORIZONTAL, command=choiceboxWidget.xview)
    choiceboxWidget.configure(xscrollcommand=bottomScrollbar.set)
    bottomScrollbar.pack(side=BOTTOM, fill=X)
    rightScrollbar.pack(side=RIGHT, fill=Y)
    choiceboxWidget.pack(side=LEFT, padx='1m', pady='1m', expand=YES, fill=BOTH)
    if runningPython3:
        choices.sort(key=str.lower)
    else:
        choices.sort(lambda x, y: cmp(x.lower(), y.lower()))
    lastInserted = None
    choiceboxChoices = list()
    for choice in choices:
        if choice == lastInserted:
            continue
        else:
            choiceboxWidget.insert(END, choice)
            choiceboxChoices.append(choice)
            lastInserted = choice

    boxRoot.bind('<Any-Key>', KeyboardListener)
    if len(choices):
        okButton = Button(buttonsFrame, takefocus=YES, text='OK', height=1, width=6)
        bindArrows(okButton)
        okButton.pack(expand=NO, side=TOP, padx='2m', pady='1m', ipady='1m', ipadx='2m')
        commandButton = okButton
        handler = __choiceboxGetChoice
        for selectionEvent in STANDARD_SELECTION_EVENTS:
            commandButton.bind('<%s>' % selectionEvent, handler)

        choiceboxWidget.bind('<Return>', __choiceboxGetChoice)
        choiceboxWidget.bind('<Double-Button-1>', __choiceboxGetChoice)
    else:
        choiceboxWidget.bind('<Return>', __choiceboxCancel)
        choiceboxWidget.bind('<Double-Button-1>', __choiceboxCancel)
    cancelButton = Button(buttonsFrame, takefocus=YES, text='Cancel', height=1, width=6)
    bindArrows(cancelButton)
    cancelButton.pack(expand=NO, side=BOTTOM, padx='2m', pady='1m', ipady='1m', ipadx='2m')
    commandButton = cancelButton
    handler = __choiceboxCancel
    for selectionEvent in STANDARD_SELECTION_EVENTS:
        commandButton.bind('<%s>' % selectionEvent, handler)

    if len(choices):
        if __choiceboxMultipleSelect:
            selectionButtonsFrame = Frame(messageFrame)
            selectionButtonsFrame.pack(side=RIGHT, fill=Y, expand=NO)
            selectAllButton = Button(selectionButtonsFrame, text='Select All', height=1, width=6)
            bindArrows(selectAllButton)
            selectAllButton.bind('<Button-1>', __choiceboxSelectAll)
            selectAllButton.pack(expand=NO, side=TOP, padx='2m', pady='1m', ipady='1m', ipadx='2m')
            clearAllButton = Button(selectionButtonsFrame, text='Clear All', height=1, width=6)
            bindArrows(clearAllButton)
            clearAllButton.bind('<Button-1>', __choiceboxClearAll)
            clearAllButton.pack(expand=NO, side=TOP, padx='2m', pady='1m', ipady='1m', ipadx='2m')
    boxRoot.bind('<Escape>', __choiceboxCancel)
    choiceboxWidget.select_set(0)
    choiceboxWidget.focus_force()
    boxRoot.mainloop()
    try:
        boxRoot.destroy()
    except:
        pass

    return __choiceboxResults


def __choiceboxGetChoice(event):
    global __choiceboxResults
    if __choiceboxMultipleSelect:
        __choiceboxResults = [choiceboxWidget.get(index) for index in choiceboxWidget.curselection()]
    else:
        choice_index = choiceboxWidget.curselection()
        __choiceboxResults = choiceboxWidget.get(choice_index)
    boxRoot.quit()


def __choiceboxSelectAll(event):
    choiceboxWidget.selection_set(0, len(choiceboxChoices) - 1)


def __choiceboxClearAll(event):
    choiceboxWidget.selection_clear(0, len(choiceboxChoices) - 1)


def __choiceboxCancel(event):
    global __choiceboxResults
    __choiceboxResults = None
    boxRoot.quit()


def KeyboardListener(event):
    key = event.keysym
    if len(key) <= 1:
        if key in string.printable:
            try:
                start_n = int(choiceboxWidget.curselection()[0])
            except IndexError:
                start_n = -1

            choiceboxWidget.selection_clear(0, 'end')
            for n in range(start_n + 1, len(choiceboxChoices)):
                item = choiceboxChoices[n]
                if item[0].lower() == key.lower():
                    choiceboxWidget.selection_set(first=n)
                    choiceboxWidget.see(n)
                    return
            else:
                for n, item in enumerate(choiceboxChoices):
                    if item[0].lower() == key.lower():
                        choiceboxWidget.selection_set(first=n)
                        choiceboxWidget.see(n)
                        return

                for n, item in enumerate(choiceboxChoices):
                    if item[0].lower() > key.lower():
                        if n > 0:
                            choiceboxWidget.selection_set(first=n - 1)
                        else:
                            choiceboxWidget.selection_set(first=0)
                        choiceboxWidget.see(n)
                        return

                lastIndex = len(choiceboxChoices) - 1
                choiceboxWidget.selection_set(first=lastIndex)
                choiceboxWidget.see(lastIndex)
                return


def exception_format():
    """
    Convert exception info into a string suitable for display.
    """
    return ''.join(traceback.format_exception(sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2]))


def exceptionbox(msg=None, title=None):
    """
    Display a box that gives information about
    an exception that has just been raised.

    The caller may optionally pass in a title for the window, or a
    msg to accompany the error information.

    Note that you do not need to (and cannot) pass an exception object
    as an argument.  The latest exception will automatically be used.

    :param str msg: the msg to be displayed
    :param str title: the window title
    :return: None

    """
    if title is None:
        title = 'Error Report'
    if msg is None:
        msg = 'An error (exception) has occurred in the program.'
    codebox(msg, title, exception_format())


def codebox(msg='', title=' ', text=''):
    """
    Display some text in a monospaced font, with no line wrapping.
    This function is suitable for displaying code and text that is
    formatted using spaces.

    The text parameter should be a string, or a list or tuple of lines to be
    displayed in the textbox.

    :param str msg: the msg to be displayed
    :param str title: the window title
    :param str text: what to display in the textbox
    """
    return textbox(msg, title, text, codebox=1)


def textbox(msg='', title=' ', text='', codebox=0):
    """
    Display some text in a proportional font with line wrapping at word breaks.
    This function is suitable for displaying general written text.

    The text parameter should be a string, or a list or tuple of lines to be
    displayed in the textbox.

    :param str msg: the msg to be displayed
    :param str title: the window title
    :param str text: what to display in the textbox
    :param str codebox: if 1, act as a codebox
    """
    global __replyButtonText
    global boxRoot
    global buttonsFrame
    global rootWindowPosition
    if msg is None:
        msg = ''
    if title is None:
        title = ''
    choices = [
     'OK']
    __replyButtonText = choices[0]
    boxRoot = Tk()
    boxRoot.protocol('WM_DELETE_WINDOW', denyWindowManagerClose)
    screen_width = boxRoot.winfo_screenwidth()
    screen_height = boxRoot.winfo_screenheight()
    root_width = int(screen_width * 0.8)
    root_height = int(screen_height * 0.5)
    root_xpos = int(screen_width * 0.1)
    root_ypos = int(screen_height * 0.05)
    boxRoot.title(title)
    boxRoot.iconname('Dialog')
    rootWindowPosition = '+0+0'
    boxRoot.geometry(rootWindowPosition)
    boxRoot.expand = NO
    boxRoot.minsize(root_width, root_height)
    rootWindowPosition = '+{0}+{1}'.format(root_xpos, root_ypos)
    boxRoot.geometry(rootWindowPosition)
    mainframe = Frame(master=boxRoot)
    mainframe.pack(side=TOP, fill=BOTH, expand=YES)
    textboxFrame = Frame(mainframe, borderwidth=3)
    textboxFrame.pack(side=BOTTOM, fill=BOTH, expand=YES)
    message_and_buttonsFrame = Frame(mainframe)
    message_and_buttonsFrame.pack(side=TOP, fill=X, expand=NO)
    messageFrame = Frame(message_and_buttonsFrame)
    messageFrame.pack(side=LEFT, fill=X, expand=YES)
    buttonsFrame = Frame(message_and_buttonsFrame)
    buttonsFrame.pack(side=RIGHT, expand=NO)
    if codebox:
        character_width = int(root_width * 0.6 / MONOSPACE_FONT_SIZE)
        textArea = Text(textboxFrame, height=25, width=character_width, padx='2m', pady='1m')
        textArea.configure(wrap=NONE)
        textArea.configure(font=(MONOSPACE_FONT_FAMILY, MONOSPACE_FONT_SIZE))
    else:
        character_width = int(root_width * 0.6 / MONOSPACE_FONT_SIZE)
        textArea = Text(textboxFrame, height=25, width=character_width, padx='2m', pady='1m')
        textArea.configure(wrap=WORD)
        textArea.configure(font=(PROPORTIONAL_FONT_FAMILY, PROPORTIONAL_FONT_SIZE))
    mainframe.bind('<Next>', textArea.yview_scroll(1, PAGES))
    mainframe.bind('<Prior>', textArea.yview_scroll(-1, PAGES))
    mainframe.bind('<Right>', textArea.xview_scroll(1, PAGES))
    mainframe.bind('<Left>', textArea.xview_scroll(-1, PAGES))
    mainframe.bind('<Down>', textArea.yview_scroll(1, UNITS))
    mainframe.bind('<Up>', textArea.yview_scroll(-1, UNITS))
    rightScrollbar = Scrollbar(textboxFrame, orient=VERTICAL, command=textArea.yview)
    textArea.configure(yscrollcommand=rightScrollbar.set)
    bottomScrollbar = Scrollbar(textboxFrame, orient=HORIZONTAL, command=textArea.xview)
    textArea.configure(xscrollcommand=bottomScrollbar.set)
    if codebox:
        bottomScrollbar.pack(side=BOTTOM, fill=X)
    rightScrollbar.pack(side=RIGHT, fill=Y)
    textArea.pack(side=LEFT, fill=BOTH, expand=YES)
    messageWidget = Message(messageFrame, anchor=NW, text=msg, width=int(root_width * 0.9))
    messageWidget.configure(font=(PROPORTIONAL_FONT_FAMILY, PROPORTIONAL_FONT_SIZE))
    messageWidget.pack(side=LEFT, expand=YES, fill=BOTH, padx='1m', pady='1m')
    okButton = Button(buttonsFrame, takefocus=YES, text='OK', height=1, width=6)
    okButton.pack(expand=NO, side=TOP, padx='2m', pady='1m', ipady='1m', ipadx='2m')
    commandButton = okButton
    handler = __textboxOK
    for selectionEvent in ['Return', 'Button-1', 'Escape']:
        commandButton.bind('<%s>' % selectionEvent, handler)

    try:
        if isinstance(text, basestring):
            pass
        else:
            try:
                text = ''.join(text)
            except:
                msgbox('Exception when trying to convert {} to text in textArea'.format(type(text)))
                sys.exit(16)

            textArea.insert('end', text, 'normal')
    except:
        msgbox('Exception when trying to load the textArea.')
        sys.exit(16)

    try:
        okButton.focus_force()
    except:
        msgbox('Exception when trying to put focus on okButton.')
        sys.exit(16)

    boxRoot.mainloop()
    areaText = textArea.get(0.0, 'end-1c')
    boxRoot.destroy()
    return areaText


def __textboxOK(event):
    boxRoot.quit()


def diropenbox(msg=None, title=None, default=None):
    """
    A dialog to get a directory name.
    Note that the msg argument, if specified, is ignored.

    Returns the name of a directory, or None if user chose to cancel.

    If the "default" argument specifies a directory name, and that
    directory exists, then the dialog box will start with that directory.

    :param str msg: the msg to be displayed
    :param str title: the window title
    :param str default: starting directory when dialog opens
    :return: Normalized path selected by user
    """
    title = getFileDialogTitle(msg, title)
    localRoot = Tk()
    localRoot.withdraw()
    if not default:
        default = None
    f = tk_FileDialog.askdirectory(parent=localRoot, title=title, initialdir=default, initialfile=None)
    localRoot.destroy()
    if not f:
        return
    return os.path.normpath(f)


def getFileDialogTitle(msg, title):
    """
    Create nicely-formatted string based on arguments msg and title
    :param msg: the msg to be displayed
    :param title: the window title
    :return: None
    """
    if msg and title:
        return '%s - %s' % (title, msg)
    if msg and not title:
        return str(msg)
    if title and not msg:
        return str(title)


class FileTypeObject:

    def __init__(self, filemask):
        if len(filemask) == 0:
            raise AssertionError('Filetype argument is empty.')
        self.masks = list()
        if isinstance(filemask, basestring):
            self.initializeFromString(filemask)
        else:
            if isinstance(filemask, list):
                if len(filemask) < 2:
                    raise AssertionError('Invalid filemask.\n' + 'List contains less than 2 members: "{}"'.format(filemask))
                else:
                    self.name = filemask[(-1)]
                    self.masks = list(filemask[:-1])
            else:
                raise AssertionError('Invalid filemask: "{}"'.format(filemask))

    def __eq__(self, other):
        if self.name == other.name:
            return True
        return False

    def add(self, other):
        for mask in other.masks:
            if mask in self.masks:
                continue
                self.masks.append(mask)

    def toTuple(self):
        return (
         self.name, tuple(self.masks))

    def isAll(self):
        if self.name == 'All files':
            return True
        return False

    def initializeFromString(self, filemask):
        self.ext = os.path.splitext(filemask)[1]
        if self.ext == '':
            self.ext = '.*'
        if self.ext == '.':
            self.ext = '.*'
        self.name = self.getName()
        self.masks = ['*' + self.ext]

    def getName(self):
        e = self.ext
        file_types = {'.*': 'All',  '.txt': 'Text',  '.py': 'Python',  '.pyc': 'Python',  '.xls': 'Excel'}
        if e in file_types:
            return '{} files'.format(file_types[e])
        if e.startswith('.'):
            return '{} files'.format(e[1:].upper())
        return '{} files'.format(e.upper())


def fileopenbox(msg=None, title=None, default='*', filetypes=None, multiple=False):
    r"""
    A dialog to get a file name.

    **About the "default" argument**

    The "default" argument specifies a filepath that (normally)
    contains one or more wildcards.
    fileopenbox will display only files that match the default filepath.
    If omitted, defaults to "\*" (all files in the current directory).

    WINDOWS EXAMPLE::

        ...default="c:/myjunk/*.py"

    will open in directory c:\myjunk\ and show all Python files.

    WINDOWS EXAMPLE::

        ...default="c:/myjunk/test*.py"

    will open in directory c:\myjunk\ and show all Python files
    whose names begin with "test".

    Note that on Windows, fileopenbox automatically changes the path
    separator to the Windows path separator (backslash).

    **About the "filetypes" argument**

    If specified, it should contain a list of items,
    where each item is either:

    - a string containing a filemask          # e.g. "\*.txt"
    - a list of strings, where all of the strings except the last one
      are filemasks (each beginning with "\*.",
      such as "\*.txt" for text files, "\*.py" for Python files, etc.).
      and the last string contains a filetype description

    EXAMPLE::

        filetypes = ["*.css", ["*.htm", "*.html", "HTML files"]  ]

    .. note:: If the filetypes list does not contain ("All files","*"), it will be added.

    If the filetypes list does not contain a filemask that includes
    the extension of the "default" argument, it will be added.
    For example, if default="\*abc.py"
    and no filetypes argument was specified, then
    "\*.py" will automatically be added to the filetypes argument.

    :param str msg: the msg to be displayed.
    :param str title: the window title
    :param str default: filepath with wildcards
    :param object filetypes: filemasks that a user can choose, e.g. "\*.txt"
    :param bool multiple: If true, more than one file can be selected
    :return: the name of a file, or None if user chose to cancel
    """
    localRoot = Tk()
    localRoot.withdraw()
    initialbase, initialfile, initialdir, filetypes = fileboxSetup(default, filetypes)
    if initialfile.find('*') < 0 and initialfile.find('?') < 0:
        initialfile = None
    else:
        if initialbase == '*':
            initialfile = None
        func = tk_FileDialog.askopenfilenames if multiple else tk_FileDialog.askopenfilename
        ret_val = func(parent=localRoot, title=getFileDialogTitle(msg, title), initialdir=initialdir, initialfile=initialfile, filetypes=filetypes)
        if multiple:
            f = [os.path.normpath(x) for x in localRoot.tk.splitlist(ret_val)]
        else:
            f = os.path.normpath(ret_val)
    localRoot.destroy()
    if not f:
        return
    return f


def filesavebox(msg=None, title=None, default='', filetypes=None):
    r"""
    A file to get the name of a file to save.
    Returns the name of a file, or None if user chose to cancel.

    The "default" argument should contain a filename (i.e. the
    current name of the file to be saved).  It may also be empty,
    or contain a filemask that includes wildcards.

    The "filetypes" argument works like the "filetypes" argument to
    fileopenbox.

    :param str msg: the msg to be displayed.
    :param str title: the window title
    :param str default: default filename to return
    :param object filetypes: filemasks that a user can choose, e.g. " \*.txt"
    :return: the name of a file, or None if user chose to cancel
    """
    localRoot = Tk()
    localRoot.withdraw()
    initialbase, initialfile, initialdir, filetypes = fileboxSetup(default, filetypes)
    f = tk_FileDialog.asksaveasfilename(parent=localRoot, title=getFileDialogTitle(msg, title), initialfile=initialfile, initialdir=initialdir, filetypes=filetypes)
    localRoot.destroy()
    if not f:
        return
    return os.path.normpath(f)


def fileboxSetup(default, filetypes):
    if not default:
        default = os.path.join('.', '*')
    initialdir, initialfile = os.path.split(default)
    if not initialdir:
        initialdir = '.'
    if not initialfile:
        initialfile = '*'
    initialbase, initialext = os.path.splitext(initialfile)
    initialFileTypeObject = FileTypeObject(initialfile)
    allFileTypeObject = FileTypeObject('*')
    ALL_filetypes_was_specified = False
    if not filetypes:
        filetypes = list()
    filetypeObjects = list()
    for filemask in filetypes:
        fto = FileTypeObject(filemask)
        if fto.isAll():
            ALL_filetypes_was_specified = True
        if fto == initialFileTypeObject:
            initialFileTypeObject.add(fto)
        else:
            filetypeObjects.append(fto)

    if ALL_filetypes_was_specified:
        pass
    else:
        if allFileTypeObject == initialFileTypeObject:
            pass
        else:
            filetypeObjects.insert(0, allFileTypeObject)
        if len(filetypeObjects) == 0:
            filetypeObjects.append(initialFileTypeObject)
        if initialFileTypeObject in (filetypeObjects[0], filetypeObjects[(-1)]):
            pass
        else:
            if runningPython26:
                filetypeObjects.append(initialFileTypeObject)
            else:
                filetypeObjects.insert(0, initialFileTypeObject)
            filetypes = [fto.toTuple() for fto in filetypeObjects]
    return (
     initialbase, initialfile, initialdir, filetypes)


def uniquify_list_of_strings(input_list):
    """
    Ensure that every string within input_list is unique.
    :param list input_list: List of strings
    :return: New list with unique names as needed.
    """
    output_list = list()
    for i, item in enumerate(input_list):
        tempList = input_list[:i] + input_list[i + 1:]
        if item not in tempList:
            output_list.append(item)
        else:
            output_list.append('{0}_{1}'.format(item, i))

    return output_list


import re

def parse_hotkey(text):
    """
    Extract a desired hotkey from the text.  The format to enclose the hotkey in square braces
    as in Button_[1] which would assign the keyboard key 1 to that button.  The one will be included in the
    button text.  To hide they key, use double square braces as in:  Ex[[qq]]it  , which would assign
    the q key to the Exit button. Special keys such as <Enter> may also be used:  Move [<left>]  for a full
    list of special keys, see this reference: http://infohost.nmt.edu/tcc/help/pubs/tkinter/web/key-names.html
    :param text:
    :return: list containing cleaned text, hotkey, and hotkey position within cleaned text.
    """
    ret_val = [
     text, None, None]
    if text is None:
        return ret_val
    res = re.search('(?<=\\[).(?=\\])', text)
    if res:
        start = res.start(0)
        end = res.end(0)
        caption = text[:start - 1] + text[start:end] + text[end + 1:]
        ret_val = [caption, text[start:end], start - 1]
    res = re.search('(?<=\\[\\[).(?=\\]\\])', text)
    if res:
        start = res.start(0)
        end = res.end(0)
        caption = text[:start - 2] + text[end + 2:]
        ret_val = [caption, text[start:end], None]
    res = re.search('(?<=\\[\\<).+(?=\\>\\])', text)
    if res:
        start = res.start(0)
        end = res.end(0)
        caption = text[:start - 2] + text[end + 2:]
        ret_val = [caption, '<{}>'.format(text[start:end]), None]
    return ret_val


def __buttonEvent(event=None, buttons=None, virtual_event=None):
    """
    Handle an event that is generated by a person interacting with a button.  It may be a button press
    or a key press.
    """
    global __replyButtonText
    global rootWindowPosition
    m = re.match('(\\d+)x(\\d+)([-+]\\d+)([-+]\\d+)', boxRoot.geometry())
    if not m:
        raise ValueError('failed to parse geometry string: {}'.format(boxRoot.geometry()))
    width, height, xoffset, yoffset = [int(s) for s in m.groups()]
    rootWindowPosition = '{0:+g}{1:+g}'.format(xoffset, yoffset)
    if virtual_event == 'cancel':
        for button_name, button in buttons.items():
            if 'cancel_choice' in button:
                __replyButtonText = button['original_text']
                continue

        __replyButtonText = None
        boxRoot.quit()
        return
    if virtual_event == 'select':
        text = event.widget.config('text')[(-1)]
        if not isinstance(text, basestring):
            text = ' '.join(text)
        for button_name, button in buttons.items():
            if button['clean_text'] == text:
                __replyButtonText = button['original_text']
                boxRoot.quit()
                return

    if buttons:
        for button_name, button in buttons.items():
            hotkey_pressed = event.keysym
            if event.keysym != event.char:
                hotkey_pressed = '<{}>'.format(event.keysym)
            if button['hotkey'] == hotkey_pressed:
                __replyButtonText = button_name
                boxRoot.quit()
                return

    print('Event not understood')


def __put_buttons_in_buttonframe(choices, default_choice, cancel_choice):
    """Put the buttons in the buttons frame
    """
    unique_choices = uniquify_list_of_strings(choices)
    buttons = dict()
    for button_text, unique_button_text in zip(choices, unique_choices):
        this_button = dict()
        this_button['original_text'] = button_text
        this_button['clean_text'], this_button['hotkey'], hotkey_position = parse_hotkey(button_text)
        this_button['widget'] = Button(buttonsFrame, takefocus=1, text=this_button['clean_text'], underline=hotkey_position)
        this_button['widget'].pack(expand=YES, side=LEFT, padx='1m', pady='1m', ipadx='2m', ipady='1m')
        buttons[unique_button_text] = this_button

    for this_button in buttons.values():
        bindArrows(this_button['widget'])
        for selectionEvent in STANDARD_SELECTION_EVENTS:
            this_button['widget'].bind('<{}>'.format(selectionEvent), lambda e: __buttonEvent(e, buttons, virtual_event='select'), add=True)

    if cancel_choice in buttons:
        buttons[cancel_choice]['cancel_choice'] = True
    boxRoot.bind_all('<Escape>', lambda e: __buttonEvent(e, buttons, virtual_event='cancel'), add=True)
    boxRoot.protocol('WM_DELETE_WINDOW', lambda : __buttonEvent(None, buttons, virtual_event='cancel'))
    if default_choice in buttons:
        buttons[default_choice]['default_choice'] = True
        buttons[default_choice]['widget'].focus_force()
    for hk in [button['hotkey'] for button in buttons.values() if button['hotkey']]:
        boxRoot.bind_all(hk, lambda e: __buttonEvent(e, buttons), add=True)


class EgStore:
    __doc__ = '\nA class to support persistent storage.\n\nYou can use EgStore to support the storage and retrieval\nof user settings for an EasyGui application.\n\n**Example A: define a class named Settings as a subclass of EgStore**\n::\n\n    class Settings(EgStore):\n        def __init__(self, filename):  # filename is required\n            #-------------------------------------------------\n            # Specify default/initial values for variables that\n            # this particular application wants to remember.\n            #-------------------------------------------------\n            self.userId = ""\n            self.targetServer = ""\n\n            #-------------------------------------------------\n            # For subclasses of EgStore, these must be\n            # the last two statements in  __init__\n            #-------------------------------------------------\n            self.filename = filename  # this is required\n            self.restore()            # restore values from the storage file if possible\n\n**Example B: create settings, a persistent Settings object**\n::\n\n    settingsFile = "myApp_settings.txt"\n    settings = Settings(settingsFile)\n\n    user    = "obama_barak"\n    server  = "whitehouse1"\n    settings.userId = user\n    settings.targetServer = server\n    settings.store()    # persist the settings\n\n    # run code that gets a new value for userId, and persist the settings\n    user    = "biden_joe"\n    settings.userId = user\n    settings.store()\n\n**Example C: recover the Settings instance, change an attribute, and store it again.**\n::\n\n    settings = Settings(settingsFile)\n    settings.userId = "vanrossum_g"\n    settings.store()\n\n'

    def __init__(self, filename):
        self.filename = None
        raise NotImplementedError()

    def restore(self):
        """
        Set the values of whatever attributes are recoverable
        from the pickle file.

        Populate the attributes (the __dict__) of the EgStore object
        from     the attributes (the __dict__) of the pickled object.

        If the pickled object has attributes that have been initialized
        in the EgStore object, then those attributes of the EgStore object
        will be replaced by the values of the corresponding attributes
        in the pickled object.

        If the pickled object is missing some attributes that have
        been initialized in the EgStore object, then those attributes
        of the EgStore object will retain the values that they were
        initialized with.

        If the pickled object has some attributes that were not
        initialized in the EgStore object, then those attributes
        will be ignored.

        IN SUMMARY:

        After the recover() operation, the EgStore object will have all,
        and only, the attributes that it had when it was initialized.

        Where possible, those attributes will have values recovered
        from the pickled object.
        """
        if not os.path.exists(self.filename):
            return self
        if not os.path.isfile(self.filename):
            return self
        try:
            with open(self.filename, 'rb') as (f):
                unpickledObject = pickle.load(f)
            for key in list(self.__dict__.keys()):
                default = self.__dict__[key]
                self.__dict__[key] = unpickledObject.__dict__.get(key, default)

        except:
            pass

        return self

    def store(self):
        """
        Save the attributes of the EgStore object to a pickle file.
        Note that if the directory for the pickle file does not already exist,
        the store operation will fail.
        """
        with open(self.filename, 'wb') as (f):
            pickle.dump(self, f)

    def kill(self):
        """
        Delete my persistent file (i.e. pickle file), if it exists.
        """
        if os.path.isfile(self.filename):
            os.remove(self.filename)

    def __str__(self):
        """
        return my contents as a string in an easy-to-read format.
        """
        longest_key_length = 0
        keys = list()
        for key in self.__dict__.keys():
            keys.append(key)
            longest_key_length = max(longest_key_length, len(key))

        keys.sort()
        lines = list()
        for key in keys:
            value = self.__dict__[key]
            key = key.ljust(longest_key_length)
            lines.append('%s : %s\n' % (key, repr(value)))

        return ''.join(lines)


package_dir = os.path.dirname(os.path.realpath(__file__))

def egdemo():
    """
    Run the EasyGui demo.
    """
    writeln('\n' * 100)
    msg = list()
    msg.append('Pick the kind of box that you wish to demo.')
    msg.append(' * Python version {}'.format(sys.version))
    msg.append(' * EasyGui version {}'.format(eg_version))
    msg.append(' * Tk version {}'.format(TkVersion))
    intro_message = '\n'.join(msg)
    while True:
        choices = [
         'msgbox',
         'buttonbox',
         'buttonbox(image) -- a buttonbox that displays an image',
         'choicebox',
         'multchoicebox',
         'textbox',
         'ynbox',
         'ccbox',
         'enterbox',
         'enterbox(image) -- an enterbox that displays an image',
         'exceptionbox',
         'codebox',
         'integerbox',
         'boolbox',
         'indexbox',
         'filesavebox',
         'fileopenbox',
         'passwordbox',
         'multenterbox',
         'multpasswordbox',
         'diropenbox',
         'About EasyGui',
         ' Help']
        choice = choicebox(msg=intro_message, title='EasyGui ' + eg_version, choices=choices)
        if not choice:
            return
        reply = choice.split()
        if reply[0] == 'msgbox':
            reply = msgbox('short msg', 'This is a long title')
            writeln('Reply was: {!r}'.format(reply))
        elif reply[0] == 'About':
            reply = abouteasygui()
        elif reply[0] == 'Help':
            _demo_help()
        elif reply[0] == 'buttonbox':
            reply = buttonbox(choices=['one', 'two', 'two', 'three'], default_choice='two')
            writeln('Reply was: {!r}'.format(reply))
            title = 'Demo of Buttonbox with many, many buttons!'
            msg = 'This buttonbox shows what happens when you specify too many buttons.'
            reply = buttonbox(msg=msg, title=title, choices=choices, cancel_choice='msgbox')
            writeln('Reply was: {!r}'.format(reply))
        elif reply[0] == 'buttonbox(image)':
            _demo_buttonbox_with_image()
        elif reply[0] == 'boolbox':
            reply = boolbox()
            writeln('Reply was: {!r}'.format(reply))
        elif reply[0] == 'enterbox':
            image = os.path.join(package_dir, 'python_and_check_logo.gif')
            message = 'Enter the name of your best friend.\n(Result will be stripped.)'
            reply = enterbox(message, 'Love!', '     Suzy Smith     ')
            writeln('Reply was: {!r}'.format(reply))
            message = 'Enter the name of your best friend.\n(Result will NOT be stripped.)'
            reply = enterbox(message, 'Love!', '     Suzy Smith     ', strip=False)
            writeln('Reply was: {!r}'.format(reply))
            reply = enterbox('Enter the name of your worst enemy:', 'Hate!')
            writeln('Reply was: {!r}'.format(reply))
        elif reply[0] == 'enterbox(image)':
            image = os.path.join(package_dir, 'python_and_check_logo.gif')
            message = 'What kind of snake is this?'
            reply = enterbox(message, 'Quiz', image=image)
            writeln('Reply was: {!r}'.format(reply))
        elif reply[0] == 'exceptionbox':
            try:
                thisWillCauseADivideByZeroException = 1 / 0
            except:
                exceptionbox()

        elif reply[0] == 'integerbox':
            reply = integerbox('Enter a number between 3 and 333', 'Demo: integerbox WITH a default value', 222, 3, 333)
            writeln('Reply was: {!r}'.format(reply))
            reply = integerbox('Enter a number between 0 and 99', 'Demo: integerbox WITHOUT a default value')
            writeln('Reply was: {!r}'.format(reply))
        elif reply[0] == 'diropenbox':
            _demo_diropenbox()
        elif reply[0] == 'fileopenbox':
            _demo_fileopenbox()
        elif reply[0] == 'filesavebox':
            _demo_filesavebox()
        elif reply[0] == 'indexbox':
            title = reply[0]
            msg = 'Demo of ' + reply[0]
            choices = ['Choice1', 'Choice2', 'Choice3', 'Choice4']
            reply = indexbox(msg, title, choices)
            writeln('Reply was: {!r}'.format(reply))
        elif reply[0] == 'passwordbox':
            reply = passwordbox('Demo of password box WITHOUT default' + '\n\nEnter your secret password', 'Member Logon')
            writeln('Reply was: {!s}'.format(reply))
            reply = passwordbox('Demo of password box WITH default' + '\n\nEnter your secret password', 'Member Logon', 'alfie')
            writeln('Reply was: {!s}'.format(reply))
        elif reply[0] == 'multenterbox':
            msg = 'Enter your personal information'
            title = 'Credit Card Application'
            fieldNames = ['Name', 'Street Address', 'City', 'State', 'ZipCode']
            fieldValues = list()
            fieldValues = multenterbox(msg, title, fieldNames)
            while True:
                if fieldValues is None:
                    break
                errs = list()
                for n, v in zip(fieldNames, fieldValues):
                    if v.strip() == '':
                        errs.append('"{}" is a required field.'.format(n))
                        continue

                if not len(errs):
                    break
                fieldValues = multenterbox('\n'.join(errs), title, fieldNames, fieldValues)

            writeln('Reply was: {}'.format(fieldValues))
        elif reply[0] == 'multpasswordbox':
            msg = 'Enter logon information'
            title = 'Demo of multpasswordbox'
            fieldNames = ['Server ID', 'User ID', 'Password']
            fieldValues = list()
            fieldValues = multpasswordbox(msg, title, fieldNames)
            while True:
                if fieldValues is None:
                    break
                errs = list()
                for n, v in zip(fieldNames, fieldValues):
                    if v.strip() == '':
                        errs.append('"{}" is a required field.\n\n'.format(n))
                        continue

                if not len(errs):
                    break
                fieldValues = multpasswordbox(''.join(errs), title, fieldNames, fieldValues)

            writeln('Reply was: {!s}'.format(fieldValues))
        elif reply[0] == 'ynbox':
            title = 'Demo of ynbox'
            msg = 'Were you expecting the Spanish Inquisition?'
            reply = ynbox(msg, title)
            writeln('Reply was: {!r}'.format(reply))
            if reply:
                msgbox('NOBODY expects the Spanish Inquisition!', 'Wrong!')
        elif reply[0] == 'ccbox':
            msg = 'Insert your favorite message here'
            title = 'Demo of ccbox'
            reply = ccbox(msg, title)
            writeln('Reply was: {!r}'.format(reply))
        elif reply[0] == 'choicebox':
            title = 'Demo of choicebox'
            longchoice = 'This is an example of a very long option which you may or may not wish to choose.' * 2
            listChoices = ['nnn', 'ddd', 'eee', 'fff', 'aaa', longchoice,
             'aaa', 'bbb', 'ccc', 'ggg', 'hhh', 'iii', 'jjj', 'kkk', 'LLL', 'mmm', 'nnn', 'ooo', 'ppp', 'qqq',
             'rrr', 'sss', 'ttt', 'uuu', 'vvv']
            msg = 'Pick something. ' + 'A wrapable sentence of text ?! ' * 30 + '\nA separate line of text.' * 6
            reply = choicebox(msg=msg, choices=listChoices)
            writeln('Reply was: {!r}'.format(reply))
            msg = 'Pick something. '
            reply = choicebox(msg=msg, title=title, choices=listChoices)
            writeln('Reply was: {!r}'.format(reply))
            msg = 'Pick something. '
            reply = choicebox(msg='The list of choices is empty!', choices=list())
            writeln('Reply was: {!r}'.format(reply))
        elif reply[0] == 'multchoicebox':
            listChoices = [
             'aaa', 'bbb', 'ccc', 'ggg', 'hhh', 'iii', 'jjj', 'kkk',
             'LLL', 'mmm', 'nnn', 'ooo', 'ppp', 'qqq',
             'rrr', 'sss', 'ttt', 'uuu', 'vvv']
            msg = 'Pick as many choices as you wish.'
            reply = multchoicebox(msg, 'Demo of multchoicebox', listChoices)
            writeln('Reply was: {!r}'.format(reply))
        elif reply[0] == 'textbox':
            _demo_textbox(reply[0])
        elif reply[0] == 'codebox':
            _demo_codebox(reply[0])
        else:
            msgbox('Choice\n\n{}\n\nis not recognized'.format(choice), 'Program Logic Error')
            return


def _demo_textbox(reply):
    text_snippet = ('It was the best of times, and it was the worst of times.  The rich ate cake, and the poor had cake recommended to them, but wished only for enough cash to buy bread.  The time was ripe for revolution! ' * 5 + '\n\n') * 10
    title = 'Demo of textbox'
    msg = 'Here is some sample text. ' * 16
    reply = textbox(msg, title, text_snippet)
    writeln('Reply was: {!s}'.format(reply))


def _demo_codebox(reply):
    code_snippet = 'dafsdfa dasflkj pp[oadsij asdfp;ij asdfpjkop asdfpok asdfpok asdfpok' * 3 + '\n' + '# here is some dummy Python code\nfor someItem in myListOfStuff:\n    do something(someItem)\n    do something()\n    do something()\n    if somethingElse(someItem):\n        doSomethingEvenMoreInteresting()\n\n' * 16
    msg = 'Here is some sample code. ' * 16
    reply = codebox(msg, 'Code Sample', code_snippet)
    writeln('Reply was: {!r}'.format(reply))


def _demo_buttonbox_with_image():
    msg = 'Do you like this picture?\nIt is '
    choices = ['Yes', 'No', 'No opinion']
    for image in [
     os.path.join(package_dir, 'python_and_check_logo.gif'),
     os.path.join(package_dir, 'python_and_check_logo.jpg'),
     os.path.join(package_dir, 'python_and_check_logo.png'),
     os.path.join(package_dir, 'zzzzz.gif')]:
        reply = buttonbox(msg + image, image=image, choices=choices)
        writeln('Reply was: {!r}'.format(reply))


def _demo_help():
    savedStdout = sys.stdout
    sys.stdout = capturedOutput = StringIO()
    print(globals()['__doc__'])
    sys.stdout = savedStdout
    codebox('EasyGui Help', text=capturedOutput.getvalue())


def _demo_filesavebox():
    filename = 'myNewFile.txt'
    title = 'File SaveAs'
    msg = 'Save file as:'
    f = filesavebox(msg, title, default=filename)
    writeln('You chose to save file: {}'.format(f))


def _demo_diropenbox():
    title = 'Demo of diropenbox'
    msg = 'Pick the directory that you wish to open.'
    d = diropenbox(msg, title)
    writeln('You chose directory...: {}'.format(d))
    d = diropenbox(msg, title, default='./')
    writeln('You chose directory...: {}'.format(d))
    d = diropenbox(msg, title, default='c:/')
    writeln('You chose directory...: {}'.format(d))


def _demo_fileopenbox():
    msg = 'Python files'
    title = 'Open files'
    default = '*.py'
    f = fileopenbox(msg, title, default=default)
    writeln('You chose to open file: {}'.format(f))
    default = './*.gif'
    msg = 'Some other file types (Multi-select)'
    filetypes = ['*.jpg', ['*.zip', '*.tgs', '*.gz', 'Archive files'], ['*.htm', '*.html', 'HTML files']]
    f = fileopenbox(msg, title, default=default, filetypes=filetypes, multiple=True)
    writeln('You chose to open file: %s' % f)


EASYGUI_ABOUT_INFORMATION = '\n========================================================================\n0.97(2014-12-20)\n========================================================================\nWe are happy to release version 0.97 of easygui.  The intent of this release is to address some basic\nfunctionality issues as well as improve easygui in the ways people have asked.\n\nRobert Lugg (me) was searching for a GUI library for my python work.  I saw easygui and liked very much its\nparadigm.  Stephen Ferg, the creator and developer of easygui, graciously allowed me to start development\nback up.  With the help of Alexander Zawadzki, Horst Jens, and others I set a goal to release before the\nend of 2014.\n\nWe rely on user feedback so please bring up problems, ideas, or just say how you are using easygui.\n\nBUG FIXES\n---------\n * sourceforge #4: easygui docs contain bad references to easygui_pydoc.html\n * sourceforge #6: no index.html in docs download file.  Updated to sphinx which as autolinking.\n * sourceforge #8: unicode issues with file*box.  Fixed all that I knew how.\n * sourceforge #12: Cannot Exit with \'X\'.  Now X and escape either return "cancel_button", if set, or None\n\nENHANCEMENTS\n------------\n * Added ability to specify default_choice and cancel_choice for button widgets (See API docs)\n * True and False are returned instead of 1 and 0 for several boxes\n * Allow user to map keyboard keys to buttons by enclosing a hotkey in square braces like: "Pick [M]e", which would assign\n   keyboard key M to that button.  Double braces hide that character, and keysyms are allowed:\n     [[q]]Exit    Would show Exit on the button, and the button would be controlled by the q key\n     [<F1>]Help   Would show Help on the button, and the button would be controlled by the F1 function key\n   NOTE: We are still working on the exact syntax of these key mappings as Enter, space, and arrows are already being\n         used.\n * Escape and the windows \'X\' button always work in buttonboxes.  Those return None in that case.\n * sourceforge #9: let fileopenbox open multiple files.  Added optional argument \'multiple\'\n * Location of dialogs on screen is preserved.  This isn\'t perfect yet, but now, at least, the dialogs don\'t\n   always reset to their default position!\n * added some, but not all of the bugs/enhancements developed by Robbie Brook:\n   http://all-you-need-is-tech.blogspot.com/2013/01/improving-easygui-for-python.html\n\nKNOWN ISSUES\n------------\n * In the documentation, there were previous references to issues when using the IDLE IDE.  I haven\'t\n   experienced those, but also didn\'t do anything to fix them, so they may still be there.  Please report\n   any problems and we\'ll try to address them\n * I am fairly new to contributing to open source, so I don\'t understand packaging, pypi, etc.  There\n   are likely problems as well as better ways to do things.  Again, I appreciate any help or guidance.\n\nOther Changes (that you likely don\'t care about)\n------------------------------------------------\n * Restructured loading of image files to try PIL first throw error if file doesn\'t exist.\n * Converted docs to sphinx with just a bit of doctest.  Most content was retained from the old site, so\n   there might be some redundancies still.  Please make any suggested improvements.\n * Set up a GitHub repository for development: https://github.com/robertlugg/easygui\n\nEasyGui is licensed under what is generally known as\nthe "modified BSD license" (aka "revised BSD", "new BSD", "3-clause BSD").\nThis license is GPL-compatible but less restrictive than GPL.\n\n========================================================================\n0.96(2010-08-29)\n========================================================================\nThis version fixes some problems with version independence.\n\nBUG FIXES\n------------------------------------------------------\n * A statement with Python 2.x-style exception-handling syntax raised\n   a syntax error when running under Python 3.x.\n   Thanks to David Williams for reporting this problem.\n\n * Under some circumstances, PIL was unable to display non-gif images\n   that it should have been able to display.\n   The cause appears to be non-version-independent import syntax.\n   PIL modules are now imported with a version-independent syntax.\n   Thanks to Horst Jens for reporting this problem.\n\nLICENSE CHANGE\n------------------------------------------------------\nStarting with this version, EasyGui is licensed under what is generally known as\nthe "modified BSD license" (aka "revised BSD", "new BSD", "3-clause BSD").\nThis license is GPL-compatible but less restrictive than GPL.\nEarlier versions were licensed under the Creative Commons Attribution License 2.0.\n\n\n========================================================================\n0.95(2010-06-12)\n========================================================================\n\nENHANCEMENTS\n------------------------------------------------------\n * Previous versions of EasyGui could display only .gif image files using the\n   msgbox "image" argument. This version can now display all image-file formats\n   supported by PIL the Python Imaging Library) if PIL is installed.\n   If msgbox is asked to open a non-gif image file, it attempts to import\n   PIL and to use PIL to convert the image file to a displayable format.\n   If PIL cannot be imported (probably because PIL is not installed)\n   EasyGui displays an error message saying that PIL must be installed in order\n   to display the image file.\n\n   Note that\n   http://www.pythonware.com/products/pil/\n   says that PIL doesn\'t yet support Python 3.x.\n\n\n========================================================================\n0.94(2010-06-06)\n========================================================================\n\nENHANCEMENTS\n------------------------------------------------------\n * The codebox and textbox functions now return the contents of the box, rather\n   than simply the name of the button ("Yes").  This makes it possible to use\n   codebox and textbox as data-entry widgets.  A big "thank you!" to Dominic\n   Comtois for requesting this feature, patiently explaining his requirement,\n   and helping to discover the tkinter techniques to implement it.\n\n   NOTE THAT in theory this change breaks backward compatibility.  But because\n   (in previous versions of EasyGui) the value returned by codebox and textbox\n   was meaningless, no application should have been checking it.  So in actual\n   practice, this change should not break backward compatibility.\n\n * Added support for SPACEBAR to command buttons.  Now, when keyboard\n   focus is on a command button, a press of the SPACEBAR will act like\n   a press of the ENTER key; it will activate the command button.\n\n * Added support for keyboard navigation with the arrow keys (up,down,left,right)\n   to the fields and buttons in enterbox, multenterbox and multpasswordbox,\n   and to the buttons in choicebox and all buttonboxes.\n\n * added highlightthickness=2 to entry fields in multenterbox and\n   multpasswordbox.  Now it is easier to tell which entry field has\n   keyboard focus.\n\n\nBUG FIXES\n------------------------------------------------------\n * In EgStore, the pickle file is now opened with "rb" and "wb" rather than\n   with "r" and "w".  This change is necessary for compatibility with Python 3+.\n   Thanks to Marshall Mattingly for reporting this problem and providing the fix.\n\n * In integerbox, the actual argument names did not match the names described\n   in the docstring. Thanks to Daniel Zingaro of at University of Toronto for\n   reporting this problem.\n\n * In integerbox, the "argLowerBound" and "argUpperBound" arguments have been\n   renamed to "lowerbound" and "upperbound" and the docstring has been corrected.\n\n   NOTE THAT THIS CHANGE TO THE ARGUMENT-NAMES BREAKS BACKWARD COMPATIBILITY.\n   If argLowerBound or argUpperBound are used, an AssertionError with an\n   explanatory error message is raised.\n\n * In choicebox, the signature to choicebox incorrectly showed choicebox as\n   accepting a "buttons" argument.  The signature has been fixed.\n\n\n========================================================================\n0.93(2009-07-07)\n========================================================================\n\nENHANCEMENTS\n------------------------------------------------------\n\n * Added exceptionbox to display stack trace of exceptions\n\n * modified names of some font-related constants to make it\n   easier to customize them\n\n\n========================================================================\n0.92(2009-06-22)\n========================================================================\n\nENHANCEMENTS\n------------------------------------------------------\n\n * Added EgStore class to to provide basic easy-to-use persistence.\n\nBUG FIXES\n------------------------------------------------------\n\n * Fixed a bug that was preventing Linux users from copying text out of\n   a textbox and a codebox.  This was not a problem for Windows users.\n\n'

def abouteasygui():
    """
    shows the easygui revision history
    """
    codebox('About EasyGui\n{}'.format(eg_version), 'EasyGui', EASYGUI_ABOUT_INFORMATION)


if __name__ == '__main__':
    egdemo()