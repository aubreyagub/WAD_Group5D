from django import forms
from restaurant.models import Page, Category, Comment, MenuItem
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
     
class MenuItemForm(forms.ModelForm):
    title = forms.CharField(max_length=MenuItem.TITLE_MAX_LENGTH, help_text="Menu item name:")
    description = forms.CharField(max_length=MenuItem.DESCRIPTION_MAX_LENGTH, help_text="Menu item description:")
    ratings = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    comments = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Comment
        fields = ('title', 'description', 'picture',)

class CommentForm(forms.ModelForm):
    title = forms.CharField(max_length=Comment.TITLE_MAX_LENGTH, help_text="Comment title:")
    comment = forms.CharField(max_length=Comment.COMMENT_MAX_LENGTH, help_text="Write comment:")
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Comment
        fields = ('title', 'comment','picture',)

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username', 'email', 'password',)

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('website', 'picture',)
