# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fool_house/__main__.py
# Compiled at: 2020-01-15 01:24:19
# Size of source mod 2**32: 563 bytes
from fool_house import schizo_count, from_int_to_schizo_str
print('Welcome to durka shell')
while True:
    command = input('corpsman>').split()
    if command[0] == 'exit':
        break
    if command[0] == 'num':
        print(from_int_to_schizo_str(command[1]))
    elif command[0] == 'help':
        print('Каждый уважающий себя математик должен знать счёт древних шизов')
        for digit in schizo_count:
            print(digit)
        else:
            print('Так считали наши шизопредки')