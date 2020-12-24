# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-intel/egg/launchpad_rtmidi_py/launchpad_rtmidi.py
# Compiled at: 2017-09-24 10:51:52
import string, random, sys, time, rtmidi
try:
    from charset import *
except ImportError:
    sys.exit('error loading Launchpad charset')

class Midi():
    instanceMidi = None

    def __init__(self):
        if Midi.instanceMidi is None:
            try:
                Midi.instanceMidi = Midi.__Midi()
            except:
                print 'unable to initialize MIDI'
                Midi.instanceMidi = None

        self.devIn = None
        self.devOut = None
        return

    def __getattr__(self, name):
        return getattr(self.instanceMidi, name)

    def OpenOutput(self, midi_id):
        if self.devOut is None:
            try:
                self.devOut = rtmidi.MidiOut()
                self.devOut.open_port(midi_id)
            except:
                self.devOut = None
                return False

        return True

    def CloseOutput(self):
        if self.devOut is not None:
            self.devOut.close_port()
            self.devOut = None
        return

    def OpenInput(self, midi_id):
        if self.devIn is None:
            try:
                self.devIn = rtmidi.MidiIn()
                self.devIn.open_port(midi_id)
            except:
                self.devIn = None
                return False

        return True

    def CloseInput(self):
        if self.devIn is not None:
            self.devIn.close_port()
            self.devIn = None
        return

    def ReadRaw(self):
        msg = self.devIn.get_message()
        if msg != (None, None):
            return msg
        else:
            return
            return

    def RawWrite(self, stat, dat1, dat2):
        self.devOut.send_message([stat, dat1, dat2])

    def RawWriteMulti(self, lstMessages):
        self.devOut.send_message(lstMessages)

    def RawWriteSysEx(self, lstMessage, timeStamp=0):
        self.devOut.send_message([240] + lstMessage + [247])

    class __Midi:

        def SearchDevices(self, name, output=True, input=True, quiet=True):
            ret = []
            i = 0
            if output == True:
                midi_out = rtmidi.MidiOut()
                for port in midi_out.get_ports():
                    if quiet == False:
                        print (
                         port, 1, 0)
                        sys.stdout.flush()
                    if port.lower().find(name.lower()) >= 0:
                        ret.append(i)
                    i += 1

            if input == True:
                midi_in = rtmidi.MidiIn()
                for port in midi_in.get_ports():
                    if quiet == False:
                        print (
                         port, 0, 1)
                        sys.stdout.flush()
                    if port.lower().find(name.lower()) >= 0:
                        ret.append(i)
                    i += 1

            return ret

        def SearchDevice(self, name, output=True, input=True, number=0):
            ret = self.SearchDevices(name, output, input)
            if number < 0 or number >= len(ret):
                return None
            return ret[number]


class LaunchpadBase(object):

    def __init__(self):
        self.midi = Midi()
        self.idOut = None
        self.idIn = None
        self.SCROLL_NONE = 0
        self.SCROLL_LEFT = -1
        self.SCROLL_RIGHT = 1
        return

    def __delete__(self):
        self.Close()

    def Open(self, number=0, name='Launchpad'):
        self.idOut = self.midi.SearchDevice(name, True, False, number=number)
        self.idIn = self.midi.SearchDevice(name, False, True, number=number)
        if self.idOut is None or self.idIn is None:
            return False
        if self.midi.OpenOutput(self.idOut) == False:
            return False
        else:
            return self.midi.OpenInput(self.idIn)

    def Check(self, number=0, name='Launchpad'):
        self.idOut = self.midi.SearchDevice(name, True, False, number=number)
        self.idIn = self.midi.SearchDevice(name, False, True, number=number)
        if self.idOut is None or self.idIn is None:
            return False
        return True

    def Close(self):
        self.midi.CloseInput()
        self.midi.CloseOutput()

    def ListAll(self):
        self.midi.SearchDevices('*', True, True, False)

    def ButtonFlush(self):
        doReads = 0
        while doReads < 3:
            msg = self.midi.ReadRaw()
            if msg:
                doReads = 0
            else:
                doReads += 1
                time.sleep(0.005)

    def EventRaw(self):
        msg = self.midi.ReadRaw()
        if msg:
            return msg
        else:
            return []


class Launchpad(LaunchpadBase):

    def Reset(self):
        self.midi.RawWrite(176, 0, 0)

    def LedGetColor(self, red, green):
        led = 0
        red = min(int(red), 3)
        red = max(red, 0)
        green = min(int(green), 3)
        green = max(green, 0)
        led |= red
        led |= green << 4
        return led

    def LedCtrlRaw(self, number, red, green):
        if number > 199:
            if number < 208:
                self.LedCtrlAutomap(number - 200, red, green)
        else:
            if number < 0 or number > 120:
                return
            led = self.LedGetColor(red, green)
            self.midi.RawWrite(144, number, led)

    def LedCtrlXY(self, x, y, red, green):
        if x < 0 or x > 8 or y < 0 or y > 8:
            return
        if y == 0:
            self.LedCtrlAutomap(x, red, green)
        else:
            self.LedCtrlRaw(y - 1 << 4 | x, red, green)

    def LedCtrlRawRapid(self, allLeds):
        le = len(allLeds)
        for i in range(0, le, 2):
            self.midi.RawWrite(146, allLeds[i], allLeds[(i + 1)] if i + 1 < le else 0)

    def LedCtrlAutomap(self, number, red, green):
        if number < 0 or number > 7:
            return
        led = self.LedGetColor(red, green)
        self.midi.RawWrite(176, 104 + number, led)

    def LedAllOn(self, colorcode=None):
        if colorcode == 0:
            self.Reset()
        else:
            self.midi.RawWrite(176, 0, 127)

    def LedCtrlChar(self, char, red, green, offsx=0, offsy=0):
        char = ord(char)
        if char < 0 or char > 255:
            return
        char *= 8
        for i in range(0, 128, 16):
            for j in range(8):
                lednum = i + j + offsx
                if lednum >= i and lednum < i + 8:
                    if CHARTAB[char] & 128 >> j:
                        self.LedCtrlRaw(lednum, red, green)
                    else:
                        self.LedCtrlRaw(lednum, 0, 0)

            char += 1

    def LedCtrlString(self, string, red, green, direction=None, waitms=150):
        limit = lambda n, mini, maxi: max(min(maxi, n), mini)
        if direction == self.SCROLL_LEFT:
            string += ' '
            for n in range((len(string) + 1) * 8):
                if n <= len(string) * 8:
                    self.LedCtrlChar(string[limit(n / 16 * 2, 0, len(string) - 1)], red, green, 8 - n % 16)
                if n > 7:
                    self.LedCtrlChar(string[limit((n - 8) / 16 * 2 + 1, 0, len(string) - 1)], red, green, 8 - (n - 8) % 16)
                time.sleep(0.001 * waitms)

        elif direction == self.SCROLL_RIGHT:
            string = ' ' + string + ' '
            for n in range((len(string) + 1) * 8 - 7, 0, -1):
                if n <= len(string) * 8:
                    self.LedCtrlChar(string[limit(n / 16 * 2, 0, len(string) - 1)], red, green, 8 - n % 16)
                if n > 7:
                    self.LedCtrlChar(string[limit((n - 8) / 16 * 2 + 1, 0, len(string) - 1)], red, green, 8 - (n - 8) % 16)
                time.sleep(0.001 * waitms)

        else:
            for i in string:
                for n in range(4):
                    self.LedCtrlChar(i, red, green)
                    time.sleep(0.001 * waitms)

    def ButtonChanged(self):
        return self.midi.Read()

    def ButtonStateRaw(self):
        a = self.midi.ReadRaw()
        if a:
            return [
             a[0][1] if a[0][0] == 144 else a[0][1] + 96, True if a[0][2] > 0 else False]
        return []

    def ButtonStateXY(self):
        a = self.midi.ReadRaw()
        if a:
            if a[0][0] == 144:
                x = a[0][1] & 15
                y = (a[0][1] & 240) >> 4
                return [
                 x, y + 1, True if a[0][2] > 0 else False]
            if a[0][0] == 176:
                return [
                 a[0][1] - 104, 0, True if a[0][2] > 0 else False]
        return []


class LaunchpadPro(LaunchpadBase):
    COLORS = {'black': 0, 'off': 0, 'white': 3, 'red': 5, 'green': 17}

    def Open(self, number=0, name='Pro'):
        retval = super(LaunchpadPro, self).Open(number=number, name=name)
        if retval == True:
            if name.lower() == 'pro':
                self.LedSetMode(0)
        return retval

    def Check(self, number=0, name='Pro'):
        return super(LaunchpadPro, self).Check(number=number, name=name)

    def LedSetLayout(self, mode):
        if mode < 0 or mode > 13:
            return
        self.midi.RawWriteSysEx([0, 32, 41, 2, 16, 34, mode])
        time.sleep(0.01)

    def LedSetMode(self, mode):
        if mode < 0 or mode > 1:
            return
        self.midi.RawWriteSysEx([0, 32, 41, 2, 16, 33, mode])
        time.sleep(0.01)

    def LedSetButtonLayoutSession(self):
        self.LedSetLayout(0)

    def LedGetColorByName(self, name):
        if name in LaunchpadPro.COLORS:
            return LaunchpadPro.COLORS[name]
        else:
            return LaunchpadPro.COLORS['black']

    def LedCtrlRaw(self, number, red, green, blue=None):
        if number < 0 or number > 99:
            return
        if blue is None:
            blue = 0
            red *= 21
            green *= 21
        limit = lambda n, mini, maxi: max(min(maxi, n), mini)
        red = limit(red, 0, 63)
        green = limit(green, 0, 63)
        blue = limit(blue, 0, 63)
        self.midi.RawWriteSysEx([0, 32, 41, 2, 16, 11, number, red, green, blue])
        return

    def LedCtrlRawByCode(self, number, colorcode=None):
        if number < 0 or number > 99:
            return
        if colorcode is None:
            colorcode = LaunchpadPro.COLORS['white']
        self.midi.RawWrite(144, number, colorcode)
        return

    def LedCtrlXY(self, x, y, red, green, blue=None, mode='classic'):
        if x < 0 or x > 9 or y < 0 or y > 9:
            return
        if mode != 'pro':
            x = (x + 1) % 10
        led = 90 - 10 * y + x
        self.LedCtrlRaw(led, red, green, blue)

    def LedCtrlXYByCode(self, x, y, colorcode, mode='classic'):
        if x < 0 or x > 9 or y < 0 or y > 9:
            return
        if mode != 'pro':
            x = (x + 1) % 10
        led = 90 - 10 * y + x
        self.LedCtrlRawByCode(led, colorcode)

    def LedCtrlXYByRGB(self, x, y, lstColor, mode='classic'):
        if type(lstColor) is not list or len(lstColor) < 3:
            return
        if x < 0 or x > 9 or y < 0 or y > 9:
            return
        if mode.lower() != 'pro':
            x = (x + 1) % 10
        led = 90 - 10 * y + x
        self.LedCtrlRaw(led, lstColor[0], lstColor[1], lstColor[2])

    def LedCtrlChar(self, char, red, green, blue=None, offsx=0, offsy=0):
        char = ord(char)
        char = min(char, 255)
        char = max(char, 0) * 8
        if blue is None:
            red *= 21
            green *= 21
            blue = 0
        for i in range(81, 1, -10):
            for j in range(8):
                sum = i + j + offsx
                if sum >= i and sum < i + 8:
                    if CHARTAB[char] & 128 >> j:
                        self.LedCtrlRaw(sum, red, green, blue)
                    else:
                        self.LedCtrlRaw(sum, 0, 0, 0)

            char += 1

        return

    def LedCtrlString(self, string, red, green, blue=None, direction=None, waitms=150):
        if blue is None:
            red *= 21
            green *= 21
            blue = 0
        limit = lambda n, mini, maxi: max(min(maxi, n), mini)
        if direction == self.SCROLL_LEFT:
            string += ' '
            for n in range((len(string) + 1) * 8):
                if n <= len(string) * 8:
                    self.LedCtrlChar(string[limit(n / 16 * 2, 0, len(string) - 1)], red, green, blue, 8 - n % 16)
                if n > 7:
                    self.LedCtrlChar(string[limit((n - 8) / 16 * 2 + 1, 0, len(string) - 1)], red, green, blue, 8 - (n - 8) % 16)
                time.sleep(0.001 * waitms)

        elif direction == self.SCROLL_RIGHT:
            string = ' ' + string + ' '
            for n in range((len(string) + 1) * 8 - 7, 0, -1):
                if n <= len(string) * 8:
                    self.LedCtrlChar(string[limit(n / 16 * 2, 0, len(string) - 1)], red, green, blue, 8 - n % 16)
                if n > 7:
                    self.LedCtrlChar(string[limit((n - 8) / 16 * 2 + 1, 0, len(string) - 1)], red, green, blue, 8 - (n - 8) % 16)
                time.sleep(0.001 * waitms)

        else:
            for i in string:
                for n in range(4):
                    self.LedCtrlChar(i, red, green, blue)
                    time.sleep(0.001 * waitms)

        return

    def LedAllOn(self, colorcode=None):
        if colorcode is None:
            colorcode = LaunchpadPro.COLORS['white']
        else:
            colorcode = min(colorcode, 127)
            colorcode = max(colorcode, 0)
        self.midi.RawWriteSysEx([0, 32, 41, 2, 16, 14, colorcode])
        return

    def Reset(self):
        self.LedAllOn(0)

    def ButtonStateRaw(self):
        a = self.midi.ReadRaw()
        if a:
            if a[0] is None:
                return []
            else:
                if a[0][0] == 144 or a[0][0] == 176:
                    return [a[0][1], a[0][2]]
                return []

        else:
            return []
        return

    def ButtonStateXY(self, mode='classic'):
        a = self.midi.ReadRaw()
        if a:
            if a[0][0] == 144 or a[0][0] == 176:
                if mode.lower() != 'pro':
                    x = (a[0][1] - 1) % 10
                else:
                    x = a[0][1] % 10
                y = (99 - a[0][1]) / 10
                return [
                 x, y, a[0][2]]
            else:
                return []

        else:
            return []


class LaunchpadMk2(LaunchpadPro):

    def Open(self, number=0, name='Mk2'):
        return super(LaunchpadMk2, self).Open(number=number, name=name)

    def Check(self, number=0, name='Mk2'):
        return super(LaunchpadMk2, self).Check(number=number, name=name)

    def LedAllOn(self, colorcode=None):
        if colorcode is None:
            colorcode = LaunchpadPro.COLORS['white']
        else:
            colorcode = min(colorcode, 127)
            colorcode = max(colorcode, 0)
        self.midi.RawWriteSysEx([0, 32, 41, 2, 24, 14, colorcode])
        return

    def Reset(self):
        self.LedAllOn(0)

    def ButtonStateXY(self):
        a = self.midi.ReadRaw()
        if a:
            if a[0][0] == 144 or a[0][0] == 176:
                if a[0][1] >= 104:
                    x = a[0][1] - 104
                    y = 0
                else:
                    x = (a[0][1] - 1) % 10
                    y = (99 - a[0][1]) / 10
                return [
                 x, y, a[0][2]]
            else:
                return []

        else:
            return []

    def LedCtrlRaw(self, number, red, green, blue=None):
        number = min(number, 111)
        number = max(number, 0)
        if number > 89 and number < 104:
            return
        else:
            if blue is None:
                blue = 0
                red *= 21
                green *= 21
            limit = lambda n, mini, maxi: max(min(maxi, n), mini)
            red = limit(red, 0, 63)
            green = limit(green, 0, 63)
            blue = limit(blue, 0, 63)
            self.midi.RawWriteSysEx([0, 32, 41, 2, 16, 11, number, red, green, blue])
            return

    def LedCtrlRawByCode(self, number, colorcode=None):
        number = min(number, 111)
        number = max(number, 0)
        if number > 89 and number < 104:
            return
        else:
            if colorcode is None:
                colorcode = LaunchpadPro.COLORS['white']
            if number < 104:
                self.midi.RawWrite(144, number, colorcode)
            else:
                self.midi.RawWrite(176, number, colorcode)
            return

    def LedCtrlXY(self, x, y, red, green, blue=None):
        if x < 0 or x > 8 or y < 0 or y > 8:
            return
        if y == 0:
            led = 104 + x
        else:
            led = 91 - 10 * y + x
        self.LedCtrlRaw(led, red, green, blue)

    def LedCtrlXYByRGB(self, x, y, lstColor):
        if type(lstColor) is not list or len(lstColor) < 3:
            return
        if x < 0 or x > 8 or y < 0 or y > 8:
            return
        if y == 0:
            led = 104 + x
        else:
            led = 91 - 10 * y + x
        self.LedCtrlRaw(led, lstColor[0], lstColor[1], lstColor[2])

    def LedCtrlXYByCode(self, x, y, colorcode):
        if x < 0 or x > 8 or y < 0 or y > 8:
            return
        if y == 0:
            led = 104 + x
        else:
            led = 91 - 10 * y + x
        self.LedCtrlRawByCode(led, colorcode)


class LaunchControlXL(LaunchpadBase):

    def Open(self, number=0, name='Control XL', template=0):
        self.UserTemplate = template
        retval = super(LaunchControlXL, self).Open(number=number, name=name)
        if retval == True:
            self.TemplateSet(self.UserTemplate)
        return retval

    def Check(self, number=0, name='Control XL'):
        return super(LaunchpadPro, self).Check(number=number, name=name)

    def TemplateSet(self, templateNum):
        if templateNum < 1 or templateNum > 16:
            return
        self.midi.RawWriteSysEx([0, 32, 41, 2, 17, 119, templateNum - 1])

    def Reset(self):
        self.midi.RawWrite(176, 0, 0)

    def LedAllOn(self, colorcode=None):
        if colorcode is None or colorcode == 0:
            self.Reset()
        else:
            self.midi.RawWrite(176, 0, 127)
        return

    def LedGetColor(self, red, green):
        led = 0
        red = min(int(red), 3)
        red = max(red, 0)
        green = min(int(green), 3)
        green = max(green, 0)
        led |= red
        led |= green << 4
        return led

    def LedCtrlRaw(self, number, red, green):
        led = self.LedGetColor(red, green)
        self.midi.RawWrite(144, number, led)

    def LedCtrlXY(self, x, y, red, green):
        if x < 0 or x > 9 or y < 0 or y > 6:
            return
        if x < 8:
            color = self.LedGetColor(red, green)
        else:
            color = self.LedGetColor(3, 3)
        if x < 8:
            if y < 3:
                index = y * 8 + x
            elif y > 3 and y < 6:
                index = (y - 1) * 8 + x
            else:
                return
        elif x == 8:
            if y > 2:
                index = 37 + y
            elif y == 1:
                index = 44
            elif y == 2:
                index = 46
            else:
                return
        elif x == 9:
            if y > 2:
                index = 37 + y
            elif y == 1:
                index = 45
            elif y == 2:
                index = 47
            else:
                return
        self.midi.RawWriteSysEx([0, 32, 41, 2, 17, 120, 0, index, color])

    def InputFlush(self):
        return self.ButtonFlush()

    def InputStateRaw(self):
        a = self.midi.ReadRaw()
        if a:
            if a[0][0] == 144:
                return [a[0][1], True, 127]
            if a[0][0] == 128:
                return [a[0][1], False, 0]
            if a[0][0] == 176:
                if a[0][1] >= 104 and a[0][1] <= 107:
                    if a[0][2] > 0:
                        return [a[0][1], True, a[0][2]]
                    else:
                        return [
                         a[0][1], False, 0]

                else:
                    return [
                     a[0][1], a[0][2], 0]
            else:
                return []
        else:
            return []


class LaunchKeyMini(LaunchpadBase):

    def Open(self, number=0, name='LaunchKey'):
        retval = super(LaunchKeyMini, self).Open(number=number, name=name)
        return retval

    def Check(self, number=0, name='LaunchKey'):
        return super(LaunchKeyMini, self).Check(number=number, name=name)

    def InputStateRaw(self):
        a = self.midi.ReadRaw()
        if a:
            if a[0][0] == 144:
                return [a[0][1], True, a[0][2]]
            if a[0][0] == 128:
                return [a[0][1], False, 0]
            if a[0][0] == 153:
                return [a[0][1], True, a[0][2]]
            if a[0][0] == 137:
                return [a[0][1], False, 0]
            if a[0][0] == 176:
                if a[0][1] >= 104 and a[0][1] <= 109:
                    if a[0][2] > 0:
                        return [a[0][1], True, 127]
                    else:
                        return [
                         a[0][1], False, 0]

                else:
                    return [
                     a[0][1], a[0][2], 0]
            else:
                return []
        else:
            return []

    def InputFlush(self):
        return self.ButtonFlush()


class Dicer(LaunchpadBase):

    def Open(self, number=0, name='Dicer'):
        retval = super(Dicer, self).Open(number=number, name=name)
        return retval

    def Check(self, number=0, name='Dicer'):
        return super(Dicer, self).Check(number=number, name=name)

    def Reset(self):
        self.midi.RawWrite(186, 0, 0)

    def LedAllOff(self):
        self.midi.RawWrite(186, 0, 112)

    def ButtonStateRaw(self):
        a = self.midi.ReadRaw()
        if a:
            if a[0][0] >= 154 and a[0][0] <= 156:
                butNum = a[0][1]
                if butNum >= 60 and butNum <= 69:
                    butNum -= 59
                    butNum += 10 * (a[0][0] - 154)
                    if a[0][2] == 127:
                        return [butNum, True, 127]
                    return [butNum, False, 0]
                else:
                    return []
            elif a[0][0] >= 157 and a[0][0] <= 159:
                butNum = a[0][1]
                if butNum >= 60 and butNum <= 69:
                    butNum -= 59
                    butNum += 100 + 10 * (a[0][0] - 157)
                    if a[0][2] == 127:
                        return [butNum, True, 127]
                    return [butNum, False, 0]
                else:
                    return []
        else:
            return []

    def LedSetLightshow(self, device, enable):
        self.midi.RawWrite(186 if device == 0 else 189, 0, 40 if enable == True else 41)

    def LedCtrlRaw(self, number, hue, intensity):
        if number < 0 or number > 130:
            return
        if number > 100:
            number -= 100
            cmd = 157
        else:
            cmd = 154
        page = number / 10
        if page > 2:
            return
        number = number - page * 10
        if number > 10:
            return
        hue = min(int(hue), 7)
        hue = max(hue, 0)
        intensity = min(int(intensity), 15)
        intensity = max(intensity, 0)
        self.midi.RawWrite(cmd + page, number + 59, hue << 4 | intensity)

    def ModeSet(self, device, mode):
        if device < 0 or device > 1:
            return
        if mode < 0 or mode > 6:
            return
        self.midi.RawWrite(186 if device == 0 else 189, 17, mode)