import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'WAD_Group_Project.settings')

import django
django.setup()
from restaurant.models import Menu,MenuItem,Review

def populate():
    # Main Menu
    mainMenu_menuItems = [
        {'menuItemID': 'Spaghetti',
         'description': 'Drumwheat pasta with ragu sauce and parmesan cheese.',
         'price': 10.99,
         'photo': None},
        {'menuItemID': 'Chicken Burger',
         'description': 'Chicken burger pate with tomatoes, lettuce and ketchup in a brioche bun.',
         'price':7.49,
         'photo': None},
        {'menuItemID': 'Sweet Potato Fries',
         'description': 'Deep-fried thin sweet potato slices with cajun seasoning.',
         'price':5,
         'photo': None}]


    # Drinks Menu
    drinks_menuItems = [
        {'menuItemID': 'Orange Juice',
         'description': 'Freshly squeezed orange juice.',
         'price': 2.49,
         'photo': None},
        {'menuItemID': 'Hot Chocolate',
         'description': 'Made with oat milk, topped with marshmallows and cream.',
         'price': 2.99,
         'photo': None}]


    # note: add more menus on this area when required
    # dictionary of dictionaries of all menus
    menus = {'Main Menu': {'menuItems': mainMenu_menuItems},
            'Drinks Menu': {'menuItems': drinks_menuItems}}


    for menuID, menu_data in menus.items():
        m = add_menu(menuID)
        for mI in menu_data['menuItems']:
            add_menuItem(m, menuItemID = mI['menuItemID'], description=mI['description'], price=mI['price'], photo=mI['photo'])

    for m in Menu.objects.all():
        for mI in MenuItem.objects.filter(menu=m):
            print(f'- {m}: {mI}')

# functions used above to add the pages and categories 
def add_menuItem(menu, menuItemID, description, price, photo):
    mI = MenuItem.objects.get_or_create(menu=menu, menuItemID=menuItemID)[0]
    mI.description=description
    mI.price = price
    mI.photo = None;
    mI.save
    return mI

def add_menu(menuID):
    m = Menu.objects.get_or_create(menuID=menuID)[0]
    m.save()
    return m

# note: this is where code execution begins
if __name__ == '__main__':
    print('Starting Restaurant population script...')
    populate()