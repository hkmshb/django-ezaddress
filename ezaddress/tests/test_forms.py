from django.forms import Form, ValidationError
from django.test import TestCase

from ezaddress.forms import AddressField, AddressWidget
from ezaddress.models import Address



class TestForm(Form):
    address = AddressField()


class AddressFieldTestCase(TestCase):
    
    def setUp(self):
        self.form = TestForm()
        self.field = self.form.base_fields['address']
    
    def test_converting_none_to_address(self):
        self.assertEqual(self.field.to_python(None), None)
    
    def test_converting_empty_string_to_address(self):
        self.assertEqual(self.field.to_python(''), None)
    
    def test_convertion_for_invalid_lat_lng(self):
        self.assertRaises(ValidationError, self.field.to_python, {'latitude': 'x'})
        self.assertRaises(ValidationError, self.field.to_python, {'longitude': 'x'})
    
    def test_convertion_for_empty_lat_lng(self):
        self.assertEqual(self.field.to_python({'latitude': ''}), None)
        self.assertEqual(self.field.to_python({'longitude': ''}), None)
    
    def test_convertion_for_dict_with_only_raw_entry(self):
        addr = self.field.to_python({'raw': 'No 1 Bank Road'})
        self.assertEqual(addr.raw, 'No 1 Bank Road')
    
