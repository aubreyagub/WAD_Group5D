import os
import re
import inspect
import tempfile
import restaurant.models
from restaurant import forms
from populate_restaurant import populate
from django.db import models
from django.test import TestCase
from django.conf import settings
from django.urls import reverse, resolve
from django.contrib.auth.models import User
from django.forms import fields as django_fields

FAILURE_HEADER = f"{os.linesep}{os.linesep}{os.linesep}================{os.linesep}TwD TEST FAILURE =({os.linesep}================{os.linesep}"
FAILURE_FOOTER = f"{os.linesep}"

f"{FAILURE_HEADER} {FAILURE_FOOTER}"


def create_user_object():
    """
    Helper function to create a User object.
    """
    user = User.objects.get_or_create(username='testuser',
                                      first_name='Test',
                                      last_name='User',
                                      email='test@test.com')[0]
    user.set_password('testabc123')
    user.save()

    return user

def create_super_user_object():
    # Helper function to create a super user (admin) account.

    return User.objects.create_superuser('admin', 'admin@test.com', 'testpassword')

def get_template(path_to_template):
    # Helper function to return the string representation of a template file.
    
    f = open(path_to_template, 'r')
    template_str = ""

    for line in f:
        template_str = f"{template_str}{line}"

    f.close()
    return template_str



class ModelTests(TestCase):
    # Tests to check whether the UserProfile model has been created according to the specification.
    
    def test_userprofile_class(self):
        # Checks to see if UserProfile exists in restaurant.models and that it contains all required attributes
        
        self.assertTrue('UserProfile' in dir(restaurant.models))

        user_profile = restaurant.models.UserProfile()

        # Now check that all the required attributes are present.
        # We do this by building up a UserProfile instance, and saving it.
        expected_attributes = {
            'website': 'www.google.com',
            'picture': tempfile.NamedTemporaryFile(suffix=".jpg").name,
            'user': create_user_object(),
        }

        expected_types = {
            'website': models.fields.URLField,
            'picture': models.fields.files.ImageField,
            'user': models.fields.related.OneToOneField,
        }

        found_count = 0

        for attr in user_profile._meta.fields:
            attr_name = attr.name

            for expected_attr_name in expected_attributes.keys():
                if expected_attr_name == attr_name:
                    found_count += 1

                    self.assertEqual(type(attr), expected_types[attr_name], f"{FAILURE_HEADER}The type of attribute for '{attr_name}' was '{type(attr)}'; we expected '{expected_types[attr_name]}'. Check your definition of the UserProfile model.{FAILURE_FOOTER}")
                    setattr(user_profile, attr_name, expected_attributes[attr_name])
        
        self.assertEqual(found_count, len(expected_attributes.keys()), f"{FAILURE_HEADER}In the UserProfile model, {found_count} attributes were found, but we are expecting {len(expected_attributes.keys())}.{FAILURE_FOOTER}")
        user_profile.save()


class RegisterFormClassTests(TestCase):
    # A series of tests to check whether the UserForm and UserProfileForm have been created as per the specification.

    def test_user_form(self):

        self.assertTrue('UserForm' in dir(forms), f"{FAILURE_HEADER}We couldn't find the UserForm class in restaurant's forms.py module. {FAILURE_FOOTER}")
        
        user_form = forms.UserForm()
        self.assertEqual(type(user_form.__dict__['instance']), User, f"{FAILURE_HEADER}Your UserForm does not match up to the User model. Check your Meta definition of UserForm.{FAILURE_FOOTER}")

        fields = user_form.fields
        
        expected_fields = {
            'username': django_fields.CharField,
            'email': django_fields.EmailField,
            'password': django_fields.CharField,
        }
        
        for expected_field_name in expected_fields:
            expected_field = expected_fields[expected_field_name]

            self.assertTrue(expected_field_name in fields.keys(), f"{FAILURE_HEADER}The field {expected_field_name} was not found in the UserForm form. Check you have complied with the specification.{FAILURE_FOOTER}")
            self.assertEqual(expected_field, type(fields[expected_field_name]), f"{FAILURE_HEADER}The field {expected_field_name} in UserForm was not of the correct type. Expected {expected_field}; got {type(fields[expected_field_name])}.{FAILURE_FOOTER}")
    
    def test_user_profile_form(self):
        self.assertTrue('UserProfileForm' in dir(forms), f"{FAILURE_HEADER}We couldn't find the UserProfileForm class in restaurant's forms.py module.{FAILURE_FOOTER}")
        
        user_profile_form = forms.UserProfileForm()
        self.assertEqual(type(user_profile_form.__dict__['instance']), restaurant.models.UserProfile, f"{FAILURE_HEADER}Your UserProfileForm does not match up to the UserProfile model. Check your Meta definition of UserProfileForm.{FAILURE_FOOTER}")

        fields = user_profile_form.fields

        expected_fields = {
            'website': django_fields.URLField,
            'picture': django_fields.ImageField,
        }

        for expected_field_name in expected_fields:
            expected_field = expected_fields[expected_field_name]

            self.assertTrue(expected_field_name in fields.keys(), f"{FAILURE_HEADER}The field {expected_field_name} was not found in the UserProfile form. Check you have complied with the specification.{FAILURE_FOOTER}")
            self.assertEqual(expected_field, type(fields[expected_field_name]), f"{FAILURE_HEADER}The field {expected_field_name} in UserProfileForm was not of the correct type. Expected {expected_field}; got {type(fields[expected_field_name])}.{FAILURE_FOOTER}")


class RegistrationTests(TestCase):
    # tests related to registering a user.
    
    def test_installed_apps(self):
        # Checks whether the 'registration' app has been included in INSTALLED_APPS.
        
        self.assertTrue('registration' in settings.INSTALLED_APPS)
    
    def test_registration_templates(self):
        #  Does the registration_form.html template exist in the correct place
        
        template_base_path = os.path.join(settings.TEMPLATE_DIR, 'registration')
        registration_form_template_path = os.path.join(template_base_path, 'registration_form.html')
        login_template_path = os.path.join(template_base_path, 'login.html')
        logout_template_path = os.path.join(template_base_path, 'logout.html')
        
        self.assertTrue(os.path.exists(registration_form_template_path), f"{FAILURE_HEADER}We couldn't find the 'registration_form.html' template in the 'templates/registration/' directory.{FAILURE_FOOTER}")
        
        self.assertTrue(os.path.exists(login_template_path), f"{FAILURE_HEADER}We couldn't find the 'login.html' template in the 'templates/registration/' directory.{FAILURE_FOOTER}")
        
        self.assertTrue(os.path.exists(logout_template_path), f"{FAILURE_HEADER}We couldn't find the 'logout.html' template in the 'templates/registration/' directory.{FAILURE_FOOTER}")

        registration_form_template_str = get_template(registration_form_template_path)
        registration_form_block_title_pattern = r'{% block title_block %}(\s*|\n*)Register(\s*|\n*){% (endblock|endblock title_block) %}'

        self.assertTrue(re.search(registration_form_block_title_pattern, registration_form_template_str), f"{FAILURE_HEADER}Is registration_form.html using template inheritance? Is your <title> block correct?{FAILURE_FOOTER}")
        
        login_template_str = get_template(login_template_path)
        login_block_title_pattern = r'{% block title_block %}(\s*|\n*)Login(\s*|\n*){% (endblock|endblock title_block) %}'

        self.assertTrue(re.search(login_block_title_pattern, login_template_str), f"{FAILURE_HEADER}Is login.html using template inheritance? Is your <title> block correct?{FAILURE_FOOTER}")
        
        logout_template_str = get_template(logout_template_path)
        logout_block_title_pattern = r'{% block title_block %}(\s*|\n*)Logged Out(\s*|\n*){% (endblock|endblock title_block) %}'

        self.assertTrue(re.search(logout_block_title_pattern, logout_template_str), f"{FAILURE_HEADER}Is logout.html using template inheritance? Is your <title> block correct?{FAILURE_FOOTER}")
        
    def test_good_form_creation(self):
        # Creates a UserProfileForm and UserForm, and attempts to save them.
        # Upon completion, we should be able to login with the details supplied.
    
        user_data = {'username': 'testuser', 'password': 'test123', 'email': 'test@test.com'}
        user_form = forms.UserForm(data=user_data)

        user_profile_data = {'website': 'http://www.bing.com', 'picture': tempfile.NamedTemporaryFile(suffix=".jpg").name}
        user_profile_form = forms.UserProfileForm(data=user_profile_data)

        self.assertTrue(user_form.is_valid(), f"{FAILURE_HEADER}The UserForm was not valid after entering the required data.{FAILURE_FOOTER}")
        self.assertTrue(user_profile_form.is_valid(), f"{FAILURE_HEADER}The UserProfileForm was not valid after entering the required data.{FAILURE_FOOTER}")

        user_object = user_form.save()
        user_object.set_password(user_data['password'])
        user_object.save()
        
        user_profile_object = user_profile_form.save(commit=False)
        user_profile_object.user = user_object
        user_profile_object.save()
        
        self.assertEqual(len(User.objects.all()), 1, f"{FAILURE_HEADER}Expecting to see a User object created, but it didn't appear.{FAILURE_FOOTER}")
        self.assertEqual(len(restaurant.models.UserProfile.objects.all()), 1, f"{FAILURE_HEADER} Expecting to see a UserProfile object created, but it didn't appear.{FAILURE_FOOTER}")
        self.assertTrue(self.client.login(username='testuser', password='test123'), f"{FAILURE_HEADER}Couldn't log  sample user in during the tests.{FAILURE_FOOTER}")
        
class LoginTests(TestCase):
    # A series of tests for checking the login functionality of restaurant.
    
    def test_login_functionality(self):
        
        # Tests the login functionality. A user should be able to log in, and should be redirected to the Restaurant homepage.
       
        user_object = create_user_object()

        response = self.client.post(reverse('auth_login'), {'username': 'testuser', 'password': 'testabc123'})
        
        try:
            self.assertEqual(user_object.id, int(self.client.session['_auth_user_id']), f"{FAILURE_HEADER}A ttempted to log a user in with an ID of {user_object.id}, but instead logged a user in with an ID of {self.client.session['_auth_user_id']}.{FAILURE_FOOTER}")
        except KeyError:
            self.assertTrue(False, f"{FAILURE_HEADER}When attempting to log in, it didn't seem to log the user in. {FAILURE_FOOTER}")

        self.assertEqual(response.status_code, 302, f"{FAILURE_HEADER}Testing your login functionality, logging in was successful. However, we expected a redirect; we got a status code of {response.status_code} instead.{FAILURE_FOOTER}")
        self.assertEqual(response.url, reverse('restaurant:index'), f"{FAILURE_HEADER}We were not redirected to the restaurant homepage after logging in.{FAILURE_FOOTER}")
        
    

class RestrictedAccessTests(TestCase):
    # Some tests to test the restricted access view. Can users who are not logged in see it?
   
    def test_restricted_url_exists(self):
        #Checks to see if the new restricted view exists in the correct place, with the correct name.
        
        url = ''

        try:
            url = reverse('restaurant:restricted')
        except:
            pass
        
        self.assertEqual(url, '/restaurant/restricted/', f"{FAILURE_HEADER}the restricted URL does not exist.{FAILURE_FOOTER}")
    
    def test_good_request(self):
        # Attempts to access the restricted view when logged in. This should not redirect. 
        
        create_user_object()
        self.client.login(username='testuser', password='testabc123')

        response = self.client.get(reverse('restaurant:restricted'))
        self.assertTrue(response.status_code, 200)
    
class LogoutTests(TestCase):
    # A few tests to check the functionality of logging out
    
    def test_bad_request(self):
        # Attepts to log out a user who is not logged in.
       
        response = self.client.get(reverse('auth_logout'))
        self.assertTrue(response.status_code, 302)
    
    def test_good_request(self):
        # Attempts to log out a user who is logged in.
        
        user_object = create_user_object()
        self.client.login(username='testuser', password='testabc123')
        
        try:
            self.assertEqual(user_object.id, int(self.client.session['_auth_user_id']), f"{FAILURE_HEADER}Attempted to log a user in with an ID of {user_object.id}, but instead logged a user in with an ID of {self.client.session['_auth_user_id']}. {FAILURE_FOOTER}")
        except KeyError:
            self.assertTrue(False, f"{FAILURE_HEADER}When attempting to log a user in, it failed.{FAILURE_FOOTER}")
        
        # Now log the user out.
        response = self.client.get(reverse('auth_logout'))
        
        self.assertTrue('_auth_user_id' not in self.client.session, f"{FAILURE_HEADER}Logging out didn't actually log the user out.{FAILURE_FOOTER}")
    
    