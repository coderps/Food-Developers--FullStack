from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from django.db.models import CharField
from django.db import models
import datetime
# Create your models here.

class Blogs(models.Model):
	bid = models.AutoField(primary_key=True)
	btitle = models.CharField(max_length=100)
	bdesc = models.CharField(max_length=15000)
	created_at = models.DateTimeField(auto_now_add=True)
	username = models.ForeignKey(User, on_delete=models.CASCADE) 

	def __str__(self):
		return self.btitle

class Cuisines(models.Model):
	cid = models.AutoField(primary_key=True)
	cname = models.CharField(max_length=50)
	remarks = models.CharField(max_length=500)

	def __str__(self):
		return self.cname

class Recipes(models.Model):
	recipe_id = models.AutoField(primary_key=True)
	rname = models.CharField(max_length=50)
	ind = models.CharField(max_length=5000, default='NA')
	rdesc = models.CharField(max_length=15000)
	cid = models.ForeignKey(Cuisines, on_delete=models.CASCADE)
	username = models.ForeignKey(User, on_delete=models.CASCADE)

	def __str__(self):
		return self.rname

class Restaurants(models.Model):
	rid = models.AutoField(primary_key=True)
	rname = models.CharField(max_length=100)
	rlocation = models.CharField(max_length=100)
	area = models.CharField(max_length=150)
	cid = models.ForeignKey(Cuisines, on_delete=models.CASCADE)

	def __str__(self):
		return self.rname

class Comments(models.Model):
	comment_id = models.AutoField(primary_key=True)
	cdesc = models.CharField(max_length=500)
	bid = models.ForeignKey(Blogs, on_delete=models.CASCADE)
	recipe_id = models.ForeignKey(Recipes, on_delete=models.CASCADE)

	def __str__(self):
		return self.comment_id

class LikedPosts(models.Model):
	lid = models.AutoField(primary_key=True)
	type_of_post = models.CharField(max_length=500)
	bid = models.ForeignKey(Blogs, on_delete=models.CASCADE)
	recipe_id = models.ForeignKey(Recipes, on_delete=models.CASCADE)
	username = models.ForeignKey(User, on_delete=models.CASCADE)

	def __str__(self):
		return self.lid