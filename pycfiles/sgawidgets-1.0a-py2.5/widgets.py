# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sgawidgets/widgets.py
# Compiled at: 2009-01-20 10:46:22
import pkg_resources
from turbogears.widgets import CSSLink, JSLink, Widget, WidgetDescription, register_static_directory, JSSource
js_dir = pkg_resources.resource_filename('sgawidgets', 'static/javascript')
register_static_directory('sgawidgets', js_dir)
modalpopup_js = JSLink('sgawidgets', 'ModalPopups.js')

class ModalPopupSGA(Widget):
    """
        Coleccion de popups modales basados en la libreria:
        http://www.modalpopups.com, este genera un popup mientras
        consigue un url
        shadow: true,
        shadowSize: 5,
        shadowColor: "#333333",
        backgroundColor: "#CCCCCC",
        borderColor: "#999999",
        titleBackColor: "#C1D2E7",
        titleFontColor: "#15428B",
        popupBackColor: "#C7D6E9",
        popupFontColor: "black",
        footerBackColor: "#C1D2E7",
        footerFontColor: "#15428B",
        okButtonText: "OK",
        yesButtonText: "Yes",
        noButtonText: "No",
        cancelButtonText: "Cancel",
        fontFamily: "Verdana,Arial",
        fontSize: "9pt"
    """
    javascript = [
     modalpopup_js]
    template = '<a href="${href}" rel="poploading">${text}</a>'

    def __init__(self, **kwargs):
        """
            Establecer las opciones por defecto de esta libreria, esta libreria acepta:
            argumentos de acuerdo al desc de esta clase
        """
        if len(kwargs) > 0:
            chunk = ('\n').join([ '%s: "%s"' % (k, kwargs[k]) for k in kwargs.keys() ])
            default_js = JSSource('ModalPopups.SetDefaults(%s)' % chunk)
            self.javascript.append(default_js)
        super(ModalPopupSGA, self).__init__()


class ModalPopupSGALoading(ModalPopupSGA):
    """
        Waiting indicator while loading a url
        id = 'id for generated indicator'
        title = 'titulo de la ventana'
        msg = 'may embed html'
        params = {width: 300, height: 200} 
    """
    template = '<a href="${href}" rel="poploading">${text}</a>'
    loading_template = '\n      // Extender las funciones de popups acordemente\n        function ModalPopupsEsperar(url){\n            ModalPopups.Indicator("%s",\n                "%s",\n                "%s",\n                %s);\n            document.location=url;\n        }\n    '

    def __init__(self, id='no_id', title='no title', msg='no mensaje', params={}, **extra_params):
        loading_js = JSSource(self.loading_template % (id, title, msg, params))
        self.javascript.append(loading_js)
        super(ModalPopupSGA, self).__init__(**extra_params)


class MyModalPopupSGADescription(WidgetDescription):
    """La descripción de este widget"""
    name = 'Widgets to generate waiting or loading msg, based on ModalPopups'
    full_class_name = 'sgawidgets.ModalPopupSGALoading'
    for_widget = ModalPopupSGA()
    template = '<div>%s</div>' % ModalPopupSGA.__doc__.replace('\n', '<br/>')