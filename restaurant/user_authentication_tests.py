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
    
    def test_registrationform_template(self):
        #  Does the registration_form.html template exist in the correct place
        
        template_base_path = os.path.join(settings.TEMPLATE_DIR, 'registration')
        template_path = os.path.join(template_base_path, 'registration_form.html')
        self.assertTrue(os.path.exists(template_path), f"{FAILURE_HEADER}We couldn't find the 'registration_form.html' template in the 'templates/registration/' directory.{FAILURE_FOOTER}")

        template_str = get_template(template_path)
        full_title_pattern = r'<title>(.*?)\s*-\s*Register\s*</title>'
        block_title_pattern = r'{% block title_block %}(\s*|\n*)Register(\s*|\n*){% (endblock|endblock title_block) %}'

        self.assertTrue(re.search(block_title_pattern, template_str), f"{FAILURE_HEADER}Is register.html using template inheritance? Is your <title> block correct?{FAILURE_FOOTER}")
    

class LoginTests(TestCase):
    """
    A series of tests for checking the login functionality of restaurant.
    """
    

class RestrictedAccessTests(TestCase):
    """
    Some tests to test the restricted access view. Can users who are not logged in see it?
    """
    def test_restricted_url_exists(self):
        """
        Checks to see if the new restricted view exists in the correct place, with the correct name.
        """
        url = ''

        try:
            url = reverse('restaurant:restricted')
        except:
            pass
        
        self.assertEqual(url, '/restaurant/restricted/', f"{FAILURE_HEADER}Have you created the restaurant:restricted URL mapping correctly? It should point to the new restricted() view, and have a URL of '/restaurant/restricted/' Remember the first part of the URL (/restaurant/) is handled by the project's urls.py module, and the second part (restricted/) is handled by the restaurant app's urls.py module.{FAILURE_FOOTER}")
    
    def test_good_request(self):
        """
        Attempts to access the restricted view when logged in.
        This should not redirect. We cannot test the content here. Only links in base.html can be checked -- we do this in the exercise tests.
        """
        create_user_object()
        self.client.login(username='testuser', password='testabc123')

        response = self.client.get(reverse('restaurant:restricted'))
        self.assertTrue(response.status_code, 200)


class LogoutTests(TestCase):
    """
    A few tests to check the functionality of logging out. Does it work? Does it actually log you out?
    """
    