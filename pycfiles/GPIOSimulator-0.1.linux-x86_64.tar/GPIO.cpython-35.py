# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/js/prog/hoerkules/software/core/env/lib/python3.5/site-packages/RPiSim/GPIO.py
# Compiled at: 2016-09-08 16:22:38
# Size of source mod 2**32: 15582 bytes
from tkinter import *
import tkinter as tk, threading, time
from .PIN import PIN
from .TypeChecker import typeassert
dictionaryPins = {}
dictionaryPinsTkinter = {}
GPIONames = [
 '14', '15', '18', '23', '24', '25', '8', '7', '12', '16', '20', '21', '2', '3', '4', '17', '27', '22', '10', '9', '11', '5', '6', '13', '19', '26']

class App(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.start()

    def callback(self):
        self.root.quit()

    def run(self):
        global dictionaryPinsTkinter
        self.root = tk.Tk()
        self.root.wm_title('GPIO EMULATOR')
        self.root.protocol('WM_DELETE_WINDOW', self.callback)
        pin2label = Label(text='5V', fg='red')
        pin2label.grid(row=0, column=0, padx=(10, 10))
        pin4label = Label(text='5V', fg='red')
        pin4label.grid(row=0, column=1, padx=(10, 10))
        pin6label = Label(text='GND', fg='black')
        pin6label.grid(row=0, column=2, padx=(10, 10))
        pin8btn = Button(text='GPIO14\nOUT=0', command='14', padx='1px', pady='1px', bd='0px', fg='blue', relief='sunken', activeforeground='blue')
        pin8btn.grid(row=0, column=3, padx=(10, 10), pady=(5, 5))
        dictionaryPinsTkinter['14'] = pin8btn
        pin10btn = Button(text='GPIO15\nOUT=0', command='15', padx='1px', pady='1px', bd='0px', fg='blue', relief='sunken', activeforeground='blue')
        pin10btn.grid(row=0, column=4, padx=(10, 10))
        dictionaryPinsTkinter['15'] = pin10btn
        pin12btn = Button(text='GPIO18\nOUT=0', command='18', padx='1px', pady='1px', bd='0px', fg='blue', relief='sunken', activeforeground='blue')
        pin12btn.grid(row=0, column=5, padx=(10, 10))
        dictionaryPinsTkinter['18'] = pin12btn
        pin14label = Label(text='GND', fg='black')
        pin14label.grid(row=0, column=6, padx=(10, 10))
        pin16btn = Button(text='GPIO23\nOUT=0', command='23', padx='1px', pady='1px', bd='0px', fg='blue', relief='sunken', activeforeground='blue')
        pin16btn.grid(row=0, column=7, padx=(10, 10))
        dictionaryPinsTkinter['23'] = pin16btn
        pin18btn = Button(text='GPIO24\nOUT=0', command='24', padx='1px', pady='1px', bd='0px', fg='blue', relief='sunken', activeforeground='blue')
        pin18btn.grid(row=0, column=8, padx=(10, 10))
        dictionaryPinsTkinter['24'] = pin18btn
        pin20label = Label(text='GND', fg='black')
        pin20label.grid(row=0, column=9, padx=(10, 10))
        pin22btn = Button(text='GPIO25\nOUT=0', command='25', padx='1px', pady='1px', bd='0px', fg='blue', relief='sunken', activeforeground='blue')
        pin22btn.grid(row=0, column=10, padx=(10, 10))
        dictionaryPinsTkinter['25'] = pin22btn
        pin24btn = Button(text='GPIO8\nOUT=0', command='8', padx='1px', pady='1px', bd='0px', fg='blue', relief='sunken', activeforeground='blue')
        pin24btn.grid(row=0, column=11, padx=(10, 10))
        dictionaryPinsTkinter['8'] = pin24btn
        pin26btn = Button(text='GPIO7\nOUT=0', command='7', padx='1px', pady='1px', bd='0px', fg='blue', relief='sunken', activeforeground='blue')
        pin26btn.grid(row=0, column=12, padx=(10, 10))
        dictionaryPinsTkinter['7'] = pin26btn
        pin28label = Label(text='ID_SC', fg='black')
        pin28label.grid(row=0, column=13, padx=(10, 10))
        pin30label = Label(text='GND', fg='black')
        pin30label.grid(row=0, column=14, padx=(10, 10))
        pin32btn = Button(text='GPIO12\nOUT=0', command='12', padx='1px', pady='1px', bd='0px', fg='blue', relief='sunken', activeforeground='blue')
        pin32btn.grid(row=0, column=15, padx=(10, 10))
        dictionaryPinsTkinter['12'] = pin32btn
        pin34label = Label(text='GND', fg='black')
        pin34label.grid(row=0, column=16, padx=(10, 10))
        pin36btn = Button(text='GPIO16\nOUT=0', command='16', padx='1px', pady='1px', bd='0px', fg='blue', relief='sunken', activeforeground='blue')
        pin36btn.grid(row=0, column=17, padx=(10, 10))
        dictionaryPinsTkinter['16'] = pin36btn
        pin38btn = Button(text='GPIO20\nOUT=0', command='20', padx='1px', pady='1px', bd='0px', fg='blue', relief='sunken', activeforeground='blue')
        pin38btn.grid(row=0, column=18, padx=(10, 10))
        dictionaryPinsTkinter['20'] = pin38btn
        pin40btn = Button(text='GPIO21\nOUT=0', command='21', padx='1px', pady='1px', bd='0px', fg='blue', relief='sunken', activeforeground='blue')
        pin40btn.grid(row=0, column=19, padx=(10, 10))
        dictionaryPinsTkinter['21'] = pin40btn
        pin1label = Label(text='3V3', fg='dark orange')
        pin1label.grid(row=1, column=0, padx=(10, 10), pady=(5, 5))
        pin03btn = Button(text='GPIO2\nOUT=0', command='2', padx='1px', pady='1px', bd='0px', fg='blue', relief='sunken', activeforeground='blue')
        pin03btn.grid(row=1, column=1, padx=(10, 10), pady=(5, 5))
        dictionaryPinsTkinter['2'] = pin03btn
        pin05btn = Button(text='GPIO3\nOUT=0', command='3', padx='1px', pady='1px', bd='0px', fg='blue', relief='sunken', activeforeground='blue')
        pin05btn.grid(row=1, column=2, padx=(10, 10))
        dictionaryPinsTkinter['3'] = pin05btn
        pin07btn = Button(text='GPIO4\nOUT=0', command='4', padx='1px', pady='1px', bd='0px', fg='blue', relief='sunken', activeforeground='blue')
        pin07btn.grid(row=1, column=3, padx=(10, 10))
        dictionaryPinsTkinter['4'] = pin07btn
        pin09label = Label(text='GND', fg='black')
        pin09label.grid(row=1, column=4, padx=(10, 10))
        pin11btn = Button(text='GPIO17\nOUT=0', command='17', padx='1px', pady='1px', bd='0px', fg='blue', relief='sunken', activeforeground='blue')
        pin11btn.grid(row=1, column=5, padx=(10, 10))
        dictionaryPinsTkinter['17'] = pin11btn
        pin13btn = Button(text='GPIO27\nOUT=0', command='27', padx='1px', pady='1px', bd='0px', fg='blue', relief='sunken', activeforeground='blue')
        pin13btn.grid(row=1, column=6, padx=(10, 10))
        dictionaryPinsTkinter['27'] = pin13btn
        pin15btn = Button(text='GPIO22\nOUT=0', command='22', padx='1px', pady='1px', bd='0px', fg='blue', relief='sunken', activeforeground='blue')
        pin15btn.grid(row=1, column=7, padx=(10, 10))
        dictionaryPinsTkinter['22'] = pin15btn
        pin17label = Label(text='3V3', fg='dark orange')
        pin17label.grid(row=1, column=8, padx=(10, 10))
        pin19btn = Button(text='GPIO10\nOUT=0', command='10', padx='1px', pady='1px', bd='0px', fg='blue', relief='sunken', activeforeground='blue')
        pin19btn.grid(row=1, column=9, padx=(10, 10))
        dictionaryPinsTkinter['10'] = pin19btn
        pin21btn = Button(text='GPIO9\nOUT=0', command='9', padx='1px', pady='1px', bd='0px', fg='blue', relief='sunken', activeforeground='blue')
        pin21btn.grid(row=1, column=10, padx=(10, 10))
        dictionaryPinsTkinter['9'] = pin21btn
        pin23btn = Button(text='GPIO11\nOUT=0', command='11', padx='1px', pady='1px', bd='0px', fg='blue', relief='sunken', activeforeground='blue')
        pin23btn.grid(row=1, column=11, padx=(10, 10))
        dictionaryPinsTkinter['11'] = pin23btn
        pin25label = Label(text='GND', fg='black')
        pin25label.grid(row=1, column=12, padx=(10, 10))
        pin27label = Label(text='ID_SD', fg='black')
        pin27label.grid(row=1, column=13, padx=(10, 10))
        pin29btn = Button(text='GPIO5\nOUT=0', command='5', padx='1px', pady='1px', bd='0px', fg='blue', relief='sunken', activeforeground='blue')
        pin29btn.grid(row=1, column=14, padx=(10, 10))
        dictionaryPinsTkinter['5'] = pin29btn
        pin31btn = Button(text='GPIO6\nOUT=0', command='6', padx='1px', pady='1px', bd='0px', fg='blue', relief='sunken', activeforeground='blue')
        pin31btn.grid(row=1, column=15, padx=(10, 10))
        dictionaryPinsTkinter['6'] = pin31btn
        pin33btn = Button(text='GPIO13\nOUT=0', command='13', padx='1px', pady='1px', bd='0px', fg='blue', relief='sunken', activeforeground='blue')
        pin33btn.grid(row=1, column=16, padx=(10, 10))
        dictionaryPinsTkinter['13'] = pin33btn
        pin35btn = Button(text='GPIO19\nOUT=0', command='19', padx='1px', pady='1px', bd='0px', fg='blue', relief='sunken', activeforeground='blue')
        pin35btn.grid(row=1, column=17, padx=(10, 10))
        dictionaryPinsTkinter['19'] = pin35btn
        pin37btn = Button(text='GPIO26\nOUT=0', command='26', padx='1px', pady='1px', bd='0px', fg='blue', relief='sunken', activeforeground='blue')
        pin37btn.grid(row=1, column=18, padx=(10, 10))
        dictionaryPinsTkinter['26'] = pin37btn
        pin39label = Label(text='GND', fg='black')
        pin39label.grid(row=1, column=19, padx=(10, 10))
        self.root.geometry('1300x100+0+0')
        self.root.mainloop()


app = App()

def toggleButton(gpioID):
    global dictionaryPins
    objBtn = dictionaryPinsTkinter[str(gpioID)]
    objPin = dictionaryPins[str(gpioID)]
    if objPin.In == '1':
        objPin.In = '0'
    elif objPin.In == '0':
        objPin.In = '1'
    objBtn['text'] = 'GPIO' + str(gpioID) + '\nIN=' + str(objPin.In)


def buttonClick(self):
    gpioID = self.widget.config('command')[(-1)]
    toggleButton(gpioID)


def buttonClickRelease(self):
    gpioID = self.widget.config('command')[(-1)]
    toggleButton(gpioID)


def drawGPIOOut(gpioID):
    gpioID = str(gpioID)
    objPin = dictionaryPins[gpioID]
    objBtn = dictionaryPinsTkinter[gpioID]
    if objPin.SetMode == 'OUT':
        objBtn['text'] = 'GPIO' + str(gpioID) + '\nOUT=' + str(objPin.Out)
        if str(objPin.Out) == '1':
            objBtn.configure(background='tan2')
            objBtn.configure(activebackground='tan2')
    else:
        objBtn.configure(background='DarkOliveGreen3')
        objBtn.configure(activebackground='DarkOliveGreen3')


def drawBindUpdateButtonIn(gpioID, In):
    objBtn = dictionaryPinsTkinter[gpioID]
    objBtn.configure(background='gainsboro')
    objBtn.configure(activebackground='gainsboro')
    objBtn.configure(relief='raised')
    objBtn.configure(bd='1px')
    objBtn['text'] = 'GPIO' + str(gpioID) + '\nIN=' + str(In)
    objBtn.bind('<Button-1>', buttonClick)
    objBtn.bind('<ButtonRelease-1>', buttonClickRelease)


class GPIO:
    LOW = 0
    HIGH = 1
    OUT = 2
    IN = 3
    PUD_OFF = 4
    PUD_DOWN = 5
    PUD_UP = 6
    BCM = 7
    setModeDone = False

    def checkModeValidator():
        if GPIO.setModeDone == False:
            raise Exception('Setup your GPIO mode. Must be set to BCM')

    @typeassert(int)
    def setmode(mode):
        time.sleep(1)
        if mode == GPIO.BCM:
            GPIO.setModeDone = True
        else:
            GPIO.setModeDone = False

    @typeassert(bool)
    def setwarnings(flag):
        pass

    @typeassert(int, int, int, int)
    def setup(channel, state, initial=-1, pull_up_down=-1):
        GPIO.checkModeValidator()
        if str(channel) not in GPIONames:
            raise Exception('GPIO ' + str(channel) + ' does not exist')
        if str(channel) in dictionaryPins:
            raise Exception('GPIO is already setup')
        if state == GPIO.OUT:
            objTemp = PIN('OUT')
            if initial == GPIO.HIGH:
                objTemp.Out = '1'
            dictionaryPins[str(channel)] = objTemp
            drawGPIOOut(channel)
        elif state == GPIO.IN:
            objTemp = PIN('IN')
            if pull_up_down == -1:
                objTemp.pull_up_down = 'PUD_DOWN'
                objTemp.In = '0'
        if pull_up_down == GPIO.PUD_DOWN:
            objTemp.pull_up_down = 'PUD_DOWN'
            objTemp.In = '0'
        else:
            if pull_up_down == GPIO.PUD_UP:
                objTemp.pull_up_down = 'PUD_UP'
                objTemp.In = '1'
            drawBindUpdateButtonIn(str(channel), objTemp.In)
            dictionaryPins[str(channel)] = objTemp

    @typeassert(int, int)
    def output(channel, outmode):
        channel = str(channel)
        GPIO.checkModeValidator()
        if channel not in dictionaryPins:
            raise Exception('GPIO must be setup before used')
        else:
            objPin = dictionaryPins[channel]
            if objPin.SetMode == 'IN':
                raise Exception('GPIO must be setup as OUT')
            if outmode != GPIO.LOW and outmode != GPIO.HIGH:
                raise Exception('Output must be set to HIGH/LOW')
            objPin = dictionaryPins[channel]
            if outmode == GPIO.LOW:
                objPin.Out = '0'
            elif outmode == GPIO.HIGH:
                objPin.Out = '1'
        drawGPIOOut(channel)

    @typeassert(int)
    def input(channel):
        channel = str(channel)
        GPIO.checkModeValidator()
        if channel not in dictionaryPins:
            raise Exception('GPIO must be setup before used')
        else:
            objPin = dictionaryPins[channel]
        if objPin.SetMode == 'OUT':
            raise Exception('GPIO must be setup as IN')
        objPin = dictionaryPins[channel]
        if objPin.In == '1':
            return True
        if objPin.Out == '0':
            return False

    def cleanup():
        pass