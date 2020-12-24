# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fpga_device_monitor/Popup.py
# Compiled at: 2020-04-09 04:27:42
# Size of source mod 2**32: 1518 bytes
from qtpy.QtWidgets import QMessageBox
import traceback

def _prepare_popup(title: str, message: str, additional_text: str, icon, buttons) -> QMessageBox:
    popup = QMessageBox()
    popup.setWindowTitle(title)
    popup.setText(message)
    popup.setInformativeText(additional_text)
    popup.setIcon(icon)
    popup.setStandardButtons(buttons)
    return popup


def info(title: str, message: str, additional_text: str=''):
    _prepare_popup(title=title, message=message,
      additional_text=additional_text,
      icon=(QMessageBox.Information),
      buttons=(QMessageBox.Ok)).exec()


def alert(title: str, message: str, additional_text: str=''):
    _prepare_popup(title=title, message=message,
      additional_text=additional_text,
      icon=(QMessageBox.Warning),
      buttons=(QMessageBox.Ok)).exec()


def confirm(title: str, message: str, additional_text: str='', on_yes=lambda : None, on_no=lambda : None):
    popup = _prepare_popup(title=title, message=message,
      additional_text=additional_text,
      icon=(QMessageBox.Question),
      buttons=(QMessageBox.Yes | QMessageBox.No))
    on_yes() if popup.exec() == QMessageBox.Yes else on_no()


def error(title: str, ex: Exception):
    alert(title=title, message=(str(ex)),
      additional_text=(traceback.format_exc()))
    raise