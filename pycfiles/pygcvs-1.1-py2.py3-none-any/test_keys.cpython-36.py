# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/okhin/git/orage.io/pygcrypt/env/lib/python3.6/site-packages/pygcrypt/test/test_keys.py
# Compiled at: 2017-04-09 08:17:00
# Size of source mod 2**32: 4030 bytes
from hashlib import sha256
import pytest
from pygcrypt.gctypes.key import Key
from pygcrypt.gctypes.sexpression import SExpression
from pygcrypt.utils import create_keys, randomize

@pytest.mark.skip(reason='Generating key takes time, so skip it.')
def test_generate_keys(context):
    priv, pub = create_keys()
    if not isinstance(priv, Key):
        raise AssertionError
    elif not isinstance(pub, Key):
        raise AssertionError


def test_keylen(context, private, public):
    if not len(private) == 4096:
        raise AssertionError
    elif not len(public) == 4096:
        raise AssertionError


def test_keygrip(context, private, public):
    if not private.keygrip == '1741a507591039059c5d565e4a041069c347a1b3':
        raise AssertionError
    elif not public.keygrip == '1741a507591039059c5d565e4a041069c347a1b3':
        raise AssertionError


def test_sanity(context, private, public):
    if not private.issane() == True:
        raise AssertionError
    elif not public.issane() == False:
        raise AssertionError


def test_algo(context, private, public):
    if not private.algo == 'rsa':
        raise AssertionError
    else:
        if not public.algo == 'rsa':
            raise AssertionError
        else:
            if not private.sign == True:
                raise AssertionError
            elif not public.sign == True:
                raise AssertionError
            assert private.encr == True
        assert public.encr == True


def test_encryption(context, private, public):
    input_data = SExpression('(data (flags)(value %s))', 'Hello World!\n')
    encrypted_data = SExpression('(enc-val (rsa (a #0081C38D19B9DB672738EBA125714C3765C6292F8EA6BD988E3663104D616F183E7F6C96C5422D13032BC4FEA2415533C35F065E13E741BB2E31FE057D943FD92157F3E09BB17CE353929231DE376483C231313694451010C27B84AD8F171EDCFA51A493B9655DF59EEDC591FFDA4C25424FEA034BD60ECC9D433AE7E67362C292309BE5226997F93E2123FB2F9AF066E0D74F8A3F6FCC1511D4B80DEC92DEB95CBD16C7A9E1EA05F5252B7A5D1954600D532B9464E830579392EFD8979320CB8DBE02932681A7BD149E06F04A58F50B6E791E4E7E8C318EA24821327AF3F96C1B8CE78039E9BB2CBF302A100987B7CBDE842D199CAF9BD059432E45C28D3C743F31FBD84192F720329DF2E55F3005271C47BCACAFB2BAE4F886391E5C9CA83AF0758B7B1C48C2CEB1DDE2D3D227A3F811ADEEE79F3607B7E0230ACE8770602013DF06B32C33A9407E7551D1B7C801EC23237E3175E397F28F21BD611FB68B6EE214F367AE52C78D4A6515352DB620B102B687DFC107AD605022EA7E8A540A96457403B1EC4DE8A783C6F13877BC869DB7DB746316697A7824BEC1F330ABCFD1C2FE7BFB41BC7BD0307FD78EE9DD111984D77704A8801C06880D2BC771883FE7C2DB6CCA9FB4812483B4262A2D1FDE23458511BACC052A219870B6E248D94DED6968C8B0EC9335523A8BB4CD89BECB11FDE3747BAF13C29BDC16421A19988D1CB3#)))')
    decrypted_data = SExpression('(value %s)', 'Hello World!\n')
    if not public.encrypt(input_data) == encrypted_data:
        raise AssertionError
    elif not private.decrypt(encrypted_data) == decrypted_data:
        raise AssertionError
    with pytest.raises(NotImplementedError):
        private.encrypt(input_data)
        public.decrypt(encrypted_data)


def test_sign(context, private, public):
    hashing = sha256()
    hashing.update('Test data inserted')
    data = hashing.digest()
    with pytest.raises(NotImplementedError):
        public.makesign(data)
    sig = private.makesign(data)
    if not sig == SExpression('(sig-val \n (rsa \n  (s #0DB6FD3B8915538E0C3619B32F47BBB2990E36F3E0ACBBA80E58BF317079928575EB06ED86247FD988A25F906BC4547983422DF30ACB64DE416D1144EEAEC08AD8DCDBA5E7A21956CECE6549CBBFA5B1D8E80994EAAEA266C4FEEBD7A613BDA1636487FA4F3FED102BF79779B8B6056F02D76F79BE96F64B555B578A0D8816535C2F6915D88ADE601FDD5D03862CB8240C4DA4A66AAE510B995EB5C76D6B62867FBB27D1BBEFE4A5BA77D0357035873F189B2FFE718F3BD164ACCCB5355D316C1A80B8BFF324AAB148854D4E1F40DF224DF7DFD7ADA056D343A0B81F9E6DCA6AD9C92924BD36C6C2D7688C94EC8DB45F3B3E38BFCA1B7475E29BF9442DCDEC154AD816AFEC1F7EE23A9228E40DB20248951FE2CE6E4AF9C546C7C108A862B58C99BD70AE72D73A8BCA00CC8A4501DC7FF5EEA7533BC065454FDFB270242DE7981B050DAFBE682A9F498F445AB6EA1ED20B1AF5BFBEE646214DF2CC214E6D3B6E59925600CDED856A49C0F5899669107A5D957E675BC94A53C32E476CE64B0DB77DDB4320179B5D36682F017FE9D8FA5D18A9C9955210F60AA4A18737AECAF9CA2DC9D938A1F73ECF274276FE3F8B9BC4879B75617F2E7AD8485FB71C7B10B2F0DCE6F2F0CE3FF1303145B7D11EE281B6A18A6F02B8E787A4956046BBE5AC5E47BF695712BAE9FC32A8881CB53D8881973B6C70AA648289A5DDB98EFF5C14A061#)\n  )\n )\n'):
        raise AssertionError
    elif not public.verify(sig, data) == True:
        raise AssertionError
    with pytest.raises(NotImplementedError):
        private.verify(sig, data)