from django.core.exceptions import ValidationError
from django.test import TestCase

from ezaddress.models import to_address
from ezaddress.models import *



class BaseTestCase(TestCase):
    
    def setUp(self):
        self.al = Country.objects.create(name='Algeria', code='AL')
        self.zm = Country.objects.create(name='Zimbabwe', code='ZW')
        self.ng = Country.objects.create(name='Nigeria', code='NG')
        self.gh = Country.objects.create(name='Ghana', code='GH')


class CountryTestCase(BaseTestCase):
    
    def test_string_representation(self):
        self.assertEqual('Nigeria', str(self.ng))
    
    def test_countries_ordered_by_name_asc(self):
        items = Country.objects.all()
        self.assertEqual(items.count(), 4)
        self.assertEqual(items[0].code, 'AL')
        self.assertEqual(items[1].code, 'GH')
        self.assertEqual(items[2].code, 'NG')
        self.assertEqual(items[3].code, 'ZW')
    
    def test_validation_fails_for_duplicate_name(self):
        country = Country(name='Nigeria', code='??')
        with self.assertRaises(ValidationError):
            country.full_clean()
    
    def test_validation_fails_for_blank_name(self):
        country = Country(code='??')
        with self.assertRaises(ValidationError):
            country.full_clean()
    
    def test_can_save_country_without_code(self):
        Country.objects.create(name='Senegal')
        self.assertEqual(Country.objects.count(), 5)    # 4 created by setUp


class StateTestCase(BaseTestCase):
    
    def setUp(self):
        super(StateTestCase, self).setUp()
        self.ng_dt = State.objects.create(name='Delta', code='DT', country=self.ng)
        self.ng_ab = State.objects.create(name='Abuja', code='AB', country=self.ng)
        self.ng_lg = State.objects.create(name='Lagos', code='LG', country=self.ng)
        self.gh_ac = State.objects.create(name='Accra', code='AC', country=self.gh)
    
    def test_string_representation(self):
        self.assertEqual('Abuja, Nigeria',  str(self.ng_ab))
    
    def test_string_representation_for_state_without_country(self):
        state = State(name='Abuja')
        with self.assertRaises(Exception):
            str(state)
    
    def test_states_ordered_by_country_state_name_asc(self):
        items = State.objects.all()
        self.assertEqual(items.count(), 4)
        self.assertEqual(items[0].code, 'AC')
        self.assertEqual(items[1].code, 'AB')
        self.assertEqual(items[2].code, 'DT')
        self.assertEqual(items[3].code, 'LG')
    
    def test_validation_fails_for_duplicate_name_for_same_country(self):
        state = State(name='Lagos', code='??', country=self.ng)
        with self.assertRaises(ValidationError):
            state.full_clean()
    
    def test_validation_fails_for_blank_country(self):
        state = State(name='Port Harcourt', code='PH')
        with self.assertRaises(ValidationError):
            state.full_clean()
    
    def test_validation_fails_for_blank_name(self):
        state = State(code='PH', country=self.ng)
        with self.assertRaises(ValidationError):
            state.full_clean()
    
    def test_states_without_code_are_valid(self):
        State.objects.create(name='Port Harcourt', country=self.ng)
        self.assertEqual(State.objects.count(), 5)    # 4 created by setUp


class AddressTestCase(BaseTestCase):
    
    def setUp(self):
        super(AddressTestCase, self).setUp()
        self.ng_dt = State.objects.create(name='Delta', code='DT', country=self.ng)
        self.ng_lg = State.objects.create(name='Lagos', code='LG', country=self.ng)
        self.gh_ac = State.objects.create(name='Accra', code='AC', country=self.gh)
        
        self.addr1 = Address.objects.create(
                # include :: in raw to differentiate from __str__ repr
                raw='No 1 Bank Road, Eko 720015, Lagos, Nigeria ::',
                street='No 1 Bank Road', town_city='Eko', 
                postal_code='720015', state=self.ng_lg)
        self.addr2 = Address.objects.create(
                raw='33 Willams Street, Asaba 720016, Delta, Nigeria',
                street='33 Willams Street', town_city='Asaba',
                postal_code='720016', state=self.ng_lg)
        self.addr3 = Address.objects.create(
                raw='5243 Koffi Avenue, Akanta 982201, Accra, Ghana',
                street='5243 Koffi Avenue', town_city='Akanta',
                postal_code='982201', state=self.gh_ac)
        self.addr4 = Address.objects.create(raw='1 Alu Avenue')
    
    def test_string_representation_with_all_fields_provided(self):
        self.assertEqual('No 1 Bank Road, Eko 720015, Lagos, Nigeria',
                         str(self.addr1))
    
    def test_string_representation_with_only_raw_field(self):
        self.assertEqual('1 Alu Avenue', str(self.addr4))
    
    def test_addresses_ordering(self):
        items = Address.objects.all()
        self.assertEqual(items.count(), 4)
        self.assertEqual(items[0].town_city, '')
        self.assertEqual(items[1].town_city, 'Akanta')
        self.assertEqual(items[2].town_city, 'Asaba')
        self.assertEqual(items[3].town_city, 'Eko')
    
    def test_validation_fails_for_blank_raw_field(self):
        addr = Address(street='No 1 Bank Road', town_city='Eko',
                       postal_code='720015', state=self.ng_lg)
        with self.assertRaises(ValidationError):
            addr.full_clean()
    
    def test_getting_address_as_dict(self):
        fields = ('raw','street','town_city','postal_code')
        addr_dict = self.addr1.as_dict()
        
        for f in fields:
            self.assertEqual(getattr(self.addr1, f), addr_dict.get(f))
        
        state = self.addr1.state
        self.assertEqual(state.name, addr_dict.get('state'))
        self.assertEqual(state.code, addr_dict.get('state_code'))
        
        country = state.country
        self.assertEqual(country.name, addr_dict.get('country'))
        self.assertEqual(country.code, addr_dict.get('country_code'))


class AddressFieldTestCase(TestCase):
    
    class TestModel(object):
        address = AddressField()
    
    def setUp(self):
        self.addr_dict = {
            'raw': 'No. 1 Bank Road, Eko 720015, Lagos, Nigeria',
            'street': 'No. 1 Bank Road',
            'town_city': 'Eko',
            'postal_code': '720015',
            'state': 'Lagos',
            'state_code': 'LG',
            'country': 'Nigeria',
            'country_code': 'NG'
        }
        self.test = self.TestModel()
    
    def test_assignment_from_string(self):
        self.test.address = to_address(self.addr_dict['raw'])
        self.assertEqual(self.test.address.raw, self.addr_dict['raw'])
    
    def test_assignment_from_dict(self):
        self.test.address = to_address(self.addr_dict)
        self.assertEqual(self.test.address.raw, self.addr_dict['raw'])
        self.assertEqual(self.test.address.street, self.addr_dict['street'])
        self.assertEqual(self.test.address.town_city, self.addr_dict['town_city'])
        self.assertEqual(self.test.address.postal_code, self.addr_dict['postal_code'])
        self.assertEqual(self.test.address.state.name, self.addr_dict['state'])
        self.assertEqual(self.test.address.state.code, self.addr_dict['state_code'])
        self.assertEqual(self.test.address.state.country.name, self.addr_dict['country'])
        self.assertEqual(self.test.address.state.country.code, self.addr_dict['country_code'])
    
    def test_assignment_from_dict_with_no_country(self):
        addr_dict = {
            'raw': 'No 1 Bank Road, Eko 720015, Lagos, Nigeria',
            'street': 'No. 1 Bank Road',
            'town_city': 'Eko',
            'postal_code': '720015',
            'state': 'Lagos',
            'state_code': 'LG',
        }
        self.test.address = to_address(addr_dict)
        self.assertEqual(self.test.address.raw, addr_dict['raw'])
        self.assertEqual(self.test.address.street, '')
        self.assertEqual(self.test.address.town_city, '')
        self.assertEqual(self.test.address.postal_code, '')
        self.assertEqual(self.test.address.state, None)
    
    def test_assignment_from_dict_with_no_state(self):
        addr_dict = {
            'raw': 'No 1 Bank Road, Eko 720015, Lagos, Nigeria',
            'street': 'No. 1 Bank Road',
            'town_city': 'Eko',
            'postal_code': '720015',
            'country': 'Nigeria',
            'country_code': 'NG',
        }
        self.test.address = to_address(addr_dict)
        self.assertEqual(self.test.address.raw, addr_dict['raw'])
        self.assertEqual(self.test.address.street, '')
        self.assertEqual(self.test.address.town_city, '')
        self.assertEqual(self.test.address.postal_code, '')
        self.assertEqual(self.test.address.state, None)
    
    def test_assignment_from_dict_with_only_address(self):
        addr_dict = {
            'raw': 'No 1 Bank Road, Eko 720015, Lagos, Nigeria',
            'street': 'No. 1 Bank Road',
            'town_city': 'Eko',
            'postal_code': '720015',
        }
        self.test.address = to_address(addr_dict)
        self.assertEqual(self.test.address.raw, addr_dict['raw'])
        self.assertEqual(self.test.address.street, addr_dict['street'])
        self.assertEqual(self.test.address.town_city, addr_dict['town_city'])
        self.assertEqual(self.test.address.postal_code, addr_dict['postal_code'])
        self.assertEqual(self.test.address.state, None)
    
    
    def test_assignment_from_dict_with_duplicate_country_code(self):
        addr_dict = {
            'raw': 'No 1 Bank Road, Eko 720015, Lagos, Nigeria',
            'street': 'No. 1 Bank Road',
            'town_city': 'Eko',
            'postal_code': '720015',
            'state': 'Lagos',
            'state_code': 'LG',
            'country': 'Nigeria',
            'country_code': 'Nigeria',
        }
        self.test.address = to_address(addr_dict)
        self.assertEqual(self.test.address.raw, addr_dict['raw'])
        self.assertEqual(self.test.address.street, addr_dict['street'])
        self.assertEqual(self.test.address.town_city, addr_dict['town_city'])
        self.assertEqual(self.test.address.postal_code, addr_dict['postal_code'])
        self.assertEqual(self.test.address.state.name, 'Lagos')
        self.assertEqual(self.test.address.state.code, 'LG')
        self.assertEqual(self.test.address.state.country.name, 'Nigeria')
        self.assertEqual(self.test.address.state.country.code, '')
    
    def test_assignment_from_dict_with_invalid_country_code(self):
        addr_dict = {
            'raw': 'No 1 Bank Road, Eko 720015, Lagos, Nigeria',
            'street': 'No. 1 Bank Road',
            'town_city': 'Eko',
            'postal_code': '720015',
            'state': 'Lagos',
            'state_code': 'LG',
            'country': 'Nigeria',
            'country_code': 'Something;Invalid',
        }
        with self.assertRaises(ValueError):
            to_address(addr_dict)
    
    def test_assignment_from_dict_with_invalid_state_code(self):
        addr_dict = {
            'raw': 'No 1 Bank Road, Eko 720015, Lagos, Nigeria',
            'street': 'No. 1 Bank Road',
            'town_city': 'Eko',
            'postal_code': '720015',
            'state': 'Lagos',
            'state_code': 'Something;Invalid',
            'country': 'Nigeria',
            'country_code': 'NG',
        }
        with self.assertRaises(ValueError):
            to_address(addr_dict)

