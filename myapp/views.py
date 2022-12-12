from django.shortcuts import render,redirect
from myapp.forms import *
from django.http import HttpResponse
from myapp.models import *
from django.contrib.auth import authenticate,login,logout
# Create your views here.


def home(request):
  post = Post.objects.all()
  context = {'title':'Blog-Site', 'post':post}
  return render(request, 'myapp/index.html',context)



    
    



def about(request):
  context = {'title':'About-Page'}
  return render(request, 'myapp/about.html',context)


# Auth

def loginUser(request):
  if request.user.is_authenticated:
    return redirect('home')
  context ={}
  if request.method == 'POST':
      username = request.POST.get('username')
      password = request.POST.get('password')
      user = authenticate(request, username = username, password = password)
      
      if user is not None:
        login(request,user)
        return redirect('home')
      else:
        context = {'message':'username or password incorrect'}
      
  return render(request,'myapp/login.html',context)


def logoutUser(request):
  logout(request)
  return redirect('home')


def registerUser(request):
  if request.user.is_authenticated:
    return redirect('home')
  
  context = {}
  if request.method == 'POST':
     username = request.POST.get('username')
     email = request.POST.get('email')
     password = request.POST.get('password')
     password1 = request.POST.get('password1')
     
     if password == password1:
       user = User.objects.create_user(username=username,email=email,password=password)
       login(request,user)
       return redirect('login')
     
     
    
  return render(request,'myapp/signup.html',context)






# POST CRUD
def getPost(request,pk):
  post = Post.objects.get(id=pk)
  context = {'title':'View-Post','post':post}
  return render(request, 'myapp/getpost.html',context)

  
  

def postDelete(request,pk):
  post = Post.objects.get(id=pk)
  post.delete()
  return redirect('home')



def createPost(request):
    context = {}
    if request.method == "POST":
        try:
            Post.objects.create(
                title = request.POST.get("title"),
                body = request.POST.get("description"),
                author = request.user
            )
            return redirect("home")
        except:
            context["message"] = "*Invalid details"
    return render(request, "myapp/new_post.html", context)
  
  
def updatePost(request,pk):
  post = Post.objects.get(id=pk)
  if request.method == "POST":
    post.title = request.POST.get("title")
    post.body = request.POST.get("description") 
    post.save()
    return redirect('home') 
    
  context={'post':post}
  return render(request,'myapp/update_post.html',context)