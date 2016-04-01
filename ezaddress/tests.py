from django.core.exceptions import ValidationError
from django.test import TestCase

from ezaddress.models import Country, State



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



