# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/castro/lib/pyvnc2swf/html_templates.py
# Compiled at: 2011-03-28 15:09:52
import sys, os, os.path
from swf import SWFParser
PYVNC2SWF_VERSION = '0.9.2'
SEEKBAR_HEADER = '\n<script language="javascript">\n/* Jesse Ruderman\n * July 18, 2004\n *\n * Remaining problems:\n *   IE sometimes crashes on exit after using the this script.\n *   In IE, it is a little ugly because IE doesn\'t support border-radius.\n *   In IE, it does not work at standalone Flash URLs.\n */\n\nfunction setupSeekBar() {\n\nsetTimeout(initFlashControls, 100);\n\nfunction initFlashControls()\n{\n  var count = 0;\n\n  function tt(elem)\n  {\n    if (typeof elem.TotalFrames != "undefined") /* do not coerce elem.StopPlay to bool, because that breaks IE */\n    {\n      addFlashControls(elem);\n      ++count;\n    }\n  }\n\n  var i, x;\n\n  for (i = 0; x = document.getElementsByTagName("object")[i]; ++i)\n    tt(x);\n\n  for (i = 0; x = document.getElementsByTagName("embed")[i]; ++i)\n    tt(x);\n\n}\n\n\nfunction addFlashControls(flash)\n{\n  var controlsDiv = document.createElement("div");\n\n  /* Put the controls under the Flash. \n   *\n   * If the Flash is an <embed> in an <object>, we do not want to touch the <object>, because that would make\n   * Mozilla re-test whether the <object> is broken and reset the <embed>.  So in that case, we put the controls\n   * under the <object>.\n   */\n  var where = flash;\n  while (where.parentNode.tagName.toLowerCase() == "object")\n    where = where.parentNode;\n  where.parentNode.insertBefore(controlsDiv, where.nextSibling);\n\n  /* Construct controls using DOM2 instead of innerHTML.\n   * In Mozilla, innerHTML= is like innerText= at standalone flash URLs.\n   */\n  var table = document.createElement("table");\n  controlsDiv.appendChild(table);\n  \n  var row = table.insertRow(-1);\n  \n  var pauseButton = document.createElement("button");\n  pauseButton.appendChild(document.createTextNode("Pause"));\n  var buttonCell = row.insertCell(-1);\n  buttonCell.appendChild(pauseButton);\n  \n  var slider = row.insertCell(-1);\n  slider.width = "100%";\n  \n  var visibleSlider = document.createElement("div");\n  visibleSlider.style.position = "relative";\n  visibleSlider.style.height = "10px";\n  visibleSlider.style.width = "100%";\n  visibleSlider.style.MozBorderRadius = "4px";\n  visibleSlider.style.background = "#aaa";\n  slider.appendChild(visibleSlider);\n  \n  var thumb = document.createElement("div");\n  thumb.style.position = "absolute";\n  thumb.style.height = "20px";\n  thumb.style.width = "10px";\n  thumb.style.top = "-5px";\n  thumb.style.MozBorderRadius = "4px";\n  thumb.style.background = "#666";\n  visibleSlider.appendChild(thumb);\n  \n\n  var sliderWidth;\n  var paused = false;\n  var dragging = false;\n\n  table.width = Math.max(parseInt(flash.width) || 0, 400);\n  \n  addEvent(pauseButton, "click", pauseUnpause);\n  addEvent(slider, "mousedown", drag);\n  addEvent(slider, "drag", function() { return false; }); /* For IE */\n  window.setInterval(update, 30);\n\n  function pauseUnpause()\n  {\n    paused = !paused;\n\n    pauseButton.style.borderStyle = paused ? "inset" : "";\n\n    if (paused)\n      flash.StopPlay();\n    else\n      flash.Play();\n  }\n\n  function update()\n  {\n    sliderWidth = parseInt(getWidth(slider) - getWidth(thumb));\n\n    if (!paused && !dragging)\n      thumb.style.left = parseInt(flash.CurrentFrame() / totalFrames() * sliderWidth) + "px";\n  }\n\n  function dragMousemove(e)\n  {\n    var pageX = e.clientX + document.body.scrollLeft; /* cross-browser, unlike e.pageX, which IE does not support */\n    var pos = bounds(0, pageX - getX(slider) - 5, sliderWidth);\n    var frame = bounds(1, Math.ceil(totalFrames() * pos / sliderWidth), totalFrames() - 2);\n\n    thumb.style.left = pos + "px";\n\n    flash.GotoFrame(frame);\n  }\n\n  function release(e)\n  {\n    removeEvent(document, "mousemove", dragMousemove);\n    removeEvent(document, "mouseup", release);\n    if (!paused)\n      flash.Play();\n    dragging = false;\n  }\n\n  function drag(e)\n  {\n    addEvent(document, "mousemove", dragMousemove);\n    addEvent(document, "mouseup", release);\n    dragging = true;\n    dragMousemove(e);\n  }\n\n\n\n  /* Boring functions, some of which only exist to hide differences between IE and Mozilla. */\n\n  function bounds(min, val, max)\n  {\n    return Math.min(Math.max(min, val), max);\n  }\n\n  function totalFrames()\n  {\n    /* This is weird.  TotalFrames differs between IE and Mozilla.  CurrentFrame does not. */\n\n    if (typeof flash.TotalFrames == "number")\n      return flash.TotalFrames; /* IE */\n    else if (typeof flash.TotalFrames == "function")\n      return flash.TotalFrames(); /* Mozilla */\n    else\n      return 1; /* Partially loaded Flash in IE? */\n  }\n\n  function getWidth(elem)\n  {\n    if (document.defaultView && document.defaultView.getComputedStyle)\n      return parseFloat(document.defaultView.getComputedStyle(elem,null).getPropertyValue("width")); /* Mozilla */\n    else\n      return parseFloat(elem.offsetWidth); /* IE (currentStyle.width can be "auto" or "100%") */\n  }\n\n  function getX(elem)\n  {\n    if (!elem) return 0;\n    return (elem.offsetLeft) + getX(elem.offsetParent);\n  }\n\n  function addEvent(elem, eventName, fun)\n  {\n    if (elem.addEventListener) /* Mozilla */\n      elem.addEventListener(eventName, fun, false);\n    else /* IE */\n      elem.attachEvent("on" + eventName, fun);\n  }\n\n  function removeEvent(elem, eventName, fun)\n  {\n    if (elem.addEventListener)\n      elem.removeEventListener(eventName, fun, false);\n    else\n      elem.detachEvent("on" + eventName, fun);\n  }\n\n}\n\n}\n</script>\n</head>\n<body onload="setupSeekBar();">\n'
NORMAL_HEADER = '</head><body>\n'

def generate_html(out, fname, seekbar=True, loop=True):
    parser = SWFParser()
    parser.open(fname, header_only=True)
    (x, width, y, height) = parser.rect
    basename = os.path.basename(fname)
    (title, ext) = os.path.splitext(basename)
    out.write('<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN">\n<html>\n<head>\n<title>%s</title>' % title)
    if seekbar:
        out.write(SEEKBAR_HEADER)
    else:
        out.write(NORMAL_HEADER)
    dic = {'title': title, 'width': int(width / 20), 'height': int(height / 20), 'basename': basename, 'swf_version': parser.swf_version, 'loop': loop, 'pyvnc2swf_version': PYVNC2SWF_VERSION}
    out.write('<h1>%(title)s</h1>\n<hr noshade><center>\n<object classid="clsid:D27CDB6E-AE6D-11cf-96B8-444553540000" width="%(width)d" height="%(height)d"\n codebase="http://download.macromedia.com/pub/shockwave/cabs/flash/swflash.cab#version=%(swf_version)d,0,0,0">\n <param name="movie" value="%(basename)s">\n <param name="play" value="true">\n <param name="loop" value="%(loop)s">\n <param name="quality" value="high">\n<embed src="%(basename)s" width="%(width)d" height="%(height)d" play="true"\n loop="%(loop)s" quality="high" type="application/x-shockwave-flash"\n pluginspage="http://www.macromedia.com/go/getflashplayer">\n</embed></object></center>\n<hr noshade>\n<div align=right>\n<em>Generated by <a href="http://www.unixuser.org/~euske/vnc2swf/">pyvnc2swf</a>-%(pyvnc2swf_version)s</em>\n</div></body></html>\n' % dic)


if __name__ == '__main__':
    import getopt

    def usage():
        print 'usage: %s [-S)eekbarless] [-L)oopless] file' % sys.argv[0]
        sys.exit(2)


    try:
        (opts, args) = getopt.getopt(sys.argv[1:], 'SL')
    except getopt.GetoptError:
        usage()
    else:
        seekbar, loop = True, True
        for (k, v) in opts:
            if k == '-S':
                seekbar = False
            elif k == '-L':
                loop = False

        if not args:
            usage()
        generate_html(sys.stdout, args[0], seekbar=seekbar, loop=loop)