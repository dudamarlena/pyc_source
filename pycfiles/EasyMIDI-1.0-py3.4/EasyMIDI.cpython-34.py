# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/EasyMIDI/EasyMIDI.py
# Compiled at: 2017-10-04 10:11:55
# Size of source mod 2**32: 30589 bytes
from copy import deepcopy
from difflib import SequenceMatcher
import os
from .midiutil.MidiFile import MIDIFile

class MusicTheory:
    __doc__ = 'MusicTheory contains some helpful music theory data, like\n       the major and minor scales based on the circle of fifths.'

    def __init__(self):
        self.notes = [
         'A', 'A#', 'B', 'C', 'C#', 'D', 'D#',
         'E', 'F', 'F#', 'G', 'G#']
        self.sharpFlatTrans = {'C#': 'Db',  'D#': 'Eb',  'F#': 'Gb',  'G#': 'Ab', 
         'A#': 'Bb'}

    @property
    def majorScales(self):
        """Builds the scales for major keys."""
        majKeys = {'C': [],  'G': [
               'F'], 
         'D': [
               'F', 'C'], 
         'A': [
               'F', 'C', 'G'], 
         'E': [
               'F', 'C', 'G', 'D'], 
         'B': [
               'F', 'C', 'G', 'D', 'A'], 
         'F#': [
                'F', 'C', 'G', 'D', 'A', 'E'], 
         'C#': [
                'F', 'C', 'G', 'D', 'A', 'E', 'B'], 
         'G#': [
                'B', 'E', 'A', 'D'], 
         'D#': [
                'B', 'E', 'A'], 
         'A#': [
                'B', 'E'], 
         'F': [
               'B']}
        majScales = {}
        for key in majKeys:
            sharpBaseIdx = []
            for sharpBaseNote in majKeys[key]:
                sharpBaseIdx.append(self.notes.index(sharpBaseNote))

            keyNotes = []
            i = 0
            while i < len(self.notes):
                if i in sharpBaseIdx:
                    i += 1
                    if key in ('G#', 'D#', 'A#', 'F'):
                        keyNotes.append(self.notes[(i - 2)])
                    else:
                        keyNotes.append(self.notes[i])
                    if self.notes[i] not in ('C', 'F'):
                        i += 1
                elif self.notes[i] in ('B', 'E'):
                    keyNotes.append(self.notes[i])
                    i += 1
                else:
                    keyNotes.append(self.notes[i])
                    i += 2

            majScales[key] = keyNotes

        for key, keyNotes in majScales.items():
            rootIndex = keyNotes.index(key)
            majScales[key] = keyNotes[rootIndex:] + keyNotes[:rootIndex]

        for sharp, flat in self.sharpFlatTrans.items():
            majScales[flat] = majScales[sharp]

        return majScales

    @property
    def minorScales(self):
        """Builds the scales for minor keys."""
        minScales = {}
        for key in self.notes:
            keyNotes = self.majorScales[key][:]
            rootIndex = (keyNotes.index(key) + 5) % 7
            minorPos = (rootIndex + 6) % 7
            minorIndex = self.notes.index(keyNotes[minorPos]) + 1
            minorNote = self.notes[(minorIndex % 12)]
            keyNotes[minorPos] = minorNote
            majMinTrans = {'C': 'A',  'G': 'E',  'D': 'B',  'A': 'F#', 
             'E': 'C#',  'B': 'G#',  'F#': 'D#', 
             'C#': 'A#',  'G#': 'F',  'D#': 'C', 
             'A#': 'G',  'F': 'D'}
            minScales[majMinTrans[key]] = keyNotes
            for key, keyNotes in minScales.items():
                rootIndex = keyNotes.index(key)
                minScales[key] = keyNotes[rootIndex:] + keyNotes[:rootIndex]

        for sharp, flat in self.sharpFlatTrans.items():
            minScales[flat] = minScales[sharp]

        return minScales

    def getMajorScales(self):
        """Get the scales for major keys.

        :returns: A dict of major scales (ex. 'C' : ['C', 'D', 'E', ...]).
        :rtype: dict

        """
        return self.majorScales

    def getMinorScales(self):
        """Get the scales for minor keys.

        :returns: A dict of minor scales (ex. 'C' : ['C', 'D', 'E', ...]).
        :rtype: dict

        """
        return self.minorScales


class EasyMIDI:
    __doc__ = 'EasyMIDI handles MIDI files with the help of midiutil.'

    def __init__(self):
        """Initialize a midiutil MIDIFile object."""
        self.midFile = MIDIFile()
        self.channel = 0
        self.track = 0

    def __midNote(self, note):
        """Returns the MIDI number of the note name and octave in a Note object.

        :param note: A Note object.
        :type note: :class:`Note`
        :returns: MIDI number of the Note.
        :rtype: int

        """
        notes = {'C': 0,  'C#': 1,  'Db': 1,  'D': 2,  'D#': 3,  'Eb': 3,  'E': 4, 
         'F': 5,  'F#': 6,  'Gb': 6,  'G': 7,  'G#': 8,  'Ab': 8, 
         'A': 9,  'A#': 10,  'Bb': 10,  'B': 11}
        name = note.getName()
        octave = note.getOctave()
        midNote = notes[name] + (octave + 1) * 12
        return midNote

    def addTracks(self, tracks):
        """Add multiple tracks to the midiutil MIDIFile object.

        :param tracks: A list of tracks.
        :type tracks: list of :class:`Track` objects

        """
        for track in tracks:
            self.addTrack(track)

    def addTrack(self, track):
        """Add a single track/channel to the midiutil MIDIFile object.

        :param track: A Track object.
        :type track: :class:`Track`

        """
        if self.channel > 15:
            print("Sorry, can't add more MIDI tracks because all 16 channels have been occupied.")
            return
        self.channel += 1
        noteList = track.getNotes()
        instrument = track.getInstrument()
        tempo = track.getTempo()
        time = 0
        self.midFile.addTempo(self.track, time, tempo)
        self.midFile.addProgramChange(self.track, self.channel, time, instrument)
        for note in noteList:
            dur = note.getDuration()
            dur *= 4
            vol = note.getVolume()
            if type(note) == Note:
                noteName = note.getName()
                if noteName != 'R':
                    self.midFile.addNote(self.track, self.channel, self._EasyMIDI__midNote(note), time, dur, vol)
            elif type(note) == Chord or type(note) == RomanChord:
                for chordNote in note.getNotes():
                    noteName = chordNote.getName()
                    if noteName != 'R':
                        self.midFile.addNote(self.track, self.channel, self._EasyMIDI__midNote(chordNote), time, dur, vol)
                        continue

            time += dur

    def writeMIDI(self, path):
        """Write the MIDI file to the disk.

        :param path: The path to store the MIDI file at (ex. output.mid).
        :type path: str

        """
        with open(path, 'wb') as (binfile):
            self.midFile.writeFile(binfile)


class Track:
    __doc__ = 'Simple Track class which keeps the list of Notes/Chords, the\n       instrument and the tempo. To be used with :func:`addTrack` or\n       :func:`addTracks` in :class:`EasyMIDI`.'

    def __init__(self, instrument, tempo=120):
        """Initializes a Track object.

        :param instrument: A midi instrument name.
        :type instrument: str
        :param tempo: The tempo of the track.
        :type tempo: int

        """
        self.noteList = []
        self.instrumentDict = {}
        path = os.path.join(os.path.dirname(__file__), 'data/instruments.tsv')
        with open(path) as (instruments):
            for i in instruments:
                midiNr, instr = i.split('\t')
                self.instrumentDict[instr.strip().lower()] = int(midiNr)

        self.instrument = self.matchInstrument(instrument)
        self.tempo = tempo

    def addNotes(self, notes):
        """Add a list of Notes or Chords to the Track.

        :param notes: The list of Notes or Chords, or single Notes or Chords.
        :type notes: :class:`Note` or :class:`Chord` in list or single objects

        """
        if type(notes) == list:
            self.noteList.extend(notes)
        else:
            self.noteList.append(notes)

    def addNote(self, note):
        """Is identical to :func:`addNotes`."""
        self.addNotes(note)

    def addChord(self, chord):
        """Is identical to :func:`addNotes`."""
        self.addNotes(chord)

    def addChords(self, chords):
        """Is identical to :func:`addNotes`."""
        self.addNotes(chords)

    def matchInstrument(self, description):
        """(Fuzzy) matches instrument descriptions to MIDI program numbers.

        :param description: The instrument description (ex. acoustic grand).
        :type description: str

        """
        description = description.strip().lower()
        if description in self.instrumentDict:
            return self.instrumentDict[description] - 1
        ratio = 0
        bestMatch = 0
        for instrumentName in self.instrumentDict:
            r = 0
            for subStr in description.split():
                bestRat = 0
                for subStr2 in instrumentName.split():
                    if subStr == subStr2:
                        bestRat = 1
                        break
                    newRat = SequenceMatcher(None, subStr, subStr2).ratio()
                    if newRat > bestRat:
                        bestRat = newRat
                        continue

                r += bestRat

            if r > ratio:
                ratio = r
                bestMatch = self.instrumentDict[instrumentName]
                continue

        for instrumentName in self.instrumentDict:
            if self.instrumentDict[instrumentName] == bestMatch:
                print('Warning: The instrument "{}" isn\'t available as MIDI program name. Selected "{}" instead.'.format(description, instrumentName))
                continue

        return bestMatch - 1

    def getNotes(self):
        """Returns a copy of the notes of this Track.

        :returns: A list of Chord and Note objects.
        :rtype: list of :class:`Chord` or :class:`Note`.

        """
        return deepcopy(self.noteList)

    def getTempo(self):
        """Returns the tempo of this Track.

        :returns: The tempo.
        :rtype: int

        """
        return self.tempo

    def getInstrument(self):
        """Returns the instrument of this Track.

        :returns: The instrument.
        :rtype: str

        """
        return self.instrument


class Note:
    __doc__ = 'The Note class contains musical notes and their properties,\n       like octave, duration and volume.'

    def __init__(self, name, octave=4, duration=0.25, volume=100):
        """Initializes a Note object.

        :param name: The name of the note (ex. C).
        :type name: str
        :param octave: The octave of the note (1-7).
        :type octave: int
        :param duration: The duration of the note (ex. 1/4 is quarter note).
        :type duration: float or int
        :param volume: The volume of the note (0 to 100)
        :type volume: int

        """
        allowedNames = [
         'C', 'C#', 'Db', 'D', 'D#', 'Eb', 'E', 'F', 'F#',
         'Gb', 'G', 'G#', 'Ab', 'A', 'A#', 'Bb', 'B', 'R']
        if name not in allowedNames:
            raise ValueError('The provided note name is not a valid music note name. Please use C, C#, Db, D, D#, Eb, E, F, F#, Gb, G, G#, Ab, A, A#, Bb, B, or R (rest).')
        self.name = name
        self.duration = duration
        if octave < 1:
            raise ValueError('The provided octave is too low. Please select an octave between 1 and 7 (including).')
        elif octave > 8:
            raise ValueError('The provided octave is too high. Please select an octave between 1 and 7 (including).')
        self.octave = octave
        self.volume = volume

    def getName(self):
        """Returns the name of the note.

        :returns: Current name (ex. C).
        :rtype: str

        """
        return self.name

    def getDuration(self):
        """Returns the duration of the note.

        :returns: Current duration (ex. 1/4).
        :rtype: float or int

        """
        return self.duration

    def getOctave(self):
        """Returns the octave of the note.

        :returns: Current octave (ex. 4).
        :rtype: int

        """
        return self.octave

    def getVolume(self):
        """Returns the volume of the note.

        :returns: Current volume (ex. 80).
        :rtype: int

        """
        return self.volume

    def setName(self, name):
        """Sets the name of the note to name.

        :param name: The new name (ex. C).
        :type name: str

        """
        self.name = name

    def setDuration(self, duration):
        """Sets the duration of the note to duration.

        :param duration: The new duration (ex. 1/4).
        :type duration: float or int

        """
        self.duration = duration

    def setOctave(self, octave):
        """Sets the octave of the note to octave.
        :param octave: The new octave (1-7).
        :type octave: int
        """
        self.octave = octave

    def setVolume(self, volume):
        """Sets the volume of the note to volume.

        :param volume: The new volume (0-100).
        :type volume: int

        """
        self.volume = volume

    def __eq__(self, other):
        """For checking if two Notes are equal to each other."""
        if isinstance(other, Note):
            return self.name == other.getName() and self.duration == other.getDuration() and self.octave == other.getOctave() and self.volume == other.getVolume()
        return NotImplemented

    def __ne__(self, other):
        """For checking if two Notes are not equal to each other."""
        return not self.__eq__(other)

    def __hash__(self):
        """For checking if two Notes are not equal to each other."""
        return hash((self.name, self.octave, self.volume))


class Chord:
    __doc__ = 'The Chord is a simple class that contains lists of Notes.'

    def __init__(self, noteList=[]):
        """Initializes a Chord object.

        :param noteList: A list of Notes that should form a chord.
        :type noteList: list of :class:`Note`

        """
        self.noteList = self._Chord__orderedSet(noteList)

    def getNotes(self):
        """
        Gets the Notes of the chord.

        :returns: The list of Notes of the Chord.
        :rtype: list of :class:`Note`

        """
        return deepcopy(self.noteList)

    def __orderedSet(self, seq):
        """Makes sure the Chord contains no duplicate Notes and that the
           Note order keeps preserved."""
        seen = set()
        seen_add = seen.add
        return [x for x in seq if not (x in seen or seen_add(x))]

    def getDuration(self):
        """Returns the duration of the longest Chord note.

        :returns: The duration.
        :rtype: float or int

        """
        highestDur = 0
        for note in self.noteList:
            curDur = note.getDuration()
            if curDur > highestDur:
                highestDur = curDur
                continue

        return highestDur

    def getVolume(self):
        """Returns the volume of the loudest Chord note.

        :returns: The volume.
        :rtype: int

        """
        highestVol = 0
        for note in self.noteList:
            curVol = note.getVolume()
            if curVol > highestVol:
                highestVol = curVol
                continue

        return highestVol

    def setNotes(self, noteList):
        """Sets the Chord notes to the Notes in noteList.

        :param noteList: A list of notes that should form a chord.

        """
        self.noteList = self._Chord__orderedSet(noteList)

    def setDuration(self, duration):
        """Sets the duration of the note to duration.

        :param duration: The new duration (ex. 1/4).
        :type duration: float or int

        """
        for note in self.noteList:
            note.setDuration(duration)

    def setOctave(self, octave):
        """Sets the octave of the note to octave.

        :param octave: The new octave (1-7).
        :type octave: int

        """
        self.octave = octave
        for note in self.noteList:
            note.setOctave(octave)

    def setVolume(self, volume):
        """Sets the volume of the note to volume.

        :param volume: The new volume (0-100).
        :type volume: int

        """
        for note in self.noteList:
            note.setVolume(volume)

    def addNote(self, note):
        """Adds a note to the Chord.

        :param note: The note to add.
        :param type: :class:`Note`

        """
        self.noteList.append(note)
        self.noteList = self._Chord__orderedSet(self.noteList)

    def removeNote(self, note):
        """Removes a note from the Chord.

        :param note: The note to remove.
        :param type: :class:`Note`

        """
        self.noteList.remove(note)


class RomanChord(Chord):
    __doc__ = "The RomanChord class supports Roman chord numerals for creating\n       chord progressions in a relatively easy way. It's also possible\n       to customize the numerals with intervals or signs and inversions:\n\n       * I6, I7: add 6th or 7th note interval to I chord\n       * Isus2, Isus4: the suspended chords relative to the I chord\n       * I-, I+: Diminished and augmented I chord\n       * Imaj7, Imin7, Idom7: major, minor and dominant 7th chord from I\n       * I*, I**: first and second inversion of the I chord, can be\n         combined with the other customizations (ex. Isus2**)\n\n       Full code example::\n\n          from EasyMIDI import *\n          mid = EasyMIDI()\n          track = Track('acoustic grand')\n          for numeral in ['I', 'IV', 'V', 'I']:\n             track.addChord(RomanChord(numeral))\n          mid.addTrack(track)\n          mid.writeMIDI('output.mid')\n\n    "

    def __init__(self, numeral='I', octave=4, duration=0.25, key='C', major=True, volume=100):
        """Initializes a RomanChord.

        :param numeral: A roman numeral (I, II, III, IV, V, VI or VII)
        :type numeral: str
        :param octave: The octave of the RomanChord (1-7).
        :type octave: int
        :param duration: The duration of the RomanChord (ex. 1/4).
        :type duration: float or int
        :param key: The key of the RomanChord (ex. Ab or G# or D).
        :type key: str
        :param major: If true, use major scale. If false, use minor scale.
        :type major: bool
        :param volume: The volume of the RomanChord (0-100).
        :type volume: int

        """
        self.theory = MusicTheory()
        self.notes = self.theory.notes
        self.majorScales = self.theory.getMajorScales()
        self.minorScales = self.theory.getMinorScales()
        self.numeral = ''
        for c in numeral:
            if c.isupper():
                self.numeral += c
            else:
                break

        self.allowedNumerals = [
         'I', 'II', 'III', 'IV', 'V', 'VI', 'VII']
        if self.numeral not in self.allowedNumerals:
            raise ValueError('The provided Roman numeral is not valid. Please use I, II, III, IV, V, VI or VII.')
        self.numeralRest = numeral.replace(self.numeral, '')
        Chord.__init__(self)
        self.key = key
        if major:
            self.scale = self.majorScales[self.key]
        else:
            self.scale = self.minorScales[self.key]
        self.major = major
        self.duration = duration
        self.octave = octave
        self.volume = volume
        self._numeralToChord()

    def _numeralToChord(self):
        """Converts a roman numeral chord to Notes to add to this Chord."""
        self.noteList = []
        intervals = [
         1, 3, 5]
        inversion = 0
        numeralRest = self.numeralRest
        if numeralRest:
            try:
                if '*' in str(numeralRest):
                    inversion = numeralRest.count('*')
                    numeralRest = numeralRest.replace('*', '')
                numeralRest = int(numeralRest)
            except ValueError:
                if numeralRest == 'sus2':
                    intervals = [
                     1, 2, 5]
                else:
                    if numeralRest == 'sus4':
                        intervals = [
                         1, 4, 5]
                    else:
                        if numeralRest == 'dom7':
                            intervals.append('7-')
                        else:
                            if numeralRest == 'maj7':
                                intervals.append(7)
                            else:
                                if numeralRest in ('min7', 'm7'):
                                    intervals = [1, '3-', 5, '7-']
                                else:
                                    if numeralRest == '-':
                                        intervals = [1, '3-', '5-']
                                    elif numeralRest == '+':
                                        intervals = [1, 3, '5+']

            if isinstance(numeralRest, int):
                if numeralRest > 14:
                    raise ValueError('The provided octave chord numeral interval is too high. Please select one between 1 and 14 (including), like V1 or V14.')
                if numeralRest < 1:
                    raise ValueError('The provided octave chord numeral interval is too low. Please select one between 1 and 12 (including), like V1 or V14.')
                intervals.append(numeralRest)
            startIdx = self.allowedNumerals.index(self.numeral)
            startNote = self.scale[startIdx]
            for interval in intervals:
                note, octave = self._intervalNote(startNote, interval)
                self.addNote(Note(note, octave, self.duration, self.volume))

            if inversion < 0:
                raise ValueError('Negative inversions are not possible.')
        elif inversion > 0:
            for i in range(inversion):
                lenBefore = len(self.noteList)
                lenAfter = 0
                while lenAfter < lenBefore:
                    firstNote = deepcopy(self.noteList[0])
                    octave = firstNote.getOctave()
                    firstNote.setOctave(octave + 1)
                    if lenAfter == 0:
                        self.noteList = self.noteList[1:]
                    self.addNote(firstNote)
                    lenAfter = len(self.noteList)

    def _intervalNote(self, startNote, interval):
        """Returns the note and octave of an interval given
           the root and the interval."""
        halfStepUp = False
        halfStepDown = False
        try:
            interval = int(interval)
        except ValueError:
            if '-' in interval:
                interval = interval.replace('-', '')
                halfStepDown = True
            else:
                if '+' in interval:
                    interval = interval.replace('+', '')
                    halfStepUp = True
                else:
                    raise ValueError('Invalid interval.')
            interval = int(interval)

        if interval > 14:
            return False
        startIdx = self.scale.index(startNote)
        noteIdx = (startIdx + (interval - 1)) % 7
        note = self.scale[noteIdx]
        octaveSignIdx = 0
        octaveSigns = ['C', 'C#', 'D']
        for octaveSign in octaveSigns:
            if octaveSign in self.scale:
                octaveSignIdx = self.scale.index(octaveSign)
                break

        if octaveSignIdx > 0:
            startIdx += len(self.scale[octaveSignIdx:])
        rootOffset = startIdx + (interval - 1)
        octave = rootOffset // 7 + self.octave
        if halfStepUp:
            note = self.notes[((self.notes.index(note) + 1) % 12)]
            if note == 'C':
                octave += 1
        elif halfStepDown:
            note = self.notes[((self.notes.index(note) - 1) % 12)]
            if note == 'B':
                octave -= 1
        return (
         note, octave)

    def setKey(self, key, major=True):
        """Sets the key of the RomanChord, optionally changes scales.

        :param key: The key of the RomanChord (ex. Ab or G# or D).
        :type key: str
        :param major: If true, use major scale. If false, use minor scale.
        :type major: bool

        """
        self.key = key
        if major:
            self.scale = self.majorScales[self.key]
        else:
            self.scale = self.minorScales[self.key]
        self.major = major
        self._numeralToChord()

    def getNumeral(self):
        """Returns the numeral of the RomanChord.

        :returns: The numeral.
        :rtype: str

        """
        return self.numeral


if __name__ == '__main__':
    from random import choice
    mid = EasyMIDI()
    track1 = Track('acoustic grand')
    track2 = Track('acoustic grand')
    melodyMeasures = 7
    numerals = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII']
    key = choice(MusicTheory().notes)
    for i in range(melodyMeasures):
        chordNr = choice(numerals)
        chord = RomanChord(chordNr + '8', duration=0.25, key=key, octave=3)
        track1.addChord(chord)
        for i in range(3):
            chordNr += '*'
            chord_inv = RomanChord(chordNr + '8', duration=0.25, key=key, octave=2)
            track1.addChord(chord_inv)

        for j in range(16):
            notes = chord.getNotes()
            note = choice(notes)
            note.setDuration(0.0625)
            track2.addNote(note)

    chordName = 'I8'
    for i in range(7):
        chordName += '*'
        chord = RomanChord(chordName, duration=0.0625, key=key, octave=2)
        for note in chord.getNotes():
            track2.addNote(note)

    track2.addChord(RomanChord('I8', duration=1, key=key))
    mid.addTracks([track1, track2])
    mid.writeMIDI('output.mid')