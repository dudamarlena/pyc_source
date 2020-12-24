# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\Mydemos_pkg\MyHelp.py
# Compiled at: 2020-05-07 09:56:19
# Size of source mod 2**32: 6716 bytes


def Help(s=None):
    if s == None:
        Help_ext()
    else:
        Help_main(s)


def Help_ext(ss=None):
    helpw = '\nWelcome to Mydemos_pkg 1.7.0\'s help utility!\n\nEnter the name of any module, keyword, or topic to get help on writing\nPython programs and using Python modules.  To quit this help utility and\nreturn to the interpreter, just type "quit".\n\nTo get a list of available modules, type "modules".  Each module also comes with a one-line summary of what it does; to list the modules whose name\nor summary contain a given string such as "spam", type "modules spam".\n'
    helpw1 = '\n\nhelp> '
    hb = '\nabout bytedesign:\nyou can output an amazing graph usage:\nfrom Mydemos_pkg import bytedesign\nbytedesign.bytedesign()\nand look at the turtle-graph!\n'
    hch = '\nabout chaos:\nit make a chaos line to you!\nfrom Mydemos_pkg import chaos\nchaos.chaos()\n'
    hcl = '\nabout clock:\nit make a clock to you!\nfrom Mydemos_pkg import clock\nclock.clock()\n'
    hco = '\nabout colormixer:\nit make a colormixer to you and u can use your mouse to control it!\nfrom Mydemos_pkg import colormixer\ncolormixer.colormixer()\n'
    hcs = '\nabout colorspiral:\nit make a colorspiral!\nfrom Mydemos_pkg import colorspiral\ncolorspiral.colorspiral(6)#sides\n'
    hd = '\nabout download:\nit download a file!\nfrom Mydemos_pkg import download_file\ndownload_file.download("http://www.example.com/demo.pdf")\n'
    hf = '\nabout forest:\nit make a forest!\nfrom Mydemos_pkg import forest\nforest.forest() #only_debug\n'
    hfr = '\nit makes a curve!\nfrom Mydemos_pkg import fractalcurves\nfractalcurves.fractalcurves()\n'
    hh = '\nit shows you how hanoi game worked.\nfrom Mydemos_pkg import hanoi\nhanoi.hanoi()\n'
    hl = '\nit make a lindenmayer.\nfrom Mydemos_pkg import lindenmayer\nlindenmayer.lindenmayer()\n'
    hpa = '\nit make a paint software.\nfrom Mydemos_pkg import paint\npaint.paint()\n'
    hpe = '\nit make a peace.\nfrom Mydemos_pkg import peace\npeace.peace()\n'
    hpen = '\nit make a penrose.\nfrom Mydemos_pkg import penrose\npenrose.penrose()\n'
    hpi = "\nit could install or uninstall or upgrade sth modules.\nusage:\nfrom Mydemos_pkg.pip_install import *\ninstall('paddlehub')\nupgrade('paddlehub')\nuninstall('paddlehub')\n"
    hpl = '\nit make earth,sun,moon.\nfrom Mydemos_pkg import planet_and_moon\nplanet_and_moon.planet_and_moon()\n'
    hpr = '\nit make a progress.\nfrom Mydemos_pkg import progress\nprogress.progress(0.1)#delay\n'
    hro = '\nit make a rosette.\nfrom Mydemos_pkg import penrose\nrosette.rosette()\n'
    hr = '\nit make a round_dance.\nfrom Mydemos_pkg import round_dance\nround_dance.round_dance()\n'
    hs = '\nit sort_test.\nfrom Mydemos_pkg import sort\nsort.sort_test()\n'
    hsa = '\nit sort_test.\nfrom Mydemos_pkg import sort_animate\nsort_animate.sort_animate()\n'
    ht = '\nit make a tree.\nfrom Mydemos_pkg import tree\ntree.tree()\n'
    htw = '\nit make two canvas.\nfrom Mydemos_pkg import two_canvas\ntwo_canvas.two_canvas()\n'
    huc = "\nit converts unicodes.\nnonBMPtoBMP ->unicodes from nonBMP to BMP,if you: print(nonBMPtoBMP('\\U0001F600'))onidle you get a emoji!\n"
    hu = '\nmake a whole unicode map.\nmake_unicode ->make unicodemap.\nunicode_1 ->BMP\nunicode_2 ->Plane2\nBMP_plane2 -> BMP and Plane2\n'
    hy = '\nit make a yinyang graph.\nfrom Mydemos_pkg import yinyang\nyinyang.yinyang()\n'
    all_helps = {'bytedesign':hb, 
     'chaos':hch, 
     'clock':hcl, 
     'colormixer':hco, 
     'colorspiral':hcs, 
     'download_file':hd, 
     'forest':hf, 
     'fractalcurves':hfr, 
     'hanoi':hh, 
     'lidenmayer':hl, 
     'nim':'nim', 
     'paint':hpa, 
     'peace':hpe, 
     'penrose':hpen, 
     'pip_install':hpi, 
     'planet_and_moon':hpl, 
     'progress':hpr, 
     'rosette':hro, 
     'sort':hs, 
     'sort_animate':hsa, 
     'tree':ht, 
     'two_canvas':htw, 
     'unicodeconvert':huc, 
     'unicodes':hu, 
     'yinyang':hy}
    mdd = '\nbytedesign\nchaos\nclock\ncolormixer\ncolorspiral\ndownload_file\nforest\nfractalcurves\nhanoi\nlidenmayer\nnim\npaint\npeace\npenrose\npip_install\nplanet_and_moon\nprogress\nrosette\nsort\nsort_animate\ntree\ntwo_canvas\nunicodeconvert\nunicodes\nyinyang\n'
    if ss == None:
        print(helpw)
        d = input(helpw1)
        while d.lower() != 'quit':
            try:
                print(all_helps[d])
            except KeyError:
                if d.replace(' ', '') == '':
                    sss = '\nYou are now leaving help and returning to the Python interpreter.\nIf you want to ask for help on a particular object directly from the\ninterpreter, you can type "help(object)".  Executing "help(\'string\')"\nhas the same effect as typing a particular string at the help> prompt.\n'
                    print(sss)
                    return
                elif 'modules' in d:
                    if d.replace(' ', '') == 'modules':
                        print(mdd)
                    else:
                        try:
                            print(all_helps[d.replace(' ', '').replace('modules', '')])
                        except KeyError:
                            print('No module found as %s' % d)

                else:
                    print('No module found as %s' % d)

            d = input(helpw1)

        sss = '\nYou are now leaving help and returning to the Python interpreter.\nIf you want to ask for help on a particular object directly from the\ninterpreter, you can type "help(object)".  Executing "help(\'string\')"\nhas the same effect as typing a particular string at the help> prompt.\n'
        print(sss)
    else:
        try:
            print(all_helps[d])
        except KeyError:
            if d == 'modules':
                print(mdd)
            else:
                print('No anything found as %s' % ss)


def Help_main(s):
    Help_ext(s)