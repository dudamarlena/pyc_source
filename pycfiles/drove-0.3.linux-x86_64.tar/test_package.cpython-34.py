# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ajdiaz/env/drove/lib/python3.4/site-packages/drove/tests/test_package.py
# Compiled at: 2015-02-18 11:04:01
# Size of source mod 2**32: 12507 bytes
import os, sys, unittest
from six import BytesIO, b
from six.moves import urllib
from base64 import b64decode
import drove.package
from drove.util import temp
from drove.package import Package, PackageError, find_package, _FileSum
_test_package_okay_folder = b('\nH4sIAC8j41QAA+2Y36+TMBTH8aoP9sV/oea+zCWwFsowS3zzD/BxiTGEQeH2hksZhZlrchP/dA+b\nJEY3GZOwGM/ngXanbGX5nl+lzJtMFXYtTW0/RKaW1cIaGwYEvt+OPPDZz2OHxV0RsKXLvaWwGBec\n+xb1R3+SIzSmjipKreg+UdHX0/f1rf+jlL/r72SqVlmhKznSHq3ASyFO6s9dftBfuB5bgp0vWcAs\nykba/4/85/rPnfIxJnPHfPkUlfozzGSWHa62KlJNEh0vNo3KE3K4JsrUpI4yQ5xY72QVZZKEIfxI\nFN/JMCTX/kPIII7Ff6frWHv0xT8Uh1/i34c5xv8UfLt52lqz9SuYxjrPZVzravts/Xr/+eAGdOc5\ngcO3N+uXYM1VIc32+dP2ReNc+dmRv+dI/B9MI7aBQ/o/4btt/EMDiP3fFJzWP6kg/pUewQ/O1x8a\nPwH38dYVUP8p6Nc/DFWh6jCERvHCPXrrf6d/V/9dOP65WP+noF///diuX5wJBsc/6M8w/0/CEP0v\nzQR98e+y7vzvCfAB0N/jQYDxPwW3b+iiMdViA4rLYkfLx/pOF+SW2nObxjpRRbaiTZ3a71oL2Hfq\nYZXKIn6/NxIS55Ex9EPnJB/3zjPTm3s4SrxdEQokMqWVjJKZkXn6w9ZSwjfxfcF1GRL/qc6TS94P\nn53/hb8v/Mx1PVjG/D8BF+g/uAyc3/91+gshMP8jCIIgCIIgCIIgyGh8B+gFFk0AKAAA\n')
_test_package_okay_upgrade = b('\nH4sIAMkj41QAA+2ZUa+TMBTH8aoP9sWvUHNf5k1gFAqYJb75AXxcYgxhULi94baMlplrchM/umUT\nY3STgchiPL8H2p3CyvLvv+fAqrIpuLA1U9q+T5Rm9dKaGtcQBUHbkihwf2w7LOLRyA094ofUcgkl\nJLBwMPmdHKFROqkxtpK7jCefT5/XN/6PUv2qv1NwzQshazbRHK3AIaUn9SceOehPPd8NTZyEbuRa\n2J1o/t/yn+t/41QPKbpx1KcPSSU/mh4risPR5iKXKJPpctPwMkOHY8aVRjopFHJSuWN1UjAUx+ZL\nkvSWxTG69A8CBnHM/52uU83R53+THH7yf2D64P85+HL1uLUW6xemm8qyZKmW9fbJ+uX+82EZ4J3v\nRA7ZXq2fm2jJBVPbp4/bZ41z4XsH/pwj/j+EJiwDh9R/YeS3/qckhPpvDk7rn9XG/1xOsA7O198U\nftScR9qlAPrPQb/+ccwF13FsCsWRc/Tm/07/Lv975vHPg/w/B/3679t2fPROMGT/bws/o78bReD/\nORiiv5CCjdkFzvb/d/09PwrB/3MwRP+xmaBPf8/t3v/41NQARn+ftP4H/f8+16/wslH1cmMUZ2KH\nqwd9KwW6xvaNjVOZcVGscKNz+00bMfEdv1/lTKRv90GE0jJRCr/rFsn7/eJZyM2deZR8vULYkLEc\n1yzJFoqV+bdYS2WuhPdFl2WI/3NZZmP+Hzg7/9NgX/i1+78Zhvw/AyP0H5wGzq//O/0ppbD/AwAA\nAAAAAAAATMpX/Ti9zQAoAAA=\n')
_test_package_okay_module = b('\nH4sIAEQ141QAA+2X20rDMBjHMxCUou8Q2ZVCbZKmjQyPL+CN3pfadltlPdDDYL6Rr+Tt7n0Ar0w2\n3IY6u26jIvt+0KR8CT39v3++NB2UvTDWiyAv9MjNiyAz0LYhEmFZqqfCIov9J4gyLohtUsHlPMop\nowhbW3+SHyjzws0wRu6TH7rPy+dVjf9T0u/6T0NbTIPV9WfUFqbU3+LUBv2bYLn+fpYMgzDZQh7U\n8L9sbam/IIKA/k1Qrb/jpCPP9fqB46yZC7X05xwRRplcBkD/Bqin/ySm5p556ajoJ7Fu8jM5/Ps9\nlMC20nWJ/oyxL/pbwmQIkyY+wI7r/3Z4pO3z8cOtPB8vDrTkcSOPfE82PkL3J627F5Sp8Lx5vzb6\nSRQY049jhHFhVCfUPInS0evBRZT45SC4UpfLG355YAX/L8q13j2q/E8JnflfVgq1/nNTgP+boH2M\njTLPjEepeBAP8XRZ19pYP9Wxl/hh3Ovgsujq5yoi48Mw6nSD2LucBDXtr18A2Ih6/q8o9EuoVf/V\n/l/+BjIC/m8CqP+7zSr7/zAOC8dZu/xX+n/2/8eZSWyi/E8t2P8DAAAAAAAAAAAAAAAAwMZ8AIVQ\n3dwAKAAA\n')
_test_package_duplicate = b('\nH4sIAF8j41QAA+3aT2+bMBgGcNZth3HZV/DUS1cpxDYGpkq77QPsWGmaEAVDXVFIgGTqpEr76DNJ\nmaYtGYEgR1Of3yFQk5ZUj1//oV3kq0wVs0bWzew+qhtZza2pUS3wvPbIAo/+fuxYjIuA+py5vrAo\nE4x5FvEm/yQ7rOomqgixortERd/3v6/v+n9q8Xf+TqYalRVlJSe6RxuwL8Te/Bln2/wFd6mv25lP\nA2oROtH9/+mZ53/pLB5i+9Kpv32JFuVXfSazbPs6U0Va2kkZz29WKk/s7Wui6sZuoqy2nbhcyyrK\npB2G+odE8a0MQ/vUvxAMsqv+u1ynukdf/evJ4Y/69/Q56t+EH2ePS+vi+o0+jcs8l3FTVssX1283\nX2+7AVm7TuCw5dn1a92aq0LWy5ePy1cr58SfHY63o/63TRMuA4es/zyXtfUvaID1nwn7808qXf+q\nnKAfHJ6/XvgJ/T7WdgXkb0J//mGoCtWEoV4ojrxH7/zf5d/N/1xv/zjmfxP6898c2+ujR4LB9a/z\npwz1b8KQ/MeOBH31z2m3/3eF7gM6f5cFAerfhPN3ZL6qq/mNTlwWa7J4aG7Lwj4ns8sZictEFdkV\nWTXp7EPbotvX6v4qlUX8cdNo23Ee1TX51HWSz5vOc1He3OmtxPsrm2iJTEklo+Silnn61NZa6O/E\n84LTGlL/aZknY54PHzz+C28z8VPOXX0Z478BI/IfPA0cvv7r8hdCYPw3Yn/+aaRymUzxGGD4/t/3\nXRf1b0Jv/sdv/w6v/y5/TgMX+z8jevM/fvs3vP459T08/zFiQP6jR4KD93+/8ueBh7//GIH93/M2\noP7Hbv9GjP+ccfz/jxHD8x8+DQxf/wnOMf4DAAAAAAAAAAAAAAAAAAAAAAAAAOz0E5oqLUcAUAAA\n')
_test_package_empty = b('\nH4sIAIY1UVQAA+3OMQqDQBCF4TnKXkAzs5thz7OgRQIBiZsinl4tBBGClan+7xWvmCle7ccam/41\n1G9jrd7kArrI7mtbdt33Rizel6To2UQtacoS/IoxR5+xlncIUp7do0y//87uAAAAAAAAAAAAAAAA\nAAD80QwnI0dmACgAAA==\n')
_test_package_none = b('\nH4sIADw2UVQAA+3OMQoCMRAF0BwlR8i4MXuegBYKC6Jroad3FQQbsVqr937xi5ni76fTfEvrKotW\n67Nj3JbPfkuxqUuGobQxlYgaLeWy8q6X62Xu55xTP+4O/f7979cdAAAAAAAAAAAA/ugBC0Tm2gAo\nAAA=\n')
_test_package_okay = b('\nH4sIANM64lQAA+2Y326bMBTGWbddzDd7Ba+9ySKF2PzzFKm72gPsYheVpgkRMNQVwQSbbJ1UaY8+\nG5oo6xKxNpSsqn8XYE4Qhnzng3Nc5nXGiomkQk4WkZC0mlp9gxTE9/UeEx9t79dY2PEI8hwXqzHC\nHkbYgn7vd7KDWsiogtCKrhIW/dx/XtfvT5Tyb/1jXqQs6zEN7qU/Jkp/3/UDo/8Q7Ndfh2w9PngO\nLXDgeXv1x9i9oz/BhFgQ9fB8nTxz/c/gPBIshq3odRVJxguYspzClFcwLmvYpgg4gyu2mKXy/Dpa\n5DPQRm2dJTMoq5qCYz+K4QHs8H9FlzWr6IIWUtjyhzx4ji7/qxfAxv+IuNr/bhAY/w9BUvEV/XiO\njHufJzv8r8eizy7g3+s/13cdrOs/x3dN/TcEe/XX27D9NWxeEk09WF4/YI7O+o/gP/V3HCdA5v0/\nBGfv4LQW1XTOiiktVrC8lpdcF3uT8UQVhQkrshmsZTr5oCPrIpAW8XkTBAAkNIVNsmyyZPR+BqDi\n9PT0izpUl2hOUIdNuIyEAOZ783+ww/92xiTLCl7Rnubo9L+zVf8Fev0nQMT4fxDG6pUeg7Etvn+N\nSv5NjWiWtdsJK1IOEh5P5zXLE9BuEyYkkFEmgB0rv1dRRkEYqotE8SUNQ+Prp8Uu/6917WuOzv6P\n+Hf876ux8f8Q/Dq5WVqjizdqGPM8p7Hk1fLFxdvmuE0DuHJtYuPlycVrFc1ZQcXy5c3yVW0f+d4N\nh7PD/23oSOv/t/73tP9N//f47Ne/KecZ7yEP7tH/eyhw9Pof8onRfwi69T+w+be6v/8Owlv66/4f\ne56p/wfh4P4/zlU7Dz+tk+RzkzwjPr9SpcTtOoBeIaholIwEzdPb2GYh4Nh/wDOn2/9hyAomw/DB\n9u+u/+9+/x2Mfcf432AwGB6T3+hf1qIAKAAA\n')
_test_package_okay_deps = b('\nH4sIANsg41QAA+2ay46bMBSG6bRdlE1fwVU2aSSIzSVUkWbXB+gyUlUhBwzjEcFgm7SpNFIfvQYm\nbZUmIheGaDT+Ftg5TmLQf37fkiKrUppbkghprbCQhE+NvoGKwPfrEgU+/LfcYiDHC+DMga6LDIg8\nBGcG8Hu/kz1UQmIOgIHvY4p/Hn5fV/szpfhf/4jlCU17TIOj9fccF6FA6e+7vtZ/EA7rX4fsun5x\nH7XAM887qD9C7o7+AQoCA8Aenq+TF67/CCyxoBFoRa84lpTlIKEZAQnjICoq0KaIOQJrupon8naD\nV9ncbKN2nSVzIHlFzGs/iuYM9vifk7KinKxILoUtf8iL++jyv2r9O/+3/ncDR/t/CGLO1tq6L5c9\n/rdTKmmaM0566qNz/nfQn/kfzlQczWAAtf+HYGIXm8ic2OL7V1ywb6pG0rS9WjRPmBmzaLqsaBab\n7TWmQpoSp8JUi8M14TglZhiqL8HRHQlDPZQ8L/b5f6trX310zv+Bv+N/X9W1/4fg181DaYwX71Q1\nYllGIsl4+WrxvnndpgFYu3Zgo/Jm8VZFM5oTUb5+KN9U9pXvXXM5e/zfhq50/vPof6/2vz7/eXoO\n69/sDCjrIQ+OP/9VCz/Pr/d/aiuo9R+Cbv3DkOZUhqFaKJ7ZR/f+f8f/DkK+3v8PQrf+TVm3nz0S\nnOx/pT9E2v9DcIr+544EXf534Hb/73oqB5T+rj7/H4jRBzCtBJ8uleIkX4NiI+9YfdhvTSwQsZjm\n6RxUMrE+1ZHtjwAkj26boGlGGRYCfN4myZcmecZsea+2Eh/nJlDEJAGc4HgsSJY8xmoK9Ul9XnBd\nTvF/wrL4nP8HHL/+95uJHzqOq5r1+D8AZ+h/8jRw/Ppvq7/neXr812g0miflN8c/c14AKAAA\n')
_test_package_failure = b('\nH4sIAIEf41QAA+2aT2vbMBjGs247zJd9BY1eukIcyX9HoLex846BMYxiy66KayeWnNFBYR99ctyM\nrU1wkxiHsud3sJXXSWTz6HlfSckirzNZjLVQenzLlRbVZNQ31BD6fnNmoU//Pm8YMccLaWDCbjCi\nzGOOOyJ+73eyhVppXhEy4jeJ5D93v6/r+gtl8VT/uCxSmfU4DJ6tv+e4jIVGf9/1A+g/BLv1b0J2\n0z66j0bgwPN26s+Y+0j/kIXhiNAenq+T/1z/czLnSsakFb2uuJZlQVKZC5KWFYkXNWmHiHVOVvJ2\nmuqrO36bT602ajejZEp0VQvr1I8CDmCL/5u26nMWsFf9D1mT/53AQ/4fgp36N8co5SYRJPbi7qg+\nuvN/8K/+Dm3KAPL/AJx/IJNaVZO5LCaiWJHFnb4um2Q/vhybopDIIpuSWqfjT01kUwREEV+tg5bF\nlRKVJl94rlACXh5b/G9nUsusKCvRUx+d/nfYn/kfDUycBTSk8P8QXJrkHluXtvrxjS/K76Ylsqw9\njmWRllZSxpN5LfPEao+JVNrSPFOWWRysRMUzYUWR+RIeX4soQgp4WWzz/0bXvvro8r+ZHD7yv2/a\n8P8Q/Dq7X44uZu9MMy7zXMS6rJavZu/Xr9thQFauHdpseTZ7a6K5LIRavr5fvqntE987OJ4t/m9D\nJ9r/e/C/R7H+G4Td+ieV8b8sexgHe6z/A+r5zf4fDRzoPwTd+keRLKSOosN3ATrr/2P/O4z5Dur/\nEHTrvz431w/OBHv73+hPGfw/BPvof2gm6PK/Qzfrf9czY8Do7+L3n4E4ev8vzrlS5PNmkHxdD56L\ncn5jlhIfpxYxJCIlleDJhRJ5+hBrWJhPYr/gtOzj/7TMk0P+H/L8+b+/LvzUcVxzGfl/AA7Qf+8y\n8Pz530Z/z/OQ/wEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAeMJvyBsJQgBQAAA=\n')
_test_package_failure_test = b('\nH4sIAPQf41QAA+2aTW+bMBjHWbcdxmVfwVMvWaUQm9cpUk+rdt6hh0jThBww1BXBBEymTqq0jz47\nlKpKE9EkjKja8zuAeZwEov/zYj9JkdUpz8eSVXK8oJVk5cToG6wIPE+fSeDhp+cWg9hugH1ldnwD\nE5fYjoG83p9kC3UlaYmQQW9jTn/vfl3X/CuleK5/JPKEpz26wYv1d22HkEDp7zmeD/oPwW79tcnS\n46PvoQX2XXen/oQ4G/oHJAgMhHv4fp385/qfozmteIQa0euSSi5ylPCMoUSUKCpq1LiIeY5WfDFN\n5OUdXWRTs7Fa2kumSJY1M0/9VYAD2BL/elz1uQrYp/4HPtH53/Y9yP9DsFN/fQwTqhJBbBV3R92j\nK//byjce9fdU/rcxcQjk/yE4/4QmdVVO5jyfsHyFijt5I3SyH1+MVVGIeZ5OUS2T8RdtaYsAy6PL\ntdE0+aIQpUR1zqV2GdOMMlpV6FqNr6iko3bC0pavtGKfpyZSxCxBax+rxIKNKpYlDxMafWmpj2Gl\nvFalZfSNZuqNUGH6Z0v8WymXPM1FyXq6R+f6zyaP6z/sKzvxcYAh/ofgQiX3yLywql8/aCF+qhFL\n0+Y45nkizFhEk3nNs9hsjjFXQS5pWplqc7BiJU2ZGYbqQ2h0w8IQYvR1sS3+W137ukdX/KvF4Ub8\ne2oM8T8Ef87ul8Zo9kENI5FlLJKiXL6ZfVxfN26AVo4VWGR5NnuvrBnPWbV8e798V1snfnbgeLbE\nf2M6Uf/vIf5dHf+w//v37NY/LlX8c9GDH+yx//ex6+n+H/Zt0H8IuvUPQ662cGF4eBegs/5vxr9N\niGdD/R+Cbv3XZz1/cCbYO/6V/phA/A/BPvofmgk6+3+43f87Ltb9X9uB338G4uj+X9Puu2qd5Pva\neUZifqu2Ek9afSWj8WaXr1DvhH7Badkn/hORxYf8P+Tl639vXfixbTtqGvL/AByg/95l4OXrv1Z/\n13Uh/wMAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADAM/4Cv2LX5gBQAAA=\n')

class TestPackage(unittest.TestCase):

    def setUp(self):
        if not hasattr(BytesIO, '__exit__'):
            BytesIO.__exit__ = lambda *a**a: None
        if not hasattr(BytesIO, '__enter__'):
            BytesIO.__enter__ = lambda *a, self, **a: self

    def test_package_find(self):
        with temp.variables({'glob.glob': lambda *a**a: [
                       'd.version']}):
            find_package(None, None)

    def test_package_filesum(self):
        with open(__file__, 'rb') as (f):
            x = _FileSum(f)
            x.tell()
            x.seek(0, 0)

    def test_package_remove_nonexistant(self):
        with self.assertRaises(PackageError):
            p = Package('foo', 'bar', None, None)
            p.remove()

    def test_package_okay(self):
        with temp.directory() as (dir):
            p = Package.from_tarballfd(BytesIO(b64decode(_test_package_okay_folder)), dir, True)
            with self.assertRaises(PackageError):
                Package.from_tarballfd(BytesIO(b64decode(_test_package_okay_folder)), dir)
            Package.from_tarballfd(BytesIO(b64decode(_test_package_okay_folder)), dir, upgrade=True)
            Package.from_tarballfd(BytesIO(b64decode(_test_package_okay_upgrade)), dir, upgrade=True)
            x = repr(p)
            p.remove()

    def test_package_remove_module(self):
        with temp.directory() as (dir):
            p = Package.from_tarballfd(BytesIO(b64decode(_test_package_okay_module)), dir, upgrade=True)
            p.remove()

    def test_package_error(self, pkg=_test_package_none):
        with temp.directory() as (dir):
            with self.assertRaises(PackageError):
                Package.from_tarballfd(BytesIO(b64decode(pkg)), dir)

    def test_package_empty(self):
        self.test_package_error(_test_package_empty)

    def test_package_failure(self):
        self.test_package_error(_test_package_failure)
        self.test_package_error(_test_package_failure_test)

    def test_package_duplicate(self):
        self.test_package_error(_test_package_duplicate)

    def test_package_nopip(self):
        with temp.directory() as (dir):
            with self.assertRaises(PackageError):
                import pip
                del pip.main
                Package.install_requirements.__globals__['pip'] = pip
                Package.from_tarballfd(BytesIO(b64decode(_test_package_okay_deps)), dir)

    def test_package_tarball(self):
        self._mock_flag = False
        if hasattr(drove.package.__builtins__, 'open'):
            self._mock_orig = drove.package.__builtins__.open
        else:
            self._mock_orig = drove.package.__builtins__['open']

        def _mock_open(*a, **kw):
            if not self._mock_flag:
                self._mock_flag = True
                return BytesIO(b64decode(_test_package_okay))
            else:
                return self._mock_orig(*a, **kw)

        with temp.directory() as (dir):
            if hasattr(drove.package.__builtins__, 'open'):
                drove.package.__builtins__.open = _mock_open
            else:
                drove.package.__builtins__['open'] = _mock_open
            try:
                Package.from_tarball('mocked', dir)
            finally:
                if hasattr(drove.package.__builtins__, 'open'):
                    drove.package.__builtins__.open = self._mock_orig
                else:
                    drove.package.__builtins__['open'] = self._mock_orig

    def test_package_url(self):
        with temp.directory() as (dir):
            _urlopen = urllib.request.urlopen
            urllib.request.urlopen = lambda *a**a: BytesIO(b64decode(_test_package_okay))
            try:
                Package.from_url('http://none', dir)
            finally:
                urllib.request.urlopen = _urlopen