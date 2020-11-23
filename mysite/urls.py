"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^signup/signingup', views.signingup, name='signingup'),
    url(r'^log_in/$', views.log_in, name='log_in'),
    url(r'^log_in/my_view/$', views.my_view, name='my_view'),
    url(r'^log_in/my_view/log_out$', views.log_out, name='log_out'),
    url(r'^rfinder/$', views.rfinder, name='rfinder'),
    url(r'^rfinder/my_view/$', views.rfinder_results, name='rfinder_results'),
    url(r'^blogs/$', views.blogs, name='blogs'),
    url(r'^blogs/write_a_blog/$', views.write_a_blog, name='write_a_blog'),
    url(r'^recipes/$', views.recipes, name='recipes'),
    url(r'^recipes/write_a_recipe/$', views.write_a_recipe, name='write_a_recipe'),
    path('cuisines/', views.cuisineList.as_view()),
    path('cuisines/<int:pk>/', views.cuisineDetail.as_view()),
    path('restaurants/', views.restList.as_view()),
    path('restaurants/<int:pk>/', views.restDetail.as_view()),
    path('restaurants/', views.restList.as_view()),
    path('restaurants/<int:pk>/', views.restDetail.as_view()),
    path('users/', views.userList.as_view()),
    path('users/<int:pk>/', views.userDetail.as_view()),
    #path('openblogs/', views.openblogs),
    #path('openblogs/<int:pk>/', views.openblogs),
    #path('recipes/', views.recipeList.as_view()),
    #path('recipes/<int:pk>/', views.recipeDetail.as_view()),
    path('comments/', views.commentList.as_view()),
    path('comments/<int:pk>/', views.commentDetail.as_view()),
    path('likedposts/', views.likedpostList.as_view()),
    path('likedposts/<int:pk>/', views.likedpostDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)