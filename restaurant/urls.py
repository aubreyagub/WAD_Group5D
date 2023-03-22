from django.urls import path
from restaurant import views
app_name = 'restaurant'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name = 'about'),
    path('menu/<slug:menu_name_slug>//add_menuItem/', views.add_menu_item, name='add_menu_item'),
    path('menu/<slug:menu_name_slug>/', views.show_menu, name='show_menu'),
    path('menu/<slug:menu_name_slug>/<slug:menuItem_name_slug>/', views.show_menu_item, name='show_menu_item'),
    #Template shows form but without any functionality
    path('add_menu/', views.add_menu, name="add_menu"),
    path('menu/<slug:menu_name_slug>/<slug:menuItem_name_slug>/add_review/', views.add_review, name="add_review"),
    path('restricted/', views.restricted, name='restricted'),
]
