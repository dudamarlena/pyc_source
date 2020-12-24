# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/contractvmd/chainstarter.py
# Compiled at: 2015-11-30 17:33:02
# Size of source mod 2**32: 1072 bytes
import os, sys

def main():
    ARGS = '-server -rpcuser=test -rpcpassword=testpass -rpcport=8080 -txindex -debug -printtoconsole -rpcallowip=0.0.0.0/0'
    if len(sys.argv) == 1:
        os.system('bitcoin-qt -testnet ' + ARGS)
    else:
        if len(sys.argv) > 1:
            cmd = '-qt'
            if len(sys.argv) == 3 and sys.argv[2] == 'daemon':
                ARGS += ' -daemon'
                cmd = 'd'
            if len(sys.argv) == 3 and sys.argv[2] == 'stop':
                cmd = '-cli'
                ARGS += ' stop'
            if sys.argv[1] == 'XLT':
                os.system('litecoin' + cmd + ' -testnet ' + ARGS)
            else:
                if sys.argv[1] == 'XTN':
                    os.system('bitcoin' + cmd + ' -testnet ' + ARGS)
                else:
                    if sys.argv[1] == 'XDT':
                        os.system('dogecoin' + cmd + ' -testtest ' + ARGS)
                    else:
                        if sys.argv[1] == 'RXLT':
                            os.system('litecoin' + cmd + ' -regtest ' + ARGS)
                        else:
                            if sys.argv[1] == 'RXTN':
                                os.system('bitcoin' + cmd + ' -regtest ' + ARGS)
                            else:
                                if sys.argv[1] == 'RXDT':
                                    os.system('dogecoin' + cmd + ' -regtest ' + ARGS)
                                else:
                                    print('unrecognized chain name', sys.argv[1])
        else:
            print('usage: python ' + sys.argv[0] + ' chaincode [daemon|stop]')


if __name__ == '__main__':
    main()