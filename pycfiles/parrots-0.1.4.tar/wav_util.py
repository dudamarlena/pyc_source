# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/xuming06/Codes/parrots/parrots/utils/wav_util.py
# Compiled at: 2018-08-26 11:22:42
"""
@author:XuMing（xuming624@qq.com)
@description:
"""
import math, wave, matplotlib.pyplot as plt, numpy as np
from python_speech_features import delta
from python_speech_features import mfcc
from scipy.fftpack import fft

def read_wav_data(filename):
    u"""
    读取一个wav文件，返回声音信号的时域谱矩阵和播放时间
    """
    wav = wave.open(filename, 'rb')
    num_frame = wav.getnframes()
    num_channel = wav.getnchannels()
    framerate = wav.getframerate()
    str_data = wav.readframes(num_frame)
    wav.close()
    wave_data = np.fromstring(str_data, dtype=np.short)
    wave_data.shape = (-1, num_channel)
    wave_data = wave_data.T
    return (wave_data, framerate)


def GetMfccFeature(wavsignal, fs):
    feat_mfcc = mfcc(wavsignal[0], fs)
    feat_mfcc_d = delta(feat_mfcc, 2)
    feat_mfcc_dd = delta(feat_mfcc_d, 2)
    wav_feature = np.column_stack((feat_mfcc, feat_mfcc_d, feat_mfcc_dd))
    return wav_feature


def GetFrequencyFeature(wavsignal, fs):
    time_window = 25
    data_input = []
    wav_length = len(wavsignal[0])
    range0_end = int(len(wavsignal[0]) / fs * 1000 - time_window) // 10
    for i in range(0, range0_end):
        p_start = i * 160
        p_end = p_start + 400
        data_line = []
        for j in range(p_start, p_end):
            data_line.append(wavsignal[0][j])

        data_line = fft(data_line) / wav_length
        data_line2 = []
        for fre_sig in data_line:
            data_line2.append(fre_sig.real)
            data_line2.append(fre_sig.imag)

        data_input.append(data_line2[0:len(data_line2) // 2])

    return data_input


def GetFrequencyFeature2(wavsignal, fs):
    time_window = 25
    window_length = fs / 1000 * time_window
    wav_arr = np.array(wavsignal)
    wav_length = wav_arr.shape[1]
    range0_end = int(len(wavsignal[0]) / fs * 1000 - time_window) // 10
    data_input = np.zeros((range0_end, 200), dtype=np.float)
    data_line = np.zeros((1, 400), dtype=np.float)
    for i in range(0, range0_end):
        p_start = i * 160
        p_end = p_start + 400
        data_line = wav_arr[0, p_start:p_end]
        data_line = np.abs(fft(data_line)) / wav_length
        data_input[i] = data_line[0:200]

    return data_input


x = np.linspace(0, 399, 400, dtype=np.int64)
w = 0.54 - 0.46 * np.cos(2 * np.pi * x / 399)

def get_frequency_features(wavsignal, fs):
    time_window = 25
    window_length = fs / 1000 * time_window
    wav_arr = np.array(wavsignal)
    wav_length = wav_arr.shape[1]
    range0_end = int(len(wavsignal[0]) / fs * 1000 - time_window) // 10
    data_input = np.zeros((range0_end, 200), dtype=np.float)
    data_line = np.zeros((1, 400), dtype=np.float)
    for i in range(0, range0_end):
        p_start = i * 160
        p_end = p_start + 400
        data_line = wav_arr[0, p_start:p_end]
        data_line = data_line * w
        data_line = np.abs(fft(data_line)) / wav_length
        data_input[i] = data_line[0:200]

    data_input = np.log(data_input + 1)
    return data_input


def wav_scale(energy):
    u"""
    语音信号能量归一化
    """
    means = energy.mean()
    var = energy.var()
    e = (energy - means) / math.sqrt(var)
    return e


def wav_scale2(energy):
    u"""
    语音信号能量归一化
    """
    maxnum = max(energy)
    e = energy / maxnum
    return e


def wav_scale3(energy):
    u"""
    语音信号能量归一化
    """
    for i in range(len(energy)):
        energy[i] = float(energy[i]) / 100.0

    return energy


def wav_show(wave_data, fs):
    time = np.arange(0, len(wave_data)) * (1.0 / fs)
    plt.plot(time, wave_data)
    plt.show()


def get_wav_list(filename):
    u"""
    读取一个wav文件列表，返回一个存储该列表的字典类型值
    ps:在数据中专门有几个文件用于存放用于训练、验证和测试的wav文件列表
    """
    txt_obj = open(filename, 'r')
    txt_text = txt_obj.read()
    txt_lines = txt_text.split('\n')
    dic_filelist = {}
    list_wavmark = []
    for i in txt_lines:
        if i != '':
            txt_l = i.split(' ')
            dic_filelist[txt_l[0]] = txt_l[1]
            list_wavmark.append(txt_l[0])

    txt_obj.close()
    return (dic_filelist, list_wavmark)


def get_wav_symbol(filename):
    u"""
    读取指定数据集中，所有wav文件对应的语音符号
    返回一个存储符号集的字典类型值
    """
    txt_obj = open(filename, 'r')
    txt_text = txt_obj.read()
    txt_lines = txt_text.split('\n')
    dic_symbol_list = {}
    list_symbolmark = []
    for i in txt_lines:
        if i != '':
            txt_l = i.split(' ')
            dic_symbol_list[txt_l[0]] = txt_l[1:]
            list_symbolmark.append(txt_l[0])

    txt_obj.close()
    return (dic_symbol_list, list_symbolmark)