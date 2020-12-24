# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/peoplefinder/Main.py
# Compiled at: 2019-02-17 14:57:23
# Size of source mod 2**32: 1616 bytes
import os, random, shelve, sys
from selenium import webdriver
from .SaveData import savedata
from .GetPhoto import get_photo
from .TelegramUpload import telegram_upload
if __name__ == '__main__':
    while True:
        try:
            _ = shelve.open('../Shelve/peopleData')
        except:
            os.makedirs('../Shelve')
            continue
        else:
            break

    data = shelve.open('../Shelve/peopleData')
    driver = webdriver.Chrome()
    driver.get('https://web.whatsapp.com')
    input('Press enter once you have logged in... ')
    try:
        i = data['last_indice']
    except KeyError:
        i = 1

    j = sys.argv[1]
    send = sys.argv[2]
    ddd = sys.argv[3]
    k = 0
    numbers = list()
    while k < int(j):
        print('{0}/{1} => {2:.1f}%'.format(str(k + 1), j, (k + 1) / int(j) * 100))
        number = '55{1}999{0}'.format(random.randint(100000, 999999), ddd)
        control = get_photo(driver, number)
        if control is not None:
            i += 1
            k += 1
            numbers.append(number)
        else:
            k += 1

    savedata(data, numbers, i)
    driver.close()
    if int(send) == 1:
        telegram_upload(data['temp_numbers'])
        data['temp_numbers'] = list()
    data.close()