from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.db.models.fields.related import ForeignObject
try:
    from django.db.models.fields.related_descriptors import ForwardManyToOneDescriptor
except ImportError:
    from django.db.models.fields.related import \
         ReverseSingleRelatedObjectDescriptor as ForwardManyToOneDescriptor
from django.utils.encoding import python_2_unicode_compatible



# python 3 fixes
import sys
if sys.version > '3':
    long = int
    basestring = (str, bytes)
    unicode = str


__all__ = ['Country', 'State', 'Address', 'AddressField']


class InconsistentDictError(Exception):
    pass


def _to_address(value):
    """Converts a dict with proper address keys into an Address object."""
    raw = value.get('raw', '')
    country = value.get('country', '')
    country_code = value.get('country_code', '')
    state = value.get('state', '')
    state_code = value.get('state_code', '')
    postal_code = value.get('postal_code', '')
    street = value.get('street', '')
    town_city = value.get('town_city', '')
    latitude = value.get('latitude', None)
    longitude = value.get('longitude', None)
    
    # raw value is mandatory; if not present dict isn't an Address equivalent
    if not raw:
        return None
    
    # require both or none of country and state, not either 
    if ((country or state) and not (country and state)):
        raise InconsistentDictError
    
    # handle country
    try:
        country_obj = Country.objects.get(name=country)
    except Country.DoesNotExist:
        if country:
            if len(country_code) > Country._meta.get_field('code').max_length:
                if country_code != country:
                    message_fmt = 'Invalid country code (too long): %s' 
                    raise ValueError(_(message_fmt) % country_code)
                country_code = ''
            country_obj = Country.objects.create(name=country, code=country_code)
        else:
            country_obj = None
    
    # handle state
    try:
        state_obj = State.objects.get(name=state)
    except State.DoesNotExist:
        if state:
            if len(state_code) > State._meta.get_field('code').max_length:
                if state_code != state:
                    message_fmt = 'Invalid state code (too long): %s'
                    raise ValueError(_(message_fmt) % state_code)
                state_code = ''
            state_obj = State.objects.create(name=state, code=state_code, 
                                             country=country_obj)
        else:
            state_obj = None
    
    # handle address
    try:
        if not (street or town_city):
            addr_obj = Address.objects.get(raw=raw)
        else:
            addr_obj = Address.objects.get(
                street = street,
                town_city = town_city,
                postal_code = postal_code,
                state = state_obj,
            )
    except Address.DoesNotExist:
        addr_obj = Address(
            raw = raw,
            street = street,
            town_city = town_city,
            postal_code = postal_code,
            state = state_obj,
            latitude = latitude,
            longitude = longitude,
        )
    
    addr_obj.save()
    return addr_obj


def to_address(value):
    if value is None:
        return None
    
    if isinstance(value, Address):
        return value
    elif isinstance(value, (int, long)):
        # assume value is model primary key
        return value
    elif isinstance(value, basestring):
        addr_obj = Address(raw = value)
        addr_obj.save()
        return addr_obj
    elif isinstance(value, dict):
        try:
            return _to_address(value)
        except InconsistentDictError:
            return Address.objects.create(raw=value['raw'])
    
    # value not in any of the recognized formats
    raise ValidationError(_('Invalid address value.'))


@python_2_unicode_compatible
class Country(models.Model):
    """A model for storing Country data."""
    name = models.CharField(max_length=50, unique=True, blank=False)
    code = models.CharField(max_length=3, blank=True)
    
    class Meta:
        verbose_name_plural = 'Countries'
        ordering = ('name',)
    
    def __str__(self):
        return self.name


@python_2_unicode_compatible
class State(models.Model):
    """A model for storing State data."""
    name = models.CharField(max_length=100, blank=False)
    code = models.CharField(max_length=3, blank=True)
    country = models.ForeignKey(Country, blank=False, null=False,
                related_name='states')
    
    class Meta:
        unique_together = ('name', 'country')
        ordering = ('country', 'name')
    
    def __str__(self):
        value = self.name
        if self.country and value:
            value += ', '
        value += self.country.name
        return value


@python_2_unicode_compatible
class Address(models.Model):
    street = models.CharField(_('Street Address'), max_length=100, blank=True)
    town_city = models.CharField(_('Town or City'), max_length=50, blank=True)
    postal_code = models.CharField(max_length=10, blank=True)
    state = models.ForeignKey(State, blank=True, null=True,
                related_name='addresses')
    raw = models.CharField(max_length=200)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    
    class Meta:
        verbose_name_plural = 'Addresses'
        ordering = ('state', 'town_city', 'postal_code', 'street')
    
    def __str__(self):
        if self.state:
            value = ''
            if self.street:
                value = self.street
            
            if self.town_city:
                if value:
                    value += ', '
                value += self.town_city
                
                if self.postal_code:
                    value += ' %s' % self.postal_code
                
            if value:
                value += ', '
            value += str(self.state)
        else:
            value = self.raw
        return value
    
    def clean(self):
        if not self.raw:
            raise ValidationError(_('Addresses may not have a blank `raw` field.'))
    
    def as_dict(self):
        addr = dict(
            street = self.street,
            town_city = self.town_city,
            raw = self.raw,
            latitude = self.latitude if self.latitude else '',
            longitude = self.longitude if self.longitude else ''
        )
        if self.state:
            addr['state'] = self.state.name
            addr['state_code'] = self.state.code 
            addr['postal_code'] = self.postal_code
            if self.state.country:
                addr['country'] = self.state.country.name
                addr['country_code'] = self.state.country.code
        return addr


class AddressDescriptor(ForwardManyToOneDescriptor):
    
    def __set__(self, instance, value):
        super(AddressDescriptor, self).__set__(instance, to_address(value))


class AddressField(models.ForeignKey):
    description = 'An address'
    
    def __init__(self, **kwargs):
        kwargs['to'] = 'ezaddress.Address'
        super(AddressField, self).__init__(**kwargs)
    
    def contribute_to_class(self, cls, name, virtual_only=False):
        super(ForeignObject, self).contribute_to_class(cls, name, virtual_only)
        setattr(cls, self.name, AddressDescriptor(self))

