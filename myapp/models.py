from django.db import models
from django.contrib.auth.models import User



class Comment(models.Model):
  author = models.ForeignKey(User, on_delete=models.CASCADE)
  post = models.ForeignKey('Post', on_delete=models.CASCADE)
  comment = models.TextField(max_length=200)
  updated = models.DateTimeField(auto_now=True)
  
  class Meta:
    ordering=['-updated']
  
  def __str__(self) -> str:
    return self.comment
  




class Post(models.Model):
  title = models.CharField(max_length=50)
  body = models.TextField()
  author = models.ForeignKey(User, on_delete=models.CASCADE)
  created = models.DateTimeField(auto_now_add=True)
  updated = models.DateTimeField(auto_now=True)
  
  class Meta:
    ordering=['-created']
  
  def __str__(self) -> str:
    return self.title

