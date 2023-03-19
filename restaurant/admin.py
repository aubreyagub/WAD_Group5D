from django.contrib import admin

# Register your models here.
from restaurant.models import UserProfile, MenuItem, Menu

class MenuItemAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('menuItemID',)}

class MenuAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('menuID',)}

admin.site.register(MenuItem, MenuItemAdmin)
admin.site.register(Menu, MenuAdmin)