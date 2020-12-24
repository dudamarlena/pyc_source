from distutils.core import setup

DESCRIPTION = """\
Python bindings (by Dalen Bernaca) for HawkVoice Direct Interface (HVDI) - cross platform network voice library by Phil Frisbie.

This package allows you to access the low-level functions of HawkVoiceDI and implements
some, more Pythonic,  higher level, classes and functions to make audio encoding/decoding as easy as possible.

The library supports the following compressed audio codecs:
    LPC,
    LPC10,
    CELP,
    GSM,
    ADPCM,
    and U-LAW.

The encoder returns packets ready for UDP transmission (encryption and signing included).
The decoder accepts the packets and even keeps track of correct sequence order for you.

Input data are strings of 8000 Hz sample rate, 16bit, mono, linear PCM audio bytes.
The minimal length of the input audio chunk that is required depends on the used codec.
The library provides you with the Mixer() class that can be used to downsample the data if necessary.
It also allows you to mix audio chunks together, perform audio gain control on them, uninterleave left and right channels
of a stereo input to be used separately and some more useful stuff.

Most simplistic usage possible:
>>> from hvdi import hvdi
>>> import wave
>>> 
>>> inwf = wave.open("input-file.wav", "r")
>>> # We need 16bit audio:
>>> assert inwf.getsampwidth()==2
>>> # Get all audio data:
>>> samples = inwf.readframes(inwf.getnframes())
>>>
>>> m = hvdi.Mixer()
>>> # If file is stereo, turn it to mono by mixing left and right channel together:
>>> if inwf.getnchannels()==2:
>>>     left, right = m.uninterleave(samples)
>>>     # Downsample to 8000 Hz if needed:
>>>     left  = m.resample(left,  inwf.getframerate(), 8000)
>>>     right = m.resample(right, inwf.getframerate(), 8000)
>>>     samples = m.mix(left, right)
>>> else:
>>>     # Downsample to 8000 Hz if needed:
>>>     samples = m.resample(samples, inwf.getframerate(), 8000)
>>> inwf.close()
>>>
>>> # Exercise gain control, just for fun of it:
>>> samples = m.agc(samples, 0.85)
>>>
>>> # Ow, we probably could have skipped boring stuff above and assume the wave file is of the right format!
>>> # But now, let us reencode the input file.
>>> # Encode it to GSM and decode from it to hear how it sounds:
>>> # I already told you that it is simple.
>>> outwf = wave.open("output-file.wav", "w")
>>> outwf.setnchannels(1)
>>> outwf.setsampwidth(2)
>>> outwf.setframerate(8000)
>>>
>>> hvdi.Decode(
>>>     hvdi.IterEncode(samples, "GSM"),
>>>     outstream=outwf)
>>> outwf.close()
>>>

HawkVoiceDI has been tested on the following platforms:
    Win32 (9x, ME, NT 4.0, 2000, XP, CE)
    Linux (various flavors).

The PyHVDI is prepared for:
    Linux and MS Windows for now,
and is tested on the following platforms:
    Ubuntu 14.04,
    Raspbian Stretch,
    Windows XP and on
    Cygwin running on Windows XP.
"""

setup(
    name='PyHVDI',
    version="1.0",
    description='Python bindings for HawkVoice Direct Interface (HVDI) - cross platform network voice library',
    long_description=DESCRIPTION,
    author='Dalen Bernaca',
    author_email='dbernaca@gmail.com',
    url='http://brailleweb.com/cgi-bin/python.py?module=PyHVDI',
    keywords=['HawkVoice', 'HawkVoiceDI', 'HVDI', 'audio codecs', 'encoding', 'decoding', 'GSM', 'LPC', 'LPC10', 'CELP', 'ADPCM', 'ULAW', 'U-Law'],
    packages=['hvdi'],
    package_dir={'hvdi': 'hvdi'},
    package_data={'hvdi': ['*.dll', '*.so']},
    include_package_data=True,
    zip_safe=False,
    license='GPL',
    classifiers=(
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules')
    )
