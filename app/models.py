from tkinter import CASCADE
from unicodedata import category
from unittest.util import _MAX_LENGTH
from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length = 100)
    email = models.TextField()
    pwd = models.CharField(max_length = 100)
    phone_number = models.CharField(max_length=100)
class Category(models.Model):
    name = models.CharField(max_length = 100)
class Article(models.Model):
    title = models.CharField(max_length = 100)
    contents = models.TextField()
    time = models.CharField(max_length= 100)
    user =models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

class FileAttach(models.Model):
    o_file_name=models.CharField(max_length = 1000)
    s_file_name=models.CharField(max_length = 1000)
    file_size = models.CharField(max_length = 100, default = 0)
    article = models.ForeignKey(Article, on_delete = models.CASCADE)

