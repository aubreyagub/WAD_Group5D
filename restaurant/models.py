from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    def __str__(self):
        return self.user.username
    
class Menu(models.Model):
    MENU_ID_MAX_LENGTH=128
    menuID = models.TextField(max_length=MENU_ID_MAX_LENGTH,unique=True) # primary key
    slug = models.SlugField(unique=True)
    def save(self, *args, **kwards):
        self.slug = slugify(self.menuID)
        super(Menu, self).save(*args, **kwards)
    def __str__(self):
        return self.menuID
    
class MenuItem(models.Model):
    MENUITEM_ID_MAX_LENGTH=128
    DESCRIPTION_MAX_LENGTH=200
    menuItemID = models.CharField(max_length=MENUITEM_ID_MAX_LENGTH, unique=True) # primary key 
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE) # foreign key: one to many - many menu items for one menu
    description = models.CharField(max_length=DESCRIPTION_MAX_LENGTH, default="None")
    price = models.FloatField(default =0.0)
    photo = models.ImageField(upload_to='menu_item_images', blank=True)
    slug = models.SlugField(unique=True)
    def save(self, *args, **kwards):
        self.slug = slugify(self.menuItemID)
        super(MenuItem, self).save(*args, **kwards)
    class Meta:
        verbose_name_plural = 'MenuItems'
    def __str__(self):
        return self.menuItemID
    
class Review(models.Model):
    REVIEW_ID_MAX_LENGTH=128
    COMMENT_MAX_LENGTH=1000
    reviewID =  models.CharField(max_length=REVIEW_ID_MAX_LENGTH, unique=True) # primary key 
    user = models.ForeignKey(User, on_delete=models.CASCADE) # foreign key: one to many - many reviews for one user 
    menuItem = models.ForeignKey(MenuItem, on_delete=models.CASCADE) # foreign key: one to many - many reviews for one menu item
    comment = models.CharField(max_length=COMMENT_MAX_LENGTH)
    ratings = models.IntegerField(default =0)
    photo = models.ImageField(upload_to='review_images', blank=True)
    def __str__(self):
        return self.reviewID
    