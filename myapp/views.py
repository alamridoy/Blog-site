from django.shortcuts import render,redirect
from myapp.forms import *
from django.http import HttpResponse
from myapp.models import *
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
# Create your views here.


def postSearch(request):
  post_search = ""
  if request.GET.get("search"):
    post_search = request.GET.get('search')
  posts = Post.objects.filter(Q(title__icontains=post_search) | Q(body__icontains=post_search))
  return posts
 
def home(request):
  posts = postSearch(request)
  context = {'title':'Blog-Site', 'post':posts}
  return render(request, 'myapp/index.html',context)

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

@login_required(login_url='login')
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
  if request.method == 'POST':
    comment = request.POST.get('comment')
    Comment.objects.create(
      post = post,
      author = request.user,
      comment = comment
    )
  context = {'title':'View-Post','post':post}
  return render(request, 'myapp/getpost.html',context)

  
  
@login_required(login_url='login')
def postDelete(request,pk):
  
  # if request.user.is_authenticated:
  post = Post.objects.get(id=pk)
  if request.user == post.author:
   post.delete()
  else:
    return HttpResponse("<h3>Please try to own your post not else!</h3>")
  
  
  return redirect('home')


@login_required(login_url='login')
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
  
@login_required(login_url='login')
def updatePost(request,pk):
  post = Post.objects.get(id=pk)
  if request.user == post.author:
     if request.method == "POST":
   
      post.title = request.POST.get("title")
      post.body = request.POST.get("description") 
      post.save()
   
      return redirect('home') 
    
  else:
    return HttpResponse("<h3>This is noy your post! please try to your own post</h3>")
    
 
  context={'post':post}
  return render(request,'myapp/update_post.html',context)



@login_required(login_url='login')
def myAccount(request):
  user = request.user
  user_post = Post.objects.filter(author=user)
  context = {'posts':user_post}
  return render(request,'myapp/my_account.html', context)