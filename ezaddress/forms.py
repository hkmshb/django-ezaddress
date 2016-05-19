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
        
        # check for garbage lat/lng/alt entries
        for field in ['latitude', 'longitude', 'altitude']:
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
        
        # also check for garbage gps_error entry
        field = 'gps_error'
        if field in value:
            try:
                value[field] = int(value[field])
            except:
                raise forms.ValidationError(
                    _('Invalid value for %(field)s'),
                    code='invalid', params={'field': field})
        return to_address(value)

