# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/pifi/Adafruit_CharLCDPlate.py
# Compiled at: 2014-10-22 23:54:57
from Adafruit_I2C import Adafruit_I2C
from time import sleep

class Adafruit_CharLCDPlate(Adafruit_I2C):
    MCP23017_IOCON_BANK0 = 10
    MCP23017_IOCON_BANK1 = 21
    MCP23017_GPIOA = 9
    MCP23017_IODIRB = 16
    MCP23017_GPIOB = 25
    SELECT = 0
    RIGHT = 1
    DOWN = 2
    UP = 3
    LEFT = 4
    OFF = 0
    RED = 1
    GREEN = 2
    BLUE = 4
    YELLOW = RED + GREEN
    TEAL = GREEN + BLUE
    VIOLET = RED + BLUE
    WHITE = RED + GREEN + BLUE
    ON = RED + GREEN + BLUE
    LCD_CLEARDISPLAY = 1
    LCD_RETURNHOME = 2
    LCD_ENTRYMODESET = 4
    LCD_DISPLAYCONTROL = 8
    LCD_CURSORSHIFT = 16
    LCD_FUNCTIONSET = 32
    LCD_SETCGRAMADDR = 64
    LCD_SETDDRAMADDR = 128
    LCD_DISPLAYON = 4
    LCD_DISPLAYOFF = 0
    LCD_CURSORON = 2
    LCD_CURSOROFF = 0
    LCD_BLINKON = 1
    LCD_BLINKOFF = 0
    LCD_ENTRYRIGHT = 0
    LCD_ENTRYLEFT = 2
    LCD_ENTRYSHIFTINCREMENT = 1
    LCD_ENTRYSHIFTDECREMENT = 0
    LCD_DISPLAYMOVE = 8
    LCD_CURSORMOVE = 0
    LCD_MOVERIGHT = 4
    LCD_MOVELEFT = 0

    def __init__(self, busnum=-1, addr=32, debug=False):
        self.i2c = Adafruit_I2C(addr, busnum, debug)
        self.porta, self.portb, self.ddrb = (0, 0, 16)
        self.i2c.bus.write_byte_data(self.i2c.address, self.MCP23017_IOCON_BANK1, 0)
        self.i2c.bus.write_i2c_block_data(self.i2c.address, 0, [
         63,
         self.ddrb,
         63,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         63,
         0,
         0,
         0,
         0,
         0,
         self.porta,
         self.portb,
         self.porta,
         self.portb])
        self.i2c.bus.write_byte_data(self.i2c.address, self.MCP23017_IOCON_BANK0, 160)
        self.displayshift = self.LCD_CURSORMOVE | self.LCD_MOVERIGHT
        self.displaymode = self.LCD_ENTRYLEFT | self.LCD_ENTRYSHIFTDECREMENT
        self.displaycontrol = self.LCD_DISPLAYON | self.LCD_CURSOROFF | self.LCD_BLINKOFF
        self.write(51)
        self.write(50)
        self.write(40)
        self.write(self.LCD_CLEARDISPLAY)
        self.write(self.LCD_CURSORSHIFT | self.displayshift)
        self.write(self.LCD_ENTRYMODESET | self.displaymode)
        self.write(self.LCD_DISPLAYCONTROL | self.displaycontrol)
        self.write(self.LCD_RETURNHOME)

    flip = (0, 16, 8, 24, 4, 20, 12, 28, 2, 18, 10, 26, 6, 22, 14, 30)

    def out4(self, bitmask, value):
        hi = bitmask | self.flip[(value >> 4)]
        lo = bitmask | self.flip[(value & 15)]
        return [hi | 32, hi, lo | 32, lo]

    pollables = (
     LCD_CLEARDISPLAY, LCD_RETURNHOME)

    def write(self, value, char_mode=False):
        """ Send command/data to LCD """
        if self.ddrb & 16:
            lo = self.portb & 1 | 64
            hi = lo | 32
            self.i2c.bus.write_byte_data(self.i2c.address, self.MCP23017_GPIOB, lo)
            while True:
                self.i2c.bus.write_byte(self.i2c.address, hi)
                bits = self.i2c.bus.read_byte(self.i2c.address)
                self.i2c.bus.write_i2c_block_data(self.i2c.address, self.MCP23017_GPIOB, [lo, hi, lo])
                if bits & 2 == 0:
                    break

            self.portb = lo
            self.ddrb &= 239
            self.i2c.bus.write_byte_data(self.i2c.address, self.MCP23017_IODIRB, self.ddrb)
        bitmask = self.portb & 1
        if char_mode:
            bitmask |= 128
        if isinstance(value, str):
            last = len(value) - 1
            data = []
            for i, v in enumerate(value):
                data.extend(self.out4(bitmask, ord(v)))
                if len(data) >= 32 or i == last:
                    self.i2c.bus.write_i2c_block_data(self.i2c.address, self.MCP23017_GPIOB, data)
                    self.portb = data[(-1)]
                    data = []

        elif isinstance(value, list):
            last = len(value) - 1
            data = []
            for i, v in enumerate(value):
                data.extend(self.out4(bitmask, v))
                if len(data) >= 32 or i == last:
                    self.i2c.bus.write_i2c_block_data(self.i2c.address, self.MCP23017_GPIOB, data)
                    self.portb = data[(-1)]
                    data = []

        else:
            data = self.out4(bitmask, value)
            self.i2c.bus.write_i2c_block_data(self.i2c.address, self.MCP23017_GPIOB, data)
            self.portb = data[(-1)]
        if not char_mode and value in self.pollables:
            self.ddrb |= 16
            self.i2c.bus.write_byte_data(self.i2c.address, self.MCP23017_IODIRB, self.ddrb)

    def begin(self, cols, lines):
        self.currline = 0
        self.numlines = lines
        self.clear()

    def stop(self):
        self.porta = 192
        self.portb = 1
        sleep(0.0015)
        self.i2c.bus.write_byte_data(self.i2c.address, self.MCP23017_IOCON_BANK1, 0)
        self.i2c.bus.write_i2c_block_data(self.i2c.address, 0, [
         63,
         self.ddrb,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         0,
         63,
         0,
         0,
         0,
         0,
         0,
         self.porta,
         self.portb,
         self.porta,
         self.portb])

    def clear(self):
        self.write(self.LCD_CLEARDISPLAY)

    def home(self):
        self.write(self.LCD_RETURNHOME)

    row_offsets = (0, 64, 20, 84)

    def setCursor(self, col, row):
        if row > self.numlines:
            row = self.numlines - 1
        elif row < 0:
            row = 0
        self.write(self.LCD_SETDDRAMADDR | col + self.row_offsets[row])

    def display(self):
        """ Turn the display on (quickly) """
        self.displaycontrol |= self.LCD_DISPLAYON
        self.write(self.LCD_DISPLAYCONTROL | self.displaycontrol)

    def noDisplay(self):
        """ Turn the display off (quickly) """
        self.displaycontrol &= ~self.LCD_DISPLAYON
        self.write(self.LCD_DISPLAYCONTROL | self.displaycontrol)

    def cursor(self):
        """ Underline cursor on """
        self.displaycontrol |= self.LCD_CURSORON
        self.write(self.LCD_DISPLAYCONTROL | self.displaycontrol)

    def noCursor(self):
        """ Underline cursor off """
        self.displaycontrol &= ~self.LCD_CURSORON
        self.write(self.LCD_DISPLAYCONTROL | self.displaycontrol)

    def ToggleCursor(self):
        """ Toggles the underline cursor On/Off """
        self.displaycontrol ^= self.LCD_CURSORON
        self.write(self.LCD_DISPLAYCONTROL | self.displaycontrol)

    def blink(self):
        """ Turn on the blinking cursor """
        self.displaycontrol |= self.LCD_BLINKON
        self.write(self.LCD_DISPLAYCONTROL | self.displaycontrol)

    def noBlink(self):
        """ Turn off the blinking cursor """
        self.displaycontrol &= ~self.LCD_BLINKON
        self.write(self.LCD_DISPLAYCONTROL | self.displaycontrol)

    def ToggleBlink(self):
        """ Toggles the blinking cursor """
        self.displaycontrol ^= self.LCD_BLINKON
        self.write(self.LCD_DISPLAYCONTROL | self.displaycontrol)

    def scrollDisplayLeft(self):
        """ These commands scroll the display without changing the RAM """
        self.displayshift = self.LCD_DISPLAYMOVE | self.LCD_MOVELEFT
        self.write(self.LCD_CURSORSHIFT | self.displayshift)

    def scrollDisplayRight(self):
        """ These commands scroll the display without changing the RAM """
        self.displayshift = self.LCD_DISPLAYMOVE | self.LCD_MOVERIGHT
        self.write(self.LCD_CURSORSHIFT | self.displayshift)

    def leftToRight(self):
        """ This is for text that flows left to right """
        self.displaymode |= self.LCD_ENTRYLEFT
        self.write(self.LCD_ENTRYMODESET | self.displaymode)

    def rightToLeft(self):
        """ This is for text that flows right to left """
        self.displaymode &= ~self.LCD_ENTRYLEFT
        self.write(self.LCD_ENTRYMODESET | self.displaymode)

    def autoscroll(self):
        """ This will 'right justify' text from the cursor """
        self.displaymode |= self.LCD_ENTRYSHIFTINCREMENT
        self.write(self.LCD_ENTRYMODESET | self.displaymode)

    def noAutoscroll(self):
        """ This will 'left justify' text from the cursor """
        self.displaymode &= ~self.LCD_ENTRYSHIFTINCREMENT
        self.write(self.LCD_ENTRYMODESET | self.displaymode)

    def createChar(self, location, bitmap):
        self.write(self.LCD_SETCGRAMADDR | (location & 7) << 3)
        self.write(bitmap, True)
        self.write(self.LCD_SETDDRAMADDR)

    def message(self, text):
        """ Send string to LCD. Newline wraps to second line"""
        lines = str(text).split('\n')
        for i, line in enumerate(lines):
            if i > 0:
                self.write(192)
            self.write(line, True)

    def backlight(self, color):
        c = ~color
        self.porta = self.porta & 63 | (c & 3) << 6
        self.portb = self.portb & 254 | (c & 4) >> 2
        self.i2c.bus.write_byte_data(self.i2c.address, self.MCP23017_GPIOA, self.porta)
        self.i2c.bus.write_byte_data(self.i2c.address, self.MCP23017_GPIOB, self.portb)

    def buttonPressed(self, b):
        return self.i2c.readU8(self.MCP23017_GPIOA) >> b & 1

    def buttons(self):
        return self.i2c.readU8(self.MCP23017_GPIOA) & 31


if __name__ == '__main__':
    lcd = Adafruit_CharLCDPlate()
    lcd.begin(16, 2)
    lcd.clear()
    lcd.message('Adafruit RGB LCD\nPlate w/Keypad!')
    sleep(1)
    col = (
     (
      'Red', lcd.RED), ('Yellow', lcd.YELLOW), ('Green', lcd.GREEN),
     (
      'Teal', lcd.TEAL), ('Blue', lcd.BLUE), ('Violet', lcd.VIOLET),
     (
      'Off', lcd.OFF), ('On', lcd.ON))
    print 'Cycle thru backlight colors'
    for c in col:
        print c[0]
        lcd.clear()
        lcd.message(c[0])
        lcd.backlight(c[1])
        sleep(0.5)

    btn = ((lcd.SELECT, 'Select', lcd.ON),
     (
      lcd.LEFT, 'Left', lcd.RED),
     (
      lcd.UP, 'Up', lcd.BLUE),
     (
      lcd.DOWN, 'Down', lcd.GREEN),
     (
      lcd.RIGHT, 'Right', lcd.VIOLET))
    print 'Try buttons on plate'
    lcd.clear()
    lcd.message('Try buttons')
    prev = -1
    while True:
        for b in btn:
            if lcd.buttonPressed(b[0]):
                if b is not prev:
                    print b[1]
                    lcd.clear()
                    lcd.message(b[1])
                    lcd.backlight(b[2])
                    prev = b
                break