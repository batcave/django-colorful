# -*- coding: utf-8 -*-
from django.conf import settings
from django.forms.widgets import TextInput
from django.utils.safestring import SafeUnicode

try:
    url = settings.STATIC_URL
except AttributeError:
    try:
        url = settings.MEDIA_URL
    except AttributeError:
        url = ''

class ColorFieldWidget(TextInput):
    class Media:
        css = {
            'all': ("%scolorful/css/colorPicker.css" % url,)
        }
        js  = ("%scolorful/js/colorpicker.js" % url,)

    input_type = 'color'

    def render_script(self, id, color):
        return u'''<div class='django-color-picker'><div style="background-color: #%s"></div></div>
        <script type="text/javascript">
                        django.jQuery(document).ready(function($){

                            $('.django-color-picker').ColorPicker({
    color: '#%s',
    onShow: function (colpkr) {
        $(colpkr).fadeIn(500);
        return false;
    },
    onHide: function (colpkr) {
        $(colpkr).fadeOut(500);
        return false;
    },
    onChange: function (hsb, hex, rgb) {
        $('#%s').val(hex).next('.django-color-picker').children('div').css('backgroundColor', '#' + hex);
    }
});
                        });
                </script>
                ''' % (color, color, id)

    def render(self, name, value, attrs={}):
        if not 'id' in attrs:
            attrs['id'] = "#id_%s" % name
        render = super(ColorFieldWidget, self).render(name, value, attrs)
        print value
        return SafeUnicode(u"%s%s" % (render, self.render_script(attrs['id'], value)))
