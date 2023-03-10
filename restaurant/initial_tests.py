import os
import importlib
from django.urls import reverse
from django.test import TestCase
from django.conf import settings

FAILURE_HEADER = f"{os.linesep}{os.linesep}{os.linesep}================{os.linesep}TwD TEST FAILURE =({os.linesep}================{os.linesep}"
FAILURE_FOOTER = f"{os.linesep}"

class InitialProjectStructureTests(TestCase):
    # Simple tests to probe the file structure of your project so far.
    # Also tests whether restaurant was added to the list of INSTALLED_APPS
    def setUp(self):
        self.project_base_dir = os.getcwd()
        self.restaurant_app_dir = os.path.join(self.project_base_dir, 'restaurant')
    
    def test_project_created(self):
        # Tests whether the WAD_Group_Project configuration directory is present and correct.
        
        directory_exists = os.path.isdir(os.path.join(self.project_base_dir, 'WAD_Group_Project'))
        urls_module_exists = os.path.isfile(os.path.join(self.project_base_dir, 'WAD_Group_Project', 'urls.py'))
        
        self.assertTrue(directory_exists, f"{FAILURE_HEADER}Your Group Project configuration directory doesn't seem to exist. Did you use the correct name?{FAILURE_FOOTER}")
        self.assertTrue(urls_module_exists, f"{FAILURE_HEADER}Your project's urls.py module does not exist. Did you use the startproject command?{FAILURE_FOOTER}")
    
    def test_restaurant_app_created(self):
        # Determines whether the Restaurant app has been created.
        directory_exists = os.path.isdir(self.restaurant_app_dir)
        is_python_package = os.path.isfile(os.path.join(self.restaurant_app_dir, '__init__.py'))
        views_module_exists = os.path.isfile(os.path.join(self.restaurant_app_dir, 'views.py'))
        
        self.assertTrue(directory_exists, f"{FAILURE_HEADER}The Restaurant app directory does not exist. Did you use the startapp command?{FAILURE_FOOTER}")
        self.assertTrue(is_python_package, f"{FAILURE_HEADER}The Restaurant directory is missing the python package file. Did you use the startapp command?{FAILURE_FOOTER}")
        self.assertTrue(views_module_exists, f"{FAILURE_HEADER}The Restaurant directory is missing the views file. Did you use the startapp command?{FAILURE_FOOTER}")
        
    def test_restaurant_has_urls_module(self):
        # Tests to see if a seperate urls.py file was created in restaurant
        module_exists = os.path.isfile(os.path.join(self.restaurant_app_dir, 'urls.py'))
        self.assertTrue(module_exists, f"{FAILURE_HEADER}The restaurant app's urls.py module is missing. You need TWO urls.py modules.{FAILURE_FOOTER}")
        
    def test_is_restaurant_app_configured(self):
        # Tests to see if the new restaurant app in the INSTALLED_APPS list
        
        is_app_configured = 'restaurant' in settings.INSTALLED_APPS
        
        self.assertTrue(is_app_configured, f"{FAILURE_HEADER}The restaurant app is missing from your setting's INSTALLED_APPS list.{FAILURE_FOOTER}")
        
class IndexPageTests(TestCase):
    # Testing the index view and URL mapping.
    # Also runs tests to check the response from the server.
    
    def setUp(self):
        self.views_module = importlib.import_module('restaurant.views')
        self.views_module_listing = dir(self.views_module)
        
        self.project_urls_module = importlib.import_module('WAD_Group_Project.urls')
    
    def test_view_exists(self):
        # Checks to see if the index() view exist in Restaurant's views.py module?
        name_exists = 'index' in self.views_module_listing
        is_callable = callable(self.views_module.index)
        
        self.assertTrue(name_exists, f"{FAILURE_HEADER}The index() view for restaurant does not exist.{FAILURE_FOOTER}")
        self.assertTrue(is_callable, f"{FAILURE_HEADER}Check that you have created the index() view correctly. It doesn't seem to be a function!{FAILURE_FOOTER}")
    
    def test_mappings_exists(self):
        # Are the URL mappings present and correct? One should be in the project's urls.py, the second in Rango's urls.py. We have the 'index' view named twice -- it should resolve to '/restaurant/'.
        
        index_mapping_exists = False
        
        # This is overridden. We need to manually check it exists.
        for mapping in self.project_urls_module.urlpatterns:
            if hasattr(mapping, 'name'):
                if mapping.name == 'index':
                    index_mapping_exists = True
        
        self.assertTrue(index_mapping_exists, f"{FAILURE_HEADER}The index URL mapping could not be found. Check the WAD_Group_Project's urls.py module.{FAILURE_FOOTER}")
        self.assertEquals(reverse('restaurant:index'), '/restaurant/', f"{FAILURE_HEADER}The index URL lookup failed. Check Restaurant's urls.py module.{FAILURE_FOOTER}")
        