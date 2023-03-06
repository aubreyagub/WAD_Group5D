from django.urls import path
from restaurant import views
app_name = 'rango'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name = 'about'),
    path('category/<slug:category_name_slug>/',
         views.show_category, name='show_category'),
    path('add_category/', views.add_category, name='add_category'),
    path('category/<slug:category_name_slug>/add_page/', views.add_page, name='add_page'), 
    path('menu/', views.show_menu, name='menu'), # page to show full menu
    path('menuitem/<slug:menu_item_name_slug>/', views.show_menu_item, name='menu_item'), # page to show a menu item along with its comments
    path('add_menu_item/', views.add_menu_item, name='add_menu_item'), # page to add a menu item
    path('menuitem/<slug:menu_item_name_slug>/<slug:comment_name_slug>', views.add_comment, name='add_comment'), # page to add a comment for a menu item
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('restricted/', views.restricted, name='restricted'),
    path('logout/', views.user_logout, name='logout'),
]
