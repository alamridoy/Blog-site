from django.urls import path
from myapp.views import *


urlpatterns = [
    path('',home, name='home' ),
    path('about/',about,name='about' ),
    path('post/<str:pk>',getPost, name='post_details'),
    path('post_delete/<str:pk>/delete', postDelete, name='post_delete'),
    path("create_post/",createPost, name="create_post"),
    path('post/<str:pk>/edit',updatePost,name='updatePost'),
    path('login/',loginUser,name='login'),
    path('logout/',logoutUser,name='logout'),
    path('signup/', registerUser,name='signup')
]
