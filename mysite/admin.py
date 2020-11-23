from mysite.models import Blogs,Cuisines,Recipes,Restaurants,Comments,LikedPosts
from django.contrib import admin

# Register your models here.

admin.site.register(Blogs)
admin.site.register(Cuisines)
admin.site.register(Recipes)
admin.site.register(Restaurants)
admin.site.register(Comments)
admin.site.register(LikedPosts)