# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/peoplefinder/TelegramUpload.py
# Compiled at: 2019-02-25 19:39:02
# Size of source mod 2**32: 1188 bytes
import glob, os, numpy as np, telegram
from astropy.table import Table
from tqdm.auto import tqdm
BOT_TOKEN = os.environ.get('PEOPLE_API_TOKEN')

def telegram_upload(savedir, verbose=False, clear=False):
    bot = telegram.Bot(BOT_TOKEN)
    if verbose:
        print('\nSending images to Telegram...\n')
    files = glob.glob(savedir + '*.png')
    data = Table.read(savedir + 'data.csv')
    for file in tqdm(files):
        phone = file[-17:-4]
        phones = np.array(data['phone'])
        status = data[(phones == phone)]['status'][0]
        photo = open(file, 'rb')
        bot.send_photo('@peoplefinder', photo=photo,
          caption=('Phone number: +{0} {1} {2}-{3}\nStatus: {4}\nhttps://api.whatsapp.com/send?phone={5}'.format(phone[0:2], phone[2:4], phone[4:9], phone[9:], status, phone)),
          timeout=60)
        if verbose:
            print('Sending {0}...'.format(phone))
        photo.close()
        if clear:
            os.remove(file)

    del bot