# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/rede/util.py
# Compiled at: 2015-09-21 13:34:34
import numpy as np

class Fasor(object):
    Tensao, Corrente, Impedancia, Potencia = range(4)

    def __init__(self, real=None, imag=None, mod=None, ang=None, tipo=None):
        if tipo is None:
            raise Exception('Um tipo precisa ser associado ao Fasor!')
        else:
            self.__tipo = tipo
        self.__base = None
        self.__pu = None
        if not real == None:
            if not imag == None:
                self.__real = real
                self.__imag = imag
                self.__mod = np.absolute(self.__real + self.__imag * complex(0.0, 1.0))
                self.__ang = np.angle(self.__real + self.__imag * complex(0.0, 1.0), deg=1)
            else:
                raise Exception('O parâmetro imag esta vazio!')
        elif not mod == None:
            if not ang == None:
                self.__mod = mod
                self.__ang = ang
                self.__real = self.__mod * np.cos(np.pi / 180.0 * self.__ang)
                self.__imag = self.__mod * np.sin(np.pi / 180.0 * self.__ang)
            else:
                raise Exception('O parâmetro ang esta vazio!')
        else:
            raise Exception('O parâmetro real ou o parâmetro mod prescisam ser passados!')
        return

    @property
    def tipo(self):
        if self.__tipo == 0:
            return 'Tensao'
        if self.__tipo == 1:
            return 'Corrente'
        if self.__tipo == 2:
            return 'Impedancia'
        if self.__tipo == 3:
            return 'Potencia'

    @tipo.setter
    def tipo(self, valor):
        raise Exception('O tipo de um fasor não pode ser alterado!')

    @property
    def base(self):
        if self.__base is None:
            raise Exception('Nenhuma Base está associada ao Fasor!')
        else:
            return self.__base
        return

    @base.setter
    def base(self, valor):
        if not isinstance(valor, Base):
            raise TypeError('O parâmetro base deve ser do tipo Base!')
        else:
            self.__base = valor

    @property
    def pu(self):
        if self.__base is None:
            raise Exception('Uma base deve estar associada ao Fasor!')
        else:
            if self.__tipo == 0:
                return self.mod / self.__base.tensao
            if self.__tipo == 1:
                return self.mod / self.__base.corrente
            if self.__tipo == 2:
                return self.mod / self.__base.impedancia
            if self.__tipo == 3:
                return self.mod / self.__base.potencia
        return

    @pu.setter
    def pu(self, valor):
        raise Exception('Esse valor não pode ser alterado!')

    @property
    def real(self):
        return self.__real

    @real.setter
    def real(self, valor):
        self.__real = valor
        self.__mod = np.absolute(self.__real + self.__imag * complex(0.0, 1.0))
        self.__ang = np.angle(self.__real + self.__imag * complex(0.0, 1.0), deg=1)

    @property
    def imag(self):
        return self.__imag

    @imag.setter
    def imag(self, valor):
        self.__imag = valor
        self.__mod = np.absolute(self.__real + self.__imag * complex(0.0, 1.0))
        self.__ang = np.angle(self.__real + self.__imag * complex(0.0, 1.0), deg=1)

    @property
    def mod(self):
        return self.__mod

    @mod.setter
    def mod(self, valor):
        self.__mod = abs(valor)
        self.__real = self.__mod * np.cos(np.pi / 180.0 * self.__ang)
        self.__imag = self.__mod * np.sin(np.pi / 180.0 * self.__ang)

    @property
    def ang(self):
        return self.__ang

    @ang.setter
    def ang(self, valor):
        self.__ang = valor
        self.__real = self.__mod * np.cos(np.pi / 180.0 * self.__ang)
        self.__imag = self.__mod * np.sin(np.pi / 180.0 * self.__ang)

    def __add__(self, other):
        if not isinstance(other, Fasor):
            raise TypeError('O objeto deve ser do tipo Fasor para proceder a soma!')
        elif not self.tipo == other.tipo:
            raise TypeError('Os fasores devem ser do mesmo tipo para proceder a soma!')
        else:
            return Fasor(real=self.real + other.real, imag=self.imag + other.imag, tipo=self.__tipo)

    def __sub__(self, other):
        if not isinstance(other, Fasor):
            raise TypeError('O objeto deve ser do tipo Fasor para proceder a subtracao!')
        elif not self.tipo == other.tipo:
            raise TypeError('Os fasores devem ser do mesmo tipo para proceder a subtracao!')
        else:
            return Fasor(real=self.real - other.real, imag=self.imag - other.imag, tipo=self.__tipo)

    def __mul__(self, other):
        if not isinstance(other, Fasor):
            raise TypeError('O objeto deve ser do tipo Fasor para proceder a multiplicacao!')
        elif not self.tipo == other.tipo:
            raise TypeError('Os fasores devem ser do mesmo tipo para proceder a multiplicacao!')
        else:
            return Fasor(mod=self.mod * other.mod, ang=self.ang + other.ang, tipo=self.__tipo)

    def __div__(self, other):
        if not isinstance(other, Fasor):
            raise TypeError('O objeto deve ser do tipo Fasor para proceder a divisao!')
        elif not self.tipo == other.tipo:
            raise TypeError('Os fasores devem ser do mesmo tipo para proceder a divisao!')
        else:
            return Fasor(mod=self.mod / other.mod, ang=self.ang - other.ang, tipo=self.__tipo)

    def __str__(self):
        return ('Fasor de {tipo}: {real} + {imag}j').format(tipo=self.tipo, real=self.real, imag=self.imag)


class Base(object):

    def __init__(self, tensao, potencia):
        self.tensao = tensao
        self.potencia = potencia
        self.corrente = self.potencia / (np.sqrt(3) * self.tensao)
        self.impedancia = self.tensao ** 2 / self.potencia

    def __str__(self):
        return ('Base de {tensao} V e potencia {} VA').format(tensao=self.tensao, potencia=self.potencia)


if __name__ == '__main__':
    fasor_1 = Fasor(real=1.0, imag=0.5)
    print fasor_1.real
    print fasor_1.imag