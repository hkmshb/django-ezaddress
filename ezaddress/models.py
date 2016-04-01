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
