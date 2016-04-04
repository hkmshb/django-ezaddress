from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from django.db import models



class Country(models.Model):
    """A model for storing Country data."""
    name = models.CharField(max_length=50, unique=True, blank=False)
    code = models.CharField(max_length=3, blank=True)
    
    class Meta:
        verbose_name_plural = 'Countries'
        ordering = ('name',)
    
    def __str__(self):
        return self.name


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

