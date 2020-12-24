# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/site-packages/gmssl/sm2_parameter.py
# Compiled at: 2020-03-10 11:26:45
# Size of source mod 2**32: 1406 bytes
from .sm2 import default_ecc_table
from .sm2_integer import *
sm2_param_entla = '0080'
sm2_param_ida = '31323334353637383132333435363738'
sm2_param_p = default_ecc_table['p']
sm2_param_n = default_ecc_table['n']
sm2_param_a = default_ecc_table['a']
sm2_param_b = default_ecc_table['b']
sm2_param_gx = default_ecc_table['g'][:64]
sm2_param_gy = default_ecc_table['g'][64:]
q = 0
q_prime = False
q_2m = False

def is_q_prime():
    global q_prime
    return q_prime


def is_q_power_of_two():
    global q_2m
    return q_2m


def set_q(a):
    global q
    global q_2m
    global q_prime
    if isPrime_MR(a, 15):
        q = a
        q_prime = True
        if is_Power_of_two(q):
            q_2m = True
        else:
            q_2m = False
    else:
        if is_Power_of_two(a):
            q = a
            q_2m = True
            if isPrime_MR(q, 15):
                q_prime = True
            else:
                q_prime = False
        else:
            print('*** ERROR: q必须为奇素数或2的幂 *** function: set_q')


def get_q():
    return q


def get_a():
    return int(sm2_param_a, 16)


def get_b():
    return int(sm2_param_b, 16)


def get_Gx():
    return int(sm2_param_gx, 16)


def get_Gy():
    return int(sm2_param_gy, 16)


def get_n():
    return int(sm2_param_n, 16)


set_q(int(sm2_param_p, 16))