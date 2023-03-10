from django import forms
from restaurant.models import Review, Menu, MenuItem
from django.contrib.auth.models import User
from restaurant.models import UserProfile

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username', 'email', 'password',)
        
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('website', 'picture',)

### REMOVE IF NOT MULTIPLE RESTAURANTS
# class RestaurantForm(forms.ModelForm):
#     restaurantID = forms.CharField(max_length=Restaurant.RESTAURANT_ID_MAX_LENGTH, help_text="Restaurant name:")
#     location = forms.CharField(max_length=Restaurant.RESTAURANT_LOCATION_MAX_LENGTH, help_text="Location:")
#     slug = forms.CharField(widget=forms.HiddenInput(), required=False)
#     class Meta:
#         model = Restaurant
#         fields = ('restaurantID', 'location', 'photo',)

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
