import os
import re
import importlib
from django.urls import reverse
from django.test import TestCase, Client
from django.conf import settings
from bs4 import BeautifulSoup


FAILURE_HEADER = f"{os.linesep}{os.linesep}{os.linesep}================{os.linesep}TwD TEST FAILURE =({os.linesep}================{os.linesep}"
FAILURE_FOOTER = f"{os.linesep}"

class TemplatesStructureTests(TestCase):
    # Tests to make sure templates, static files and media files are set up correctly
    
    def setUp(self):
        self.project_base_dir = os.getcwd()
        self.templates_dir = os.path.join(self.project_base_dir, 'templates')
        self.restaurant_templates_dir = os.path.join(self.templates_dir, 'restaurant')
    
    def test_templates_directory_exists(self):
        # Does the templates/ directory exist?
    
        directory_exists = os.path.isdir(self.templates_dir)
        directory_exists = os.path.isdir(self.restaurant_templates_dir)
        
        self.assertTrue(directory_exists, f"{FAILURE_HEADER}Your project's templates directory does not exist.{FAILURE_FOOTER}")
        self.assertTrue(directory_exists, f"{FAILURE_HEADER}The Restaurant templates directory does not exist.{FAILURE_FOOTER}")
        
    def test_template_dir_setting(self):
        # Does the TEMPLATE_DIR setting exist, and does it point to the right directory?
        
        variable_exists = 'TEMPLATE_DIR' in dir(settings)
        self.assertTrue(variable_exists, f"{FAILURE_HEADER}Your settings.py module does not have the variable TEMPLATE_DIR defined.{FAILURE_FOOTER}")
        
        template_dir_value = os.path.normpath(settings.TEMPLATE_DIR)
        template_dir_computed = os.path.normpath(self.templates_dir)
        self.assertEqual(template_dir_value, template_dir_computed, f"{FAILURE_HEADER}Your TEMPLATE_DIR setting does not point to the expected path. Check your configuration, and try again.{FAILURE_FOOTER}")
        
    def test_templates_exist(self):
        # Do the index.html, about.html, base.html, categories.html, login.html, register.html, and restricted.html templates exist in the correct place?
        
        index_path = os.path.join(self.restaurant_templates_dir, 'index.html')
        about_path = os.path.join(self.restaurant_templates_dir, 'about.html')
        base_path = os.path.join(self.restaurant_templates_dir, 'base.html')
        categories_path = os.path.join(self.restaurant_templates_dir, 'categories.html')
        login_path = os.path.join(self.restaurant_templates_dir, 'login.html')
        register_path = os.path.join(self.restaurant_templates_dir, 'register.html')
        restricted_path = os.path.join(self.restaurant_templates_dir, 'restricted.html')
        
        self.assertTrue(os.path.isfile(index_path), f"{FAILURE_HEADER}Your index.html template does not exist, or is in the wrong location.{FAILURE_FOOTER}")
        self.assertTrue(os.path.isfile(about_path), f"{FAILURE_HEADER}Your about.html template does not exist, or is in the wrong location.{FAILURE_FOOTER}")
        

class BaseTemplateTest(TestCase):
    def setUp(self):
        self.project_base_dir = os.getcwd()
        self.templates_dir = os.path.join(self.project_base_dir, 'templates')
        self.restaurant_templates_dir = os.path.join(self.templates_dir, 'restaurant')
        self.client = Client()
        
    def test_css_present(self):
        base_path = os.path.join(self.restaurant_templates_dir, 'base.html')
        file = open(base_path)

        soup = BeautifulSoup(file, 'html.parser')

        # find the <link> element with the specific href value
        link = soup.find('link', href="{% static 'css/style.css' %}")

        # get the href attribute value of the <link> element
        href = link.get('href')
        
        self.assertEqual(href, "{% static 'css/style.css' %}", f"{FAILURE_HEADER}No CSS Style sheet found in base.html.{FAILURE_FOOTER}")
        
    def test_css(self):
        response = self.client.get('/')
        self.assertContains(response, 'css/style.css', status_code=200)
        self.assertContains(response, 'font-awesome.min.css', status_code=200)
        self.assertContains(response, 'bootstrap.min.css', status_code=200)

    def test_jquery(self):
        response = self.client.get('/')
        self.assertContains(response, 'jquery.slim.min.js', status_code=200)
        self.assertContains(response, 'popper.min.js', status_code=200)
        self.assertContains(response, 'bootstrap.bundle.min.js', status_code=200)

    def test_ajax(self):
        response = self.client.get('/')
        self.assertContains(response, 'jquery-3.2.1.slim.min.js', status_code=200)
        self.assertContains(response, 'popper.min.js', status_code=200)
        self.assertContains(response, 'bootstrap.min.js', status_code=200)

class IndexPageTests(TestCase):
    # A series of tests to ensure that the index page/view has been updated to work with templates.
    
    def setUp(self):
        self.response = self.client.get(reverse('restaurant:index'))
    
    def test_index_uses_template(self):
        # Checks whether the index view uses a template -- and the correct one!
        
        self.assertTemplateUsed(self.response, 'restaurant/index.html', f"{FAILURE_HEADER}Your index() view does not use the expected index.html template.{FAILURE_FOOTER}")
    
class StaticTests(TestCase):
    # A series of tests to check whether static files have been setup and used correctly.
    
    def setUp(self):
        self.project_base_dir = os.getcwd()
        self.static_dir = os.path.join(self.project_base_dir, 'static')
        self.media_dir = os.path.join(self.project_base_dir, 'media')
    
    def test_does_static_directory_exist(self):
        # Tests whether the static directory exists in the correct location -- and the images subdirectory.

        does_static_dir_exist = os.path.isdir(self.static_dir)
        does_images_static_dir_exist = os.path.isdir(os.path.join(self.static_dir, 'images'))
        
        self.assertTrue(does_static_dir_exist, f"{FAILURE_HEADER}The static directory was not found in the expected location. Check the instructions in the book, and try again.{FAILURE_FOOTER}")
        self.assertTrue(does_images_static_dir_exist, f"{FAILURE_HEADER}The images subdirectory was not found in your static directory.{FAILURE_FOOTER}")
    
    def test_static_configuration(self):
        
        static_dir_exists = 'STATIC_DIR' in dir(settings)
        self.assertTrue(static_dir_exists, f"{FAILURE_HEADER}Your settings.py module does not have the variable STATIC_DIR defined.{FAILURE_FOOTER}")
        
        expected_path = os.path.normpath(self.static_dir)
        static_path = os.path.normpath(settings.STATIC_DIR)
        self.assertEqual(expected_path, static_path, f"{FAILURE_HEADER}The value of STATIC_DIR does not equal the expected path. It should point to your project root, with 'static' appended to the end of that.{FAILURE_FOOTER}")
        
        staticfiles_dirs_exists = 'STATICFILES_DIRS' in dir(settings)
        self.assertTrue(staticfiles_dirs_exists, f"{FAILURE_HEADER}The required setting STATICFILES_DIRS is not present in your project's settings.py module. Check your settings carefully. So many students have mistyped this one.{FAILURE_FOOTER}")
        self.assertEqual([static_path], settings.STATICFILES_DIRS, f"{FAILURE_HEADER}Your STATICFILES_DIRS setting does not match what is expected. Check your implementation against the instructions provided.{FAILURE_FOOTER}")
        
        staticfiles_dirs_exists = 'STATIC_URL' in dir(settings)
        self.assertTrue(staticfiles_dirs_exists, f"{FAILURE_HEADER}The STATIC_URL variable has not been defined in settings.py.{FAILURE_FOOTER}")
        self.assertEqual('/static/', settings.STATIC_URL, f"{FAILURE_HEADER}STATIC_URL does not meet the expected value of /static/. Make sure you have a slash at the end!{FAILURE_FOOTER}")
        
    