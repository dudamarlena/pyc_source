# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.6/dist-packages/inkscapeslide/__init__.py
# Compiled at: 2010-07-12 14:13:27
import lxml.etree, sys, os, re

def main():
    import warnings
    warnings.filterwarnings('ignore', category=DeprecationWarning)
    if len(sys.argv) < 2 or sys.argv[1].startswith('--'):
        print 'Usage: %s [svgfilename]' % sys.argv[0]
        sys.exit(1)
    FILENAME = sys.argv[1]
    f = open(FILENAME)
    cnt = f.read()
    f.close()
    doc = lxml.etree.fromstring(cnt)
    layers = [ x for x in doc.iterdescendants(tag='{http://www.w3.org/2000/svg}g') if x.attrib.get('{http://www.inkscape.org/namespaces/inkscape}groupmode', False) == 'layer' ]
    content_layer = [ x for x in layers if x.attrib.get('{http://www.inkscape.org/namespaces/inkscape}label', False).lower() == 'content' ]
    if not content_layer:
        print "No 'content'-labeled layer. Create a 'content'-labeled layer and put a text box (no flowRect), with each line looking like:"
        print ''
        print '   background, layer1'
        print '   background, layer2'
        print '   background, layer2, layer3'
        print '   background, layer2 * 0.5, layer3'
        print '   +layer4 * 0.5'
        print ''
        print 'each name being the label of another layer. Lines starting with'
        print "a '+' will add to the layers of the preceding line, creating"
        print "incremental display (note there must be no whitespace before '+')"
        print ''
        print 'The opacity of a layer can be set to 50% for example by adding '
        print "'*0.5' after the layer name."
        sys.exit(1)
    content = content_layer[0]
    preslides = [ x.text for x in content.findall('{http://www.w3.org/2000/svg}text/{http://www.w3.org/2000/svg}tspan') if x.text ]
    if not bool(preslides):
        print "Make sure you have a text box (with no flowRect) in the 'content' layer, and rerun this program."
        sys.exit(1)
    orig_style = {}
    for l in layers:
        label = l.attrib.get('{http://www.inkscape.org/namespaces/inkscape}label')
        if 'style' not in l.attrib:
            l.set('style', '')
        orig_style[label] = l.attrib['style']

    slides = []
    for sl in preslides:
        if sl:
            if sl.startswith('+'):
                sl = sl[1:]
                sl_layers = slides[(-1)].copy()
            else:
                sl_layers = {}
            for layer in sl.split(','):
                elements = layer.strip().split('*')
                name = elements[0].strip()
                opacity = None
                if len(elements) == 2:
                    opacity = float(elements[1].strip())
                sl_layers[name] = {'opacity': opacity}

            slides.append(sl_layers)

    def set_style(el, style, value):
        """Set the display: style, add it if it isn't there, don't touch the
        rest
        """
        if re.search('%s: ?[a-zA-Z0-9.]*' % style, el.attrib['style']):
            el.attrib['style'] = re.sub('(.*%s: ?)([a-zA-Z0-9.]*)(.*)' % style, '\\1%s\\3' % value, el.attrib['style'])
        else:
            el.attrib['style'] = '%s:%s;%s' % (style, value, el.attrib['style'])

    pdfslides = []
    for (i, slide_layers) in enumerate(slides):
        for l in layers:
            label = l.attrib.get('{http://www.inkscape.org/namespaces/inkscape}label')
            l.set('style', orig_style[label])
            set_style(l, 'display', 'none')
            if label in slide_layers:
                set_style(l, 'display', 'inline')
                opacity = slide_layers[label]['opacity']
                if opacity:
                    set_style(l, 'opacity', str(opacity))

        svgslide = os.path.abspath(os.path.join(os.curdir, '%s.p%d.svg' % (FILENAME, i)))
        pdfslide = os.path.abspath(os.path.join(os.curdir, '%s.p%d.pdf' % (FILENAME, i)))
        f = open(svgslide, 'w')
        f.write(lxml.etree.tostring(doc))
        f.close()
        os.system('inkscape -A %s %s' % (pdfslide, svgslide))
        os.unlink(svgslide)
        pdfslides.append(pdfslide)
        print 'Generated page %d.' % (i + 1)

    joinedpdf = False
    has_pyPdf = False
    try:
        import pyPdf
        has_pyPdf = True
    except:
        pass

    if has_pyPdf:
        print "Using 'pyPdf' to join PDFs"
        output = pyPdf.PdfFileWriter()
        inputfiles = []
        for slide in pdfslides:
            inputstream = file(slide, 'rb')
            inputfiles.append(inputstream)
            input = pyPdf.PdfFileReader(inputstream)
            output.addPage(input.getPage(0))

        outputStream = file('%s.pdf' % FILENAME.split('.svg')[0], 'wb')
        output.write(outputStream)
        outputStream.close()
        for f in inputfiles:
            f.close()

        joinedpdf = True
    elif not os.system('which pdfjoin > /dev/null'):
        print "Using 'pdfsam' to join PDFs"
        os.system('pdfjoin --outfile %s.pdf %s' % (FILENAME.split('.svg')[0],
         (' ').join(pdfslides)))
        joinedpdf = True
    elif not os.system('which pdftk > /dev/null'):
        print "Using 'pdftk' to join PDFs"
        os.system('pdftk %s cat output %s.pdf' % ((' ').join(pdfslides),
         FILENAME.split('.svg')[0]))
        joinedpdf = True
    else:
        print "Please install pdfjam, pdftk or install the 'pyPdf' python package, to join PDFs."
    if joinedpdf:
        for pdfslide in pdfslides:
            os.unlink(pdfslide)

    return