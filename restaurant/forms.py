from django import forms
from restaurant.models import Page, Category
from restaurant.models import Restaurant, Review, Menu, MenuItem
from django.contrib.auth.models import User
from restaurant.models import UserProfile

class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=Category.NAME_MAX_LENGTH, help_text="Please enter the category name.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Category
        fields = ('name',)

class PageForm(forms.ModelForm):
     title = forms.CharField(max_length=Page.TITLE_MAX_LENGTH, help_text="Please enter the title of the page.")
     url = forms.URLField(max_length=200, help_text="Please enter the URL of the page.")
     views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

     class Meta:
         model = Page
         exclude = ('category',)

     def clean(self):
         cleaned_data = self.cleaned_data
         url = cleaned_data.get('url')

         if url and not url.startswith('http://'):
             url = f'http://{url}'
             cleaned_data['url'] = url

         return cleaned_data

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username', 'email', 'password',)
        
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('website', 'picture',)

class RestaurantForm(forms.ModelForm):
    restaurantID = forms.CharField(max_length=Restaurant.RESTAURANT_ID_MAX_LENGTH, help_text="Restaurant name:")
    location = forms.CharField(max_length=Restaurant.RESTAURANT_LOCATION_MAX_LENGTH, help_text="Location:")
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)
    class Meta:
        model = Restaurant
        fields = ('restaurantID', 'location', 'photo',)

class MenuForm(forms.ModelForm):
    menuID = forms.CharField(max_length=Menu.MENU_ID_MAX_LENGTH, help_text="Menu name:")
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)
    class Meta:
        model = Menu
        fields = ('menuID',)
    def clean(self):
         cleaned_data = self.cleaned_data
         url = cleaned_data.get('url')
         if url and not url.startswith('http://'):
             url = f'http://{url}'
             cleaned_data['url'] = url
         return cleaned_data
    
class MenuItemForm(forms.ModelForm):
    menuItemID = forms.CharField(max_length=MenuItem.MENUITEM_ID_MAX_LENGTH, help_text="Menu item name:")
    description = forms.CharField(max_length=MenuItem.DESCRIPTION_MAX_LENGTH, help_text="Describe this menu item:")
    price = forms.FloatField(initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)
    class Meta:
        model = MenuItem
        fields = ('menuItemID', 'description', 'price', 'photo',)
    def clean(self):
         cleaned_data = self.cleaned_data
         url = cleaned_data.get('url')
         if url and not url.startswith('http://'):
             url = f'http://{url}'
             cleaned_data['url'] = url
         return cleaned_data
    
class ReviewForm(forms.ModelForm):
    title = forms.CharField(max_length=Review.REVIEW_ID_MAX_LENGTH, help_text="Comment title:")
    comment = forms.CharField(max_length=Review.COMMENT_MAX_LENGTH, help_text="What did you think about this menu item?")
    rating = forms.IntegerField(initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)
    class Meta:
        model = Review 
        fields = ('title', 'comment', 'rating', 'photo',)
    def clean(self):
         cleaned_data = self.cleaned_data
         url = cleaned_data.get('url')
         if url and not url.startswith('http://'):
             url = f'http://{url}'
             cleaned_data['url'] = url
         return cleaned_data
