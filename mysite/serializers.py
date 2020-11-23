from rest_framework import serializers
from django.contrib.auth.models import User
from mysite.models import Blogs,Cuisines,Recipes,Restaurants,Comments,LikedPosts

class userSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = '__all__'

class cuisinesSerializer(serializers.ModelSerializer):
	class Meta:
		model = Cuisines
		fields = '__all__'

class restSerializer(serializers.ModelSerializer):
	class Meta:
		model = Restaurants
		fields = '__all__'

class blogSerializer(serializers.ModelSerializer):
	class Meta:
		model = Blogs
		fields = '__all__'

class recipeSerializer(serializers.ModelSerializer):
	class Meta:
		model = Recipes
		fields = '__all__'

class commentSerializer(serializers.ModelSerializer):
	class Meta:
		model = Comments
		fields = '__all__'

class likedpostSerializer(serializers.ModelSerializer):
	class Meta:
		model = LikedPosts
		fields = '__all__'