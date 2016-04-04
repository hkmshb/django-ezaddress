from django.utils.translation import ugettext_lazy as _
from django import forms

from .models import Address, to_address



# python 3 fixes
import sys
if sys.version > '3':
    long = int
    basestring = (str, bytes)
    unicode = str


__all__ = ['AddressWidget', 'AddressField']


class AddressWidget(forms.TextInput):
    pass


class AddressField(forms.ModelChoiceField):
    widget = AddressWidget
    
    def __init__(self, *args, **kwargs):
        kwargs['queryset'] = Address.objects.none()
        super(AddressField, self).__init__(*args, **kwargs)
    
    def to_python(self, value):
        if value is None or value == '':
            return None
        
        # check for garbage lat/lng entries
        for field in ['latitude', 'longitude']:
            if field in value:
                if value[field]:
                    try:
                        value[field] = float(value[field])
                    except:
                        raise forms.ValidationError(
                            _('Invalid value for %(field)s'),
                            code='invalid', params={'field': field})
                else:
                    value[field] = None
        return to_address(value)

