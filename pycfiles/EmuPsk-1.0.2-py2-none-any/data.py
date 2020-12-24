# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ht/PycharmProjects/THANN/data.py
# Compiled at: 2019-11-28 14:06:38
import numpy as np
from sklearn.model_selection import train_test_split
path = '/home/ht/PycharmProjects/THANN/data/'
path1 = '/home/ht/Desktop/NN/'
z = 9.21
pk = np.loadtxt(path + 'powerspectrum.txt', unpack=True)
pk = pk.T
pk = np.delete(pk, [0, 1, 9], 1)
pk = pk
Nk_bins = np.loadtxt(path + 'no_of_bins.txt', unpack=True)
Nk_bins = Nk_bins.T
Nk_bins = np.delete(Nk_bins, [0, 1, 9], 1)
k = np.loadtxt(path + 'k.txt', unpack=True)
k = np.delete(k, [0, 1, 9])
k = k
params = np.loadtxt(path + 'params.txt', unpack=True)
params = params.T
x_HI = np.loadtxt(path + 'neutral_frac.txt', unpack=True)
x_HI = x_HI / 1000.0
x_HI = x_HI.reshape(len(x_HI), 1)
index = [
 800, 854, 908, 953, 962]
params = np.delete(params, index, axis=0)
params = params
pk = np.delete(pk, index, axis=0)
pk = pk
x_HI = np.delete(x_HI, index, axis=0)
x_HI = x_HI
Nk_bins = np.delete(Nk_bins, index, axis=0)
Nk_bins = Nk_bins
Omega_bh2 = 0.0224
Omega_mh2 = 0.1424
dT_b = 27.0 * x_HI * (Omega_bh2 / 0.023) * np.power(0.15 * (1.0 + z) / (10.0 * Omega_mh2), 0.5)
PK = np.zeros(shape=pk.shape)
for i in range(len(pk[:])):
    PK[i] = k ** 3 * pk[i] / (2 * np.pi ** 2)
    PK[i] = PK[i] * dT_b[i] ** 2

cov = PK / Nk_bins ** (1.0 / 2.0)
inde = [
 23, 24, 25, 26, 808, 809, 810, 811, 812, 813, 814, 815, 816,
 817, 818, 819, 820, 821, 822, 823, 824, 825, 826, 827, 828, 829,
 830, 831, 832, 833, 834, 835, 836, 837, 838, 839, 840, 841, 842,
 843, 844, 845, 846, 847, 848, 849, 850, 851, 852, 853, 854, 855,
 856, 857, 858, 859, 860, 861, 862, 863, 864, 865, 866, 867, 868,
 869, 870, 871, 872, 873, 874, 875, 876, 877, 878, 879, 880, 881,
 882, 883, 884, 885, 886, 887, 888, 889, 890, 891, 892, 893, 894,
 895, 896, 897, 898, 899, 900, 901, 902, 903, 904, 905, 906, 907,
 908, 909, 910, 911, 912, 913, 914, 915, 916, 917, 918, 919, 920,
 921, 922, 923, 924, 925, 926, 927, 928, 929, 930, 931, 932, 933,
 934, 935, 936, 937, 938, 939, 940, 941, 942, 943, 944, 945, 946,
 947, 948, 949, 950, 951, 952, 953, 954, 955, 956, 957, 958, 959,
 960, 961, 962, 963, 964, 965]
i_2 = [
 0, 1, 2, 3, 4, 8, 13, 17, 22, 26, 31, 35, 40,
 44, 52, 57, 61, 66, 70, 75, 79, 84, 88, 93, 97, 105,
 110, 114, 119, 123, 128, 132, 137, 141, 149, 157]
indexx = np.where(params[:, 0] == 105.0)
cov_inv = np.zeros(shape=(7, 7))
ind = int(input('index between 0 to %d:' % (len(i_2) - 1)))
for i in range(7):
    cov_inv[(i, i)] = 1.0 / cov[indexx[0][ind]][i]

print params[indexx[0][ind]]