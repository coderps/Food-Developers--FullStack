from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, HttpResponseRedirect, render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from mysite.models import Blogs,Cuisines,Recipes,Restaurants,Comments,LikedPosts
from random import randint
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . serializers import cuisinesSerializer, userSerializer, restSerializer, blogSerializer, recipeSerializer, commentSerializer, likedpostSerializer
from rest_framework import generics
import os, string

def index(request):
    return render(request,'index.html')

def log_in(request):
    return render(request,'log_in.html')

def signup(request):
	return render(request,'signup.html')

def log_out(request):
	logout(request)
	return redirect('/')

def rfinder(request):
    return render(request,'rfinder.html')

def signingup(request):
	username = request.POST.get("username")
	firstname = request.POST.get("fname")
	lastname = request.POST.get("lname")
	mail = request.POST.get("mail")
	pwd = request.POST.get("pwd")
	user = User.objects.create_user(username,mail,pwd)
	user.first_name = firstname
	user.last_name = lastname
	user.save()
	user1 = authenticate(username=username, password=pwd)
	if user1 is not None:
		return render(request,'welcome.html',{'username':username},content_type=RequestContext(request))
	else:
		return render(request,'fail.html',{},content_type=RequestContext(request))

#Blogs
@csrf_exempt
def write_a_blog(request):
	if request.method=='POST':
		username = request.user
		btitle = request.POST.get("btitle")
		bdesc = request.POST.get("bdesc")
		blog = Blogs(username=username, btitle=btitle, bdesc=bdesc)
		blog.save()
	return redirect('/blogs/')

@csrf_exempt
def blogs(request):
	if request.user.is_authenticated:
		username = request.user
		ublogs = Blogs.objects.filter(username=username)
		all_blogs = Blogs.objects.all()
		return render(request, 'blog.html', {'username':username, 'ublogs':ublogs, 'all_blogs':all_blogs}, content_type=RequestContext(request))
	return redirect('/log_in')

#Recipes
@csrf_exempt
def write_a_recipe(request):
	if request.method=='POST':
		username = request.user
		rname = request.POST.get("rname")
		ind = request.POST.get("ind")
		rdesc = request.POST.get("rdesc")
		cuisine = request.POST.get("cname")
		ccid = cuisine.split()[0][:-1]
		cid = Cuisines.objects.get(cid=ccid)
		recipe = Recipes(username=username, rname=rname, ind=ind, rdesc=rdesc, cid=cid)
		recipe.save()
	return redirect('/recipes/')

@csrf_exempt
def recipes(request):
	if request.user.is_authenticated:
		username = request.user
		urecipes = Recipes.objects.filter(username=username)
		all_recipes = Recipes.objects.all()
		all_cuisines = Cuisines.objects.all().order_by('cname')
		return render(request, 'recipe.html', {'username':username, 'ublogs':urecipes, 'all_blogs':all_recipes, 'all_cuisines':all_cuisines}, content_type=RequestContext(request))
	return redirect('/log_in')

#Login/Landing
@csrf_exempt
def my_view(request):
	if request.method=='POST':
		username = request.POST.get("username")
		password = request.POST.get("password")
		user = authenticate(username=username, password=password)
		if user is not None:
			login(request, user)
		else:
			return render(request,'fail.html',{},content_type=RequestContext(request))
	username=request.user.username
	print(username)
	return render(request,'welcome.html',{'username':username},content_type=RequestContext(request))

def rfinder_results(request):
	zipcode = 0
	if request.method=='POST':
		zipcode = request.POST.get("postalcode")
	if zipcode:
		restaurants = Restaurants.objects.all()
		num_of_restaurants = len(restaurants)
		result = []
		for i in range(0, num_of_restaurants):
			if str(zipcode) in str(restaurants[i].area):
				result.append(restaurants[i])
	print(zipcode)
	return render(request,'result.html',{'result':result},content_type=RequestContext(request))

#Cuisine Details
class cuisineList(APIView):
    def get(self, request, format=None):
        snippets = Cuisines.objects.all()
        serializer = cuisinesSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = cuisinesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class cuisineDetail(APIView):
	def get_object(self, pk):
		try:
			return Cuisines.objects.get(pk=pk)
		except Cuisines.DoesNotExist:
			raise Http404 

	def get(self, request, pk, format=None):
		snippet = self.get_object(pk)
		serializer = cuisinesSerializer(snippet)
		return Response(serializer.data)

	def put(self, request, format=None):
		snippet = self.get_object(pk)
		serializer = cuisinesSerializer(snippet, data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def delete(self, request, pk, format=None):
		snippet = self.get_object(pk)
		snippet.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)

#Restaurant Details
class restList(APIView):
    def get(self, request, format=None):
        snippets = Restaurants.objects.all()
        serializer = restSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = restSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class restDetail(APIView):
	def get_object(self, pk):
		try:
			return Restaurants.objects.get(pk=pk)
		except Restaurants.DoesNotExist:
			raise Http404 

	def get(self, request, pk, format=None):
		snippet = self.get_object(pk)
		serializer = restSerializer(snippet)
		return Response(serializer.data)

	def put(self, request, format=None):
		snippet = self.get_object(pk)
		serializer = restSerializer(snippet, data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def delete(self, request, pk, format=None):
		snippet = self.get_object(pk)
		snippet.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)

#User Details
class userList(APIView):
    def get(self, request, format=None):
        snippets = User.objects.all()
        serializer = userSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = userSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class userDetail(APIView):
	def get_object(self, pk):
		try:
			return User.objects.get(pk=pk)
		except User.DoesNotExist:
			raise Http404 

	def get(self, request, pk, format=None):
		snippet = self.get_object(pk)
		serializer = userSerializer(snippet)
		return Response(serializer.data)

	def put(self, request, format=None):
		snippet = self.get_object(pk)
		serializer = userSerializer(snippet, data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def delete(self, request, pk, format=None):
		snippet = self.get_object(pk)
		snippet.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)

#Blog Details
class blogList(APIView):
    def get(self, request, format=None):
        snippets = Blogs.objects.all()
        serializer = blogSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = blogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class blogDetail(APIView):
	def get_object(self, pk):
		try:
			return Blogs.objects.get(pk=pk)
		except Blogs.DoesNotExist:
			raise Http404 

	def get(self, request, pk, format=None):
		snippet = self.get_object(pk)
		serializer = blogSerializer(snippet)
		return Response(serializer.data)

	def put(self, request, format=None):
		snippet = self.get_object(pk)
		serializer = blogSerializer(snippet, data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def delete(self, request, pk, format=None):
		snippet = self.get_object(pk)
		snippet.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)

#Recipe Details
class recipeList(APIView):
    def get(self, request, format=None):
        snippets = Recipes.objects.all()
        serializer = recipeSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = recipeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class recipeDetail(APIView):
	def get_object(self, pk):
		try:
			return Recipes.objects.get(pk=pk)
		except Recipes.DoesNotExist:
			raise Http404 

	def get(self, request, pk, format=None):
		snippet = self.get_object(pk)
		serializer = recipeSerializer(snippet)
		return Response(serializer.data)

	def put(self, request, format=None):
		snippet = self.get_object(pk)
		serializer = recipeSerializer(snippet, data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def delete(self, request, pk, format=None):
		snippet = self.get_object(pk)
		snippet.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)

#Comment Details
class commentList(APIView):
    def get(self, request, format=None):
        snippets = Comments.objects.all()
        serializer = commentSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = commentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class commentDetail(APIView):
	def get_object(self, pk):
		try:
			return Comments.objects.get(pk=pk)
		except Comments.DoesNotExist:
			raise Http404 

	def get(self, request, pk, format=None):
		snippet = self.get_object(pk)
		serializer = commentSerializer(snippet)
		return Response(serializer.data)

	def put(self, request, format=None):
		snippet = self.get_object(pk)
		serializer = commentSerializer(snippet, data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def delete(self, request, pk, format=None):
		snippet = self.get_object(pk)
		snippet.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)

#LikedPost Details
class likedpostList(APIView):
    def get(self, request, format=None):
        snippets = LikedPosts.objects.all()
        serializer = likedpostSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = likedpostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class likedpostDetail(APIView):
	def get_object(self, pk):
		try:
			return LikedPosts.objects.get(pk=pk)
		except LikedPosts.DoesNotExist:
			raise Http404 

	def get(self, request, pk, format=None):
		snippet = self.get_object(pk)
		serializer = likedpostSerializer(snippet)
		return Response(serializer.data)

	def put(self, request, format=None):
		snippet = self.get_object(pk)
		serializer = likedpostSerializer(snippet, data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def delete(self, request, pk, format=None):
		snippet = self.get_object(pk)
		snippet.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)