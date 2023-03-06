from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

class Category(models.Model):
    NAME_MAX_LENGTH = 128

    name = models.CharField(max_length=NAME_MAX_LENGTH, unique=True)
    views = models.IntegerField(default =0)
    likes = models.IntegerField(default = 0)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwards):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwards)
    class Meta:
        verbose_name_plural = 'Categories'
    def __str__(self):
        return self.name
    
class Page(models.Model):
    TITLE_MAX_LENGTH = 128
    URL_MAX_LENGTH = 200

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=TITLE_MAX_LENGTH)
    url = models.URLField()
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.title
    
class MenuItem(models.Model):
    TITLE_MAX_LENGTH=128
    DESCRIPTION_MAX_LENGTH=200

    name = models.CharField(max_length=TITLE_MAX_LENGTH, unique=True)
    description = models.CharField(max_length=DESCRIPTION_MAX_LENGTH, default="None")
    picture = models.ImageField(upload_to='profile_images', blank=True)
    ratings = models.IntegerField(default =0)
    comments = models.IntegerField(default =0)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwards):
        self.slug = slugify(self.name)
        super(MenuItem, self).save(*args, **kwards)
    class Meta:
        verbose_name_plural = 'MenuItems'
    def __str__(self):
        return self.name

    
class Comment(models.Model):
    TITLE_MAX_LENGTH=128
    COMMENT_MAX_LENGTH=1000

    comment = models.ForeignKey(MenuItem, on_delete = models.CASCADE)
    title =  models.CharField(max_length=TITLE_MAX_LENGTH, unique=True)
    comment = models.CharField(max_length=COMMENT_MAX_LENGTH)
    picture = models.ImageField(upload_to='comment_images', blank=True)

    def __str__(self):
        return self.title

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    def __str__(self):
        return self.user.username

