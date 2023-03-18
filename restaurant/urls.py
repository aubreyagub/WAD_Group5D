from django.urls import path
from restaurant import views
app_name = 'restaurant'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name = 'about'),
    # path('category/<slug:category_name_slug>/',
    #      views.show_category, name='show_category'),
    # path('add_category/', views.add_category, name='add_category'),
    # path('category/<slug:category_name_slug>/add_page/', views.add_page, name='add_page'),

    # Add menu Item does not work because of missing menu_name_slug
    path('add_menuItem/', views.add_menu_item, name="add_menuItem"),
    # Works but it's empty at the moment
    path('menu/', views.show_menu, name='show_menu'),
    #Template shows form but without any functionality
    path('add_menu/', views.add_menu, name="add_menu"),
    
    path('restricted/', views.restricted, name='restricted'),
]
