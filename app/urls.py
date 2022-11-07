from django.urls import path, include

from django.contrib import admin
from . import views
urlpatterns = [
    path('signup/', views.signup ),
    path('home/', views.home),
    path('signin/', views.signin),
    path('signout/', views.signout),
    path('articlelist/', views.article_list),
    path('upload/', views.upload),
    path('detail/<int:id>', views.detail),
    path('mypage/', views.mypage),
    path('makecategory/', views.makecategory),
    path('category_list/', views.category_list),
    path('remove_category/', views.remove_category),
    path('call_category/', views.call_category),
    path('modify_article/', views.modify_article),
    path('remove_article/', views.remove_article),

]