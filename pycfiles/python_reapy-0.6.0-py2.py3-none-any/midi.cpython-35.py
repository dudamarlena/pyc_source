# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /media/despres/MAIN/Users/despres/Desktop/reaper/scripts/reapy/reapy/core/reaper/midi.py
# Compiled at: 2019-03-01 15:17:23
# Size of source mod 2**32: 2231 bytes
import reapy, reapy.reascript_api as RPR
from reapy.tools import Program

def get_active_editor():
    """
    Return active MIDI editor, or None if no editor is active.

    Returns
    -------
    editor : MIDIEditor or None
        Active MIDI editor, or None if no editor is active.
    """
    editor = reapy.MIDIEditor(RPR.MIDIEditor_GetActive())
    if not editor._is_defined:
        editor = None
    return editor


def get_input_names():
    """
    Return names of all input channels.

    Returns
    -------
    names : list of str
        Names of input channels.
    """
    code = '\n    n_channels = reapy.midi.get_n_inputs()\n    names = [RPR.GetMIDIInputName(i, "", 2048)[2] for i in range(n_channels)]\n    '
    names, = Program(code, 'names').run()
    return names


def get_max_inputs():
    """
    Return maximum number of MIDI inputs.

    Returns
    -------
    max_inputs : int
        Maximum number of MIDI inputs.
    """
    max_inputs = RPR.GetMaxMidiInputs()
    return max_inputs


def get_max_outputs():
    """
    Return maximum number of MIDI outputs.

    Returns
    -------
    max_outputs : int
        Maximum number of MIDI outputs.
    """
    max_outputs = RPR.GetMaxMidiOutputs()
    return max_outputs


def get_n_inputs():
    """
    Return number of MIDI inputs.

    Returns
    -------
    n_inputs : int
        Number of MIDI inputs.
    """
    n_inputs = RPR.GetNumMIDIInputs()
    return n_inputs


def get_n_outputs():
    """
    Return number of MIDI outputs.

    Returns
    -------
    n_outputs : int
        Number of MIDI outputs.
    """
    n_outputs = RPR.GetNumMIDIOutputs()
    return n_outputs


def get_output_names():
    """
    Return names of all output channels.

    Returns
    -------
    names : list of str
        Names of output channels.
    """
    code = '\n    n_channels = reapy.midi.get_n_outputs()\n    names = [RPR.GetMIDIOutputName(i, "", 2048)[2] for i in range(n_channels)]\n    '
    names, = Program(code, 'names').run()
    return names


def reinit():
    """Reset all MIDI devices."""
    RPR.midi_reinit()