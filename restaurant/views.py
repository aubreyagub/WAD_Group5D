from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from datetime import datetime
from restaurant.models import Menu, MenuItem, Review
from restaurant.forms import MenuForm, MenuItemForm, ReviewForm

def index(request):
    context_dict = {}
    context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'

    visitor_cookie_handler(request)
    response = render(request, 'restaurant/index.html', context=context_dict)
    return response

def about(request):
    context_dict = {'boldmessage': 'This tutorial has been put together by Anastasiia'}
    visitor_cookie_handler(request)
    context_dict['visits'] = request.session['visits']
    return render(request, 'restaurant/about.html', context=context_dict)


@login_required
def restricted(request):
     return render(request, 'restaurant/restricted.html')

def visitor_cookie_handler(request, response):
    visits = int(request.COOKIES.get('visits', '1'))
    last_visit_cookie = request.COOKIES.get('last_visit', str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7], '%Y-%m-%d %H:%M:%S')

    if (datetime.now() - last_visit_time).days > 0:
        visits = visits + 1
        response.set_cookie('last_visit', str(datetime.now()))
    else:
        response.set_cookie('last_visit', last_visit_cookie)
    response.set_cookie('visits', visits)

def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val

def visitor_cookie_handler(request):
    visits = int(get_server_side_cookie(request, 'visits', '1'))
    last_visit_cookie = get_server_side_cookie(request,
                                               'last_visit',
                                               str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7],
'%Y-%m-%d %H:%M:%S')
    if (datetime.now() - last_visit_time).days > 0:
        visits = visits + 1
        request.session['last_visit'] = str(datetime.now())
    else:
        request.session['last_visit'] = last_visit_cookie

    request.session['visits'] = visits

@login_required
def add_menu(request):
    form = MenuForm()
    if request.method == 'POST':
        form = MenuForm(request.POST)
        if form.is_valid():
            cat = form.save(commit=True)
            print(cat, cat.slug)
            return redirect('/rango/')
        else:
            print(form.errors)
    return render(request, 'rango/add_menu.html', {'form': form})

def get_menu(request, menu_name_slug):
    context_dict = {}
    
    try:
        menu = menu.objects.get(slug=menu_name_slug)
        menuItems = MenuItem.objects.filter(menu=menu)
        context_dict['menuItems'] = menuItems
    except Menu.DoesNotExist:
        context_dict['menuItems'] = None

    return render(request, 'restaurant.html', context=context_dict)

def get_menu_item(request, menu_name_slug):
    context_dict = {}
    
    try:
        menuItem = menuItem.objects.get(slug=menu_name_slug)
        reviews = MenuItem.objects.filter(menu=menu)
        context_dict['menuItems'] = menuItems
    except Menu.DoesNotExist:
        context_dict['menuItems'] = None

    return render(request, 'restaurant.html', context=context_dict)

