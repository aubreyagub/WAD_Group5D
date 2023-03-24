import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'WAD_Group_Project.settings')

import django
from django.core.files import File

django.setup()
from restaurant.models import Menu,MenuItem,Review,User

def populate():
    # Spaghetti Reviews
    spaghetti_reviews = [
        {'reviewID': 'Delicious spaghetti',
         'user_id':2,
         'comment': 'Lovely sauce, not too sweet. Made with fresh ingredients and good quality pasta. ',
         'ratings': 5,
         'photo': None},
        {'reviewID': 'A tad expensive',
         'user_id':1,
         'comment': 'Good pasta however a bit more expensive than standard. The portion was also too small for me.',
         'ratings': 3,
         'photo': "population_photos/bad_spaghetti.jpg"}
    ]
    # Chicken Burger Reviews
    chickenBurger_reviews = [
        {'reviewID': 'HORRIBLE, never again.',
         'user_id':2,
         'comment': 'I usually enjoy most things I get from this place, however their chicken burger is absolutely horrendous. Mine came undercooked and still very pink inside. Burger was dry and I think I saw mould, gross! NEVER ORDER THIS!!!',
         'ratings': 0,
         'photo': None},
        {'reviewID': 'Decent but not amazing',
         'user_id':1,
         'comment': "I've had better burgers, it won't hurt to eat but wouldn't have it again.",
         'ratings': 3,
         'photo': None},
         {'reviewID': 'Uncooked and mouldy!',
          'user_id':3,
         'comment': "Gross gross gross! My burger if I can even call it that came frozen (how?> even I don't know) and the bread had green stuff on it! Never get this.",
         'ratings': 1,
         'photo': None}
    ]
    # Sweet Potato Fries Reviews
    spFries_reviews = [{'reviewID': 'Unique side',
         'user_id':2,
         'comment': "They have an interesting texture, definitely not as crispy as normal potato fries but tastes very very good. I'd reccomend to try if you're up for something different.",
         'ratings': 4,
         'photo': None}
         ]
    hotChocolate_reviews = [
        {'reviewID': 'Yummy drink',
         'user_id':1,
         'comment': "Hands down one of if not THE BEST hot chocolate in the city! Bonus points for being vegan too. And the marshmallow were soooooooo good. Definitely order this if you're ever here!",
         'ratings': 5,
         'photo': "population_photos/good_hot_chocolate.jpg"}]
    # Orange Juice Reviews
    oj_reviews = [
        {'reviewID': 'Fresh juice',
        'user_id':3,
         'comment': "Sweet and tangy orange juice, bonus that you can see into the open kitchen where they squeeze out the oranges!",
         'ratings': 5,
         'photo': None}]
    # Apple Juice Reviews
    appleJuice_reviews = [
        {'reviewID': 'Luke warm but still delicious',
        'user_id':2,
         'comment': "Perfectly sweet and the apple bits were very crunchy and fresh. However, my one complaint is that it was a bit warm so could do with more time in the fridge.",
         'ratings': 4,
         'photo': None}]

    # Main Menu
    mainMenu_menuItems = [
        {'menuItemID': 'Spaghetti',
         'description': 'Drumwheat pasta with ragu sauce and parmesan cheese.',
         'price': 10.99,
         'photo': 'population_photos/spaghetti.jpg',
         'reviews': spaghetti_reviews},
        {'menuItemID': 'Chicken Burger',
         'description': 'Chicken burger pate with tomatoes, lettuce and ketchup in a brioche bun.',
         'price':7.49,
         'photo': 'population_photos/chicken_burger.jpeg',
         'reviews': chickenBurger_reviews},
        {'menuItemID': 'Sweet Potato Fries',
         'description': 'Deep-fried thin sweet potato slices with cajun seasoning.',
         'price':5,
         'photo': 'population_photos/sweet-potato-fries.jpeg',
         'reviews': spFries_reviews}]


    # Drinks Menu
    drinks_menuItems = [
        {'menuItemID': 'Orange Juice',
         'description': 'Freshly squeezed orange juice.',
         'price': 2.49,
         'photo': 'population_photos/orange_juice.jpg',
         'reviews': oj_reviews},
        {'menuItemID': 'Hot Chocolate',
         'description': 'Made with oat milk, topped with marshmallows and cream.',
         'price': 2.99,
         'photo': 'population_photos/hot-chocolate.jpeg',
         'reviews': hotChocolate_reviews},
         {'menuItemID': 'Apple Juice',
         'description': 'Bottled apple juice, with chunks of fresh apple.',
         'price': 1.99,
         'photo':'population_photos/juice_apple.jpg',
         'reviews': appleJuice_reviews}]


    # note: add more menus on this area when required
    # dictionary of dictionaries of all menus
    menus = {'Main Menu': {'menuItems': mainMenu_menuItems},
            'Drinks Menu': {'menuItems': drinks_menuItems}}
    
    users = [
        {'username':'burgerFanatic', 'password' : 'abcdefg17'},
        {'username':'foodLover23', 'password' : 'abcdefg23'},
        {'username':'deeeserts<3', 'password' : 'abcdefg33'}]

    for user in users:
        add_user(user['username'],user['password'])

    for menuID, menu_data in menus.items():
        m = add_menu(menuID)
        for menuItem in menu_data['menuItems']:
            mI = add_menuItem(m, menuItemID = menuItem['menuItemID'], description=menuItem['description'], price=menuItem['price'], photoPath=menuItem['photo'])
            for review in menuItem['reviews']:
                add_review(mI, reviewID = review['reviewID'], user_id = review['user_id'], comment = review['comment'], ratings = review['ratings'], photoPath = review['photo'])


    for m in Menu.objects.all():
        for mI in MenuItem.objects.filter(menu=m):
            print(f'- {m}: {mI}')

os.path.dirname(os.path.abspath(__file__))

# functions used above to add menus, menu items and reviews
def add_user(username,password):
    user = User.objects.get_or_create(username = username, password = password)
    return user

def add_review(menuItem, user_id, reviewID, comment, ratings, photoPath):
    review = Review.objects.get_or_create(menuItem=menuItem, user_id=user_id, reviewID=reviewID)[0]
    review.comment = comment
    review.ratings = ratings
    if photoPath!=None:
        with open(photoPath, 'rb') as photo:
            photo = File(photo)
            nameParts = os.path.split(photoPath)
            review.photo.save(photoPath[1], photo, save=True)
    else:
        review.photo = photoPath
    review.save()
    return review

def add_menuItem(menu, menuItemID, description, price, photoPath):
    mI = MenuItem.objects.get_or_create(menu=menu, menuItemID=menuItemID)[0]
    mI.description=description
    mI.price = price
    if photoPath!=None:
        with open(photoPath, 'rb') as photo:
            photo = File(photo)
            nameParts = os.path.split(photoPath)
            mI.photo.save(photoPath[1], photo, save=True)
    else:
        mI.photo = photoPath
    mI.save()
    return mI

def add_menu(menuID):
    m = Menu.objects.get_or_create(menuID=menuID)[0]
    m.save()
    return m

# note: this is where code execution begins
if __name__ == '__main__':
    print('Starting Restaurant population script...')
    populate()