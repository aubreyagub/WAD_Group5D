import os
import warnings
import importlib
from restaurant.models import Menu, MenuItem, Review
from django.urls import reverse
from django.test import TestCase
from django.conf import settings
from django.contrib.auth.models import User

FAILURE_HEADER = f"{os.linesep}{os.linesep}{os.linesep}================{os.linesep}TwD TEST FAILURE =({os.linesep}================{os.linesep}"
FAILURE_FOOTER = f"{os.linesep}"

class DatabaseConfigurationTests(TestCase):
    # tests to see if the database is configured
    
    def setUp(self):
        pass
    
    def does_gitignore_include_database(self, path):
        # checks to see if the db.sqlite3 is present in the .gitignore file
        
        f = open(path, 'r')
        
        for line in f:
            line = line.strip()
            
            if line.startswith('db.sqlite3'):
                return True
        
        f.close()
        return False
    
    def test_databases_variable_exists(self):
        
        self.assertTrue(settings.DATABASES, f"{FAILURE_HEADER}Your project's settings module does not have a DATABASES variable, which is required. {FAILURE_FOOTER}")
        self.assertTrue('default' in settings.DATABASES, f"{FAILURE_HEADER}You do not have a 'default' database configuration in your project's DATABASES configuration variable.{FAILURE_FOOTER}")


class TestModels(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser")
        self.menu = Menu.objects.create(menuID="menu1")
        self.menuItem = MenuItem.objects.create(menuItemID="item1", menu=self.menu)
        self.review = Review.objects.create(reviewID="review1", user=self.user, menuItem=self.menuItem, comment="Great food!", ratings=5)
        
    def test_menu(self):
        self.assertEqual(str(self.menu), self.menu.menuID)
        
    def test_menu_item(self):
        self.assertEqual(str(self.menuItem), self.menuItem.menuItemID)
        
    def test_review(self):
        self.assertEqual(str(self.review), self.review.reviewID)
        
class TestMenuItemModel(TestCase):
    def setUp(self):
        self.menu = Menu.objects.create(menuID="menu1")
        
    def test_menu_item_slug(self):
        menuItem = MenuItem.objects.create(menuItemID="item1", menu=self.menu)
        self.assertEqual(menuItem.slug, "item1")
        
    def test_menu_item_price_default_value(self):
        menuItem = MenuItem.objects.create(menuItemID="item1", menu=self.menu)
        self.assertEqual(menuItem.price, 0.0)
        
    def test_menu_item_str(self):
        menuItem = MenuItem.objects.create(menuItemID="item1", menu=self.menu)
        self.assertEqual(str(menuItem), menuItem.menuItemID)