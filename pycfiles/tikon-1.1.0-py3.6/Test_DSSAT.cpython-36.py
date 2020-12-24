# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tikon\Proyectos\Test_DSSAT.py
# Compiled at: 2016-01-05 13:51:41
# Size of source mod 2**32: 1494 bytes
import subprocess
dssat = subprocess.Popen('C:\\DSSAT46\\DSCSM046.EXE MZCER046 B DSSBatch.v45', shell=True,
  stdin=(subprocess.PIPE),
  stdout=(subprocess.PIPE),
  cwd='F:\\Julien\\PhD\\Python\\Resultados_DSSAT')
print(dssat.communicate(input=b'F:\\Plagas_prueba.txt'))
día = 0
dssat.stdin.write(b'F:\\Plagas_prueba.txt')
test = dssat.stdin.write(b'F:\\Plagas_prueba.txt')
print(dssat.stdout)
print(test)
print(día)
dssat.poll()
día += 1